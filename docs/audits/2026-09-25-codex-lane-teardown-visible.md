# Codex Review — lane-teardown-visible

**Date:** 2026-09-25
**Branch:** `worktree-lane-teardown-visible`
**HEAD:** `deef3e83`
**Diff range:** `main..worktree-lane-teardown-visible`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

no-consumer: this lane files no BACKLOG row of its own for these findings -- both were fixed
directly in the same session's follow-up commit `9582c4ab`, the same direct-disposition route
`2026-09-25-codex-lane-launcher-fixes.md`'s own no-consumer line takes for its findings.

---

## Focus

- R3: teardown must STOP a lane's session (batch_janitor.py), never claude rm it, so the session and its transcript survive.
- no_leftovers.py checks 8/9 were changed to be state-aware (a job record / agents entry pointing at a torn-down lane is only a leftover if its own state is NOT terminal per batch_janitor._ENDED_STATES); verify this reasoning and the fail-closed behavior on missing/unknown state.
- templates/integrator-order-template.md teardown step and Close-digest step were reworded for R3 (stop not remove; per-lane session id + transcript path in the digest).
- tests/test_teardown_visible.py is new -- verify it actually proves the property end-to-end via injected seams (batch_janitor's agents/run seam, no_leftovers's throwaway-hub fixture, routing_agreement.transcript_paths) rather than trivially passing.

---

## Findings
## Critical

(none)

## High

### tests/test_teardown_visible.py:111 — Session survival is fabricated, not observed through the janitor seam

**What:** The test supplies a stopped second janitor listing but never asserts `report.after`; it then constructs an unrelated `after_agents` record after teardown.  
**Why:** It can pass without proving that the janitor’s post-stop observation preserves the session/listing required by R3.  
**Fix direction:** Model one shared agent listing in the injected `run`/`agents` seams, assert `report.after` contains the stopped session, and pass that same listing to `no_leftovers`.

### tests/test_no_leftovers.py:269 — Unknown terminal-state vocabulary is not regression-tested

**What:** Tests cover known terminal and missing/non-terminal states, but not a pointing record with an unknown string state.  
**Why:** A future permissive change could classify a newly introduced or malformed state as terminal, silently passing checks 8/9 contrary to the fail-closed requirement.  
**Fix direction:** Add job-record and agents-entry cases with an unknown state value and assert both checks fail.

## Medium

(none)

## Low

(none)

---

## Dispositions (lane-teardown-visible, same session, commit `9582c4ab`)

- **HIGH 1 (Session survival is fabricated, not observed through the janitor seam) —
  ACCEPTED, fixed.** `after_listing` is now one shared object: it is what the injected
  `agents` callable returns on the janitor's post-stop read AND what is passed to
  `no_leftovers.run_checks` below. The test now asserts `report.after` itself names the
  session `stopped`/`live=False` before ever touching `no_leftovers`.

- **HIGH 2 (Unknown terminal-state vocabulary is not regression-tested) — ACCEPTED, fixed.**
  Added `test_8_fails_closed_on_a_pointing_record_with_an_UNKNOWN_state` and
  `test_9_fails_closed_on_a_pointing_entry_with_an_UNKNOWN_state`
  (`tests/test_no_leftovers.py`), each pinning that a `state` value absent from
  `batch_janitor._ENDED_STATES` still fails the check rather than reading as terminal.

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-25-codex-lane-teardown-visible.md | ACTIONED | 9582c4ab |