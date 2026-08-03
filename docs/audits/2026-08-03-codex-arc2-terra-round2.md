# Codex Review — arc2-terra-round2

**Date:** 2026-08-03
**Branch:** `fix/arc2-vacuous-green-trio`
**HEAD:** `405ffdcb`
**Diff range:** `main..fix/arc2-vacuous-green-trio`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Round 2. Round 1 raised 1 CRITICAL + 2 HIGH; all three were fixed in commit 98d973d0. Verify the FIXES, and look for anything round 1 missed.
- normalize_headers: the parse-failure path now prints to stderr and still returns text unchanged, exit 0. Is that genuinely non-destructive AND visible? Is `except Exception` still hiding anything it should not?
- test_boundary_headers: the case-sensitivity test now monkeypatches os.path.normcase to str.lower to simulate Windows on any host. Is that a sound simulation, and does the test now fail on Linux if the module reverts to fnmatch?
- test_normalize_headers: the corpus tests were rebuilt to use an independent ATX oracle and to DEMOTE headings first so they are non-vacuous. Are they now genuinely non-vacuous and non-tautological? Is the container-prefix / setext-underline handling in _looks_like too permissive to detect a real desync?
- Any remaining tautology, vacuous assertion, or test that constructs the thing it asserts.

---

## Findings
## CRITICAL

(none)

## HIGH

### tests/test_normalize_headers.py:274 — Container-prefix oracle accepts invalid list syntax

**What:** `_CONTAINER_PREFIX_RE` permits list markers with no required following whitespace, so `-# ordinary text` is stripped to `# ordinary text` and accepted as an ATX heading.  
**Why:** A real parser/splitter index desync landing on such prose can pass the claimed independent heading-map check, masking a rewriter regression.  
**Fix direction:** Model container prefixes with CommonMark-valid list-marker spacing (and add a negative desync case such as `-# ...`) rather than stripping arbitrary marker runs.

## MEDIUM

(none)

## LOW

(none)