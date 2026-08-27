---
id: "[#419]"
title: "We run routines whose output nobody consumes"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
depends-on: "#426"
generates: BACKLOG.md
---

- [#419] [P2][M] **We run routines whose output nobody consumes** — the nightly conformance routine emits a digest nightly and nobody reads it. Operator's framing: how routine output reaches a decision, NOT branch cleanup (touch no branch). Rule + gate landed 07-26 (ADR-105); coverage pegged to [#426]. STAYS OPEN. · **AMENDED 2026-08-11** (operator ruling, Fork 3 / I-F3 — the absorb step becomes an organ by amending this row, so no fresh row is born) · Done when: `routine_consumers` reports zero routines missing `consumer:` or `consumption_path:` within its stated coverage; unconsumed output is reported by a detector rather than silently accumulating; and for the nightly conformance routine specifically — (i) the absorb has a trigger that fires without an operator remembering, (ii) a detector reports queue depth (the count of unmerged `claude/conformance-*` branches) at a surface the operator already reads, and (iii) a scheduler-run check distinguishes a night with no run from a night whose output went unabsorbed — each of (i)–(iii) proven by a test · refs #270, #271, #348, #409, #410, #411, ADR-80, the five conformance branches · kill-candidates: none — #270 gauges operator LOAD, not whether output is ever read · serialize-group: settings-json · depends-on: #426
