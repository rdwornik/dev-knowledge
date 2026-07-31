---
id: "[#463]"
title: "win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since 2026-07-11 admission"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: environment
generates: BACKLOG.md
---

- [#463] [P2][S] **win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since 2026-07-11 admission** — fleet-audit deep review 2026-07-31 (the 98-commit `automation/fleet-audit` read): identical evidence on the 07-11 admission audit, every daily through 07-16, and today's baseline (`ecosystem/win-tooling/history/2026-07-31.md`): `config.yaml` not dot-prefixed (ADR-59) FAIL · VISION+ARCHITECTURE `last_reviewed 2026-07-11` predates their 07-12 edits FAIL · workspace sort settings absent WARN · not listed in `deployed-versions.yaml` (ADR-91) WARN. Consumer-repo work — ADR-41, queue-only here. · Done when: each of the four is fixed in win-tooling or recorded accept-with-reason, and the fleet baseline shows win-tooling green · refs ecosystem/win-tooling/history/2026-07-31.md, ADR-59, ADR-91 · kill-candidates: none — no open row names win-tooling · serialize-group: environment
