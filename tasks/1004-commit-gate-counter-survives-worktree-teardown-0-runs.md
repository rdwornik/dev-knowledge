---
id: "[#1004]"
title: "Commit-gate counter survives worktree teardown; '0 runs' reads UNMEASURED, not REMOVE"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1004] [P1][M] **Commit-gate counter survives worktree teardown; '0 runs' reads UNMEASURED, not REMOVE** - S2 proposed row 4, time-critical (expiry 2026-09-25): the commit-hook counter store is per-checkout (`<toplevel>/logs/TELEMETRY.db`, gitignored), so every lane's rows die at teardown; 4 armed hooks show zero runs in the primary store, and the 2026-09-25 verdict as worded cannot distinguish "never ran" from "never caught" (`docs/audits/2026-09-23-technical-hook-architecture-appendix.md` A3) · Done when: a lane's `hook_run` rows are readable from the primary checkout after its worktree is removed (the counter store moves to the git common dir); the 2026-09-25 expiry report lists runs and blocks per hook, and marks a hook with zero runs UNMEASURED rather than REMOVE · implements: ADR-120 · refs `scripts/telemetry_emit.py`, `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md` · kill-candidates: none -- no open row moves the counter store to survive teardown; time-critical per the source digest's own expiry date
