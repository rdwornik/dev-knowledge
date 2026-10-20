---
id: "[#1675]"
title: "A finished bg lane leaves its worktree locked by a dead pid, so teardown needs a hand unlock"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1675] [P3][S] **A finished bg lane leaves its worktree locked by a dead pid, so teardown needs a hand unlock** - After job `20745ef9` ended `done` with a clean tree, `git worktree remove` met a stale 'claude session e2-rows-r164 (pid 36660)' lock on a pid that was not running and the integrator unlocked it by hand (`to-browser/SESSION-integrator-e2-0-2026-10-18.md` TEARDOWN e2-rows-r164, DEFECT SEV-3); the empty-husk cases at TEARDOWN e2-rulings and e2-census-2 are the same family · owner: a lane-teardown lane · Done when: (1) RED first: a test shows a lock whose pid is dead and whose job is `done` surviving the lane's end; (2) the lane-end path or `no_leftovers` clears a lock only after proving the pid is dead and the job is done; (3) real-use witness: the next finished lane tears down with no `worktree unlock` · touches: `scripts/no_leftovers.py` · kill-candidates: `[#1421]` -- husk worktree; one fix may close both · refs `[#1421]`, `[#1010]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-integrator-e2-0-2026-10-18.md` item TEARDOWN e2-rows-r164 (owed row 3, locked worktree)
