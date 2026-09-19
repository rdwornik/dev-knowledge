# Codex Review — wave3-dispatch-split-rereview-3

**Date:** 2026-09-19
**Branch:** `worktree-wave3-dispatch-split`
**HEAD:** `242b7061`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/0/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Fourth pass. Verify the two CRITICALs of docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview-2.md are fixed by c5808275 (only a VERIFIED lane id is ever stopped: _bind, verified, _recover, _safe_stop), and look for NEW defects in scripts/dispatch.py (govern, govern_cmd, _bind, _recover, _safe_stop, find_lane_by_slug, bind_lane, lane_alive, commit_witness) and templates/dispatch-shim.ps1.
- Lane contract: dispatch.py never starts a lane; the shim is the sole spawner; usage bound by session id, no --slug-dir; unbindable/blind/over-cap/failed-governor lane STOPPED (exit 5/3), exit 4 only when the lane may still be running; model/effort from the contract table or a flag, never defaulted.

---

## Findings
## Critical

## [CRITICAL] scripts/dispatch.py:783 — A stale ended lane can be accepted as the verified lane

**What:** `_bind()` accepts a provisional listing entry solely because its `cwd` matches; unlike `find_lane_by_slug()`, it does not require a live state.  
**Why:** A false shim ID can bind an old `done` record for the same worktree, report completion/stop that stale ID, and leave the newly launched live lane uncapped.  
**Fix direction:** Require the binding accepted before assigning `verified` to be live and still match the requested worktree; otherwise continue safe discovery.

## [CRITICAL] templates/dispatch-shim.ps1:139 — Governor invocation failures leave the spawned lane uncapped

**What:** The shim forwards any failure from `Invoke-Hub $governArgs` directly to the shell, with no recovery or contract-normalized exit.  
**Why:** If `uv`/Python/govern fails before `govern_cmd` reaches its recovery handler, the already-started background lane continues without a governor and the shim can exit with an arbitrary code (for example 1), not the required 4/5/3 outcome.  
**Fix direction:** Handle abnormal governor-invocation failures in the shim with safe re-binding/stop recovery; if the lane cannot be proven, explicitly return the “may still be running” exit-4 verdict.

## High

(none)

## Medium

(none)

## Low

(none)

---

## Disposition (author's, appended before commit)

Fourth pass, `main...HEAD` at `242b7061`. Both prior CRITICALs (`c5808275`) were not re-raised; two
new ones came against the binding and the shim:

- **CRITICAL (dispatch.py:783, a stale ENDED record accepted as the lane)** -- accepted. RED
  `7aa37b0a`, fixed `1f742353`: `LaneBinding.live`; `_bind` drops a non-live record and rediscovers
  the live lane by worktree.
- **CRITICAL (shim:139, governor invocation failure leaves the lane uncapped)** -- accepted. RED
  `7aa37b0a` (including a real-pwsh test of the shim against stub `uv`/`claude`), fixed `1f742353`:
  new hub verb `stop --slug`; the shim passes the documented governor codes through and otherwise
  recovers via `stop`, ending 5 or 4.

A fifth pass over `1f742353` follows (`...-rereview-4.md`).

no-consumer: lane output awaiting integrator merge (wave 3, L3 split); it files and closes no BACKLOG row, so no [#id] cites it yet.