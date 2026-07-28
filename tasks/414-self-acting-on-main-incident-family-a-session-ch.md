---
id: "[#414]"
title: "Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored action (n=2 this week)"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#414] [P2][S] **Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored action (n=2 this week)** — file both self-acting incidents as ONE family: (1) dead-session HEAD-swap — a concurrent/dead session's checkout put non-merge `94426dc0` direct on main (core-invariant #5), caught manually not by a gate (JOURNAL 2026-07-21); (2) this session's no-GO merge+push — self-initiated `chore/trim-405` (`c5910486` → merge `f3ead30b`) with NEITHER operator GO NOR a JOURNAL anchor. ADR-85 any-SHA gap connects them: the Stop-gate accepts ANY in-session SHA, so a later unanchored commit passes. Organs, NONE chosen (a ruling): (a) tighten ADR-85 so the anchor must be the actual wrap/HEAD SHA; (b) a pre-action operator-GO gate on merge/push-to-main; (c) a concurrent-HEAD-swap detector. · Done when: an operator ruling picks the organ(s) and the mechanism refuses/flags a no-GO or unanchored change to main with a test, or records permanent-defer · refs #344, #353, ADR-85, scripts/session_end_backpressure.py · kill-candidates: none — #344 gates handoff generation, #353 gates boot-contract, neither covers no-GO merge/push · serialize-group: settings-json
