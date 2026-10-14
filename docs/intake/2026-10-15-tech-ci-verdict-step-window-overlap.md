---
intake-id: 109
status: SEED
origin: "BATCH-GREEN-MAIN-PILOT-2026-10-14, main 64704a83 run 38646687088 -- ci_verdict --ref (no baseline) reports RED with 12 new reds while both legs' known-reds-compare.out say PASS"
consumed-by:
---

# SEED -- ci_verdict's known_reds step window overlaps the retired gate step

`scripts/ci_verdict.py` `_step_window` (~:249-266) pads the known_reds step's (startedAt, completedAt) by one second (`gh run view --json jobs` has one-second resolution) and `parse_suite_gate_block` (~:268) reads every `  REGRESSION` line inside that window. On main 64704a83 run 38646687088 the retired `[#802]` gate step printed 6 REGRESSION lines per leg at 22:29:21.13Z and the known_reds step ran at 22:29:21.21Z, inside the same second, so `ci_verdict --ref 64704a83...` (no baseline) reports RED with 12 new reds while both legs' known-reds-compare.out say PASS, 0 outside the registry. `merge_path.py land` is unaffected (it judges against the base: PRE-EXISTING). The live log's TAB-separated step field did carry the real step name on this run, contrary to the module docstring's "UNKNOWN STEP" measurement. This is a residual of the green-main pilot's X3 fix (8788e197).

Carrier row: [#1534]. A row decides nothing: it asks for the block to be scoped by itself or by the step field (ADR-111).
