---
id: "[#1911]"
title: "gen_handoff --trial-cut honours the cut's non-blocking preflight rows (defect 22)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1911] [P2][S] **gen_handoff --trial-cut honours the cut's non-blocking preflight rows (defect 22)** - `--trial-cut` (and `--preflight-only`) exit 1 on any FAIL (`scripts/gen_handoff.py:4963-4965`), including the rows the real cut excludes from its raise as `PREFLIGHT_NON_BLOCKING_ROWS` (landed_vs_ratified, operator_decisions_list); landed_vs_ratified FAILs on every landed R-id since R0 that no RATIFICATION file names, so the batch-close trial stage refuses the close by construction (phase 4 of the 2026-11-05 night). Defect 22 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a trial cut whose only FAIL is a non-blocking row exits 0 and still prints the row; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
