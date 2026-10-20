---
id: "[#1679]"
title: "`build_plan` and `build_repair_plan` are two argv builders for one launch (H7)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1679] [P3][S] **`build_plan` and `build_repair_plan` are two argv builders for one launch (H7)** - `scripts/dispatch.py:618` `build_plan` and `:1850` `build_repair_plan` each assemble the claude/codex argv, so a flag added to one (model, effort, permission mode) is silently missing from the other · owner: a dispatch.py lane · Done when: (1) RED first: a test shows a flag present in `build_plan` and absent in `build_repair_plan`; (2) one builder, repair passes its differences; (3) real-use witness: `launch` and `repair` print the same argv shape for the same model · touches: `scripts/dispatch.py` · kill-candidates: `[#1632]` -- same repair path · refs `[#1632]`, `[#1630]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H7 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
