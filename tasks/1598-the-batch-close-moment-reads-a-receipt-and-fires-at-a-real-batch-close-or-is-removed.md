---
id: "[#1598]"
title: "The `batch-close` moment reads a receipt and fires at a real batch close, or is removed"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1598] [P2][S] **The `batch-close` moment reads a receipt and fires at a real batch close, or is removed** - DECLARED-ONLY: only prose at `templates/integrator-order-template.md:131`; `[#1028]` records that its digest organ reads no receipt · Done when: RED first: a test asserts the batch-close digest organ reads `logs/MERGE-RECEIPTS.jsonl` for the batch and fails on a3d0ae31; the row closes with a real close or the moment removed · touches: `ecosystem/harness.yaml`, digest organ, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1028]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md`. Defect H33: `ci_red_age` is not named in the batch-close checklist (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
