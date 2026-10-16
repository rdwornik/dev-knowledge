---
intake-id: 117
status: SEED
origin: "to-cc/AMEND-2-BATCH-NIGHT-CLOSEOUT-2026-10-15.md (PART 9) and AMEND-3 (PART 10); operator ruling 2026-10-16: built but unused is a failure"
consumed-by:
---

# SEED -- every declared process is used in a real run or removed, and the start-up context shrinks

The night close-out's process matrix (`docs/audits/2026-10-16-technical-process-matrix.md`) found 90 declared processes: 57 WORKS, 12 BROKEN, 8 DEAD, 6 DECLARED-ONLY, 6 UNRUN, 1 DUPLICATE, plus empty cells where nothing fires (dependency, CI workflow, release, delete-propagation, protocols). Each DEAD or DECLARED-ONLY process is a row: used in a real run with a witness by the next batch's close, else removed. The CRUD sandbox QA suite decided on 2026-09-25 was never built. The token baseline measured the same night (55,634 tokens at start-up, 25.4 k of them this repo's) yields three cut rows whose witness is the baseline re-measured lower.

Carrier rows: [#1596], [#1597], [#1598], [#1599], [#1600], [#1601], [#1602], [#1603], [#1604], [#1605], [#1606], [#1607], [#1608], [#1609], [#1610], [#1611], [#1612], [#1613], [#1614], [#1615], [#1616], [#1617], [#1618]. A row decides nothing (ADR-111).
