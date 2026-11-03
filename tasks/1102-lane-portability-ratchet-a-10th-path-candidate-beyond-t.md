---
id: "[#1102]"
title: "lane-portability-ratchet: a 10th path-defect candidate beyond T2's named 9"
status: closed
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1102] [P3][S] **lane-portability-ratchet: a 10th path-defect candidate beyond T2's named 9** - while separating host-witness cases from genuine portability defects for row L3 (they must never share the `operator_host` marker -- that would hide a real code defect, not a host read), lane-host-witness found `tests/test_preflight_freeze_predicates.py::test_i_off_repo_path_that_does_not_exist_is_refused` failing Linux-only in CI run 36314839016, matching T2's "path" class but outside the 9 sites T2 named (lane-portability-ratchet's row L4 files: "the 9 test/script sites"). Left unconfirmed and unfixed here -- out of this lane's owned files. · Done when: L4's inventory either includes this id with a fix (or a named reason it is not a path defect) · refs tests/test_preflight_freeze_predicates.py, to-browser/SESSION-decision-ci-verification-2026-09-26-seat-71020de7.md (T2, K3), CI run 36314839016 job 108607476905 (ubuntu-latest) · kill-candidates: none -- no open row tracks this candidate · **CLOSED 2026-11-03** — evidence 41df0087b3cff012aaf2a7075d038520fb4cb1f6
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-27 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
