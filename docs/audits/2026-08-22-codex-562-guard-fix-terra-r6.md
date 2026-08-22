# Codex Review — 562-guard-fix-terra-r6

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `9cbc1ac7`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 3/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 6 on scripts/nopack_sandbox.py. Round 5
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r5.md) found 2 Critical / 1 High; this
  diff closes them: _load now requires a manifest and runs verify_provenance +
  postcondition_clean with no degraded mode; _resolves_outside resolves attached option
  values; GuardedResult carries stage_returncodes and probe() requires no stage failed.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- Residual limits are stated deliberately in the module docstring. Flag anything NOT
  honestly covered by them, and say explicitly if you believe nothing remaining rises to
  Critical or High.

---

## Findings
## Critical

## [CRITICAL] scripts/nopack_sandbox.py:1585 — Short attached option values can still read outside the sandbox

**What:** `_attached_value()` greedily treats alphanumeric attached values as part of the option name, so `grep -fescape …` is not checked as reading `escape`; on Windows, `grep -fC:\host\secrets …` is likewise not recognized as an absolute path.  
**Why:** A symlinked `escape` or a Windows absolute path lets an allowlisted command open a host file outside the clone.  
**Fix direction:** Parse short options with command-aware argument arity, retaining the entire value after an option that consumes one; add `-fescape` symlink and `-fC:\…` regressions.

## [CRITICAL] scripts/nopack_sandbox.py:269 — Recursive symlink-following modes bypass operand containment

**What:** The guard permits options such as `find -L .`, `grep -R pattern .`, and `rg --follow pattern .`.  
**Why:** Their explicit operands are inside the sandbox, but they dereference a symlink encountered during traversal and read outside the clone. This is not one of the documented residual limits.  
**Fix direction:** Refuse symlink-dereferencing traversal flags for all allowlisted recursive readers, with execution-level symlink traversal tests.

## [CRITICAL] scripts/nopack_sandbox.py:1907 — Direct API callers can bypass `_load()` provenance checks

**What:** `run_guarded()` accepts a raw `Path` and treats it as the sandbox cwd without validating a manifest, provenance, registry, or postcondition.  
**Why:** A direct integration can call `run_guarded(Path(outside), ...)` and read relative host files, bypassing the newly hardened CLI `exec` path.  
**Fix direction:** Require a verified sandbox object at this boundary, or perform the same provenance and clean-postcondition validation before every guarded execution.

## High

(none)

## Medium

(none)

## Low

(none)