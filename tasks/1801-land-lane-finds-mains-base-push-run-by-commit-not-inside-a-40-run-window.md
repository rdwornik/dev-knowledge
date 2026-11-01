---
id: "[#1801]"
title: "land_lane finds main's base push run by commit, not inside a 40-run window"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1801] [P1][S] **land_lane finds main's base push run by commit, not inside a 40-run window** - `scripts/actions_verdict.py` `fetch_run` lists only the newest 40 conductor.yml push runs, so a base push run older than that (e30-bootstrap's base c6618dbb7, run 41035368018, at position 55-56) is read as absent and land_lane exits 3 `RED UNATTRIBUTED ... no baseline was given` although the baseline WAS given · Done when: `fetch_run` finds a sha's push run with `gh run list --workflow conductor.yml --event push --commit <sha>` (newest push run wins, `ActionsUnavailable` and the [#742] job-list sentinel unchanged); a baseline whose lookup succeeded but found no run renders `baseline run not found for <sha>`, one whose lookup raised `ActionsUnavailable` renders `baseline run unavailable (<error>)`; neither says `no baseline was given`; tests in `tests/test_actions_verdict.py` · owner: the integrator · touches: `scripts/actions_verdict.py`, `tests/test_actions_verdict.py` · kill-candidates: none -- no open row covers the fetch_run window · source: `LANE-e30-actions-window.md` (GO-E3.0 C1), evidence the 2026-11-01 e30-bootstrap landing (orchestrator HAND-STEP) · refs scripts/actions_verdict.py, tests/test_actions_verdict.py
