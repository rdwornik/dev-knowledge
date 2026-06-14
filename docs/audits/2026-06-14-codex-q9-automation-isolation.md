# Codex Review — q9-automation-isolation

**Date:** 2026-06-14
**Branch:** `feat/q9-automation-isolation`
**HEAD:** `9590daa`
**Diff range:** `main..feat/q9-automation-isolation`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- scripts/audit.py _commit_routine_outputs: separate-index (GIT_INDEX_FILE) commit-tree plumbing onto automation/fleet-audit. Verify main HEAD/index/working-tree are never mutated, the finally-block restore is crash-safe, and tracked-vs-untracked restore (_restore_durable_scope) is correct (no arbitrary untracked file removed; modified-tracked restored from HEAD).
- .github/workflows/nightly-conformance-triage.yml guard-PASS divert: commit-tree push to automation/conformance-digest + gh pr close (no squash-merge to main). Check shell-injection safety (set -euo pipefail, no unquoted untrusted expansion), orphan-first-run vs accumulate-with-parent, and the loud-fail push path.
- scripts/validate_no_ff.py: removal of _is_automation/_AUTOMATION_* leaves no silent-pass; BASELINE_DATE bump to 2026-06-15 grandfathers legacy on-main automation (<=2026-06-14) only; filter_violations still correct.

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH scripts/audit.py:1603 — restore is skipped if the initial durable-scope status fails

**What:** `_commit_routine_outputs` returns on `git status` failure before entering the `try/finally`, so `_restore_durable_scope(...)` never runs.  
**Why:** `cmd_run` has already written durable outputs into the main working tree, so this failure path can leave `main` dirty and violates the automation-isolation cleanup contract.  
**Fix direction:** Put the status snapshot and `changed` initialization inside a cleanup-protected block, defaulting `changed` safely so restore still runs whenever durable outputs may have been written.

## HIGH .github/workflows/nightly-conformance-triage.yml:225 — PR close failure is not handled after digest push

**What:** `gh pr close "$PR_NUMBER" --delete-branch` runs under `set -e`, but has no explicit failure handling after the digest has already been pushed.  
**Why:** If close/delete fails, the digest is recorded but the PR remains open and the workflow exits without creating a triage issue, leaving an inconsistent state that can be rerun or require manual discovery.  
**Fix direction:** Wrap `gh pr close` like the push path: emit an error, open a `nightly-triage` issue describing the already-pushed digest commit, and exit nonzero.

## MEDIUM

(none)

## LOW

(none)
