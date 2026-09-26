---
id: "[#1077]"
title: "R1b: the whole-graph check refuses cycles and dangling ids"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
implements: "ADR-122"
generates: BACKLOG.md
---

- [#1077] [P2][S] **R1b: the whole-graph check refuses cycles and dangling ids** - ADR-122 D3's whole-graph check refuses dangling ids and cycles, as GitHub's dependency API does (422 / 404), carried in by RATIFICATION-2026-09-25 R1 · Done when: `docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md` and `protocols/STANDING_RULINGS.md` §AM both cite R1b, and D3's text reads "refuses dangling ids and cycles" -- `grep -q "refuses dangling ids and cycles" docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md && grep -q "R1b" protocols/STANDING_RULINGS.md` · implements: ADR-122 · refs docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md, protocols/STANDING_RULINGS.md §AM · kill-candidates: none -- no prior row tracked this ratification; discharged by this lane's own ADR-122 and STANDING_RULINGS §AM landing
