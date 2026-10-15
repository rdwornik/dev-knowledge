---
id: "[#1612]"
title: "A job in state done or blocked with a handback on the transport is stopped automatically"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1612] [P1][M] **A job in state done or blocked with a handback on the transport is stopped automatically** - memory-diag harness row #10 (`to-browser/DIGEST-MEMORY-DIAG-2026-10-03.md`): finished sessions stay resident and hold RAM until a seat stops them by hand; `[#1010]` (closed) only requires a HANDBACK line to end a lane session · Done when: RED first: a test over a fake job list asserts a done/blocked job whose handback file exists is returned by `seat_registry.py stoppable` and one with no handback is not; fails on a3d0ae31 · touches: `scripts/seat_registry.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#918]`, `[#970]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
