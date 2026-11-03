---
id: "[#1624]"
title: "test_manifest_link_route's class-enum assert compares by identity, so a module reload by an earlier test in the same xdist worker reds it"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1624] [P3][S] **test_manifest_link_route's class-enum assert compares by identity, so a module reload by an earlier test in the same xdist worker reds it** - `tests/test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object` (line 236) asserts `is` on a frozenset; the full `-n 2` run of the night-retire lane at `92918815` failed it with two equal frozensets that were different objects, while it passed alone (15 passed, `-n 0`) and was green on `0bea1ff6`. An earlier test in the same worker reloads the hermetization module, so identity is order-dependent. Tech-Architect-45 ruling 2026-10-17: order-dependent, not a defect of the night-retire merge · Done when: RED first: a test reloads the hermetization module before the assert and fails on `39ff8268`; then the assert compares by equality (or the test guards against the reload) and passes alone, after a reload and in a full `-n 2` run · touches: `tests/test_manifest_link_route.py` · kill-candidates: none -- no open row covers this assert · refs `[#1350]` · source: Tech-Architect-45 ruling 2026-10-17 (1), the night-retire land
