---
id: "[#1628]"
title: "M1: measured model and effort table per role"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1628] [P1][M] **M1: measured model and effort table per role** - A measured model and effort table per role replaces the unenforced R101 tiering. D0.4 (M1): four task types x {Haiku 5.5 at its highest accepted effort, Haiku 5.5 default, Sonnet 5.5 default} plus Copilot on the RED-test task, blind graded; USD, tokens and wall time per cell. owner: M1 lane (codespace scratch branch, never merged); operator rules the table. target batch: D0 · Done when: `scratch/m1-model-probe/RESULT.md` holds one row per cell with the served model id, USD, tokens, wall time and a blind grade, and a PROPOSED role -> model + effort table; real-use witness: `gen_lane_contract.py` / the role table of the D1 distiller row reads its values · touches: see the body · kill-candidates: none -- R101 tiering was never coded and no measurement exists · refs R101, `[#1536]`, `to-cc/PLAN-HARNESS-2026-10-18.md` · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
