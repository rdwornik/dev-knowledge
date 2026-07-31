---
id: "[#463]"
title: "win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since admission"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: environment
generates: BACKLOG.md
---

- [#463] [P2][S] **win-tooling onboarding debt — 2 FAILs + 2 WARNs unchanged since admission** — fleet-audit deep review: identical evidence from the 2026-07-11 admission audit through today's baseline (`ecosystem/win-tooling/history/`): `config.yaml` not dot-prefixed (ADR-59) FAIL · VISION+ARCHITECTURE edited the day after review, never re-reviewed FAIL · workspace sort settings absent WARN · absent from `deployed-versions.yaml` (ADR-91) WARN. Consumer-repo work — ADR-41, queue-only here. · Done when: each of the four is fixed in win-tooling or recorded accept-with-reason, and the fleet baseline shows win-tooling green · refs ecosystem/win-tooling/history/, ADR-59, ADR-91 · kill-candidates: none — no open row names win-tooling · serialize-group: environment
