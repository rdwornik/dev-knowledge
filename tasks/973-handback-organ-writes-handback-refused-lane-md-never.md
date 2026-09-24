---
id: "[#973]"
title: "Handback organ writes `HANDBACK-REFUSED-<lane>.md`, never the integrator's own `REFUSED-<lane>.md`"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#973] [P1][S] **Handback organ writes `HANDBACK-REFUSED-<lane>.md`, never the integrator's own `REFUSED-<lane>.md`** - D10: the handback organ wrote `REFUSED-<lane>.md`, the same name the integrator's own repair-order path uses, and overwrote one once, because no transport schema names which writer owns which filename · Done when: the handback organ writes `HANDBACK-REFUSED-<lane>.md` exclusively; a transport-adapter check (built alongside D19's registry) enforces that only the integrator writes bare `REFUSED-<lane>.md`; a witness run shows no filename collision between the two writers · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `to-cc/BATCH-WAVE5A-2026-09-23.md` (dispatcher rule 5, repairs read `REFUSED-<slug>.md` only from the integrator) · kill-candidates: none -- no open row names this collision or its fix
