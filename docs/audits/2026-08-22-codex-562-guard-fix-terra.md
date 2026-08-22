# Codex Review — 562-guard-fix-terra

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `4b63b4f0`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 4/1/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- This diff REPAIRS two Criticals a prior terra pass found in scripts/nopack_sandbox.py.
- Critical 1 was: teardown() recursively deleted any path handed to --sandbox. Verify the
  new containment + marker provenance actually closes it, including symlink escape and
  TOCTOU between the check and the rmtree.
- Critical 2 was: shell=True with a segment-only allowlist. Verify the new hand-written
  lexer + argv exec has no path back to a shell, no injection through glob expansion, and
  no way for a screened command to differ from the executed argv.
- Also verify the manifest/marker placement under .git/nopack cannot clobber, and that a
  failed provision cannot leave an unstripped clone on disk.

---

## Findings
## Critical

### scripts/nopack_sandbox.py:234 — Allowlisted tools can still execute shells and writes

**What:** `python`, `python3`, `awk`, `find`, and `xargs` are allowed without argument-level restrictions.  
**Why:** `python3 -c`, `awk system(...)`, `find -exec`, or `xargs sh` reintroduce arbitrary execution—including shells and filesystem writes—despite `subprocess.run(..., shell=False)`.  
**Fix direction:** Remove execution-capable tools from the read surface or enforce command-specific argument grammars that prohibit code execution, `-exec`, and spawned commands.

### scripts/nopack_sandbox.py:1156 — Glob expansion occurs after policy validation

**What:** The code validates the unexpanded `Stage.argv`, then expands globs and executes the resulting argv without rerunning argv0 and Git mutation checks.  
**Why:** A screened command can differ from the command executed; e.g., a glob in Git’s command position can expand to `commit`, or a globbed argv0 such as `*/python3` can select an unvalidated executable. Relative/absolute glob patterns can also expand outside the sandbox.  
**Fix direction:** Expand only sandbox-contained path arguments, prohibit globs in executable/subcommand positions, and rerun the complete structural policy over the final argv before execution.

### scripts/nopack_sandbox.py:894 — Teardown has a check-to-delete pathname race

**What:** `teardown()` validates containment and marker provenance, then calls `rmtree()` by pathname.  
**Why:** A concurrent rename or parent-symlink swap after `read_marker()` can replace the validated directory with another directory before deletion; the same race can make `_abort_provision()` treat a disappeared destination as successfully cleaned while the unstripped clone remains at its renamed location.  
**Fix direction:** Anchor deletion to verified directory handles/inodes with no-follow traversal, and make abort cleanup verify the original cloned object—not merely that its original pathname is absent.

### scripts/nopack_sandbox.py:475 — The marker is forgeable, so it is not proof of provenance

**What:** A “valid” marker only needs public JSON fields, a random-looking nonce, and the target’s own resolved path.  
**Why:** Any directory inside the configured root can be made deletable by adding a syntactically valid self-claiming marker; copying is rejected, but fabrication is not.  
**Fix direction:** Bind provenance to state outside the deletable tree that the sandbox cannot forge or alter, and verify it alongside the marker.

## High

### scripts/nopack_sandbox.py:489 — Metadata writes follow symlinked `.git/nopack` directories

**What:** `mkdir(..., exist_ok=True)` and `open(..., "x")` resolve parent-directory symlinks; `write_manifest()` repeats this at line 837.  
**Why:** A race or substituted `.git/nopack` symlink can redirect marker/manifest creation outside the sandbox. Exclusive creation prevents overwriting an existing final file, but does not prevent unintended external writes.  
**Fix direction:** Create and traverse metadata directories via trusted directory descriptors with no-follow checks, and reject any symlinked path component.

## Medium

(none)

## Low

(none)