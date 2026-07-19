# Codex Review — residual-completeness-gate

**Date:** 2026-07-19
**Branch:** `feat/residual-completeness-gate`
**HEAD:** `2e444fa3`
**Diff range:** `main..feat/residual-completeness-gate`
**Codex version:** codex-cli 0.144.5
**Mode:** diff-review

---

## Focus

- FILL-IN region regex: backreference on the region name, DOTALL body capture, inline single-line form inside a markdown table cell. Any way a region is missed or over-matched?
- Diff-trigger correctness: git status --porcelain -uall -z parsing; the -uall is load-bearing because git collapses a NEW untracked bundle dir to one entry. Deletions skipped. Fail-soft to empty list on git error.
- region_is_unfilled predicate: empty or placeholder-only. Is the _(fill: ...)_ match too narrow or too broad?
- ANTI-BLUFF NON-COLLISION: the gate must NOT demand content, only that the placeholder was replaced, because probe P7 and verify_handoff_probes' answer-hint rung require the ship-gate verdict / WARN count / drifted id to be ABSENT from the bundle. PROBES.md is excluded from BUNDLE_FILES. Is this argument sound and are the two pinning tests sufficient?
- ecosystem/doc-code-edge.yaml exempt entry: is xempt the right classification for a check whose enforced rule is not yet written in any protocol doc, versus annotating coverage_scope?
- audit.py adapter: FAIL-class per region, fail-soft to WARN on exception, Finding evidence markdown-table-safe (no pipe).

---

## Findings
## CRITICAL

(none)

## HIGH

### HIGH — scripts/validate_residual_completeness.py:55 — Supported bundle shapes bypass the gate

**What:** `BUNDLE_FILES` excludes `HANDOFF_BOOT.md`, `EPIC_BOOT.md`, and `FUNCTIONAL_BOOT.md`; epic and functional placeholders also use `_FILL-IN ..._`, which the predicate does not recognize.  
**Why:** Supported bundles can ship entirely unfilled hand-authored regions without producing a FAIL.  
**Fix direction:** Scan every FILL-IN carrier except `PROBES.md`, recognize both live placeholder forms, and add untracked epic/functional bundle tests.

### HIGH — scripts/validate_residual_completeness.py:65 — Placeholder regex can consume authored prose

**What:** With `DOTALL`, `.*?` expands to the final `)_`, so `_(fill: placeholder)_\n_(authored prose)_` is incorrectly classified as placeholder-only.  
**Why:** Legitimately authored content can falsely block commits, contradicting the tested contract that a remaining placeholder plus real prose counts as filled.  
**Fix direction:** Require the first placeholder terminator to end the body, and add a regression test for authored prose ending in `)_`.

## MEDIUM

(none)

## LOW

(none)
