---
id: "[#1916]"
title: "land_lane has no resume path for an already-pushed integration commit and its CI run"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1916] [P1][S] **land_lane has no resume path for an already-pushed integration commit and its CI run** - `scripts/land_lane.py` always fetches, refuses a dirty tree, checks out origin/main detached and re-merges (`land_lane.py:281-305`), so a run killed after push-integration (CI-LAND 2026-11-06: Claude Code's memory reaper killed the poll; integration merge 4dc39481e, CI run 42201596616 green) cannot be completed: the partial receipt, the integration worktree and the remote integration branch must be deleted by an operator act and the whole land re-run, costing a second ~30 min CI run. Item 8 of to-browser/RATIFICATION-2026-11-06.md. · touches: `scripts/land_lane.py`, `scripts/merge_path.py`, `tests/test_land_lane.py` · kill-candidates: none - no open row owns resuming a landing · refs `scripts/land_lane.py`, `[#1893]`, to-browser/DIGEST-MORNING-LANDINGS-2026-11-06.md · Done when: RED first - a test where the integration branch already holds the judged merge of the same lane ref and a completed CI run exists, and land_lane resumes at poll/land without re-merging, while a mismatched integration sha still refuses; then land_lane implements it; the lane-branch CI run is green outside known reds · decided-by: operator, to-browser/RATIFICATION-2026-11-06.md Item 8 · source: to-browser/DIGEST-MORNING-LANDINGS-2026-11-06.md (CI-LAND)
