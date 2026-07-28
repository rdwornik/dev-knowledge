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

- [#278] [P2][M] Test-suite hygiene epic (consumes intake-id 3) — theatricality review of the pytest corpus (find tests asserting nothing real, padding the collected count) + impacted-test selection so `/ship` runs only change-affected tests, not the full corpus. PRECONDITION (first): the suite recently got faster for an unverified reason — answer WHY with evidence before any cleanup lands. UAT = intake doc #3 ex-ante ACs VERBATIM: (1) ship-gate wall-time delta AND collected-count delta measured against a baseline RECORDED BEFORE cleanup starts (not reconstructed after); (2) the "why did it get faster" question answered with evidence, not a guess, before any cleanup lands. Constraints (doc #3 non-goals): no test deletion without operator review (core-invariant #3); no coverage reduction disguised as cleanup. Selection mechanism (markers / path-map / git-diff) = technical architect's call; decomposition = a later session. **Census scope note (2026-07-08):** the theatricality pre-scan was CLEAN fleet-wide (zero `assert True` / `assert 1 ==` / assert-nothing tests), so #278 narrows to impacted-test selection + ship wall-time + the parametrize candidate (ai-council `test_base_provider.py`, 28 one-assertion tests — each asserts real behaviour, a shape not theatre). · Done when: both UAT ACs hold AND the theatricality review + impacted-test selection ship · refs docs/intake/archive/2026-07-07-test-suite-hygiene.md, scripts/audit.py, ADR-98, docs/audits/2026-07-08-fleet-consistency-census.md Part 2
