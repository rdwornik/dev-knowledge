---
id: "[#1884]"
title: "An engine is admitted for critical work only after one non-critical lane passed end to end on it"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1884] [P2][S] **An engine is admitted for critical work only after one non-critical lane passed end to end on it** - L16 of to-browser/DIGEST-WINDOW-LESSONS-AND-CARRY-TA48-ADDENDUM-1-2026-11-05.md: [#1869] was the first lane run end to end on the conductor engine and was put on the critical path; P1 halted on a deterministic defect ([#1879]). Mechanism: an engine admission record; `dispatch.py` refuses a critical lane on an engine with no recorded non-critical end-to-end pass. · touches: scripts/dispatch.py, ecosystem/harness.yaml, tests/test_dispatch*.py · kill-candidates: none - no open row gates engine admission · refs `scripts/dispatch.py` · Done when: a critical lane on an engine with no recorded end-to-end pass is refused at launch (test) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: lesson L16
