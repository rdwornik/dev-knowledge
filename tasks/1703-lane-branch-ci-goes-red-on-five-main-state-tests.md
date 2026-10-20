---
id: "[#1703]"
title: "Every lane branch CI shows five main-state reds that hide real regressions"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1703] [P2][S] **Every lane branch CI shows five main-state reds that hide real regressions** - `tests/test_check_derived_copies.py` x2 (`ecosystem/doc-counts.md` is stale because the lane adds a test file) and `tests/test_onboarding_items.py` x3 (`journal_spine_anchor`: the branch lags main) fail on every lane branch (runs #1114, #1122, #1129, #1137 of the E2 night) and bury a lane's own regressions; input to lane L2 of the test-execution plan (`to-browser/DIGEST-TEST-EXECUTION-EVAL-2026-10-20.md` section 6) · owner: the test-execution L2 lane · Done when: (1) RED first: a test shows a lane branch that adds one test file reads red on `test_check_derived_copies` today; (2) those tests judge the lane's own delta, or are excluded from the lane-branch verdict with a recorded reason; (3) real-use witness: the next lane-branch CI run shows none of the five ids in `known-reds-compare.out` · touches: `tests/test_check_derived_copies.py`, `tests/test_onboarding_items.py` or the known-reds list · kill-candidates: `[#1629]` -- also reads journal_spine_anchor, on main not on lane branches; `[#1566]` -- census classification · refs `[#1560]`, `[#1629]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/DIGEST-TEST-EXECUTION-EVAL-2026-10-20.md` section 6, CI runs #1114 #1122 #1129 #1137
