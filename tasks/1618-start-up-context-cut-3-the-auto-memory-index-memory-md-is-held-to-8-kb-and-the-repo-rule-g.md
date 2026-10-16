---
id: "[#1618]"
title: "Start-up context cut 3: the auto-memory index `MEMORY.md` is held to 8 KB and the repo rule `git-discipline.md` to 2 KB"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1618] [P2][S] **Start-up context cut 3: the auto-memory index `MEMORY.md` is held to 8 KB and the repo rule `git-discipline.md` to 2 KB** - `MEMORY.md` is 18,064 B (about 4.7 k tokens) and `.claude/rules/git-discipline.md` 5,694 B (about 1.5 k), both loaded every session; the preflight row `memory_within_cap` reads `[n/a-reason:NO-DECLARED-BUDGET]` · Done when: RED first: (1) `canonical_docs.MEMORY_BYTE_BUDGET` is declared at 8,192 and `memory_within_cap` passes on the live file; (2) a test asserts `.claude/rules/git-discipline.md` <= 2,048 B with the detail moved to PLAYBOOK; (3) witness: the baseline re-measured <= 51,500; fails on a3d0ae31 · touches: `~/.claude/projects/.../memory/MEMORY.md`, `.claude/rules/git-discipline.md`, `scripts/canonical_docs.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1616]`, `[#1617]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
