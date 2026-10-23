---
id: "[#1705]"
title: "The start-up token probe runs on a dirty tree and prints sum, not calls = sum / iterations[0]"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1705] [P2][S] **The start-up token probe runs on a dirty tree and prints sum, not calls = sum / iterations[0]** - a dirty tree makes the Stop hook (`session_end_backpressure.py:470`) continue the turn, so `claude -p` makes a second call and its `usage` sums both (89,785 vs 44,707 on the same clone and CLI; CLIs 2.1.302/303/304 identical); the '53k tool block' of DIGEST-HARNESS-MAP-2026-10-20 D matches those 2x sums, and the 55,634 baseline in `[#1616]` is suspect for the same reason · owner: the harness-measurement lane (the `[#1616]` cut-1 owner) · Done when: (1) RED first: a test that the probe helper `[#1616]`'s witness uses exits non-zero with a message naming the dirty files when `git status --porcelain` is non-empty and prints `calls=N`; (2) the helper reports calls = sum / `usage.iterations[0]`; (3) real-use witness: `claude -p "Reply with OK." --output-format json --model claude-sonnet-5-5` once on a clean tree (one call, <= 52,000) and once with an untracked file (refused by the helper, not reported as a start-up cost); fails on 6043eaf5f · touches: the probe helper, `tests/` · kill-candidates: `[#1616]` -- its witness is invalid unless taken clean; `[#1618]` -- same measurement caveat · refs `[#1616]`, `[#1618]`, `[#1700]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-e2-startup-bisect.md` Item 5 · **CLOSED 2026-10-23** — evidence 21a9a369b
