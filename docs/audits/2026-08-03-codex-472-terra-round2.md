# Codex Review — 472-terra-round2

**Date:** 2026-08-03
**Branch:** `feat/472-declaration-anchor`
**HEAD:** `d0d58549`
**Diff range:** `main..feat/472-declaration-anchor`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Round 2. Round 1 raised 1 HIGH (prefix-id collision + fenced markers), fixed in d0d58549.
- Verify the FIX: _DECL_START_RE / _DECL_END_RE are now full-line with a lookahead id boundary, and markers on fenced lines are ignored via toc.generator._code_line_indices. Any remaining way to read the WRONG block, or to reject the REAL one? Consider: the live ADR block content is itself inside a fence between the markers (must still parse), CRLF input, a marker with trailing spaces, an end marker before a start, indented markers, and an id that is a SUFFIX or contains the anchor id.
- Is importing toc.generator._code_line_indices into audit.py sound (private cross-module symbol, import cost on the audit-health pre-commit path, any circular-import risk)?
- _declaration_agreement: still catches both drift directions and duplicates after the change?
- The two bumped line pins in tests/test_reverse_dep_oracle.py - correct values, and is the third pin genuinely not live?
- Any vacuous or self-constructing assertions among the three new fixtures?

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:3259 — Package-mode audit invocation cannot import the fence helper

**What:** `from toc.generator import _code_line_indices` only resolves when `scripts/` is on `sys.path`; `python -m scripts.audit` instead has the repo root on it.  
**Why:** The supported package-mode `audit health` crashes with `ModuleNotFoundError` when it reaches this hub check.  
**Fix direction:** Use the established package/script dual-import pattern (`scripts.toc.generator` with script-mode fallback) and add a package-mode regression test.

### tests/test_reverse_dep_oracle.py:218 — Declaration-exclusion assertion still uses the old source line

**What:** `Finding` now starts at `scripts/audit.py:322`, but the negative assertion still excludes line 321.  
**Why:** If the oracle regresses and returns the declaration as a reverse dependent, it would return line 322 and this test would still pass.  
**Fix direction:** Update the exclusion assertion to line 322, matching the live declaration location.

## Medium

(none)

## Low

(none)

The two bumped definition pins (lines 79 and 215) are correct. The `:312` formatting fixture is hand-constructed and not live; the stale line 321 exclusion above is a separate live pin. The revised marker logic correctly handles the requested prefix/suffix cases, fenced marker examples, CRLF normalization, trailing whitespace, indentation/code blocks, and end-before-start; the fenced live payload remains parsed.