---
id: "[#1427]"
title: "BD-ci counts pre-existing gate-job reds as new reds because it reads CI with no baseline"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1427] [P2][S] **BD-ci counts pre-existing gate-job reds as new reds because it reads CI with no baseline** - `handoff_state.row_ci` calls `ci_verdict.verdict_for(ref, timeout_s=0)` with no `baseline` and no `required_contexts` (`handoff_state.py:179`), so the cut recorded `6d79ef0` as "RED (26 new red(s), run 37490604437)" while that run's pytest legs on ubuntu and windows passed and only the ship-gate and commit-gate jobs were red, both pre-existing (readiness digest F3) · Done when: `row_ci` classifies a red run against its first parent (`actions_verdict`) and states REGRESSED / PRE-EXISTING, so pre-existing gate-job reds never read as new; a RED-first test over a recorded run · owner: `scripts/handoff_state.py`'s owner · touches: `scripts/handoff_state.py`, tests · kill-candidates: `[#1426]`; `[#1020]` triages the commit-gate job's own reds, which this row only stops miscounting · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/handoff_state.py, ADR-129
