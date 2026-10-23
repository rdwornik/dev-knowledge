---
id: "[#1625]"
title: "AS-IS process model: binding file, generated diagrams, 14-row index"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1625] [P1][M] **AS-IS process model: binding file, generated diagrams, 14-row index** - The AS-IS process model exists as a machine-readable binding file with generated colour diagrams and a 14-row index. D0.1: L0 plus L1 of P1 dispatch, P11 integration/land and P13 seat lifecycle, one row per node (type, actor today, `file:line` + verified anchor, target zone BROWSER/HARNESS/BOTH, TODAY-GLUE flag), diagrams RENDERED from it, never hand-drawn; handoff-ready block <= 4 KB. owner: Tech-Architect seat proposes, CC lane D0.1 builds, operator ratifies the file's repo home. target batch: D0 · Done when: `to-browser/DIGEST-PROCESS-ASIS-2026-10-18.md` and its ANNEX hold the binding file; the mechanical check shows every `file:line` anchor exact or marked HOLE; the diagrams regenerate byte-identically from the binding file; real-use witness: the next handoff cut inlines the L0 + index block and the seat exam (D0.6) is answered from it · touches: `ecosystem/process-binding.yaml`, `scripts/gen_process_diagrams.py`, `tests/test_process_diagrams.py`, `tests/test_process_anchor_binding.py`, `tests/test_process_gate.py`, `tests/test_process_gate_inputs.py` (P1 landed by lane connector-land; P11 and P13 not yet modelled) · kill-candidates: none -- no row covers the process model · refs `protocols/STANDING_RULINGS.md`, `to-cc/DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`, `to-cc/AMEND-1-DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`, `to-cc/PLAN-HARNESS-2026-10-18.md` · decided-by: R131, R129 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
