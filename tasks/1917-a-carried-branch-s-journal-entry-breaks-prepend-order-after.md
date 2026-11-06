---
id: "[#1917]"
title: "A carried branch's JOURNAL entry breaks prepend order once newer entries land on main first"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1917] [P1][S] **A carried branch's JOURNAL entry breaks prepend order once newer entries land on main first** - A JOURNAL entry written on a carrier branch (worktree-handoff-2026-11-05's 2026-11-05 (c)) lands after other entries reached main (2026-11-06 (a)/(b)); after origin/main is merged into the carrier, the carried entry sits below main's, and commit-gate's `validate_prepend_order` refuses (`not-prepended`, H5-LAND CI run 42213181451) although git merged cleanly. Nothing before CI tests the merged JOURNAL against main. Item 8 of to-browser/RATIFICATION-2026-11-06.md. · touches: `scripts/land_lane.py`, `scripts/validate_prepend_order.py`, `tests/test_land_lane.py` · kill-candidates: none - no open row owns a pre-push prepend check of a carried branch · refs `scripts/validate_prepend_order.py`, `[#786]`, to-browser/DIGEST-MORNING-LANDINGS-2026-11-06.md · Done when: RED first - a carried branch whose JOURNAL entry would sit below main's after the integration merge is refused by land_lane before push-integration (naming the entry and the fix: move it above main's entries), while a correctly prepended one passes; the lane-branch CI run is green outside known reds · decided-by: operator, to-browser/RATIFICATION-2026-11-06.md Item 8 · source: to-browser/DIGEST-MORNING-LANDINGS-2026-11-06.md (H5-LAND)
