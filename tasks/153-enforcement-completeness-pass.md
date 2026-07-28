---
id: "[#153]"
title: "Enforcement-completeness pass"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#153] [P2][M] Enforcement-completeness pass — move browser-re-stated constraints to CC-side mechanical enforcement (a rule the browser repeats each session is the symptom of a missing hook). The `--no-ff` FF-guard shipped (`no_ff_merges` WARN, hub-only) and the true-FF *prevention* pre-push gate too (`block-ff-push`, 2026-06-20, hub-only + bypassable). Remaining: server-side prevention teeth (the local hook is bypassable); mechanize-or-accept each of minimal-diffs / append-only (LESSONS/TOKEN-LOG/JOURNAL) / no-CHANGELOG-recreation; **define core-invariant #5's `--no-ff` scope boundary** (hub vs `~/.claude` vs child repos — which trees the rule binds); and decide the **methodology-reach question** — should ecosystem commit-discipline enforcement reach `~/.claude` at all, or is that the runtime-config repo's own concern (filed separately as the `~/.claude`-executed #189). · Done when: each remaining prose-only constraint is mechanized or recorded as accepted-prose-only with a reason, the #5 `--no-ff` scope boundary is defined, and the ~/.claude-reach question is decided · refs ~/.claude/rules/core-invariants.md #5, #189 · serialize-group: audit-py
