---
id: "[#1569]"
title: "moment:merge runs without a hand-set HARNESS_CONTRACT, takes its worktree from the integration checkout, and its open-receipt file is git-ignored"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1569] [P1][S] **moment:merge runs without a hand-set HARNESS_CONTRACT, takes its worktree from the integration checkout, and its open-receipt file is git-ignored** - `merge_receipt` stops at `models` with HARNESS_CONTRACT unset and defaults `--worktree` to a path absent inside an integration worktree; `logs/.merge-receipt-<worktree>.json` is untracked-not-ignored and was staged into a merge (to-browser/SESSION-integrator-bu-2026-10-15.md:67,155; `to-browser/LANE-END-green-main-2026-10-14.md:13`) · Done when: (1) a test runs the merge moment in a temp integration worktree with HARNESS_CONTRACT unset and gets exit 0, the worktree resolved from the checkout; (2) `git check-ignore logs/.merge-receipt-x.json` exits 0; (3) both fail on 97bcd374 · touches: `scripts/merge_receipt.py`, `.gitignore`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1024]`, `[#885]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
