---
id: "[#1383]"
title: "The Linux pytest leg runs in at most 420 s on two consecutive push runs, carried from B2-W1 W1-3's unmet Done item 4"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1383] [P2][M] **The Linux pytest leg runs in at most 420 s on two consecutive push runs, carried from B2-W1 W1-3's unmet Done item 4** - Lane b2-ci-poll removed the 300 s idle from `tests/test_connection_loop.py`, but its Done item 4 (Linux pytest step at most 420 s on both runs) stayed UNMET: 384 s and 551 s, while main's own Linux step is 537-642 s. The leg is bound by the suite's throughput, not by that file. The architect ruled (2026-10-05, OPERATOR-ACTION 8): not waived, not re-baselined (N1); W1-3 merges with item 4 UNMET, carried by B2-W2 lane W2-13 (shards) as this row · Done when: (1) two consecutive push runs of `main` show the `pytest (ubuntu-latest)` step at most 420 s by job step time; (2) the change is sharding or worker count (R72), with no test skipped, deselected or moved and no threshold changed; (3) W2-13's contract cites this row · owner: B2-W2 lane W2-13 `b2-ci-shards-coverage` · kill-candidates: none -- no open row carries the Linux leg's wall time · refs `[#1372]`, `[#889]`, `tests/test_connection_loop.py` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (W1-3 FATE; DECIDED-BY-SEAT 1)
