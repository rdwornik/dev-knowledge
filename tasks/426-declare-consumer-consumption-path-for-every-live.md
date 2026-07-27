---
id: "[#426]"
title: "Declare `consumer` + `consumption_path` for every LIVE routine"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#426] [P2][M] **Declare `consumer` + `consumption_path` for every LIVE routine** — ADR-105's activation gate governs exactly ONE backlog row ([#348]); the routines that actually emit unconsumed output are hooks and schedules, none of which is a BACKLOG row and none of which is therefore checked. L0 enumeration 2026-07-26 counted **30**: session hooks **12** (SessionStart 6 · Stop 3 · PreToolUse 2 · Notification 1, across global/project/plugin layers — the global layer and Notification class were both missed on first pass) · commit-time gates **15** · scheduled/remote **3**. Priority driver: `nightly-triage` has a **DEAD producer** (`.github/` deleted at `82227f08`, last Issue 2026-06-25) yet **15 Issues stay open, surfaced every session start**; `automation/fleet-audit` is STALE. Full table in this session's JOURNAL entry. · Done when: every live routine declares a consumer and consumption path or is retired, and the dead-producer nags are resolved · refs ADR-105, #419, scripts/surface_triage.ps1, .claude/settings.json · kill-candidates: none — [#419] frames the defect, this executes the retrofit · serialize-group: settings-json
