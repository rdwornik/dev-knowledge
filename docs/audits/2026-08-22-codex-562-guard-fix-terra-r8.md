# Codex Review — 562-guard-fix-terra-r8

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `60b87e12`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 8 on scripts/nopack_sandbox.py. Round 7
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r7.md) found 2 Critical / 0 High; this
  diff closes them: ls/diff dereference modes refused; _resolve_executable resolves the
  program from the trusted PATH to an absolute path and refuses any resolution inside the
  sandbox root.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything, and whether any check can still pass VACUOUSLY.
- The module docstring states residual limits deliberately. Flag anything NOT honestly
  covered by them. If nothing remaining rises to Critical or High, say so explicitly.

---

## Findings
## Critical

- **scripts/nopack_sandbox.py:2033** — Bare-`Path` execution drops the sandbox denylist.

  **What:** `run_guarded(..., sandbox.path)` sets `names` to an empty set instead of loading the verified manifest’s `denied` entries.  
  **Why:** This intended library route permits history output such as `git log --stat -1` to disclose stripped artifact paths, and can expose Class-A history blobs that do not match a canary. It violates the stated Layer A/Layer B guarantees.  
  **Fix direction:** Rehydrate and verify manifest metadata for `Path` inputs (or require a fully loaded `Sandbox`), and add a regression test for history/path disclosure through `sandbox.path`.

- **scripts/nopack_sandbox.py:2335** — `--manifest` is read from an arbitrary host path before provenance is checked.

  **What:** `_load()` accepts `manifest_path` verbatim and calls `candidate.read_text()` before proving that it is the sandbox’s in-tree manifest.  
  **Why:** `exec`/`probe` can read outside the sandbox clone through their own control path, contrary to the claimed read boundary; this residual is not documented.  
  **Fix direction:** Require the manifest to resolve exactly to the verified sandbox’s metadata path, rejecting external paths and symlink escapes before opening it; cover explicit external-manifest inputs in tests.

## High

(none)

## Medium

(none)

## Low

(none)