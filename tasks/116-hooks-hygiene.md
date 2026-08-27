---
id: "[#116]"
title: "Hooks hygiene"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#116] [P3][S] Hooks hygiene — `shell:"powershell"` + `args:[]` exec-form migration: replace wrapper-string invocations on our PowerShell hooks with the array exec-form to kill the Windows quoting failure class; note the `.cmd` shim caveat (per the hooks doc); also adopt `if:` conditional filters on PreToolUse guards to scope spawn overhead · Done when: our PS hooks use exec-form `args:[]` and at least one PreToolUse guard carries an `if:` scope filter · refs docs/audits/2026-06-07-platform-max-audit.md UN-5/UN-6 · serialize-group: settings-json · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
