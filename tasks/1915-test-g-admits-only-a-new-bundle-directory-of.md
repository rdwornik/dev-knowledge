---
id: "[#1915]"
title: "test_g admits only a new bundle directory of the full date-repo-mode shape (defect 26, the L-ci judge's follow-up)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1915] [P3][S] **test_g admits only a new bundle directory of the full date-repo-mode shape (defect 26, the L-ci judge's follow-up)** - After [#1886]'s fix on worktree-e30-handoff-landing-ci (a07081e20), test_g lets a branch add files under one new `docs/handoffs/<YYYY-MM-DD>...` directory but accepts any text after the date, so a misnamed bundle directory passes (judge follow-up, receipt to-browser/SESSION-e30-handoff-landing-ci.md). Defect 26 of the 2026-11-05 cut. · touches: `tests/test_handoff_v5_boot.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `tests/test_handoff_v5_boot.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a new directory not matching `<YYYY-MM-DD>-<repo>-<mode>` (mode in gen_handoff's --mode choices) fails test_g; a well-formed one passes; lands after or with [#1886]; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
