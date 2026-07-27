# Codex Review — 436-ratchet-gate8

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `04be5084`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

EIGHTH pass, merge gate. Rounds returned 5, 3, 2, 3, 2, 2, 1 HIGH; 18 fixed, none dispositioned. The last one is claimed fixed in 04be5084:
_index_worktree_divergence() no longer intersects staged and unstaged lists. It now returns 'diverged' if git diff --name-only -- <paths> is non-empty OR git ls-files --others --exclude-standard -- <paths> is non-empty; 'unknown' if either probe fails; 'ok' only when both are clean.
Verify: RESOLVED or STILL HIGH. Report any NEW blocking defect.
Merge gate: state plainly whether ANY blocking/HIGH defect remains anywhere in this diff. MEDIUM/LOW are non-blocking and need not be listed unless you consider them severe.

---

## Findings
Claimed `04be5084` fix: **RESOLVED**.

Merge gate: **BLOCKED — one new HIGH defect remains.**

## CRITICAL

(none)

## HIGH scripts/audit.py:2696 — Target baseline loses its detector identity

**What:** `_ref_baseline_state()` validates and returns only the target’s numeric `baseline`, allowing `_ratchet_findings()` to compare a current `silent-rule-v5` baseline numerically against a `silent-rule-v4` target—or a target missing `detector_id` entirely—and pass.

**Why:** The detector contract explicitly declares counts from different detector versions non-commensurable. A detector revision can therefore silently rebase the metric and bypass the ratchet-down invariant.

**Fix direction:** Carry and validate the target baseline’s `detector_id`; block missing or mismatched IDs and require an explicit migration/remeasurement path. Add regression tests for mismatched and absent target detector IDs.
