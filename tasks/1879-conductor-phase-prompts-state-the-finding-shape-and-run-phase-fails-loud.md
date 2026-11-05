---
id: "[#1879]"
title: "Conductor phase prompts state the Finding shape, and run_phase records why a payload was not harvested"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1879] [P1][S] **Conductor phase prompts state the Finding shape, and run_phase records why a payload was not harvested** - [#1869]'s first conductor run halted twice at r1 P1 (2026-11-05 01:13Z, 01:30Z): the producer wrote `findings` as strings, `ecosystem/schema/phase_receipt.py` Finding is an object {id, severity, claim, evidence} with extra=forbid, and `scripts/run_phase.py::fresh_payload` (:85-97) swallows the validation error, so the receipt reads FAILED "exited 0 with no fresh valid payload" with no reason. The phase prompts in `ecosystem/harness.yaml:186-188` never state the Finding shape (Q-N5-1, to-browser/QUESTION-E30-SEAT-LIFECYCLE-P1-HALT-2026-11-05.md; L16 of to-browser/DIGEST-WINDOW-LESSONS-AND-CARRY-TA48-ADDENDUM-1-2026-11-05.md). · touches: ecosystem/harness.yaml, scripts/run_phase.py, scripts/gen_lane_contract.py, tests/test_run_phase*.py · kill-candidates: none - no open row owns the phase prompt text or the harvest diagnostics · refs `scripts/run_phase.py` · Done when: a payload with string findings is refused with the validation error recorded in the phase receipt (test), and every phase prompt names the Finding fields (test) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N8 section 6 row candidate 1; carried Q-N5-1 (DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2)
