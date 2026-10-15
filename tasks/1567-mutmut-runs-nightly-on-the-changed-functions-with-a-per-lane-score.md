---
id: "[#1567]"
title: "mutmut runs nightly on the night's changed functions with a per-lane score, a 70 % threshold and a loud 0-mutant failure (R120 goal, first night)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1567] [P1][M] **mutmut runs nightly on the night's changed functions with a per-lane score, a 70 % threshold and a loud 0-mutant failure (R120 goal, first night)** - The pilot's scope is hardcoded to one module and one test file (`pyproject.toml:236-238`). Its 2077-of-2291 result (run 38706597567; baseline `logs/MUTATION-BASELINE.json`, run 38073707389) is therefore that module's score, not the repo's. mutmut 3.x has no git-diff selection for `.py` files but accepts name filters; it needs `fork`, so it runs on Linux only (`pyproject.toml:200-204`). A 0-executed guard already exists (`.github/workflows/report-only-wall.yml:330-356`) · Done when: RED first: (1) the night job computes the changed functions in the night's first-parent range, runs mutmut with a name filter over them and with the tests `impacted_tests.select` gives for their modules, and retires the hardcoded pilot scope; (2) score = killed / (killed + survived + timeout + no_tests) per lane, where a function belongs to the LAST merge in first-parent order that touched it; (3) a module with a changed function and 0 executed mutants FAILS naming the module; a night with no changed function prints `SKIPPED`; (4) the threshold is 70 %, advisory for 5 nights and then blocking (OQ2), and the morning digest prints each lane's score; (5) a fixture night with two merges touching one function attributes it to the later merge; (6) the tests fail on `b6161972` · touches: `.github/workflows/report-only-wall.yml`, `pyproject.toml`, `scripts/` (one new night helper), tests · kill-candidates: none -- `[#1451]` item 3 (the schedule) and `[#502]` (the pilot) are its inputs, not duplicates (grep `changed functions|mutation score` over tasks/ 2026-10-15) · refs `[#1451]`, `[#502]`, `[#1566]`, R81, `docs/intake/2026-10-15-tech-test-strategy-rows.md` · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q7
