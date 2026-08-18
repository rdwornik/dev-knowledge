---
id: "[#428]"
title: "`nightly-triage` reports a dead producer to every session start"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#428] [P2][S] **`nightly-triage` reports a dead producer to every session start** — the producer has been dead since 2026-07-09 (`.github/workflows/nightly-conformance-triage.yml` deleted at `82227f08`, on no branch; last Issue 2026-06-25) yet **15 Issues stay open and every SessionStart tells the operator they await action**. **NOT [#426]'s class**: this is a **live consumer fed a false claim by a producer that no longer runs**. **NARROWED by [#434]'s ruling — BUILD THE CONSUMER**; the acceptance contract must close or explicitly disclaim the structural-drift blind spot. **Leg 2 is PARTIAL and leg 1 undischarged, so the row stays OPEN.** · Done when: no session-start surface asserts pending work from a producer with no run in the last 30 days (with a test seeding a dead producer), and the GitHub Issue backlog is either closed out or `scripts/surface_triage.ps1` no longer reads it — with the Issue count at closing time recorded in the commit · refs #255, #419, #426, scripts/surface_triage.ps1, `82227f08` · kill-candidates: none — [#426] covers undeclared consumers, not false claims from dead producers · serialize-group: settings-json · source: docs/audits/2026-08-15-technical-night3-decision-queue.md D5/D6, which carry the partial-discharge wording and the locator correction
