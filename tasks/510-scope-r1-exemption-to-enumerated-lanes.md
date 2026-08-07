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

- [#510] [P2][M] **Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today** — `batch_manifest.exempt()` keys condition 1 on branch SHAPE (`LANE_BRANCH_RE`), not the manifest's lane roster — any `worktree-lane-*` merge is exempt from `check_journal_spine_anchor` mid-batch, one `git branch -m` away. Batch 2 demonstrated it live (packet §2). **Assessed for S-fix, rejected as M** (reasoning: packet §2): no machine-readable roster today; `docs/audits/` immutability forces a prospective no-roster ruling; ripples into Ch8 + template + ADR-110. Push leg never consults the manifest (bounded blast radius). · Done when: the exemption resolves against a lane roster the open manifest declares, the no-roster posture is ruled and encoded, a test proves a lane branch OUTSIDE the roster is not exempt mid-batch, and Ch8 + the manifest template carry the field · refs `scripts/batch_manifest.py` (HONEST LIMITS #2), `tests/test_batch_manifest.py`, `docs/audits/2026-08-07-technical-batch-2-packet.md` §2, ADR-110 amendment 2026-08-07, [#505] · kill-candidates: none — [#508] owns the enum coupling; no open row owns this scope · serialize-group: gates
