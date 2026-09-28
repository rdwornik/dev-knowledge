---
id: "[#1124]"
title: "Handoff part B: BD-seats compares seat identity and liveness, not the status string"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1124] [P2][S] **Handoff part B: BD-seats compares seat identity and liveness, not the status string** - R26 (to-browser/RATIFICATION-2026-09-28.md v5) item 3: `BD-seats` (LIVE-DRIFTS) compares the cut-time `seat_health_line` to a live re-derivation by exact string, so it fails whenever any session changes state between cut and verify, the cut session included — a known false negative of part A, waived for the 2026-09-28 cut with `claude agents --json` as evidence · Done when: the rule compares seat identity and liveness (a seat named at cut is still resolvable; no seat wedged that the cut did not name) and a test shows a state change alone no longer FAILs it · refs scripts/verify_handoff_probes.py, scripts/handoff_state.py, scripts/seat_registry.py · kill-candidates: none -- no open row tracks BD-seats
