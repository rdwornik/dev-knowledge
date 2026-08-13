# Codex Review — w3-landing-predicate

**Date:** 2026-08-13
**Branch:** `worktree-lane-c-513-landing-predicate`
**HEAD:** `cec9a533`
**Diff range:** `main..worktree-lane-c-513-landing-predicate`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:2730 — CommonMark line-map mismatch breaks fenced-import filtering

**What:** The `markdown_it` token line ranges are applied to `text.splitlines(keepends=True)`, which recognizes Unicode line separators that CommonMark does not.  
**Why:** A Unicode separator before a valid fence shifts indices, so `@imports` inside that fence are scanned as live and can falsely fail the blocking `import_edges` check.  
**Fix direction:** Split source lines with the same CR/LF/CRLF semantics used by `scripts/toc/generator.py` before applying token maps.

**Disposition:** Fixed. `_blank_fenced_code_blocks` now splits on `_EOL_SPLIT_RE = re.compile(r"(\r\n|\r|\n)")` (the same predicate as `scripts/toc/generator.py`'s `_EOL_RE`), captured so each line's separator survives reconstruction. Verified directly: constructed both the pre-fix and post-fix implementations side by side and confirmed a two-U+2028-separator fixture leaks a fenced `@import` under the old `splitlines(keepends=True)` logic and does not leak under the fix; added as `tests/test_audit.py::test_import_edges_fence_survives_unicode_line_separator`, which fails against the pre-fix code and passes against the fix.

## Medium

(none)

## Low

(none)