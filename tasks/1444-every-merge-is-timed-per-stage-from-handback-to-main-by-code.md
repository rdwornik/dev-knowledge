---
id: "[#1444]"
title: "Every merge is timed per stage from handback to main, by code on the integrator's path, with a median and p90 report (W2-24, R85)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1444] [P1][M] **Every merge is timed per stage from handback to main, by code on the integrator's path, with a median and p90 report (W2-24, R85)** - R85 (operator, 2026-10-05) holds R62's handback -> `main` median at <= 15 min against 98 min measured, and orders the merge clock (W2-24) first. Today `scripts/merge_receipt.py` records a stage only when the integrator wraps a command (`STAGE_ORDER`, `time`); none of B2-W1's 14 receipts carries a handback stage, its `median` has no p90 and no handback -> main figure, and the 98 min was reconstructed by hand from session lines and mtimes · Done when: (1) every integration after this row lands writes a machine-readable record with handback, pick-up, integration worktree ready, merge commit, CI requested, each CI job's end (per attempt), verdict and push to `main`, its disjoint stages summing to handback -> main within 60 s, written by code on the integrator's path that never blocks a merge; (2) one command prints median and p90 per stage and the median handback -> main over the last N merges, an unmeasured stage reading UNMEASURED, never 0; (3) RED-first: the report flags a receipt with no stage times (fails on `03d21ff8`) · kill-candidates: none -- no open row times merges per stage (`git grep -n -i "merge clock" origin/main -- tasks` = 0) · refs `scripts/merge_receipt.py`, `scripts/merge_path.py`, `ecosystem/harness.yaml`, `protocols/STANDING_RULINGS.md` (R62) · source: R85 in `to-browser/RATIFICATION-2026-10-05.md`; `to-browser/DIGEST-DECIDE-MERGE-LATENCY-2026-10-05.md`; batch B2-W2 lane `b2w2-merge-clock` (`to-cc/BATCH-B2-W2-2026-10-09.md` §3 lane 2)
