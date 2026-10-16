---
id: "[#1554]"
title: "A new ask that duplicates an open row is refused at distill, naming the row, before an id is allocated"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1554] [P2][M] **A new ask that duplicates an open row is refused at distill, naming the row, before an id is allocated** - UC9 (a duplicate is stopped at the front). `[#1535]` (5)(6) refuses a plan that duplicates an existing ORGAN; nothing refuses an ask that duplicates an open ROW, and duplicates are caught by review today (REVIEW-SEAT-CHECKLIST-2026-10-10:215, "A new row would duplicate [#615]."). Tier T2 (R117): the similarity method is a technology choice · Done when: RED first: (1) distill compares an incoming ask with every OPEN `tasks/` row through a deterministic similarity oracle chosen library-first in the row's CHALLENGE (no model call inside the oracle) and refuses a seeded duplicate, naming the `[#id]`, before an id is allocated; (2) a seeded near-miss that is not a duplicate passes; (3) a false positive is overridden only by a NEW-JUSTIFIED line recorded in the DistillReceipt; (4) the oracle's precision and recall on a labelled set of past rows (including the `[#615]` case) are recorded · starts after: `[#1535]` merged · touches: `scripts/gen_lane_contract.py`, `ecosystem/schema/`, tests · kill-candidates: none -- `[#190]` is intra-file code duplication, not row duplication · refs `[#1535]`, `[#617]`, `[#190]`, `docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md` · source: `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md` §1 UC9; `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md`
