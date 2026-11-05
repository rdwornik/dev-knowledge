---
id: "[#1886]"
title: "test_g applies to lane branches, not to a handoff cut's landing (defect 14)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1886] [P1][S] **test_g applies to lane branches, not to a handoff cut's landing (defect 14)** - `tests/test_handoff_v5_boot.py::test_g_handoff_files_are_unchanged_from_origin_main` (lines 146-166, added 2026-11-02 by `3b303914f` under `[#1834]`) asserts that `git diff --name-only origin/main...HEAD -- docs/handoffs` is empty, so every handoff landing fails it by construction: the H5-LAND integration run 42089244162 on `5e4bc68dd` failed it with exactly the 16 files of `docs/handoffs/2026-11-05-dev-knowledge-architect/`. Defect 14 of to-browser/DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05.md. A `members` entry for that node was registered on the carrier branch by ADDENDUM-2 item 2 (`8f9598ba4`) and reverted after lane-branch run 42111195229 showed that any registry edit reds `tests/test_known_reds_gate_hooks.py::test_registry_is_origin_main_plus_exactly_the_lines_field` (defect 19); so this row's fix, landed on main before the bundle, is the only exit and no registry entry is owed. · touches: `tests/test_handoff_v5_boot.py` · kill-candidates: none - no open row scopes test_g · refs `[#1834]`, `tests/test_handoff_v5_boot.py`, to-browser/DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05.md (defect 14) · Done when: RED first - a test that runs test_g's predicate on a branch that adds one new dated bundle dir under docs/handoffs/ and nothing else, and expects it to pass, while a branch that edits an EXISTING bundle file still fails; then test_g implements that scope; the lane-branch CI run is green outside known reds · decided-by: architect, DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05 option B item 2 · source: conductor run 42089244162
