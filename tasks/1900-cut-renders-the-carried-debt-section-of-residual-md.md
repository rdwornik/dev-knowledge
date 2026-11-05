---
id: "[#1900]"
title: "--cut renders the Carried debt section of RESIDUAL.md (defect 6)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1900] [P3][S] **--cut renders the Carried debt section of RESIDUAL.md (defect 6)** - The section was computed by hand at the 2026-11-05 cut from gen_handoff.carriage_verdicts (carried since PLAN-NEXT-2026-10-28 item 2). Defect 6 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - the section is rendered by the cut in the 10-28 shape; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
