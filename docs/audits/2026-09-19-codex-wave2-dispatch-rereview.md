# Codex Review â€” wave2-dispatch-rereview

**Date:** 2026-09-19
**Branch:** `worktree-wave2-dispatch`
**HEAD:** `da321ac5`
**Diff range:** `main..worktree-wave2-dispatch`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/2/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes â€” [#469])
**Review profile:** code

---

## Focus

Re-review scripts/dispatch.py after fixes to a prior 4 CRITICAL / 2 HIGH review (other-provider key scrub, unobservable usage = UNGOVERNED, failed stop, blind liveness probe, streamed child exit, codex post-hoc label). Verify each is actually fixed and look for new defects in govern(), run_streamed(), child_env().

---

## Findings
## Critical

### [CRITICAL] scripts/dispatch.py:379 â€” Background-lane usage is not locatable

**What:** `_lane_reader()` calls `lane_usage(slug)` without the required transcript-directory mapping for a `claude --bg` lane.  
**Why:** Background lanes are stored under the launching session rather than a slugged directory, so normal launches remain unreadable and become UNGOVERNED while the lane continues uncapped.  
**Fix direction:** Capture the actual transcript/session locator at launch and use it for both baseline and polling; refuse launch if it cannot be bound.

### [CRITICAL] scripts/dispatch.py:368 â€” Streamed usage can be silently treated as zero

**What:** `run_streamed()` returns a successful under-cap verdict even if it parsed no valid usage event.  
**Why:** A changed/malformed provider stream can consume tokens but exit zero and be reported as `used 0`, bypassing the intended UNGOVERNED posture for unobservable spend.  
**Fix direction:** Track whether attributable usage was observed and return an UNGOVERNED verdict when none is available.

## High

### [HIGH] scripts/dispatch.py:468 â€” Stop and liveness subprocess failures can escape uncapped

**What:** The `claude stop` and `claude agents --json` calls have neither timeouts nor handling for execution errors.  
**Why:** A hung or failed control command raises or blocks outside the existing `False`/`GovernorBlind` handling, terminating the governor without an UNGOVERNED result while the lane may continue.  
**Fix direction:** Use bounded subprocess calls and convert timeout/OS failures into the existing failed-stop or blind-governor verdicts.

### [HIGH] scripts/dispatch.py:361 â€” Streamed termination is not verified

**What:** The over-cap branch calls `proc.terminate()` and immediately reports the lane stopped without waiting for or checking process exit.  
**Why:** A process that ignores or outlives termination can continue after a â€œCAP EXCEEDED -- lane stoppedâ€ result.  
**Fix direction:** Wait with a timeout, escalate termination as needed, and report UNGOVERNED if the process cannot be confirmed stopped.

## Medium

(none)

## Low

(none)

no-consumer: lane output awaiting integrator merge (night wave 2, L3); it files and closes no BACKLOG row, so no [#id] cites it yet.
