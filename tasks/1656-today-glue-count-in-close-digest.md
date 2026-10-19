---
id: "[#1656]"
title: "TODAY-GLUE count in every close digest (R145)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1656] [P2][S] **TODAY-GLUE count in every close digest (R145)** - R145: the hand steps the harness still leaves to a human (TODAY-GLUE) are counted at every batch close so they can be driven to zero · owner: E2 lane. target batch: E2.1 · Done when: (1) the close-digest generator prints the TODAY-GLUE count and names each step; (2) RED first: a test fails a close digest with no TODAY-GLUE line; real-use witness: the E2.0 close digest carries the count and lists the hand copies this batch needed · touches: the close-digest generator, the `to-cc/` batch template · kill-candidates: none -- no open row counts hand steps · refs `protocols/STANDING_RULINGS.md`, `to-browser/RATIFICATION-2026-10-18.md` R145 · decided-by: R145 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
