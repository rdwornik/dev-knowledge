# Codex Review — lane-portability-ratchet-repair-1

**Date:** 2026-09-28
**Branch:** `worktree-lane-portability-ratchet`
**HEAD:** `fb00e01b`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- REFUSED-lane-portability-ratchet.md item 1 (the 8th id): scripts/preflight_contract.py's
  _OFF_REPO_PATH_RE POSIX-root branch now accepts a backslash root separator, matching what
  _expand_off_repo already normalises downstream -- check this doesn't over-match ordinary
  prose (false positives) or under-match a real citation.
- Repair does not touch logs/KNOWN-REDS-REGISTRY.json, tasks/, or any file outside the
  contract's Files you own list -- verify no such edits are present in this diff.

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/platform_skip_ratchet.py:355 — Baseline can be rebased in the same diff

**What:** `--write-baseline` accepts a missing or detector-mismatched prior baseline, allowing a change to add a platform skip and commit it in the new baseline.  
**Why:** The live check only compares the working tree to that working tree’s baseline, so the stated shrink-only contract can be bypassed silently.  
**Fix direction:** Add a merge-base/target-branch comparison that rejects added baseline site keys and detector-rebase bypasses.

## Medium

(none)

## Low

(none)

Scope check: no changes were present under `logs/KNOWN-REDS-REGISTRY.json` or `tasks/`. The only diff path outside the requested code list is `docs/audits/2026-09-27-codex-lane-portability-ratchet.md`, which I did not review.