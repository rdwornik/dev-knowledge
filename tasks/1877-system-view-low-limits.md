---
id: "[#1877]"
title: "System view LOW limits: live refresh adds new nodes, a truncated receipt is not UNREADABLE-only, empty receipt files are not OK"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1877] [P3][S] **System view LOW limits: live refresh adds new nodes, a truncated receipt is not UNREADABLE-only, empty receipt files are not OK** - e31-system-view documents three LOW limitations only in code: live refresh updates existing nodes only; a truncated JSON receipt shows UNREADABLE; empty MERGE-RECEIPTS / QUOTA-READS files show OK. No row carries them; [#1748] is the broader view (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/system_map.py, tests/test_system_map*.py · kill-candidates: none - [#1748] is the broader view and does not name these three · refs `scripts/system_map.py` · Done when: live refresh adds a new node, and an empty receipt file reads as EMPTY not OK (tests) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 6
