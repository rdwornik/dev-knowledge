---
id: "[#188]"
title: "Deny-rule + hook completeness audit"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#188] [P3][M] Deny-rule + hook completeness audit — a read-only pass enumerating every PreToolUse guard / `permissions.deny` glob / pre-commit hook against the zones they should cover (ADR-75 register), surfacing uncovered zones + bypassable globs (a coverage matrix). Distinct from #132's organ *inventory* — this is a coverage *gap* audit. · Done when: a read-only pass emits a coverage matrix flagging any zone/path lacking a guard · refs #112, #185, #132, ADR-75, ADR-77 · DEFER — peg: #112 arc landed · **RE-PEGGED 2026-08-27** (X1 step 3, night-harvest governance session) — peg `#112` verified: `[#112]` was adjudicated this session against the C4 top-40 (census row 40) and **HELD** — the `adr_amend` sanctioned-writer mechanism it names does not exist, so the row is un-started rather than overtaken. The peg RESOLVES; this row is not orphaned.
