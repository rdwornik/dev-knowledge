# Codex Review — ruff-hub-pin

**Date:** 2026-07-12
**Branch:** `chore/ruff-hub-pin`
**HEAD:** `ce81f99c`
**Diff range:** `main..chore/ruff-hub-pin`
**Codex version:** codex-cli 0.144.1
**Mode:** diff-review

---

## Focus

- .pre-commit-config.yaml ruff hook converted from language:system local hook to pinned astral-sh/ruff-pre-commit @ v0.15.5 (args: []), matching corp-monorepo + ai-council
- pyproject.toml [tool.ruff] required-version floor comment updated
- Verify: rev pin (v0.15.5) is consistent with the >=0.15.5 floor; args:[] is check-only (no --fix); no YAML structural regressions

---

## Findings
## Critical

(none)

## High

`.pre-commit-config.yaml:165`

**What:** The pinned `ruff-pre-commit` v0.15.5 hook is configured as `id: ruff`, but that release exposes the lint hook as `ruff-check`.  
**Why:** Pre-commit will reject the unknown hook ID, blocking commits instead of running Ruff.  
**Fix direction:** Use the release’s `ruff-check` hook ID; retain `args: []` for check-only behavior.

## Medium

(none)

## Low

(none)
