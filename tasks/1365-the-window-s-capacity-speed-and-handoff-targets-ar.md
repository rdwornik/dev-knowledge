---
id: "[#1365]"
title: "The window's capacity, speed and handoff targets are measured at every merge, not asserted"
status: open
priority: P2
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1365] [P2][L] **The window's capacity, speed and handoff targets are measured at every merge, not asserted** - R62 (operator, 2026-10-03): three focus areas. Capacity: about 12 to 13 lanes at once across local, Codespace and Anthropic cloud, the dispatcher measuring RAM and CPU itself. Speed: handback to `main` takes far less than 37 minutes with test quality not falling. Handoff: a new architect always knows what to read, what to know and how to dispatch. Addenda: cost is recorded as a fact and does not decide; one harness dispatcher with three substrates. · Done when: the batch-close digest records (1) the maximum lanes live at once, by substrate, and the RAM and CPU values the dispatcher measured at admission with their source; (2) minutes from each lane's handback to its merge on `main`, set against the 37-minute baseline; (3) a test-quality figure (mutation score or equivalent) before and after any change made to speed tests, with no fall; (4) the handoff boot test of the R73 row passing; cost appears as a recorded column and is read by no gate · owner: the dispatcher and integrator lanes of B2 W2; the batch-close report (R65 row) carries the figures · touches: the dispatcher's admission record, the batch-close report, tests · kill-candidates: none -- `[#902]` gates lane concurrency on free memory and is one input to the capacity figure, not the measure · refs `[#902]`, `protocols/STANDING_RULINGS.md` section AR (R62) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R62 in `to-browser/RATIFICATION-2026-10-03.md R62`
