# Codex Review — lane-launch-adapter

**Date:** 2026-09-21
**Branch:** `worktree-lane-launch-adapter`
**HEAD:** `3a3a9f00`
**Diff range:** `main..worktree-lane-launch-adapter`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low, counted from the Findings section below. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/dispatch.py launch_lane / _held_by / _SlugLock / _identify: refuses a collision (live job, live lane in the worktree, fresh unlisted receipt, lock); spawns exactly once; intent receipt before the spawn; unidentified start is exit 8.
- scripts/dispatch.py monitor / govern_cmd / _watch: MUST NEVER stop, pause or kill a lane under any condition -- read every subprocess, signal, timeout and exception path.
- scripts/dispatch.py parse_dispatch_block / request_from_contract / _validate_line: the Dispatch block is read for fields, never run; hostile values refused.
- scripts/dispatch.py run_prelaunch / _pre_launch_gaps: runs the declared pre-launch moment; a skipped or missing organ does not clear a launch.
- templates/dispatch-shim.ps1: thin wrapper; -DryRun, -Run, -Help; needs no cap; exit code of launch comes back unchanged.
- tests/test_dispatch_launch.py: any assertion that would still pass if the implementation were stubbed; the declared harness row is run as written.

---

## Findings
## Critical

### scripts/dispatch.py:817 — Fresh Codex intent receipts do not hold the slug

**What:** `_held_by()` returns immediately for any Codex receipt when it lacks a recorded live PID, bypassing the fresh-unlisted-receipt check at lines 827–829.  
**Why:** If Codex starts but record finalization is interrupted, a second launch can start during the listing/receipt gap, violating single-launch/worktree safety.  
**Fix direction:** Apply the fresh-receipt hold to incomplete Codex receipts too; only permit relaunch after reliable evidence the prior process is no longer live.

## High

### tests/test_dispatch_launch.py:710 — “Interrupted after provider started” test never starts a provider

**What:** The injected `spawn` raises `KeyboardInterrupt` before returning a started process, so the test only proves a pre-spawn intent receipt blocks a second launch.  
**Why:** It passes if the post-spawn/interrupted-record path is broken, including the uncovered Codex collision path above.  
**Fix direction:** Exercise an interruption or write failure after a successful spawn, and assert a second launch is refused while the started lane remains live.

## Medium

(none)

## Low

(none)

---

## Disposition (recorded by the lane, after commit `925ffa7b`; the review text above is verbatim)

| finding | verdict | what was done |
|---|---|---|
| Critical, `_held_by` — a Codex receipt with no recorded live pid skips the fresh-receipt hold | **Real. Fixed** in `925ffa7b` | An INTENT receipt is written before `Popen`, so a Codex receipt with no pid can mean the process already started. It now holds the slug while it is younger than `LISTING_LAG_SECONDS`; only a pid the OS reports dead (or an aged, pid-less receipt) releases it. Test: `test_a_fresh_codex_intent_receipt_with_no_pid_yet_holds_the_slug`. Mutation (drop the age hold) → that test goes RED. |
| High, test — "interrupted after provider started" never starts a provider | **Real. Fixed** in `483c7ec4` | Added `test_an_interrupt_after_a_successful_spawn_leaves_the_started_lane_holding_its_slug`: the spawn SUCCEEDS, then the record write is interrupted, and a second launch is refused. The older pre-spawn-interrupt test stays; it proves a different, real property (the intent receipt exists before the spawn). Mutation (no intent receipt) → the new test goes RED. |

Recorded honestly: the review ran against `3a3a9f00`; the fixes are in later commits, and the tests named above were run RED-then-GREEN, not re-reviewed by Codex. No Medium or Low findings.