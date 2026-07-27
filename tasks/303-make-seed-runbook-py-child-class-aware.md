---
id: "[#303]"
title: "Make seed_runbook.py child-class-aware"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#303] [P2][S] Make seed_runbook.py child-class-aware (ADR-36 no-local-handoffs) — the leg-b seeder (scripts/seed_runbook.py, #164 leg b) unconditionally writes <target>/docs/handoffs/README.md, but ADR-36 children (corp-monorepo, and the class the #293 fan-out will hit) carry NO local docs/handoffs/ by contract — a literal seed creates the exact dir ADR-36 forbids. Same class as ai-council's G3 (hub resolved: "create docs/intake/ only"). Make the seeder read the target's handoff-locality class and either (a) seed intake guidance instead, or (b) skip + emit a documented "hub-handoff-only, nothing to seed" status, so the deferred fan-out (ADR-41) cannot silently create forbidden dirs. · Done when: a --check/seed run against an ADR-36 child skips-or-redirects (never writes docs/handoffs/) with a test, and the seeder encodes the ADR-36 child class · refs scripts/seed_runbook.py, ADR-36, #293, #164, docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md, corp-monorepo docs/intake/2026-07-10-runbook-gap-notes.md G10 · kill-candidates: #293 (the deferred fan-out this de-risks) · serialize-group: architecture
