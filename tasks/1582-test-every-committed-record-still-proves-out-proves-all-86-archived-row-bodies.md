---
id: "[#1582]"
title: "`test_every_committed_record_still_proves_out` proves all 86 archived row bodies"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1582] [P2][S] **`test_every_committed_record_still_proves_out` proves all 86 archived row bodies** - 81 of 86 proven on base, 80 of 86 after a sanctioned note on row 669 (LEG C); red on base and merge (to-browser/SESSION-integrator-bu-2026-10-15.md:13,81,100,127) · Done when: RED first: the existing test passes on a tree where the row-669 note and the five unproven records are repaired by `archive_row_body.py` (not hand edits); fails on 97bcd374 · touches: `tasks/archive/`, `scripts/archive_row_body.py` · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#669]`, `[#664]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
