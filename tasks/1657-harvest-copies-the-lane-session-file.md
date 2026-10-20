---
id: "[#1657]"
title: "Harvest copies the lane SESSION file back (R145 hand step)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1657] [P2][S] **Harvest copies the lane SESSION file back (R145 hand step)** - A Codespace lane writes its `to-browser/SESSION-<lane>.md` inside the box and the orchestrator copies it by hand (TODAY-GLUE) · owner: E2 lane. target batch: E2.1 · Done when: (1) `codespace-harvest` copies the lane's SESSION file into the laptop's `to-browser/` and records its sha; (2) RED first: a test harvests a fake box and fails if the SESSION file is absent after; real-use witness: the next box lane's SESSION file appears with no hand copy · touches: harvest path in `scripts/dispatch.py` · kill-candidates: none -- no open row widens the harvest · refs `protocols/STANDING_RULINGS.md`, `to-browser/RATIFICATION-2026-10-18.md` R145 · decided-by: R145. Defect C2: a codespace harvest reports `ok: true` with an empty manifest (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
