---
id: "[#894]"
title: "Lane ac-285 wedged after a successful tool call -- an unexplained single-lane wedge, cause unverified"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#894] [P2][S] **Lane ac-285 wedged after a successful tool call -- an unexplained single-lane wedge, cause unverified** - `lane-ac-285-config-headers` (batch AC) produced zero commits and left a clean tree. Its transcript froze at 66 lines, and the last real event was a SUCCESSFUL `H:`-path contract read at 22:16:30 UTC 2026-09-17. `SESSION-dispatcher.md`'s three-sample liveness check read 66/66/66 while its siblings read 200+. It was the only one of six local lanes in that state. Two causes are ruled OUT on evidence: transport, because the last read succeeded, and the suspended-spawn defect, which B0 measured NOT reproducing (12/12 clean, zero new orphans). **The cause is unknown and this row does not guess one** (ruling R5). Priced by `lane_cost.py`: 4 calls, USD 0.20, so it was wedged almost at once. Its worktree is torn down by the integrator under R5 · Done when: either the cause is established by a witnessed reproduction, or the next window's liveness sampler catches a second instance with a capture taken while it is wedged (process tree, last transcript record, hook state). Two windows with no recurrence retire this row as unreproduced, and the retirement is recorded as such, never as fixed · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` R5 + §6 W3, `to-browser/HANDBACK-batch-AC-consolidated.md` (L3), `to-browser/SESSION-dispatcher.md`, `[#863]` (the suspended-spawn class, ruled out here), `[#833]` (seat registry: a wedged seat is invisible) · kill-candidates: `[#833]` -- if its wedged-seat detection lands with a capture-on-detect leg, this row's Done-when is met by it
