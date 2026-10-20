---
id: "[#1676]"
title: "Human-head work happens outside the phase chain (P6): the `origin/` slug fix, the F1 delegation and the review fix leave no receipt"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1676] [P2][M] **Human-head work happens outside the phase chain (P6): the `origin/` slug fix, the F1 delegation and the review fix leave no receipt** - e2-distill-pilot ran `run_phase.py` for its phases but three pieces of work were done by the head outside any phase: the `origin/` slug fix, the F1 delegation and the review-major fix, each small and tested but absent from the chain's receipts (`to-browser/SESSION-e2-distill-pilot.md` DEFECT 6) · owner: a conductor lane · Done when: (1) the chain gains a phase kind or receipt line for head work with who, what and the commit; (2) RED first: a lane with head work and no line is refused at handback; (3) real-use witness: the next code lane's handback lists its head work from the receipts · touches: `scripts/conductor.py`, `scripts/run_phase.py` · kill-candidates: `[#1600]` -- the chain table · refs `[#1600]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: P6 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
