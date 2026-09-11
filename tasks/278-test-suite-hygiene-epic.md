---
id: "[#278]"
title: "Test-suite hygiene epic"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#278] [P2][M] Test-suite hygiene epic (consumes intake-id 3) — theatricality review of the pytest corpus + impacted-test selection so `/ship` runs only change-affected tests. PRECONDITION (first): the suite recently got faster for an unverified reason — answer WHY with evidence before any cleanup lands. UAT = the intake doc's ex-ante ACs VERBATIM: (1) ship-gate wall-time delta AND collected-count delta measured against a baseline RECORDED BEFORE cleanup starts (not reconstructed after); (2) the "why did it get faster" question answered with evidence, not a guess, before any cleanup lands. Constraints (doc #3 non-goals): no test deletion without operator review (core-invariant #3); no coverage reduction disguised as cleanup. Selection mechanism = technical architect's call. **Census note:** the theatricality pre-scan was CLEAN fleet-wide, so #278 narrows to impacted-test selection + ship wall-time + one parametrize candidate · Done when: both acceptance criteria from `docs/intake/archive/2026-07-07-test-suite-hygiene.md` hold with the criterion text quoted in the closing commit, and the theatricality review ships as a `docs/audits/` artifact and impacted-test selection is live in the verify cadence with a test · refs scripts/audit.py, ADR-98, the fleet-consistency census Part 2 · UN-DEFERRED 2026-09-11 by batch W lane w-7 (AW2-1). The 2026-08-27 icebox DEFER stated its own condition — "Un-defers when an arc claims the row" — and an arc claims it, so the clause is struck. Peg retained: **no row-level dependency was ever claimed**; this was an ATTENTION decision, not a blocked-by.
