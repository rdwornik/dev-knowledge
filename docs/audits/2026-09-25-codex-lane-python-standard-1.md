# Codex Review — lane-python-standard-1

**Date:** 2026-09-25
**Branch:** `worktree-lane-python-standard-1`
**HEAD:** `2228a574`
**Diff range:** `main..worktree-lane-python-standard-1`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: LANE-5B2-14-python-standard-1.md (this lane's frozen contract, WAVE5B-N2 row 14).
Diff: 12 ruff extend-select codes added to pyproject.toml + templates/ruff-config-block.toml
(FURB122, PLE2515, PLR1711, RET501, RUF010, RUF019, SIM300, SIM905, SIM910, UP012, UP033,
UP034), each measured at zero violations tree-wide; plus the safe auto-fixes (ruff --fix,
never --unsafe-fixes) that made them zero, restricted to scripts/+tests/ files no other
WAVE5B-N2 lane owns. Please check: (1) the two config files are byte-identical in their
extend-select list, (2) no owned-by-another-lane file was touched, (3) the auto-fixes are
mechanical/behavior-preserving (no hand-edited logic), (4) no # noqa suppression was
stripped incorrectly.

---

## Findings
## Critical

(none)

## High

### .devcontainer/provision.sh:552 — another lane’s Codespaces change is in this lane’s diff

**What:** `main..worktree-lane-python-standard-1` includes the `leg_pc_login_path` Codespaces repair (and matching provisioning/test changes), originating from `worktree-lane-codespace-proof-repair-1` via the merge of `origin/main`.

**Why:** This violates the frozen row-14 lint lane’s declared scripts/tests-only autofix scope, so the requested diff is not reviewable as a self-contained Ruff-standard change.

**Fix direction:** Refresh/reconcile the local `main` base (or review against the appropriate upstream base) so the lane diff contains only its owned Ruff configuration and mechanical autofixes.

**Disposition: tooling artifact, not a scope violation.** The wrapper's default diff range
(`main..HEAD`) resolved against this worktree's **local** `main`, which was frozen at this
lane's base commit `da11291b` and had not yet observed `worktree-lane-codespace-proof-repair-1`
landing on `origin/main` at `3d13a2d2`. The lane's actual, isolable contribution is verified via
`git log origin/main..HEAD`, which shows exactly two commits: the lane's own
`5e2ad0b8` (the 12-code ruff standard) and `2228a574` (`Merge origin/main into
worktree-lane-python-standard-1`, mandated by this batch's common rules §3 — sync only via
`git fetch origin` + `git merge origin/main`). `git merge-base --is-ancestor 3d13a2d2
origin/main` confirms the flagged devcontainer commits are already part of `origin/main`
itself, not something this lane introduced or cherry-picked. No file this lane owns
(`pyproject.toml` `[tool.ruff.lint]`, `templates/ruff-config-block.toml`) touches
`.devcontainer/provision.sh`, and no devcontainer file appears in `5e2ad0b8`'s own diff.
Accepted as a false positive caused by reviewing against a stale local base rather than
`origin/main`; no remediation needed on this lane's files. ROWS-OWED below files the
generalizable gap (the review wrapper should default to `origin/main` for lanes that sync
via merge).

## Medium

(none)

## Low

(none)

The two `extend-select` lists are identical in content and order. I found no removed `# noqa` suppressions; modified lines retained their suppressions. The Ruff-owned rewrites appear mechanical/behavior-preserving.