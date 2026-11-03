---
id: "[#392]"
title: "fleet_analytics rename-alias loses history on path-reuse"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#392] [P3][S] **fleet_analytics rename-alias loses history on path-reuse** — `scripts/fleet_analytics.py:326`'s global `old→new` alias map can't represent `a→b→a` (`canonical_path("a")` returns an untracked `b`), discarding older history → undercounts revisions/coupling/edit-age (terra 2026-07-22). Make rename resolution commit-time-aware, add a real-git rename-back regression test. · Done when: a rename-back sequence carries full history with a covering test · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §4, #384 · kill-candidates: none — fleet_analytics correctness fix · serialize-group: audit-py
