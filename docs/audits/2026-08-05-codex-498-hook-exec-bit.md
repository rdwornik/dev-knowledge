# Codex Review — 498-hook-exec-bit

**Date:** 2026-08-05
**Branch:** `fix/498-hook-exec-bit`
**HEAD:** `90089f36`
**Diff range:** `main..fix/498-hook-exec-bit`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Tally:** 0/0/0/0 (C/H/M/L)

---

> **Canonical review-artifact header ([#480] P3 ruling, 2026-08-05).** The `**Tally:**` line
> above is the shape ruled at the 2026-08-05 morning review and applies FORWARD-ONLY from that
> date; the legacy artifacts that predate it are immutable records and are never retro-edited.
> This artifact is the first written in the canonical shape — dogfooded on the arc that ruled it.

---

## Focus

- Is test_carried_script_entries_are_executable genuinely STRUCTURAL (covers a future carried script with no edit), or does it smuggle an enumeration?
- Is the non-vacuity guard correct and sufficient? Could the test still pass vacuously by another route (e.g. yaml shape change, entry key rename, a hook with language: script but no entry)?
- _tracked_mode reads git ls-files -s rather than the filesystem. Is that the right oracle on BOTH Windows and POSIX? Any failure mode where it returns a wrong/misleading mode (submodule, symlink 120000, intent-to-add, path with spaces, quoted/unicode path)?
- Is the docstring's scope claim ACCURATE — that scripts/block_unanchored_push.py occurs zero times in .pre-commit-hooks.yaml and is therefore out of scope by construction?
- The fix is git update-index --chmod=+x (mode-only, blob hash unchanged). Any way this regresses or is silently reverted (core.fileMode, a later git add on Windows, .gitattributes)?
- Fail-open risk: does _tracked_mode returning None on git error make the assertion PASS anything it should catch?

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

The new check is genuinely structural: it iterates all current and future `language: script` hook-source entries. Its non-vacuity assertion prevents a silent pass if none remain; malformed YAML/entries and git errors fail the test rather than pass. `git ls-files -s` is the appropriate cross-platform oracle for the tracked executable bit, and the `block_unanchored_push.py` scope note matches the current hook-source/configuration.