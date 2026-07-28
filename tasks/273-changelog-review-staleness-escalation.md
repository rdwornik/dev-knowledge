---
id: "[#273]"
title: "Changelog-review staleness escalation"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#273] [P3][S] Changelog-review staleness escalation (intake doc #2 R3) — the SessionStart sentinel nudges, but a month-long unreviewed window (2.1.178–2.1.201) happened anyway; add escalation teeth: unreviewed-window > N versions or > 14 days surfaces in the morning triage (a fleet_health digest line), not just a boot line · Done when: an over-threshold window renders an escalation line in the SessionStart digest (with a test) and the N/days thresholds are recorded · refs scripts/changelog_sentinel.py, scripts/fleet_health.py, ecosystem/tool-versions.yaml, docs/intake/archive/2026-07-06-platform-feature-scan.md §6 R3 · serialize-group: settings-json
