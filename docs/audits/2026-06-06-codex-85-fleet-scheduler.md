# Codex Review — 85-fleet-scheduler

**Date:** 2026-06-06
**Branch:** `feat/85-fleet-scheduler`
**HEAD:** `061bc9f`
**Diff range:** `main..feat/85-fleet-scheduler`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- fleet_health.py: subprocess timeout correctness, atomic write (os.replace + temp cleanup in finally), completed_at/stale logic, fail-soft exit-0 invariant
- setup-fleet-scheduler.ps1: Register-ScheduledTask idempotency (-Force), principal/logon-type (no stored creds), no-wake settings, dry-run path, error handling, PS 5.1 compatibility
- safety-critical: scheduled-task registration on a real machine; ensure read-only workload, no destructive ops

---

## Findings
## CRITICAL

(none)

## HIGH

**HIGH — scripts/fleet_health.py:83 — incomplete baseline is not treated as stale**

**What:** `is_completed_stale()` returns `False` when `completed_at` is missing, while timeout/error refreshes write a same-day digest with no `completed_at`.  
**Why:** After a failed scheduled run, `is_stale()` sees today’s `run_date`, skips rerun, and `surface_line()` can still report green/issues from partial or old state without flagging the incomplete baseline.  
**Fix direction:** Treat missing `completed_at` as an incomplete/stale condition in `main()` and/or make `surface_line()` explicitly surface incomplete baselines; update the test at `tests/test_fleet_health.py:310` accordingly.

**HIGH — scripts/fleet_health.py:108 — atomic write temp path is race-prone**

**What:** `_atomic_write()` always uses the shared path `FLEET-HEALTH.md.tmp`.  
**Why:** Concurrent SessionStart and scheduled-task runs can overwrite or remove each other’s temp file, causing a lost digest write or fail-soft exception despite the atomic `os.replace()`.  
**Fix direction:** Use a unique temp file in the same directory, such as `tempfile.NamedTemporaryFile(delete=False, dir=path.parent)`, and clean up only that process-owned temp path in `finally`.

## MEDIUM

(none)

## LOW

(none)
