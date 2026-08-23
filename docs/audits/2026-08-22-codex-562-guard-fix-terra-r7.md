# Codex Review — 562-guard-fix-terra-r7

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `f973af95`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 7 on scripts/nopack_sandbox.py. Round 6
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r6.md) found 3 Critical / 0 High; this
  diff closes them: _attached_values returns every suffix; _pattern_positions is an
  ordered short-option scan; symlink-following traversal flags refused;
  _require_provisioned runs at the execution boundary for Sandbox and bare Path alike.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- The module docstring states residual limits deliberately. Flag anything NOT honestly
  covered by them. If nothing remaining rises to Critical or High, say so explicitly.

---

## Findings
## Critical

### scripts/nopack_sandbox.py:254 — `ls -LR` can traverse symlinked directories outside the sandbox

**What:** `ls` is allowed but has no forbidden dereference flags, so `ls -LR .` passes screening.  
**Why:** `-L` follows symlinks and `-R` descends directories; a symlink within the clone can therefore enumerate host paths while operand checks see only `.`.  
**Fix direction:** Refuse `ls` dereference modes and add a `run_guarded("ls -LR .")` external-symlink regression test.

### scripts/nopack_sandbox.py:1416 — ambient `PATH` can replace any allowlisted command with an arbitrary executable

**What:** The child environment retains `PATH`/`PATHEXT`, while execution invokes bare names such as `cat` at line 2036.  
**Why:** A shadowing `cat.exe`/`git.exe` earlier on `PATH` executes outside the allowlist and can read or act outside the sandbox; Layer B only inspects returned text.  
**Fix direction:** Resolve commands from a controlled trusted tool location before execution, rather than inheriting ambient command resolution; add a shadowed-command regression test.

## High

(none)

## Medium

(none)

## Low

(none)