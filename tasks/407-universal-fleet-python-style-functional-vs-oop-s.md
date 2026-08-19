---
id: "[#407]"
title: "Universal fleet Python style — functional-vs-OOP stance + uniform naming (the paradigm/naming half of parity)"
status: closed
priority: P3
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: playbook
generates: BACKLOG.md
---

- [#407] [P3][M] **Universal fleet Python style — functional-vs-OOP stance + uniform naming (the paradigm/naming half of parity)** — one fleet-wide way of producing code: a functional-vs-OOP stance ruled once, plus uniform naming for classes / files / objects / variables — a universal Python-delivery methodology improvable BECAUSE it is universal. The 2026-07-19 ruff/pytest parity covered TOOLING only (lint + test config); the paradigm + naming half is unfiled. Filing only, zero build — the stance is an operator ruling, not a CC pick. · Done when: an architect ruling (ADR-108 §A; re-routed) records the functional-vs-OOP stance AND a uniform naming convention (classes/files/objects/variables) is documented as fleet doctrine, or recorded deferred-with-reason · refs 2026-07-19 ruff/pytest parity arc, PLAYBOOK, ADR-51 · kill-candidates: none — no open task owns the code paradigm/naming half of fleet parity · serialize-group: playbook · RULED 2026-08-19 (architect L-5 block, transcribed by the S-1 seat): fleet Python doctrine is **functional-first with dataclasses; classes only for stateful lifecycles; naming = PEP 8**. Filed as an in-file AMENDMENT to ADR-108 (section §B-4) — the row's own re-routed home — landed at `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md`, arming no gate and binding prospectively · CLOSED 2026-08-19 — both Done-when limbs discharged: the stance is ruled AND the naming convention is documented as fleet doctrine
