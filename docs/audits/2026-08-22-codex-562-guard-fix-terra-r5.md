# Codex Review — 562-guard-fix-terra-r5

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `1a4852f5`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/1/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 5 on scripts/nopack_sandbox.py. Round 4
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r4.md) found 4 Critical / 1 High; this
  diff closes them: _resolves_outside resolves existing operands at exec time;
  _pattern_positions models -e (data) vs -f (file); _option_forms/_attached_value handle
  attached and bundled short options and sort's write modes; GPG paths removed; probe()
  positive controls now require rc==0 and non-empty output.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- Residual limits are stated deliberately in the module docstring. Flag anything NOT
  honestly covered by them, and say so if you believe the remaining findings are below
  Critical/High.

---

## Findings
## Critical

## [CRITICAL] scripts/nopack_sandbox.py:2155 — `exec` accepts an arbitrary directory as its sandbox

**What:** `_load()` uses the caller-supplied `--sandbox` path without validating containment, marker, manifest provenance, or `postcondition_clean`; with no manifest it only emits a warning.  
**Why:** `exec --sandbox <outside-dir> -- "cat secret"` runs with that outside directory as `cwd`, so a relative operand reads outside the provisioned clone. This is not one of the stated residual limits.  
**Fix direction:** Refuse `exec`/`probe` unless the resolved sandbox is a registered, marked, clean provisioned descendant of its recorded sandbox root; do not offer a degraded execution mode.

## [CRITICAL] scripts/nopack_sandbox.py:1628 — attached file-valued options bypass symlink containment

**What:** `_resolves_outside()` immediately ignores every token beginning with `-`, including options such as `grep --file=escape`, whose attached value is an opened file.  
**Why:** If `escape` is a sandbox symlink to a host file, the lexical check passes and `grep --file=escape CLAUDE.md` reads the host path. The new symlink protection covers only bare operands, not attached option operands.  
**Fix direction:** Parse file-valued option arguments into their actual path values, then resolve and contain those values before execution; add an execution-level symlink regression test for `--file=` and attached short forms.

## High

## [HIGH] scripts/nopack_sandbox.py:1938 — piped positive controls can pass after an upstream failure

**What:** `run_guarded()` overwrites `returncode` for each pipeline stage and returns only the final stage’s status; `probe()` then accepts any non-empty final output.  
**Why:** A control such as `cat missing | wc -l` returns `0\n` with final status 0 and passes, although the intended read failed. This contradicts the test’s stated pipeline-vacuity goal and affects the default `ls … | wc -l` control.  
**Fix direction:** Preserve and report any stage failure (or require per-stage success) when evaluating controls, with a regression test for a failing upstream stage plus non-empty downstream output.

## Medium

(none)

## Low

(none)