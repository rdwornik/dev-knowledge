---
id: "[#1421]"
title: "Each seat cycle tears down its own worktree and branch at CYCLE-END"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1421] [P2][S] **Each seat cycle tears down its own worktree and branch at CYCLE-END** - The operator ruled to the B2-W1 integrator seat (cycle 17) on 2026-10-06: "each seat cycle tears down its own worktree at CYCLE-END". Batch B2-W1 ran 18 integrator and 22 dispatcher seat cycles, and the `## Cycle` sections of both seat orders hand over (claim, bind, readback, `CYCLED`, release, unbind) without ever removing the outgoing seat's worktree or its `worktree-seat-<role>-<batch>-cycle-<n>` branch, so they piled up until batch close: 13 clean, merged seat worktrees and branches (dispatcher cycles 13-20, integrator cycles 11-15) were removed by hand at 13:33Z, plus cycle-16's earlier, with an empty husk `seat-integrator-b2-w1-cycle-4` still held by a process. Teardown of a seat cycle is currently nobody's step · Done when: (1) `templates/integrator-order-template.md` and `templates/dispatcher-order-template.md` `## Cycle` each carry a CYCLE-END step in which the outgoing seat, after the successor reads back `CYCLED`, verifies its own worktree clean and its branch merged (`git rev-list --count origin/main..<branch>` = 0), removes the worktree (plain `git worktree remove`, no `--force`) and deletes the branch locally and on origin by `-d`, and appends a `TEARDOWN` line to its receipt; a dirty or unmerged seat tree is reported, never forced; (2) `no_leftovers.py verify --contract <ROLE>-<BATCH>-cycle-<n>` reports the outgoing cycle's worktree and branch absent; (3) a test pins the step's presence in both templates · kill-candidates: none -- no open row carries seat-cycle teardown (`git grep -n -i -E "CYCLE-END|tears down its own" origin/main -- tasks` = 0) · refs `templates/integrator-order-template.md`, `templates/dispatcher-order-template.md`, `scripts/no_leftovers.py`, `scripts/claim.py`, `scripts/seat_registry.py` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (OPERATOR-RULING 13:30Z seat ruling and TEARDOWN SEATS 13:33Z, cycle 17)
