---
id: "[#1633]"
title: "The code runs the queue; the integrator only integrates (R130)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1633] [P1][M] **The code runs the queue; the integrator only integrates (R130)** - Code fires `dispatch.py queue` on events (a lane's handback, a merge, a refusal); the integrator only integrates: it watches what has finished, lands each lane on its handback and stacks ready disjoint lanes (R37 cut 3); the dispatcher seat and the integrator's queue duty retire (R130, R128). Today the dispatcher template is live (`templates/dispatcher-order-template.md:31,40-47`) while the integrator is said to own the queue (R128); in BU the dispatcher ended with no successor and the integrator ran `queue` by improvisation (`[#1573]`); in batch E1 the orchestrator fires the queue once by hand and records each launch as a TODAY-GLUE line · owner: E2 lane (the runner and the template change land in one change); the operator ratifies ADR-alpha's text. target batch: E2 · Done when: RED first: (1) a test feeds the runner a handback event, a merge event and a refusal event for a state file and asserts it fires `queue` once per event for the eligible lanes and never for a lane whose receipt reads MERGED; (2) the dispatcher template is retired and the integrator template names no `queue` call, a test pins both; (3) the integrator's context load per landed lane is recorded in the batch close digest (R130: measured); real-use witness: the first batch after E2 is launched, observed and landed with no `queue` typed by a seat, each launch receipt naming the runner as its caller · touches: see the body · kill-candidates: `[#1573]` -- the first-handover step; this row decides who owns the queue and `[#1573]` keeps the handover · refs `[#1573]`, `[#1536]`, `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18.md` · decided-by: R130, R128 (retro-ratification, D8) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0); rewritten by lane e1-rows under R130
