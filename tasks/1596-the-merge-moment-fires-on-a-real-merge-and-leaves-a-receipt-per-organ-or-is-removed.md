---
id: "[#1596]"
title: "The `merge` moment fires on a real merge and leaves a receipt per organ, or is removed"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1596] [P1][M] **The `merge` moment fires on a real merge and leaves a receipt per organ, or is removed** - DEAD: `lane-integrate.md:179` calls it, yet the 51 `logs/MERGE-RECEIPTS.jsonl` rows since 2026-10-01 show no `assemble` step; 'BW did not run the moments' (`operator-asks-register:46`) · Done when: RED first: a test replays the newest `MERGE-RECEIPTS.jsonl` row through the moment declaration in `ecosystem/harness.yaml` and fails while any declared merge organ has no receipt step; passes when the next merge shows each step, or the moment is removed from `harness.yaml` by a ruling; fails on a3d0ae31 · touches: `ecosystem/harness.yaml`, `scripts/merge_receipt.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1444]`, `[#1569]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
