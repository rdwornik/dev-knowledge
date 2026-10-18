---
id: "[#1645]"
title: "R133 consolidation track and plan_lint decision gate"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1645] [P1][M] **R133 consolidation track and plan_lint decision gate** - R125 applies to decisions ratified after 2026-10-18; the older decisions are reviewed, not burned down mechanically (R133). Two parts: a read-only consolidation report of the older decisions, and `plan_lint` refusing a batch that leaves a newer ratified decision older than 7 days with no carrier (adoption-audit finding C01). owner: E2 lane for the gate; the read-only fan-out (Haiku, and Gemini through agy where it runs) writes the report and the operator rules on it. target batch: E2 · Done when: (1) `to-browser/DIGEST-DECISION-CONSOLIDATION-<date>.md` classes every decision of the adoption audit's data as HOLDS, WORTH ADOPTING or OBSOLETE (withdraw) with a witness each, and the operator's ruling on it is recorded in a RATIFICATION file; (2) RED first: `plan_lint check` on a batch order, with a decision ratified after 2026-10-18 whose carrier is missing for more than 7 days, exits non-zero naming the decision, and a decision ratified earlier does not trigger it; real-use witness: the next batch order passes through the gate and a seeded violation is refused in its output · touches: see the body · kill-candidates: `[#1627]` -- its gate half (refuse a batch while a ratified decision older than 7 days has no carrier): decide whether this row subsumes it · refs `[#1627]`, `[#1623]`, `to-browser/DIGEST-ADOPTION-AUDIT-2026-10-18.md` · decided-by: R133, R125 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
