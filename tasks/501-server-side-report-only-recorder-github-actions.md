---
id: "[#501]"
title: "Server-side report-only recorder (`.github/workflows/`) — records, never judges"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: architecture
generates: BACKLOG.md
---

- [#501] [P1][M] **Server-side report-only recorder (`.github/workflows/`) — records, never judges** — all hard gates here are client-side, so `git push --no-verify` erases any RED; a push-triggered Actions run re-runs them, leaving a tamper-evident record no local bypass reaches. Path operator-APPROVED; no dir until BUILD. Draft YAML + six earned requirements: `docs/audits/2026-08-06-technical-night-prep-packs.md`. Load-bearing: `fetch-depth: 0` (shallow grafts read as whole-file creations — 5 false `canonical_freshness` FAILs) and the exact uv pin `==0.11.19`. **REPORT-ONLY trajectory, and it stays there**: Free tier, repo private by standing ruling, so no promote-to-gate path exists and the ADR-at-arming has no live trigger until the tier changes; do not plan it early. NOT the [#255] object — that reversal killed a *PR-gate* organ as vacuous under local-merge; a recorder is different. · Done when: runs on push, records the gate outcome retrievably, judges nothing, and the owed ARCHITECTURE Ch2+Ch6 rows land with it · footprint: `.github/workflows/`, `ARCHITECTURE.md` · refs #255, #153 · kill-candidates: none — no row owns server-side recording · serialize-group: architecture
