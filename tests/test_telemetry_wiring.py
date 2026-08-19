"""Tests for the [#529] `check_run` wiring at `audit.run_checks` — lane L2, contract STEP 2.

WHAT IS ACTUALLY AT RISK, and it is not "does an event appear". Three things:

  * **The findings must not move.** `run_checks` feeds the `audit-health` pre-commit gate and
    the `ship-gate` verdict, and `CHECK_ORDER` is part of the byte-identical output contract the
    git hooks read. Telemetry is an observer; a wired runner that returns one different finding
    has broken the gate mesh to measure it. `test_findings_are_byte_identical_with_telemetry_on`
    is the load-bearing case here, and it mirrors `test_audit_parallel.py`'s serial-vs-parallel
    parity rather than inventing a second idea of what "identical" means.

  * **The store must land where the CALLER said.** `telemetry_emit._REPO_ROOT` and
    `audit._REPO_ROOT` are independent module-level values, so monkeypatching the one the whole
    suite already patches does NOT redirect `telemetry_emit.default_db_path()`. A wired gate that
    relied on the default would write into the REAL `logs/` on every suite run while
    `tests/test_ship_gate.py::test_ship_gate_is_readonly` kept passing — a seam that detaches
    silently, which is the failure class `audit_checks/registry.py` documents.
    `test_the_store_lands_under_the_callers_repo_root_not_the_librarys` is the regression test.

  * **stderr must stay clean.** `audit.py` calls `logging.basicConfig(level=INFO)` at module
    scope and `telemetry_emit._log_event` logs each event at INFO, so an unguarded wiring adds
    one `telemetry: {...}` line per check — 43 per run, on a gate that fires on every commit.
    Measured, not hypothetical. The existing hook tests assert stderr SUBSTRINGS, which survive
    extra output, so this property cannot be delegated to them and needs its own case.

Every case passes an explicit `db_path` (or asserts where the derived one landed), which is also
what proves the wiring honours the explicit-path rule rather than merely happening to work.

`tests/test_audit.py` is untouched by this lane (the seam leg's file) and
`tests/test_audit_parallel.py` must stay green UNEDITED, so everything new lives here.
"""
from __future__ import annotations

import json
import logging
import sqlite3
import threading
from pathlib import Path

import pytest
from click.testing import CliRunner

import audit as aud
import telemetry_emit as te


# --- helpers ------------------------------------------------------------------------------

def _make_check(name: str, delay: float = 0.0, n_findings: int = 1, status: str = "pass"):
    """A stand-in check: sleeps, records its thread, emits `n_findings` findings.

    Deliberately the same shape as `tests/test_audit_parallel.py::_make_check` — the two files
    test the same function and a second, subtly different stand-in would let them disagree about
    what a check IS.
    """
    import time

    def _check(_repo):
        if delay:
            time.sleep(delay)
        _check.threads.append(threading.current_thread().name)
        return [aud.Finding(name, status, f"{name} finding {i}") for i in range(n_findings)]
    _check.__name__ = name
    _check.threads = []
    return _check


def _raising_check(name: str, exc: Exception):
    def _check(_repo):
        raise exc
    _check.__name__ = name
    return _check


def _rows(db_path):
    """Every event in the store, in insertion order — read back, never inferred."""
    with sqlite3.connect(str(db_path)) as conn:
        cur = conn.execute(
            "SELECT event_type, name, outcome, duration_ms, context_json FROM events ORDER BY id")
        return [dict(zip(("event_type", "name", "outcome", "duration_ms", "context_json"), r))
                for r in cur.fetchall()]


def _fields(findings):
    """The full content of each finding — what "byte-identical" means here."""
    return [(f.check_name, f.status, f.evidence) for f in findings]


@pytest.fixture(autouse=True)
def _no_ambient_telemetry_env(monkeypatch):
    """Neither switch may leak in from the host shell.

    `DEV_KNOWLEDGE_TELEMETRY` would turn emission on under a test asserting it is off, and
    `DEV_KNOWLEDGE_TELEMETRY_DB` would redirect the store out from under the path assertions —
    both would make this file's verdict depend on whose machine ran it.
    """
    monkeypatch.delenv(aud.TELEMETRY_ENV, raising=False)
    monkeypatch.delenv(te.DB_PATH_ENV, raising=False)


# --- case 1: emission happens -------------------------------------------------------------

def test_a_wired_run_emits_one_check_run_per_check(tmp_path):
    db = tmp_path / "T.db"
    checks = [_make_check("c1"), _make_check("c2")]
    aud.run_checks(tmp_path, checks=checks, telemetry=True, telemetry_db=db)

    rows = _rows(db)
    assert [r["event_type"] for r in rows] == ["check_run", "check_run"]
    assert [r["name"] for r in rows] == ["c1", "c2"]


# --- case 2: parity — the load-bearing one ------------------------------------------------

@pytest.mark.parametrize("parallel", [False, True])
def test_findings_are_byte_identical_with_telemetry_on(tmp_path, parallel):
    """Telemetry is an OBSERVER. Findings returned with it on are field-by-field what they were
    with it off, in both modes. This is the property that keeps `audit-health` and `ship-gate`
    reading the same bytes they read before the wiring landed."""
    def _checks():
        return [_make_check("a", n_findings=2), _make_check("b"), _make_check("c", n_findings=3)]

    off = aud.run_checks(tmp_path, checks=_checks(), parallel=parallel, workers=3)
    on = aud.run_checks(tmp_path, checks=_checks(), parallel=parallel, workers=3,
                        telemetry=True, telemetry_db=tmp_path / "T.db")
    assert _fields(on) == _fields(off)


# --- case 3: emission order is registry order ---------------------------------------------

def test_emission_order_is_registry_order_even_when_completion_order_is_reversed(tmp_path):
    """Delays descend, so the check submitted FIRST finishes LAST. An emitter that fired inside
    the worker would record completion order; one that walks the flattened slots records registry
    order. The same worst-case construction `test_audit_parallel.py` uses for the findings."""
    db = tmp_path / "T.db"
    checks = [_make_check(f"c{i}", delay=(6 - i) * 0.05) for i in range(6)]
    aud.run_checks(tmp_path, checks=checks, parallel=True, workers=6,
                   telemetry=True, telemetry_db=db)

    assert [r["name"] for r in _rows(db)] == ["c0", "c1", "c2", "c3", "c4", "c5"]


# --- case 4: one row per check per run, including a check with no findings -----------------

def test_a_check_that_returns_no_findings_still_emits_a_row(tmp_path):
    """A check that found nothing still RAN, and "fires>0/blocks=0" is exactly the memo's
    retire-this-check question — so a zero-finding check must not vanish from the record. This is
    also why the event `name` is the check's `__name__`: a check with no findings has no
    `Finding.check_name` to borrow."""
    db = tmp_path / "T.db"
    checks = [_make_check("loud", n_findings=2), _make_check("silent", n_findings=0)]
    aud.run_checks(tmp_path, checks=checks, telemetry=True, telemetry_db=db)

    rows = _rows(db)
    assert [r["name"] for r in rows] == ["loud", "silent"]
    assert json.loads(rows[1]["context_json"])["findings"] == 0


# --- case 5: a multi-finding check emits ONE event with the aggregate ----------------------

def test_a_multi_finding_check_emits_one_event_carrying_the_aggregate(tmp_path):
    """The organ being measured is the CHECK, not the finding. N events for one check would
    inflate every per-check count by however many findings that check happens to emit."""
    db = tmp_path / "T.db"

    def _mixed(_repo):
        return [aud.Finding("m", "pass", "ok"),
                aud.Finding("m", "warn", "drifting"),
                aud.Finding("m", "warn", "also drifting")]
    _mixed.__name__ = "mixed"

    aud.run_checks(tmp_path, checks=[_mixed], telemetry=True, telemetry_db=db)

    rows = _rows(db)
    assert len(rows) == 1
    ctx = json.loads(rows[0]["context_json"])
    assert ctx["statuses"] == {"pass": 1, "warn": 2}
    assert ctx["findings"] == 3
    assert ctx["finding_names"] == ["m"]


def test_a_fail_maps_to_block_and_everything_non_fail_maps_to_pass(tmp_path):
    """The STEP-1 mapping, pinned. `emit_event` REFUSES an unknown outcome and `safe_emit`
    deliberately does not swallow `TelemetryError`, so a drifting mapping would crash the audit
    rather than degrade — which is why this is a test and not a comment."""
    db = tmp_path / "T.db"
    checks = [_make_check("p", status="pass"), _make_check("w", status="warn"),
              _make_check("na", status="n/a"), _make_check("u", status="unavailable"),
              _make_check("f", status="fail")]
    aud.run_checks(tmp_path, checks=checks, telemetry=True, telemetry_db=db)

    assert {r["name"]: r["outcome"] for r in _rows(db)} == {
        "p": "pass", "w": "pass", "na": "pass", "u": "pass", "f": "block"}


# --- case 6: duration_ms is the check's own time, not its queue wait -----------------------

def test_duration_is_the_checks_own_time_not_its_queue_wait(tmp_path):
    """With ONE worker the second check waits for the first, so timing taken around
    `future.result()` would bill it for the whole queue and report a fabricated `duration_ms`.
    Timing must sit around `check(repo_path)` INSIDE the worker."""
    db = tmp_path / "T.db"
    checks = [_make_check("slow", delay=0.6), _make_check("quick", delay=0.0)]
    aud.run_checks(tmp_path, checks=checks, parallel=True, workers=1,
                   telemetry=True, telemetry_db=db)

    rows = {r["name"]: r["duration_ms"] for r in _rows(db)}
    assert rows["slow"] >= 500
    assert rows["quick"] < 300, (
        f"quick was billed {rows['quick']}ms — that is the slow check's queue wait, "
        "so the timer is around future.result() rather than around the check")


# --- case 7: a dead store never breaks the run --------------------------------------------

def test_an_unwritable_store_never_breaks_the_run(tmp_path):
    """`safe_emit` at work: a locked database or a read-only disk must not turn a green gate
    into a failed commit. The store's parent is a regular FILE here, so `connect()`'s
    `mkdir(parents=True)` raises `OSError` — the class `safe_emit` swallows."""
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x\n", encoding="utf-8")

    checks = [_make_check("c1"), _make_check("c2")]
    out = aud.run_checks(tmp_path, checks=checks, telemetry=True,
                         telemetry_db=blocker / "nested" / "T.db")

    assert _fields(out) == _fields(aud.run_checks(tmp_path, checks=[_make_check("c1"),
                                                                   _make_check("c2")]))


# --- case 8: a worker exception still propagates ------------------------------------------

@pytest.mark.parametrize("parallel", [False, True])
def test_an_exception_still_propagates_with_telemetry_on(tmp_path, parallel):
    """`test_audit_parallel.py::test_an_exception_in_a_worker_propagates_and_is_never_swallowed`
    must not be weakened by the wiring. A runner that swallowed a crash to finish its bookkeeping
    would turn a loud failure into a silently short report — the worst outcome an audit has."""
    db = tmp_path / "T.db"
    checks = [_raising_check("boom", RuntimeError("check exploded"))]

    with pytest.raises(RuntimeError, match="check exploded"):
        aud.run_checks(tmp_path, checks=checks, parallel=parallel, workers=2,
                       telemetry=True, telemetry_db=db)


def test_a_raising_check_is_recorded_as_an_error_before_it_propagates(tmp_path):
    """`error` is the third `OUTCOMES` value precisely because a crashed check is neither a pass
    nor a block. Recording it is what makes a crash countable instead of merely loud."""
    db = tmp_path / "T.db"
    with pytest.raises(RuntimeError):
        aud.run_checks(tmp_path, checks=[_raising_check("boom", RuntimeError("x"))],
                       telemetry=True, telemetry_db=db)

    rows = _rows(db)
    assert [(r["name"], r["outcome"]) for r in rows] == [("boom", "error")]
    assert "RuntimeError" in json.loads(rows[0]["context_json"])["error"]


# --- case 9: OFF is the default, and off means zero rows -----------------------------------

def test_telemetry_is_off_by_default_and_off_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    aud.run_checks(tmp_path, checks=[_make_check("c1")])
    assert not (tmp_path / "logs").exists()


def test_the_default_is_a_named_constant_not_an_inline_literal():
    """Mirrors `test_audit_parallel.py::test_the_worker_cap_is_a_named_constant_not_an_inline_literal`.
    The architect's config-surface ruling for this lane is "named module constant + click option
    + env-var switch" — the constant is the part a reader can find and an operator can argue
    with, so its existence is asserted rather than assumed."""
    assert aud._TELEMETRY_DEFAULT is False
    assert aud.TELEMETRY_ENV == "DEV_KNOWLEDGE_TELEMETRY"


def test_health_exposes_the_telemetry_flag_and_defaults_to_off(tmp_path, monkeypatch):
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(aud, "ALL_CHECKS", [_make_check("sentinel")])

    res = CliRunner().invoke(aud.cmd_health)
    assert res.exit_code == 0, res.output
    assert not (tmp_path / "logs").exists()

    res = CliRunner().invoke(aud.cmd_health, ["--telemetry"])
    assert res.exit_code == 0, res.output
    assert [r["name"] for r in _rows(tmp_path / "logs" / "TELEMETRY.db")] == ["sentinel"]


def test_the_env_switch_turns_health_on_and_the_explicit_flag_still_wins(tmp_path, monkeypatch):
    """The hooks have no click layer, so the env var is how `audit-health` can ever be turned on
    in a hook context. An explicit `--no-telemetry` must still beat it — otherwise an operator
    could not turn emission off for one run without editing their environment."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(aud, "ALL_CHECKS", [_make_check("sentinel")])
    monkeypatch.setenv(aud.TELEMETRY_ENV, "1")

    assert CliRunner().invoke(aud.cmd_health).exit_code == 0
    assert len(_rows(tmp_path / "logs" / "TELEMETRY.db")) == 1

    assert CliRunner().invoke(aud.cmd_health, ["--no-telemetry"]).exit_code == 0
    assert len(_rows(tmp_path / "logs" / "TELEMETRY.db")) == 1  # unchanged: the flag won


# --- case 10: stderr stays clean ----------------------------------------------------------

def test_a_wired_health_run_puts_no_telemetry_line_on_stderr(tmp_path, monkeypatch, capfd):
    """The regression test for the MEASURED `audit.py:283` finding.

    `basicConfig(format="%(name)s: %(message)s", level=INFO)` runs at `audit` import and
    `_log_event` logs at INFO to logger `"telemetry"`, whose default stream is stderr. Wiring
    without the caller-side quieting adds one `telemetry: {...}` line per check to a per-commit
    gate. Asserted on real captured output, at fd level, because that is where the handler writes.
    """
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(aud, "ALL_CHECKS", [_make_check("c1"), _make_check("c2")])
    capfd.readouterr()  # drop anything collection left behind

    res = CliRunner().invoke(aud.cmd_health, ["--telemetry"])
    captured = capfd.readouterr()

    assert res.exit_code == 0, res.output
    assert len(_rows(tmp_path / "logs" / "TELEMETRY.db")) == 2  # it really did emit
    assert "telemetry: " not in captured.err
    assert "telemetry: " not in captured.out
    assert "telemetry: " not in res.output


def test_the_quieting_is_caller_side_and_leaves_the_library_untouched():
    """The fix belongs to `audit.py`, not to `telemetry_emit`. Fixing it in the library would
    touch `test_emit_survives_an_unusable_log_side_channel` and
    `test_logger_backend_reports_which_side_channel_is_live` — pinned tests, for a defect the
    library does not have: a hook that imports only `telemetry_emit` has no handler configured,
    so `logging.lastResort` (WARNING) already keeps its stderr byte-clean (measured)."""
    assert logging.getLogger("telemetry").level >= logging.WARNING
    assert te.logger_backend() in {"stdlib-logging", "structlog"}


# --- case 11: the store lands where the caller said ---------------------------------------

def test_the_store_lands_under_the_callers_repo_root_not_the_librarys(tmp_path, monkeypatch):
    """The regression test for the seam finding.

    `telemetry_emit.default_db_path()` reads `telemetry_emit._REPO_ROOT`, which no test patches;
    `audit._REPO_ROOT` is a different value and is one of the 25 names the suite DOES patch. A
    wiring that leaned on the default would write into the real repo on every suite run while
    every sandbox assertion kept passing. The derived path must follow the caller's root.
    """
    real_store = Path(te._REPO_ROOT) / te.DEFAULT_DB_RELPATH
    real_existed = real_store.exists()
    real_before = real_store.stat().st_mtime_ns if real_existed else None

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    aud.run_checks(tmp_path, checks=[_make_check("c1")], telemetry=True)

    assert [r["name"] for r in _rows(tmp_path / "logs" / "TELEMETRY.db")] == ["c1"]
    assert real_store.exists() == real_existed, (
        f"the wiring created the LIBRARY's default store at {real_store} — the caller's "
        "explicit path is not being honoured")
    if real_existed:
        assert real_store.stat().st_mtime_ns == real_before


def test_the_operator_env_override_still_relocates_the_store(tmp_path, monkeypatch):
    """`DEV_KNOWLEDGE_TELEMETRY_DB` stays the operator/sandbox override. Deriving the default
    from the caller's root must not silently disable it — that env var is how a hook subprocess
    in a test gets pointed at a tmp store."""
    elsewhere = tmp_path / "elsewhere" / "T.db"
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv(te.DB_PATH_ENV, str(elsewhere))

    aud.run_checks(tmp_path, checks=[_make_check("c1")], telemetry=True)

    assert [r["name"] for r in _rows(elsewhere)] == ["c1"]
    assert not (tmp_path / "logs").exists()


# --- the runner's existing contract, re-asserted with telemetry ON -------------------------

def test_serial_with_telemetry_on_still_runs_on_the_calling_thread(tmp_path):
    """`test_audit_parallel.py::test_the_default_is_serial_and_runs_on_the_calling_thread` pins
    that the default puts no work on a thread. Emission must not smuggle one in."""
    check = _make_check("c1")
    aud.run_checks(tmp_path, checks=[check], telemetry=True, telemetry_db=tmp_path / "T.db")
    assert check.threads == [threading.main_thread().name]
