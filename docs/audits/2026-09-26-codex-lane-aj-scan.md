# Codex Review — lane-aj-scan

**Date:** 2026-09-26
**Branch:** `worktree-lane-aj-scan`
**HEAD:** `fd021236`
**Diff range:** `main..worktree-lane-aj-scan`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/aj_scan.py:224 — Commit retrieval silently stops at the first API page

**What:** The `gh api` call does not paginate, so repos with more than GitHub’s default page size of commits return only the first page.  
**Why:** The scan then advances that repo’s cursor, permanently omitting the remaining commits from future candidate scans.  
**Fix direction:** Retrieve all commit pages (or explicitly detect/refuse a truncated result) before advancing state.

## [HIGH] scripts/aj_scan.py:420 — Repository cursors advance past commits not included in the query

**What:** Each repo’s `since` value is set to `now_iso`, generated after all repository queries complete.  
**Why:** A commit created after a repo is queried but before `now_iso` is recorded is skipped permanently on the next scan.  
**Fix direction:** Advance the cursor from the retrieved commit boundary, or use an overlap/deduplication strategy.

## [HIGH] scripts/aj_scan.py:346 — New repository deltas are persisted without the required delegated read

**What:** New commit sets become carried candidates with `what="unknown until the diff is read"`; no delegate is invoked for them.  
**Why:** Once persisted, they are treated as carried rows and never receive the promised diff analysis, leaving candidates permanently unknown.  
**Fix direction:** Complete the delegated diff read before carrying the candidate forward, or retain an explicit pending-analysis state that is retried.

## Medium

(none)

## Low

(none)

---

## Disposition (common rule 3(e): fix a Codex review's P1 findings)

All three HIGH findings fixed in the same lane, on top of this record's `HEAD`:

- **Pagination:** `scan_repo_commits` now calls `gh api --paginate --slurp`, flattening the
  page list (measured live against `gh 2.93.0`: `--paginate` alone still returned only the
  first page).
- **Cursor advancement:** a repo's new high-water mark is now the latest OBSERVED commit's own
  date (`_next_repo_since`), never a clock reading taken after the query ran; an empty result
  on an already-tracked repo leaves the mark unchanged rather than jumping to "now".
- **Delegated repo-commit read:** a repo's new commit delta is now described by the same
  `delegate_describe` call the course-delta branch already used, with its served model
  recorded on the row (`served_model`), rather than a permanent static placeholder.

Verified: `tests/test_aj_scan.py` (25 tests, including new pagination and cursor-advancement
cases) and a second live run against the real course folder and the three reference repos —
`ecosystem/aj-scan-state.yaml` shows `SkillPanel/maister`'s cursor advanced to its actual
latest commit date (`2026-09-22T20:19:10Z`), and C-6's `what` field now carries a real
delegated answer instead of the static placeholder.