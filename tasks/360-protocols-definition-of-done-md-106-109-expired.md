---
id: "[#360]"
title: "`protocols/DEFINITION_OF_DONE.md:106-109` expired in place"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#360] [P3][S] **`protocols/DEFINITION_OF_DONE.md:106-109` expired in place** — the `## Scope-freeze` clause froze the gate's doc set "for 4 weeks from ADR-85 (i.e. until ~2026-07-14)"; that window elapsed before the census HEAD (2026-07-19) with no successor clause, so a clause that still reads as binding has silently lapsed. Routes to W6. (The lane prompt cited this as `protocols/...:509`; the verified location is `DEFINITION_OF_DONE.md:106-109` — that file is 123 lines, and `PLAYBOOK.md:509` is the unrelated two-tier rider.) · **CONVERTED TO A DATED REVIEW 2026-09-09** (2026-08-10, operator input I-1 on the seat-27 checklist; register `protocols/STANDING_RULINGS.md` I-I1): **the author's original intent is unrecoverable** — the operator confirms it, the `file:line` referent has drifted, and searching does not recover it. So the row is not reconstructed; on the review date it is decided on its face. Date chosen as the repo's own 30-day review cadence (`canonical_freshness_gate.FRESHNESS_CADENCE_DAYS`) from the ruling date, the operator having named no date; row status unchanged · Done when: on the review date the freeze is lifted, renewed with a new window, or recorded expired-with-reason · refs protocols/DEFINITION_OF_DONE.md, ADR-85 · kill-candidates: none — an expired-in-place clause; no open task covers the ADR-85 scope freeze · serialize-group: audit-py
