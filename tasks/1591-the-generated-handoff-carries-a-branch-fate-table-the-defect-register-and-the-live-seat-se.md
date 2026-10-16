---
id: "[#1591]"
title: "The generated handoff carries a branch-fate table, the defect register and the live seat/session map"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1591] [P1][M] **The generated handoff carries a branch-fate table, the defect register and the live seat/session map** - the successor seat inherited 15 branches without fates; the handoff has no defect register and no live seat map (night close-out PART 7 / amend C) · Done when: RED first: a `gen_handoff` fixture test asserts the cut contains a fate table (branch, contained-in-main, carrier, proposed fate), the open rows tagged `defect-register`, and the seat map from `seat_registry`; fails on 97bcd374 · touches: `scripts/gen_handoff.py`, `templates/`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1456]`, `[#1450]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
