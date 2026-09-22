---
id: "[#942]"
title: "State as data -- the STATUS surface, the state query, and the four escalation events"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#942] [P2][M] **State as data -- the STATUS surface, the state query, and the four escalation events** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b" and `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` E4. Value: the browser seat is summoned by an event, never a heartbeat (ADR-87's 2026-09-22 amendment) -- today that only holds if a human reads the STATUS file at the right moment. Formalizing the four escalation events (batch closed, a lane refused or a merge hard-fail, a lane filed a question, a wait exceeded its limit) as one queryable surface closes the gap between "the data exists" and "the seat is actually reached". · Done when: the STATUS file's "now" section is written by each of the four events in one shared shape; one state-query organ reads it and answers "does the architect need to look" without a log read; a live batch exercises at least two of the four events and the query reflects both. · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` (E4), `docs/decisions/ADR-87-equilibrium-contract.md` (2026-09-22 amendment) · kill-candidates: none -- no open row covers the state-query organ
