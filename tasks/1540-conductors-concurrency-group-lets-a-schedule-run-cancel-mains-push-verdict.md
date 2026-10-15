---
id: "[#1540]"
title: "conductor's concurrency group is keyed by ref only, so a scheduled run on main cancels main's push verdict"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1540] [P1][S] **conductor's concurrency group is keyed by ref only, so a scheduled run on main cancels main's push verdict** - `.github/workflows/conductor.yml:87-89` sets `group: conductor-${{ github.ref }}` with `cancel-in-progress: true`. A `schedule` run on `main` therefore cancels the in-progress `push` run of the same ref: on 2026-10-05 push run 37304780263 (ca022976) lost its Windows leg ("cancelled") to schedule run 37305923170 on the same sha, and the integrator lost main's base verdict for that OS (a cancelled required check never reads as a pass). Recorded as ROWS-OWED in the B2-W1 integrator receipt (cycle 9) and never filed. The AMEND v5 L3 ask "add concurrency + cancel-in-progress" is already met by these lines; this is the defect left in them · Done when: RED first: a test reads `conductor.yml` and asserts that a schedule run and a push run of the same ref fall in different concurrency groups (for example the group carries `github.event_name`), while two pushes of the same ref still share one, so a superseded push is still cancelled; and the next schedule run on main leaves the concurrent push run's legs uncancelled (run ids in the receipt) · touches: `.github/workflows/conductor.yml`, `tests/test_conductor.py` · kill-candidates: none -- no open row owns the concurrency key (grep over tasks/ 2026-10-15) · refs `docs/intake/2026-10-15-tech-build1-owed-rows.md` · source: B2-W1 integrator receipt cycle 9 (ROWS-OWED); `to-cc/AMEND-BATCH-BUILD1-PREP-2026-10-15.md` v5 L3
