---
id: "[#1610]"
title: "'Superseded means code removed' (ADR-125) is enforced when an ADR is superseded or a feature deleted"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1610] [P2][M] **'Superseded means code removed' (ADR-125) is enforced when an ADR is superseded or a feature deleted** - EMPTY CELL: delete for ADRs and feature code; `operator-asks-register:36` counts 7 Proposed-stale and 84 Accepted with no evidence · Done when: RED first: a test asserts a superseded ADR names the removing commit or row and fails on a fixture ADR that does not; `[#1561]` and `[#1568]` own the test half; fails on a3d0ae31 · touches: `scripts/decision_coverage.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1561]`, `[#1568]`, `[#864]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
