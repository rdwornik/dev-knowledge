---
id: "[#1626]"
title: "B-vs-C spike on P1 dispatch: state machine vs BPMN engine"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1626] [P2][S] **B-vs-C spike on P1 dispatch: state machine vs BPMN engine** - The B-vs-C spike grades P1 dispatch as a state machine and as a BPMN engine before ADR-beta is ruled. D0.5: `python-statemachine` / `transitions` (B) vs SpiffWorkflow (C) on P1, dry-run against `dispatch.py` verbs; graded on gateways bound, readability, error paths, zone colouring, fit with Conductor E (R105), dependency cost and licence. owner: spike lane (codespace scratch branch, never merged); operator rules ADR-beta. target batch: D0 · Done when: `scratch/b-vs-c-spike/RESULT.md` on the scratch branch holds a grading table with a measured value or UNVERIFIED in every cell and ONE recommendation; real-use witness: `PROPOSAL-ADR-PROCESS-MODEL` cites those cells · touches: see the body · kill-candidates: none -- the process-model form is undecided · refs `to-cc/DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`, `[#669]` · decided-by: R131 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
