---
id: "[#1682]"
title: "R158 (REUSE CHECK before building) is not taught in the seat templates or the lane-contract generator (H29)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1682] [P2][S] **R158 (REUSE CHECK before building) is not taught in the seat templates or the lane-contract generator (H29)** - R158 is a ruling but no template or generated contract tells the executor to quote the existing mechanism with file:line before building; only hand-built contracts carry it · owner: a templates lane · Done when: (1) the lane-contract generator and the order templates emit the REUSE CHECK step; (2) real-use witness: a generated contract's Done-contract item 0 reads REUSE CHECK; (3) R159 before/after lines · touches: `scripts/gen_lane_contract.py`, `templates/dispatcher-order-template.md` · kill-candidates: `[#1447]` -- generator agrees with plan-lint · refs `[#1447]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H29 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
