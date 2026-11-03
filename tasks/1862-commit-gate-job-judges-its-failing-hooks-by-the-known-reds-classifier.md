---
id: "[#1862]"
title: "conductor: the commit-gate JOB step judges its failing hooks by the registered known-reds classifier, so the job concludes success when every red is a registered environment mismatch"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "AMEND-CGG-1"
generates: BACKLOG.md
---

- [#1862] [P1][M] **conductor: the commit-gate JOB step judges its failing hooks by the registered known-reds classifier, so the job concludes success when every red is a registered environment mismatch** - `.github/workflows/conductor.yml` job `commit-gate`, step "Run the moved commit-gate hooks over this range's staged set", ends `exit $rc` over `pre-commit run --hook-stage manual`; `audit-health` always fails there on host-local checks that `logs/KNOWN-REDS-REGISTRY.json` registers, so the job could not succeed on the CI host by construction (Q-CG-A6b) · Done when: `scripts/known_reds.py compare-commit-gate` (`compare_commit_gate` + `render_compare_commit_gate`) classifies EVERY failing hook of commit-gate.out through the unchanged `compare_hook` and the same registry, matches audit-health at LINE level against the new `hooks.audit-health.lines` field (Amendment CGG-1), fails closed on an unparseable failure, and the first step exits through it; the commit-gate JOB of the lane's push run concludes `success`; tests in `tests/test_known_reds_gate_hooks.py` (Done-contract 1-4 of LANE-e30-commit-gate-green) · touches: `scripts/known_reds.py`, `.github/workflows/conductor.yml`, `logs/KNOWN-REDS-REGISTRY.json`, `tests/test_known_reds_gate_hooks.py`, `tasks/1862-commit-gate-job-judges-its-failing-hooks-by-the-known-reds-classifier.md` · implements: AMEND-CGG-1 · kill-candidates: `[#1800]` -- stays open until the post-MERGED check · refs `.github/workflows/conductor.yml:878-920`, `scripts/known_reds.py:1077`, [#1800], [#1863], to-browser/DIGEST-RULING-Q-CG-A6-A6B-2026-11-02.md R2 option A, tasks/manifest.json node 1862 · source: LANE-e30-commit-gate-green.md · decided-by: the architect (Q-CG-A6-A6B R2 option A; Q-CGG-1 = A)
