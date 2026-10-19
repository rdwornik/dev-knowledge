---
id: "[#1669]"
title: "The distiller reads none of an R130 integrator's refusals (defect 9)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1669] [P2][S] **The distiller reads none of an R130 integrator's refusals (defect 9)** - The lane distiller reads the lane's own handback but not the integrator's REFUSED file, so a repair lane starts without the refusal text · owner: E2 lane. target batch: E2.1 · Done when: (1) the distiller takes the REFUSED file as an input when a repair is launched; (2) RED first: a test builds a repair contract from a REFUSED file and fails today because its quoted lines are absent; real-use witness: the next repair launch's contract quotes the refusal verbatim · touches: `scripts/gen_lane_contract.py` · kill-candidates: `[#1631]` -- same distiller; sequence the two · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 9 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
