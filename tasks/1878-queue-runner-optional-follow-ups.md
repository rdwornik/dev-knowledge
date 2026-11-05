---
id: "[#1878]"
title: "Queue-runner optional follow-ups: validate in record(), the dispatch repair codespace finding, and the same-vendor judge note"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1878] [P3][S] **Queue-runner optional follow-ups: validate in record(), the dispatch repair codespace finding, and the same-vendor judge note** - e30-queue-runner (its SESSION file, lines 107 and 141) left optional follow-ups with no row: validate in `record()` (terra's note); the `dispatch.py repair` codespace finding; the judge ran as an isolated same-vendor session because of the sol quota (VENDOR-FAIL). [#1633] and [#1572] are open for other scope (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/queue_runner.py, scripts/dispatch.py, tests/test_queue_runner*.py · kill-candidates: none - [#1633] and [#1572] cover other queue-runner scope · refs `scripts/queue_runner.py` · Done when: `record()` refuses an invalid record (test); the repair finding is fixed or REJECTED with a reason · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 7
