---
id: "[#1668]"
title: "The laptop slept 02:00-15:00: 13 h of no progress (the off-the-laptop goal, defect 8)"
status: open
priority: P2
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1668] [P2][L] **The laptop slept 02:00-15:00: 13 h of no progress (the off-the-laptop goal, defect 8)** - The orchestrator and queue run on the laptop, so a sleeping laptop stops the batch; the goal is that a batch advances with the laptop shut · owner: E2 lane. target batch: E2.2 · Done when: (1) the batch loop runs where it does not sleep (E2.2 queue runner in a box or CI) and records its own heartbeat; (2) RED first: a test fails a heartbeat gap longer than the stated bound; real-use witness: a batch advances across a night with the laptop asleep and the heartbeat log shows no gap above the bound · touches: queue runner (E2.2), heartbeat record · kill-candidates: none -- `[#1633]` is the queue runner this depends on · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 8 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
