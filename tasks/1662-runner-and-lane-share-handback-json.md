---
id: "[#1662]"
title: "The runner and the lane both write `/workspaces/dispatch/handback.json` (SEV-1; defect 1)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1662] [P1][S] **The runner and the lane both write `/workspaces/dispatch/handback.json` (SEV-1; defect 1)** - Both write the same path, so the later write silently overwrites the earlier; interim S5: the lane writes `lane-handback.json` and the orchestrator copies it by hand · owner: E2 lane. target batch: E2.1 · Done when: (1) the runner refuses to start a lane whose handback path it also writes, or relocates its own; (2) RED first: a test with both writers fails today on the overwrite; real-use witness: a real box lane's handback and the runner's both survive in the harvested box · touches: runner and handback writers in `scripts/dispatch.py` · kill-candidates: none -- no open row fixes the shared path · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 1 and S5 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
