---
id: "[#1665]"
title: "`merge_receipt` has no abandon verb for a refused land (defect 5)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1665] [P2][S] **`merge_receipt` has no abandon verb for a refused land (defect 5)** - A refused land leaves its receipt open with no way to mark it abandoned · owner: E2 lane. target batch: E2.1 · Done when: (1) `merge_receipt` gains an `abandon` verb that records the refusal and its reason; (2) RED first: a test refuses a land and fails if the receipt can only be left open; real-use witness: the refused e2-rulings land is abandoned with its REFUSED file cited · touches: `scripts/merge_receipt.py` · kill-candidates: none -- no open row adds the verb · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 5 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
