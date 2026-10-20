---
id: "[#1688]"
title: "`run_phase` hard-wires `stdin=DEVNULL`, so R147's 'prompt on stdin' verify is impossible (P4)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1688] [P2][S] **`run_phase` hard-wires `stdin=DEVNULL`, so R147's 'prompt on stdin' verify is impossible (P4)** - R147 requires the isolated verifier to get its prompt on stdin, but `run_phase` opens the child with `stdin=DEVNULL`, so the prompt had to go as an argument (and a `--allowedTools Read "prompt"` argv swallowed it once) · owner: a run_phase lane · Done when: (1) RED first: a phase with a stdin prompt receives it; (2) `run_phase` pipes the prompt on stdin when the phase declares it; (3) real-use witness: the R147 verify runs from `run_phase` · touches: `scripts/run_phase.py` · kill-candidates: `[#1653]` -- same file · refs `[#1653]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 4 (P4) in `to-browser/SESSION-e2-distill-pilot.md`
