"""Witnesses for scripts/hooks/quota_daily.py -- the SessionStart trigger for quota_watch.py
(LANE-5B3-2-wire-quota-distiller, Done-contract item 2).

Four claims, one test class each: SKIP when a read already exists for today; FIRE (claim +
spawn a detached worker) when it does not; ERROR fails open (a guard-level exception and a
worker that cannot start both still return 0); BUDGET -- p95 of >= 10 runs stays under the
contract's 2s figure in both the skip and fire paths.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.hooks import quota_daily as qd  # noqa: E402


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _write_ledger_row(repo_root: Path, measured: str) -> None:
    ledger = repo_root / "logs" / "QUOTA-READS.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    row = {"group": "codespaces_core_hours", "cycle": "2026-09-01", "used": 1.0,
          "quota": 180.0, "pct": 0.01, "billed": False, "measured": measured}
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")


class _RefusingLaneEndGuard:
    """A spy that fails the test if the guard ever reaches a spawn on the skip path."""

    @staticmethod
    def spawn_worker(argv, cwd, env):  # pragma: no cover -- must never be called
        raise AssertionError("spawn_worker must not be called on the skip path")


class _FakeLaneEndGuard:
    def __init__(self):
        self.calls = []

    def spawn_worker(self, argv, cwd, env):
        self.calls.append(argv)
        return True


class _BrokenLaneEndGuard:
    @staticmethod
    def spawn_worker(argv, cwd, env):
        raise OSError("no interpreter")


# --- skip -------------------------------------------------------------------

def test_skip_when_a_read_exists_today(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    _write_ledger_row(tmp_path, f"{_today()}T10:00:00+00:00")
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: _RefusingLaneEndGuard)

    assert qd.main([]) == 0
    assert "skip" in capsys.readouterr().out.lower()
    assert not (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).exists()


def test_does_not_skip_on_a_prior_days_read(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    _write_ledger_row(tmp_path, "2020-01-01T10:00:00+00:00")
    fake = _FakeLaneEndGuard()
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: fake)

    assert qd.main([]) == 0
    assert len(fake.calls) == 1


# --- fire ---------------------------------------------------------------------

def test_fire_spawns_a_detached_worker_when_no_read_today(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    fake = _FakeLaneEndGuard()
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: fake)

    assert qd.main([]) == 0

    assert len(fake.calls) == 1
    assert fake.calls[0][-1] == qd._PRODUCER_FLAG
    claim = json.loads(
        (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).read_text(encoding="utf-8"))
    assert claim["status"] == "running"
    assert claim["date"] == _today()


def test_fire_claims_only_once_across_two_calls_in_the_same_window(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    fake = _FakeLaneEndGuard()
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: fake)

    qd.main([])
    qd.main([])

    assert len(fake.calls) == 1


def test_stale_running_claim_is_reaped_and_retried(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    claim_path = qd._claim_path(tmp_path)
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim_path.write_text(json.dumps({"status": "running", "date": _today()}), encoding="utf-8")
    old = time.time() - qd._CLAIM_STALE_S - 60
    os.utime(claim_path, (old, old))
    fake = _FakeLaneEndGuard()
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: fake)

    assert qd.main([]) == 0
    assert len(fake.calls) == 1


# --- error, fails open ---------------------------------------------------------

def test_unreadable_ledger_fails_open(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    ledger = tmp_path / "logs" / "QUOTA-READS.jsonl"
    ledger.mkdir(parents=True)  # a directory where a file is expected -> read raises

    assert qd.main([]) == 0
    assert "guard error" in capsys.readouterr().out.lower()


def test_a_worker_that_cannot_start_still_returns_0_and_records_failed(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: _BrokenLaneEndGuard)

    assert qd.main([]) == 0

    claim = json.loads(
        (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).read_text(encoding="utf-8"))
    assert claim["status"] == "FAILED"
    assert "could not start the worker" in claim["reason"]


def test_a_worker_that_could_not_break_away_is_treated_as_failed(tmp_path, monkeypatch):
    """Codex terra HIGH, 2026-09-26: `spawn_worker` returning False means the worker is
    still inside this hook's own job and can die with it -- that must not be read as a
    successful spawn, or a `running` claim could sit unreaped for `_CLAIM_STALE_S`."""
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)

    class _NonBreakawayLaneEndGuard:
        @staticmethod
        def spawn_worker(argv, cwd, env):
            return False

    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: _NonBreakawayLaneEndGuard)

    assert qd.main([]) == 0

    claim = json.loads(
        (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).read_text(encoding="utf-8"))
    assert claim["status"] == "FAILED"
    assert "break" in claim["reason"].lower()


def test_run_producer_records_failed_on_timeout(tmp_path, monkeypatch):
    """Codex terra HIGH, 2026-09-26: the producer's `subprocess.run` must be bounded, and a
    timeout must still leave a terminal claim result rather than none at all."""
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)

    import subprocess as _subprocess

    def _fake_run(*args, **kwargs):
        assert kwargs.get("timeout") == qd._PRODUCER_TIMEOUT_S
        raise _subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])

    monkeypatch.setattr(qd.subprocess, "run", _fake_run)

    assert qd.run_producer(tmp_path) == 1

    claim = json.loads(
        (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).read_text(encoding="utf-8"))
    assert claim["status"] == "FAILED"
    assert "timeout" in claim["reason"].lower()


def test_run_producer_records_failed_when_the_subprocess_cannot_launch(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)

    def _fake_run(*args, **kwargs):
        raise OSError("no interpreter")

    monkeypatch.setattr(qd.subprocess, "run", _fake_run)

    assert qd.run_producer(tmp_path) == 1

    claim = json.loads(
        (tmp_path / "logs" / "receipts" / qd._CLAIM_NAME).read_text(encoding="utf-8"))
    assert claim["status"] == "FAILED"
    assert "could not launch" in claim["reason"].lower()


# --- budget: p95 of >= 10 runs, both paths --------------------------------------

def _p95(samples):
    ordered = sorted(samples)
    idx = max(0, int(round(0.95 * (len(ordered) - 1))))
    return ordered[idx]


def test_skip_path_budget_p95_under_2s(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    _write_ledger_row(tmp_path, f"{_today()}T10:00:00+00:00")
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: _RefusingLaneEndGuard)

    times = []
    for _ in range(10):
        start = time.perf_counter()
        assert qd.main([]) == 0
        times.append(time.perf_counter() - start)

    assert _p95(times) < 2.0, f"skip path p95={_p95(times):.3f}s over {times}"


def test_fire_path_budget_p95_under_2s(tmp_path, monkeypatch):
    monkeypatch.setattr(qd, "_REPO_ROOT", tmp_path)
    fake = _FakeLaneEndGuard()
    monkeypatch.setattr(qd, "_import_lane_end_guard", lambda: fake)
    claim_path = qd._claim_path(tmp_path)

    times = []
    for _ in range(10):
        if claim_path.exists():
            claim_path.unlink()
        start = time.perf_counter()
        assert qd.main([]) == 0
        times.append(time.perf_counter() - start)

    assert len(fake.calls) == 10
    assert _p95(times) < 2.0, f"fire path p95={_p95(times):.3f}s over {times}"
