# Codex Review — seat-release-b1

**Date:** 2026-09-29
**Branch:** `worktree-lane-handoff-moments`
**HEAD:** `81e9fe62`
**Diff range:** `main..worktree-lane-handoff-moments`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/0/0/0 <!-- Critical/High/Medium/Low. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

LANE-5B5-2-lane-handoff-moments.md (H:\My Drive\CLAUDE PROMPT DIR) is the consumer contract for this diff: implement moment:seat-release in ecosystem/harness.yaml as a refusing release transaction (4 organs: notes, bundle, manifest, copy), retire two fates rows, add a CI job to conductor.yml, RED-first tests. Check: does the transaction genuinely refuse on each missing artifact; is fates retirement safe (does check_organ_truth still resolve these paths as declared, not orphaned); is the CI job's era-gating sound (skip pre-manifest bundles) or does it create a false-negative window; any security issue in the inline python organs reading env vars.

---

## Findings
## CRITICAL

### .github/workflows/conductor.yml:700

**What:** A missing, unreadable, or empty `manifest.files` receipt is treated as a pre-manifest-era bundle and skipped.  
**Why:** A post-era bundle can evade the tamper check by deleting/corrupting `HANDOFF_RECEIPT.json` or clearing `manifest.files`; the local `BD-manifest` rule would refuse those states.  
**Fix direction:** Determine era independently of receipt validity, then run `BD-manifest` and fail for absent/unreadable/empty manifests on every in-era bundle.

### scripts/hooks/scope_guard.py:576

**What:** The narrowed bare-wildcard rule permits `*` below arbitrary non-`Users`/`home` paths.  
**Why:** The excluded-root contract permits a bare root name wherever mounted; e.g. a wildcard can expand to an excluded directory under `C:\staging\*\...`, bypassing the scope boundary.  
**Fix direction:** Keep uncertain path globs fail-closed, and address regex/pathspec false positives through command-aware parsing rather than assuming a protected root’s location.

**Resolution.** The `conductor.yml:700` finding is genuine and in this lane's own scope (LANE-5B5-2
B1) — fixed same-lane: era is now read from each bundle's own directory-name date (cutoff
2026-09-28) instead of from `HANDOFF_RECEIPT.json`, so an in-era bundle can no longer dodge
`BD-manifest` by deleting/emptying its own receipt. RED-first witness added
(`tests/test_ci_manifest_step_fails_an_in_era_bundle_that_deleted_its_own_receipt`), confirmed
red against the pre-fix step, green after. See `.github/workflows/conductor.yml`'s
`handoff-manifest` job and `.claude/commands/handoff-verify.md`.

The `scripts/hooks/scope_guard.py:576` finding is **out of scope for LANE-5B5-2** — this diff
carries no edit to `scope_guard.py`; it appears here only because the reviewed range
(`main..worktree-lane-handoff-moments`) includes prior, already-landed commits from a different
lane (`worktree-lane-scope-guard-3`, merged @ 9ec8aaf1) that this branch's local `main` ref had
not yet caught up to at review time. Not actioned by this lane; left for the scope-guard lane's
own record.

## HIGH

(none)

## MEDIUM

(none)

## LOW

(none)