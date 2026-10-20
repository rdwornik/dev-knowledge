---
id: "[#1704]"
title: "The merge receipt reads 'FAILED step(s): suite' on a green run after a crashed first land call"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1704] [P2][S] **The merge receipt reads 'FAILED step(s): suite' on a green run after a crashed first land call** - for e2-rows-map the first land call pushed `10d21de97` then crashed at `merge_receipt.record_push` ('no open receipt for e2-rows-map at <primary>\\logs\\.merge-receipt-e2-rows-map.json', the receipt was opened in the integration worktree); the re-run closed the receipt with 'FAILED step(s): suite' and 'UNRECORDED required step(s): handback, merge, teardown' although the run succeeded, because the crashed call recorded no ci leg (`to-browser/SESSION-integrator-e2-0-2026-10-18.md:801-811`); the same 'FAILED step(s): suite' also appears on a PRE-EXISTING suite (:340) · owner: an integrator-tooling lane (`scripts/merge_receipt.py`) · Done when: (1) RED first: a test opens a receipt, crashes the first land call before the ci leg, re-runs, and expects the suite step to read from the re-run's CI verdict, not FAILED; (2) the receipt keeps one ci leg per push and a crashed call is recorded as a crash, not as a failed suite; (3) real-use witness: the next landing that needs a second land call closes with no 'FAILED step(s): suite' · touches: `scripts/merge_receipt.py`, `tests/test_merge_receipt.py` · kill-candidates: `[#1698]` -- same script, a different defect (the line lags a landing); sequence the two · refs `[#1698]`, `[#1665]`, `[#957]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-integrator-e2-0-2026-10-18.md:801-811` (LAND e2-rows-map, RECEIPT e2-rows-map)
