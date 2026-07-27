# Codex Review — 436-ratchet-gate6

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `7793c63a`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

SIXTH pass, merge gate. Rounds so far returned 5, 3, 2, 3, 2 HIGH; 15 fixed, none dispositioned. The last two are claimed fixed in 7793c63a:
1. _ref_baseline_state now pins the resolved commit OID and uses it for BOTH ls-tree and show, instead of re-reading the mutable ref name.
2. check_task_tree_coherence now FAILs when the index and working tree disagree on BACKLOG.md or tasks/, rather than trusting a working-tree read.
Verify each: RESOLVED or STILL HIGH. Report any NEW blocking defect these two changes introduced.
This is a merge gate: state plainly whether any BLOCKING/HIGH defect remains. MEDIUM/LOW are non-blocking here.

---

## Findings
BLOCKING/HIGH defects remain: **YES — 2 HIGH. Do not merge.**

Fix verification:

1. `_ref_baseline_state` OID pin: **RESOLVED**. The resolved OID is used for both `ls-tree` and `show`.
2. Task-tree index/worktree protection: **STILL HIGH**. It catches the tested stage-then-restore case only when both Git probes succeed; probe failure silently restores the unsafe working-tree behavior.

## CRITICAL

(none)

## HIGH

### HIGH — scripts/audit.py:2575 — staged baseline raises can bypass the ratchet

**What:** `_load_silent_rule_baseline` reads the working-tree file, while the detector and eventual commit use the index; staging a raised baseline and restoring the working copy makes the check validate the old value while committing the raised one.

**Why:** This defeats the ratchet-down-only invariant and permits silent baseline inflation.

**Fix direction:** Read the baseline from the index blob, or fail on any index/worktree divergence for `ecosystem/silent-rule-baseline.yaml`.

### HIGH — scripts/audit.py:2838 — Git-probe failures bypass the task-tree guard

**What:** When either `_git diff` call returns `None` or nonzero, the divergence check is skipped and `find_incoherences` proceeds against the working tree.

**Why:** A timeout or Git error reopens the exact staged-content hiding path this change intends to close; a read-only probe confirmed that forcing `_git` to fail still returns `pass`.

**Fix direction:** Return a FAIL finding whenever either Git probe cannot complete successfully, or perform the coherence check directly against a single index snapshot.

## MEDIUM

(none)

## LOW

(none)

Validation: 1,836 tests collected; four relevant read-only live tests passed.
