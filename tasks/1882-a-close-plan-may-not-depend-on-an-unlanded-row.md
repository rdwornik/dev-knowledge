---
id: "[#1882]"
title: "A close plan may not depend on an unlanded row: a preflight row refuses it"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1882] [P1][S] **A close plan may not depend on an unlanded row: a preflight row refuses it** - L13 of to-browser/DIGEST-WINDOW-LESSONS-AND-CARRY-TA48-ADDENDUM-1-2026-11-05.md: the session close waited for [#1869]'s mechanism, which put an L-size lane on an unproven engine on the handoff's critical path. Mechanism: the handoff/close path may depend on no open lane; a preflight row refuses a close plan that names an unlanded row as a precondition. · touches: scripts/gen_handoff.py, ecosystem/handoff-preflight-rows.yaml, tests/test_gen_handoff*.py · kill-candidates: none - no open row owns close-plan preconditions · refs `scripts/gen_handoff.py` · Done when: a fixture close plan naming an open row as a precondition is refused by preflight (test) · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: lesson L13
