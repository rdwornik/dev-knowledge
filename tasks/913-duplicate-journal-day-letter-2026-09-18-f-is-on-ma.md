---
id: "[#913]"
title: "Duplicate JOURNAL day-letter 2026-09-18 (f) is on main -- audit journal_day_letters FAILs"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "night wave 2 integrator ruling 2026-09-19"
generates: BACKLOG.md
---

- [#913] [P2][S] **Duplicate JOURNAL day-letter 2026-09-18 (f) is on main -- audit journal_day_letters FAILs** - `audit.py::check_journal_day_letters` (floor 2026-07-30; letters are assigned once, at integration) returns `fail: duplicate JOURNAL day-letter(s) since 2026-07-30: 2026-09-18 (f)` on main (witnessed at `233294c0` and `7b585263`, 2026-09-19). The collision landed before night wave 2 and was not introduced by it. JOURNAL is append-only, so the fix is not an in-place re-letter of either landed entry. It is whatever the day-letter doctrine sanctions for a landed collision: an amendment marker, or a floor or exception entry in the check, recorded with its reason, as for the two pre-doctrine collisions the floor already excludes · Done when: `check_journal_day_letters` passes on main, and the disposition of the 2026-09-18 (f) pair is recorded (which entry keeps (f), and by what sanctioned mechanism the other is distinguished) without editing either entry's body · implements: night wave 2 integrator ruling 2026-09-19 · refs `scripts/audit.py` (`check_journal_day_letters`, `_JOURNAL_DAY_LETTER_FLOOR`), `JOURNAL.md` 2026-09-18
