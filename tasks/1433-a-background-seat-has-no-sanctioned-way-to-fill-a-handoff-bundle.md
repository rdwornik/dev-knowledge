---
id: "[#1433]"
title: "A background seat has no sanctioned way to fill a handoff bundle"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1433] [P2][M] **A background seat has no sanctioned way to fill a handoff bundle** - A background session's isolation guard refuses file edits in the primary checkout, and `assert_boundary_hygiene` (`gen_handoff.py:578`) refuses the `--filled` re-render while any linked worktree exists, the session's own included. The 2026-10-06/07 attempts moved files between a worktree and the primary by hand (readiness digest F12) · Done when: a tested path lets a background seat fill and finalise a bundle with no hand-moved file -- the readiness command's scratch clone landed as one commit from a lane, or a `--filled` that accepts the session's own worktree -- and `docs/handoffs/README.md` names it · owner: the handoff generator · touches: `scripts/gen_handoff.py`, `docs/handoffs/README.md`, tests · kill-candidates: `[#1436]` · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
