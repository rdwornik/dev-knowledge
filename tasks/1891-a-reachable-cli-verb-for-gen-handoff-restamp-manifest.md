---
id: "[#1891]"
title: "A reachable CLI verb for gen_handoff.restamp_manifest (defect 7)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1891] [P1][S] **A reachable CLI verb for gen_handoff.restamp_manifest (defect 7)** - No CLI verb reaches `gen_handoff.restamp_manifest` since ADR-132 folded `--restamp-manifest` into `--cut`; the 2026-11-05 cut called it by hand. Defect 7 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - `gen_handoff.py --restamp <bundle>` runs restamp_manifest with its existing gate and receipt; the runbook names it; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
