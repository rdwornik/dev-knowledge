# Codex Review — no-leftovers-detector

**Date:** 2026-06-02
**Branch:** `chore/no-leftovers-cleanup`
**HEAD:** `f8834f6`
**Diff range:** `main..HEAD`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH scripts/audit.py:776 — Same-prefix sibling repos are treated as orphaned worktrees

**What:** `check_no_sibling_orphans` flags every sibling directory named `<repo>-*` unless it appears in `git worktree list`.  
**Why:** A legitimate sibling repo or folder with the same prefix will now fail `audit run`, `audit repo`, and `health` even though it is not a leftover worktree.  
**Fix direction:** Narrow the detector to directories with evidence of being worktree leftovers, or scope it to explicitly managed worktree names/locations instead of all `<repo>-*` siblings.

## MEDIUM

(none)

## LOW

(none)
