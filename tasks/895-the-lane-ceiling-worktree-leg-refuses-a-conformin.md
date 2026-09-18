---
id: "[#895]"
title: "The lane-ceiling worktree leg refuses a conforming plan -- it counts the freezing seat's own worktree as a provisioned lane"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#895] [P2][S] **The lane-ceiling worktree leg refuses a conforming plan -- it counts the freezing seat's own worktree as a provisioned lane** - At batch AC's freeze, `seat_refusals.py lane-ceiling --check-worktrees` refused a conforming 6-lane plan with `REFUSED [lane-ceiling]: the ceiling was checked LATE: 1 lane(s) already provisioned (...\.claude\worktrees\ac-night-freeze)`. The same plan PASSED without the flag (`6 lane(s) <= 6`). The worktree leg counts DIRECTORIES under `.claude/worktrees/`, not lanes. The freeze seat's branch `worktree-ac-night-freeze` is not a lane branch (`validate_branch_naming.is_lane_branch` is False for it), but it was counted as one. The only workaround is tearing the seat's own worktree down before step 0, which the seat cannot do from inside it · Done when: the worktree leg counts only worktrees whose branch is a lane branch by `is_lane_branch` (the one predicate, not a copy), so a seat's non-lane worktree never reads as a provisioned lane. RED-first witness: a tree holding one `worktree-<seat>` worktree and zero lane worktrees PASSES a plan at the ceiling, and a tree holding one `worktree-lane-*` worktree still refuses as checked-late · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W4, `scripts/seat_refusals.py` (`refuse_lane_ceiling`, `cmd_lane_ceiling`), `scripts/validate_branch_naming.py` (`is_lane_branch`), `to-browser/HANDBACK-batch-AC-consolidated.md` (L-freeze item 4) · kill-candidates: none -- no open row names the lane-ceiling worktree leg
