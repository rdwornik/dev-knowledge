# Review — lane-hook-watchdog repair-1

**Consumer:** `LANE-5B5-5-lane-hook-watchdog.md`

**Date:** 2026-09-30
**Branch:** `worktree-lane-hook-watchdog`
**HEAD:** `d901ada9`
**Diff range:** `2564619f..d901ada9` (repair-1 only — the fix for the flaky Windows
CPU-sample test; the prior full-arc review is
`docs/audits/2026-09-30-codex-lane-hook-watchdog.md`)
**Files in scope:** `scripts/hooks/hook_watchdog.py`, `tests/test_hook_watchdog.py`
**Tally:** 0/1/2/0
**Reviewer:** `agy` CLI, model `gemini-3.1-pro-high` — **SUBSTITUTION**: Codex
(`gpt-5.6-terra`) returned `ERROR: You've hit your usage limit ... try again at Oct 3rd,
2026 9:07 PM` on the first `codex-review.ps1` invocation; the reset is 3 days out, so this
review substitutes `agy` rather than blocking the lane on it. Findings below were also
independently reproduced by direct inspection of the diff before the `agy` run returned,
so the High finding is corroborated by two independent readings, not `agy` alone.
**Review profile:** code, correctness-only

---

## Focus

Reviewing only repair-1's diff: `_cpu_total_tree()` (new), and its use in `sweep()`'s two
sample points, added to fix a flaky Windows CI test where a venv `python.exe` launcher's
own CPU reads flat while its child does the real work.

---

## Findings

## Critical

(none)

## High

### `scripts/hooks/hook_watchdog.py` — a short-lived busy child exiting before the t1
sample makes a live process tree read as suspended-at-creation

**What:** `sweep()`'s second-sample loop kills on `cpu1 is None or cpu1 > cpu0`.
`_cpu_total_tree()` sums CPU across only the CURRENTLY LIVE descendants
(`proc.children(recursive=True)` at the moment it is called). If a child accumulates real
CPU and then exits entirely between the t0 and t1 samples, that child drops out of the t1
sum; the tree's total can FALL (`cpu1 < cpu0`) even though real work happened in the
window.

**Why:** `cpu1 > cpu0` is false whenever `cpu1 <= cpu0`, so a fall reads identically to "no
movement at all" — the exact `[#863]` kill signature. A launcher whose short-lived worker
child did real work and finished before the second sample gets its whole tree killed,
which is the same class of bug repair-1 exists to close, reopened by a different
mechanism.

**Fix direction:** Compare with `cpu1 != cpu0` instead of `cpu1 > cpu0` — any change in
either direction is proof of real accumulated work somewhere in the tree; only a
bit-identical total at both samples is the genuine suspended-at-creation signature.

**Disposition: FIXED.** `sweep()`'s second loop now reads `if cpu1 is None or cpu1 !=
cpu0: continue`. Regression witness:
`tests/test_hook_watchdog.py::test_a_short_lived_busy_child_that_exits_before_t1_is_never_a_candidate`
(RED against the pre-fix `cpu1 > cpu0` comparison, GREEN after).

## Medium

### `scripts/hooks/hook_watchdog.py::_cpu_total_tree` — a root that exits in the
microsecond window between its own `cpu_times()` read and the `children()` call returns a
stale (root-only) total instead of `None`

**What:** `_cpu_total(proc)` is read first; if the root then exits before the following
`proc.children(recursive=True)` call, that call raises `NoSuchProcess`, which is caught
and treated as `children = []`, so the function returns the root's last-known total rather
than `None`.

**Why:** A caller cannot distinguish "the process has no children" from "the process
vanished mid-read"; in the latter case the returned total is momentarily frozen rather
than reflecting reality, which could — in the same narrow race — read as no movement.

**Disposition: SKIPPED.** Narrower than the High finding above (a single-microsecond race
on the root's own exit, vs. the High finding's window-wide, routinely-hit child-lifecycle
case) and shares the same fail-open posture `_session_id_for`/`kill_tree` already take
elsewhere in this module (best-effort on a `NoSuchProcess` mid-walk). Not fixed in this
pass; left as a known, narrower edge for a future lane if it is ever observed live.

### `scripts/hooks/hook_watchdog.py` — no `try/except psutil.Error` around the t1
`_cpu_total_tree()` call in `sweep()`'s second loop

**What:** The first (baseline) loop wraps its candidate read in `try/except psutil.Error`;
the second loop's `cpu1 = _cpu_total_tree(proc)` call is unwrapped.

**Disposition: NO CHANGE NEEDED — verified false positive.** `psutil.ZombieProcess`
subclasses `psutil.NoSuchProcess` (confirmed via `psutil.ZombieProcess.__mro__` in this
session's environment), and both `_cpu_total()` and the `children()` call inside
`_cpu_total_tree()` already catch `(psutil.NoSuchProcess, psutil.AccessDenied)` internally
and degrade to `None` / `[]` respectively — `_cpu_total_tree()` cannot raise
`psutil.Error` to its caller under a dead-or-zombie-process read, so the second loop needs
no additional wrapping.

## Low

(none)

---

## Verification

- `uv run --locked pytest -x --tb=short tests/test_hook_watchdog.py -q` — 20 passed
  (19 prior + 1 new regression witness).
- `uv run --locked ruff check scripts/hooks/hook_watchdog.py tests/test_hook_watchdog.py` —
  all checks passed.
