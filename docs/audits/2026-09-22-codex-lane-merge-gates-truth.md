# Codex Review — lane-merge-gates-truth

**Date:** 2026-09-22
**Branch:** `worktree-lane-merge-gates-truth`
**HEAD:** `965835d2`
**Diff range:** `main..worktree-lane-merge-gates-truth`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- R-W4-1: scripts/audit_checks/check_organ_truth.py now reads harness.yaml's `fates:` block for every uncalled organ. A future `manual_until` WARNs naming the date; a passed one hard-FAILs (dated debt now due); `retire_candidate: true` WARNs in a list for the operator; a `moment: <name>` fate whose named moment left a receipt in the last 30 days reads OK with no Finding; an uncalled organ with no fate still hard-FAILs. Please check: is the roster genuinely not narrowed anywhere (every bucket lists every path in full, never truncated)? Does an undated/malformed fate (e.g. two shapes on one entry, or none) correctly fail loudly rather than silently passing?
- R-W4-4: ecosystem/harness.yaml's `merge` moment gains `merge_receipt.open` as its first organ -- an inline `python -c` snippet that opens the lane's receipt only if `merge_receipt.scratch_path(...)` does not already exist, so a caller that runs only `doit moment:merge` still reaches `models` with an open receipt. Please check idempotency and that it can't silently clobber or race an already-open receipt.
- .claude/commands/lane-integrate.md: reordered the per-lane chain so `merge_receipt.py actions` runs right after `git push` (while the receipt is still open), then teardown steps (worktree remove, prune, branch -d), then `merge_receipt.py close` + a commit of the ledger append, and only then `moment:teardown` -- fixing a recorded connection-test failure where closing after teardown left `logs/.merge-receipt-<lane>.json` untracked and the `no_leftovers` working-tree-clean check failed. Please check the new ordering is internally consistent and that nothing between push and close can leave the receipt in a half-open state on failure.
- Tests added/changed: tests/test_organ_truth.py (8 new tests for the fate classes), tests/test_integrator_surface.py (new organ-open tests + chain-order tests asserting push < actions < close < commit < teardown from the command file's own text), tests/test_spine_moments.py (updated the `merge` moment's exact organ-id list to include the new first organ). Please check these tests would actually catch a regression (not vacuously true), and that the chain-order test genuinely reads the command file rather than asserting a hardcoded expectation disconnected from it.


---

## Findings
## Critical

(none)

## High

### scripts/audit_checks/check_organ_truth.py:307 — Fate dispositions are never applied

**What:** The uncalled-organ loop unconditionally appends every path to `unfated`; the loaded `fates`, date parser, receipt check, and all other fate buckets are unused.  
**Why:** Every recorded fate incorrectly hard-fails as absent, so future/manual, retire-candidate, and recent-moment behavior is nonfunctional; several newly added fate tests should fail.  
**Fix direction:** Classify each uncalled row from its loaded fate, populating exactly one appropriate bucket and using the date/receipt helpers.

### ecosystem/harness.yaml:58 — Receipt-open check has a create race

**What:** The inline organ performs `scratch_path(...).exists()` before calling `open_receipt`; neither check atomically reserves the scratch path.  
**Why:** Two concurrent merge-moment callers can both observe no receipt and both write it, silently overwriting one in-flight receipt. The sequential idempotency test does not exercise this race.  
**Fix direction:** Use an atomic exclusive-create/open primitive for receipt creation, with a deliberate “already open” no-op path for this organ.

### scripts/audit_checks/check_organ_truth.py:270 — Future-dated receipts satisfy the “last 30 days” condition

**What:** `(today - mtime).days <= 30` accepts negative ages, including receipts dated in the future.  
**Why:** An uncalled organ with a `moment:` fate can silently pass on a clock-skewed or future-timestamp receipt rather than a receipt from the prior 30 days.  
**Fix direction:** Require the receipt age to be within an inclusive `0..30`-day range and add a future-timestamp regression test.

## Medium

(none)

## Low

(none)