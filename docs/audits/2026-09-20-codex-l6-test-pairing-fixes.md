# Codex Review — l6-test-pairing-fixes

**Date:** 2026-09-20
**Branch:** `worktree-lane-l6-test-pairing`
**HEAD:** `b3e36b87`
**Diff range:** `main..worktree-lane-l6-test-pairing`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/4/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Re-review after fixes to the five HIGH findings of docs/audits/2026-09-20-codex-l6-test-pairing.md. Verify each fix actually closes its finding and introduces no new defect.
- The pytest plugin (_PLUGIN / read_events / run_pytest): xdist duplicates, concurrent appends, a red overwritten by a later green, missing events file, PYTHONPATH handling, plugin file leaking into the tested clone.
- Baseline confirmation in pair(): batched rerun on BASE, reclassification to lane candidate, interaction with collection-error file-level ids and with the flake rule.
- Any way a lane-caused red can still exit 0.

---

## Findings
The five prior HIGH findings are closed. New HIGH findings remain.

## Critical

(none)

## High

### scripts/test_pairing.py:137 — xdist workers concurrently append to one event file

**What:** Multiple pytest/xdist processes append JSON lines to the same file without interprocess synchronization.  
**Why:** Writes can interleave or be lost; `read_events()` silently discards malformed rows, allowing a HEAD failure to disappear and the pairing to report `CLEAN`/exit 0.  
**Fix direction:** Use per-worker event files or a single controller-side writer, then validate the complete merged result.

### scripts/test_pairing.py:160 — Missing or empty event output is accepted as a successful test result

**What:** `read_events()` returns `{}` when the event file is absent, and `run_pytest()` accepts pytest exit codes 0 and 1 with no events.  
**Why:** Plugin/reporting failure can turn a real failing run into empty HEAD results, producing `CLEAN` and exit 0.  
**Fix direction:** Fail closed when the required event artifact is missing or inconsistent with a pytest invocation.

### scripts/test_pairing.py:193 — Inherited `PYTHONPATH` can import code outside the detached clone

**What:** The subprocess preserves the caller’s entire `PYTHONPATH`.  
**Why:** A source checkout or editable path in that variable can shadow code in BASE or HEAD, so a lane-caused failure can be hidden by a different local version and exit 0.  
**Fix direction:** Construct a controlled import path for the plugin and clone; exclude caller paths resolving into the source checkout.

### scripts/test_pairing.py:356 — `--tests` permits directory targets and can run the full suite

**What:** The option accepts arbitrary pytest targets, including `.` or `tests/`, despite being documented as test files.  
**Why:** This bypasses the no-full-suite contract and can unexpectedly run all tests.  
**Fix direction:** Validate explicit targets as individual test files/node IDs, rejecting directories and broad pytest selectors.

## Medium

(none)

## Low

(none)

---

## Disposition (lane-l6-test-pairing, appended after the fixes)

Pass 2 confirmed the five HIGH of pass 1 closed and raised four new ones, all against the plugin
path introduced by fixing pass 1. Every one was opened against the code before acceptance.
**4 ACCEPT, 0 REJECT.** RED-first: `test(pairing): RED -- the second codex terra pass...`
(9 failed, 1 passed) precedes `fix(pairing): codex terra pass 2`.

1. **Concurrent appends to one event file (`:137`)** -- ACCEPT, and *measured, not argued*:
   `test_many_workers_lose_no_result` recorded **293 of 300** results with three xdist workers
   on one shared file. One file per process now (`<prefix>.<pid>`), merged on read.
2. **Missing or empty event output accepted (`:160`)** -- ACCEPT. The plugin creates its file at
   session start, so an absent file proves it never ran; `read_events` raises on no file or a
   malformed row, and `run_pytest` raises when pytest exit 1 shows no red or exit 2 shows no
   result. Guard against over-correction: `test_a_skipped_only_run_is_not_mistaken_for_a_missing_report`.
3. **Inherited `PYTHONPATH` (`:193`)** -- ACCEPT. The subprocess gets only the plugin's directory.
   Test: `test_the_callers_pythonpath_is_not_inherited_by_the_clone_run`.
4. **`--tests` accepts a directory (`:356`)** -- ACCEPT. Files and node ids only; a directory,
   `.`, a non-`.py` path or a missing file is exit 2. Tests:
   `test_explicit_tests_must_be_files_never_a_directory[...]`, `test_an_explicit_node_id_is_accepted`.

**Not done:** no third Codex pass. Two passes, nine HIGH, all fixed with a witnessed RED each;
the fixes of pass 2 are covered by their own tests and were exercised live under xdist on a
synthetic repository, but they have not been independently re-reviewed.
