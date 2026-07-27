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

- [#428] [P2][S] **`nightly-triage` reports a dead producer to every session start** — the triage producer has been dead since 2026-07-09 (`.github/` deleted at `82227f08`, on no branch; last Issue 2026-06-25) yet **15 Issues stay open and every SessionStart — including the one that found this — tells the operator they await action**. **NOT [#426]'s class:** [#426] is routines with no declared consumer; this is a **live consumer being fed a false claim by a producer that no longer runs**. Also record that `scripts/surface_triage.ps1`'s own header documents the identical defect diagnosed under **#255** ("a PR-triggered organ under a local-merge workflow was vacuous — it never fired") and never generalized — **third habitat of this class in one session**, after [#424]'s inert gates and [#419]'s unread branches. · Done when: no session-start surface asserts pending work from a producer that does not run, AND the 15 open Issues are dispositioned or the surface is retired · refs #255, #419, #426, scripts/surface_triage.ps1, `82227f08` · kill-candidates: none — [#426] covers undeclared consumers, not false claims from dead producers · serialize-group: settings-json
