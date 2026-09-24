---
id: "[#1006]"
title: "Boot banner stops printing re-armed hooks as 'DECLARED BROKEN'"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1006] [P2][S] **Boot banner stops printing re-armed hooks as 'DECLARED BROKEN'** - S2 proposed row 6: seven re-armed hooks are printed "DECLARED BROKEN" at every boot because `logs/HOOK-BYPASSES-BROKEN.json` was never reconciled with the 2026-09-22/23 re-arm (`docs/audits/2026-09-23-technical-hook-architecture-appendix.md` A6 item 6) · Done when: no hook is printed DECLARED BROKEN while settings arm it with a PASS record newer than the declaration; the declarations file and the settings `//` register read from one record ([#888]'s DEGRADED record, or a reconciling check); the seven stale declarations are reinstated · implements: ADR-120 · refs `scripts/fleet_health.py`, `logs/HOOK-BYPASSES-BROKEN.json`, `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `[#888]` · kill-candidates: none -- no open row reconciles the banner with the re-arm
