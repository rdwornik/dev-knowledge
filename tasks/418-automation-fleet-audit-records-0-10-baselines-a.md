---
id: "[#418]"
title: "`automation/fleet-audit` records 0–10 baselines a day, not one"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#418] [P2][S] **`automation/fleet-audit` records 0–10 baselines a day, not one** — the writer branch carries up to 10 commits on a single day (2026-07-10) and 0 on many others (none since 2026-07-16), so "the daily baseline" is neither daily nor singular. Causal chain — STRONG BUT UNINSTRUMENTED: `fleet_health.py` fires from BOTH a Windows Task Scheduler task (`\DevKnowledge\fleet-baseline`, 09:00, verified Ready) AND the SessionStart hook, both reaching `audit.py run`; its once-per-day throttle reads `logs/FLEET-HEALTH.md`, which is gitignored and therefore PER-WORKING-TREE — so every worktree and clone independently believes the baseline is stale and re-runs it. Nothing measures this today: the build's FIRST step is a controlled reproduction (instrument the triggers, count runs against commits), NOT a fix. · Done when: the multiplicity is reproduced under instrumentation AND a one-baseline-per-day contract is enforced, or the multiplicity is recorded acceptable with a reason · refs scripts/fleet_health.py, scripts/audit.py, .claude/settings.json, ADR-76, ADR-84, #417 · kill-candidates: none — no open task owns baseline cadence · serialize-group: audit-py
