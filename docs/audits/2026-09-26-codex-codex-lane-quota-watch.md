# Codex Review — codex-lane-quota-watch

**Date:** 2026-09-26
**Branch:** `worktree-lane-quota-watch`
**HEAD:** `e47cef2d`
**Diff range:** `origin/main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low. All 3 HIGH findings fixed in the next commit: projected exhaustion is capped at the billing-cycle reset, record_read's read-detect-append is serialized under a ledger lock, and a negative --projected-core-hours is refused before it can mask a real crossing. This tally counts what the review found, not what remains open. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

consumer: the frozen contract H:\My Drive\CLAUDE PROMPT DIR\LANE-5B2-6-quota-watch.md (LANE-5B2-6-quota-watch, batch WAVE5B-N2) -- review scripts/quota_watch.py, ecosystem/quotas.yaml, the transport-registry/harness.yaml additions, the two order-template edits, and tests/test_quota_watch.py for correctness against the Done-contract: per-SKU used/quota/%/burn/projected-exhaustion; exactly one 80%% crossing on 79%% then 81%%; a crossing writes a registered QUOTA-WARN transport file; the ONE hard veto is Codespaces core-hours only (everything else warns, never refuses); no secret or token is stored or printed.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/quota_watch.py:265 — Projected exhaustion can extend beyond the monthly reset

**What:** The projection always returns `now + remaining / burn`, even when that date is after the current billing cycle ends.  
**Why:** Monthly quotas reset, so reporting a December exhaustion date for September consumption is incorrect rather than “projected exhaustion this cycle.”  
**Fix direction:** Cap the projection at the billing-cycle boundary and report no exhaustion when the computed date falls after that boundary.

### scripts/quota_watch.py:367 — Crossing detection is not serialized with the ledger append

**What:** `record_read` reads the prior row, detects crossings, then appends without a lock or transaction.  
**Why:** Concurrent `record` calls can both read the 79% row and independently emit the 80% warning, violating the exactly-once crossing contract.  
**Fix direction:** Serialize the read/detect/append operation per ledger (or per SKU-cycle) so only one invocation can claim a crossing.

### scripts/quota_watch.py:536 — Negative projected core-hours bypass the sole launch veto

**What:** `--projected-core-hours` accepts negative values, which reduce the calculated projected total.  
**Why:** A caller can receive an OK verdict despite an actual launch crossing the Codespaces core-hour quota.  
**Fix direction:** Reject negative projections at CLI and function boundaries.

## MEDIUM

(none)

## LOW

(none)