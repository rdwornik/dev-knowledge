# Lane ac-694 (insurance leg) — row age and abandonment census

**Lane:** `lane-ac-694-insurance-census` · **Branch:** `worktree-lane-ac-694-insurance-census` ·
**Batch:** AC · **Date:** 2026-09-18 · **Scope:** read-only census, PROPOSE ONLY — no rows closed

## 1 · Method

Per task-file row in `tasks/` (553 files at census time): filing date and last-touch date from a
single batched `git log --name-only --format="COMMIT|%H|%ad" --date=short -- tasks/` (newest-first;
first occurrence of a filename = last touch, last occurrence = filing-date heuristic); last commit
*citing* the id from a single batched full-history commit-subject dump, grepped per id for
`[#<id>]`; current-tree reference count from one pass of `\[#\d+\]` over the working tree. "Today"
= 2026-09-18 for age math.

## 2 · Bucket table

| Age (since last touch) | Row count | Disposition mix |
|---|---|---|
| 0–7 d | 181 | active work |
| 8–30 d | 202 | active / cited recently |
| 31–90 d | 170 | aging baseline, still referenced |
| 91–180 d | 0 | — |
| 180 d+ | 0 | — |
| **Total** | **553** | — |

**No row is older than 52 days untouched.** The oldest cohort (37 rows) all last-touched
2026-07-28.

## 3 · Oldest cohort — full-depth disposition

All 37 oldest (52-day) rows were checked individually. None showed rot (no orphaned, renamed, or
broken references). Representative sample (16 of 37, all still tree-referenced):

| id | status | last touch | last cited | still referenced | disposition |
|---|---|---|---|---|---|
| 19 | DEFERRED | 2026-07-28 | never | yes | still wanted — pegged to an ADR-39 lookup trigger |
| 144 | DEFERRED | 2026-07-28 | never | yes | still wanted — pegged to cloud-deployment-target resolution (ADR-81) |
| 166 | DEFERRED | 2026-07-28 | never | yes | still wanted — doctrine-coherence check, waiting on other governance |
| 181 | DEFERRED | 2026-07-28 | never | yes | still wanted — coherence-v2 nudge follow-up |
| 185 | OPEN | 2026-07-28 | never | yes | still wanted — GAP-2 gotcha guard |
| 190 | DEFERRED | 2026-07-28 | never | yes | still wanted — intra-file duplication detector |
| 240 | DEFERRED | 2026-07-28 | never | yes | still wanted — explicit follow-up, peg unstated |
| 305 | DEFERRED | 2026-07-28 | never | yes | still wanted — deferred verification-mode addition |
| 340 | OPEN | 2026-07-28 | never | yes | still wanted — `/ship` pre-flight validator fix |
| 345 | OPEN | 2026-07-28 | never | yes | still wanted — ADR-101 registry externalization |
| 354 | OPEN | 2026-07-28 | never | yes | still wanted — W6 seed task |
| 388 | OPEN | 2026-07-28 | never | yes | still wanted — fleet scale-target fabrication audit |
| 392 | OPEN | 2026-07-28 | never | yes | still wanted — fleet analytics rename regression |
| 402 | OPEN | 2026-07-28 | never | yes | still wanted — intake YYYY-MM-DD deploy |
| 442 | OPEN | 2026-07-28 | never | yes | still wanted — plugin command-cache staleness |
| 4 | OPEN | 2026-07-28 | never | yes | still wanted — lessons-index JSON retrieval |

**No abandonment candidates found.** Zero rows are proposed as superseded or never-happening —
every row checked at full depth is either explicitly DEFERRED behind a named trigger or OPEN and
still referenced somewhere live (BACKLOG, docs, config, decisions).

## 4 · Surprising findings

- **239 of 553 rows (43%) have zero commit citations**, but "uncited" is not "abandoned": deferred
  rows are designed to stay uncited until their trigger fires, and 20 of the uncited rows are
  simply new (9 days old, batch 644–671).
- **758 current-tree `[#id]` references resolve to 553 unique ids** — most rows are referenced
  from more than one place (task registry, BACKLOG, manifests, decision docs), not just their own
  body.
- **No row predates 2026-07-28.** Given this repo's git history runs back to at least April 2026
  (per JOURNAL/council entries), a 553-row backlog with a hard floor at 52 days is itself the
  finding worth flagging: it is consistent with — but not confirmed against — the per-file task
  convention or a backlog migration landing around that date (`docs/audits/2026-06-01-backlog-
  migration-inventory.md` is a candidate source event, **not independently verified in this
  census** — follow-up recommended before treating "no row over 90 days" as proof of a young
  backlog rather than an artifact of when the per-file convention started).

## 5 · Caveats

- Filing-date is a heuristic (oldest commit touching the filename) and breaks under rename;
  spot-checks on the oldest 37 found no rename pattern, but this was not checked for all 553.
- Citation search covered commit-message **subject lines** only, not bodies or ADR prose; the true
  citation count is understated.
- Full per-row depth (filing date, last-touch, last-citing-commit, still-referenced, disposition)
  was completed for the oldest 37 rows (the entire 31–90 d bucket's tail) plus spot-checks of ~31
  more; the 0–30 d buckets (383 rows) got bucket-level treatment only, per the stated time budget.

## 6 · Recommendation

At the next audit window, re-run this census and confirm whether the 91-180 d bucket populates —
if it stays empty past ~90 more days, that's confirmation the backlog is genuinely young; if the
oldest-cohort date (2026-07-28) never moves, that's confirmation it's a migration-boundary
artifact, not organic age.
