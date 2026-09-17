---
id: "[#592]"
title: "Dispatch drift organ — every literal command in Ch8 must resolve on the machine"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#592] [P2][S] **Dispatch drift organ — every literal command in Ch8 must resolve on the machine** — Four rival launch commands made ~30 seats correctly informed and wrong. Acts 2-3 fixed the pages; nothing stops them drifting again. This is the organ that makes it structurally unrecurrable: a doc naming a dead or rival command goes RED. · Done when: every literal command in PLAYBOOK Ch8's table resolves via `Get-Command` at commit time, `.claude/commands/lane-boot.md` is asserted to contain the ruled verb, a fire-test proves the check REDs on a planted dead command, and the machine-dependence is handled explicitly — in CI or a container the check reports `info` and NEVER green-by-skip · refs docs/intake/2026-08-26-tech-dispatch-consolidation-remainder.md (intake #52), docs/audits/2026-08-25-technical-dispatch-consolidation-plan.md section 4, protocols/PLAYBOOK.md Ch8, .claude/commands/lane-boot.md, protocols/STANDING_RULINGS.md section V · source: intake #52 (I4), the DRIFT-ORGAN act — second of three · kill-candidates: none — no open row asserts doc-to-machine command agreement; `[#285]` extends freshness GATING and checks no command resolves · serialize-group: gates · **CLOSED 2026-09-16** — evidence dd76e2b8
