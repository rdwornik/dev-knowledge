# Codex Review — 562-guard-fix-terra-r3

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `d09a78fa`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 3/1/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 3 of a repair lane on scripts/nopack_sandbox.py. Round 2
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r2.md) found 2 Critical / 1 High;
  this diff closes them: _screen_git parses git pre-command options and allowlists read
  subcommands; _sed_script_is_read_only enforces a read-only sed grammar; the registry
  takes a per-root lock and lands via os.replace.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone, or execute
  anything, via any allowlisted tool.
- The module docstring states residual limits deliberately (allowlist completeness, the
  check-to-delete race on Windows, marker/registry forgeability by a root writer). Flag
  anything NOT honestly covered by them.

---

## Findings
## Critical

## [CRITICAL] scripts/nopack_sandbox.py:1612 — Literal path operands can read outside the clone

**What:** The guard expands only globs; it never confines ordinary path arguments, so commands such as `cat ../secret`, `ls /`, `find ..`, and `sed -n '1p' /etc/passwd` are allowed and execute from the host filesystem.  
**Why:** Setting `cwd` to the sandbox is not a filesystem boundary; this defeats the stated read-surface containment.  
**Fix direction:** Parse and constrain path-bearing arguments for every retained tool (including symlink traversal), or reduce the surface to wrappers that can enforce sandbox-rooted reads.

## [CRITICAL] scripts/nopack_sandbox.py:1489 — Compact `sed -eSCRIPT` bypasses the script grammar

**What:** `_sed_scripts()` does not recognize the valid compact option form, e.g. `sed -e'1w /tmp/out' file` or `sed -e'1e command' file`, so it returns no script to validate.  
**Why:** GNU sed treats the remainder of `-eSCRIPT` as its program, permitting both an outside-sandbox write and command execution.  
**Fix direction:** Parse short options with attached operands and validate every form sed accepts; add regression tests for compact `-e` write and `e` programs.

## [CRITICAL] scripts/nopack_sandbox.py:1427 — Allowed Git options can launch external programs

**What:** The Git subcommand allowlist accepts all options for read subcommands, including `git help --web`, `git diff --ext-diff`, and forced pagination via `git -p log`.  
**Why:** These modes can invoke a browser, external diff helper, or configured pager; the subprocess also inherits host Git environment/configuration.  
**Fix direction:** Deny Git modes that invoke helpers, force a scrubbed Git environment and `--no-pager`, and allow only audited per-subcommand option sets.

## High

## [HIGH] scripts/nopack_sandbox.py:672 — A live registry lock can be stolen after 10 seconds

**What:** Any waiter unlinks the lock after its own timeout without establishing that the holder died.  
**Why:** A paused or slow holder can resume concurrently, overwrite a newer registry update, and remove another holder’s lock, losing sandbox registrations and leaving later teardowns unable to clean up.  
**Fix direction:** Use ownership-verified locking with safe stale-lock recovery, or fail rather than breaking a lock whose holder cannot be proven dead.

## Medium

(none)

## Low

(none)