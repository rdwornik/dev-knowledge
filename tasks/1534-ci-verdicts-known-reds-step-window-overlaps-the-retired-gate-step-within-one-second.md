---
id: "[#1534]"
title: "ci_verdict's known_reds step window overlaps the retired gate step within one second and reads its REGRESSION lines"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1534] [P1][S] **ci_verdict's known_reds step window overlaps the retired gate step within one second and reads its REGRESSION lines** - `scripts/ci_verdict.py` `_step_window` (~:249-266) pads the known_reds step's (startedAt, completedAt) by one second (`gh run view --json jobs` resolves to the second) and `parse_suite_gate_block` (~:268) reads every `  REGRESSION` line inside it; on main 64704a83 run 38646687088 the retired `[#802]` gate step printed 6 REGRESSION lines per leg at 22:29:21.13Z and the known_reds step ran at 22:29:21.21Z, within the same second, so `ci_verdict --ref 64704a83...` (no baseline) reports RED with 12 new reds while both legs' known-reds-compare.out say PASS, 0 outside the registry. `merge_path.py land` is unaffected (it judges against the base: PRE-EXISTING). The live log's TAB-separated step field did carry the real step name on this run, contrary to the module docstring's "UNKNOWN STEP" measurement. Residual of the green-main pilot's X3 fix (8788e197); the nearest rows, [#1427] and [#1426], own `handoff_state.row_ci`'s baseline and same-SHA flapping, not this step scoping · Done when: a RED-first test with a job log in which the retired gate step's REGRESSION lines and the known_reds block share one second proves `parse_suite_gate_block`/`verdict_for` return only the known_reds block's REGRESSION ids (scoped by the block itself -- the 'known-reds compare' header through its 'verdict' line -- or by the step field), and `uv run --locked python scripts/ci_verdict.py --ref 64704a83755add7115adc3f5216b5f5e5d9b81de` reports 0 new reds · refs `scripts/ci_verdict.py`, `docs/intake/2026-10-15-tech-ci-verdict-step-window-overlap.md` · kill-candidates: none -- no open row owns ci_verdict's step scoping (grep over tasks/ on 2026-10-15) · source: `docs/intake/2026-10-15-tech-ci-verdict-step-window-overlap.md`; BATCH-GREEN-MAIN-PILOT-2026-10-14
