---
id: "[#1437]"
title: "Batch close generates and requires a disposition for every decision of its batch"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1437] [P1][M] **Batch close generates and requires a disposition for every decision of its batch** - B2-W1's integrator ruled a disposition for each of twelve decisions (seat ruling 3, 2026-10-05) and none reached `decision_coverage.DECISION_DISPOSITIONS`, so P13 refused them at the next handoff cut. `scripts/decision_carriage.py` (landed with this row) derives a decision's carriage from evidence and renders the register entries; R90 (b) makes batch close generate them and refuse until every decision of the batch is disposed · Done when: `decision_carriage.py` grows `propose --batch <ID>`: it enumerates the batch's decision files, gathers evidence, renders register entries for decisions whose every lane is carried and an `implements:` proposal for a partly executed one; batch close refuses until every in-era decision of the batch has a register entry, an OPEN implementing row or a written refusal; the ESTABLISHED entries land in the close commit and the rest go to the seat as one list; tests over a fixture batch · owner: the batch-close moment's owner · touches: `scripts/decision_carriage.py`, `scripts/decision_coverage.py`, the batch-close moment, tests · kill-candidates: `[#1385]` -- it reads an AMEND as carried when all its lanes merged, which this generator proposes and the seat rules · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/decision_carriage.py, scripts/decision_coverage.py
