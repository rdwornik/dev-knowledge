---
id: "[#1913]"
title: "conductor tier1's 15-minute ceiling fits the selection a change to a widely imported script draws (defect 24)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1913] [P2][S] **conductor tier1's 15-minute ceiling fits the selection a change to a widely imported script draws (defect 24)** - The `tier1` job (`.github/workflows/conductor.yml:528-542`, `timeout-minutes: 15`) selects the import closure of the changed scripts; a change to scripts/verify_handoff_probes.py selects 109 test files and is cancelled at about 61% (runs 42136490526, 42140618428, lane e30-handoff-landing-ci, 2026-11-06), while a sibling lane's tier1 (run 42138417748) finished with 48 s of headroom; so any lane touching that module is red by construction on a job outside its scope. Defect 24 of the 2026-11-05 cut. · touches: `.github/workflows/conductor.yml`, `scripts/ci_os_plan.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `.github/workflows/conductor.yml`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: the tier1 budget is derived from the selection's measured duration (or the selection is sharded) so the lane e30-handoff-landing-ci tip passes tier1; a test pins that the ceiling covers the largest current selection; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
