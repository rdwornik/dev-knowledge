---
id: "[#1888]"
title: "The landing judge follows a same-sha reused base run to the run that ran the suite (defect 18)"
status: closed
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1888] [P1][S] **The landing judge follows a same-sha reused base run to the run that ran the suite (defect 18)** - `actions_verdict.fetch_run` takes the first `--event push` run for the base sha; when that is main's push run whose pytest leg is `Same-sha verdict reused (no suite run)` (`.github/workflows/conductor.yml:195-197`), the base failure set is empty and every registered known red at the tip reads new, so every `land_lane.py` onto that main refuses REGRESSED by construction (H5-LAND, run 42089244162: 38 new; replayed with base run 42013383491: 1 new). It blocks every landing on main 50cbabf1c, this fix's own included. Defect 18 of the 2026-11-05 cut. · touches: `scripts/actions_verdict.py`, `tests/test_actions_verdict.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/actions_verdict.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a test where the base sha has two push runs, main's with the reuse step executed and an integration-branch run that ran the suite, and the verdict must compare against the latter; then fetch_run (or verdict_for) selects the run whose pytest leg ran; replay of 5e4bc68dd vs 50cbabf1c names only test_g; how the fix itself lands is a morning decision (it cannot be judged by the code it replaces); the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · **CLOSED 2026-11-07** — evidence 5dada2c8656ac2438662ea7a5b8d2624a0baa6b7 · CI run 42194599253 (success) · tests tests/test_actions_verdict.py::test_e30_reused_base_uses_newest_older_suite_run_for_test_attribution
