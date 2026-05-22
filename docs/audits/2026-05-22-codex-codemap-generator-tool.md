# Codex Review — codemap-generator-tool

**Date:** 2026-05-22
**Branch:** `feat/codemap-generator-tool`
**HEAD:** `5445270`
**Diff range:** `main..feat/codemap-generator-tool`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
## CRITICAL

## [CRITICAL] scripts/codemap/cli.py:47 — CLI writes into `ARCHITECTURE.md` from `scripts/`

**What:** The new `generate --write` path mutates `ARCHITECTURE.md` via `arch_file.write_text(...)`.
**Why:** This repo’s architectural invariant is that Layer 2 `scripts/` are read-only validators; adding a mutating path is an architectural invariant violation and breaks the “passive storage / no execution” contract for this repository.
**Fix direction:** Remove the in-place write mode from this repo’s `scripts/` tooling, or move any mutating codemap generator outside Layer 2 so the validator here remains read-only.

## HIGH

## [HIGH] scripts/codemap/check.py:27 — `ARCHITECTURE.md` reads are unguarded

**What:** `check_codemap()` calls `arch_file.read_text(...)` without handling `OSError` or decode failures.
**Why:** A permission/encoding problem will crash the command with a traceback instead of returning a controlled status code, which makes the check path brittle for the main file it is supposed to validate.
**Fix direction:** Catch the expected file-read exceptions and convert them into an explicit error return, consistent with the function’s documented exit-code behavior.

## [HIGH] scripts/codemap/cli.py:30 — write-mode file I/O is unguarded

**What:** The `generate --write` path reads and writes `ARCHITECTURE.md` without handling `OSError` or decode failures.
**Why:** On read-only files, permission issues, or encoding problems, the CLI will abort with an unhandled traceback instead of emitting a user-facing error code, which is especially risky on the only mutating path in the tool.
**Fix direction:** Wrap the read/write operations in targeted file-I/O exception handling and return explicit nonzero exit codes with stderr messages.

## MEDIUM

(none)

## LOW

(none)
