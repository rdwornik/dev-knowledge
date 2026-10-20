---
id: "[#1689]"
title: "`conductor.py lane` runs the harness `phases:` table, which disagrees with the lane contract's own phases (P5)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1689] [P2][M] **`conductor.py lane` runs the harness `phases:` table, which disagrees with the lane contract's own phases (P5)** - `conductor.py lane --lane L --round N` ran P1 opus, P3 copilot, P5, P6a codex, P6b grok, P7 opus, not the contract's P1 RED / P2 / P3, so the pilot used `run_phase.py` directly and the conductor never carried a lane end to end · owner: a conductor lane · Done when: (1) the conductor reads the phases from the lane contract; (2) RED first: a contract with three phases yields three; (3) real-use witness: one lane runs end to end under `conductor.py lane` · touches: `scripts/conductor.py` · kill-candidates: `[#1600]` -- conductor dogfood · refs `[#1600]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 5 (P5) in `to-browser/SESSION-e2-distill-pilot.md`
