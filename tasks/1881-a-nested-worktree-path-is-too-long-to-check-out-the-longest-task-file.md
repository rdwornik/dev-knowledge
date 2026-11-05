---
id: "[#1881]"
title: "A nested seat worktree path is too long for Windows to check out the longest task file"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1881] [P2][S] **A nested seat worktree path is too long for Windows to check out the longest task file** - at N1 (2026-11-04 night) the integrator could not switch branches in the nested worktree `.claude/worktrees/integrator-e3-0-cycle-4/.claude/worktrees/integrator-e3-0-cycle-5`: Windows refused `tasks/1857-conductor-p5-is-a-model-session-...md` with 'Filename too long' (SESSION-integrator-E3.0-2026-10-31.md, N1 entry). Fix: a test bounds the longest tracked path plus the deepest admitted worktree prefix under the Windows limit, or the filing path caps the task-file slug; ADR-140's I1 anchor removes nesting, and this row pins the limit. · touches: scripts/validate_hermetization.py, tests/test_task_path_length*.py · kill-candidates: none - ADR-140 removes nesting but no row pins the path limit · refs `scripts/validate_hermetization.py` · Done when: a test fails when the longest tracked path plus the admitted worktree prefix exceeds the Windows limit · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N8 section 6 row candidate 3
