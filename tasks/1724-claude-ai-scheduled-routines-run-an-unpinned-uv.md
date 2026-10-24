---
id: "[#1724]"
title: "The claude.ai scheduled (cloud) routines run an unpinned `uv`; no check ties a routine bootstrap to pyproject's `required-version`"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1724] [P2][S] **The claude.ai scheduled (cloud) routines run an unpinned `uv`; no check ties a routine bootstrap to pyproject's `required-version`** - the cloud substrate was refused partly for an unpinned `uv` (`ecosystem/substrate-registry.yaml:67`); CL-1 keeps the scheduled routines, so they must run the ADR-106 pinned toolchain, and today nothing proves it · owner: lane routine-uv-pin (`scripts/audit_checks/check_routine_consumers.py`) · Done when: (1) RED first: `tests/test_routine_uv_pin.py` fails when a routine bootstrap installs a `uv` other than the exact pin (0.8.17 fixture, unpinned fixture) and passes on the pinned one; (2) the check READS the pin from `pyproject.toml` `[tool.uv] required-version`, never retypes it; (3) the routine environment setup lives OUTSIDE the repo (claude.ai side), so the exact setup line is handed to the operator as `OPERATOR-ACTION` and the repo-side check reports NOT-APPLICABLE until a repo-hosted bootstrap exists; (4) real-use witness: the check run against today's tree, `uv --version` quoted · touches: `scripts/audit_checks/check_routine_consumers.py`, `tests/test_routine_uv_pin.py` · kill-candidates: none -- no open row covers the routine uv pin · refs RATIFICATION-2026-10-24 H1-X, `[#1721]` · decided-by: the operator, 2026-10-24, RATIFICATION-2026-10-24 amendment (b) H1-X, CL-1 · source: `ecosystem/substrate-registry.yaml:67`, `docs/audits/2026-07-06-arc5-routines-pilot-design.md`
