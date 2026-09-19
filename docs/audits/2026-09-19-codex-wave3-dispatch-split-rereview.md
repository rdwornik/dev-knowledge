# Codex Review — wave3-dispatch-split-rereview

**Date:** 2026-09-19
**Branch:** `worktree-wave3-dispatch-split`
**HEAD:** `10868a8e`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/0/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Re-review after fixes 12977bdb to a prior 1 CRITICAL / 1 HIGH (prior artifact: docs/audits/2026-09-19-codex-wave3-dispatch-split.md). Verify each is actually fixed, and look for NEW defects in scripts/dispatch.py (govern, govern_cmd, find_lane_by_slug, bind_lane, lane_alive, commit_witness, plan_cmd, parse_contract_model_effort) and templates/dispatch-shim.ps1.
- Contract of the lane: dispatch.py never starts a lane; the shim is the sole spawner; a default --bg launch binds usage by session id with no --slug-dir; an unbindable/blind/over-cap lane is STOPPED (exit 5/3), exit 4 only when the lane may still be running; model/effort come from the contract table or a flag, never a default.

---

## Findings
Prior audit verification: both prior findings are fixed—missing IDs now use worktree discovery, and an already-ended blind lane exits 5 rather than 4.

## Critical

## [CRITICAL] templates/dispatch-shim.ps1:129 — An arbitrary 8-hex token can select the wrong lane

**What:** The shim treats the first lowercase 8-hex token in launcher output as the lane ID; `govern` then accepts a successful binding without verifying that its `cwd` matches the planned slug’s worktree.  
**Why:** A false match can govern/stop another live lane while the newly launched lane remains running uncapped.  
**Fix direction:** Treat the parsed token as provisional and require the bound entry’s worktree to match the planned slug; otherwise rediscover the unique lane by worktree or report it may still be running.

## [CRITICAL] scripts/dispatch.py:621 — Transcript-read failures leave the bound lane running

**What:** Exceptions from `lane_cost.seat_usage()`—for example malformed numeric usage in a transcript or a filesystem enumeration error—escape `_session_reader` and bypass `govern()`’s refusal/stop path.  
**Why:** The governor exits with an exception while the launched lane continues without a cap.  
**Fix direction:** Convert transcript-read failures into an unobservable-lane verdict and route them through the existing fail-closed stop behavior.

## High

(none)

## Medium

(none)

## Low

(none)

---

## Disposition (author's, appended before commit)

Range `main...HEAD` (three-dot: this lane's own commits). The reviewer confirmed both findings of
the first pass fixed, and raised two new CRITICALs against the fix commit `12977bdb`'s tree:

- **CRITICAL (shim:129, wrong lane selected)** -- accepted. RED `5bc9c3f9`, fixed `e60712d2`:
  `_bind` requires the bound entry's cwd to be `.../worktrees/<slug>`, drops a provisional id that
  belongs to another lane and rediscovers ours by worktree; never stops another lane. The shim's id
  match is also anchored on the `backgrounded` line.
- **CRITICAL (dispatch.py:621, transcript-read exception)** -- accepted. RED `5bc9c3f9`, fixed
  `e60712d2`: `_session_reader` reads any failure as unobservable (-> stop after the blind polls);
  and `govern_cmd` stops the bound lane on ANY unexpected exception (exit 5; 4 only if that stop
  fails). The class, not only the instance.

A third pass over `e60712d2` follows (`...-rereview-2.md`).

no-consumer: lane output awaiting integrator merge (wave 3, L3 split); it files and closes no BACKLOG row, so no [#id] cites it yet.