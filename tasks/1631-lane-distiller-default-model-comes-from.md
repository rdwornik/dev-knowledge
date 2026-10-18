---
id: "[#1631]"
title: "Lane distiller default model comes from a role table"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1631] [P2][S] **Lane distiller default model comes from a role table** - The lane distiller takes its default model from a role table, not the hard-coded DEFAULT_MODEL opus. `scripts/gen_lane_contract.py:200` `DEFAULT_MODEL = "opus"`; `emit --model` accepts only the bare aliases that `plan_lint` then refuses, and `--shape codespace` emits a win-tooling `Dispatch-Codespace` line. owner: D1 lane. target batch: D1 · Done when: RED first: `emit --kind code` with no `--model` yields an explicit versioned id from the role table and passes `plan_lint check`; a codespace-shaped contract carries a `dispatch.py codespace-exec` line; real-use witness: the next batch's contracts are emitted with no hand edit of the Model cell · touches: see the body · kill-candidates: none -- no row covers the distiller default · refs `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18.md`, the model-probe row · decided-by: R134, R114 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
