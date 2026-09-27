---
id: "[#1103]"
title: "conductor.yml does not yet exclude operator_host from the CI pytest invocation"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1103] [P2][S] **conductor.yml does not yet exclude operator_host from the CI pytest invocation** - row L3 (lane-host-witness) registers and marks the confirmed host-witness tests (`tests/conftest.py::OPERATOR_HOST_TESTS`), but `.github/workflows/conductor.yml` is out of this lane's owned files (BATCH-COMMON-WAVE5B-N4 ruling k: only `lane-ci-matrix`/`lane-server-governance`/`lane-arm-ci` edit it) and its pytest invocation does not pass `-m "not operator_host"` — Codex terra review of this lane's diff flagged it HIGH (`docs/audits/2026-09-27-codex-lane-host-witness.md`): "CI still executes operator_host witnesses... Linux CI continues to run host-dependent witnesses and treats their failures as known reds, violating the host-witness isolation contract". Until wired, the marker is registered but not yet load-bearing on CI. · Done when: `conductor.yml`'s pytest job(s) pass `-m "not operator_host"` (or an equivalent selector) and a test asserts the selector is present in the workflow file · refs .github/workflows/conductor.yml, tests/conftest.py, docs/audits/2026-09-27-codex-lane-host-witness.md · kill-candidates: none -- no open row tracks this wiring gap
