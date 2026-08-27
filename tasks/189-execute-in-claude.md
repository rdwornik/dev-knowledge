---
id: "[#189]"
title: "Execute in ~/.claude"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
generates: BACKLOG.md
---

- [#189] [P3][S] **Execute in ~/.claude** (runtime-config repo; queue-only here, per the #100 execute-elsewhere precedent) — a session-end `~/.claude` commit-check (hook or routine) that flags uncommitted config/safety drift (chronic uncommitted `~/.claude` changes are the recurring failure). The methodology-reach question (should ecosystem enforcement own this?) is decided in #153. · Done when: a session-end check surfaces uncommitted `~/.claude` config/safety drift · refs #153, #100 (execute-elsewhere precedent), ~/.claude/rules · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
