# Codex Review — lane-organ-wirings

**Date:** 2026-09-26
**Branch:** `worktree-lane-organ-wirings`
**HEAD:** `897e84fc`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low. Both fixed in the same commit this record ships with; this tally counts what the review found, not what remains open. -->

**Consumer:** lane contract `H:\My Drive\CLAUDE PROMPT DIR\LANE-5B2-10-organ-wirings.md` (batch WAVE5B-N2) — its Done-contract item 4 requires this record.

**Disposition:** both HIGHs fixed, each pinned by a new/strengthened assertion: the replay's own gap (it armed the script directly, so a revert of `.pre-commit-config.yaml`'s `block-commit-on-main` back to `stages: [manual]` would have stayed green) is closed by `tests/test_block_commit_on_main_replay.py::test_the_hook_this_replay_exercises_is_actually_armed_at_pre_commit`, which reads the live config and asserts the stage directly; the fates tests' under-constraint (any of the four organ-wiring paths could flip to `moment:`/`retire_candidate:` and still pass "exactly one shape") is closed by `tests/test_organ_truth.py::test_every_organ_wiring_fate_stays_manual_until_not_moment_or_retire`, which pins the exact `manual_until: 2026-10-05` value and the absence of the other two keys.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- ecosystem/harness.yaml: fates: corrections for scripts/handback.py, scripts/hooks/deny_and_point.py, scripts/lane_boot.py, scripts/plan_lint.py, scripts/codespace_regime.py, scripts/surface_triage.ps1/.py -- judged DECIDED-BY-LANE not to wire as live moment organs (dispatch.py pre-launch gate + lane_end_guard.py lane-end run for real, fleet-wide, no soft-fail path)
- .pre-commit-config.yaml: block-commit-on-main moved from stages:[manual] to the default pre-commit stage
- tests/test_block_commit_on_main_replay.py (new): replays the integrator's own --no-ff merge / regen commit / ledger-line commit / fast-forward push sequence against the newly-armed hook
- tests/test_organ_truth.py: new tests pinning the live fates: entries for the four organ-wiring paths
- Consumer of this review: H:\My Drive\CLAUDE PROMPT DIR\LANE-5B2-10-organ-wirings.md (lane-organ-wirings frozen contract)

---

## Findings
## Critical

(none)

## High

## HIGH [tests/test_block_commit_on_main_replay.py](/C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/lane-organ-wirings/tests/test_block_commit_on_main_replay.py:56) — Replay bypasses the configured hook stage

**What:** The replay manually writes a native `pre-commit` hook instead of installing/running the `.pre-commit-config.yaml` hook configuration.

**Why:** Reverting `block-commit-on-main` to `stages: [manual]` would leave this replay green while disabling the intended default commit-time protection.

**Fix direction:** Assert the resolved hook configuration places this hook on `pre-commit`, or install via pre-commit in the test before replaying the sequence.

## HIGH [tests/test_organ_truth.py](/C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/lane-organ-wirings/tests/test_organ_truth.py:524) — Fate tests do not pin the required manual disposition

**What:** The tests require only one recognized fate shape, so any of the four entries may change to `moment` or `retire_candidate` and still pass.

**Why:** That permits a regression from the lane’s DECIDED-BY-LANE `manual_until` disposition without a failing test.

**Fix direction:** Assert each listed path retains `manual_until: 2026-10-05` (and, where required, its deferred-wiring rationale).

## Medium

(none)

## Low

(none)