---
id: "[#185]"
title: "GAP-2 deterministic gotcha-injection guard"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#185] [P2][M] GAP-2 deterministic gotcha-injection guard — a read-only PreToolUse guard that injects the matching gotcha when a commit-message / Edit-deletion pattern is about to fire (the execution-time micro-decision class that recurred n=2/n=3 even with the standing "check gotchas" line; prose can't fix it, a deterministic backstop can). Orthogonal to the ADR-87 prompt contract (ADR-87 closes the governance/read-only load gaps GAP-1/GAP-3, not GAP-2). Sibling of the #105/#112 PreToolUse guards. · Done when: a seeded commit-message / Edit-deletion pattern triggers injection of the matching gotcha (read-only, fail-soft), with tests · refs ADR-87, #105, #112, gotchas skill
