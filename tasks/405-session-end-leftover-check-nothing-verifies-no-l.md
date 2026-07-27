---
id: "[#405]"
title: "Session-end leftover check — nothing verifies \"no leftovers\""
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#405] [P2][S] **Session-end leftover check — nothing verifies "no leftovers"** — cleanup failed 3x the 2026-07 arc (scaffold branch, empty `.claude/worktrees/`, report-only cleanup): `session_end_backpressure.py` checks JOURNAL/BACKLOG but NO organ checks worktree/branch hygiene — leftover worktrees, undeleted merged branches, stale `.git/worktrees/` metadata, dead-pid locks, orphan dirs (CLAUDE.md §5 rule 9 is prose-only here). **RULED 2026-07-25 — organ (a): a hygiene leg in the `session_end_backpressure` Stop hook.** Not (b) a ship-gate leg (fires at merge — too late to stop a leftover leaving the session); not (c) a SessionStart reporter (surfaces the NEXT session's mess). Ruling only; build + test is a separate arc landing with or after [#417] — a leg on a gate that already fires daily on non-work compounds the bypass it trains. · Done when: the Stop-hook hygiene leg flags each named leftover class with a test · refs scripts/session_end_backpressure.py, CLAUDE.md §5 rule 9, PLAYBOOK "No leftovers", ADR-85, #344, #417 · kill-candidates: none — no open task owns session-end worktree/branch hygiene (#344 gates handoff generation, not teardown) · serialize-group: settings-json
