---
id: "[#1627]"
title: "R125 audit: every ruling since 2026-07-01 counted by adoption state"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1627] [P2][S] **R125 audit: every ruling since 2026-07-01 counted by adoption state** - The R125 decision-to-implementation audit counts every ruling since 2026-07-01 by BUILT+USED / BUILT-UNUSED / ROW-OPEN / NO-CARRIER / WITHDRAWN. D0.3 (S0b): every RATIFICATION, DECLARE, AMEND, accepted ADR, STANDING_RULINGS section and PROPOSAL-ADR since 2026-07-01 is one row with decision, date, carrier, state and witness; every NO-CARRIER and BUILT-UNUSED item becomes a deduped row with a real-use Done-when; one ranked adopt-next list. owner: CC audit track D0.3; the gate half stays in the DECLARE (refuse a batch while an operator-ratified decision older than 7 days has NO-CARRIER). target batch: D0 · Done when: `to-browser/DIGEST-ADOPTION-AUDIT-2026-10-18.md` carries the counts per state and the ranked list, each witness opened or marked UNVERIFIED; real-use witness: the operator picks rows from the adopt-next list · touches: see the body · kill-candidates: none -- no row carries the audit · refs `protocols/STANDING_RULINGS.md`, `to-cc/DECLARE-DECISION-ADOPTION-AUDIT-2026-10-16.md`, R125 · decided-by: R125, R133 (retro-ratification, D8). Defect H20: R148-R159 were not landed in `protocols/STANDING_RULINGS.md` when the map was drawn (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
