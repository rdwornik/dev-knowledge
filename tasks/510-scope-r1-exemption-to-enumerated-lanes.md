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

- [#510] [P2][M] **Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today** — `batch_manifest.exempt()` keys condition 1 on branch SHAPE (`LANE_BRANCH_RE`), not the manifest's lane roster — any `worktree-lane-*` merge is exempt from `check_journal_spine_anchor` mid-batch, one `git branch -m` away. Batch 2 demonstrated it live (packet §2). **Assessed for S-fix, rejected as M** (reasoning: packet §2): no machine-readable roster today; `docs/audits/` immutability forces a prospective no-roster ruling; ripples into Ch8 + template + ADR-110. Push leg never consults the manifest (bounded blast radius). · Done when: the exemption resolves against a lane roster the open manifest declares, the no-roster posture is ruled and encoded, a test proves a lane branch OUTSIDE the roster is not exempt mid-batch, and Ch8 + the manifest template carry the field · **W1 PARTIAL 2026-08-11** (batch-4 lane A, `1c6d4255`) — the self-grant is NARROWED, not closed. `exempt()`/`is_lane_merge` now key on the ratified grammar via the single imported `LANE_BRANCH_RE`, so 9 of 16 historical lane-branch shapes no longer qualify, and `test_an_off_grammar_lane_branch_gets_NO_exemption_mid_batch` pins an off-grammar `worktree-lane-*` branch getting nothing mid-batch. **All four ROSTER legs stand:** no manifest `lanes:` field, no ruled no-roster posture, no Ch8 or template carrier — a conforming branch is still exempt whether or not the open manifest enumerates it, so the rename escape is harder to reach by accident but not foreclosed. W1 stopped at the grammar deliberately: shipping a roster field whose carriers do not exist would be precisely the half-landed adoption `[#513]` was amended to detect, and Ch8 + the template sit outside W1's contracted footprint (PLAYBOOK also being at silent-rule-ratchet headroom 1) · refs `scripts/batch_manifest.py` (HONEST LIMITS #2), `tests/test_batch_manifest.py`, `docs/audits/2026-08-07-technical-batch-2-packet.md` §2, ADR-110 amendment 2026-08-07, [#505] · kill-candidates: none — [#508] owns the enum coupling; no open row owns this scope · serialize-group: gates
