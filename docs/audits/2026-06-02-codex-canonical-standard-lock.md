# Codex Review — canonical-standard-lock

**Date:** 2026-06-02
**Branch:** `chore/lock-canonical-standard`
**HEAD:** `d18aeb5`
**Diff range:** `main..chore/lock-canonical-standard`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

- audit.py check_canonical_structure: startswith spine matching correctness, child-repo safety, read-only
- _CANONICAL_MANDATORY 4->7 promotion: any check that now over/under-requires files
- test inversions + new structural tests assert the new behavior

---

## Findings
## Critical

(none)

## High

## HIGH scripts/audit.py:867 — spine heading matcher can false-pass

**What:** `line.startswith(heading)` accepts non-matching headings like `## Visionary` for required `## Vision` or `# Journalized` for `# Journal`.  
**Why:** A child repo can omit the exact mandatory `[U]` spine heading while `canonical_structure` still reports PASS, silently weakening the new structural standard.  
**Fix direction:** Match heading boundaries explicitly, allowing only exact heading text plus an approved suffix separator for repo-specific titles.

## Medium

(none)

## Low

(none)
