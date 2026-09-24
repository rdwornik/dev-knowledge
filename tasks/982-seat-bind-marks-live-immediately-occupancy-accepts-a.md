---
id: "[#982]"
title: "Seat bind marks live immediately; occupancy accepts a starting record instead of exit 2"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#982] [P2][S] **Seat bind marks live immediately; occupancy accepts a starting record instead of exit 2** - D23: a bound seat reads "absent" until its first hook event fires, and `worktree_occupancy.py` exits 2 on a starting record because it expects an external `state`/`status` shape the bind does not yet write · Done when: `seat_registry.py bind` marks the seat live at bind time (not at first hook event); `worktree_occupancy.py` accepts either a `state` or a `status` key on a starting record without exiting 2; a witness bind-then-immediately-check sequence reads live, not absent · implements: ADR-120 · refs `scripts/seat_registry.py`, `scripts/worktree_occupancy.py`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row fixes the bind-to-first-observation gap
