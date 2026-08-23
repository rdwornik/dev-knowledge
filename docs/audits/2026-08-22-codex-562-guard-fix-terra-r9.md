# Codex Review — 562-guard-fix-terra-r9

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `64c22552`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 9 on scripts/nopack_sandbox.py. Round 8
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r8.md) found 2 Critical / 0 High; this
  diff closes them: run_guarded rehydrates a verified Sandbox for bare-Path and
  denylist-less inputs; _load refuses a manifest_path that is not the sandbox's own.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- The module docstring states residual limits deliberately. Flag anything NOT honestly
  covered by them. If nothing remaining rises to Critical or High, SAY SO EXPLICITLY --
  a clean pass is a meaningful result here, not a failure to find something.

---

## Findings
## Critical

- **scripts/nopack_sandbox.py:2340** — A symlinked in-tree manifest can still read an arbitrary host file before provenance verification.

  **What:** `_load()` resolves the default manifest path but never requires its target to remain inside the sandbox; `candidate.read_text()` runs before `verify_provenance()`.
  **Why:** An unprovisioned `--sandbox` directory can make `.git/nopack/manifest.json` a symlink to a host JSON file. The control path then reads outside the clone, contradicting the stated boundary.
  **Fix direction:** Reject symlinked metadata components and require the resolved marker/manifest targets to be contained in the resolved sandbox before reading either file.

## High

(none)

## Medium

(none)

## Low

(none)