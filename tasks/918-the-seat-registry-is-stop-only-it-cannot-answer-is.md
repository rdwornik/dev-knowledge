---
id: "[#918]"
title: "The seat registry is Stop-only -- it learns about a seat when it ends, so it cannot answer \"is this seat live\""
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-SPINE-AND-B3-2026-09-19"
generates: BACKLOG.md
---

- [#918] [P2][M] **The seat registry is Stop-only -- it learns about a seat when it ends, so it cannot answer "is this seat live"** - `~/.claude/seat-registry.jsonl` ([#833]) on 2026-09-19: 165 rows -- 162 `Stop` events, 4 binds (all 2026-09-17/18), ZERO `SessionStart` rows. Its only writer is the Stop hook (`scripts/session_end_backpressure.py:558`); `seat_registry.py:104` maps SessionStart/UserPromptSubmit as events, but `seat_registry` appears in neither `.claude/settings.json` nor `~/.claude/settings.json`, so nothing ever records a seat starting. It never saw witness `4c128d01` (killed mid-first-turn, never reached a Stop), and `absent` is derived from a dead pid / missing worktree / SessionEnd (`seat_registry.py:38`), so a stopped-then-resumed session reads `absent` exactly when it is about to come back. Its refusals are step-0 boot refusals only (`seat_refusals.py:refuse_lane_owned`, `refuse_no_live_integrator`); no teardown path reads it. The surface that DID know the witness was bound is `~/.claude/jobs/<id>/state.json` (`worktreePath`, `state: running`, `respawnFlags`) · Done when: the registry records a seat at start (a wired SessionStart writer, or it reads the daemon's job records) and answers "is seat X live" correctly for a `--bg` lane across stop, daemon-resume and `claude rm`, witnessed live; or the registry is retired as a liveness source and `[#916]`'s teardown check names the job record instead, by ruling · implements: DECLARE-SPINE-AND-B3-2026-09-19 · refs filed by the wave-3 close operator order 2026-09-19, `scripts/seat_registry.py`, `scripts/session_end_backpressure.py:558`, SCAN-live-worktree-teardown-am5-contracts-2026-09-19.md section 1c, `[#833]`, `[#916]`
