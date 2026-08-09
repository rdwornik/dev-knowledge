---
id: "[#171]"
title: "Build the conformance dashboard at `ecosystem/conformance.md`"
status: open
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#171] [P3][M] Build the conformance dashboard at `ecosystem/conformance.md` (ADR-86 / ADR-85 R2) — a read-only validator generates it and commits its own output (ADR-80 committed-generated-zone writer policy); this is the deterministic surface #169's ungated-doc staleness signal lands in, and ARCHITECTURE Ch2 points to it. · Done when: `ecosystem/conformance.md` is generated + committed by a read-only validator (Layer-2-safe) and ARCHITECTURE Ch2 carries the pointer · refs docs/decisions/ADR-86-conformance-dashboard-location.md, ADR-80, ARCHITECTURE.md Ch2, #169 · UN-DEFERRED 2026-08-09 (ARC-2): peg "post-Wave-1 n=2 consumers" met 2026-07-07; un-blocks the [#169]/[#322] chain
