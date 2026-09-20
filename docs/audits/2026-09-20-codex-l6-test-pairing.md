# Codex Review — l6-test-pairing

**Date:** 2026-09-20
**Branch:** `worktree-lane-l6-test-pairing`
**HEAD:** `dd14c277`
**Diff range:** `main..worktree-lane-l6-test-pairing`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/5/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/test_pairing.py attribution: can a lane-caused red be reported as pre-existing or FLAKE (rerun logic, id matching between base and head runs, collection-error ids, parametrised ids)?
- Isolation: git clone --shared of a worktree, cleanup on every exit path including SystemExit and PairingError, leftovers.
- Selection: does a declined impacted_tests selection ever run everything or silently narrow to nothing while reporting CLEAN?
- Exit codes and verdict artifact: does the merge moment get a non-zero exit whenever the lane's set is non-empty?
- tests/test_test_pairing.py: vacuous assertions, tests that pass without the module doing the work.

---

## Findings
## Critical

(none)

## High

### scripts/test_pairing.py:220 — A flaky baseline red can mask a lane-caused red as pre-existing

**What:** Classification treats any red node ID present in both one-shot runs as pre-existing and never reruns it.  
**Why:** If BASE fails transiently and HEAD has a real lane-caused failure with the same ID, the tool returns `CLEAN`/exit 0 and reports it as pre-existing.  
**Fix direction:** Confirm baseline-red results with reruns, or surface uncertain overlap as non-clean rather than pre-existing.

### scripts/test_pairing.py:143 — Parametrized IDs with unmatched brackets are parsed as part of the failure message

**What:** The ` - ` splitter requires balanced `[`/`]`, but pytest permits arbitrary custom parameter IDs, including IDs containing unmatched brackets.  
**Why:** The parsed node ID can include assertion text; changing only a failure message then changes identity between BASE and HEAD, producing incorrect attribution and an invalid rerun target.  
**Fix direction:** Use a structured pytest result surface, or parsing that does not infer node-ID boundaries from bracket counts.

### scripts/test_pairing.py:230 — Collection errors are recorded as initial `FAILED` observations

**What:** `_rerun()` always starts observations with `"FAILED"`, even when the HEAD result was `ERROR`.  
**Why:** The verdict artifact falsely records collection-error results and does not preserve the actual first observation required for attribution/flake evidence.  
**Fix direction:** Pass the candidate’s actual HEAD status into `_rerun()` and record that value.

### scripts/test_pairing.py:230 — `--reruns 0` disables the mandatory flake check

**What:** The CLI accepts zero or negative reruns, causing `_rerun()` to perform no rerun.  
**Why:** A transient lane candidate is charged to the lane after one observation, contrary to the tool’s stated flake rule.  
**Fix direction:** Reject values below one, or enforce at least one rerun internally.

### scripts/test_pairing.py:282 — A failed scratch cleanup can still exit successfully

**What:** A `LEFTOVER` cleanup result is written into the verdict, but a `CLEAN` verdict still receives exit code 0.  
**Why:** The merge can proceed despite leaked shared clones, violating the isolation/cleanup contract.  
**Fix direction:** Treat unremoved scratch state as a non-zero pairing failure and retain cleanup diagnostics.

## Medium

(none)

## Low

(none)

---

## Disposition (lane-l6-test-pairing, appended after the fixes)

Every HIGH was opened against the code it cites before acceptance. **5 ACCEPT, 0 REJECT.**
Each fix has its own RED-first test, committed and witnessed failing in its own commit
(`test(pairing): RED -- the five HIGH findings...`: 8 failed, 16 passed) before the fix commit
(`fix(pairing): codex terra HIGH 1-5`).

1. **Flaky baseline masks a lane red as pre-existing (`:220`)** -- ACCEPT. The pre-existing set is
   now rerun once on BASE in one batch; a red that passes there becomes a lane candidate
   (`was: red-once-on-base`) and faces the HEAD rerun. `--no-confirm-baseline` skips it and the
   verdict says `baseline_confirmed: false`. Test:
   `test_a_transient_baseline_red_does_not_mask_a_lane_red_as_preexisting`.
2. **Unmatched brackets in a parametrised id (`:143`)** -- ACCEPT. The `-rA` summary parser is
   gone; results come from a pytest plugin that records exact node ids. Test:
   `test_a_parametrised_id_with_unmatched_brackets_is_recorded_exactly`.
3. **Collection errors recorded as a first `FAILED` (`:230`)** -- ACCEPT. Observations start from
   the candidate's real HEAD status. Test: `test_a_collection_error_records_ERROR_as_its_first_observation`.
4. **`--reruns 0` disables the flake check (`:230`)** -- ACCEPT. Refused (exit 2). Test:
   `test_zero_reruns_is_refused_because_it_would_disable_the_flake_rule`.
5. **A leftover clone can exit 0 (`:282`)** -- ACCEPT. An unremoved scratch directory forces
   exit 2. Test: `test_a_leftover_clone_is_a_non_zero_exit_even_when_the_pairing_is_clean`.
