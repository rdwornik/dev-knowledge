---
id: "[#389]"
title: "Prompt-lint — gate the five architect fields before a lane runs"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
depends-on: "390"
source: BACKLOG.md
derived: true
---

- [#389] [P2][S] **Prompt-lint — gate the five architect fields before a lane runs** — the ADR-87 contract (architect emits intent · closure · anti-patterns · MODE · governance-pointer) is advisory prose today: a prompt missing its pointer or its MODE basis runs anyway, surfacing only as a mid-lane wrong turn. Gate it — validate the five fields present, MODE carrying its *basis* (ADR-87 item 5), refuse/WARN on a miss. Honest limit up front: an **off-repo** prompt pasted into a browser cannot be gated by a repo hook — the R6 hard-probe-vs-soft-check question ([E8] W6, **UNRULED**); rule R6 first, or scope to surfaces a hook reaches. · Done when: R6 is ruled AND a seeded prompt missing a required field is refused/WARNed, with tests, OR recorded permanent-defer-with-reason · refs ADR-87 §5 §7, docs/audits/2026-07-19-technical-night-s7-prompt-authoring-quality.md §4, #185, #390 · kill-candidates: none — guard-to-gate conversion of the ADR-87 contract; #185 is GAP-2 (execution-time gotchas), not the prompt-field contract · depends-on: 390 · serialize-group: audit-py
