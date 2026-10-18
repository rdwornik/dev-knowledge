---
id: "[#1630]"
title: "R101(a) tier refusal runs in pre-launch"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1630] [P1][S] **R101(a) tier refusal runs in pre-launch** - The R101(a) tier refusal runs in pre-launch: a contract whose model/effort tier exceeds its role is refused before it spawns. R101(a) is OWED with no row (`protocols/STANDING_RULINGS.md:6542`); `parse_contract_model_effort` checks shape only and `warn_model_alias` only warns, so six BU lanes all ran Opus (USD 162.27). owner: D1 lane; table from `[M1 row]` (see the model-probe row). target batch: D1 · Done when: RED first: a contract naming a tier above its role's table cell exits 5 from `dispatch.py launch` and `plan`; real-use witness: the next batch's contracts pass through it and a refusal is shown in a launch receipt · touches: see the body · kill-candidates: `[#810]` -- the Codespace runner cannot pass a model; check whether this refusal subsumes it · refs R101, `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18.md` Model and effort · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
