---
id: "[#1639]"
title: "Two-way completeness gate: node to code, entry point to node"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1639] [P1][M] **Two-way completeness gate: node to code, entry point to node** - The two-way completeness gate: every P1/P11/P13 node binds to `file:line` + test, and every dispatch or launch entry point maps to a node. Gate form depends on ADR-beta. An unmapped entry point is a leftover to delete or model · owner: D1 lane after ADR-beta. target batch: D1 · Done when: the gate fails on a node with no binding and on an entry point with no node (both RED first); real-use witness: it runs in CI on the next batch · touches: see the body · kill-candidates: none -- no gate checks the model against the code · refs `protocols/STANDING_RULINGS.md`, `to-cc/DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md` Recommended path 3, the AS-IS model row · decided-by: R131, R129 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
