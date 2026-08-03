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

- [#424] [P2][S] **Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare** — `scripts/validate_backlog.py:78` compiles `#(\d+)`, so `_parse_deps` returns `[]` for any clause lacking the hash. Census: the recorded 8 clauses / 4 inert was stale; **live 2026-08-03 it was 7 / 3 inert**, and this arc's [#383] `382` edge removal leaves **6 clauses, 4 parse, 2 inert** — PARSED `[#112] '#23'`, `[#169] '#171'`, `[#271] '#270'`, `[#348] '#270'`; **INERT** `[#389] '390'`, `[#385] '383'`. The inert four are exactly the [E9] North-Star chain plus [#389], so the sequencing that preamble relies on is prose, not machinery. Normalizing bare refs changes dependency-graph behaviour (reference-existence + cycle detection start firing) and touches [#389], unrelated to [E9] — its own contract, not a text repair. · Done when: every `depends-on` clause parses, a regression test pins the bare-id form, and the `plugins/tier1-lifecycle` twin moves in lockstep · refs scripts/validate_backlog.py, tests/test_validate_backlog.py, #156, #206, #425 · kill-candidates: none — no open task owns the depends-on parser · serialize-group: audit-py
