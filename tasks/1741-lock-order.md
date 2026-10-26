---
id: "[#1741]"
title: "stop_check state before receipt lock"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1741] [P3][S] **stop_check state before receipt lock** - `seat_cycle.stop_check` records CROSSED in the state file before it takes the receipt lock, so a lock timeout with no later Stop leaves the receipt without the line (state has it, receipt does not) -- in `scripts/seat_cycle.py` `stop_check` (`seat_state.update_counters(... crossed_line=line)` runs before `with seat_state.locked(receipt)`, `LOCK_TIMEOUT_S = 2.0`) a receipt-lock failure leaves the line in the STATE file's `crossed` list but absent from the receipt; a later Stop that is still over threshold retries the append, but if no further Stop fires the receipt stays without the line while the state file carries it; terra's "lost record" claim was NOT-REPRODUCED as stated and this is its residual, not a defect of the ruled design · owner: integrator-e2-1 (`scripts/seat_cycle.py`, `scripts/seat_state.py`) · Done when: (1) RED first: a test holds the receipt lock past `LOCK_TIMEOUT_S`, calls `stop_check` once with no second call, and fails today because the state file's `crossed` list has the line and the receipt does not; (2) the fix is one of two, named in the module docstring: the receipt step runs before `update_counters`, or `seat_cycle.py check` appends any `crossed` line missing from the receipt at the next wake; the same test then passes with the lock released before that wake; (3) `uv run --locked pytest -n0 tests/test_seat_cycle.py` passes · touches: `scripts/seat_cycle.py`, `scripts/seat_state.py`, `tests/test_seat_cycle.py` · refs `[#1636]`, `[#1700]` · decided-by: the operator, 2026-10-26, RATIFICATION-2026-10-26.md ruling B ("the terra residual") · source: `to-browser/SESSION-sh1x-landed-review.md:19-21` · filed by the integrator from the operator grant 1737-1743 (RATIFICATION-2026-10-26.md ruling B + D-ID; S-ID: no id beyond it)
