# Codex Review — sacred-files-cadence-check10

**Date:** 2026-06-01
**Branch:** `feat/sacred-files-cadence-2026-06-01`
**HEAD:** `e6f9bd7`
**Diff range:** `main..feat/sacred-files-cadence-2026-06-01`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

- A2 git-date logic in check_canonical_freshness: correctness of last_reviewed < git_date -> FAIL; equal-date, uncommitted-working-tree-edit, no-git, no-history edge cases; %cs committer-date choice
- _parse_last_reviewed: YAML date/datetime/quoted-string/missing-key/unclosed-frontmatter/non-date handling; can it raise instead of returning None?
- Severity aggregation: A2 FAIL must dominate A1 WARN must dominate missing-WARN; can a stale file be silently missed or mis-ranked?
- Portability: any hidden .dev-knowledge-specific assumption in the parameterised _FRESHNESS_FILES check (it must drop into a child repo unchanged)?
- Tests: do they over-mock _git_last_commit_date such that a real bug would pass? Is the deliberately-staled-fixture FAIL genuinely proven?
- Read-only / Layer-2 invariant: subprocess git log must be read-only, must not mutate state

---

## Findings
## Critical
(none)

## High

## [HIGH] scripts/audit.py:627 — A2 misses uncommitted or untracked edits, so stale files can pass

**What:** `_git_last_commit_date()` only looks at `git log -1`, and `check_canonical_freshness()` uses that as the sole A2 “edited since review” signal.  
**Why:** A canonical file changed in the working tree after its `last_reviewed` stamp has no newer commit yet, so A2 is skipped and the file can be reported fresh or only A1-warned. That silently misses the main failure mode this check claims to enforce.  
**Fix direction:** Fold working-tree state into A2 for tracked freshness files before falling back to commit history; handle dirty, untracked, and no-history cases explicitly instead of treating them all as “no git signal.”

## [HIGH] scripts/audit.py:627 — `%cs` uses committer date, which can false-fail after rebase/cherry-pick

**What:** The git helper uses `git log -1 --format=%cs -- <file>`, which returns the last committer date, not a stable “content was edited on this day” signal.  
**Why:** Rebases, cherry-picks, and amends rewrite committer dates even when the file content and `last_reviewed` stamp are unchanged, so A2 can start failing on history rewrites rather than real post-review edits.  
**Fix direction:** Use a content-edit signal that is robust to rewritten commit metadata, or at minimum switch away from committer date and document the remaining semantics clearly.

## [HIGH] tests/test_audit.py:815 — The new tests over-mock git, so the real freshness path is not proven

**What:** Every freshness test monkeypatches `_git_last_commit_date`; none exercises the real subprocess call, a dirty working tree, equal-date behavior, or a no-history/untracked file.  
**Why:** The suite will stay green even if the production helper is wrong or if A2 misses real stale files in git-backed repos, so the “deliberately staled fixture” does not actually validate the shipped path.  
**Fix direction:** Add at least one integration-style test with a temporary git repo that uses the real helper and covers committed-stale, equal-date, dirty-working-tree, and no-history cases.

## Medium
(none)

## Low
(none)
