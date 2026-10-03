---
id: "[#1338]"
title: "The batch template says no scheduled wake-ups; the batch practice is CronCreate and never ScheduleWakeup"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1338] [P2][S] **The batch template says no scheduled wake-ups; the batch practice is CronCreate and never ScheduleWakeup** - `templates/batch-common-rules-template.md:73` says "No cron, no scheduled wake-ups, no loops. Nothing of yours outlives your last message", while batch FOUNDATION's rendered common rules (section 4) arm every wake-up with `CronCreate` (session-only, recurring, deleted at stop) and forbid `ScheduleWakeup`, because outside `/loop` it ends a `--bg` seat's turn and never wakes (WAVE5B-N5 dispatcher 406d75c3, 2026-09-29). The template a render starts from and the rule a seat obeys disagree, and no file in the repo says which tool a waiting seat uses · Done when: the template states the wake-up mechanism for a waiting `--bg` seat (`CronCreate`, session-only, deleted at stop) and that `ScheduleWakeup` is for `/loop` only, and a test pins the template to the sentence the render copies · touches: `templates/batch-common-rules-template.md`, tests · kill-candidates: none -- no open row tracks the wake-up rule · refs `templates/batch-common-rules-template.md`, `templates/integrator-order-template.md` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
