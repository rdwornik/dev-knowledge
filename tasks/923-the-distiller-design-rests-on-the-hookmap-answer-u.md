---
id: "[#923]"
title: "The distiller design rests on the hookmap answer -- UserPromptSubmit CAN inject, but whether a LONG injected description is used is untested"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#923] [P2][M] **The distiller design rests on the hookmap answer -- UserPromptSubmit CAN inject, but whether a LONG injected description is used is untested** - Wave-3 lane W3-3 measured, in live child sessions, that a `UserPromptSubmit` hook injects into the model's context through both channels (plain stdout 3/3, `additionalContext` 3/3, control 0/2; `docs/audits/2026-09-19-technical-wave3-hookmap-evidence.md`). That is the delivery path the (kind, subject) distiller (`gen_lane_contract.py distill`, B2 lane 3; `protocols/BUILD-LIST.md` "pre-action distillation") would use to put a distilled contract or organ description in front of the seat before it acts. The audit's own caveat bounds it: n=3 per channel, one small model, a short sentinel token -- "this proves injection is possible, not that a long injected description is used equally well (that is the distiller's own test)". A further confound it records: user-level `disableAllHooks: true` suppresses every hook unless a higher settings layer sets `false` · Done when: the distiller's delivery design is written down against the hookmap evidence (which event, which channel, what size), and a pre-registered child-session measurement shows whether a distiller-sized injected payload (not a sentinel) changes what the seat does, with the bar, raw count and control fixed before the first run; a miss is recorded as a result, not re-run · refs `docs/audits/2026-09-19-technical-wave3-hookmap-evidence.md`, `scripts/gen_lane_contract.py` (`distill`), `protocols/BUILD-LIST.md`
