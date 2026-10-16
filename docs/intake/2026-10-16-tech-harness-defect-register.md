---
intake-id: 116
status: SEED
origin: "to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md PART 8 and to-cc/AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15.md"
consumed-by:
---

# SEED -- the harness defects found on 2026-10-14/15 are rows, not report prose

Many sessions of 2026-10-14/15 found defects that lived only in their own reports. This night close-out collected them (verified harness map, NV lane digests, phase 0, the BU integrator receipt and lane handbacks, the inventory digest, the outcome scoreboard), deduplicated each against `tasks/`, and filed the remainder as one row per defect cluster with an executable Done-when. A defect that already had a row got that row's id, not a new one.

Carrier rows: [#1569], [#1570], [#1571], [#1572], [#1573], [#1574], [#1575], [#1576], [#1577], [#1578], [#1579], [#1580], [#1581], [#1582], [#1583], [#1584], [#1585], [#1586], [#1587], [#1588], [#1589], [#1590], [#1591], [#1592], [#1593], [#1594], [#1595]. A row decides nothing (ADR-111). The defect-to-row index is in `to-browser/DIGEST-NIGHT-CLOSEOUT-2026-10-15.md`.


## Evidence set -- the archived digests this register was built from

The defect rows above cite these digests (archived into `docs/audits/` by the same night close-out) as their evidence. This record lists them so each has a governance-pool consumer (the consumer-at-landing rule); it decides nothing (ADR-111).

- `2026-10-14-technical-handoff-gaps.md`
- `2026-10-14-technical-handover-answers.md`
- `2026-10-14-technical-how-work-runs.md`
- `2026-10-14-technical-night-ready.md`
- `2026-10-14-technical-operator-asks-register.md`
- `2026-10-14-technical-outer-loop-research-v2.md`
- `2026-10-14-technical-phase0.md`
- `2026-10-14-technical-verify-ci.md`
- `2026-10-14-technical-verify-commands-skills.md`
- `2026-10-14-technical-verify-dispatch.md`
- `2026-10-14-technical-verify-handoff-tools.md`
- `2026-10-14-technical-verify-hooks-gates.md`
- `2026-10-14-technical-verify-land.md`
- `2026-10-14-technical-verify-providers.md`
- `2026-10-14-technical-verify-spine-engine.md`
- `2026-10-14-technical-verify-telemetry.md`
- `2026-10-14-technical-verify-transport.md`
- `2026-10-15-technical-build1-challenge-eval1.md`
- `2026-10-15-technical-build1-challenge-eval2.md`
- `2026-10-15-technical-build1-challenge-m2-r113.md`
- `2026-10-15-technical-build1-challenge-m3-r114.md`
- `2026-10-15-technical-build1-challenge-m4-runner.md`
- `2026-10-15-technical-build1-challenge-m5-l6.md`
- `2026-10-15-technical-build1-challenge-responses.md`
- `2026-10-15-technical-build1-design-recheck.md`
- `2026-10-15-technical-build1-ready.md`
- `2026-10-15-technical-design-outer-loop-checker.md`
- `2026-10-15-technical-design-outer-loop.md`
- `2026-10-15-technical-outcome-scoreboard.md`
- `2026-10-15-technical-plan-harness-2026-10-14-r7.md`
- `2026-10-15-technical-ratification-2026-10-14-v9.md`
- `2026-10-15-technical-test-execution-map.md`
- `2026-10-15-technical-test-strategy-decision-annex.md`
- `2026-10-15-technical-test-strategy-decision.md`
- `2026-10-15-technical-token-burn-and-handoff-inventory-annex.md`
- `2026-10-15-technical-token-burn-and-handoff-inventory.md`
- `2026-10-15-technical-verified-harness-map.md`
- `2026-10-16-technical-process-matrix.md`
