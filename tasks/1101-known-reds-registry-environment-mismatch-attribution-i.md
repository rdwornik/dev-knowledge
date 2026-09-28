---
id: "[#1101]"
title: "logs/KNOWN-REDS-REGISTRY.json: the 4 'environment-mismatch' members no longer reproduce"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1101] [P3][S] **logs/KNOWN-REDS-REGISTRY.json: the 4 'environment-mismatch' members no longer reproduce** - lane-host-witness (row L3) re-checked its premises against live CI (R14/R17) before registering `operator_host` tests and found the registry's 4 `environment-mismatch`-attributed members (`provision_legs.py::test_history_check_exits_0_on_this_repo`, `test_validate_branch_naming.py::test_local_branches_reads_the_live_repo`, `test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH`, `test_worktree_seed.py::test_the_verdict_names_WHY_rather_than_only_failing`) absent from BOTH OS legs' FAILED set on the current origin/main tip -- `lane-ci-matrix`'s `fetch-depth: 0` fix (merged 316d3205) resolved the "no local main ref" cause the registry recorded them for. The registry itself is out of this lane's owned files (contract "Do not" list bars editing it), so the shrink is left for the registry's own owner. · Done when: a comparison run (`scripts/known_reds.py compare` or equivalent) against a current CI run confirms these 4 members are green on both OS legs and removes them from the registry, or the check that would have surfaced an attribution rot on its own runs and is confirmed green · refs logs/KNOWN-REDS-REGISTRY.json, scripts/known_reds.py, CI run 36314839016 (job 108607476905 ubuntu / 108607476913 windows) on origin/main 316d3205 · kill-candidates: none -- no open row tracks this registry drift
