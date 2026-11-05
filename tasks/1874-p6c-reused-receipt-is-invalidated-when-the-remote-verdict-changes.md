---
id: "[#1874]"
title: "A reused P6c receipt is invalidated when the remote CI verdict for the same sha changes"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1874] [P2][S] **A reused P6c receipt is invalidated when the remote CI verdict for the same sha changes** - SESSION-e30-conductor-phase-order.md:42: a P6c receipt for the same sha whose remote verdict later changed is "not invalidated in code"; `scripts/conductor.py:1013-1024` checks only `sha != HEAD` (T2-STALE). [#1848] is open with a different scope (C-VENDOR at P4) (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/conductor.py, tests/test_conductor*.py · kill-candidates: none - [#1848] covers C-VENDOR at P4, not P6c reuse · refs `scripts/conductor.py` · Done when: a P6c receipt whose recorded verdict differs from the current remote verdict of the same sha is not reused (test) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 3
