---
id: "[#1680]"
title: "The learning distiller is built but its run output is absent: nothing runs it and no contract reads it (H18)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1680] [P2][M] **The learning distiller is built but its run output is absent: nothing runs it and no contract reads it (H18)** - `scripts/learning_distiller.py` exists with tests, yet no scheduled run, hook or contract generator calls it and there is no distilled-rows output to read; [#1669] covers only the missing refusal INPUT, and clause 2 (a contract built from a REFUSED file quotes its lines) is not done because `scripts/gen_lane_contract.py` was out of the pilot's footprint (`to-browser/SESSION-e2-distill-pilot.md` Open) · owner: a learning-loop lane · Done when: (1) a wiring surface runs the distiller and writes its output to one named path; (2) `gen_lane_contract.py` reads it; (3) real-use witness: the next contract built after a REFUSED file quotes that file's lines · touches: `scripts/learning_distiller.py`, `scripts/gen_lane_contract.py` · kill-candidates: `[#1669]` -- clause 2 is this row's second half; sequence the two · refs `[#1669]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H18 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
