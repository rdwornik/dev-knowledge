# Codex Review — arc3-terra-round2

**Date:** 2026-08-03
**Branch:** `fix/arc3-mechanical-adoptions`
**HEAD:** `229c8813`
**Diff range:** `main..fix/arc3-mechanical-adoptions`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Round 2. Round 1 raised 2 HIGH, both fixed in 229c8813.
- toc/generator: the heading_open token gate was REPLACED by _code_line_indices (fence/code_block ranges) + the original _HEADER_RE over all other lines. Does that now genuinely preserve the pre-fix behaviour outside fences, including HTML blocks, unterminated HTML comments, link reference definitions, and setext underlines? Can it DROP any header the legacy toggle returned?
- Does _code_line_indices miss any CommonMark code construct that the legacy `startswith("```")` toggle DID skip, i.e. can the fix newly ADMIT a header from inside a code block?
- tests/test_toc.py: corpus comparison now uses Counter multiset difference. Sound? Non-vacuous? Are the two new tests (html block, duplicate occurrences) actually pinning the contract, or do they construct what they assert?
- Anything remaining in floor_conformance onexc.

---

## Findings
## Critical

(none)

## High

### tests/test_toc.py:308 — Corpus guard rejects an intentional parser correction

**What:** `Counter(legacy) - Counter(fixed)` requires every legacy header to remain, but the supported tilde-fence case at line 246 intentionally removes a legacy false-positive header.  
**Why:** Adding a valid `##` line inside a `~~~` code fence to any repository Markdown file will make this live-corpus test fail despite correct CommonMark behavior, blocking valid changes.  
**Fix direction:** Replace the “never drops” invariant with one compatible with intentional code-fence exclusions, while separately pinning the raw-line compatibility cases.

## Medium

(none)

## Low

(none)