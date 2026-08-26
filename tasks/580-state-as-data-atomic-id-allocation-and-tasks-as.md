---
id: "[#580]"
title: "State-as-data: atomic id allocation, and `tasks/` as the SOLE source (packet ARC-B)"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#580] [P1][M] **State-as-data: atomic id allocation, and `tasks/` as the SOLE source (packet ARC-B)** — Id allocation is `max+1` over a hand-edited manifest, so two concurrent lanes can allocate the same id; state becomes data and `tasks/` becomes the sole source in fact, not only in ADR-107's wording. · Full body as born (nothing deleted, relocated for D-2): `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: allocating an id and filing a row require no hand edit of `tasks/manifest.json`, two concurrent allocations cannot yield the same id (shown by a test that fails against today's `max+1`), the C09 fork is recorded as decided with its reason, and ADR-107's schema statement either carries `SOLE` or is amended to say what it actually means · refs docs/audits/2026-08-25-technical-register-ruling-packet.md §3 ARC-B, protocols/STANDING_RULINGS.md section U, ADR-107, ADR-109, scripts/gen_task_tree.py, tasks/manifest.json, #429, #433 · source: packet row C08+C09 (ARC-B), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — no open row carries id allocation; `[#523]` renders a view over the GENERATED file and touches no allocation path · serialize-group: architecture
