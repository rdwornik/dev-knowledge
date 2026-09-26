---
id: "[#1026]"
title: "integrator: batch_janitor.py reads a removed job as live"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1026] [P3][S] **integrator: batch_janitor.py reads a removed job as live** - WAVE5B-N1 close: `batch_janitor run --batch WAVE5B-N1` reported "11 of 11 live" for jobs already removed by `claude rm` -- an absent-reads-live defect, not the lane's per-lane-scope gap ([#1025]). · Done when: the janitor treats a `claude agents --json`-absent job as gone rather than live, RED-first witnessed on a fixture where the job record was removed before the janitor runs · refs `scripts/batch_janitor.py`, DIGEST-WAVE5B-N1-2026-09-25 ("integrator: batch_janitor reads a removed job as live") · kill-candidates: none -- distinct mechanism from [#1025] (scope vs staleness)
