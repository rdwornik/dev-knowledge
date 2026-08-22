# Codex Review — 562-guard-fix-terra-r11

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `6f912cd0`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 11 on scripts/nopack_sandbox.py. Round 10
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r10.md) found 1 Critical / 0 High;
  this diff closes it: _load resolves the sandbox root from caller/env/default only,
  refuses a symlinked sandbox path, and requires containment BEFORE reading any metadata;
  the manifest's own sandbox_root is never consulted; run_guarded takes sandbox_root.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- The module docstring states residual limits deliberately. Flag anything NOT honestly
  covered by them. If nothing remaining rises to Critical or High, SAY SO EXPLICITLY -- a
  clean pass is a meaningful result, not a failure to find something. Do not manufacture
  a Critical to have something to report.

---

## Findings
## Critical

## [CRITICAL] scripts/nopack_sandbox.py:273 — Indirect filename streams can read outside the sandbox

**What:** Allowlisted tools still accept host paths through stdin/list files, e.g. `printf '/etc/passwd\n' | file -f -`; `find -files0-from -`, `wc --files0-from=-`, and checksum `--check -` modes are likewise not blocked.  
**Why:** `_screen_paths()` validates argv operands only, while these modes interpret piped bytes as filenames; Layer B will return non-canary host content. This is outside the docstring’s stated residual write-mode limit.  
**Fix direction:** Refuse all filename-list/checkfile input modes (including stdin variants) for allowlisted tools, or remove those tools, and add execution-level regressions.

## [CRITICAL] scripts/nopack_sandbox.py:1803 — Git “read” allowlist permits mutation and an editor launch

**What:** `git symbolic-ref HEAD refs/heads/main` is accepted despite mutating `.git/HEAD`; it can attach the detached sandbox, after which the also-accepted `git branch --edit-description` can launch Git’s editor.  
**Why:** This executes a program outside the guarded argv surface and can read host editor configuration. It is not merely an unmodelled write contained in the disposable clone.  
**Fix direction:** Parse `symbolic-ref` into explicit read-only forms and use per-subcommand flag allowlists for `branch`/other “bare listing” commands; add regressions for this sequence.

## High

(none)

Medium and Low were not assessed, per the repository’s diff-review mode.