---
id: "[#424]"
title: "Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#424] [P2][S] **Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare** — `scripts/validate_backlog.py:78` compiles `#(\d+)`, so `_parse_deps` returns `[]` for any clause lacking the hash. Census 2026-07-26: 8 clauses, **4 parse, 4 do not** — PARSED `L38 [#112] '#23'`, `L64 [#169] '#171'`, `L238 [#271] '#270'`, `L240 [#348] '#270'`; **INERT** `L47 [#389] '390'`, `L391 [#382] '381'`, `L395 [#383] '382'`, `L406 [#385] '383'`. The inert four are exactly the [E9] North-Star chain plus [#389], so the sequencing that preamble relies on is prose, not machinery. Normalizing bare refs changes dependency-graph behaviour (reference-existence + cycle detection start firing) and touches [#389], unrelated to [E9] — its own contract, not a text repair. · Done when: every `depends-on` clause parses, a regression test pins the bare-id form, and the `plugins/tier1-lifecycle` twin moves in lockstep · refs scripts/validate_backlog.py, tests/test_validate_backlog.py, #156, #206, #425 · kill-candidates: none — no open task owns the depends-on parser · serialize-group: audit-py
