---
id: "[#1711]"
title: "G-EDGE: organs called only from a command or an order template have no wiring edge (R149)"
status: open
priority: P3
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1711] [P3][M] **G-EDGE: organs called only from a command or an order template have no wiring edge (R149)** - `lane_boot.py`, `id_allocator.py`, `worktree_import_proof.py`, `system_map.py`, `handback.py`, `ship_gate_diff.py` are called from `.claude/commands/*.md` or imports, which the census does not count; three now hold `called_by`, `ship_gate_diff.py` holds `manual_until: 2026-11-23`, and `handback.py` / `lane_boot.py` keep the expired 2026-10-19 date because `tests/test_organ_truth.py` pins it · owner: census/graph lane · target batch: E3 · Done when: (1) RED first: `test_every_organ_wiring_fate_stays_manual_until_not_moment_or_retire` is changed to pin the shape, not the date; (2) `handback.py` and `lane_boot.py` get their fate (`called_by` or dated); (3) real-use witness: `audit.py ship-gate` reads 0 hard-fail with `organ_truth` green · touches: `tests/test_organ_truth.py`, `ecosystem/harness.yaml` · kill-candidates: `[#664]` -- the open question whether a command is a trigger · decided-by: R149 (operator, 2026-10-19) · source: G-EDGE in `to-browser/DIGEST-E1-FATES-2026-10-19.md`
