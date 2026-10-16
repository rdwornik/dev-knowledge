---
id: "[#1608]"
title: "A CI workflow change (create, update, delete) is gated before it lands"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1608] [P2][M] **A CI workflow change (create, update, delete) is gated before it lands** - EMPTY CELL: nothing fires when `.github/workflows/*.yml` changes (process matrix, `docs/audits/2026-10-16-technical-process-matrix.md`) · Done when: RED first: a test asserts a gate refuses a workflow with a job that has no declared `harness.yaml` stage or a removed required check; fails on a3d0ae31 · touches: `.pre-commit-config.yaml`, a gate script, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1422]`, `[#1606]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
