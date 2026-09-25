---
id: "[#1023]"
title: "integrator: test_wal_concurrency_smoke_real_processes flaked once on CI, not in the known-reds registry"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1023] [P2][S] **integrator: test_wal_concurrency_smoke_real_processes flaked once on CI, not in the known-reds registry** - WAVE5B-N1 integrator FINDING: `tests/test_telemetry_emit.py::test_wal_concurrency_smoke_real_processes` reddened once in CI on lane 9's merge (1 of 4 writers failed to connect), passes locally, and lane 9 touches no telemetry -- a runner concurrency flake, not yet in `logs/` known-reds. · Done when: the flake is reproduced and fixed, or added to the known-reds registry with the CI run id as evidence · refs `tests/test_telemetry_emit.py::test_wal_concurrency_smoke_real_processes`, DIGEST-WAVE5B-N1-2026-09-25 · kill-candidates: none -- no open row tracks this flake
