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
from pathlib import Path

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


def _tiered_sentinel(name, tier, calls):
    def _fn(_repo):
        calls.append(name)
        return [aud.Finding(name, "pass", "ran")]
    _fn.__name__ = f"check_{name}"
    return aud._tier(tier, _fn)


def test_health_applies_the_commit_tier_under_parallel(monkeypatch):
    """The [#597] successor to `test_health_keeps_gate_mode_set_during_the_loop_under_parallel`:
    `_GATE_MODE` was a process-global read by `check_doc_claims`, and the tier replaces it. The
    parallel path must select the SAME set as the serial one -- it builds `slots` differently
    (pre-seeded deferrals + a sparse future map, rather than a comprehension), which is exactly
    where a divergence would hide. Mirrors the property `tests/test_audit.py` pins for serial."""
    calls = []
    monkeypatch.setattr(aud, "ALL_CHECKS", [_tiered_sentinel("a", aud.TIER_COMMIT, calls),
                                            _tiered_sentinel("b", aud.TIER_SHIP, calls)])
    result = CliRunner().invoke(aud.cmd_health, ["--parallel"])
    assert calls == ["a"]
    assert "b: " in result.output          # deferred, still enumerated in registry order
    assert "ship-tier" in result.output


def test_health_needs_no_state_restored_when_a_parallel_check_raises(monkeypatch):
    """The tier is an argument, so the raise cannot leave a global set -- there is none. What
    still must hold is that the exception PROPAGATES rather than being swallowed into a
    short report, and that a later run is unaffected."""
    def _boom(_repo):
        raise RuntimeError("check exploded")

    monkeypatch.setattr(aud, "ALL_CHECKS", [_boom])
    result = CliRunner().invoke(aud.cmd_health, ["--parallel"])
    assert isinstance(result.exception, RuntimeError)
    assert not hasattr(aud, "_GATE_MODE")

    calls = []
    monkeypatch.setattr(aud, "ALL_CHECKS", [_tiered_sentinel("a", aud.TIER_COMMIT, calls),
                                            _tiered_sentinel("b", aud.TIER_SHIP, calls)])
    CliRunner().invoke(aud.cmd_health, ["--parallel"])
    assert calls == ["a"]


def test_parallel_worker_width_is_sized_to_the_checks_that_actually_run(monkeypatch):
    """A pool sized to `len(active)` would open 46 threads to run 36 checks. Sized to the
    RUNNING set instead -- and floored at 1, because `ThreadPoolExecutor(max_workers=0)` raises
    and an all-deferred list is a legitimate call."""
    seen = {}
    real = aud.ThreadPoolExecutor

    class _Spy(real):
        def __init__(self, max_workers=None, **kw):
            seen["width"] = max_workers
            super().__init__(max_workers=max_workers, **kw)

    monkeypatch.setattr(aud, "ThreadPoolExecutor", _Spy)
    calls = []
    checks = [_tiered_sentinel(f"s{i}", aud.TIER_SHIP, calls) for i in range(5)]
    checks.append(_tiered_sentinel("c", aud.TIER_COMMIT, calls))
    aud.run_checks(Path("."), checks=checks, parallel=True, tier=aud.TIER_COMMIT)
    assert seen["width"] == 1          # one runnable check, not six
    assert calls == ["c"]

    calls.clear()
    aud.run_checks(Path("."), checks=checks[:5], parallel=True, tier=aud.TIER_COMMIT)
    assert seen["width"] == 1          # all deferred: floored at 1, never 0
    assert calls == []


# --- intake #71 P3: the per-run read cache ------------------------------------------------
#
# THE DEFECT THESE EXIST BECAUSE OF. The cache landed with no test at all and was INERT at the
# commit tier for a day: `args`/`kwargs` were part of the key, this corpus is walked once with
# `read_text(encoding="utf-8")` and once with `read_text(encoding="utf-8", errors="replace")`,
# so the same file under the same mtime occupied two entries and every read missed. Measured
# before the fix: 4,085 `read_text` calls, 4,085 real reads, hit rate 0.0%. A speed organ that
# silently does nothing is the failure mode a "measured 70% fewer reads" commit message cannot
# catch, so what is pinned below is that the cache HITS -- not merely that it returns the right
# answer, which an absent cache also does.


def _count_reads(monkeypatch):
    """Install counters UNDER the cache and return them. A call reaching these is a real read."""
    calls = {"text": 0, "bytes": 0}
    orig_t, orig_b = Path.read_text, Path.read_bytes

    def t(self, *a, **kw):
        calls["text"] += 1
        return orig_t(self, *a, **kw)

    def b(self, *a, **kw):
        calls["bytes"] += 1
        return orig_b(self, *a, **kw)

    monkeypatch.setattr(Path, "read_text", t)
    monkeypatch.setattr(Path, "read_bytes", b)
    return calls


def test_the_read_cache_actually_hits_across_differing_errors_kwargs(tmp_path, monkeypatch):
    """The regression itself: two arg-shapes for one file must cost ONE physical read."""
    p = tmp_path / "doc.md"
    # write_BYTES, not write_text: on Windows `write_text` translates the LF to CRLF, so a
    # byte-level assertion written against the source literal fails on one platform only.
    p.write_bytes(b"hello\n")
    calls = _count_reads(monkeypatch)

    with aud._cached_reads():
        a = p.read_text(encoding="utf-8")
        b = p.read_text(encoding="utf-8", errors="replace")
        c = p.read_bytes()

    assert a == b == "hello\n"
    assert c == b"hello\n"
    assert calls["bytes"] + calls["text"] == 1, (
        f"one file, three reads, {calls} physical reads -- the cache is not hitting")


def test_the_read_cache_shares_one_open_between_text_and_bytes(tmp_path, monkeypatch):
    """`read_text` is served by DECODING the bytes `read_bytes` already read, not by a second
    open -- which is what makes the two entry points one cache rather than two."""
    p = tmp_path / "doc.md"
    p.write_text("x" * 100, encoding="utf-8")
    calls = _count_reads(monkeypatch)

    with aud._cached_reads():
        for _ in range(5):
            p.read_bytes()
            p.read_text(encoding="utf-8")

    assert calls["bytes"] + calls["text"] == 1, calls


def test_the_read_cache_preserves_universal_newline_translation(tmp_path):
    """A CRLF file must read back with LF endings exactly as uncached `read_text` gives them.

    `Path.read_text` opens in TEXT mode, so Python translates; `bytes.decode` does not. Serving
    a decode of the raw bytes without reapplying the translation would leave a carriage return
    at every line end -- and a frontmatter value of `open\\r` matches nothing, which turns a
    speed change into a silently different verdict."""
    p = tmp_path / "crlf.md"
    p.write_bytes(b"---\r\nstatus: open\r\n---\r\n")
    uncached = p.read_text(encoding="utf-8")

    with aud._cached_reads():
        assert p.read_text(encoding="utf-8") == uncached
        assert p.read_text(encoding="utf-8") == uncached      # again, from the cache
    assert "\r" not in uncached


def test_the_read_cache_keeps_strict_decoding_strict(tmp_path):
    """`errors=None` must still RAISE on undecodable bytes, and must not be contaminated by an
    `errors="replace"` read of the same file. Sharing the I/O may never share the semantics."""
    p = tmp_path / "bad.md"
    p.write_bytes(b"ok \xff\xfe not utf-8\n")

    with aud._cached_reads():
        replaced = p.read_text(encoding="utf-8", errors="replace")
        assert "�" in replaced
        with pytest.raises(UnicodeDecodeError):
            p.read_text(encoding="utf-8")
        # ...and in the other order, on a cache already holding the strict failure.
        assert p.read_text(encoding="utf-8", errors="replace") == replaced


def test_the_read_cache_is_restored_and_leaks_nothing():
    """Nothing outlives the context -- criterion 6 of #71. A cache that survived its run would
    make a gate lie, which is worse than a slow gate."""
    before_t, before_b = Path.read_text, Path.read_bytes
    with aud._cached_reads():
        assert Path.read_text is not before_t
        assert Path.read_bytes is not before_b
    assert Path.read_text is before_t
    assert Path.read_bytes is before_b


def test_the_read_cache_re_reads_a_file_that_changed_mid_run(tmp_path):
    """Keyed on (path, mtime_ns, size), not path alone. Every check is documented read-only, so
    this should never fire in practice -- but the key catches a mutation rather than serving
    stale content, and that is the difference between a cache and a bug."""
    p = tmp_path / "moving.md"
    p.write_text("first", encoding="utf-8")
    with aud._cached_reads():
        assert p.read_text(encoding="utf-8") == "first"
        p.write_text("second-and-longer", encoding="utf-8")
        assert p.read_text(encoding="utf-8") == "second-and-longer"
