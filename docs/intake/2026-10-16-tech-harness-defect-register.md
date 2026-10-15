---
intake-id: 116
status: SEED
origin: "to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md PART 8 and to-cc/AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15.md"
consumed-by:
---

# SEED -- the harness defects found on 2026-10-14/15 are rows, not report prose

Many sessions of 2026-10-14/15 found defects that lived only in their own reports. This night close-out collected them (verified harness map, NV lane digests, phase 0, the BU integrator receipt and lane handbacks, the inventory digest, the outcome scoreboard), deduplicated each against `tasks/`, and filed the remainder as one row per defect cluster with an executable Done-when. A defect that already had a row got that row's id, not a new one.

Carrier rows: [#1569], [#1570], [#1571], [#1572], [#1573], [#1574], [#1575], [#1576], [#1577], [#1578], [#1579], [#1580], [#1581], [#1582], [#1583], [#1584], [#1585], [#1586], [#1587], [#1588], [#1589], [#1590], [#1591], [#1592], [#1593], [#1594], [#1595]. A row decides nothing (ADR-111). The defect-to-row index is in `to-browser/DIGEST-NIGHT-CLOSEOUT-2026-10-15.md`.
