---
id: "[#162]"
title: "Vocab decision"
status: open
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S1] Match the handoff payload to the work mode"
serialize-group: handoff
source: BACKLOG.md
derived: true
---

- [#162] [P2][M] Vocab decision (architect-session): disambiguate "architect" as the Layer-1 **actor** (ARCHITECTURE.md / ADR-28 — the browser-chat role) vs the handoff **mode** (HANDOFF_PROCESS.md §13 / HANDOFF_BOOT — architect|execution). Enumerate every surface where each sense appears and decide the disambiguation atomically (rename one sense, or formally scope both — do not leave the collision live). The boot-ack narrow slice shipped 2026-06-11 (HANDOFF_BOOT.md ack → "Layer-1 browser", no on-load mode claim); the model decision remains. · Done when: an ADR or operator ruling lands the disambiguation across all enumerated surfaces · refs ADR-28, protocols/HANDOFF_BOOT.md, protocols/HANDOFF_PROCESS.md §13, ARCHITECTURE.md Ch1 · serialize-group: handoff
