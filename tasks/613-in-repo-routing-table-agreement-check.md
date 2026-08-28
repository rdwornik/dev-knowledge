---
id: "[#613]"
title: "In-repo routing table + L0 agreement check"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#613] [P2][M] **In-repo routing table + L0 agreement check** (packet-born 2026-08-28 under register ruling Z-G1; funded by the window's banked ledger) -- ruling **Z-G3 / A2** places the **authoritative** routing table **in-repo**: a table the hub cannot read is a table the hub cannot gate, which is the four-rival-dispatch-commands disease (register section V, ~30 consecutive seats) in a new costume. `L0` (`~/.claude/ROUTING.md`) may keep a **derived** copy, and an agreement check asserts the two match -- the shape `[#592]` already built, reused rather than reinvented. **BLOCKED-ON: operator path selection (P1).** The path is deliberately NOT decided and **no file is created until it is** -- selection gates this row's EXECUTION, not its filing. Both candidate paths recorded so the operator picks rather than authors: **(a)** `ecosystem/routing-table.yaml`, beside the machine-read fleet registries the audit layer already loads; **(b)** `protocols/ROUTING.md`, beside the doctrine it encodes and PLAYBOOK Ch8. · Done when: the operator selects a path; the authoritative table exists there; a check asserts L0 agreement and FAILs on divergence · refs protocols/STANDING_RULINGS.md Z-G3, #592
