---
id: "[#1903]"
title: "The hand-written Operator decisions section has one home inside the manifest fill surface (defect 11)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1903] [P3][S] **The hand-written Operator decisions section has one home inside the manifest fill surface (defect 11)** - Its only generated heading is in CUT_DRAFTS.md, outside `_BD_MANIFEST_FILL_SURFACE` (gen_handoff.py:1081), so a filled section cannot be restamped and the bundle carries two such headings. Defect 11 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - one Operator decisions heading, inside the fill surface; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
