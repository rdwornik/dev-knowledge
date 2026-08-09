---
id: "[#308]"
title: "Decide the `verify` skill's canonical home"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#308] [P3][S] Decide the `verify` skill's canonical home (#9 self-flagged open question), pegged to P6 — the hub `.claude/skills/verify` self-flags "canonical-home open — #9, hub-local pilot": distribute it to consumers via the floor/plugin carrier (like tier1-lifecycle) OR ratify it permanently hub-local. Parallel half-adoption gap: ai-council carries NO project-gotchas skill at all (no .claude/skills/ dir), so the universal+per-project skill pattern is only half-realized fleet-wide. Decide (do not build today) as part of the P6 consumer-carrier step, where the distribution mechanism is already being touched. · Done when: the verify-skill home is decided (floor/plugin-distributed vs permanently hub-local) and recorded, at/along the P6 carrier step · refs .claude/skills/verify/, plugins/tier1-lifecycle/, deploy/manifest-v1.2.0.yaml, docs/audits/2026-07-11-census-consolidated-morning-brief.md §5c, #221 · kill-candidates: none — no open task subsumes the verify-skill-home decision · serialize-group: settings-json · DEFER — peg RE-PEGGED 2026-08-09 to the intake #25 W-wave carrier decision (W-2/W-3), ACCEPTED and live; old peg #221 closed 8aab4356 with no successor
