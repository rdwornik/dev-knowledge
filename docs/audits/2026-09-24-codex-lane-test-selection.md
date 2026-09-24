# Codex Review — lane-test-selection

**Date:** 2026-09-24
**Branch:** `worktree-lane-test-selection`
**HEAD:** `d5959e49`
**Diff range:** `main..worktree-lane-test-selection`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Consumer:** [#1009] (this lane's row, `LANE-5A-2-test-selection.md`)

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

**Disposition:** the test-coverage HIGH (`tests/test_impacted_tests.py:631`) is FIXED in the
same branch, one commit after this record's HEAD — the ledger test now asserts the complete
`MERGE_RECEIPTS_TEST_TARGET` set, not one member of it. The consumer-safety HIGH
(`scripts/impacted_tests.py:589`) is an ACCEPTED, contract-directed residual, not fixed here:
LANE-5A-2's Done-contract item 1 is precisely "a prose or generated edit no longer expands
into the 58-file union... selectable on its own so the INTEGRATOR can run it once per batch"
— i.e. the docs tier's execution is meant to move OUT of every per-merge/per-compare run and
INTO a once-per-batch integrator step. `scripts/test_pairing.py` (the consumer Codex names)
is explicitly out of this lane's scope (`Do not: touch ... test_pairing.py ... other lanes
own them`), so wiring its `choose_tests`/`choose_tests_from_lane_diff` (or `gates.py`'s
per-merge gate) to call the new `Selection.docs_tier_args()` once per batch is next-lane
work, not something this lane can close. Until that wiring lands, a mixed diff's `compare`
run no longer exercises the live-tree marker tier — CI's full suite remains the backstop net
the module's own docstring already names ("the integrator keeps one full suite per
integration as the net"). Recorded as a FINDING in this lane's session file and row `[#1009]`
for the next consumer to pick up.

---

## Focus

- scripts/impacted_tests.py: does the new merge-receipts-ledger fixed rule correctly stop logs/MERGE-RECEIPTS.jsonl from forcing the full suite, without weakening the unmapped-path fail-safe for anything else?
- Does removing the marker/file union step in select() correctly decouple the doc tier (now only reachable via the new Selection.docs_tier_args()) from the lane's own pytest_args(), without silently under-selecting a mixed diff?
- Is Selection.docs_tier_args() safe for every caller of Selection (esp. scripts/test_pairing.py, which this lane must not modify) -- does it change any existing consumer's behavior in a way that under-selects or drops coverage?
- tests/test_impacted_tests.py: are the new RED-first tests for both fixes actually meaningful (would they fail against the prior code), or could they pass vacuously?

---

## Findings
## Critical

(none)

## High

### scripts/impacted_tests.py:589 — Mixed diffs silently drop the docs tier for existing consumers

**What:** The selector no longer unions live-repo tests, but existing consumers such as `test_pairing` discard `marker` when `test_files` is nonempty and never call `docs_tier_args()`.  
**Why:** A mixed code+docs diff now runs only code-selected tests there; previously it also covered the docs tier, so live-tree regressions can be silently missed.  
**Fix direction:** Preserve a consumer-safe representation of the separate docs tier, or update every consumer to explicitly schedule `docs_tier_args()`.

### tests/test_impacted_tests.py:631 — Ledger test does not verify both required fixed targets

**What:** The new ledger test asserts `tests/test_merge_receipt.py` but not `tests/test_lane_digest.py`.  
**Why:** A regression that removes the lane-digest target still passes all new ledger tests, dropping required coverage.  
**Fix direction:** Assert the complete expected target set for the ledger rule.

## Medium

(none)

## Low

(none)