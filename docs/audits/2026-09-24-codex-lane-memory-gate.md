# Codex Review — lane-memory-gate

**Date:** 2026-09-24
**Branch:** `worktree-lane-memory-gate`
**HEAD:** `f9d9403b`
**Diff range:** `main..worktree-lane-memory-gate`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/2/0/0 <!-- Critical/High/Medium/Low. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** LANE-5A-3 (`H:\My Drive\CLAUDE PROMPT DIR\LANE-5A-3-memory-gate.md`), done-contract
item 5 ("Codex terra review with its consumer cited"); D7 in
`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`.

no-consumer: this lane files no BACKLOG row of its own for D7 -- DECLARE-WINDOW-DEFECTS'
own `lands-via` line assigns filing one row per D-item to LANE-5A-5, not the lane that fixes
the item -- so this review's finding is disposed against the frozen contract directly (above),
the same governance identity `harness.yaml`'s new `fates:` line for this module already cites.

---

## Focus

(none specified)

---

## Findings
## CRITICAL

### `scripts/memory_admission_gate.py:282` — Sampler silently swallows all failures

**What:** `_sample_peak` catches `Exception` and discards it without reporting.  
**Why:** Broken memory sampling becomes an apparently valid receipt with missing/stale peak data, hiding failures in the safety mechanism.  
**Fix direction:** Catch only expected sampling errors and record a diagnostic in the receipt or logging output.

## HIGH

### `scripts/memory_admission_gate.py:369` — Concurrent admissions do not reserve their estimated memory

**What:** Each process independently computes workers and checks current free memory; acquiring a slot does not deduct or reserve that process’s estimated memory for other contenders.  
**Why:** Multiple slot holders can all pass against the same free-memory reading and start together, collectively exhausting RAM—the OOM condition this gate is intended to prevent.  
**Fix direction:** Make memory admission an atomic shared allocation, accounting for estimates already claimed by active slot holders before computing workers and launching.

### `scripts/gates.py:202` — A memory-gate timeout aborts the gate runner without a verdict

**What:** The gated-argv path does not convert `MemoryGateTimeout` (or other gate exceptions) into a failed gate row.  
**Why:** A configured admission timeout raises out of `run_gates`, preventing remaining gates from running and preventing the merge verdict from being written.  
**Fix direction:** Handle admission-gate failures like other gate failures: produce a nonzero result and diagnostic text, then continue building the verdict.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (LANE-5A-3, 2026-09-24)

**All three findings were genuine; all three fixed, in the same session as this review.**

1. **CRITICAL, sampler swallows failures.** `_sample_peak` now takes an `errors: list[str]`
   and appends `repr(exc)` instead of discarding it; `GateResult` gained `sampler_errors`,
   threaded into the JSON receipt. Regression:
   `test_run_gated_surfaces_sampler_failures_instead_of_swallowing_them`.
2. **HIGH, concurrent admissions don't reserve memory.** Added a reservation ledger
   (`logs/receipts/memory-gate-slots/reservations.json`, keyed by slot id, guarded by its own
   `reservations.lock`): after `wait_for_memory`'s own (now reservation-adjusted) read
   succeeds, `run_gated` re-checks and registers atomically under the ledger lock before
   proceeding, looping back into `wait_for_memory` on a lost race instead of starting anyway.
   An entry counts only while the slot id it names is still actually OS-locked (probed as a
   non-blocking `filelock` acquire attempt), so a killed holder's reservation self-heals on the
   next read with no separate liveness protocol — closing the crash-leak risk a naive ledger
   would otherwise add. Regressions: `test_reserved_mb_excluding_*` (4 tests) and
   `test_run_gated_does_not_admit_a_second_call_whose_estimate_would_exceed_free_memory`,
   `test_run_gated_deregisters_its_reservation_so_the_next_caller_can_be_admitted`.
3. **HIGH, gates.py swallows nothing, crashes instead.** `_run_argv_gated` now also catches
   `memory_admission_gate.MemoryGateTimeout` and `subprocess.TimeoutExpired`, converting either
   into a failed gate row (`_NOT_STARTED`, diagnostic text) instead of letting it propagate out
   of `run_gates` and abort the whole verdict before it is written. Regression:
   `test_a_memory_gate_timeout_is_red_not_an_uncaught_crash`.

**Full re-verification after the fixes:** `tests/test_memory_admission_gate.py` — 27 passed.
`tests/test_integrator_surface.py` — 35 passed. `ruff check` on all five touched files — clean.