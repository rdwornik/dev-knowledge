---
id: "[#327]"
title: "Protocols-as-interface genre ruling"
status: deferred
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: architecture
generates: BACKLOG.md
---

- [#327] [P2][M] Protocols-as-interface genre ruling (fleet-parity register acceptance) — unify the three current meanings of `protocols/` (hub=methodology, ai-council=Council domain, corp=absent) into ONE genre: "what other repos/agents must know to interact with THIS repo". Minimal start = a `protocols/README.md` (genre definition + the methodology-vs-local boundary applied inside) + one interface doc per repo; corp gets `protocols/` per the closed #314 sibling ruling. Reversible; a ruling + minimal docs, not a framework. **Progress (Lane D 2026-07-25):** the hub genre wording ALREADY exists (`protocols/README.md` scope marker), so the residue was corp's two deferral markers — resolved BY REFERENCE on corp branch `docs/327-interface-genre-markers` @ 4c7d7f4, UNMERGED; open until it ships. · Done when: `protocols/` is documented as the interface genre AND each onboarded repo carries `protocols/README.md` + ≥1 interface doc (n≥1, corp included) · refs docs/audits/2026-07-11-technical-fleet-parity-register.md §5, #314, #316, ADR-41 · kill-candidates: none — operator-ruled register follow-up · serialize-group: architecture · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
