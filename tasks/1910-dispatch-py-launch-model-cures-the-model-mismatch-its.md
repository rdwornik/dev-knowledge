---
id: "[#1910]"
title: "dispatch.py launch: --model cures the model mismatch its own refusal names (defect 21)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1910] [P2][S] **dispatch.py launch: --model cures the model mismatch its own refusal names (defect 21)** - A contract whose Model table says `sonnet` and whose Dispatch line says `claude-sonnet-5-5` is refused with 'pass --model to say which', but the block-vs-table comparison runs before the override (`scripts/dispatch.py:835-842`), so passing `--model claude-sonnet-5-5` is refused identically (witnessed launching LANE-e30-handoff-landing-ci, 2026-11-05 night); the only cure is editing the published contract. Defect 21 of the 2026-11-05 cut. · touches: `scripts/dispatch.py`, `tests/test_dispatch_launch.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/dispatch.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - with --model (or --effort) given, the block-vs-table check is skipped for that field and the given value is used; without it the refusal stands; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
