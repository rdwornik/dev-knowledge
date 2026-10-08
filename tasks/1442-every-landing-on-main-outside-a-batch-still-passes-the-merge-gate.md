---
id: "[#1442]"
title: "Every landing on main outside a batch still passes the merge gate (step 2 bypassed it and put 3 NEW reds on main -- see [#1441])"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1442] [P1][M] **Every landing on main outside a batch still passes the merge gate (step 2 bypassed it and put 3 NEW reds on main -- see [#1441])** - Evidence: the B+ step-2 landing (merge `350c07f7`, 2026-10-08) was a seat landing outside any batch. It went through `git merge --no-ff` and `git push`, and the pre-commit, commit-msg and pre-push hooks all passed. The merge gate in `scripts/merge_path.py` (ci_verdict + `scripts/known_reds.py compare` against the registry, REFUSE on a NEW red) never ran, because only a batch integrator's path calls it. CI run 37790704091 then read `known_reds.py compare` FAIL -- REGRESSION -- 3 on both OS, plus 14 NEW ship-gate hard-fails and 3 NEW commit-gate findings, all owned by [#1441] · Done when: (1) every landing on `main` -- batch lane, seat landing, handoff bundle -- passes one merge gate that judges the merged tree against the known-reds registry, REFUSES a NEW red before `main` moves, and names it; (2) a test reproduces the step-2 shape (a seat branch merged `--no-ff` and pushed outside any batch, carrying a test the registry does not know as red) and shows the push refused, failing before the fix; (3) the sanctioned bypass, if one is kept, is a named, declared exception recorded in the merge commit, never silence · kill-candidates: [#1367] -- the integrator merges only on a green CI verdict for the exact sha; fold this row into it if W2 makes that gate cover every landing, not only the integrator's · refs [#1441], [#1367], `scripts/merge_path.py`, `scripts/known_reds.py` · source: operator order 2026-10-08 (the handoff-bundle merge authorization), filed on `worktree-handoff-bundle-2026-10-08` before its merge
