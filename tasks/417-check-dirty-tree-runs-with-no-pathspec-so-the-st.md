---
id: "[#417]"
title: "`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#417] [P3][S] **`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work** — `scripts/session_end_backpressure.py:340-349` calls a bare `git status --porcelain`, so it counts the tool-owned untracked `ecosystem/*/history/*.md` dailies that ADR-84 writer isolation deliberately keeps off main. The gate therefore trips in an ordinary clean session; a gate that fires daily on nothing trains bypass ([#355] precedent). Note for the build: a reusable scope list already exists at `scripts/audit.py:2625-2633`, but it is a LOCAL variable inside the branch-commit helper (needs extraction before it can be shared) AND it spans `docs/audits/` too — wider than this gate wants. Filing only, zero build. · Done when: the dirty-tree leg ignores tool-owned writer-isolated paths with a test, or the exclusion is recorded rejected with a reason · refs scripts/session_end_backpressure.py, scripts/audit.py, ADR-84, ADR-85, #355, #405, #418 · kill-candidates: none — no open task owns the dirty-tree pathspec · serialize-group: settings-json
