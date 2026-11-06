---
id: "[#1887]"
title: "handoff_probes BD rows read n/a in CI where the transport and gh are absent (defect 16)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1887] [P1][S] **handoff_probes BD rows read n/a in CI where the transport and gh are absent (defect 16)** - `scripts/audit.py health`'s `handoff_probes` check re-derives the active bundle's BD rows live; in the conductor's `commit-gate` job there is no Drive transport and no authenticated gh, so BD-ci, BD-plan, BD-rulings, BD-capabilities and BD-decisions report `toothless` by construction and audit-health exits 1 (run 42089244162, `commit-gate`). Defect 16 of to-browser/DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05.md. `handoff_probes` and its five BD lines were registered on the carrier branch by ADDENDUM-2 item 3 (`8f9598ba4`) and reverted after lane-branch run 42111195229 showed the extra lines red four fixture tests of `tests/test_known_reds_gate_hooks.py` that pin the allowlist to the four CGG-1 check names (defect 19); so this row's fix, landed on main before the bundle, is the only exit and no registry entry is owed. · touches: `scripts/audit.py`, `scripts/verify_handoff_probes.py`, `tests/test_verify_handoff_probes.py`, `tests/test_handoff_state.py` · kill-candidates: none - no open row owns the BD rows' CI behaviour · refs `[#1834]`, `scripts/audit.py`, to-browser/DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05.md (defect 16) · Done when: RED first - a test that runs the handoff_probes check with the transport root unresolved and gh unavailable and expects each BD row that needs them to read n/a (WARN, not FAIL), while a BD row whose inputs ARE present and disagree still FAILs; then the check implements it; the lane-branch CI run's commit-gate is green outside known reds · decided-by: architect, DIGEST-RULING-H5-LAND-INPUTS-ADDENDUM-2-2026-11-05 option B item 3 · source: conductor run 42089244162 job commit-gate
