# Codex Review — lane-claim-marker

**Date:** 2026-09-27
**Branch:** `worktree-lane-claim-marker`
**HEAD:** `2431e58f`
**Diff range:** `main..worktree-lane-claim-marker`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low. All three HIGH findings fixed in the same commit (ruling e): _Sentinel.__exit__ now prints a WARNING instead of swallowing a lock-cleanup OSError; release() treats a concurrent FileNotFoundError on unlink() as the same idempotent success as an already-absent marker; the two-process concurrency test now synchronizes both racers on a ready/wait/go barrier file instead of hoping they overlap. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/claim.py:186 — lock-cleanup failure is silently reported as a successful claim

**What:** `_Sentinel.__exit__` suppresses every `OSError` from `unlink()`.  
**Why:** A failed cleanup leaves the sentinel behind while `claim()` returns success; subsequent claims block for the timeout and then refuse until someone manually removes the stale lock.  
**Fix direction:** Surface lock-removal failure as an error (with recovery guidance) rather than swallowing it.

### scripts/claim.py:244 — concurrent releases can violate the advertised idempotency

**What:** `release()` checks `marker.exists()` and then unlinks separately, without synchronization or handling a concurrent `FileNotFoundError` as success.  
**Why:** Two simultaneous releases of the same session can both observe the marker; one succeeds and the other exits with an internal error after the first removes it.  
**Fix direction:** Make the removal race-safe, treating an already-removed marker as idempotent success or serializing release with the claim lock.

### tests/test_claim.py:50 — the concurrency witness does not guarantee concurrent contention

**What:** The two processes are started consecutively but are not synchronized at the contention point.  
**Why:** The test passes if one process completes its check/create sequence before the other starts, so it would not reliably catch a regression to a non-atomic check-then-create implementation.  
**Fix direction:** Coordinate both workers with a barrier or test hook so they reach the claim critical section concurrently.

## MEDIUM

(none)

## LOW

(none)