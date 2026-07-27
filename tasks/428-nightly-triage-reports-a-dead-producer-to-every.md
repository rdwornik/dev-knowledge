---
id: "[#428]"
title: "`nightly-triage` reports a dead producer to every session start"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#428] [P2][S] **`nightly-triage` reports a dead producer to every session start** — the producer has been dead since 2026-07-09 (`.github/` deleted at `82227f08`, on no branch; last Issue 2026-06-25) yet **15 Issues stay open and every SessionStart tells the operator they await action**. **NOT [#426]'s class** (routines with no declared consumer): this is a **live consumer fed a false claim by a producer that no longer runs**. `surface_triage.ps1`'s header documents the identical defect under **#255** ("a PR-triggered organ under a local-merge workflow was vacuous — it never fired"), never generalized — **third habitat in one session** ([#424] inert gates, [#419] unread branches). **NARROWED by [#434]'s ruling — BUILD THE CONSUMER; the acceptance contract must close or explicitly disclaim the structural-drift blind spot.** · Done when: no session-start surface asserts pending work from a producer that does not run, AND the 15 open Issues are dispositioned or the surface is retired · refs #255, #419, #426, scripts/surface_triage.ps1, `82227f08` · kill-candidates: none — [#426] covers undeclared consumers, not false claims from dead producers · serialize-group: settings-json
