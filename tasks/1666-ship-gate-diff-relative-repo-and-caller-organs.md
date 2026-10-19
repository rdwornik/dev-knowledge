---
id: "[#1666]"
title: "`ship_gate_diff.py` fails on a relative `--repo` and runs the caller's organ code on the target tree (defect 6)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1666] [P2][S] **`ship_gate_diff.py` fails on a relative `--repo` and runs the caller's organ code on the target tree (defect 6)** - A relative `--repo` fails building the baseline worktree, and the organs run are the caller's code against the target tree, not the target's own · owner: E2 lane. target batch: E2.1 · Done when: (1) `--repo` is resolved to an absolute path and the target tree's own organ code is run; (2) RED first: a test with a relative path fails today; real-use witness: the integrator's `ship_gate_diff.py diff --repo .claude/worktrees/<lane>` runs and reports the target's organs · touches: `scripts/ship_gate_diff.py` · kill-candidates: `[#1564]` -- also edits the ship_gate_diff run; sequence the two · refs `protocols/STANDING_RULINGS.md`, `to-browser/REFUSED-e2-rulings.md` Notes, `to-browser/LEDGER-dev-knowledge.md` v238 defect 6 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
