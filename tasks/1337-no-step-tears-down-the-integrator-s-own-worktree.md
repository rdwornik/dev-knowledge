---
id: "[#1337]"
title: "No step tears down the integrator's own worktree, branch, job and claim"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1337] [P2][S] **No step tears down the integrator's own worktree, branch, job and claim** - `templates/integrator-order-template.md` tears down each LANE (step 5: job, worktree, branches, claim marker, then `no_leftovers.py verify --lane <slug> --contract <lane-contract-name>`) and removes the integration worktree (step 4); its Close section ends "Stop every Monitor, poll and shell of yours, and stop". Nothing releases the integrator seat's OWN claim marker (`claim.py release INTEGRATOR-<BATCH>`), removes its own worktree and branch, or verifies them with `no_leftovers.py verify --contract INTEGRATOR-<BATCH>`, so a closed batch can leave its integrator behind (the same half-teardown class as [#762]) · Done when: the Close section names the integrator's own teardown (claim, worktree, both branches, job) and a test over the template pins the sentence; a live round-trip leaves `no_leftovers.py verify --contract INTEGRATOR-<BATCH>` reporting CLEAN · touches: `templates/integrator-order-template.md`, `scripts/no_leftovers.py`, tests · kill-candidates: none -- [#762] is the stop-hook race on a LANE teardown and does not cover the integrator seat · refs `templates/integrator-order-template.md`, `scripts/no_leftovers.py`, `scripts/claim.py`, [#762] · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
