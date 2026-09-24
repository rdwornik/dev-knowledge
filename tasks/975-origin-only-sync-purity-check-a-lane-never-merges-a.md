---
id: "[#975]"
title: "Origin-only sync + purity check: a lane never merges a local, unverified main"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#975] [P1][M] **Origin-only sync + purity check: a lane never merges a local, unverified main** - D12: a lane merged a local unverified `main` twice this window (contamination), because worktrees share refs and nothing checks that the base a lane merges against actually matches origin · Done when: every merge syncs with `git fetch origin` then `git merge origin/main` only (never a bare local main); the merge organ runs a purity check asserting the merged base matches `origin/main` before proceeding; a witness run against a deliberately stale local main refuses · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `to-cc/BATCH-WAVE5A-2026-09-23.md` (rule 3, Sync and purity) · kill-candidates: none -- no open row builds the purity check; lane-merge-path (W4B-1, deferred) is the broader merge-path unification this sits inside
