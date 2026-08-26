---
id: "[#582]"
title: "Substrate router — one gated enum, a capability-keyed table, and the generator that reads it (packet ARC-D)"
status: open
priority: P1
size: L
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: architecture
generates: BACKLOG.md
---

- [#582] [P1][L] **Substrate router — one gated enum, a capability-keyed table, and the generator that reads it (packet ARC-D)** — Nothing declares which of three substrates a lane runs on; a contract's Substrate line stays documentation until a gated enum, a capability-keyed table and a generator that READS it replace prose. · Full body as born: `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: one ADR extends `SHAPE_ENUM` with generator, hook and routing table moving in a single commit, `gen_lane_contract` derives substrate and command from the capability-keyed table rather than from prose, the four capability keys are populated from the three declared sources, the per-provider status block is generated and freshness-gated across all six providers, and every routing number the ADR cites is measured with its command recorded · refs docs/audits/2026-08-25-technical-register-ruling-packet.md §3 ARC-D + addendum, STANDING_RULINGS section U, docs/intake/2026-08-24-tech-substrate-router.md, #554, #568 · source: packet row C30+C31+C32 plus the D-vis addendum (ARC-D), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — `[#554]` built the devcontainer this routes to, `[#568]` owns the config D-vis reads; both are inputs · serialize-group: architecture
