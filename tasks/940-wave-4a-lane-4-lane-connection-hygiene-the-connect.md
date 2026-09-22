---
id: "[#940]"
title: "Wave 4a lane 4 (lane-connection-hygiene) -- the connection test tells the truth, stably"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#940] [P2][M] **Wave 4a lane 4 (lane-connection-hygiene) -- the connection test tells the truth, stably** - filed by LANE-W4-1 per `to-cc/DECLARE-WAVE4A-2026-09-22.md` hard precondition 3 (rows for lanes 1-5 exist before lanes 2-5 fire; R-W4-7); frozen contract `LANE-W4-4-connection-hygiene.md`, branch `worktree-lane-connection-hygiene`, a wave-4a lane closing the loop `[#929]` evaluated. Value: The connection test is the harness's own instrument. Today it flakes under parallel runs, its toy copy of the repo turns gates red for reasons that are not the loop's, and two path families are invisible to the test selector. An instrument that lies is worse than none. · Done when: carried verbatim from the frozen contract -- 1. **Stable:** the three tests red at `-n 4` and green alone are fixed at the cause (serialization of the walk, shared state), proven green 2/2 at `-n 2` and 1/1 alone. 2. **Honest toy:** the throwaway repository no longer produces gate reds that are artifacts of the copy (unarmed hooks, commit-date-driven checks, unregistered repo, missing commit objects): the fixture arms or registers what a real box has, or the walk records those causes as FIXTURE-ARTIFACT, distinct from a loop stop. The loop's real stops stay visible. 3. **Selector:** `impacted_tests.py select` maps `templates/*.ps1` and `tests/fixtures/**`, so a pairing over them is no longer partial. 4. **Deploy manifest:** the new Stop hook entry is declared in the deploy manifest; the `fleet_parity` WARN for it is gone. 5. **Transport isolation proven** before and after every run. 6. **Codex terra review** with its consumer cited; **pre-handback self-check**; **handback**. · refs `LANE-W4-4-connection-hygiene.md`, `to-cc/WAVE4-COMMON-2026-09-22.md`, `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `scripts/impacted_tests.py` · kill-candidates: none -- no open row covers this lane's work
