---
id: "[#959]"
title: "Wave 4b lane 3 (lane-gate-verdicts) -- gates speak data, and the connection test reads it"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#959] [P1][M] **Wave 4b lane 3 (lane-gate-verdicts) -- gates speak data, and the connection test reads it** - filed by LANE-W4B-0 per `to-cc/WAVE4B-COMMON-2026-09-22.md` rule 1; frozen contract `LANE-W4B-3-gate-verdicts.md`, branch `worktree-lane-gate-verdicts`. Depends on lane 0 (`[#956]`); runs in parallel with lanes 2, 4, 5 after lane 0 merges. Value: the connection test is the harness's instrument, and it failed because it searched the last 6-11 lines of gate output for names printed at the top; three of its tests also fail at `-n 2` because they share state, and the module takes 18 minutes. After this lane the gates hand over data, the instrument reads data, and it runs green in parallel. · implements: ADR-120 · Done when: 1. **FR4 as written in the plan:** `gates.py` writes a per-organ JSON verdict listing every hard-fail and warning name; the human-readable output stays (common rule 8). 2. **The census** emits the 36 dated organs in that JSON. 3. **The connection test** reads toy-copy markers from the JSON, not from output tails. 4. **The launch-step trio** (`launched_once...`, `human_writes...`, `loop_stops...`) is fixed at the cause -- shared state between tests -- and proven green 3/3 at `-n 2` and 1/1 alone. 5. **Runtime:** the module at `-n 2` on an idle box in <= 10 minutes, measured three times; if a test is inherently slow, say which and why. 6. **Do not change the merge moment's organ list or its expected lists;** lane-merge-path owns that change after this lane merges. 7. **Codex terra review** with its consumer cited; **self-check and purity**; **handback** · refs `LANE-W4B-3-gate-verdicts.md`, `to-cc/WAVE4B-COMMON-2026-09-22.md`, `to-cc/PLAN-WAVE4B-SESSION-2026-09-22.md` (FR4), `to-browser/DIGEST-WAVE4-FINAL-2026-09-22.md` (G6 and findings 4, 10), `[#955]` (the epic this row implements) · kill-candidates: none -- no open row covers structured gate verdicts
