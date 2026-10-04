---
id: "[#1378]"
title: "The rulings gate is armed at batch close and the first real cut, and its verdict is recorded"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1378] [P1][S] **The rulings gate is armed at batch close and the first real cut, and its verdict is recorded** - R79 item 3 (operator, 2026-10-04): "we must be certain it is never forgotten". The gate is `scripts/decision_coverage.py rulings`, registered as the `check_rulings_carried` audit finding and in the handoff organ set, so the batch-close trial cut and the real cut both run it. This row keeps the gate honest after it lands: it must be seen to run where it was meant to, and to refuse when it should. · Done when: the B2-W1 batch-close trial cut's `ship_gate` row names `rulings_carried` among its organs and passes, pasted in the digest; the test that seeds an unlanded ruling older than one closed batch (in `tests/test_decision_coverage.py`) still fails the gate when run; the first real cut after landing records the gate's verdict in its receipt; any refusal on a ruling outside R55-R79 is named in the digest and not silenced by an exclusion · owner: the integrator at B2-W1 close; the next incoming seat at its first cut · touches: none (verification only): `scripts/decision_coverage.py`, `scripts/gen_handoff.py --trial-cut` · kill-candidates: `[#721]` -- it asks the same question of the register at entry granularity; the integrator closes it when its own Done-when holds, and this row outlives it as the arming check · refs `[#721]`, `scripts/decision_coverage.py`, `protocols/STANDING_RULINGS.md` section AR (R79) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R79 in `to-browser/RATIFICATION-2026-10-04.md R79`
