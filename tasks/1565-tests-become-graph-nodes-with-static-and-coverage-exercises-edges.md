---
id: "[#1565]"
title: "Tests become graph nodes: static exercises edges in FPG, and a nightly per-sha coverage-context edge artifact (R120.1, first night)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1565] [P1][M] **Tests become graph nodes: static exercises edges in FPG, and a nightly per-sha coverage-context edge artifact (R120.1, first night)** - FPG has no test node or test edge; `tests/` is excluded on purpose so the orphan census does not move (`scripts/impacted_tests.py:371-375`, `scripts/file_purpose_graph.py`). In-process coverage cannot see 72.6 % of test->script edges, which are subprocess-only (`scripts/impacted_tests.py:15-24`), so neither source alone is the graph. pytest-cov's `--cov-context=test` is the xdist-safe context source (pytest-cov #604); pytest-cov and coverage are not in `uv.lock` · Done when: RED first: (1) FPG carries node kind `test` and edge kind `exercises` with `source: static`, built from the impacted_tests table (imports to depth 3, naming, literal text), and `orphan_census`'s process walk is unchanged (its count on `b6161972` is the same after); (2) the night job runs `uv run --locked pytest -n 4 --dist loadgroup -m "not operator_host" --cov=scripts --cov-context=test --cov-report= -p no:cacheprovider` on Linux, then `coverage json --show-contexts`, and uploads `test-edges-<sha>.json` (test -> module with line counts, `source: coverage`) as an artifact; nothing is committed; (3) `system_map`'s `tests` field reads the FPG edges; (4) the night records the coverage overhead against the unsplit Linux time; (5) pytest-cov and coverage are declared per OQ1; (6) the tests fail on `b6161972` · touches: `scripts/file_purpose_graph.py`, `scripts/system_map.py`, `.github/workflows/conductor.yml`, `pyproject.toml`, `uv.lock`, tests · kill-candidates: none -- `[#1451]` item 2 (R86's coverage no-drop gate) stays there and reads this run (grep `test node|exercises` over tasks/ 2026-10-15) · refs `[#1451]`, `[#664]`, R118, `docs/intake/2026-10-15-tech-test-strategy-rows.md`. Defect H36: the test hygiene tools are not locked (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q5; S2 (`to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md`) measures the run's cost
