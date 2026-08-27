---
id: "[#579]"
title: "Code doctrine & FDD — one ADR merging intakes #31 and #34 (packet ARC-A)"
status: open
priority: P1
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
depends-on: "#153"
generates: BACKLOG.md
---

- [#579] [P1][L] **Code doctrine & FDD — one ADR merging intakes #31 and #34 (packet ARC-A)** — Two intakes (#31 code style, #34 architecture enforcement) are answered by ONE ADR carrying all five decisions, so the fleet stops having two half-answers and no ruling. · Full body as born (nothing deleted, relocated for D-2): `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: one ADR reads `Accepted` and carries all five decisions (style, ruff selection, complexity ceiling, import-linter contract, mypy), intake #31 and intake #34 each carry a terminal `status:` with `decided-by`, the §D hotspot measurement is recorded before any refactor row is filed, and every rule the ADR states either names its enforcing gate or is explicitly recorded as judgment-only · refs docs/audits/2026-08-25-technical-register-ruling-packet.md §3 ARC-A, protocols/STANDING_RULINGS.md section U, docs/intake/2026-08-09-func-code-style-doctrine.md, docs/intake/2026-08-16-code-architecture-enforcement.md, ADR-108 §B, ADR-111 · source: packet row C22+C23 (ARC-A), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — no open row owns code-level style or architecture doctrine; `[#146]` and `[#153]` CONSUME such an ADR rather than produce it · depends-on: #153
