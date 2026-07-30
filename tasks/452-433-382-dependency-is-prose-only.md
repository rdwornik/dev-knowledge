---
id: "[#452]"
title: "`[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only — no `depends-on` clause exists"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#452] [P3][S] **`[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only — no `depends-on` clause exists** — the pilot-precedes-contract ruling makes [#433] sequence before [#382], and ADR-107 carries it as a named obligation, but the relationship is written **only** as prose plus a bare `refs #382`. Verified 2026-07-31: **neither `tasks/433-*` nor `tasks/382-*` carries a `depends-on` clause at all**, so no parser sees the edge and no gate can enforce the ordering. **Distinct from [#424]**, which owns clauses that EXIST but fail to parse; a clause never written passes its Done-when ("every `depends-on` clause parses") untouched. Same family — sequencing in prose not machinery — different sub-case. Open: add the clause, or record that ADR-carried obligations are deliberately outside the dependency graph. · Done when: the pair is either expressed as a parseable `depends-on` clause or recorded as intentionally prose-carried, and [#424]'s scope note distinguishes absent clauses from unparsable ones · refs tasks/433, tasks/382, #424, ADR-107 · kill-candidates: none — [#424] owns unparsable clauses, not absent ones · serialize-group: audit-py
