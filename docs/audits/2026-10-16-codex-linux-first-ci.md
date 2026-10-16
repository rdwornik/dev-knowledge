# Codex Review — linux-first-ci

**Date:** 2026-10-16
**Branch:** `worktree-linux-first-ci-2026-10-16`
**HEAD:** `ec465782`
**Diff range:** `main..worktree-linux-first-ci-2026-10-16`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low, counted from the Findings section below: one Critical, one High. Round 1 of the review of the first commit (ec465782); both are fixed in the next commit, see Disposition. -->
**Consumer:** ADR-127 AMENDMENT 2 (`docs/decisions/ADR-127-ci-os-verification.md`; batch `BATCH-LINUX-FIRST-CI-2026-10-16`)

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/ci_os_plan.py: is the Windows-sensitive derivation fail-closed everywhere (unreadable diff, failed git grep, missing registry, zero-sha 'before', branch creation)? Can a Windows-sensitive diff ever read as Linux-only?
- scripts/merge_path.py land/verdict: contexts is computed once from base..sha; does the receipt's second read judge the same set? Any path where the Windows context is dropped for a sensitive diff?
- .github/workflows/conductor.yml: plan job output feeding matrix via fromJSON; pull_request/schedule/dispatch/branch-push base resolution; windows-nightly-triage permissions and shell quoting.
- deploy/conductor-required-checks.ruleset.json: five contexts; consequences if armed.

---

## Findings
## CRITICAL

### deploy/conductor-required-checks.ruleset.json:19 — Armed ruleset does not enforce Windows for a Windows-sensitive merge

**What:** The required-check set omits `pytest (windows-latest)`, so a Windows-sensitive SHA with five green contexts can be pushed to `main` despite a failed or absent Windows leg.  
**Why:** `merge_path.land` enforces the conditional Windows requirement, but GitHub’s armed server-side rule does not; bypassing that script defeats the stated sensitive-diff safety invariant.  
**Fix direction:** Add a single always-required CI verdict context that conditionally requires the Windows job when the plan marks the diff sensitive.

## HIGH

### scripts/ci_os_plan.py:124 — Missing or malformed known-reds registry is treated as an empty sensitive set

**What:** A failed `git show <ref>:logs/KNOWN-REDS-REGISTRY.json` is ignored, and invalid JSON returns an empty set.  
**Why:** A diff that is Windows-sensitive only through registry membership can be classified Linux-only when either registry read is unavailable or unparsable.  
**Fix direction:** Treat unavailable, unreadable, or structurally invalid registry data at either diff endpoint as a scan failure that requires Windows.

## MEDIUM

(none)

## LOW

(none)

---

## Disposition (author, same day)

- **CRITICAL (ruleset omits Windows) — FIXED.** The ruleset is still `enforcement: disabled`, so
  nothing was exposed, but the finding is right about the armed state. `windows-gate` (new job,
  `.github/workflows/conductor.yml`) is now the sixth required context: it passes when the plan
  left Windows out, requires the whole `pytest` matrix to succeed when the plan put Windows in, and
  fails closed on an unreadable plan. `actions_verdict.REQUIRED_CONTEXTS` and the ruleset file
  carry it; `merge_path.land` still adds the Windows leg itself for a sensitive diff.
- **HIGH (unreadable registry = empty set) — FIXED.** `ci_os_plan.sensitive_files` raises when the
  registry cannot be read at either end of the diff, `registry_windows_only_files` raises on text
  that is not a registry, and `windows_reasons` turns both into "Windows required".
  Test: `test_an_unreadable_registry_at_either_end_fails_closed`.