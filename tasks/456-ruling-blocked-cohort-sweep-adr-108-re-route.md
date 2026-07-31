---
id: "[#456]"
title: "Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR-108 §A"
status: open
priority: P2
size: M
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#456] [P2][M] **Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR-108 §A** — the night-batch grooming dossier enumerated **33 rows (18%)** whose Done-when cannot be satisfied by building anything: the completion condition is a *ruling*. ADR-108 §A routes that authority — operator rules FUNCTIONAL questions, architect rules TECHNICAL ones in its own lane, and §A item 4 retires the option-menu anti-pattern. Three rows ([#406] [#407] [#414]) were re-routed in the 2026-07-31 grooming arc; the remaining ~30 are untriaged. Roughly three or four are genuinely operator-owned, for a reason other than being functional — [#122] and [#189]/[#346] by deletion authority and core-invariant #6, [#322] genuinely split. ADR-108's own Consequences concede that nothing mechanically detects an option-menu brief, so this cohort is that gap's standing evidence. · Done when: every remaining row in the cohort is either re-routed, confirmed operator-owned with the reason recorded, or recorded deferred-with-reason · refs ADR-108, #406, #407, #414, #122, #322 · kill-candidates: none — the three re-routed rows are cohort MEMBERS, not its owner; no open task owns the sweep
