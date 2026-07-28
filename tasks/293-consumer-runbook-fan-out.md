---
id: "[#293]"
title: "Consumer runbook fan-out"
status: deferred
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---

- [#293] [P3][S] Consumer runbook fan-out — seed each consumer repo's `docs/handoffs/README.md` from the hub canonical source via `python scripts/seed_runbook.py --target-root <repo>` (the DEFERRED half of #164 leg b — the hub-side seeder + hermetic test shipped with #164; operator ruling deferred the fan-out because the don't-touch-consumers guardrail bars a hub write into a consumer tree and the ai-council pilot is live in parallel). Executes per-repo in the Wave-1/Wave-2 onboarding arcs (ADR-41 — consumer-side, queue-only here), same shape as [#282]. · Done when: each onboarded consumer carries the seeded runbook (per-repo tracked, n≥1 recorded) · refs scripts/seed_runbook.py, docs/handoffs/README.md, #164, #282, ADR-41 · DEFER — peg: Wave-1 onboarding
