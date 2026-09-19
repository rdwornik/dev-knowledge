# Codex Review — wave3-dispatch-split-rereview-2

**Date:** 2026-09-19
**Branch:** `worktree-wave3-dispatch-split`
**HEAD:** `236295b6`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/0/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Third pass. Verify the two CRITICALs of docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview.md are actually fixed by e60712d2 (wrong-lane id: _bind/_cwd_is_lane; transcript-read exception: _session_reader and the govern_cmd catch-all), and look for NEW defects in scripts/dispatch.py (govern, govern_cmd, _bind, find_lane_by_slug, bind_lane, lane_alive, commit_witness) and templates/dispatch-shim.ps1.
- Lane contract: dispatch.py never starts a lane; the shim is the sole spawner; usage is bound by session id with no --slug-dir; an unbindable/blind/over-cap/failed-governor lane is STOPPED (exit 5/3), exit 4 only when the lane may still be running; model/effort from the contract table or a flag, never defaulted.

---

## Findings
## Critical

## [CRITICAL] scripts/dispatch.py:735 — Exception cleanup can stop an unverified provisional ID

**What:** `KeyboardInterrupt` (and the catch-all at line 741) stops `lane_id` even if `_bind()` was interrupted before rejecting a provisional ID whose `cwd` belongs to another lane.  
**Why:** A false ID parsed by the shim can still stop another live lane during a control-plane failure or Ctrl-C.  
**Fix direction:** Track a separately verified lane ID only after its worktree has matched the requested slug; only that ID may be stopped by recovery paths.

## [CRITICAL] scripts/dispatch.py:741 — Failure handling can itself escape without an exit-4/5 verdict

**What:** The catch-all recovery directly calls `stop_lane()` without protecting that call; an exception during stop (including Ctrl-C) escapes the governor.  
**Why:** The lane may remain running while the command exits outside the contract’s refused/ungoverned exit codes.  
**Fix direction:** Contain stop failures in both recovery handlers and return exit 4 when termination cannot be confirmed.

## High

(none)

## Medium

(none)

## Low

(none)

---

## Disposition (author's, appended before commit)

Third pass, `main...HEAD` at `236295b6`. Both prior CRITICALs (`e60712d2`) were confirmed fixed; two
new ones were raised against that fix, both in the RECOVERY path it added:

- **CRITICAL (dispatch.py:735, an unverified id can be stopped in recovery)** -- accepted. RED
  `84008b9d`, fixed `c5808275`: a `verified` id is set only after the lane's listed worktree matched
  the slug, and it is the only id any recovery path may stop; `_bind` drops an unlisted or foreign id.
  A lane nothing verified is UNGOVERNED (exit 4, "may be running"), never a guessed stop.
- **CRITICAL (dispatch.py:741, recovery can itself escape)** -- accepted. RED `84008b9d`, fixed
  `c5808275`: `_safe_stop` contains a stop that raises or is interrupted; `_recover` always reaches
  exit 5 (stopped) or exit 4 (not confirmed).

A fourth pass over `c5808275` follows (`...-rereview-3.md`).

no-consumer: lane output awaiting integrator merge (wave 3, L3 split); it files and closes no BACKLOG row, so no [#id] cites it yet.