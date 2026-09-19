---
id: "[#919]"
title: "The token cap is POLLED, not enforced -- a stop-loss, not a limit: witness A overshot 5.5x before the first poll acted"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-SPINE-AND-B3-2026-09-19"
generates: BACKLOG.md
---

- [#919] [P2][M] **The token cap is POLLED, not enforced -- a stop-loss, not a limit: witness A overshot 5.5x before the first poll acted** - `[#908]` is ADVANCED, NOT CLOSED by the L3 merge (`b55dc909`): `scripts/dispatch.py govern` binds a `--bg` lane by session id and stops it past the cap, but it observes spend after the fact. Live witnesses, re-read by the integrator from the transcripts with `lane_cost.seat_usage`: witness A, cap 5,000 -> STOPPED at **27,670** (haiku, 2 calls, 27,178 of it cache-write) before the first poll could act -- 5.5x over; the pre-fix witness `4c128d01`, cap 5,000 -> stopped at 57,081 fresh, **113,381** including cache reads. A lane spends whatever it can between polls, and a single large first call overruns any small cap. And the lane that BUILT the cap (`b1fc54db`, sonnet, 137 calls) ran **585,943** fresh tokens against 200k ordered -- the cap it built would not have stopped that, because no launcher read an order. Stream-metered lanes (codex, `claude -p`, codespace) are now REFUSED by the shim rather than capped (handback section 2). The row's question: can the cap be enforced at LAUNCH rather than observed after the fact, and if the stream is metered rather than capped, what is the smallest thing that refuses before spend? · Done when: a witness launch with a cap smaller than its first call is REFUSED or stopped at or under the cap (ORDERED vs RAN recorded, overshoot = 0 or bounded by a stated, measured per-call ceiling); or the operator rules the poll's overshoot acceptable with a stated bound, and `[#908]`'s done-when is re-worded to that bound · implements: DECLARE-SPINE-AND-B3-2026-09-19 · refs filed by the wave-3 close operator order 2026-09-19, `[#908]` (advanced, not closed), `scripts/dispatch.py`, `templates/dispatch-shim.ps1`, `docs/audits/2026-09-19-technical-wave3-dispatch-split.md` sections 2-3, JOURNAL 2026-09-19 (an)
