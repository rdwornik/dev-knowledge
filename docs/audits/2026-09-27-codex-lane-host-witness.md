# Codex Review — lane-host-witness

**Date:** 2026-09-27
**Branch:** `worktree-lane-host-witness`
**HEAD:** `316d3205`
**Diff range:** `main..worktree-lane-host-witness`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- tests/conftest.py (new): the operator_host marker, its registration list (OPERATOR_HOST_TESTS), and the pytest_collection_modifyitems drift check (find_unregistered_drift / find_unregistered_markers)
- tests/test_integrator_surface.py: @pytest.mark.operator_host applied to the 6 confirmed Linux-only host-witness tests
- tests/test_test_pairing.py: the operator_host drift-detection witness tests (pytester-based), and the HARNESS_MEMORY_GATE_DISABLE fix for test_many_workers_lose_no_result's nested memory-gate deadlock
- Consumer contract: LANE-5B4-5-host-witness.md, row L3 (host-witness isolation + deadlock)

---

## Findings
## Critical

### .github/workflows/conductor.yml:91 — Matrix job no longer satisfies required `pytest` context

**What:** The matrix emits `pytest (ubuntu-latest)` and `pytest (windows-latest)`, while the ruleset still requires `pytest`.  
**Why:** Enabling the declared ruleset will leave the required `pytest` check permanently unsatisfied, blocking merges. The new workflow tests validate job IDs rather than emitted matrix check names, so they miss this drift.  
**Fix direction:** Update the required-check contract and its test to use the matrix-generated contexts (or retain a non-matrix aggregate `pytest` check).

## High

### .github/workflows/conductor.yml:148 — CI still executes `operator_host` witnesses

**What:** The suite invocation does not exclude `operator_host` despite the new marker/registry classifying these as operator-machine-only tests.  
**Why:** Linux CI continues to run host-dependent witnesses and treats their failures as known reds, violating the host-witness isolation contract and obscuring genuine regressions.  
**Fix direction:** Exclude `operator_host` from the CI suite selection and add a workflow-contract assertion for that selector.

## Medium

(none)

## Low

(none)