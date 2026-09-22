# Codex Review — lane-batch-digest

**Date:** 2026-09-22
**Branch:** `worktree-lane-batch-digest`
**HEAD:** `cdecb29a`
**Diff range:** `main..worktree-lane-batch-digest`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0

**Consumer:** [#939] wave-4a lane 3 (`LANE-W4-3-batch-digest.md`, R-W4-3)

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## CRITICAL

(none)

## HIGH

### HIGH scripts/lane_digest.py:215 — merge SHA lookup ignores batch identity

**What:** `load_merge_shas()` selects the newest ledger row by lane slug only; the reports-mode caller never supplies or filters on the current batch.  
**Why:** Reusing a lane slug in a later batch makes an earlier batch digest display the later batch’s merge SHA, silently misattributing a merge.  
**Fix direction:** Filter ledger rows by the active batch (and merge-record type) before selecting the newest SHA; add a cross-batch reused-slug test.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (lane-batch-digest, recorded before handback)

| # | Finding | Disposition | Evidence |
|---|---|---|---|
| 1 | HIGH `lane_digest.py:215` -- `load_merge_shas` selects the newest ledger row by slug alone, so a lane slug reused in a later batch would hand an earlier batch's digest the later batch's merge sha | **ACTIONED.** `load_merge_shas` takes an optional `batch` and filters ledger rows to it before picking the newest row per slug; `main()` resolves the batch from `--batch`, else `--lane` (the unedited harness.yaml row's `{batch}` substitution), else `$HARNESS_BATCH`. An unnamed batch keeps the old, unfiltered behaviour (the only thing possible without knowing which batch to prefer). | `tests/test_lane_digest.py::test_a_reused_lane_slug_across_batches_does_not_misattribute_the_merge_sha` (red if the filter or the batch resolution is reverted) |