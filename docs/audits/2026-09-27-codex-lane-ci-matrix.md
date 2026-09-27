# Codex Review — lane-ci-matrix

**Date:** 2026-09-27
**Branch:** `worktree-lane-ci-matrix`
**HEAD:** `4ad29e44`
**Diff range:** `main..worktree-lane-ci-matrix`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. Verified against the Findings section below: one High (ruleset context mismatch), zero elsewhere. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: to-cc/LANE-5B4-3-ci-matrix.md (contract) -- WAVE5B-N4 lane-ci-matrix (proposal row L1).
Diff: .github/workflows/conductor.yml, tests/test_conductor.py against origin/main.
Focus:
- The pytest job's strategy.matrix + fail-fast:false + runs-on: matrix.os is correct GitHub Actions syntax.
- defaults.run.shell: bash is job-level and covers every run: step including the new local-main-ref step.
- The local `main` ref step (git branch main origin/main) runs after checkout and before every step that needs refs/heads/main, and is idempotent/safe if refs/heads/main already exists (push to main itself).
- The per-OS artifact name (pytest-${{ matrix.os }}-${{ github.sha }}) actually avoids the v4 upload-artifact duplicate-name refusal across the two matrix legs.
- Push trigger branches [main, worktree-**, epic/**] -- does this silently drop any previously-covered branch shape, and does epic/** collide with anything.
- tests/test_conductor.py's new/updated assertions actually pin the above (not vacuously true).

---

## Findings
## Critical

(none)

## High

### .github/workflows/conductor.yml:91 — matrix renames the required pytest check contexts

**What:** The matrix emits `pytest (ubuntu-latest)` and `pytest (windows-latest)`, while the existing ruleset still requires `pytest`.  
**Why:** If the declared ruleset is enabled, it will wait for a `pytest` context that this workflow no longer produces, blocking protected-branch updates. `tests/test_conductor.py:575` only compares required-context strings to job IDs, so it misses this mismatch.  
**Fix direction:** Update the required-check contract for both matrix contexts (or add an aggregate job named `pytest`) and test the actual matrix-generated context names.

## Medium

(none)

## Low

(none)