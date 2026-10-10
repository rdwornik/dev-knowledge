# Codex Review — b2w3-ci-schedules

**Date:** 2026-10-10
**Branch:** `worktree-b2w3-ci-schedules`
**HEAD:** `ea9b0603`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0

**Model used:** `gpt-6-astra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#1103] LANE-1103-b2w3-ci-schedules

---

## Focus

Begin your reply with the exact line NONCE: c2fbbeb12b994436 . Lane b2w3-ci-schedules ([#1103]): (1) conductor.yml pytest step selector -m not operator_host, (2) report-only-wall.yml nightly schedule + mutation-pilot if + job-level concurrency, (3) six [#1103] ubuntu entries removed from logs/KNOWN-REDS-REGISTRY.json, (4) the three new tests. Check the YAML is valid and that the deselection cannot hide any non-operator_host test, that the registry removal touched only the six entries, and that the tests would fail if the change were reverted. Report-only; no write-back is intended.

---

## Findings
NONCE: c2fbbeb12b994436 .

## Critical

(none)

## High

**.github/workflows/report-only-wall.yml:240 — Pilot concurrency does not isolate scheduled runs**

**What:** The new schedule still enters the workflow-level `report-only-wall-${{ github.ref }}` group shared with pushes to main; job-level concurrency does not override it.

**Why:** If one run is active and a push run is pending, a scheduled run can cancel that pending push’s entire record, despite `cancel-in-progress: false`. [GitHub concurrency semantics](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency).

**Fix direction:** Isolate scheduled runs from the push workflow group and test that isolation explicitly.

## Medium

(none)

## Low

(none)

Verified exactly six Ubuntu `[#1103]` registry removals, with no other registry changes. The marker selector excludes only marked tests.

By inspection, reverting the changes fails the selector pin and extended schedule test; the comment-witness and permissions tests still pass.

YAML appears syntactically valid, but executable YAML validation and tests were blocked by read-only access to uv’s cache.

---

## Record (added by the lane, not by the reviewer)

- **Contract:** `LANE-1103-b2w3-ci-schedules` (batch B2-W3, lane 3), the close-out diff review of Done 6 (S-38 (b), common rules section 2 (e)). The diff reviewed is `origin/main...HEAD` at `ea9b0603`.
- **Served model id, from the tool's own log:** `gpt-6-astra` (`turn_context.model` in the codex session log `rollout-2026-10-10T17-17-36-01a12664-127a-7a83-96e4-e6fee1184065.jsonl`; codex-cli 0.155.0).
- **Nonce returned:** `c2fbbeb12b994436` (the reply's first line; the same string is in the session log).
- **Wrapper tally vs. counted tally:** the wrapper's heuristic read 0/0/0/0 because the finding is written `**file:line — title**`; counted by hand from the Findings section it is 0 Critical / 1 High / 0 Medium / 0 Low.
- **Disposition of the High: FIXED.** The workflow-level concurrency group now keys the `schedule` event apart from pushes (`report-only-wall-nightly-<ref>` against `report-only-wall-<ref>`), still `cancel-in-progress: false`, and `tests/test_report_only_wall.py::test_the_mutation_pilot_is_gated_until_502_has_a_verdict` asserts it. RED before the workflow edit (`assert "github.event_name == 'schedule'" in 'report-only-wall-${{ github.ref }}'`), GREEN after (75 passed across `tests/test_report_only_wall.py` and `tests/test_conductor.py`). The reviewer's remark that it could not run the tests (read-only uv cache) is its own limit; the lane ran them.