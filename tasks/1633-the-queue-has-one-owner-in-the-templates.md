---
id: "[#1633]"
title: "The queue has one owner in the templates (ADR-alpha)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1633] [P1][S] **The queue has one owner in the templates (ADR-alpha)** - The queue has exactly one owner in the templates, per ADR-alpha. The dispatcher template is live (`templates/dispatcher-order-template.md:31,40-47`) while the integrator is said to own the queue (R128); in BU the dispatcher ended with no successor and the integrator ran `queue` by improvisation (`[#1573]`). owner: D1 lane after the operator ratifies ADR-alpha. target batch: D1 · Done when: one template names the queue call and the other does not; `dispatcher_order_adopts_queue`-style test pins it; real-use witness: the next batch has no `queue` call by a seat the template does not name · touches: see the body · kill-candidates: `[#1573]` -- the first-handover step; this row decides who owns it · refs `[#1573]`, `[#1536]`, `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18.md` · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
