# Codex Review — tier1-precommit-stage-fix

**Date:** 2026-06-03
**Branch:** `chore/tier1-closeout-fixes`
**HEAD:** `0f3536a`
**Diff range:** `main..chore/tier1-closeout-fixes`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

- Focus the .pre-commit-config.yaml change (other changed files are markdown).
- Change adds top-level 'default_stages: [pre-commit]'.
- Root cause fixed: pre-commit is installed for BOTH pre-commit and commit-msg git hooks; working-tree hooks declared no stages, so they re-ran at the commit-msg stage and printed a misleading '(no files to check) Skipped' for validate-backlog/codemap-freshness even though they passed in the pre-commit stage.
- Verify default_stages: [pre-commit] correctly scopes all stage-less hooks to the pre-commit stage WITHOUT disabling backlog-id-on-close (explicit stages: [commit-msg]). Any way this weakens or skips a gate that should run?

---

## Findings
## CRITICAL

(none)

## HIGH

(none)

## MEDIUM

(none)

## LOW

(none)

Verified: `default_stages: [pre-commit]` scopes only hooks without explicit `stages`, while `backlog-id-on-close` keeps its explicit `stages: [commit-msg]`, so it remains active for the commit-message hook. I don’t see a gate weakened or skipped by this change.

Sources checked: official pre-commit docs for `default_stages` and hook stages: https://pre-commit.com/
