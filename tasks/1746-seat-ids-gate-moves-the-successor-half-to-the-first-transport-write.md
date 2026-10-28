---
id: "[#1746]"
title: "seat-ids: the successor half of seat_ids_both moves to the successor's first transport write (ADR-132 D3)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1746] [P2][S] **seat-ids: the successor half of seat_ids_both moves to the successor's first transport write (ADR-132 D3)** - the preflight row `seat_ids_both` asks for a successor Tech-Architect id that cannot exist before the cut, and refuses a real cut today; D3 of ADR-132 checks the OUTGOING seat only and has `scripts/transport.py` refuse a `by:` naming a Tech-Architect id that `ecosystem/seat-ids.yaml` has not registered · Done when: `transport.write`/`append` refuse an unregistered Tech-Architect id in `by:` (the registering write that states its own id/session pair excepted), `_row_seat_ids_both` checks the outgoing seat only, and `tests/test_transport_seat_gate.py` plus `tests/test_gen_handoff_preflight_truth.py` pass · touches: `scripts/transport.py`, `scripts/gen_handoff.py`, `tests/test_transport_seat_gate.py`, `tests/test_gen_handoff_preflight_truth.py` · kill-candidates: none -- no open row owns the seat-ids successor gate · refs `ADR-132`, `to-cc/AMEND-2-PLAN-E2-2-SESSION-CLOSE-2026-10-28.md` · source: PROPOSAL-ADR-HANDOFF-2026-10-27 D3 · decided-by: the operator, 2026-10-28, AMEND-2 (id reserved by docs-boot, closed by lane bind-handoff)
