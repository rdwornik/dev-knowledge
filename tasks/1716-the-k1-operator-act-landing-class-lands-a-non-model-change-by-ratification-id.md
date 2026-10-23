---
id: "[#1716]"
title: "The K1 operator-act landing class: land_lane.py lands a non-model change keyed by a ratification id"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1716] [P2][S] **The K1 operator-act landing class: land_lane.py lands a non-model change keyed by a ratification id** - `scripts/land_lane.py` has one landing shape, a lane merge whose handback `merge_path.land()` reads through `subst_gate.handback_problems`, so a change no model produced (the held ADR-131 status flip, tag `archive/adr-131-accept-2026-10-22` = commit `89e23db1b`) has no handback and no path. K1 of `to-browser/RATIFICATION-2026-10-22.md` ratified ADR-131 and held that flip to land first "through an operator-act landing class keyed by a ratification id"; D1 of `to-browser/RATIFICATION-2026-10-23.md` admits this row under the H1 exception · implements: ADR-131 · owner: lane landing-class (`scripts/land_lane.py`, `scripts/merge_path.py`) · Done when: (1) `land_lane.py --operator-act K1 --ratification to-browser/RATIFICATION-2026-10-22.md --lane-ref <ref>` lands the ref's change through the same merge, CI judgement and same-sha rule as a lane landing; (2) it REFUSES, exit 5 and nothing pushed, unless the id resolves to a ratified table row `| K1 |` in that file; (3) the id and the ratification file are recorded in the landed merge commit (`Ratified-by:` line); the receipt SCHEMA has no ratification field, so a receipt field is a follow-up inside `scripts/merge_receipt.py` after ci-one-verdict lands; (4) it makes 0 model calls; (5) real-use witness: the integrator's landing of the ADR-131 flip through this class on `main` · touches: `scripts/land_lane.py`, `scripts/merge_path.py`, `tests/test_land_lane_operator_act.py` · kill-candidates: `[#1698]` -- same lane, same landing path, no overlap in Done-when; none removed · refs `[#1698]`, ADR-131 · decided-by: the operator, 2026-10-22, RATIFICATION K1 and 2026-10-23 D1 (H1 exception) · source: `to-browser/RATIFICATION-2026-10-22.md` K1, `to-browser/RATIFICATION-2026-10-23.md` D1, `to-cc/PLAN-HARNESS-2026-10-23.md` §7 L8
