---
id: "[#293]"
title: "Consumer runbook fan-out"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---

- [#293] [P3][S] Consumer runbook fan-out — seed each consumer repo's `docs/handoffs/README.md` from the hub canonical source via `python scripts/seed_runbook.py --target-root <repo>` (the DEFERRED half of #164 leg b — the hub-side seeder + hermetic test shipped with #164; operator ruling deferred the fan-out because the don't-touch-consumers guardrail bars a hub write into a consumer tree and the ai-council pilot is live in parallel). Executes per-repo in the Wave-1/Wave-2 onboarding arcs (ADR-41 — consumer-side, queue-only here), same shape as [#282]. · Done when: each onboarded consumer carries the seeded runbook (per-repo tracked, n≥1 recorded) · refs scripts/seed_runbook.py, docs/handoffs/README.md, #164, #282, ADR-41 · UN-DEFERRED 2026-08-09 (ARC-2): peg "Wave-1 onboarding" met 2026-07-07; work NOT done (0 of 6 consumers seeded), so un-defer not close · **DENOMINATOR RULED at phase-1 integration (R6): 8, not 6** — ADR-104's declared non-hub members; governance outranks row prose, so read "0 of 6" above as **0 of 8**. Lane Q merged `dce393ec` and advanced this row BY ZERO by design (contract line-3 STOP: the Done-when needs consumer-repo writes nothing authorised). **Seeding stays OPERATOR-GATED, not executed** · see the phase-1 integration packet · **LANE k 2026-08-16: operator word given, 7 of 8 seeded** — per-repo worktree/branch → PR (RULING-W shape; never the live checkout), none merged (each consumer's own merge discipline governs integration): corp-monorepo#54, corp-ops#1, corp-sca-time-automation#1, demo-prep#1, life-architect#1, terminal-setup#1, win-tooling#1 · ai-council STOP-and-report — its own `validate-docs-registry` pre-commit hook refuses an unregistered `docs/handoffs/` corpus; unblocks once ai-council's own maintainer registers it in its `docs/audits/README.md` Live-corpora table, no hub-side fix invented · row stays OPEN pending the 7 PR merges + ai-council · see the lane-k packet
