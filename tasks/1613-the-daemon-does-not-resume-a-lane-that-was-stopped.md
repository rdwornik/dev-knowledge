---
id: "[#1613]"
title: "The daemon does not resume a lane that was stopped"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1613] [P1][S] **The daemon does not resume a lane that was stopped** - memory-diag harness row #11 (A4): `claude stop` leaves the job record and the daemon resumes it (memory note `claude-stop-leaves-the-job-record-and-the-daemon-resumes-it`) · Done when: RED first: a test asserts `seat_registry.py` records a `stopped-by-seat` event for a stopped job and that the queue/resume path refuses a job with that event; fails on a3d0ae31 · touches: `scripts/seat_registry.py`, `scripts/dispatch.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#918]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
