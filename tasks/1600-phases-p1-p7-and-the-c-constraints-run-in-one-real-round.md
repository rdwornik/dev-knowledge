---
id: "[#1600]"
title: "Phases P1-P7 and the C-* constraints run in one real round"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1600] [P1][M] **Phases P1-P7 and the C-* constraints run in one real round** - DECLARED-ONLY: no live round has run; `run_phase.py` is dated 2026-11-15 and the `phase-gate` job reads 'NOT GATED (1): #689 build' · Done when: RED first: a test asserts at least one `PhaseReceipt` per phase P1..P7 exists under `logs/` for one real lane and fails on a3d0ae31; the row closes with that round's receipts · touches: `scripts/conductor.py`, `ecosystem/harness.yaml`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1535]`, `[#689]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md`. Defect N11: `run_phase` carried the dogfood lane but the conductor did not (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
