---
id: "[#482]"
title: "Repair the boundary-headers glob engine — `*` silently crosses `/`, so a glob reads narrower than it behaves"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: pre-commit-config
generates: BACKLOG.md
---

- [#482] [P3][S] **Repair the boundary-headers glob engine — `*` silently crosses `/`, so a glob reads narrower than it behaves** — operator ruling 2026-08-03: **REPAIR (true-glob), not REMOVE.** `fnmatch` has no `**` and its `*` matches `/`, so `.claude/*.md` is ALREADY recursive while `.claude/**/*.md` is a strict subset adding nothing. Measured over 1830 tracked files: fnmatch 1/12/11, true-glob 1/1/12 — **union 13 either way**, so this is INTENT, not coverage. REMOVE rejected: it leaves `.claude/*.md` reading narrower than it behaves — the name-vs-measured-thing defect of [#481]. An engine swap is a **gate change** earning its own contract + terra, which is why `4e2c809b` fixed only the case-sensitivity leg. · Done when: the matcher uses true-glob semantics AND a test pins the governed set, so a later `_GOVERNED_GLOBS` addition whose meaning differs under the new engine FIRES instead of drifting · refs scripts/boundary_headers.py, 4e2c809b, #481, #369 · kill-candidates: none — [#369] owns wiring `--check` into pre-commit, not matcher semantics · serialize-group: pre-commit-config
