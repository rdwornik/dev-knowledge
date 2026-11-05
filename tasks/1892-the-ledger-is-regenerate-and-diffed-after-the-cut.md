---
id: "[#1892]"
title: "The LEDGER is regenerate-and-diffed after the cut's own JOURNAL anchor commit (defect 13)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1892] [P1][S] **The LEDGER is regenerate-and-diffed after the cut's own JOURNAL anchor commit (defect 13)** - ledger_refreshed is stale by construction after the cut: the JOURNAL anchor commit changes the LEDGER's newest-entry line and the only remedy the row names is `--cut`, barred after hand fills (DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-1). Defect 13 of the 2026-11-05 cut. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - a handoff-repair row from the night census makes no open row redundant · refs `scripts/gen_handoff.py`, `[#1834]`, to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6 · Done when: RED first - after an anchor commit the row's remedy is a regenerate step that reuses the cut's own call (`_fresh_ledger_text` + `_write_if_different` + `transport.emit`), not `--cut`; the lane-branch CI run is green outside known reds · decided-by: night mission act A2 (to-cc/PLAN-NIGHT-HANDOFF-SELF-REPAIR-2026-11-05.md phase 3), filed by the night orchestrator; ranking per AMEND-1 A4 · source: to-browser/DIGEST-NIGHT-HANDOFF-SELF-REPAIR-2026-11-06.md, to-browser/CLOSE-REPORT-E3.0-2026-11-05-FINAL.md section 6
