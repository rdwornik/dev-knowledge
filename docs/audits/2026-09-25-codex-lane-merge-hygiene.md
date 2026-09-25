# Codex Review — lane-merge-hygiene

**Date:** 2026-09-25
**Branch:** `worktree-lane-merge-hygiene`
**HEAD:** `2697a87d`
**Diff range:** `main..worktree-lane-merge-hygiene`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/1/0 <!-- Critical/High/Medium/Low. Both HIGH and the MEDIUM finding below were fixed in cce67b55 (see commit message); this tally counts what the review found, not what remains open. -->

**Disposition:** all 3 findings fixed in commit `cce67b55` (both HIGH: first-parent diff in check_post_merge.py, absent-is-unproven in batch_janitor.py; the MEDIUM mitigated with a direct `_ENDED_STATES == dispatch._ENDED` comparison test, since dispatch.py is owned by a different lane and cannot be edited here).

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: lane contract to-cc/LANE-5B-4-merge-hygiene.md (task [#1014], DIGEST-WAVE5A-2026-09-24.md blind spots 3 and 4).
Changes: scripts/merge_receipt.py (added StepTiming.ended property + start->end display in render_summary); new scripts/check_post_merge.py (git diff-tree -c based conflict-marker scan on a merge commit); new scripts/batch_janitor.py (stops a named batch's finished --bg sessions via dispatch.py's own LAUNCH-JOB receipts + claude agents --json listing, using claude stop); their tests under tests/; one additive fates: line per new script organ in ecosystem/harness.yaml.
Please check: correctness of the git diff-tree -c narrowing logic, the terminal-state duplication from dispatch.py's private _ENDED set, safety of the claude stop invocation (never targeting a live session), and whether the new modules match this repo's existing conventions.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/check_post_merge.py:146 — Combined diff omits marker-bearing files brought in unchanged from one parent

**What:** `-c` only lists paths differing from every parent, so a feature file containing a marker that is unchanged in the feature parent is omitted.  
**Why:** The check can report clean for a merge whose resulting tree contains a conflict marker, defeating the stated post-merge equivalent-of-pre-commit coverage.  
**Fix direction:** Derive paths from the merge’s first-parent diff (or scan the merge tree) rather than the combined-diff intersection.

### scripts/batch_janitor.py:210 — An absent listing entry is treated as safe to stop

**What:** A receipt-backed job missing from one `claude agents --json` snapshot is marked non-live and then targeted by `claude stop`.  
**Why:** Absence is not affirmative terminal-state evidence; a transient/stale listing can cause the janitor to stop a still-live session, contrary to its safety contract.  
**Fix direction:** Stop only sessions explicitly observed in a known terminal state; report absent jobs as indeterminate/skipped.

## MEDIUM

### scripts/batch_janitor.py:75 — Terminal-state vocabulary duplicates dispatch’s private state set

**What:** `_ENDED_STATES` independently copies `dispatch._ENDED`; the tests do not compare the two definitions.  
**Why:** A future dispatcher state addition silently leaves finished sessions resident, while the module’s “same convention” claim becomes false.  
**Fix direction:** Expose and consume a public dispatch liveness/state-classification helper or shared terminal-state constant.

## LOW

(none)