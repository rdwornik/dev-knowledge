---
id: "[#808]"
title: "A hung hook wedges its session with no record; every hook needs a bound that fails OPEN loudly"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#808] [P1][M] **A hung hook wedges its session with no record; every hook needs a bound that fails OPEN loudly** - Operator ruling 2026-09-16 (wave 1 of PLAN-2026-09-16-execution-order, batch AB lane 1). **Measured cost this week: ~14 h of wedged seats** -- the integrator twice (~6 h) and one lane at 8 h, every instance parked at "running PreToolUse hooks". **A guard that hangs is worse than one that is absent, because absence is visible.** Under `bypassPermissions`, which every lane uses, a `PreToolUse` exit 2 is one of the only two refusal channels, so the guard cannot simply be removed; it has to be bounded. `.claude/settings.json` already carries per-hook `timeout` values, and the wedges happened anyway, so the first act is to establish what that field actually bounds on this platform (Windows, POSIX-shell hook commands) before building beside it. · Done when: (1) RED-first: a test guard that sleeps past its bound is BYPASSED (the tool call proceeds) and the bypass is RECORDED to a durable, named surface with hook id, bound, elapsed time and session id -- a silent pass is a failure of this row; (2) every hook registered in `.claude/settings.json` carries an explicit bound, and a registration without one is refused by a check; (3) the record is surfaced at SessionStart, so a guard that keeps timing out is visible rather than quietly disarmed; (4) the fail-OPEN posture is stated per hook with its reason, and any hook that must fail CLOSED past its bound is named with a ruling, never by default · refs `.claude/settings.json`, `[#768]` (one refusal channel: a violation and an unevaluable environment look the same), `[#684]` (a guard's environment failure turned into total refusal), ARCHITECTURE Ch2 failure posture · kill-candidates: none -- `[#768]` is the refusal-channel shape; this row is the time bound · source: operator ruling 2026-09-16, batch AB manifest
