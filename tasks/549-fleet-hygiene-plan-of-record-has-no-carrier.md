---
id: "[#549]"
title: "The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#549] [P2][S] **The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier** — `docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md` carries `status: ACCEPTED`, `disposition: deferred`, `trigger: "#328 build"` and `decided-by: "operator approval at the 2026-07-11 session wrap (v4 plan-of-record)"`. It holds the binding architecture frame (sensors, event pipeline, rules engine, inventory, presentation, response), the A–F phase sequence with per-phase exit criteria, and is named in its own `note:` as *"the incoming sessions' comparison baseline per #301(iv)"*. **[#328] does not exist** — no `tasks/328-*.md`, zero `^- [#328]` rows (verified 2026-08-17) — so an operator-approved plan is permanently un-startable, and its Phase-A charter ([#548], intake #12) and Phase-E requirements ([#550], intake #14) are parked on the same departed id. **The fork is a decision, not an execution:** the [E9] Fleet Desired-State theme now covers part of the same ground (ADR-109 rules the desired-state contract; [#383]/[#385]/[#388] are live), so intake #13 is either superseded-in-part or re-anchored, and nothing in the corpus says which. · Done when: intake #13 is either recorded SUPERSEDED with [E9]/ADR-109 named as the successor for the overlapping phases and any residue re-filed, or its `trigger:` is re-anchored onto a live id or a date — and if superseded, no living surface still cites it as the incoming sessions' comparison baseline · refs docs/intake/2026-07-11-tech-plan-of-record-fleet-hygiene.md, docs/decisions/ADR-109-fleet-desired-state-contract-v1.md, #301, #383, #385, #548, #550 · kill-candidates: none — [#383]/[#385] execute [E9] waves and neither dispositions intake #13; [#548] and [#550] carry the charter and requirements halves of the same departed build · source: docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md step 2 (intake sweep), building on docs/audits/2026-08-16-census-nb6-archive-sweep.md §1.3
