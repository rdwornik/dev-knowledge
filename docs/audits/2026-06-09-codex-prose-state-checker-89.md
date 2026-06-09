# Codex Review — prose-state-checker-89

**Date:** 2026-06-09
**Branch:** `docs/codex-89-review`
**HEAD:** `9bbb415`
**Diff range:** `27735a6..9bbb415`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- HIGHEST RISK: _GATE_MODE in scripts/audit.py — the cmd_health self-audit loop is wrapped in try/finally to set _GATE_MODE=True then reset False. Verify no path leaves it stuck True (would silently disable claim-3 pytest_collected on the full-audit path) and no cross-call leak. It is a module global mutated via global — check re-entrancy/threading assumptions.
- check_doc_claims adapter: hub-only guard, WARN-only/fail-soft (never FAIL, never raise), evidence sanitation (no pipe chars), correct mismatch vs anchor-missing branching.
- validate_doc_claims.reconcile: claim-3 skip logic (run_expensive), anchor-missing never synthesized as mismatch, pytest subprocess fail-soft (None -> skipped), set-equality roster.
- extract_claimed_hooks window-bounding (zero false positives from changelog prose), extract_hook_ids counts ALL ids incl commit-msg stage.
- Tests: do they actually prove the deployed path (registered in ALL_CHECKS) and the gate-mode skip?

---

## Findings
## CRITICAL

## CRITICAL scripts/validate_doc_claims.py:117 — pytest collection is not read-only

**What:** `_derive_pytest_collected` runs `pytest --collect-only -q` without disabling pytest cache or Python bytecode writes.  
**Why:** Pytest collection can create/update `.pytest_cache` and imported modules can create `__pycache__`, violating the validator’s read-only/Layer-2 contract.  
**Fix direction:** Run collection with cache/bytecode writes disabled, or derive the count through a path that is explicitly proven not to mutate the repo.

## HIGH

## HIGH tests/test_validate_doc_claims.py:175 — expensive claim test permits skipped results

**What:** `test_reconcile_evaluates_test_count_when_expensive` allows `"skipped"` and the follow-up assertion still passes because skipped results carry a non-empty `actual` string.  
**Why:** Claim-3 could silently stop evaluating on the full-audit path and this test would still pass.  
**Fix direction:** Mock the pytest subprocess or deriver to return deterministic collection output and assert a non-skipped match/mismatch, with a separate test for `None -> skipped`.

## HIGH tests/test_validate_doc_claims.py:250 — gate-mode test bypasses the deployed wrapper

**What:** The test sets `_GATE_MODE=True` directly and calls `check_doc_claims`, but never exercises `cmd_health` setting and resetting the flag around the `ALL_CHECKS` loop.  
**Why:** A regression in the high-risk global mutation path, including a missing reset after failure, would not be caught.  
**Fix direction:** Add a `cmd_health`/Click-runner test with sentinel checks that observes `_GATE_MODE` during the loop and verifies it is restored afterward.

## MEDIUM

(none)

## LOW

(none)

I did not run tests because this was a read-only review.
