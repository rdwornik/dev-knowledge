"""Witnesses for `scripts/memory_admission_gate.py` (LANE-5A-3, D7).

Four groups, per the done-contract's "Tests, red first" line: waits below reserve; slot
contention; `-n` computation; receipt shape. Every wait/sleep/clock/memory reading is injected
so these run in milliseconds and never touch the real machine's memory or the real clock --
the one test group that DOES touch real files is slot contention, because a `filelock.FileLock`
is the thing under test and a fake one would prove nothing about cross-process exclusion.
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

import memory_admission_gate as mag  # noqa: E402


def _config(**overrides) -> mag.GateConfig:
    base = dict(reserve_gb=2.0, per_worker_mb=500.0, slots=4, min_workers=1, max_workers=6,
               poll_interval_s=0.0, sample_interval_s=0.0, wait_timeout_s=None)
    base.update(overrides)
    return mag.GateConfig(**base)


def _incrementing_clock(step: float = 0.1):
    """A fake `clock_fn` that always moves forward by `step` -- avoids hand-counting how many
    times the code under test calls it, which a fixed-length sequence would require."""
    state = {"t": 0.0}

    def clock() -> float:
        t = state["t"]
        state["t"] = t + step
        return t

    return clock


# --------------------------------------------------------------------------- compute_workers

def test_compute_workers_low_memory_clamps_to_min():
    n = mag.compute_workers(2100.0, reserve_mb=2048.0, per_worker_mb=500.0,
                            min_workers=1, max_workers=6)
    assert n == 1


def test_compute_workers_high_memory_clamps_to_max():
    n = mag.compute_workers(200_000.0, reserve_mb=2048.0, per_worker_mb=500.0,
                            min_workers=1, max_workers=6)
    assert n == 6


def test_compute_workers_mid_range_is_read_off_the_budget():
    # budget = 2048 (free) - 1024 (reserve) = 1024 MB; 1024 // 256 = 4 workers.
    n = mag.compute_workers(2048.0, reserve_mb=1024.0, per_worker_mb=256.0,
                            min_workers=1, max_workers=6)
    assert n == 4


def test_compute_workers_never_reports_less_than_the_floor():
    n = mag.compute_workers(0.0, reserve_mb=2048.0, per_worker_mb=500.0,
                            min_workers=2, max_workers=6)
    assert n == 2


# ------------------------------------------------------------------------- wait_for_memory

def test_wait_for_memory_returns_immediately_when_already_clear():
    slept: list[float] = []
    result = mag.wait_for_memory(reserve_mb=1000.0, estimate_mb=500.0, poll_interval_s=1.0,
                                 free_mb_fn=lambda: 5000.0, sleep_fn=slept.append,
                                 clock_fn=_incrementing_clock())
    assert result.checks == 1
    assert slept == []  # never slept: admitted on the first reading


def test_wait_for_memory_polls_until_the_reserve_clears():
    readings = iter([500.0, 800.0, 3000.0])
    slept: list[float] = []
    result = mag.wait_for_memory(reserve_mb=1000.0, estimate_mb=1000.0, poll_interval_s=0.25,
                                 free_mb_fn=lambda: next(readings), sleep_fn=slept.append,
                                 clock_fn=_incrementing_clock(0.1))
    assert result.checks == 3
    assert slept == [0.25, 0.25]
    assert result.free_mb_final == 3000.0


def test_wait_for_memory_raises_on_timeout_and_never_admits_under_reserve():
    with pytest.raises(mag.MemoryGateTimeout):
        mag.wait_for_memory(reserve_mb=1000.0, estimate_mb=1000.0, poll_interval_s=0.1,
                            timeout_s=0.25, free_mb_fn=lambda: 100.0,
                            sleep_fn=lambda s: None, clock_fn=_incrementing_clock(0.1))


def test_wait_for_memory_with_no_timeout_polls_forever_until_admitted():
    readings = iter([100.0, 100.0, 100.0, 100.0, 5000.0])
    slept: list[float] = []
    result = mag.wait_for_memory(reserve_mb=1000.0, estimate_mb=1000.0, poll_interval_s=0.1,
                                 timeout_s=None, free_mb_fn=lambda: next(readings),
                                 sleep_fn=slept.append, clock_fn=_incrementing_clock(10.0))
    assert result.checks == 5
    assert len(slept) == 4  # never gave up despite elapsed clock racing past any typical timeout


# ----------------------------------------------------------------------------- acquire_slot

def test_acquire_slot_second_caller_waits_for_release(tmp_path):
    slot_a = mag.acquire_slot(slots=1, lock_dir=tmp_path, poll_interval_s=0.02)
    assert slot_a.slot_id == 0

    order: list[str] = []
    released_at = {}
    acquired_at = {}

    def release_a():
        time.sleep(0.1)
        order.append("release")
        released_at["t"] = time.monotonic()
        slot_a.release()

    def acquire_b():
        handle = mag.acquire_slot(slots=1, lock_dir=tmp_path, poll_interval_s=0.02)
        order.append("acquire")
        acquired_at["t"] = time.monotonic()
        handle.release()

    releaser = threading.Thread(target=release_a)
    acquirer = threading.Thread(target=acquire_b)
    releaser.start()
    acquirer.start()
    releaser.join(timeout=5)
    acquirer.join(timeout=5)

    assert order == ["release", "acquire"]
    assert acquired_at["t"] >= released_at["t"]


def test_acquire_slot_times_out_when_every_slot_is_held(tmp_path):
    held = mag.acquire_slot(slots=1, lock_dir=tmp_path, poll_interval_s=0.02)
    try:
        with pytest.raises(mag.MemoryGateTimeout):
            mag.acquire_slot(slots=1, lock_dir=tmp_path, poll_interval_s=0.02, timeout_s=0.1)
    finally:
        held.release()


def test_acquire_slot_picks_a_different_free_slot_without_waiting_for_slot_zero(tmp_path):
    slot0 = mag.acquire_slot(slots=2, lock_dir=tmp_path, poll_interval_s=0.02)
    assert slot0.slot_id == 0
    slot1 = mag.acquire_slot(slots=2, lock_dir=tmp_path, poll_interval_s=0.02, timeout_s=0.1)
    assert slot1.slot_id == 1
    slot0.release()
    slot1.release()


# -------------------------------------------------------------------------------- run_gated

def _stub_run(returncode: int = 0):
    calls: list[dict] = []

    def run(argv, cwd=None, **kwargs):
        calls.append({"argv": list(argv), "cwd": cwd, "kwargs": kwargs})
        return SimpleNamespace(returncode=returncode, stdout="", stderr="")

    run.calls = calls
    return run


def test_run_gated_disabled_flag_skips_both_gates_and_runs_verbatim(tmp_path):
    stub = _stub_run()
    result = mag.run_gated(
        ["echo", "hi"], disabled=True, config=_config(),
        receipt_path=tmp_path / "receipt.json",
        workers_flag="-n",  # must be IGNORED entirely under disabled -- old behaviour
        subprocess_run=stub,
    )
    assert result.gated is False
    assert result.waited_s == 0.0
    assert result.workers is None
    assert stub.calls[0]["argv"] == ["echo", "hi"]  # no -n appended


def test_run_gated_computes_and_appends_the_workers_flag(tmp_path):
    stub = _stub_run()
    cfg = _config(reserve_gb=1.0, per_worker_mb=250.0, min_workers=1, max_workers=6)
    # free 2048 MB - reserve 1024 MB = 1024 MB budget / 250 MB per worker = 4 workers.
    result = mag.run_gated(
        ["pytest"], config=cfg, workers_flag="-n",
        receipt_path=tmp_path / "receipt.json",
        lock_dir=tmp_path / "slots",
        free_mb_fn=lambda: 2048.0, used_mb_fn=lambda: 1000.0,
        sleep_fn=lambda s: None, clock_fn=_incrementing_clock(),
        subprocess_run=stub,
    )
    assert result.workers == 4
    assert stub.calls[0]["argv"] == ["pytest", "-n", "4"]


def test_run_gated_waits_when_below_reserve_then_runs(tmp_path):
    stub = _stub_run()
    cfg = _config(reserve_gb=1.0, per_worker_mb=250.0, poll_interval_s=0.01)
    readings = iter([500.0, 500.0, 2000.0])
    result = mag.run_gated(
        ["audit.py", "ship-gate"], config=cfg,
        receipt_path=tmp_path / "receipt.json",
        lock_dir=tmp_path / "slots",
        free_mb_fn=lambda: next(readings), used_mb_fn=lambda: 1000.0,
        sleep_fn=lambda s: None, clock_fn=_incrementing_clock(),
        subprocess_run=stub,
    )
    assert result.gated is True
    assert result.waited_s >= 0.0
    assert stub.calls[0]["argv"] == ["audit.py", "ship-gate"]  # no -n: no workers_flag given


def test_run_gated_writes_a_receipt_with_the_required_shape(tmp_path):
    stub = _stub_run(returncode=7)
    receipt = tmp_path / "receipt.json"
    result = mag.run_gated(
        ["pytest", "-x"], config=_config(), workers_flag="-n",
        receipt_path=receipt, lock_dir=tmp_path / "slots",
        free_mb_fn=lambda: 4096.0, used_mb_fn=lambda: 2000.0,
        sleep_fn=lambda s: None, clock_fn=_incrementing_clock(),
        subprocess_run=stub,
    )
    assert receipt.is_file()
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    for key in ("schema", "ran", "gated", "waited_s", "slot_id", "workers", "peak_used_mb",
               "returncode", "argv", "written_at"):
        assert key in payload, f"receipt missing {key!r}"
    assert payload["ran"] is True
    assert payload["gated"] is True
    assert payload["returncode"] == 7
    assert payload["slot_id"] == 0
    assert result.returncode == 7


def test_run_gated_samples_peak_memory_during_the_run(tmp_path):
    """A subprocess that takes measurable time must yield a peak reading -- and the reading
    is `used`, not `free`, because this gate protects headroom, not any one process's size."""
    readings = iter([1000.0, 4000.0, 2000.0])

    def slow_run(argv, cwd=None, **kwargs):
        time.sleep(0.05)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    result = mag.run_gated(
        ["sleep-ish"], config=_config(sample_interval_s=0.01),
        receipt_path=tmp_path / "receipt.json", lock_dir=tmp_path / "slots",
        free_mb_fn=lambda: 4096.0,
        used_mb_fn=lambda: next(readings, 2000.0),
        sleep_fn=lambda s: None, clock_fn=_incrementing_clock(),
        subprocess_run=slow_run,
    )
    assert result.peak_used_mb is not None
    assert result.peak_used_mb >= 1000.0


def test_run_gated_waited_s_includes_slot_wait_not_just_memory_wait(tmp_path):
    """`acquire_slot` has no return value to carry its own duration (unlike `wait_for_memory`),
    so a slot wait that costs real time must still show up in the receipt's `waited_s` --
    caught live during this lane's own development: the first cut of this function only
    summed `wait_for_memory`'s `waited_s`, so a two-process slot-contention proof reported
    `waited_s: 0.0` on the process that visibly waited several seconds for the slot."""
    lock_dir = tmp_path / "slots"
    held = mag.acquire_slot(slots=1, lock_dir=lock_dir, poll_interval_s=0.01)

    slept: list[float] = []

    def sleep_then_release(seconds: float) -> None:
        slept.append(seconds)
        if len(slept) == 3:  # release the slot on the third poll so the caller below waits
            held.release()

    stub = _stub_run()
    result = mag.run_gated(
        ["pytest"], config=_config(slots=1, poll_interval_s=0.01), receipt_path=tmp_path / "r.json",
        lock_dir=lock_dir, free_mb_fn=lambda: 4096.0, used_mb_fn=lambda: 1000.0,
        sleep_fn=sleep_then_release, clock_fn=_incrementing_clock(0.5), subprocess_run=stub,
    )
    assert result.waited_s > 0.0
    assert len(slept) >= 3  # actually contended for the slot before acquiring it


def test_run_gated_releases_the_slot_even_when_the_command_raises(tmp_path):
    def raising_run(argv, cwd=None, **kwargs):
        raise subprocess.TimeoutExpired(cmd=argv, timeout=1)

    lock_dir = tmp_path / "slots"
    with pytest.raises(subprocess.TimeoutExpired):
        mag.run_gated(
            ["pytest"], config=_config(slots=1), receipt_path=tmp_path / "receipt.json",
            lock_dir=lock_dir, free_mb_fn=lambda: 4096.0, used_mb_fn=lambda: 1000.0,
            sleep_fn=lambda s: None, clock_fn=_incrementing_clock(),
            subprocess_run=raising_run,
        )
    # the slot must be free again -- a second acquisition must not time out.
    handle = mag.acquire_slot(slots=1, lock_dir=lock_dir, poll_interval_s=0.01, timeout_s=1.0)
    handle.release()


# ---------------------------------------------------------------------------------- config

def test_load_config_falls_back_to_defaults_when_the_file_is_missing(tmp_path):
    cfg = mag.load_config(tmp_path / "does-not-exist.yaml")
    assert cfg.reserve_gb == mag._DEFAULTS.reserve_gb
    assert cfg.slots == mag._DEFAULTS.slots


def test_load_config_reads_the_shipped_yaml():
    cfg = mag.load_config()
    assert cfg.reserve_gb > 0
    assert cfg.per_worker_mb > 0
    assert cfg.slots >= 1
    assert cfg.min_workers >= 1
    assert cfg.max_workers >= cfg.min_workers
