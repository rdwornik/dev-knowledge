---
id: "[#426]"
title: "Declare `consumer` + `consumption_path` for every LIVE routine"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#426] [P2][M] **Declare `consumer` + `consumption_path` for every LIVE routine** — ADR-105's activation gate governs exactly ONE backlog row ([#348]); the routines that actually emit unconsumed output are hooks and schedules, none of which is a BACKLOG row and so none is checked. L0 counted **30**: session hooks **12** · commit-time gates **15** · scheduled/remote **3**; full table in JOURNAL 2026-07-26. Priority driver: `nightly-triage` has a **DEAD producer** (`.github/` deleted at `82227f08`) yet **15 Issues stay open, surfaced every session start**; `automation/fleet-audit` is STALE. · Done when: every live routine declares a consumer and consumption path or is retired, and the dead-producer nags are resolved · refs ADR-105, #419, scripts/surface_triage.ps1, .claude/settings.json · kill-candidates: none — [#419] frames the defect, this executes the retrofit · routine: trigger=operator night-batch request · scope=hub night-batch reports (branch-only) · consumer=the morning verification batch · consumption_path=branch-only night output → local gates → operator merge · verified_by=local pytest + audit.py ship-gate · review_date=2026-08-26 · serialize-group: settings-json
