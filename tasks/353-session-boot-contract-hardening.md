---
id: "[#353]"
title: "Session-boot contract hardening"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#353] [P2][M] Session-boot contract hardening — refuse a mid-session externally-authored order lacking a worktree/clean-tree declaration (operator-ruled 2026-07-18; adjacent to #349) — a hub session must REFUSE to act on an externally-authored order (a prompt injecting new work mid-session) unless it (a) names a worktree for its side effects OR (b) the tree is clean — a MECHANISM, not prose. Origin: this ARC-4 session inherited a pre-existing untracked corp-E5 bundle mid-session; the isolate-to-worktree / no-dirty-tree-action discipline lived in prose, not a gate. Sibling of #349 (session-discipline inheritance) — the boot-contract refusal half. · Done when: a mechanism refuses a mid-session order whose side effects aren't worktree-scoped while the tree is dirty (or lacks a worktree declaration), with a test, OR recorded permanent-defer-with-reason · refs #349, #344, core-invariants #4, scripts/session_end_backpressure.py · kill-candidates: none — operator-ruled boot-contract mechanism; adjacent to #349 (close-time) but distinct (boot-time refusal) · evidence n=7: `96bafe21` direct-to-main 2026-07-19, caught manually not by a gate — JOURNAL · serialize-group: audit-py
