---
id: "[#99]"
title: "FLEET-HEALTH digest names the failing check per red repo"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
generates: BACKLOG.md
---

- [#99] [P3][S] FLEET-HEALTH digest names the failing check per red repo — today the digest shows `corp-monorepo !! 1 fail` with no check name; the operator needs a second command (`audit.py repo <name>`) to learn WHAT is red · Done when: a red repo's digest line carries the failing check name(s) · refs ADR-76, #85, ADR-36 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
