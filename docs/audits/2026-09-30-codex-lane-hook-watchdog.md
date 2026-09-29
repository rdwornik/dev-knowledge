# Codex Review — lane-hook-watchdog

**Date:** 2026-09-30
**Branch:** `worktree-lane-hook-watchdog`
**HEAD:** `28b764a9` (review base; fixes landed in a later commit on this branch)
**Diff range:** `origin/main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/2/0/0
**Model used:** `gpt-5.6-terra`
**Review profile:** code

---

## Focus

Consumer: `LANE-5B5-5-lane-hook-watchdog.md` (batch `WAVE5B-N5`, row `[#863]`).

Reviewed the four-file diff (`scripts/hooks/hook_watchdog.py`, `tests/test_hook_watchdog.py`,
`scripts/fleet_health.py`, `ecosystem/harness.yaml`) only. The deliberate absence of a
`.claude/settings.json` change was not treated as a defect: this watchdog has a `manual_until`
fate and no automatic caller.

Codex's own reviewer policy is read-only (`~/.codex/AGENTS.md`), so it returned the findings as
ready-to-paste text rather than writing this file itself; this record is that text, verbatim
below, with a **Disposition** line added per finding after the fixes it prompted.

---

## Findings

## Critical

### scripts/hooks/hook_watchdog.py:152, 155, 280, 284 — Zero CPU plus orphanhood does not prove a process was never resumed

**What:** `sweep()` force-kills any process whose command line merely contains a registered hook
basename, whose parent is gone, and whose CPU total does not change for one threshold window. A
legitimately running hook can be orphaned and blocked in I/O, sleeping, or receive no CPU
scheduling during that interval; all meet this signature.
**Why:** The action is `taskkill /T /F`, so this can kill a live hook and its descendants. The
broad substring match can also select a non-hook process whose arguments contain a hook script
name.
**Fix direction:** Require a discriminator that establishes OS-level suspended/stopped state
(and tighter command identity) before killing; otherwise make the ambiguous zero-CPU case
report-only or require an additional confirmation.

**Disposition: FIXED.** `sweep()` now requires the FIRST CPU sample itself to already be
near-zero (`_NEAR_ZERO_BASELINE_CPU_S`, 0.1 s) before a candidate is even tracked into the
threshold window — the real `[#863]` signature is "0 s CPU from creation", not "flat during
whatever window we happened to sample it in". A process that ran real work before `sweep` ever
saw it (the "ran, then legitimately blocked" mode) is excluded at the baseline, regardless of
what it does afterward. Regression witness:
`tests/test_hook_watchdog.py::test_a_process_with_real_accumulated_cpu_is_never_a_candidate_even_if_flat_now`.
The broad substring match on command line is unchanged by design (it mirrors the live
`.claude/settings.json` convention, read dynamically rather than hardcoded a second time) — the
near-zero-baseline requirement is what removes the dangerous half of this finding (killing a
*live* process); a coincidental cmdline match against a *dead-from-birth* process was already
the intended, narrow target.

## High

### scripts/hooks/hook_watchdog.py:155; tests/test_hook_watchdog.py:171, 185 — POSIX orphan reproduction is not detected

**What:** On POSIX, a child whose creator exits is normally reparented to PID 1 or a configured
subreaper, so `psutil.Process(pid).parent()` is a live process rather than `None`; the fixture's
`assert proc.parent() is None` and subsequent expected kill do not hold.
**Why:** The required non-skipped POSIX branch fails and a genuinely stopped orphan is omitted
from `sweep()` on that platform.
**Fix direction:** Define orphan detection per platform (including POSIX
reparenting/subreaper semantics) and make the fixture assert that platform's actual orphan
representation.

**Disposition: FIXED.** New `_is_orphaned(proc)` helper: `parent() is None` (the Windows shape)
OR `ppid() in (0, 1)` (the POSIX reparented-to-init shape). `_is_candidate` and the fixture
assertion both route through it now. Unit-tested directly against fake parent/ppid doubles
(`test_is_orphaned_true_when_parent_is_none`, `test_is_orphaned_true_when_reparented_to_pid_1`,
`test_is_orphaned_false_with_a_live_non_init_parent`) so the platform branches are exercised
deterministically rather than only by whichever OS runs the suite. Not independently verified on
a POSIX runner in this session (Windows-only box) — CI's Linux leg is the live proof; flagged
here rather than silently assumed.

### scripts/hooks/hook_watchdog.py:222; tests/test_hook_watchdog.py:326 — POSIX `kill_tree()` kills only the root process

**What:** The non-Windows branch calls `os.kill(pid, 9)`, which leaves descendants alive; the
test explicitly expects the child to be gone.
**Why:** The implementation contradicts its whole-tree contract and the cross-platform tree-kill
test will fail on POSIX, potentially leaving descendants running.
**Fix direction:** Use a process-group or recursive descendant termination strategy on POSIX,
with fixture setup that gives the tested root a dedicated process group.

**Disposition: FIXED**, via a `psutil`-based recursive walk (`root.children(recursive=True)`,
then `.kill()` each descendant plus the root) rather than a process-group signal —
`bounded_hook.py::_kill_tree`'s `os.killpg` was considered and rejected as a direct reuse: it
depends on the target being its own process-group leader (`start_new_session=True` at spawn
time), a property this module cannot assume about a process it did not spawn. No dedicated
process group is needed for the psutil walk. Same regression witness as before
(`test_kill_tree_kills_the_whole_process_tree`); not independently re-verified on POSIX in this
session for the same reason as the finding above.

## Medium

(none)

## Low

(none)

---

`fleet_health.py`'s surfacing shape and the `ecosystem/harness.yaml` manual fate entry were
found to match local conventions and drew no findings.
