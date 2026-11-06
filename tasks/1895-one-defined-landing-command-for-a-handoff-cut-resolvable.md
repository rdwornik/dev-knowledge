---
id: "[#1895]"
title: "One defined landing command for a handoff cut, resolvable for amended act rows (defects 3, 8, 12)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1895] [P2][M] **One defined landing command for a handoff cut, resolvable for amended act rows (defects 3, 8, 12)** - `--land` lacks the integrator identity, so every cut needs an operator act whose land_lane parameters are re-derived each time (3, 8); `land_lane.py` resolves only a row starting `| H5-LAND |` (land_lane.py:146-149), so an amended act cannot be cited by its own row (12). Defects 3, 8, 12 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `scripts/land_lane.py`, `tests/test_land_lane.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/land_lane.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - one command lands a cut with no per-cut operator parameters; an amended act row resolves; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
