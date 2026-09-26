---
id: "[#1048]"
title: "AJ C-2: per-lane process efficiency (VSM work over cycle time) is not computed by lane_cost.py"
status: open
priority: P3
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1048] [P3][M] **AJ C-2: per-lane process efficiency (VSM work over cycle time) is not computed by lane_cost.py** - Architekt Jutra candidate (DIGEST-AJ-DELTA-2026-09-25 C-2): value-stream-mapping work-time over cycle-time, derived from a lane's contract-freeze, first-commit and merge timestamps -- `scripts/lane_cost.py` computes token/dollar cost today, not this ratio. · Done when: `scripts/lane_cost.py` (or a sibling) computes work/cycle from those three timestamps for at least one landed lane, RED-first witnessed · refs `scripts/lane_cost.py`, `docs/audits/2026-09-21-technical-aj-all-front.md` · kill-candidates: none -- no open row computes this ratio
