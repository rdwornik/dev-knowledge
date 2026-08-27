---
id: "[#273]"
title: "Changelog-review staleness escalation"
status: deferred
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#273] [P3][S] Changelog-review staleness escalation (intake doc #2 R3) — the SessionStart sentinel nudges, but a month-long unreviewed window (2.1.178–2.1.201) happened anyway; add escalation teeth: unreviewed-window > N versions or > 14 days surfaces in the morning triage (a fleet_health digest line), not just a boot line · Done when: an over-threshold window renders an escalation line in the SessionStart digest (with a test) and the N/days thresholds are recorded · refs scripts/changelog_sentinel.py, scripts/fleet_health.py, ecosystem/tool-versions.yaml, docs/intake/archive/2026-07-06-platform-feature-scan.md §6 R3 · serialize-group: settings-json · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
