---
id: "[#1648]"
title: "plan_lint: a code lane needs an integrator"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1648] [P1][S] **plan_lint: a code lane needs an integrator** - A batch whose lanes include code and that names no integrator seat leaves its lanes with nobody to land them (R130: the integrator lands each lane on its handback). `scripts/plan_lint.py` reads lane contracts only, not a batch order · owner: E2 lane, with or after `[#1623]` which gives `plan_lint` its batch-order reader. target batch: E2 · Done when: RED first: `plan_lint check` on a fixture batch order with a lane of kind code and no integrator order named exits non-zero naming the batch, and the same order naming its integrator passes; real-use witness: the next batch with a code lane is rendered through the lint and its output is quoted in the batch's launch record · touches: see the body · kill-candidates: `[#1623]` -- the same lint family (a batch-order reader in `plan_lint`): decide whether one reader serves both rows · refs `[#1623]`, `templates/integrator-order-template.md` · decided-by: R130, R128 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
