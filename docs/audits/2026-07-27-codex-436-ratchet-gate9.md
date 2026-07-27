# Codex Review — 436-ratchet-gate9

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `24a32bbb`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

NINTH pass, merge gate. Rounds returned 5, 3, 2, 3, 2, 2, 1, 1 HIGH; 19 fixed, none dispositioned. The last one is claimed fixed in 24a32bbb: _ref_baseline_state/_target_baseline_state now carry the target's detector_id; a missing/non-string detector_id => 'invalid'; a DIFFERENT detector => WARN naming the migration with no numeric comparison; same detector => ordinary raise check.
Verify: RESOLVED or STILL HIGH. Report any NEW blocking defect.
Merge gate: state plainly whether ANY blocking/HIGH defect remains anywhere in this diff.

---

## Findings
```text
Claimed 24a32bbb fix: STILL HIGH.

Merge gate: BLOCKED — one HIGH defect remains. No separate new blocking defect found.

## CRITICAL

(none)

## HIGH

HIGH scripts/audit.py:2660 — Mixed-detector target refs are compared numerically

What: `_target_baseline_state()` applies `min()` across `origin/main` and `main` before reconciling their detector IDs, so a mixed-detector state can return the matching detector and PASS.

Why: Changing only the old detector’s non-commensurable numeric scale changes the verdict from migration WARN to PASS, bypassing the required explicit migration review.

Fix direction: Detect differing detector IDs before any numeric comparison; surface a migration/indeterminate result naming both refs, and use `min()` only when all valid refs share the same detector. Add a mixed-ref regression test.

## MEDIUM

(none)

## LOW

(none)
```
