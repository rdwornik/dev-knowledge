---
id: "[#1845]"
title: "seat_registry: an integrator seat holds a SET of batch binds; refuse_no_live_integrator checks membership"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1845] [P1][M] **seat_registry: an integrator seat holds a SET of batch binds; refuse_no_live_integrator checks membership** - `scripts/seat_registry.py` `seats()` does `binds[session] = row`, so a second `bind --role integrator --batch E3.1` REPLACES the first and the one integrator stops being live for E3.0: the 21:4x `REFUSED [no-live-integrator]` for E3.0 after the integrator's E3.1/E3.2 binds (DEFECT 33) · Done when: only successive `--role integrator` binds of one session accumulate into `Seat.batches` (lowest batch id first, compared numerically: E3.2 before E3.10), a bind to any other role replaces the role and clears every prior integrator batch, `unbind --batch B` removes one batch while bare `unbind` keeps today's meaning, `Seat.batch` stays the first of `batches`, `Seat.binds` carries one `BatchBind(batch, priority, landing)` per batch (priority = the batch id's `(major, minor)`, landing = `arrival`; metadata only, no refusal or landing decision reads it), `refuse_no_live_integrator` and `seat_health_line` check membership in `batches`, `show` prints every batch with priority and `landing=arrival`, and a legacy one-batch row set reads exactly as before; tests in `tests/test_seat_registry.py`, `tests/test_seat_refusals.py` and the committed fixture `tests/fixtures/seat_registry/legacy-registry.jsonl` · owner: the integrator · touches: `scripts/seat_registry.py`, `scripts/seat_refusals.py`, `tests/test_seat_registry.py`, `tests/test_seat_refusals.py`, `tests/fixtures/seat_registry/legacy-registry.jsonl` · kill-candidates: none -- no open row covers the integrator's multi-batch bind · source: `LANE-e30-seat-registry-binds.md` (GO-E3.0 C1), evidence `to-browser/DIGEST-RULING-PIN-COMMIT-AND-DEFECT-33-2026-11-01.md` Ruling 2, `to-browser/SESSION-dispatcher-E3.0-2026-10-31.md` (DEFECT 33), `scripts/seat_registry.py:383-385` · refs scripts/seat_registry.py, scripts/seat_refusals.py, tests/test_seat_registry.py, tests/test_seat_refusals.py
