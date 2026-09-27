# Codex Review — lane-subagent-cost

**Date:** 2026-09-27
**Branch:** `worktree-lane-subagent-cost`
**HEAD:** `f9926cb4`
**Diff range:** `main..worktree-lane-subagent-cost`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: to-cc/LANE-5B4-16-subagent-cost.md (BATCH-WAVE5B-N4, row L5, [#Context 5] recursive attribution).
Reviews scripts/lane_cost.py and scripts/routing_agreement.py: both now read a session's
sibling <session-id>/subagents/*.jsonl directory (keyed per session, verified against real
on-disk data on this host) in addition to the top-level transcript, classifying each model
use as main/subagent. Please verify: (1) the per-session keying is correct and does not
blend two sessions' subagents together, (2) de-duplication across main/subagent roles is
sound, (3) lane_usage/ran_models remain backward compatible for callers that do not care
about role, (4) the new fixture tests/fixtures/subagent_session/ has no real transcript
content.

---

## Findings
## Critical

(none)

## High

## [HIGH] .github/workflows/conductor.yml:91 — Matrix check contexts are not validated against required-check contexts

**What:** The `pytest` matrix emits OS-suffixed GitHub check contexts, while the existing test only compares required contexts to job IDs and therefore treats plain `pytest` as valid.  
**Why:** When required checks are enabled, a stale plain `pytest` requirement will never receive a result and can block branch updates indefinitely.  
**Fix direction:** Assert the exact check-context names emitted by the matrix against the declared required contexts.

## [HIGH] scripts/routing_agreement.py:347 — Main/subagent model messages are not de-duplicated

**What:** `_tally_transcripts()` has no `message.id`/`uuid` seen-set, so `ran_models()` counts a record twice if it appears in both a main and subagent transcript.  
**Why:** The duplicate can inflate a model’s tally and change the dominant `ran_model`, producing a false routing agreement or divergence.  
**Fix direction:** Carry one identity-based seen-set across both role path lists, matching the cross-role deduplication already used by `lane_cost`.

## Medium

(none)

## Low

(none)

---

## Disposition (ruling (e): fix P1, record the rest)

- **`scripts/routing_agreement.py:347`** — **FIXED**, commit `2bcd2f9d`: `_tally_transcripts` now
  takes a `seen` set threaded across both roles, matching `lane_cost.py`'s own cross-role
  de-duplication. Regression test:
  `test_a_turn_replayed_across_main_and_subagent_is_counted_once`.
- **`.github/workflows/conductor.yml:91`** — **OUT OF SCOPE for this lane.** The diff range
  `main..worktree-lane-subagent-cost` widened to include `lane-ci-matrix`'s CI-matrix commits
  because the local pinned `main` lags `origin/main` (architecture note: local `main` is not
  remote). This file is not in `lane-subagent-cost`'s **Files you own**; recorded here as a
  candidate row for the integrator's digest — see `ROWS-OWED` in
  `to-browser/SESSION-lane-subagent-cost.md`.