# Codex Review — arc3-mechanical-adoptions

**Date:** 2026-08-03
**Branch:** `fix/arc3-mechanical-adoptions`
**HEAD:** `546d583b`
**Diff range:** `main..fix/arc3-mechanical-adoptions`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- toc/generator.parse_headers: replaced a `startswith("```")` fence toggle with markdown_it heading tokens, but EXTRACTION still uses the old _HEADER_RE against the raw source line. Can the token map index and the _EOL_RE split ever desync so _HEADER_RE is applied to the WRONG line? Any case where the new parser DROPS a header the old one correctly found (the stated safety property)?
- Does routing extraction through _HEADER_RE silently change the generated TOC for any file (levels, text, tag stripping, dedup/anchor behaviour)?
- floor_conformance._rmtree_guarded: onerror -> onexc. Is the callback signature correct under onexc (exception instance, not exc_info tuple)? Any behaviour change on the read-only-packfile retry path?
- Tests: are any of the new tests vacuous, tautological, or asserting something they construct themselves? The corpus test embeds a copy of the OLD algorithm as a reference implementation - is that sound, and is the test non-vacuous? Is the "non-regression, not distinguishing" labelling in the floor tests accurate?

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/toc/generator.py:73 — token gate drops legacy headers outside fences

**What:** `heading_open` excludes `##`/`###` lines inside CommonMark HTML blocks/comments; the prior raw-line parser included them.  
**Why:** This violates the claimed fence-only/safety property and can silently remove TOC entries (and shift duplicate-anchor numbering).  
**Fix direction:** Use markdown-it solely to identify fenced ranges, or explicitly change the compatibility contract and cover these contexts.

## [HIGH] tests/test_toc.py:302 — corpus safety comparison loses duplicate occurrences

**What:** `h not in fixed` tests membership, not header occurrence counts.  
**Why:** Legacy `[(2, "Foo"), (2, "Foo")]` versus fixed `[(2, "Foo")]` passes despite a lost TOC row/`#foo-1` anchor. The corpus test is non-vacuous, but not fully sound.  
**Fix direction:** Compare multisets/order-preserving occurrences and add an HTML-block duplicate-header case.

## Medium

(not assessed — default diff review is Critical/High only)

## Low

(not assessed — default diff review is Critical/High only)

The token-map/EOL split is aligned for LF, CRLF, and CR-only input; I found no index-desync case. `onexc`’s callback signature is correct, and its retry behavior is unchanged. The floor tests’ “non-regression, not distinguishing” label is accurate.