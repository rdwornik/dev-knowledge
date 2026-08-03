# Codex Review — arc2-vacuous-green-trio

**Date:** 2026-08-03
**Branch:** `fix/arc2-vacuous-green-trio`
**HEAD:** `705b0bcf`
**Diff range:** `main..fix/arc2-vacuous-green-trio`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- gen_intake_index._parse_frontmatter: the regex->yaml.safe_load swap. Are the four documented contracts genuinely preserved (no leading ---, unterminated -> {}, keys lowercased, values coerced to stripped str)? Any input where the new parser returns something the old one did not, beyond the intended underscore-key fix?
- normalize_headers: this hook REWRITES FILES IN PLACE via pre-commit. Can _heading_lines + _split_keep_eol ever desync so a NON-heading line is rewritten, or a heading line be missed? Check the \r\n / \r / lone-\n handling against markdown_it normalization, and the fail-safe except.
- boundary_headers: fnmatch -> fnmatchcase. Does this narrow the governed set anywhere it should not?
- Tests: are any of the new tests vacuous, tautological, or asserting something they construct themselves? Especially the corpus tests and the "structural derivation" ones.

---

## Findings
## CRITICAL

## [CRITICAL] scripts/normalize_headers.py:100 — parser failures are silently swallowed

**What:** `except Exception` returns the original text without logging or failing the hook.  
**Why:** A dependency/API or programming failure makes the rewriting gate silently no-op while reporting success.  
**Fix direction:** Preserve the non-destructive behavior, but emit a clear diagnostic and avoid swallowing unexpected exceptions silently.

## HIGH

## [HIGH] tests/test_boundary_headers.py:417 — case-sensitivity regression test is host-dependent

**What:** The test only observes `fnmatchcase` on the current host; reverting to `fnmatch` still passes on Linux/macOS, where `fnmatch` is already case-sensitive.  
**Why:** CI can go green with the original Windows-only governed-set bug restored.  
**Fix direction:** Test the Windows case-folding behavior deterministically (or assert the selected matcher through an isolated seam).

## [HIGH] tests/test_normalize_headers.py:271 — corpus heading test is tautological and may exercise nothing

**What:** The assertion calls `_heading_lines`, the exact helper `normalize_text` uses to decide which lines to rewrite; if no current corpus file changes, its loop makes no assertions at all.  
**Why:** It cannot detect a heading-map/splitter desynchronization—the key safety claim for this in-place rewriter.  
**Fix direction:** Add a non-vacuous mixed-EOL fixture checked against an independently obtained token map, and require at least one corpus transformation if retaining the corpus assertion.

## MEDIUM

(none)

## LOW

(none)