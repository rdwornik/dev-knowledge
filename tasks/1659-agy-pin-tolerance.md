---
id: "[#1659]"
title: "agy pin tolerance: 1.3.5 -> 1.4.2 must not block a launch (R140)"
status: closed
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1659] [P3][S] **agy pin tolerance: 1.3.5 -> 1.4.2 must not block a launch (R140)** - The agy pin moved 1.3.5 -> 1.4.2 and the pins gate blocked a launch; a bump of a laptop-only agy should be tolerated or written by the verb · owner: E2 lane. target batch: E2.1 · Done when: (1) the pins gate tolerates a patch or minor bump of agy, or the launch verb writes the pin commit; (2) RED first: a test with pin 1.3.5 and installed 1.4.2 fails today; real-use witness: the next agy bump on the laptop launches with no hand edit · touches: the pins gate in `scripts/` · kill-candidates: `[#1664]` -- the same gate for the claude CLI; one fix may close both · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 3 · decided-by: R140 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19) · **CLOSED 2026-10-21** — subsumed by [#1671] (operator GO 2026-10-21, LEDGER v271)
