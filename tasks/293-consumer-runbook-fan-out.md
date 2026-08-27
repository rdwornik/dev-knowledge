---
id: "[#293]"
title: "Consumer runbook fan-out"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
depends-on: "#303"
generates: BACKLOG.md
---

- [#293] [P3][S] Consumer runbook fan-out — seed each consumer repo's `docs/handoffs/README.md` from the hub canonical source via `python scripts/seed_runbook.py --target-root <repo>` (the DEFERRED half of #164 leg b). UN-DEFERRED 2026-08-09 (ARC-2). **DENOMINATOR RULED at phase-1 integration (R6): 8, not 6** — ADR-104's declared non-hub members; governance outranks row prose. **Row BLOCKED-ON-RULING since lane k (2026-08-16):** operator word was given and seeding executed 7 of 8 via per-repo PRs, then REVERTED IN FULL — ADR-60 forbids a child repo carrying a local `docs/handoffs/`, the exact target this row's own prose names, and the architect ruled ADR-60 wins over a task row's stated path. Nothing was lost and every consumer verified clean; what is open is the correct consumer-side home, and `[#303]` — this row's own named prerequisite — must land first. Seeding stays OPERATOR-GATED. · Done when: each onboarded consumer carries the seeded runbook (per-repo tracked, n≥1 recorded) · refs scripts/seed_runbook.py, docs/handoffs/README.md, #164, #282, #303, ADR-41, ADR-60 · source: docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md, which carries the 7 PR numbers, the revert evidence and the two candidate homes in full · depends-on: #303
