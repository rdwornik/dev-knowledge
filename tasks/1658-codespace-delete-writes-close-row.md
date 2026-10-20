---
id: "[#1658]"
title: "`codespace-delete` writes its close row (R144; true for the verb since 2026-10-19)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1658] [P2][S] **`codespace-delete` writes its close row (R144; true for the verb since 2026-10-19)** - R144 needs compute-hours measured; as of 2026-10-19 the delete verb already writes its close row, so this row is the regression test that pins it · owner: E2 lane. target batch: E2.1 · Done when: (1) a test runs the delete verb against a fake box and fails if no close row lands in `logs/CODESPACE-RECEIPTS.jsonl`; real-use witness: the next real box delete leaves a close row whose deleted-at is the manifest-gated delete time · touches: delete verb in `scripts/dispatch.py`, `tests/` · kill-candidates: none -- no open row pins the close row · refs `logs/CODESPACE-RECEIPTS.jsonl`, `to-browser/RATIFICATION-2026-10-18.md` R144 · decided-by: R144. Defect C10: 4 D0 boxes still hold open rows (`logs/CODESPACE-RECEIPTS.jsonl`: 42 rows, 19 open without close) (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
