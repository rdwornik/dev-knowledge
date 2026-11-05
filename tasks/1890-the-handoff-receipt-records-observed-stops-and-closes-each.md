---
id: "[#1890]"
title: "The handoff receipt records observed stops and closes each wait (defect 20)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1890] [P1][S] **The handoff receipt records observed stops and closes each wait (defect 20)** - `HANDOFF_RECEIPT.json` `stops:` and `waits:` are written at the cut from ADR-132 D4's design: both the 2026-10-28 and 2026-11-05 receipts list exactly steps 5, 12, 13 with `end: null`, while the 2026-11-05 cut stopped 8 times; ADR-132's response measure and flip-condition are blind (PROPOSAL-ADR-HANDOFF-FLIP-2026-11-06 F1). Defect 20 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a refusal of the cut or its landing appends an observed stop (step, actor, reason, time) and an operator input closes the open wait; active time is computable from the receipt; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
