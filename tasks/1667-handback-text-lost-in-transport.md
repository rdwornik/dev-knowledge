---
id: "[#1667]"
title: "Handback text is lost in transport: the handback becomes a checked file, not a rendered one (defect 7)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1667] [P1][S] **Handback text is lost in transport: the handback becomes a checked file, not a rendered one (defect 7)** - The twelve drafted rows reached the transport as empty bullets and nothing refused the empty block · owner: E2 lane. target batch: E2.1 · Done when: (1) the handback is a file the lane writes and lints (`scripts/transport_lint.py check`) and a fenced block of empty lines is refused; (2) RED first: a test feeds a handback with an empty `ROWS` block and fails today; real-use witness: the next lane handback carries its full rows and the integrator reads them from the file · touches: `scripts/transport_lint.py`, the lane handback template · kill-candidates: none -- `[#1647]` lints prompts, not handback content · refs `protocols/STANDING_RULINGS.md`, `to-browser/REFUSED-e2-rulings.md` item 3, `to-browser/LEDGER-dev-knowledge.md` v238 defect 7 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
