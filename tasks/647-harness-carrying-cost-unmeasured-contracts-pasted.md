---
id: "[#647]"
title: "The harness's own carrying cost is unmeasured, and lane contracts are pasted rather than referenced"
status: open
priority: P3
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#647] [P3][M] **The harness's own carrying cost is unmeasured, and lane contracts are pasted rather than referenced** — DECLARE-REVIEWS finding R-5 measured the machinery around a batch at 24 hooks, 56 checks, a 6,813-line audit module and 19 lane contracts totalling 388 KB, all of it to govern merges that take 9 to 28 seconds, beside 75 dispositions and a 1.1 MB corpus the seats are told is read on demand. R-5's organ half is already owned by `[#639]`; this row is the half nobody took — the contract corpus itself. A contract that pastes the common clauses of three predecessors verbatim into every lane brief is the reason the number is what it is, and the fix R-5 names is grammar: contracts by reference · Done when: the lane-contract generator emits shared clauses by reference rather than by paste, the per-batch contract byte total is printed at freeze so the number moves visibly, and the on-demand corpus figure is either reproduced by a script or withdrawn as unmeasurable · refs DECLARE-REVIEWS §B R-5, `scripts/gen_lane_contract.py`, `[#639]` (the organ half), `[#642]` · source: DECLARE-REVIEWS R-5, filed by batch V lane V-4
