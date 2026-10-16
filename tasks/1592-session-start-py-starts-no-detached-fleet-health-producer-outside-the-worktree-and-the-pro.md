---
id: "[#1592]"
title: "`session_start.py` starts no detached fleet_health producer outside the worktree, and the producer completes a pass"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1592] [P3][S] **`session_start.py` starts no detached fleet_health producer outside the worktree, and the producer completes a pass** - `FLEET-HEALTH-PRODUCER.json` reads FAILED: 'audit.py run did not complete a full pass' (775 s); running `session_start.py` in lane b started a detached producer outside the worktree (`to-browser/LANE-END-lane-nv-929-c-handoff-transport.md`; `to-browser/SESSION-lane-nv-929-b-ci-gates.md` SIDE EFFECT). `[#962]` is the design row · Done when: RED first: a test runs the SessionStart reader in a temp worktree and asserts no child process is left whose cwd is outside it; fails on 97bcd374 · touches: `scripts/hooks/session_start.py`, `scripts/fleet_health.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#962]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
