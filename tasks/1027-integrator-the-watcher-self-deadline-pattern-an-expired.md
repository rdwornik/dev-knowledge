---
id: "[#1027]"
title: "integrator: the watcher self-deadline pattern (an expired Monitor leaves its loop running) needs a harness-level fix, not a per-batch workaround"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1027] [P2][S] **integrator: the watcher self-deadline pattern (an expired Monitor leaves its loop running) needs a harness-level fix, not a per-batch workaround** - WAVE5B-N1 FINDING: an expired Monitor left 13 orphan bash loops eating handback events into a shared seen-file; this batch's fix was a self-deadline + `WATCH-START slug@sha` marker applied by hand each time -- owed as a reusable harness pattern rather than per-lane discipline. · Done when: a shared helper (or documented convention) gives every Monitor loop a self-deadline and start marker by default, so a future lane does not have to reinvent it · refs DIGEST-WAVE5B-N1-2026-09-25 ("FINDING watcher"), memory an-expired-monitor-leaves-its-bash-loop-running, `docs/audits/2026-09-26-technical-lane-rows-owed-2-provenance.md` · kill-candidates: none -- no open row generalizes this pattern
