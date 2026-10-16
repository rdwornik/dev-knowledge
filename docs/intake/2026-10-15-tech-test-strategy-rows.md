---
intake-id: 115
status: SEED
origin: "to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md (T2 council on R119 and R120), base main b6161972"
consumed-by:
---

# SEED -- the day/night test system (R119) and tests in the graph (R120) need build rows

R119 (the operator, 2026-10-15) moves the full both-OS suite to one night batch: by day a lane gets fast Tier-1 checks on its branch, and by night the integration batch runs sharded, with mutmut and the heavy gates. R120 makes tests graph nodes. Removing a feature carries its tests, and tests that prove nothing are found by measurement. The T2 council turned both into a draft ADR for the operator's ratification. This intake carries the rows the draft needs: BUILD-2a slot 1 (tiered CI) and the first night's census.

Carrier rows:
- BUILD-2a slot 1: [#1560], [#1561], [#1562], [#1563], [#1564];
- the first night: [#1565], [#1566], [#1567];
- BUILD-2b: [#1568].

A row decides nothing (ADR-111). The matrices, the adversaries' objections and their answers, the ADR draft and the three open questions are in `to-browser/DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md` and its ANNEX.

Ids were taken above the reach of the parallel sessions: task ids from [#1560] and intake 115. On 2026-10-15 the highest task id on any ref was 1540 and the highest intake id 110, while S3 and the BU lanes may file rows.
