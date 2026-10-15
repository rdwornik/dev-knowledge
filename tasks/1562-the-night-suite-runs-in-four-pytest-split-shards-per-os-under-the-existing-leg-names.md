---
id: "[#1562]"
title: "The night suite runs in four pytest-split shards per OS, and a fail-closed aggregator keeps the two pytest leg names and the known-reds compare unchanged (R119 night, BUILD-2a slot 1)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1562] [P1][M] **The night suite runs in four pytest-split shards per OS, and a fail-closed aggregator keeps the two pytest leg names and the known-reds compare unchanged (R119 night, BUILD-2a slot 1)** - The Windows leg takes 1551-1555 s and Linux 544-770 s (runs 38725590391, 38656374259); R119 shards the night suite and R86 approved `pytest-split`. `land` reads six contexts, two of them `pytest (ubuntu-latest)` and `pytest (windows-latest)` (`scripts/actions_verdict.py:97-98`), and the compare pins the worker count (`scripts/known_reds.py:583-592`), so shards must reach the verdict as the same two legs · Done when: RED first: (1) each OS leg runs 4 shards, `--splits 4 --group <k> --splitting-algorithm least_duration`, each with `-n 4 --dist loadgroup -m "not operator_host" --junitxml`; (2) a per-OS aggregator job named as today's leg FAILS the leg when any shard is missing, cancelled or has no artifact, unions the shard results and runs the existing known-reds compare (`conductor.yml:165-227`) unchanged, recording `-n 4` per shard; (3) the aggregator converts JUnit times to `.test_durations` and uploads it for the next night; with no durations the split is by count; (4) a witness test FAILS when any `xdist_group` spans two shards (if it fires, a conftest hook pins group members to the first member's shard); (5) the night's per-OS wall time is recorded beside 1551 s / 751 s; (6) pytest-split is declared per OQ1; (7) the witnesses fail on `b6161972` · touches: `.github/workflows/conductor.yml`, `pyproject.toml`, `uv.lock`, `tests/conftest.py` (only if (4) fires), tests · kill-candidates: [#1383] -- its 420 s Linux target is met per shard here, and `[#1451]` item 1 (the split) is carried by this row · refs `[#1451]`, `[#1383]`, `[#1560]`, ADR-127 D1/D2, `docs/intake/2026-10-15-tech-test-strategy-rows.md` · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q2
