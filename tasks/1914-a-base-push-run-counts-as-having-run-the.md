---
id: "[#1914]"
title: "A base push run counts as having run the suite only if a completed pytest leg shows it (defect 25)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1914] [P1][S] **A base push run counts as having run the suite only if a completed pytest leg shows it (defect 25)** - After [#1888]'s fix on worktree-e30-judge-reused-base (964f81510), `actions_verdict.fetch_run(skip_reused=True)` and the base read of `verdict_for` accept an older push run with no pytest job or an empty job list as a suite-running base, because it lacks the reuse marker; a green tip over that empty base reads PASS (review terra RV-2e6b4f10 MAJOR at scripts/actions_verdict.py:336; judge sol JG-a93c71e5 ACCEPT-WITH-NOTE: valid, serious, file promptly). Defect 25 of the 2026-11-05 cut. · touches: `scripts/actions_verdict.py`, `tests/test_actions_verdict.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/actions_verdict.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - reused newest run, then a jobless (or pytest-less) older run, gives UNATTRIBUTED naming both, not PASS; a run counts as a suite base only with a completed pytest leg (conclusion success or failure); lands after or with [#1888]; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
