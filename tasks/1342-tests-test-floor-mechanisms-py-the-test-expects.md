---
id: "[#1342]"
title: "tests/test_floor_mechanisms.py: the test expects 21 plain floor components and the manifest declares 23"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1342] [P2][S] **tests/test_floor_mechanisms.py: the test expects 21 plain floor components and the manifest declares 23** - DCT D7. `test_pre_existing_components_are_untouched_by_the_mechanism_reader` asserts `len(plain) == 21`; `deploy/manifest-v1.5.0.yaml` yields 23 at 2e7fa5f2 (22 when registered; f643e4e3 added the component `codex-review-organ`). The count is typed into the test, so every new floor component reds it; whether the manifest or the typed number is the stale half is unread. **A real defect, still to be fixed**: held at 23 under a ceiling (AM2-3), owner `rob`, expiry 2026-10-17 · Done when: the test derives its expectation from the manifest (or the manifest is corrected, with the reason for each component recorded) instead of a retyped integer, the test is green on both CI legs, and the registry entry is removed · touches: `tests/test_floor_mechanisms.py`, `deploy/manifest-v1.5.0.yaml`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- no open row owns the floor component count · refs `tests/test_floor_mechanisms.py`, `deploy/manifest-v1.5.0.yaml`, `logs/KNOWN-REDS-REGISTRY.json` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
