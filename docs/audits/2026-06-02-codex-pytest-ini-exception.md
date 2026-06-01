# Codex Review — pytest-ini-exception

**Date:** 2026-06-02
**Branch:** `chore/universalization-upstream-support`
**HEAD:** `ff677c5`
**Diff range:** `main..chore/universalization-upstream-support`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

- audit.py: pytest.ini added to _DOT_PREFIX_EXCEPTIONS — correct set semantics, no regression to check_dot_prefix_discipline
- test_audit.py: new exemption test + extended pass-case — assertions meaningful, not vacuous
- Scope: confirm the change is minimal and the exception logic matches ADR-59 intent (root-only, exact-name match)

---

## Findings
## Critical
(none)

## High
(none)

## Medium
(none)

## Low
(none)

I found no issues in the scoped diff.

The `pytest.ini` change in [scripts/audit.py](/C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:57) is minimal and matches ADR-59’s 2026-06-02 amendment: the exemption is an exact-name match via `p.name in _DOT_PREFIX_EXCEPTIONS`, and `check_dot_prefix_discipline()` remains root-only because it iterates `repo_path.iterdir()` and skips subfolders. There is no regression that would broaden the rule beyond root-level `pytest.ini`.

The new tests in [tests/test_audit.py](/C:/Users/1028120/Documents/Dev/.dev-knowledge/tests/test_audit.py:263) are meaningful rather than vacuous. The extended pass-case proves `pytest.ini` coexists with existing dotted/exempt files, and the dedicated exemption test would fail if `pytest.ini` were not on the exact-name exception list. Residual gap: there is still no explicit negative test for a near-miss name like `pytest-local.ini`, but that is a coverage improvement, not a defect in this diff.
