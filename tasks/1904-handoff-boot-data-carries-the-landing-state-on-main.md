---
id: "[#1904]"
title: "HANDOFF_BOOT data carries the landing state: on main, or carried on a branch at a sha (boot-test gap G1)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1904] [P2][S] **HANDOFF_BOOT data carries the landing state: on main, or carried on a branch at a sha (boot-test gap G1)** - Neither boot-test reader could state the git state the window starts from or whether the bundle landed (2026-11-05 bundle, Q14). Gap g1 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `protocols/HANDOFF_BOOT.md` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a probe-checked BOOT-DATA row names main's sha and the bundle's landing state; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
