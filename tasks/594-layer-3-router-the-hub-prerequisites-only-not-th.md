---
id: "[#594]"
title: "Layer-3 router — the HUB prerequisites only, not the verb itself"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: architecture
depends-on: "#582"
generates: BACKLOG.md
---

- [#594] [P3][M] **Layer-3 router — the HUB prerequisites only, not the verb itself** — Making `dispatch` a real router is win-tooling's act; this row owns only what the hub must supply first — the contract schema and the substrate registry the router reads. Scoped deliberately narrow so it cannot schedule work in an operator-owned repo. · Done when: the substrate registry has ONE home that both the layer-2 validator and any future router read (no second copy), the contract `Substrate:` field is schema-declared rather than conventional, the hub-side half is demonstrably consumable by a router that does not yet exist, and PLAYBOOK Ch8 states the LOCAL-ONLY limitation in the same sentence that names the verb until the router lands · refs docs/intake/2026-08-26-tech-dispatch-consolidation-remainder.md (intake #52), protocols/STANDING_RULINGS.md section V (V1, V7), scripts/gen_lane_contract.py, #582 · source: intake #52 (I4), the LAYER-3 act — third of three, hub prerequisites only · kill-candidates: none — `[#582]`'s ARC consumes this schema; the two are ordered, not duplicated · serialize-group: architecture · depends-on: #582
