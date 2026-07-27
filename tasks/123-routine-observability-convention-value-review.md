---
id: "[#123]"
title: "Routine observability convention + value review"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
source: BACKLOG.md
derived: true
---

- [#123] [P2][S] Routine observability convention + value review — (1) all automation commits carry a standard marker (scope `chore(routine/<name>)` or trailer `Routine: <name>`) so routine output is git-indexable; (2) periodic value review in the morning funnel: findings-acted-on vs noise per routine (first datapoint: 2026-06-07 nightly digest 0/0/0 vs local baseline 1 FAIL) · Done when: the marker convention is recorded + adopted by the fleet/routine jobs AND one morning-funnel value review records per-routine findings-acted-on vs noise · refs #85, #14, #113, audit C matrix R7 · origin: operator proposal 2026-06-07
