---
id: "[#122]"
title: "Retire the PATH shim"
status: closed
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#122] [P3][S] Retire the PATH shim (`claude.cmd`) — the native settings.json `env` route (empty `ANTHROPIC_API_KEY`) is primary since 2026-06-06 and covers all launch paths; the shim is now redundant. Sentinel stays as a tripwire; removal needs an explicit operator ask per the no-delete invariant · Done when: the operator approves and the shim is removed (or the item is closed as keep-for-defence-in-depth) · refs docs/audits/2026-06-07-platform-max-audit.md UN-1 · TRANSCRIBED 2026-08-19 (architect L-5 block, S-1 seat) — **HELD, not closed**: the remove-vs-keep call is the operator's one word, and the architect RECOMMENDS **keep-for-defence-in-depth**. The row's own Done-when already requires the operator (*"the operator approves and the shim is removed, or the item is closed as keep-for-defence-in-depth"*), and the no-delete invariant makes the removal branch unavailable without an explicit ask, so this row stays OPEN and closes on the operator's word alone. It is the ONE of the eight L-5 rulings that did not discharge its row · **OPERATOR WORD 2026-08-19: KEEP-for-defence-in-depth.** The architect's L-5 block held this row for the one call it could not make, and the operator has made it: the PATH shim (`claude.cmd`) STAYS as a tripwire beside the native `settings.json` `env` route, and is NOT removed. The Done-when's second branch — *"or the item is closed as keep-for-defence-in-depth"* — is therefore the one that discharges, and the no-delete invariant is never reached because nothing is deleted · CLOSED 2026-08-19 — the last of the eight L-5 rulings to reach a terminal state
