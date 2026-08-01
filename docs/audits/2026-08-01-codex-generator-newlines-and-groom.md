# Codex Review — generator-newlines-and-groom

**Date:** 2026-08-01
**Branch:** `fix/generator-newlines-and-groom`
**HEAD:** `cae18323`
**Diff range:** `main..fix/generator-newlines-and-groom`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
## CRITICAL

(none)

## HIGH tests/test_generator_newlines.py:66 — Newline guard skips nested scripts

**What:** `_SCRIPTS.glob("*.py")` scans only top-level scripts, excluding subpackages such as `scripts/toc/cli.py`, whose write still lacks `newline=`.

**Why:** The guard passes while a live generator can still emit CRLF on Windows, leaving the platform-dependent rewrite defect partially unfixed.

**Fix direction:** Recursively scan with `rglob("*.py")`, pin the nested write sites, and add a nested-script regression case.

## MEDIUM

(none)

## LOW

(none)
