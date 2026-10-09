---
id: "[#1426]"
title: "BD-ci gives a different answer for the same sha within twenty minutes"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1426] [P2][S] **BD-ci gives a different answer for the same sha within twenty minutes** - In the 2026-10-07 readiness dry run BD-ci re-derived `6d79ef0` as NOT-RUN ("no Actions run matched 6d79ef086847 after waiting 0s") and about twenty minutes later agreed with the cut's RED again. `ci_verdict.list_runs` collapses an empty or null listing to `[]` (`ci_verdict.py:192-197`); a gh failure would have read GH-UNAVAILABLE (`:394`, `:457`), and a run that fell out of the 40-run window cannot come back, so the listing returned no matching run once. The exact cause is not yet established (readiness digest F3) · Done when: the cause is named from a captured `gh run list` on a reproduction; an empty or null listing is its own state, never NOT-RUN; BD-ci for a recorded sha reads the run by id (`verdict_for(run_id=)`), so a re-derivation cannot miss it; tests for each · owner: `scripts/ci_verdict.py`'s owner · touches: `scripts/ci_verdict.py`, `scripts/handoff_state.py`, tests · kill-candidates: `[#1427]` -- the same row and organ; one lane may take both · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/ci_verdict.py, scripts/handoff_state.py, ADR-129
