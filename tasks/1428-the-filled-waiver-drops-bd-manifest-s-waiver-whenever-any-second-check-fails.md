---
id: "[#1428]"
title: "The --filled waiver drops BD-manifest's waiver whenever any second check fails"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1428] [P1][S] **The --filled waiver drops BD-manifest's waiver whenever any second check fails** - `_row_ship_gate` (`gen_handoff.py:1218-1247`) waives a `--filled` re-render only when the hard-fails are exactly the bundle's own BD-manifest (plus BD-ci/BD-seats by identity, `:1066`, `:1152`). Any other failure voids the whole waiver, so BD-manifest -- stale by construction once a bundle is filled -- is reported as a blocker beside the real one: 3 hard-fails at the dry run's stage 8, 2 with P13 masked at stage 9 (readiness digest F15, F16) · Done when: the waiver is per finding: the bundle's own BD-manifest is waived whatever else fails, every other hard-fail still refuses, and the refusal names only the unwaived findings; a RED-first test with BD-manifest plus one unrelated hard-fail · owner: the handoff generator · touches: `scripts/gen_handoff.py`, tests · kill-candidates: `[#1425]` · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/gen_handoff.py, ADR-129
