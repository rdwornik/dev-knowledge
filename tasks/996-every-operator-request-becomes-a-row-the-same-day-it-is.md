---
id: "[#996]"
title: "Every operator request becomes a row the same day it is made -- a boot-time count, target 0"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#996] [P2][M] **Every operator request becomes a row the same day it is made -- a boot-time count, target 0** - O-4c: 10 of 17 standing operator requests measured this window had no row or home at all (`docs/audits/2026-09-23-technical-handoff-readiness.md` §6), because nothing lists every RATIFICATION/ANSWER/DECLARE 'Operator:' item and checks it against the backlog · Done when: a check enumerates every RATIFICATION/ANSWER/DECLARE 'Operator:' item of the current window and reports which carry no citing row; the boot banner prints the count; the target is 0 uncited operator requests older than the day they were made · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-handoff-readiness.md` §6, `scripts/fleet_health.py` · kill-candidates: none -- no open row builds this same-day-citation check
