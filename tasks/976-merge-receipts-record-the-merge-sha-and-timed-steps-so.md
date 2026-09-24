---
id: "[#976]"
title: "Merge receipts record the merge sha and timed steps, so batch-close can name the task"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#976] [P1][M] **Merge receipts record the merge sha and timed steps, so batch-close can name the task** - D13: ledger rows lack the merge sha; a batch digest named 0 of 6 shas (B1/B4), because `merge_receipt` records no merge sha and no timed step under the procedure the integrator actually runs (`docs/audits/2026-09-23-technical-state-of-the-harness.md` §1, 'Why batch-close stops') · Done when: `merge_receipt` records the merge sha and each timed step (gates, compare, ship-gate) under whichever merge path is actually operated; the batch-close digest names the task and the merge sha for every row it reports, witnessed on a real batch · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-state-of-the-harness.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row completes the merge_receipt sha/step record; sits inside lane-merge-path's scope (W4B-1, deferred)
