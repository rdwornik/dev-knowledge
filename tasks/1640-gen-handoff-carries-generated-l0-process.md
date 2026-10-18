---
id: "[#1640]"
title: "gen_handoff carries generated L0, process index, staleness preflight"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1640] [P1][M] **gen_handoff carries generated L0, process index, staleness preflight** - gen_handoff carries the generated L0, the 14-row process index and a staleness preflight. Plan r4 rule 4: the handoff carries L0 + index generated from the bindings, and `gen_handoff` FAILs when the picture is older than the code it binds; until the model exists it carries the AS-IS L0 with holes marked. A hand-drawn L0 in the handoff is forbidden. owner: D1 lane; handoff mechanics are the operator's lane. target batch: D1 · Done when: RED first: a cut with a stale binding hash FAILs the preflight; the cut inlines the block (<= 4 KB); real-use witness: the next cut's seat answers the seat exam from the block · touches: see the body · kill-candidates: none -- no row carries the L0 in the handoff · refs `protocols/STANDING_RULINGS.md`, `to-cc/AMEND-1-DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`, the AS-IS model row · decided-by: R129 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
