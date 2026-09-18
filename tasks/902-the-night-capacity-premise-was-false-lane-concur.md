---
id: "[#902]"
title: "The night-capacity premise was false -- lane concurrency must be gated by free memory measured at dispatch, not by the hour"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18"
generates: BACKLOG.md
---

- [#902] [P1][S] **The night-capacity premise was false -- lane concurrency must be gated by free memory measured at dispatch, not by the hour** - Architect declaration 2026-09-18 (`to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W9). Batch AC was sized on "at night the workstation is idle, so more runs locally". **That premise was measured false.** B0 found 20.4 of 27.67 GB held by NON-Claude processes, and the M6 candidate comparison run was killed for critically low memory. The hour of day predicts nothing about headroom. Today nothing gates concurrency on memory at all: `scripts/resource_lifecycle.py`'s admission refusal is disabled (`b03ec766`, [#827]). The per-seat constant stays PROVISIONAL at 646.1 MB, n=1 (`e535ed6a`). `[#827]` owns deriving that constant from a dispatch ledger. This row owns the other half: the dispatch act reads live free memory and admits or refuses on that reading, never on a schedule · Done when: (1) the lane-dispatch path takes a free-memory reading at dispatch time and admits a lane only when that reading covers the per-seat figure plus a named floor; (2) RED-first witness: a fixture box with low free memory refuses a dispatch at any hour, and one with ample memory admits it; (3) no dispatch or batch-sizing surface carries an hour-of-day or "night" capacity assumption, checked by a named test · implements: DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18 · refs `scripts/resource_lifecycle.py`, `[#827]`, `[#792]`; transport: `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W9 · source: architect declaration 2026-09-18 · kill-candidates: `[#827]` -- if its admission leg is re-enabled with a live dispatch-time reading, this row folds into it
