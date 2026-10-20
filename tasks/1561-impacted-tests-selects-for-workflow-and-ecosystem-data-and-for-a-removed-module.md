---
id: "[#1561]"
title: "impacted_tests.py selects the tests a changed workflow or ecosystem data file feeds, and the tests a removed module leaves behind (Tier-1 holes, BUILD-2a slot 1)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1561] [P1][S] **impacted_tests.py selects the tests a changed workflow or ecosystem data file feeds, and the tests a removed module leaves behind (Tier-1 holes, BUILD-2a slot 1)** - Tier 1 (`[#1560]`) trusts the selector, whose measured miss rate is 0.048 (`scripts/impacted_tests.py:34-35`). Two holes are silent: a changed `.github/workflows/*.yml` or `ecosystem/*.yaml` is not under a source root and selects only `-m live_repo` tests (`:88`, `:275-278`), and `tests/test_conductor_governance_jobs.py` and `tests/test_report_only_wall.py` carry no `live_repo` marker; a deleted script selects nothing, because the table is built from the tree on disk (`:515-529`). The third hole, an empty selection, is `[#703]`'s and is not re-filed here · Done when: RED first: (1) a diff touching `.github/workflows/conductor.yml` selects `tests/test_conductor_governance_jobs.py`, and a diff touching an `ecosystem/*.yaml` that a test names selects that test (the literal-text rule already used for `templates/*.ps1` and `tests/fixtures/**`, `:462-512`), else `# FULL SUITE`; (2) a diff that deletes or renames away `scripts/<m>.py` selects every test that imports or names `<m>`, read from the base tree; (3) both fixtures fail on `b6161972` and pass after; (4) no existing selection test changes its expected set · touches: `scripts/impacted_tests.py`, `tests/test_impacted_tests.py` · kill-candidates: none -- `[#703]` owns only the empty-selection case (grep `deleted.*select|workflow.*select` over tasks/ 2026-10-15) · refs `[#703]`, `[#1560]`, `docs/intake/2026-10-15-tech-test-strategy-rows.md`. Defect N7: on main `select()` in `scripts/impacted_tests.py` has no existence guard, so a deleted test path reaches its callers (`tests/test_pairing.py`); the guard exists only on the e2-tier1 repair (81e440f6:647) (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: repo reading for `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q1 (brief D item 1)
