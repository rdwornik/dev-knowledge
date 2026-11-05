---
id: "[#1906]"
title: "HANDOFF_BOOT states the backlog mechanics the browser cannot read in scripts/ (boot-test gap G3)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1906] [P2][S] **HANDOFF_BOOT states the backlog mechanics the browser cannot read in scripts/ (boot-test gap G3)** - Id allocation (scripts/id_allocator.py), claim (scripts/claim.py) and close (scripts/row_close.py) were reachable only through repo code (Q5). Gap g3 of the 2026-11-05 cut. · touches: `protocols/HANDOFF_BOOT.md`, `tests/test_handoff_v5_boot.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `protocols/HANDOFF_BOOT.md`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: a fixed paragraph names the three mechanisms and the sanctioned writer; the boot byte cap holds; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
