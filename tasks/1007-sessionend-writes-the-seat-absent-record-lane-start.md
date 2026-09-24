---
id: "[#1007]"
title: "SessionEnd writes the seat absent record; lane-start gets its trigger"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1007] [P2][M] **SessionEnd writes the seat absent record; lane-start gets its trigger** - S2 proposed row 7: `seat_registry.py` maps SessionEnd to an `absent` record but no hook sends it, and `harness.yaml`'s `lane-start` moment has no trigger at all, so a lane that skips it is invisible · Done when: a SessionEnd stdlib hook writes the seat's `absent` record; the first SessionStart in a lane worktree claims and detaches `moment:lane-start` exactly once per lane, witnessed by its receipt · implements: ADR-120 · refs `scripts/seat_registry.py`, `ecosystem/harness.yaml`, `docs/audits/2026-09-23-technical-hook-architecture.md` · kill-candidates: none -- no open row wires SessionEnd or lane-start
