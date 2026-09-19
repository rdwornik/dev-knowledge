# Codex Review â€” wave2-dispatch

**Date:** 2026-09-19
**Branch:** `worktree-wave2-dispatch`
**HEAD:** `f6a02d58`
**Diff range:** `main..worktree-wave2-dispatch`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 4/2/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes â€” [#469])
**Review profile:** code

---

## Focus

Review scripts/dispatch.py: token cap enforcement correctness (governor, stream meter), env scrubbing for third-party providers, injection via argv, race/overshoot handling, and dry-run vs live paths.

---

## Findings
## CRITICAL

## [CRITICAL] scripts/dispatch.py:189 â€” Third-party launches retain other provider API keys

**What:** `child_env()` removes only Anthropic credentials; selecting DeepSeek, ZAI, or Moonshot passes the other providersâ€™ API-key environment variables through to the selected third party.  
**Why:** An unrelated provider credential can be exposed to a third-party-backed child process.  
**Fix direction:** Construct a provider-specific environment or scrub all known provider secrets except the selected providerâ€™s required key.

## [CRITICAL] scripts/dispatch.py:346 â€” Missing transcript is reported as zero usage

**What:** `_lane_reader()` converts an absent/unreadable lane transcript into an all-zero `TokenUsage`, and the governor can subsequently report â€œfinished under cap.â€  
**Why:** A lane whose spend cannot be observed is ungoverned, but this path falsely reports successful cap enforcement.  
**Fix direction:** Preserve a distinguishable â€œusage unavailableâ€ state and exit UNGOVERNED rather than treating it as zero spend.

## [CRITICAL] scripts/dispatch.py:435 â€” Failed stop is reported as a successful cap stop

**What:** `stop()` discards the return status of `claude stop`, while `_report()` unconditionally says the lane was stopped.  
**Why:** If the stop command fails, the lane can continue spending after the cap while the dispatcher reports enforcement.  
**Fix direction:** Check the stop result and verify the lane has exited; report an ungoverned failure and retain/escalate termination on failure.

## [CRITICAL] scripts/dispatch.py:304 â€” Codex stream meter only receives usage after the turn completes

**What:** The Codex path counts usage only from `turn.completed`, then terminates after that event arrives.  
**Why:** The over-cap Codex turn has already completed before the meter can act, so an individual turn can overshoot the cap without a bound.  
**Fix direction:** Use a source that provides incremental usage or explicitly refuse/label this mode as post-hoc accounting rather than enforced metering.

## HIGH

## [HIGH] scripts/dispatch.py:438 â€” Status-query failure is interpreted as lane completion

**What:** `alive()` returns `False` when `claude agents --json` fails or returns malformed/empty output.  
**Why:** The governor then exits with success and reports an under-cap lane even though the background lane may still be running.  
**Fix direction:** Check the subprocess result and treat an unavailable status query as UNGOVERNED, not as proof of completion.

## [HIGH] scripts/dispatch.py:337 â€” Streamed child failures exit as successful under-cap runs

**What:** `run_streamed()` ignores the child process return code and always returns a non-exceeded verdict after EOF.  
**Why:** A failed `codex exec` is reported with exit code 0 as â€œfinished under cap,â€ masking a failed or partially metered launch.  
**Fix direction:** Propagate non-zero child exits as dispatch failures distinct from a completed under-cap run.

## MEDIUM

(none)

## LOW

(none)