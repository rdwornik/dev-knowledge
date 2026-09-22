---
id: "[#953]"
title: "Events that file rows -- some escalation events should produce a task row automatically, not just a STATUS entry"
status: open
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#953] [P3][M] **Events that file rows -- some escalation events should produce a task row automatically, not just a STATUS entry** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` E6 "Deferred to wave 5". Value: E4 of ADR-87's 2026-09-22 amendment names four events that write state for the browser to read; a subset of these (a repeated refusal, a recorded finding that recurs) are themselves backlog-worthy today and require a human to notice the STATUS entry and file the row by hand. · Done when: at least one escalation event (named at pickup) files a task row automatically, with the filed row citing the event's own receipt as its evidence, and a human review confirms the auto-filed row is not noise. · refs `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` (E6), `docs/decisions/ADR-87-equilibrium-contract.md` (2026-09-22 amendment, E4) · kill-candidates: none -- no open row files rows from events
