---
id: "[#1607]"
title: "A `uv.lock` change (create, update, delete a dependency) is gated by a process"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1607] [P2][M] **A `uv.lock` change (create, update, delete a dependency) is gated by a process** - EMPTY CELL: only the implicit `--locked` failure on a stale lock; no audit, no `dependabot.yml`; `.github/` holds three workflows · Done when: RED first: a test over a fixture lock change asserts a named gate fires (lock fresh, no unpinned, `uv` pin untouched, ADR-106) and refuses a hand-edited lock; fails on a3d0ae31 · touches: `.pre-commit-config.yaml`, a gate script, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1606]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
