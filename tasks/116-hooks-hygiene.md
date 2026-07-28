---
id: "[#116]"
title: "Hooks hygiene"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#116] [P3][S] Hooks hygiene — `shell:"powershell"` + `args:[]` exec-form migration: replace wrapper-string invocations on our PowerShell hooks with the array exec-form to kill the Windows quoting failure class; note the `.cmd` shim caveat (per the hooks doc); also adopt `if:` conditional filters on PreToolUse guards to scope spawn overhead · Done when: our PS hooks use exec-form `args:[]` and at least one PreToolUse guard carries an `if:` scope filter · refs docs/audits/2026-06-07-platform-max-audit.md UN-5/UN-6 · serialize-group: settings-json
