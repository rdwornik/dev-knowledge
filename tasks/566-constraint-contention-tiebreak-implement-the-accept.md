---
id: "[#566]"
title: "Constraint-contention tiebreak — implement the accepted `[#488]` LEAN"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#566] [P2][M] **Constraint-contention tiebreak — implement the accepted `[#488]` LEAN** — The `[#488]` axis LEAN is **accepted** (architect, 2026-08-20), so this row builds it: rank by **constraint-contention over `serialize-group`**, layered as a tiebreak **UNDER** the hand-set `[P1..P3]` rather than replacing it, with **`P-enum + age` (id as a monotonic, ledger-backed age proxy) as the zero-cost floor** beneath both. The C4 prework measured every candidate axis against the same two rows and this is the only one that needs **no new field**, is **fully derivable by the existing generator today** (`serialize-group` is set on 116 of 183 open rows and is already parsed), and separates the pair **41-to-0** — it is also the only axis that would have predicted the batch-6 dispatch refusal *before* it happened. **What the LEAN forecloses, recorded so it is not re-costed:** WSJF and RICE each demand 3-4 recurring estimates across 183 rows for an ordering they produce by judgement anyway (WSJF alone = 732 new estimates), and the row's own graph-centrality candidate is **inert on today's 3-edge population** and is reframed as a prose-mention attention measure or dropped. Fibonacci binding holds for any estimated field that does enter. · Done when: the ranking is computed by the existing generator from `serialize-group` with no new authored field, `[P1..P3]` remains the primary key and the contention count breaks ties within a tier, `P-enum + age` breaks what remains, and a test pins the ordering of a seeded tie block · refs docs/audits/2026-08-19-technical-c4-ruling-prework.md, #488, #533, scripts/gen_task_tree.py, ADR-107 · kill-candidates: none — `[#488]` is the DECISION row and its ruling is now given; this is the build that ruling releases, and `[#488]` closes on its own research-and-ruling clause
