# Codex Review — codemap-amendment-and-dogfood

**Date:** 2026-05-23
**Branch:** `feat/codemap-amendment-and-dogfood`
**HEAD:** `2653271`
**Diff range:** `main..feat/codemap-amendment-and-dogfood`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
## Critical
(none)

## High
(none)

## Medium
(none)

## Low

## [LOW] .pre-commit-config.yaml:16 — Codemap hook triggers on unrelated Python files

**What:** The `files` regex matches every `*.py` file in the repo, including tests and fixture files outside the `scripts/` source root that `scripts.codemap.cli check . --source-root scripts` actually analyzes.  
**Why:** This makes the hook run on many changes that cannot affect the generated codemap, adding avoidable pre-commit noise and latency.  
**Fix direction:** Narrow the trigger to files that can change codemap output, such as `^scripts/.*\.py$`, plus the root `tach.toml` and `ARCHITECTURE.md` inputs.
