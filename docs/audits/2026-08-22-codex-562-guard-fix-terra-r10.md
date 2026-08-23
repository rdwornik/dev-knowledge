# Codex Review — 562-guard-fix-terra-r10

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `f56353e3`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 10 on scripts/nopack_sandbox.py. Round 9
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r9.md) found 1 Critical / 0 High; this
  diff closes it: read_metadata_file checks every path component for symlinks, resolves
  the target and requires containment before reading; read_marker and _load both use it.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- The module docstring states residual limits deliberately. Flag anything NOT honestly
  covered by them. If nothing remaining rises to Critical or High, SAY SO EXPLICITLY -- a
  clean pass is a meaningful result here, not a failure to find something. Do not
  manufacture a Critical to have something to report.

---

## Findings
## Critical

- **scripts/nopack_sandbox.py:2381** — `_load` reads metadata before proving the supplied sandbox directory is contained by the configured root.

  **What:** `read_metadata_file()` treats `sandbox_path.resolve()` as its boundary, so `_load` can read a regular manifest from an arbitrary `--sandbox` directory (or an in-root symlink resolving outside) before `verify_provenance()` rejects it.
  
  **Why:** The control path can still access a file outside the sandbox clone; the prior symlink fix protects metadata below the supplied path, not the supplied path’s own provenance.
  
  **Fix direction:** Establish the configured sandbox root before reading metadata, require the resolved requested sandbox path to be contained by it (and reject a symlinked sandbox path), and do not infer that boundary from the unverified manifest.

## High

(none)

## Medium

(none)

## Low

(none)