---
id: "[#429]"
title: "Worktree provisioning is not portable across the fleet"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: environment
generates: BACKLOG.md
---

- [#429] [P2][M] **Worktree provisioning is not portable across the fleet** — the hub seeds worktree untracked files from `.worktreeinclude`, but the mechanism is **hub-shaped**: a satellite without the manifest cannot provision, and one with a **shared editable install** imports the PRIMARY checkout's source inside a worktree — so worktree `pytest` tests the wrong files and goes **GREEN**. Evidence: `ai-council` has no `.worktreeinclude` (verified), and its V3 import proof needs a worktree to run — **the proof requires the thing it proves**. **Second evidence:** ids on UNMERGED branches are invisible to next-free scans — that caused the [#427] collision; [#421]/[#422] will repeat it. Two legs, unbuilt: **(a)** a portable seed-manifest stated ONCE in the hub, not hand-copied per satellite; **(b)** a per-worktree venv so imports follow the checkout. · Done when: a satellite can provision a worktree AND prove by a runnable check that its pytest imports THAT worktree's source · refs `.worktreeinclude`, ADR-61, #425, #427, #505 (cross-ref) · kill-candidates: none — no open task owns worktree portability; [#425] owns fixture coverage, not provisioning · serialize-group: environment
