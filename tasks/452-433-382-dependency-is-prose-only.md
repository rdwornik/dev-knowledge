---
id: "[#452]"
title: "`[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only — no `depends-on` clause exists"
status: retired
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#452] [P3][S] **`[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only — no `depends-on` clause exists** — the pilot-precedes-contract ruling makes [#433] sequence before [#382], and ADR-107 carries it as a named obligation, but the relationship is written **only** as prose plus a bare `refs #382`. Verified 2026-07-31: **neither `tasks/433-*` nor `tasks/382-*` carries a `depends-on` clause at all**, so no parser sees the edge and no gate can enforce the ordering. **Distinct from [#424]**, which owns clauses that EXIST but fail to parse; a clause never written passes its Done-when ("every `depends-on` clause parses") untouched. Same family — sequencing in prose not machinery — different sub-case. Open: add the clause, or record that ADR-carried obligations are deliberately outside the dependency graph. · Done when: the pair is either expressed as a parseable `depends-on` clause or recorded as intentionally prose-carried, and [#424]'s scope note distinguishes absent clauses from unparsable ones · refs tasks/433, tasks/382, #424, ADR-107 · kill-candidates: none — [#424] owns unparsable clauses, not absent ones · serialize-group: audit-py

**RETIRED 2026-08-12 — operator ruling (adjudication hour; register `protocols/STANDING_RULINGS.md` M-7 / `N2-R1-07`).** The 2026-08-10 census named this **the one genuine kill candidate** in the DEFECTIVE-8 set, and the reason is structural rather than editorial: the dependency this row tracks is `[#433]`→`[#382]`, and **both of those rows are `status: closed`**. A `depends-on` edge between two closed rows enforces an ordering that can no longer be violated, so writing the clause would add a parseable statement of a constraint with nothing left to constrain. **Nothing is lost, and that is what makes this a retire rather than a deferral:** the generalisable obligation behind the row — that a landing predicate is expressed as a parseable clause rather than carried in prose — survives at **`[#513]`**, whose amended Done-when (a) *is* a landing-predicate check. **Kill note pegs to `[#513]`.** This file remains on disk as the ADR-107 §6.3 allocation record that keeps the id `[#452]` spent and un-reissued.
