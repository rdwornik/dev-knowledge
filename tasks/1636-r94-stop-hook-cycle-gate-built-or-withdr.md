---
id: "[#1636]"
title: "R94 Stop-hook cycle gate built or withdrawn"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1636] [P2][S] **R94 Stop-hook cycle gate built or withdrawn** - The R94 Stop-hook cycle gate is built or withdrawn. R94 (`RATIFICATION-2026-10-10`) is ratified and unbuilt: the integrator cycles by a clock it reads itself (3 h vs the dispatcher's 2 h, rules disagree) and one cycle killed a live 95-minute pytest · owner: D1 lane; withdraw needs the operator. target batch: D1 · Done when: either a Stop hook refuses to end a seat past its cycle bound without a handover record (RED first), or the ruling is withdrawn by an operator line; real-use witness: the next cycle shows the hook's receipt · touches: see the body · kill-candidates: none -- R94 has no row · refs `protocols/STANDING_RULINGS.md`, R94, `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18-ANNEX.md` L8 · decided-by: R94, R136 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0) · The seat-cycle mechanism the Stop-hook trigger would call (e2-seat-cycle, R136/R179: check, handover, successor, bound, verified stop; the trigger itself still unbuilt) is pinned by `scripts/seat_cycle.py`, `ecosystem/seat-cycle.yaml`, `templates/seat-handover-template.md`, `tests/test_seat_cycle.py`, `tests/test_seat_cycle_bound.py`, `tests/test_handoff_verify_retired.py`.
