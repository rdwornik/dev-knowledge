# Codex Review — leg1-fleet-parity-gitdir-scrub

**Date:** 2026-07-20
**Branch:** `worktree-gate-fixes`
**HEAD:** `36ca03f0`
**Diff range:** `7a9ddc6d^..7a9ddc6d`
**Codex version:** codex-cli 0.144.5
**Mode:** diff-review

---

## Focus

- The defect: _git() passed cwd= but no env=; GIT_DIR overrides cwd AND -C, so under pre-commit every collect_facts probe of a consumer repo read the HUB's index. Confirmed empirically.
- Is the NAMED scrub set (_GIT_LOCATION_ENV) complete for repo-location resolution? Any GIT_* var that redirects which repo/index/objects git reads and is MISSING from the tuple is a real finding.
- Is scrubbing by name (vs blanket startswith GIT_) the right failure mode? We deliberately keep GIT_CONFIG_GLOBAL / GIT_AUTHOR_* / GIT_SSH_COMMAND.
- Does the regression test genuinely fail before the fix, and is it two-sided (consumer file present AND foreign file absent)? Could it pass for a wrong reason (e.g. empty snapshot)?
- Fixture ordering: repos are built BEFORE monkeypatch because the test module's own _git helper is unscrubbed. Is that reasoning sound?
- Confirm polarity is untouched: the INVERSE/MUST verdict branches are not modified.

---

## Findings
## CRITICAL

(none)

## HIGH scripts/fleet_parity.py:485 — Repository-local scrub set is incomplete

**What:** `_GIT_LOCATION_ENV` omits Git repository-local variables including `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_IMPLICIT_WORK_TREE`, `GIT_GRAFT_FILE`, `GIT_SHALLOW_FILE`, `GIT_REPLACE_REF_BASE`, and `GIT_NO_REPLACE_OBJECTS`; Git 2.55 also adds `GIT_REFERENCE_BACKEND`.

**Why:** These can redirect configuration/worktree state or alter the object graph used by `config`, `status`, and `merge-base`, producing silently incorrect consumer facts. Git explicitly recommends clearing `git rev-parse --local-env-vars` before accessing a foreign repository from a hook. [Git hooks documentation](https://git-scm.com/docs/githooks/2.46.0.html)

**Fix direction:** Expand the named scrub to Git’s complete repository-local set while retaining intentional variables such as `GIT_CONFIG_GLOBAL`, author identity, and SSH settings; extend the regression test with representative config and ancestry variables.

## MEDIUM

(none)

## LOW

(none)

The existing regression test is otherwise sound: fixture ordering is correct, it fails before the fix, and `git_error == ""` plus consumer-present and foreign-absent assertions prevent an empty or union snapshot from passing. The INVERSE/MUST verdict branches are untouched.
