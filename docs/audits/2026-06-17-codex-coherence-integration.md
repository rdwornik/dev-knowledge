# Codex Review — coherence-integration

**Date:** 2026-06-17
**Branch:** `feat/coherence-integration`
**HEAD:** `b5c4981`
**Diff range:** `main..feat/coherence-integration`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- Edge->flag bridge (enumerate_from_edge / enumerate_repo): path resolution under a repo_root, no stub leakage
- Spec-version parser dedup: parse_spec_version tolerance vs _numeric_version normalization; three consumers (checker numeric / enumerator full-text / nudge equality) preserved
- coherence_nudge _extract_version None-coalescing of "" (unparseable) — should_nudge correctness
- Removal of SpecSource.version_re — any missed consumer
- Closure-gate test correctness: does it actually prove drift-detected + missed sites enumerated by category, not a vacuous pass

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH scripts/coherence_nudge.py:52 — nudge compares raw version text after parser dedup

**What:** `_extract_version()` now returns the full `Version:` value, so `should_nudge()` compares raw strings instead of the previous numeric capture.
**Why:** A content change with semantically unchanged version text like `v5.2` -> `5.2` can now suppress the forgotten-version-bump nudge, letting coherence drift pass silently.
**Fix direction:** Keep `parse_spec_version()` shared, but normalize the nudge comparison through the same numeric normalization used by the checker while still coalescing unparseable `""` to `None`.

## HIGH scripts/coherence_enumerator.py:35 — package import mode is broken

**What:** The new `import validate_reconciliation as vr` only works when `scripts/` is on `sys.path`.
**Why:** Importing as `scripts.coherence_enumerator` or running `python -m scripts.coherence_enumerator` from repo root will fail with `ModuleNotFoundError`, unlike `audit.py` and `coherence_nudge.py` which support package/direct modes.
**Fix direction:** Use the same package-first/direct-fallback import pattern already used in the neighboring scripts.

## MEDIUM

(none)

## LOW

(none)
