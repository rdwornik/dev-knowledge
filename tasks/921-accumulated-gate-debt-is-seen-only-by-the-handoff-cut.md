---
id: "[#921]"
title: "Accumulated gate debt is seen only by the handoff cut -- 11 hard-fails and 272 unruled WARNs built up in one day of merging and nothing surfaced them"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#921] [P1][M] **Accumulated gate debt is seen only by the handoff cut -- 11 hard-fails and 272 unruled WARNs built up in one day of merging and nothing surfaced them** - On 2026-09-19 the architect handoff cut (`scripts/gen_handoff.py --mode architect`, preflight row `ship_gate`) refused over `audit.py ship-gate` RED: 11 hard-fail organs (canonical_freshness, fleet_parity, silent_rule_ratchet, journal_day_letters, landing_predicate, substrate_declaration, consumer_at_landing x5) and 272 new/undispositioned WARNs, at main `1a87132b`. Every one of them landed through a merge on 2026-09-18/19 that passed its own gates. The only mechanism that runs the full `ALL_CHECKS` sweep and reads the aggregate is `ship-gate`, and in practice it fires at the handoff cut, once per window: the least useful moment, because the debt must then be repaired under the cut instead of refused at the merge that introduced it. Cause, measured rather than assumed: `audit-health` is `stages: [manual]` (report-only in conductor `commit-gate`), merge commits run no pre-commit hooks at all, `fleet_health`'s SessionStart sweep is not wired, and integrators land lanes with a bare `git merge --no-ff` from an integration worktree rather than `/ship` (every 2026-09-19 JOURNAL merge entry). So a hard-fail introduced by a merge is invisible until the cut · Done when: a hard-fail or a net-new undispositioned WARN introduced by a merge to `main` is surfaced AT THAT MERGE (refused, or recorded on a surface the integrator reads before the next merge), with a RED-first witness showing a merge that adds a ship-tier hard-fail is caught before the handoff cut, and the handoff cut is no longer the first mechanism to see it · refs operator order 2026-09-19 (pre-handoff repair arc, "the only mechanism that sees accumulated gate debt runs at the least useful moment"), `scripts/gen_handoff.py` (`_row_ship_gate`), `scripts/audit.py` (`cmd_ship_gate`), `.pre-commit-config.yaml` (`audit-health`), `docs/audits/2026-08-27-technical-lane-nb-tiering.md`
