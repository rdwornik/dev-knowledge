---
id: "[#1889]"
title: "Known-reds registry pin tests are lane-scoped, so a sanctioned registry entry can land (defect 19)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1889] [P1][S] **Known-reds registry pin tests are lane-scoped, so a sanctioned registry entry can land (defect 19)** - `tests/test_known_reds_gate_hooks.py::test_registry_is_origin_main_plus_exactly_the_lines_field` asserts the branch registry equals origin/main apart from `lines` with exactly 12 lines, and four fixture tests pin the audit-health allowlist to the four CGG-1 check names, so any known-reds entry added on a branch reds five tests (carrier run 42111195229) and the A5 registration path cannot land. Defect 19 of the 2026-11-05 cut. · touches: `tests/test_known_reds_gate_hooks.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `tests/test_known_reds_gate_hooks.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - a branch that adds one well-formed members entry keeps the file green; the 12-lines pin applies to the CGG-1 lane's own change only; fixtures read the checks list from the registry they build; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
