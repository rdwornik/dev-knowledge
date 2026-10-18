---
id: "[#1649]"
title: "plan_lint: a row birth needs a ratifying act"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1649] [P1][S] **plan_lint: a row birth needs a ratifying act** - ADR-111 section 4 makes a row's birth auditable only if its `decided-by` names a ratifying act, and no organ checks it: eighteen rows were born on 2026-10-18 without one. A batch order or lane contract that files a row must name the ratifying act, a landed ruling in `protocols/STANDING_RULINGS.md`, an Accepted ADR or an ACCEPTED intake. owner: E2 lane, with or after `[#1623]`. target batch: E2 · Done when: RED first: `plan_lint check` on a fixture order that files a row with no `decided-by`, or with one naming an R-id absent from `protocols/STANDING_RULINGS.md`, exits non-zero naming the row, and the same order citing a landed R-id passes; real-use witness: the next batch order that files rows passes only with a `decided-by` on each, and a seeded violation is refused in the lint output · touches: see the body · kill-candidates: `[#1623]` -- the same lint family (a batch-order reader in `plan_lint`): decide whether one reader serves both rows · refs `docs/decisions/ADR-111-finding-triage-pipeline.md`, `[#1623]` · decided-by: ADR-111 section 4 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
