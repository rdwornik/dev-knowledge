# Codex Review — dynamic-toc

**Date:** 2026-06-03
**Branch:** `feat/dynamic-toc`
**HEAD:** `5e7a92c`
**Diff range:** `main..feat/dynamic-toc`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

- scripts/toc/ generator package mirrors scripts/codemap/ — verify the mirror is faithful (CLI, exit codes 0/1/2/3, fail-on-stale check model)
- GitHub anchor slugging correctness: full-header slug (## Purpose [CORE] -> #purpose-core), double-hyphen on removed '&' preserved, [TAG] stripped from display text only, dup-anchor -1/-2
- fenced code-block skipping in parse_headers (triple-backtick toggling); h1 and h4+ excluded
- marker-block replacement whitespace contract vs codemap (leading newline, do-not-edit comment, END on own line)
- toc-freshness pre-commit hook wiring: files filter, pass_filenames false, default_stages applies, standalone (not an audit.py check)

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/toc/cli.py:26 — unreadable input bypasses exit-code contract

**What:** `_cmd_generate()` calls `generate_toc(md_file)` before wrapping file reads in error handling.  
**Why:** If the markdown file exists but cannot be read or decoded, the CLI raises a traceback instead of returning exit code `2`, breaking the codemap mirror contract and pre-commit failure model.  
**Fix direction:** Catch read/generation `OSError`/decode failures in the generate path and return `2` with a concise stderr error, matching codemap.

## Medium

(none)

## Low

(none)

Tests not run; review was read-only.
