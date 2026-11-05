---
id: "[#1875]"
title: "Round-verdict handback follow-ons: one CI read for P5 and P6c, exits 5/6 write a QUESTION, `_PHASE_LABELS` limit"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1875] [P3][S] **Round-verdict handback follow-ons: one CI read for P5 and P6c, exits 5/6 write a QUESTION, `_PHASE_LABELS` limit** - named follow-ons of e30-round-verdict-handback (its SESSION file, lines 89-95) with no open row: Q-E2-1, the duplicate P5 and P6c CI read; exit 5 and exit 6 not wired to `write_question`; the `_PHASE_LABELS` limit. Only closed or unrelated rows mention them (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/conductor.py, tests/test_conductor*.py · kill-candidates: none - [#1857] (the source lane's row) is closed · refs `scripts/conductor.py` · Done when: one CI read serves both P5 and P6c, exits 5 and 6 each write a QUESTION, and the phase-label table covers every phase id (tests) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 4
