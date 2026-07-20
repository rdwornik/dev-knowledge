# Codex Review — leg2-handoff-bundle-selection

**Date:** 2026-07-20
**Branch:** `worktree-gate-fixes`
**HEAD:** `95ef6d26`
**Diff range:** `36ca03f0^..36ca03f0`
**Codex version:** codex-cli 0.144.5
**Mode:** diff-review

---

## Focus

The working tree is CLEAN at commit 95ef6d26. Review the commit objects in the given range.
- Defect: check_handoff_probes used sorted(dirs, key=name)[-1], picking a lexically-max but STALE bundle ('-arc5' sorts after '' so an older bundle won). Fix ranks by git add-date via log --diff-filter=A --reverse --format=%at.
- Is --diff-filter=A + --reverse + first-line the correct first-add date? We deliberately avoid -1 (git applies it before --reverse). Any case yielding the wrong commit (renames, merges, path filters)?
- Freshness = empty --diff-filter=A output. Is the guard (rev-parse --show-toplevel normcase-equals repo_path, plus rev-parse --verify HEAD) sufficient to distinguish 'never added' from 'not this repo'? Any case where a bundle is wrongly classified fresh, causing a spurious ambiguous FAIL?
- The >=2-fresh case FAILs by design (operator ruling: never silently pick). Is the no-git lexical fallback right, or does it mask misconfiguration?
- Verify EVERY git call routes through the scrubbed runner; note a later commit b0443523 derives the scrub set from 'git rev-parse --local-env-vars'.
- Do the four tests genuinely lock selection, or could any pass for a wrong reason?
- Determinism of dated.sort((add_date, slug)); Windows normcase correctness.

---

## Findings
## Critical

(none)

## High

### HIGH — scripts/audit.py:1527 — Git environment scrub is incomplete

**What:** The hand-written scrub omits eight variables reported by `git rev-parse --local-env-vars`, including `GIT_SHALLOW_FILE`, `GIT_GRAFT_FILE`, and `GIT_CONFIG*`.

**Why:** Inherited values can alter repository history or configuration, causing incorrect add dates or false “fresh” classifications despite every Git call using `_run`.

**Fix direction:** Derive the scrub set from `git rev-parse --local-env-vars` with a complete fallback. This is addressed by later commit `b0443523`.

### HIGH — scripts/audit.py:1578 — Lexical fallback hides Git failures and bypasses fresh-bundle ambiguity

**What:** Failed Git execution, a mismatched root, and an unborn `HEAD` all silently select the lexical maximum.

**Why:** An unborn repository containing multiple uncommitted bundles bypasses the required ambiguous FAIL; Git misconfiguration can likewise restore the original stale-bundle false green.

**Fix direction:** Distinguish confirmed non-Git operation from Git errors and unborn `HEAD`; treat unborn candidates as fresh and return degraded output for invocation/root failures.

### HIGH — tests/test_verify_handoff_probes.py:759 — Git fixture failures are ignored

**What:** `_commit_at` and most `_git_repo` operations never assert successful `git add`, `commit`, or configuration.

**Why:** The add-date and inherited-`GIT_DIR` tests can pass if the second intended commit fails, because the supposedly committed newest bundle then wins as “fresh.”

**Fix direction:** Assert every setup command’s return code and verify the expected commits and timestamps before invoking the selector.

### HIGH — tests/test_verify_handoff_probes.py:841 — Scrub test does not lock every Git call

**What:** The test checks only the final selection; it still passes if `rev-parse --verify HEAD` bypasses the scrubbed runner while the top-level and log calls remain scrubbed.

**Why:** A future regression can violate the stated “every Git call” invariant without failing this test.

**Fix direction:** Instrument the subprocess runner and assert that each selector Git invocation receives the scrubbed environment.

## Medium

(none)

## Low

(none)
