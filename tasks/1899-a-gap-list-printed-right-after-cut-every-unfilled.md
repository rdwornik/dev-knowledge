---
id: "[#1899]"
title: "A gap list printed right after --cut: every unfilled hand region and every required transport input (defect 5)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1899] [P2][S] **A gap list printed right after --cut: every unfilled hand region and every required transport input (defect 5)** - The cut stops once per gap; the 2026-11-05 boot test also found a file the bundle names that did not exist (gap G8). Defect 5 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - `--cut` prints the full gap list including every named file that does not resolve; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
