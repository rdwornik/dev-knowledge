---
id: "[#524]"
title: "Four ruled check extensions — the N2 set, Codex-produced"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#524] [P2][S] **Four ruled check extensions — the N2 set, Codex-produced** — the 2026-08-12 adjudication approved four extensions to **existing** organs (no new organ family), producer = **Codex, CC verifies** (register L-10, the step-12 routing); ARC2 landed the records and built none of it. Legs, in Done-when order: `N2-E4-02` (a), `N2-E4-03` (b), `N2-L5` (c), `N2-L12` (d). Leg (c) is a **WARN by design** — it catches the shape, not the intent. A leg recorded-with-a-reason lands at its G-6 home, `protocols/STANDING_RULINGS.md`. · Done when: (a) `audit.py health` REDs on a seeded duplicate JOURNAL day-letter and passes on a contiguous run (3 tests); AND (b) `validate_backlog` WARNs on a past body-date and is silent on a future one (2 tests); AND (c) `journal_anchor` WARNs "anchored by mention, not by record" on the seeded shape; AND (d) `check_hooks_armed` asserts the **pre-push** hook type (1 test) · refs STANDING_RULINGS L-10, ADR-85 · kill-candidates: none — [#424]/[#425] own the depends-on parser and its fixture coverage; neither covers these four organs · serialize-group: audit-py
