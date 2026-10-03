---
id: "[#1345]"
title: "The desired-state schema lags the parity surfaces: a settings_hook_script probe type is not in its enum"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1345] [P2][S] **The desired-state schema lags the parity surfaces: a settings_hook_script probe type is not in its enum** - `tests/test_desired_state_loader.py::test_live_repo_loads_clean_and_writes_nothing` fails with a pydantic validation error for `Probe` (the `type` enum does not list the probe type the live surfaces use) and `tests/test_desired_state_schema.py::test_enums_match_parity_surfaces_on_disk` names the extra item `settings_hook_script`. Both legs, every recent run; registered pre-freeze without an owner. Cause read from the failure text only · Done when: the schema enum and the parity surfaces on disk agree, with the enum derived from or checked against the surfaces rather than retyped, and both tests are green on both CI legs · touches: `scripts/desired_state_loader.py`, `tests/test_desired_state_loader.py`, `tests/test_desired_state_schema.py` · kill-candidates: none -- no open row tracks the probe-type enum · refs `scripts/desired_state_loader.py`, `tests/test_desired_state_loader.py`, `tests/test_desired_state_schema.py` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
