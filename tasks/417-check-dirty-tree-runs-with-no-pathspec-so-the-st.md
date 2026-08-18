---
id: "[#417]"
title: "`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#417] [P3][S] **`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work** — `git status --porcelain` was called bare, so it counted the tool-owned untracked `ecosystem/*/history/*.md` dailies that ADR-84 writer isolation deliberately keeps off main. The gate therefore trips in an ordinary clean session; a gate that fires daily on nothing trains bypass ([#355] precedent). **The pathspec half LANDED 2026-08-16** — `check_dirty_tree` now filters through `_is_lane_owned_daily`, tested both directions; the EXTRACTION remains. · Done when: the `history_specs`/`pathspecs` scope list at `_commit_routine_outputs` (`scripts/audit.py:4751-4760`) is extracted into a location shared with `check_dirty_tree`'s exclusion scope, narrowed to what the dirty-tree gate wants (not the wider `docs/audits/`-spanning branch-commit-helper scope), or `protocols/STANDING_RULINGS.md` carries a section naming `[#417]` and stating why the extraction was rejected · refs scripts/session_end_backpressure.py, scripts/audit.py, ADR-84, ADR-85, #355, #405, #418 · kill-candidates: none — no open task owns the dirty-tree pathspec · serialize-group: settings-json · source: docs/audits/2026-08-16-verification-nb6-backlog-truth.md §1.8, which carries the landed filter, its tests and `4bef950`
