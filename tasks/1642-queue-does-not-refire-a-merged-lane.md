---
id: "[#1642]"
title: "queue does not refire a MERGED lane"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "intake-118"
generates: BACKLOG.md
---

- [#1642] [P1][S] **queue does not refire a MERGED lane** - `dispatch.py queue` does not refire a lane whose integrator receipt already reads MERGED. Sibling of `[#1572]` (`to-browser/SESSION-integrator-bu-2026-10-15.md:217-226`): `decide_lane` never checks the lane's own MERGED state, so a merged lane whose job ended is relaunched. owner: lane `lane-dz-1572-queue-halt` (second Done item) or a D1 lane. target batch: D0 · Done when: RED first: a batch with one lane whose `--state-file` line reads MERGED fires only the unmerged lanes; real-use witness: a `queue --watch` re-run of a finished batch fires nothing · touches: see the body · kill-candidates: `[#1572]` -- same code path · implements: intake-118 · refs `[#1572]`, `[#1536]` · decided-by: R137 (Q5: the plan r4 OK of 2026-10-18) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
