---
id: "[#1733]"
title: "A lane cannot register its own row in the task manifest, so its branch CI is red by construction"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1733] [P1][S] **A lane cannot register its own row in the task manifest, so its branch CI is red by construction** - an H1-X lane files its row through `scripts/id_allocator.py`, but `tasks/manifest.json` gains a node only by hand, and `scripts/gen_task_tree.py` has no add verb and refuses an unregistered row; the contract keeps the manifest out of the lane footprint, so every row-filing lane hands back a branch whose CI fails `task_tree_coherence` plus the tier1 task-tree tests until the integrator inserts the node at landing (P1 `land-lane-receipt-anchor` branch CI 40122512305: commit-gate + 12 tier1 REGRESSIONs, all from the missing [#1721] node; P4 `no-leftovers-claims` branch CI 40112196751 task-coverage; P4 isolated verify item 5b FAIL for the same reason) · owner: `scripts/gen_task_tree.py` · Done when: (1) RED first: a test fails while a task file with a valid `story:` and no manifest node cannot be registered by any `gen_task_tree.py` verb; (2) `gen_task_tree.py` gains an add verb that inserts the node after the last task node of the file's own frontmatter story, is idempotent, and refuses an unknown story or a file whose `id` does not match its name; (3) `scripts/gen_lane_contract.py`'s row-filing text names the verb, so a lane registers its own row inside its footprint; (4) real-use witness: the next row-filing lane's branch CI is green on `task_tree_coherence` and the task-tree tier1 tests with no integrator manifest edit · touches: `scripts/gen_task_tree.py`, `tests/test_gen_task_tree.py`, `scripts/gen_lane_contract.py`, `tests/test_gen_lane_contract.py` · kill-candidates: none removed -- `[#1721]` and the P4 row are its first victims, not duplicates · refs `[#1721]`, RATIFICATION-2026-10-24 H1-X · decided-by: the operator, 2026-10-24, OPERATOR GO G4 relayed by Tech-Architect-47 (H1-X) · source: `to-browser/SESSION-land-lane-receipt-anchor.md` (DECIDED-BY-LANE: "gen_task_tree.py, which has no add verb and REFUSES an unregistered row"), `to-browser/SESSION-no-leftovers-claims.md`
