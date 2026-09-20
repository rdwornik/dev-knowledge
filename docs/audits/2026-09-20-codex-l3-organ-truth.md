# Codex Review — l3-organ-truth

**Date:** 2026-09-20
**Branch:** `worktree-lane-l3-organ-truth`
**HEAD:** `82b1dab1`
**Diff range:** `main..worktree-lane-l3-organ-truth`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0
**Disposition (lane-l3-organ-truth):** all three HIGH fixed in `e00b69f2`, each with a RED test committed first in `643dc4d7` (5 failed / 21 passed before the fix, 26 passed after): `-c` from-imports and absent optional imports (`graph_queries._snippet_scripts`), malformed declaration refused (`MomentsUnreadable`), and any index claim about a vanished hook contradicts (`arming_contradictions`). Review ran at `82b1dab1`; the fixes were not re-reviewed.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/generate_organ_index.py: is any hook still reported ARMED on the strength of being present? manual_until parsing scope (per-hook block); arming_contradictions correctness (name/source keys, ARMED-vs-absent).
- scripts/graph_queries.py moments mode: does the declared-at-moment / optional-unbuilt / nowhere classification mis-assign (path extraction from argv, -c imports, dotted ids)? Is the roster narrowed anywhere to make it pass?
- scripts/audit_checks/check_organ_truth.py + audit.py registration: verdict never unavailable; TIER_SHIP justification; false pass paths.
- ecosystem/routing-table.yaml: adversarial model pin is one the repo already uses.
- tests/test_organ_truth.py: vacuous assertions, RED-first validity.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/graph_queries.py:1472

**What:** `-c` import extraction only accepts bare `import name`, and discards imports whose `scripts/name.py` is not already present.  
**Why:** Declared scripts imported via `from name import …` are falsely reported as `declared-nowhere`; optional missing scripts imported via `-c` are omitted entirely and can let the organ check pass.  
**Fix direction:** Parse supported `-c` import forms into candidate script paths regardless of current existence, then classify existence afterward; add RED tests for `from` imports and absent optional imports.

### scripts/graph_queries.py:1517

**What:** A moment organ with a non-list `command` is silently converted to an empty command rather than refusing the malformed declaration.  
**Why:** Such an optional-unbuilt organ has no `primary` path and is skipped by `organ_moments`, allowing a malformed declaration to produce a clean result.  
**Fix direction:** Treat an invalid organ command (and invalid `moments`/`organs` shapes) as `MomentsUnreadable`/a failing finding; add a malformed-command RED test.

### scripts/generate_organ_index.py:847

**What:** An index claim for a `MANUAL` hook is ignored when that hook no longer exists in the live config; only stale `ARMED` claims are reported.  
**Why:** The organ-truth check can pass while the committed index claims an on-demand/conductor hook remains available when it is actually absent.  
**Fix direction:** Report every claimed hook missing from live config as `ABSENT`-contradicting, not only `ARMED` claims; cover stale `MANUAL` and dated-`MANUAL` rows.

## MEDIUM

(none)

## LOW

(none)