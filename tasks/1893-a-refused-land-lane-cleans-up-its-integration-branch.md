---
id: "[#1893]"
title: "A refused land_lane cleans up its integration branch or the retry replaces it (defect 17)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1893] [P1][S] **A refused land_lane cleans up its integration branch or the retry replaces it (defect 17)** - A refused `land_lane.py` leaves `worktree-integrate-<batch>` on origin holding the unlanded sha; every retry is a non-fast-forward until a reserved deletion (H5-LAND 2026-11-05: 5e4bc68dd). Defect 17 of the 2026-11-05 cut. · touches: `scripts/land_lane.py`, `scripts/merge_path.py`, `tests/test_land_lane.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/land_lane.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - after a RED refusal the integration branch is deleted (the scratch receipt kept as the record) or a retry with the same slug replaces it by lease; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
