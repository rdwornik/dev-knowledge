"""Tests for `audit.run_checks` — the serial/parallel check runner ([#533] leg 2, STEP 4/5).

WHAT IS ACTUALLY AT RISK. `CHECK_ORDER` is load-bearing: it is the order findings are emitted
in, and therefore part of the byte-identical output contract the git hooks read. A thread pool
completes work in whatever order the OS hands back, so the one thing a parallel runner can
silently destroy is exactly the thing that must not move. Every test here exists to make that
impossible to break quietly:

  * completion order is deliberately made the REVERSE of registry order (descending sleeps), so
    a runner that emits in completion order fails loudly instead of passing by luck on a machine
    where the checks happen to finish in the order they were submitted;
  * a check emitting SEVERAL findings must keep them contiguous and in its own slot, which is
    the failure a naive `as_completed` + `extend` produces;
  * serial and parallel are compared field-by-field on real checks against the live tree, not
    just on synthetic ones.

DEFAULT IS SERIAL, and one test pins that by observing the thread each check runs on. Flipping
the hook's default is explicitly a separate ruling, not this lane's, so "the default did not
move" is a property worth a test rather than a comment.

`tests/test_audit.py` is untouched by this leg; its 25 monkeypatch seams belong to the seam leg.
This file reaches `audit` by bare name (the repo's Shape B import substrate) and monkeypatches
only `ALL_CHECKS`, which is a seam that file already relies on.
"""
from __future__ import annotations

import threading
import time

import pytest
from click.testing import CliRunner

import audit as aud
from audit_checks.registry import CHECK_ORDER


# --- synthetic checks: order is knowable, timing is controllable -------------------------

def _make_check(name: str, delay: float = 0.0, n_findings: int = 1):
    """A stand-in check that sleeps, records its thread, and emits `n_findings` findings."""
    def _check(_repo):
        if delay:
            time.sleep(delay)
        _check.threads.append(threading.current_thread().name)
        return [aud.Finding(name, "pass", f"{name} finding {i}") for i in range(n_findings)]
    _check.__name__ = name
    _check.threads = []
    return _check


def _names(findings):
    return [f.check_name for f in findings]


def _fields(findings):
    """The full byte content of each finding — the comparison that "byte-identical" means."""
    return [(f.check_name, f.status, f.evidence) for f in findings]


# --- emission order ----------------------------------------------------------------------

def test_parallel_emits_in_registry_order_even_when_completion_order_is_reversed(tmp_path):
    """The load-bearing property, tested against the worst case rather than the average one.

    Delays descend, so the check registered FIRST finishes LAST. A runner that emits as work
    completes returns the exact reverse of the required order; a runner that emits in registry
    order is unaffected. With enough workers to hold every check at once, this is deterministic
    rather than a race the test hopes to win.
    """
    checks = [_make_check(f"c{i}", delay=(6 - i) * 0.05) for i in range(6)]
    out = aud.run_checks(tmp_path, checks=checks, parallel=True, workers=6)
    assert _names(out) == ["c0", "c1", "c2", "c3", "c4", "c5"]


def test_parallel_is_byte_identical_to_serial_on_synthetic_checks(tmp_path):
    checks = [_make_check(f"c{i}", delay=(6 - i) * 0.02, n_findings=1 + i % 3) for i in range(6)]
    serial = aud.run_checks(tmp_path, checks=checks, parallel=False)
    parallel = aud.run_checks(tmp_path, checks=checks, parallel=True, workers=6)
    assert _fields(parallel) == _fields(serial)


def test_a_multi_finding_check_keeps_its_findings_contiguous_and_in_its_own_slot(tmp_path):
    """The specific corruption an `as_completed` + `extend` runner produces.

    Interleaved findings would still contain the right SET, so a test that only compared sorted
    contents would pass while the emitted report was scrambled.
    """
    checks = [_make_check("first", delay=0.15, n_findings=3),
              _make_check("second", delay=0.0, n_findings=2),
              _make_check("third", delay=0.05, n_findings=1)]
    out = aud.run_checks(tmp_path, checks=checks, parallel=True, workers=3)
    assert _names(out) == ["first", "first", "first", "second", "second", "third"]
    assert [f.evidence for f in out[:3]] == [f"first finding {i}" for i in range(3)]


def test_every_check_runs_exactly_once(tmp_path):
    checks = [_make_check(f"c{i}", delay=0.01) for i in range(8)]
    aud.run_checks(tmp_path, checks=checks, parallel=True, workers=4)
    assert [len(c.threads) for c in checks] == [1] * 8


def test_a_check_returning_no_findings_occupies_no_slot(tmp_path):
    checks = [_make_check("a", n_findings=1), _make_check("b", n_findings=0),
              _make_check("c", n_findings=1)]
    out = aud.run_checks(tmp_path, checks=checks, parallel=True, workers=3)
    assert _names(out) == ["a", "c"]


def test_an_empty_registry_is_not_an_error(tmp_path):
    assert aud.run_checks(tmp_path, checks=[], parallel=True) == []
    assert aud.run_checks(tmp_path, checks=[], parallel=False) == []


# --- the default must not move -----------------------------------------------------------

def test_the_default_is_serial_and_runs_on_the_calling_thread(tmp_path):
    """Pins the contract that this lane does NOT change what any hook does.

    Observed on the thread each check actually ran on, because that is the difference that
    matters; a flag's default value can be read from a signature, but "no worker thread was
    involved" is the claim being made to the operator.
    """
    checks = [_make_check(f"c{i}") for i in range(3)]
    aud.run_checks(tmp_path, checks=checks)
    assert all(c.threads == [threading.main_thread().name] for c in checks)


def test_explicit_parallel_actually_uses_worker_threads(tmp_path):
    """The converse -- otherwise `parallel=True` could be a no-op and every test above
    would still pass while measuring nothing."""
    checks = [_make_check(f"c{i}", delay=0.05) for i in range(4)]
    aud.run_checks(tmp_path, checks=checks, parallel=True, workers=4)
    used = {t for c in checks for t in c.threads}
    assert threading.main_thread().name not in used
    assert len(used) > 1


# --- worker count is configuration, never a literal --------------------------------------

def test_the_default_worker_count_is_the_configured_cap_against_the_check_count():
    assert aud._parallel_workers(100) == aud._PARALLEL_MAX_WORKERS
    assert aud._parallel_workers(3) == 3
    assert aud._parallel_workers(aud._PARALLEL_MAX_WORKERS) == aud._PARALLEL_MAX_WORKERS


def test_the_worker_cap_is_a_named_constant_not_an_inline_literal():
    assert isinstance(aud._PARALLEL_MAX_WORKERS, int)
    assert aud._PARALLEL_MAX_WORKERS >= 1


def test_a_zero_check_run_still_asks_for_at_least_one_worker():
    """`ThreadPoolExecutor(max_workers=0)` raises; the guard belongs in the helper."""
    assert aud._parallel_workers(0) >= 1


def test_an_explicit_worker_count_is_honoured(tmp_path):
    checks = [_make_check(f"c{i}", delay=0.05) for i in range(6)]
    aud.run_checks(tmp_path, checks=checks, parallel=True, workers=2)
    used = {t for c in checks for t in c.threads}
    assert len(used) <= 2


# --- failure posture ---------------------------------------------------------------------

def test_an_exception_in_a_worker_propagates_and_is_never_swallowed(tmp_path):
    """A parallel runner that turned a raising check into a missing result would convert a
    loud failure into a silently short report -- the worst outcome available to an audit."""
    def _boom(_repo):
        raise RuntimeError("check exploded")

    checks = [_make_check("ok"), _boom]
    with pytest.raises(RuntimeError, match="check exploded"):
        aud.run_checks(tmp_path, checks=checks, parallel=True, workers=2)
    with pytest.raises(RuntimeError, match="check exploded"):
        aud.run_checks(tmp_path, checks=checks, parallel=False)


# --- the registry the ordering contract is defined against -------------------------------

def test_check_order_still_agrees_with_all_checks():
    """Closes the honest limit `audit_checks/registry.py` states about itself.

    Its docstring records that "nothing currently asserts that CHECK_ORDER still agrees with
    audit.ALL_CHECKS" and that the guard belongs in `tests/`. The parallel runner's whole
    ordering contract is stated in terms of registry order, so that agreement stops being
    documentation and becomes a precondition of this leg being correct.
    """
    assert tuple(c.__name__ for c in aud.ALL_CHECKS) == CHECK_ORDER


def test_run_checks_defaults_to_the_live_registry(tmp_path, monkeypatch):
    """`checks=None` must read `ALL_CHECKS` off the module AT CALL TIME.

    Capturing it as a default argument would silently detach the seam that
    `tests/test_audit.py` monkeypatches -- a check that still passes while testing nothing,
    which is the exact class `audit_checks/registry.py` warns about.
    """
    sentinel = _make_check("sentinel")
    monkeypatch.setattr(aud, "ALL_CHECKS", [sentinel])
    assert _names(aud.run_checks(tmp_path)) == ["sentinel"]


# --- real checks against the live tree ---------------------------------------------------

# The sub-0.1s members measured in STEP-1 attribution. Named rather than sliced so the set is
# stable if CHECK_ORDER changes, and kept cheap so this stays a test and not a second audit run.
_CHEAP = (
    "check_vision_md", "check_adr38_baseline", "check_claude_md",
    "check_dot_prefix_discipline", "check_canonical_md_visibility",
    "check_workspace_settings", "check_handoff_bundle_structure",
    "check_canonical_structure", "check_handoff_version_stamp",
    "check_amendment_coherence", "check_floor_integrity", "check_import_edges",
    "check_routine_consumers", "check_boot_byte_budget", "check_journal_day_letters",
    "check_preflight_backlog_ids",
)


@pytest.mark.live_repo
def test_serial_and_parallel_are_byte_identical_on_real_checks_against_the_live_tree():
    """The contract's STEP-4 parity requirement, on real checks and a real tree.

    Restricted to the cheap members so the suite does not pay for a second full audit; the
    ordering property is proven exhaustively by the synthetic tests above, and this one proves
    that real check bodies -- which read files and shell out to git -- return the same verdicts
    when run concurrently.
    """
    by_name = {c.__name__: c for c in aud.ALL_CHECKS}
    checks = [by_name[n] for n in _CHEAP if n in by_name]
    assert len(checks) >= 10, "the cheap subset went stale; re-derive it from attribution"

    repo = aud.Path(aud._REPO_ROOT)
    serial = aud.run_checks(repo, checks=checks, parallel=False)
    parallel = aud.run_checks(repo, checks=checks, parallel=True)
    assert _fields(parallel) == _fields(serial)
    assert _names(serial) == _names(parallel)


# --- the CLI surface ---------------------------------------------------------------------

def test_health_accepts_the_parallel_flags_and_defaults_to_serial(monkeypatch):
    """`--parallel/--no-parallel` and `--workers` exist, and the default path is serial.

    Driven through a single sentinel check so the assertion is about the flag wiring and not
    about the live tree's health verdict.
    """
    sentinel = _make_check("sentinel")
    monkeypatch.setattr(aud, "ALL_CHECKS", [sentinel])

    result = CliRunner().invoke(aud.cmd_health)
    assert result.exit_code == 0, result.output
    assert sentinel.threads == [threading.main_thread().name]

    sentinel.threads.clear()
    result = CliRunner().invoke(aud.cmd_health, ["--parallel", "--workers", "2"])
    assert result.exit_code == 0, result.output
    assert sentinel.threads and sentinel.threads != [threading.main_thread().name]

    sentinel.threads.clear()
    result = CliRunner().invoke(aud.cmd_health, ["--no-parallel"])
    assert result.exit_code == 0, result.output
    assert sentinel.threads == [threading.main_thread().name]


def test_health_keeps_gate_mode_set_during_the_loop_under_parallel(monkeypatch):
    """`_GATE_MODE` is a process-global read by `check_doc_claims`; the parallel path must not
    change when it is set or when it is cleared. Mirrors the property
    `tests/test_audit.py` pins for the serial path -- asserted here rather than there, because
    that file is read-only to this leg."""
    seen = {}

    def _sentinel(_repo):
        seen["during"] = aud._GATE_MODE
        return [aud.Finding("sentinel", "pass", "observed gate mode")]

    monkeypatch.setattr(aud, "_GATE_MODE", False)
    monkeypatch.setattr(aud, "ALL_CHECKS", [_sentinel])
    CliRunner().invoke(aud.cmd_health, ["--parallel"])
    assert seen["during"] is True
    assert aud._GATE_MODE is False


def test_health_restores_gate_mode_when_a_parallel_check_raises(monkeypatch):
    def _boom(_repo):
        raise RuntimeError("check exploded")

    monkeypatch.setattr(aud, "_GATE_MODE", False)
    monkeypatch.setattr(aud, "ALL_CHECKS", [_boom])
    result = CliRunner().invoke(aud.cmd_health, ["--parallel"])
    assert isinstance(result.exception, RuntimeError)
    assert aud._GATE_MODE is False
