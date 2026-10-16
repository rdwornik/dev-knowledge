---
id: "[#1571]"
title: "A reaper-killed `merge_path.py land` resumes from its recorded CI run without a second integration push, and the restart-once rule is data"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1571] [P1][M] **A reaper-killed `merge_path.py land` resumes from its recorded CI run without a second integration push, and the restart-once rule is data** - the memory-pressure reaper killed `land` (and queue and pytest runs) and Claude Code forbids an unprompted restart; the seat waited for the operator (to-browser/SESSION-integrator-bu-2026-10-15.md:125-126; lane-1537 C3 reaped; lane-1450 paired baseline killed). `[#1012]` `[#970]` cover the reaper and admission gate, not land resume · Done when: RED first: (1) a fake-runner test kills `land` after the integration push and before the main push, re-runs it, and asserts no second integration push and the CI verdict read from the recorded run id; (2) the restart-once rule is a data field read by a test (`restart_once: true` for land and queue); fails on 97bcd374 · touches: `scripts/merge_path.py`, `ecosystem/harness.yaml`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1012]`, `[#970]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
