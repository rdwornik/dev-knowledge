---
id: "[#1841]"
title: "Wire scripts/startup_probe.py to a real caller or remove it under R56 before 2026-11-09"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1841] [P2][S] **Wire scripts/startup_probe.py to a real caller or remove it under R56 before 2026-11-09** - `scripts/startup_probe.py` has no caller of any class: its only record is the `ecosystem/harness.yaml` fates row `manual_until: 2026-11-09`, and `ORPHAN_DISPOSITIONS` carries `NO-CALLER: manual_until 2026-11-09 [#1841]` (operator ruling D, 2026-11-01: a manual_until row is not a caller) · Done when: before 2026-11-09 the script is wired to a real caller (a template, a `.claude/commands` command, a workflow or a protocol step) or removed under R56, and its disposition row goes with it · touches: `scripts/startup_probe.py`, `scripts/graph_queries.py` · kill-candidates: [#1800] · refs [#1800], [#1711] · source: operator ruling D on lane e30-commit-gate, 2026-11-01 · decided-by: the operator, 2026-11-01
