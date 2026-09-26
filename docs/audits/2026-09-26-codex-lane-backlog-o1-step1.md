# Codex Review — lane-backlog-o1-step1

**Date:** 2026-09-26
**Branch:** `worktree-lane-backlog-o1-step1`
**HEAD:** `87f44c72`
**Diff range:** `main..worktree-lane-backlog-o1-step1`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

This is lane-backlog-o1-step1 (LANE-5B3-11-backlog-o1-step1.md), continuing ADR-122
Migration step 1 (Contract and reconciliation) over scripts/task_record.py, which this
lane owns. Please focus on:
- correctness of the new efs typed field on TaskRecord and its convert_row wiring
  (comma-split, tuple, no data loss vs the old legacy_body fallback)
- correctness of removing defer from _ALREADY_CAPTURED_PREFIXES (does a DEFER clause
  now land safely in legacy_body with no crash / no silent drop, for every shape in the
  real corpus, not just the synthetic test fixtures?)
- whether any other clause prefix in _ALREADY_CAPTURED_PREFIXES has the same
  silently-dropped-instead-of-preserved defect this lane just fixed for defer
- ADR-122's Do-not: this lane must not flip the source of truth or build step 2
  (SQLite projection, closure sweep) -- flag anything that oversteps that boundary

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/task_record.py:417 — converter discards the row’s narrative description

**What:** `convert_row()` sets `description=title`, dropping all text between the title and first `·` clause.  
**Why:** This silently loses substantive row content (for example [#1080]’s reconciliation rationale), despite ADR-122 defining `description` as the record’s prose carrier and step 1 requiring complete accounting.  
**Fix direction:** Extract and preserve the leading narrative in `description` (or explicitly retain it in `legacy_body`) and add a corpus-shaped regression test.

## Medium

(none)

## Low

(none)

The new `refs` field is comma-split into a tuple and no alternate `refs:` corpus spelling was found. Removing `defer` from the allowlist preserves the real `· DEFER …` forms in `legacy_body`; I found no analogous loss among the remaining captured prefixes. No SQLite projection, closure sweep, or source-of-truth flip is introduced.

## Disposition

Per ruling (e) (batch common rules §2: "Fix a Codex review's P1 findings; record the
rest"), only Critical (P1) is fix-obligated; this run found 0 Critical. The one High
above pre-dates this lane (`description=title` was already the shape in the code
`lane-adr122-accept-2` landed) and is out of this lane's own scope — `[#1080]`'s named
remainder is `refs`/legacy_body, not `description`. Recorded, not fixed, as
`ROWS-OWED` in `to-browser/SESSION-lane-backlog-o1-step1.md`.