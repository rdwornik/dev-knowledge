---
id: "[#1847]"
title: "batch close compares the merge clock and the lane clock with their targets; a missed target queues the next line-throughput /decide by code"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1847] [P1][L] **batch close compares the merge clock and the lane clock with their targets; a missed target queues the next line-throughput /decide by code** - the throughput of the line is noticed by a seat, if at all, not measured at the close of a batch · Done when: at every batch close the merge clock ([#1444], WAKE -> main push by stage) and a lane clock (launch -> first push -> hand-back by stage: repair, review, quota wait, order wait, from stage records and session transcripts) each write one ledger; batch close prints median and worst against the targets (R62 hand-back -> main <= 15 min; the lane-cycle target the operator ratifies from the line-throughput /decide); a missed target queues the next line-throughput /decide with the new numbers, no seat noticing · owner: the integrator · touches: `scripts/batch_clocks.py` (new), `scripts/lane_digest.py`, `tests/test_batch_clocks.py` (new) · kill-candidates: #1444 -- the merge clock this row extends · source: `LANE-e30-seat-registry-binds.md` (GO-E3.0 C1), evidence `to-browser/DIGEST-INTEGRATION-REMEASURE-REVIEW-AMENDMENT-1-2026-11-01.md` "How the harness fixes itself" items 1-4 · filing only, not built by the lane that filed it · refs scripts/lane_digest.py
