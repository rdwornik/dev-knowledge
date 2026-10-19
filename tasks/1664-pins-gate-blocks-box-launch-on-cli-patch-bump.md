---
id: "[#1664]"
title: "The pins gate blocks every box launch on each laptop CLI patch bump (defect 3)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1664] [P2][S] **The pins gate blocks every box launch on each laptop CLI patch bump (defect 3)** - Each laptop CLI patch bump (claude 2.1.302 -> 2.1.303) blocks every box launch until a hand pin edit · owner: E2 lane. target batch: E2.1 · Done when: (1) the launch verb writes the pin commit or tolerates a patch bump; (2) RED first: a test with pin 2.1.302 and installed 2.1.303 fails today; real-use witness: the next real claude patch bump on the laptop launches a box lane with no hand edit · touches: the pins gate and launch verb in `scripts/` · kill-candidates: `[#1659]` -- the same gate for agy; one fix may close both · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 3 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
