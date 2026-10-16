---
id: "[#1611]"
title: "Create and delete under `protocols/` are gated like any other doc"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1611] [P3][S] **Create and delete under `protocols/` are gated like any other doc** - EMPTY CELL: protocols create and delete; handoff/boot delete (process matrix, `docs/audits/2026-10-16-technical-process-matrix.md`) · Done when: RED first: a test asserts adding or deleting a `protocols/*.md` without its index and freshness updates is refused; fails on a3d0ae31 · touches: `.pre-commit-config.yaml`, a gate script, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1593]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
