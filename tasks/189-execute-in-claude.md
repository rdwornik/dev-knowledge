---
id: "[#189]"
title: "Execute in ~/.claude"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
source: BACKLOG.md
derived: true
---

- [#189] [P3][S] **Execute in ~/.claude** (runtime-config repo; queue-only here, per the #100 execute-elsewhere precedent) — a session-end `~/.claude` commit-check (hook or routine) that flags uncommitted config/safety drift (chronic uncommitted `~/.claude` changes are the recurring failure). The methodology-reach question (should ecosystem enforcement own this?) is decided in #153. · Done when: a session-end check surfaces uncommitted `~/.claude` config/safety drift · refs #153, #100 (execute-elsewhere precedent), ~/.claude/rules
