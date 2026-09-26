---
id: "[#1025]"
title: "integrator: batch_janitor.py has no per-lane scope and resolves receipts under its own checkout"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1025] [P3][S] **integrator: batch_janitor.py has no per-lane scope and resolves receipts under its own checkout** - WAVE5B-N1 integrator FINDING: the janitor needs `HARNESS_RECEIPTS_DIR` (or an equivalent) to resolve a lane's receipts from its own worktree rather than the janitor's own checkout. · Done when: `scripts/batch_janitor.py` accepts a per-lane receipts-directory override and a fixture proves it reads the right one · refs `scripts/batch_janitor.py`, DIGEST-WAVE5B-N1-2026-09-25 · kill-candidates: none -- no open row tracks this scope gap
