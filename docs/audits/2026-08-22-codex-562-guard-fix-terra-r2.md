# Codex Review — 562-guard-fix-terra-r2

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `751f02d6`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/1/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 2 of a repair lane. Round 1 (docs/audits/2026-08-22-codex-562-guard-fix-terra.md)
  found 4 Critical / 1 High on scripts/nopack_sandbox.py; this diff closes them.
- Verify: interpreters removed from ALLOWED_ARGV0 + _FORBIDDEN_ARGS flag table; glob
  expansion now re-screened by screen_stages over the expanded argv; teardown re-verifies
  marker + dir identity before rmtree and requires a root-level registry entry;
  _meta_dir refuses symlinked components; _abort_provision reports a vanished dest.
- The module's docstring states three residual limits deliberately (allowlist completeness,
  check-to-delete race on Windows, marker/registry forgeability by a root writer). Judge
  whether those are honestly scoped, and flag anything NOT covered by them.

---

## Findings
The specified R2 repairs are present, but three merge-blocking issues remain.

## Critical

## [CRITICAL] scripts/nopack_sandbox.py:1310 — Git options with values bypass write-command detection

**What:** The Git parser skips option tokens but not their operands, so `git -C . config --global user.name x` treats `.` as the subcommand and permits a global-config write.  
**Why:** This breaks the read-only boundary and permits host-state modification; the same bypass can inject a shell-backed Git alias.  
**Fix direction:** Parse Git global options and their operands correctly, then allow only explicit read-only subcommands/options; add regressions for `-C . config --global` and `-c alias.x=!...`.

## [CRITICAL] scripts/nopack_sandbox.py:275 — Allowed `sed` scripts can write or execute outside the sandbox

**What:** Only `sed -i` is refused; scripts such as `sed '1w /outside/file' input` or GNU sed’s `e` command pass screening.  
**Why:** `w` accepts absolute paths and `e` executes commands, so the stated containment does not hold and `shell=False` is bypassed by the allowed tool itself. This is not honestly covered by the documented residual limit.  
**Fix direction:** Remove `sed` from the allowlist, or strictly support only a parsed, non-executing subset that rejects `w` and `e` commands; add external-write and execution regressions.

## High

## [HIGH] scripts/nopack_sandbox.py:600 — Sandbox registry updates are unsynchronised and non-atomic

**What:** Concurrent `register_sandbox`/`unregister_sandbox` calls perform read-modify-write without locking, and writes truncate the live registry directly.  
**Why:** Parallel provisions can lose entries or leave malformed JSON, causing later teardown to refuse and leave sandboxes behind.  
**Fix direction:** Serialize registry updates per root and write via an atomic replace; cover simultaneous provision/teardown behavior.

## Medium

(none)

## Low

(none)