---
id: "[#1683]"
title: "R159 (update what teaches a process in the SAME change) is not taught in the seat templates or the lane-contract generator (H30)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1683] [P2][S] **R159 (update what teaches a process in the SAME change) is not taught in the seat templates or the lane-contract generator (H30)** - R159 is a ruling but no template or generated contract carries the 'T. Teaching' step, so a change to a process lands without its teaching unless a human adds the step · owner: a templates lane · Done when: (1) the generator and templates emit the T step; (2) real-use witness: a generated contract carries item T; (3) R159 before/after lines · touches: `scripts/gen_lane_contract.py`, `templates/dispatcher-order-template.md` · kill-candidates: `[#1447]` -- same generator · refs `[#1447]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H30 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
