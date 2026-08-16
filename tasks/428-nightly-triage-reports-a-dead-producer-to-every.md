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

- [#428] [P2][S] **`nightly-triage` reports a dead producer to every session start** — the producer has been dead since 2026-07-09 (`.github/workflows/nightly-conformance-triage.yml` deleted at `82227f08`, on no branch; last Issue 2026-06-25) yet **15 Issues stay open and every SessionStart tells the operator they await action**. **[LOCATOR CORRECTED 2026-08-16, night3 decision-queue D6]:** `.github/` now exists again (holds the unrelated `[#501]` report-only wall workflow), which falsified the row's prior evidence clause naming the whole deleted directory — the dead producer was always the one deleted workflow file named above; the premise (no nightly-conformance producer runs) still holds. **NOT [#426]'s class** (routines with no declared consumer): this is a **live consumer fed a false claim by a producer that no longer runs**. `surface_triage.ps1`'s header documents the identical defect under **#255** (a PR-triggered organ under a local-merge workflow, vacuous — never fired), never generalized — a repeating habitat this session ([#424], [#419]). **NARROWED by [#434]'s ruling — BUILD THE CONSUMER; the acceptance contract must close or explicitly disclaim the structural-drift blind spot.** **[LEG 2 PARTIAL, `PHASE2-MAX-PACK.md` §A1 / night3 decision-queue D5]:** the ruled 15-Issue GitHub-backlog closure (recording count 15 in its own closing commit) discharges leg 2's count-recording clause but NOT leg 1 (the dead-producer test) — row stays OPEN, leg 1 undischarged; no closure, no birth taken here. · Done when: no session-start surface asserts pending work from a producer with no run in the last 30 days (with a test seeding a dead producer), and the GitHub Issue backlog is either closed out or `scripts/surface_triage.ps1` no longer reads it — with the Issue count at closing time recorded in the commit · refs #255, #419, #426, scripts/surface_triage.ps1, `82227f08` · kill-candidates: none — [#426] covers undeclared consumers, not false claims from dead producers · serialize-group: settings-json
