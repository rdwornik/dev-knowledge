---
id: "[#1661]"
title: "A Codespace handback fires a Monitor WAKE (R145 hand step; defect 4)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1661] [P2][S] **A Codespace handback fires a Monitor WAKE (R145 hand step; defect 4)** - A box lane's handback fires no Monitor WAKE, so the orchestrator polls or waits by hand (LEDGER v238 defect 4) · owner: E2 lane. target batch: E2.1 · Done when: (1) the harvest path writes an event a Monitor until-loop can wait on when `lane-handback.json` lands; (2) RED first: a test fails if the handback lands and no wake file is written; real-use witness: a real box lane's handback wakes the orchestrator with no poll · touches: harvest path in `scripts/dispatch.py` · kill-candidates: none -- `[#972]` cleans up wakes, it does not fire one · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 4 · decided-by: R145 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
