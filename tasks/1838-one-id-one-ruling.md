---
id: "[#1838]"
title: "one id, one ruling"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1838] [P2][S] **one id, one ruling** - disambiguate the two R11 rulings (GO-E3.0 R11 vs `protocols/STANDING_RULINGS.md:4885`) and add a check that refuses duplicate ruling ids (E3.2; operator P-4, 2026-11-01) · Done when: RED first: a check over `protocols/STANDING_RULINGS.md` refuses two rulings that carry the same id and names both; the two R11 rulings (GO-E3.0 R11 "routing as data", recorded at `protocols/STANDING_RULINGS.md:7667`, and R11 "the CI/OS ADR is ratified", `protocols/STANDING_RULINGS.md:4885`) are disambiguated by a recorded ruling and the check is green on the tree. Evidence: both R11 entries exist today, `protocols/STANDING_RULINGS.md:4885` and `protocols/STANDING_RULINGS.md:7667` (full text of the second: GO-E3.0.md:20). · touches: `protocols/STANDING_RULINGS.md`, `scripts/validate_standing_rulings.py`, `tests/test_validate_standing_rulings.py` · kill-candidates: none -- no open row owns duplicate ruling ids · refs `protocols/STANDING_RULINGS.md` · source: to-browser/DIGEST-E3-1-PACKAGE-2026-11-01.md P-4 · decided-by: the operator, 2026-11-01, E3.1 package
