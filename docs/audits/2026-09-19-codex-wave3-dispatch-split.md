# Codex Review — wave3-dispatch-split

**Date:** 2026-09-19
**Branch:** `worktree-wave3-dispatch-split`
**HEAD:** `f09c7ac8`
**Diff range:** `main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/1/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Layer-2 split: scripts/dispatch.py must not start any lane (plan + govern only); templates/dispatch-shim.ps1 is the sole spawner. Look for any remaining spawn path, and for the shim running an argv/env it did not get from the hub plan.
- Token cap: a default --bg launch binds its own usage by session id from claude agents --json (bind_lane, _session_reader -> lane_cost.seat_usage). An unbindable / blind / probe-failed lane must be STOPPED (exit 5), never left running as ungoverned; only a failed stop is ungoverned (exit 4). Look for any path where a running lane escapes the cap or is reported under-cap without its spend having been observed.
- No model/effort default: model and effort come from the contract's | Model | Mode | Effort | table or an explicit flag; a contract with neither is refused (plan). Check parse_contract_model_effort and the shim for a default.
- DONE means a commit (commit_witness: reflog start point vs tip) and USER-scope CLAUDE_PROMPTS_DIR (windows_user_env) are preserved behaviours.

---

## Findings
## Critical

## [CRITICAL] templates/dispatch-shim.ps1:129 — Lane can be launched but left uncapped when its ID is not parsed

**What:** A successful launch whose output lacks a lowercase 8-hex token exits 4 and tells the operator to stop it manually.  
**Why:** This leaves a running lane outside governance; exit 4 is used without a failed stop, violating the required fail-closed token-cap behavior.  
**Fix direction:** Use a reliable, validated lane-identity handoff and attempt a programmatic stop before returning; reserve exit 4 for a verified stop failure.

## High

## [HIGH] scripts/dispatch.py:190 — Blind lane completion returns ungoverned without attempting stop

**What:** If usage is unreadable and `lane_alive()` reports done before `blind_polls`, `govern()` returns `EXIT_UNGOVERNED` directly.  
**Why:** A non-observed lane is neither stopped nor refused, so exit 4 no longer exclusively represents a failed stop as required.  
**Fix direction:** Treat this blind completion path as fail-closed: attempt stop and return refusal on success, or ungoverned only if that stop fails.

## Medium

(none)

## Low

(none)

---

## Disposition (author's, appended before commit)

- **RANGE CAVEAT.** The wrapper was given `main..HEAD`, a TWO-dot range: it diffs main's tree
  against this branch's, so it also carried the wave-2 lanes L1/L2/L4/L5 that main has and this
  branch (based on L3, `c00f9c10`) does not -- the file list above includes `pyproject.toml`,
  `scripts/dodo.py`, `scripts/stage_library_first.py` and others that are not this lane's. Both
  findings are nonetheless in this lane's own files. The re-review uses `main...HEAD`.
- **CRITICAL (shim:129)** -- accepted. RED `1a64ce57`, fixed `12977bdb`: `govern` finds a lane whose
  id the shim could not read by its worktree cwd; ambiguity is None, never a guess.
- **HIGH (dispatch.py:190)** -- accepted in part. The lane had already ENDED, so a stop attempt has
  nothing to act on; the defect was the exit code. It is now REFUSED (exit 5, no stop call), which
  keeps exit 4 meaning "the lane may still be running". RED `1a64ce57`, fixed `12977bdb`.

no-consumer: lane output awaiting integrator merge (wave 3, L3 split); it files and closes no BACKLOG row, so no [#id] cites it yet.