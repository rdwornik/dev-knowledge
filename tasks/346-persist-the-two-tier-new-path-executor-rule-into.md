---
id: "[#346]"
title: "Persist the two-tier new-path executor rule into `~/.claude`"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: claude-md
generates: BACKLOG.md
---

- [#346] [P2][S] Persist the two-tier new-path executor rule into `~/.claude` (durability) — the proceed-with-citation-vs-STOP AGENT behavior (pattern-sanctioned: derive+cite+proceed; unsanctioned/ambiguous/new-folder: STOP) is **already in force** (ADR-101 two-tier amendment, operator ruling — NOT gated on this task). Persist it into `~/.claude` with a `verify:` line so future sessions inherit it without reading the ADR (CLAUDE.md §5 rule 7). The `~/.claude` EDIT is global-infra (core-invariant #6) → the edit needs its own operator ruling; the behavior does not. Sibling of the #189/#153 `~/.claude`-reach question. · Done when: the `~/.claude` executor rule lands under an explicit ruling with a `verify:` line, OR is recorded permanent-defer-with-reason · refs ADR-101 §3, CLAUDE.md §5 rule 7, core-invariants #6, #189, #153 · kill-candidates: none — persists the ADR-101 amendment's executor behavior; a `~/.claude` edit, none owns it · serialize-group: claude-md
