---
id: "[#961]"
title: "Wave 4b lane 5 (lane-plan-lint) -- the architect's plan is checked by code before it freezes"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#961] [P1][M] **Wave 4b lane 5 (lane-plan-lint) -- the architect's plan is checked by code before it freezes** - filed by LANE-W4B-0 per `to-cc/WAVE4B-COMMON-2026-09-22.md` rule 1; frozen contract `LANE-W4B-5-plan-lint.md`, branch `worktree-lane-plan-lint`. Depends on lane 0 (`[#956]`); runs in parallel with lanes 2, 3, 4 after lane 0 merges. Carries FR6, which the epic row `[#955]` does not carry. Value: in three waves the architect missed two cross-lane dependencies, wrote contradictory instructions once, and set two time targets with no measurement behind them. Each cost hours. After this lane a wave's contracts are checked by code before they freeze, and time estimates come from receipts. · implements: ADR-120 · Done when: 1. **FR6 as written in the plan.** Input: a set of lane contracts (the transport's `LANE-*.md` format, `Files you own` and `Depends on`/`Serial` statements) plus the harness declaration. Findings, each with the two contracts involved: two lanes owning the same file; a lane consuming an artifact or schema no earlier lane or main provides; a lane changing a list that another lane's test asserts literally (the W4-2/W4-4 class) -- detected from `harness.yaml` moments touched vs tests that reference those organ names; a serial lane that another lane does not wait for, or a wait on a lane that is not serial. 2. **Estimates:** from `SESSION-integrator-*` receipts, median and spread of lane work time and of pickup-to-push time; a wave estimate = serial chain + integration count x median. 3. **Proof on real data:** run it over the wave-4a and wave-4b contracts on the transport (read-only) and paste the findings; it must flag the W4-2/W4-4 conflict of wave 4a. 4. **Acceptance tests of FR6** from the plan, red first; synthetic contracts only. 5. **Codex terra review** with its consumer cited; **self-check and purity**; **handback** · refs `LANE-W4B-5-plan-lint.md`, `to-cc/WAVE4B-COMMON-2026-09-22.md`, `to-cc/PLAN-WAVE4B-SESSION-2026-09-22.md` (FR6), `to-cc/DECLARE-WAVE4B-DIRECTION-2026-09-22.md` (RC6), `[#955]` (the epic this row does not carry FR6 for -- this lane row is FR6's sole carrier) · kill-candidates: none -- no open row covers plan linting
