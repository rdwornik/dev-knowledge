---
id: "[#1076]"
title: "R1a: PR / CI-gated close is the closure-sweep model"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
implements: "ADR-122"
generates: BACKLOG.md
---

- [#1076] [P2][S] **R1a: PR / CI-gated close is the closure-sweep model** - ADR-122 D4's closure sweep takes a PR / CI-gated close as its model (a task closes when its PR merges green, not by hand), carried in by RATIFICATION-2026-09-25 R1 · Done when: `docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md` and `protocols/STANDING_RULINGS.md` §AM both cite R1a, and D4's closure-sweep text names a PR / CI-gated close as its model -- `grep -q "PR / CI-gated close" docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md && grep -q "R1a" protocols/STANDING_RULINGS.md` · implements: ADR-122 · refs docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md, protocols/STANDING_RULINGS.md §AM · kill-candidates: none -- no prior row tracked this ratification; discharged by this lane's own ADR-122 and STANDING_RULINGS §AM landing
