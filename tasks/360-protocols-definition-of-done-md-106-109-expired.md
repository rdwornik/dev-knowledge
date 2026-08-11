---
id: "[#360]"
title: "`protocols/DEFINITION_OF_DONE.md` `## Scope-freeze` expired in place"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#360] [P3][S] **`protocols/DEFINITION_OF_DONE.md` `## Scope-freeze` expired in place** — the `## Scope-freeze` clause froze the gate's doc set "for 4 weeks from ADR-85 (i.e. until ~2026-07-14)"; that window elapsed before the census HEAD (2026-07-19) with no successor clause, so a clause that still reads as binding has silently lapsed. Routes to W6. (Locator history, kept because it is the row's own drift record: the lane prompt cited `protocols/...:509`; the row then carried `DEFINITION_OF_DONE.md:106-109`, correct when the file was 123 lines. **That line range is now stale** — the file is 185 lines and `## Scope-freeze` sits at :168, so lines 106-109 hold unrelated text. `PLAYBOOK.md:509` was always the unrelated two-tier rider.) · **RE-ANCHORED 2026-08-11** (operator ruling; the 2026-09-09 dated review is WITHDRAWN): **I-1 superseded by census evidence; operator informed.** Input I-1 recorded the author's intent as unrecoverable; the 2026-08-10 backlog-testability census **refuted that** by locating the referent — `protocols/DEFINITION_OF_DONE.md` **`## Scope-freeze`**, which reads *"No docs are added to this gate for 4 weeks from ADR-85 (i.e. until ~2026-07-14)"*. That is a freeze, with a window, which expired and still stands verbatim — precisely "expired in place", and it fits this row's Done-when and nothing else in the file. **The row is anchored to the `## Scope-freeze` heading, not to a line number**, so it cannot drift again (the citation convention 3b-4). Evidence: `docs/audits/2026-08-10-technical-backlog-testability-census.md` §3 · Done when: the `## Scope-freeze` clause is lifted, renewed with a new window, or recorded expired-with-reason · refs protocols/DEFINITION_OF_DONE.md, ADR-85 · kill-candidates: none — an expired-in-place clause; no open task covers the ADR-85 scope freeze · serialize-group: audit-py
