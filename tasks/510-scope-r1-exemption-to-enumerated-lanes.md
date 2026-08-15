---
id: "[#510]"
title: "Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#510] [P2][M] **Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today** — `batch_manifest.exempt()` keys condition 1 on branch SHAPE (`LANE_BRANCH_RE`), not the manifest's lane roster — any `worktree-lane-*` merge is exempt from `check_journal_spine_anchor` mid-batch, one `git branch -m` away. Batch 2 demonstrated it live. **W1 NARROWED it, did not close it** (`1c6d4255`): both keys now read the ratified grammar via one imported `LANE_BRANCH_RE`, so 9 of 16 historical lane shapes no longer qualify, pinned by `test_an_off_grammar_lane_branch_gets_NO_exemption_mid_batch`. **All four ROSTER legs stand** — no manifest `lanes:` field, no ruled no-roster posture, no Ch8 or template carrier — so a conforming branch is still exempt whether or not the manifest enumerates it · Done when: the exemption resolves against a lane roster the open manifest declares, the no-roster posture is ruled and encoded, a test proves a lane branch OUTSIDE the roster is not exempt mid-batch, and Ch8 + the manifest template carry the field · refs `scripts/batch_manifest.py` (HONEST LIMITS #2), `tests/test_batch_manifest.py`, ADR-110 amendment, [#505] · kill-candidates: none — [#508] owns the enum coupling · serialize-group: gates
