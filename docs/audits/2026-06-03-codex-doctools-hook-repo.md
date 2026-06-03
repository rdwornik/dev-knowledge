# Codex Review — doctools-hook-repo

**Date:** 2026-06-03
**Branch:** `feat/doctools-hook-repo`
**HEAD:** `cece0d0`
**Diff range:** `main..feat/doctools-hook-repo`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- codemap --arch-file parametrization backward-compatible (default still <repo>/ARCHITECTURE.md)?
- scripts/codemap_hook.py + toc_hook.py sys.path insertion correct for import resolution inside a cloned hook repo?
- .pre-commit-hooks.yaml hook ids/stages/pass_filenames/files correct; generate hooks manual-only?

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH .pre-commit-hooks.yaml:26 — hook entry targets non-executable script

**What:** `language: script` invokes `scripts/codemap_hook.py`, but the new wrapper files are committed as mode `100644`, not executable.  
**Why:** POSIX consumers of the cloned hook repo will fail to execute the hook entry directly, making `codemap-freshness` and `codemap-generate` unusable.  
**Fix direction:** Commit `scripts/codemap_hook.py` and `scripts/toc_hook.py` with executable mode, or use an entry form that explicitly invokes Python.

## HIGH .pre-commit-hooks.yaml:44 — TOC hook has the same executable-mode failure

**What:** `toc-freshness` and `toc-generate` also invoke `scripts/toc_hook.py` through `language: script`, while that file is committed as mode `100644`.  
**Why:** The TOC hooks will fail the same way in cloned pre-commit hook repos on POSIX systems.  
**Fix direction:** Make the wrapper executable in git or change the hook entry to call Python explicitly.

## MEDIUM

(none)

## LOW

(none)
