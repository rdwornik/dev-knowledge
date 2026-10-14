---
id: "[#1533]"
title: "The system-map refresh is not a closed loop -- it leaves an unmerged branch and a worktree behind"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1533] [P2][S] **The system-map refresh is not a closed loop -- it leaves an unmerged branch and a worktree behind** - the `/map` refresh (`scripts/system_map.py`, `.claude/commands/map.md`) wrote its record `ecosystem/system-map-record.json` for map_sha 88f1bc52 on branch `worktree-system-map-2026-10-14` (c2953534, 2026-10-14) in worktree `.claude/worktrees/system-map-2026-10-14` and stopped; nothing merged, landed or tore it down, so it sat unmerged while main moved. BATCH-GREEN-MAIN-PILOT-2026-10-14 Part C landed it by hand and recorded this GAP; the refresh has no lifecycle owner (the nearest rows, [#1337] and [#1421], own the integrator's and the seat cycle's teardown, not the map refresh) · Done when: a /map refresh either lands its record through `merge_path.py land` and tears down its worktree and branch (no_leftovers verify passes), or writes nothing outside the gitignored scratch -- a test proves a refresh leaves no worktree-* branch and no worktree behind · refs `scripts/system_map.py`, `.claude/commands/map.md`, `ecosystem/system-map-record.json`, `docs/intake/2026-10-15-tech-map-refresh-closed-loop.md` · kill-candidates: none -- no open row owns the map refresh's lifecycle (grep over tasks/ on 2026-10-15) · source: `docs/intake/2026-10-15-tech-map-refresh-closed-loop.md`; BATCH-GREEN-MAIN-PILOT-2026-10-14 Part C
