---
id: "[#1440]"
title: "Handoff readiness pins the commit and a completed CI run id across dry run and cut; every gate condition must be satisfiable after the steps it gates"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1440] [P1][M] **Handoff readiness pins the commit and a completed CI run id across dry run and cut; every gate condition must be satisfiable after the steps it gates** - Evidence: the 2026-10-08 cut order gated the real cut on "BD-ci must equal dry run #2", and the same order required step 2 to land on `main` first. Landing moves `main`, so BD-ci (re-derived from `origin/main`) could never equal the dry run's `6d79ef0` value: dry run #2 recorded '`6d79ef0` RED (26 new red(s), run 37490604437)', the landed `350c07f7` gave NOT-RUN while its run was in progress and then '`350c07f` RED (42 new red(s), run 37790704091)'. The seat withdrew the condition (`to-browser/RATIFICATION-2026-10-08.md` v2) · Done when: (1) the readiness command ([#1436]) records one pinned input -- a commit sha and the id of a COMPLETED CI run on it -- and the dry run, the probe stage and the cut each read that pin and refuse a different one; (2) BD-ci on a pinned cut reports the pinned run, never an in-progress one; (3) a check over the readiness procedure asserts no gate condition depends on state that a step it gates must change (the 2026-10-08 conflict is its first fixture, and it fails before the fix) · kill-candidates: [#1426] [#1427] -- the BD-ci non-determinism and no-baseline rows; fold whichever lands first into this pin · refs [#1436], [#1426], [#1427], `scripts/handoff_state.py`, `scripts/ci_verdict.py` · source: `to-browser/RATIFICATION-2026-10-08.md` v2 (the cut-option ruling), filed at the 2026-10-08 architect cut (`docs/handoffs/2026-10-08-dev-knowledge-architect/`)
