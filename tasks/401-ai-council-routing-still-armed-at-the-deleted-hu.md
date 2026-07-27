---
id: "[#401]"
title: "ai-council routing still ARMED at the deleted hub landing zone"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#401] [P2][S] **ai-council routing still ARMED at the deleted hub landing zone** — routed-mirror retired, zone deleted (`b4435fad` 2026-07-22; ADR-43 amendment 2026-07-23), but ai-council `settings.yaml` `target_projects` still lists `.dev-knowledge`: a `target-project:` run would silently RE-CREATE it as untracked files. (a) ai-council-side config fix — drop `.dev-knowledge` from `target_projects` + the hub-landing docs; OPEN, untouched here. (b) gap — nothing PREVENTS re-creation after (a): ADR-77's guard covers only Claude Edit/Write, not CLI writes; `docs/decisions/` is sanctioned so Rule A won't fire. **(b) RULED: `routing.py` PATH-REFUSAL** — the routing component itself refuses the `.dev-knowledge` target. Reason: refusal at the point of use is ONE organ; extending an existing guard adds a SECOND organ watching the first, and this fleet already carries organ sprawl. **Rejected:** extending the ADR-77 guard / hermetization gate to the zone. · Done when: (a) shipped in ai-council AND (b) built per this ruling · refs ADR-43 amendment, ADR-77, night-batch audit P3a · kill-candidates: none — no open task covers the CLI-side re-creation hazard · serialize-group: architecture
