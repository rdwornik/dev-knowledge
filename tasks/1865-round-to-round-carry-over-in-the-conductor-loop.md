---
id: "[#1865]"
title: "Round-to-round carry-over in the conductor loop (the row reserved as [#1865] and never filed)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1865] [P2][M] **Round-to-round carry-over in the conductor loop (the row reserved as [#1865] and never filed)** - the e30-round-loop lane (SESSION-e30-round-loop.md:60) handed this off as "filed by the dispatcher as row [#1865], NOT built here", but only the reservation `refs/reservations/task-id/1865` was ever created (N0 board reconcile, to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). A later round of `scripts/conductor.py lane --run` does not carry the earlier round's findings and accepted state forward as its input. Fix: the round N+1 input names round N's verdict, findings and head sha, and a test pins that a round-2 producer sees round-1's findings. · touches: scripts/conductor.py, tests/test_conductor*.py · kill-candidates: none - no open row owns round carry-over · refs `scripts/conductor.py` · Done when: a two-round fixture lane shows round 2's phase inputs naming round 1's verdict and findings (test) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 1
