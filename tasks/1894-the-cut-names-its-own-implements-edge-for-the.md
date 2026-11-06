---
id: "[#1894]"
title: "The cut names its own implements edge for the bundle files (defect 15)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1894] [P2][S] **The cut names its own implements edge for the bundle files (defect 15)** - graph-task-coverage refuses generated bundle files that no OPEN row claims; the 2026-11-05 landing needed `[#1834]`'s touches clause extended by hand with 17 paths (graph leg 1 matches files only, scripts/file_purpose_graph.py:968-972). Defect 15 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `scripts/file_purpose_graph.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a cut's bundle files are covered by an implements edge the cut itself writes (a row clause or a file naming the row); the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
