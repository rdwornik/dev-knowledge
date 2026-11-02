---
id: "[#392]"
title: "fleet_analytics rename-alias loses history on path-reuse"
status: closed
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#392] [P3][S] **fleet_analytics rename-alias loses history on path-reuse** — `scripts/fleet_analytics.py:326`'s global `old→new` alias map can't represent `a→b→a` (`canonical_path("a")` returns an untracked `b`), discarding older history → undercounts revisions/coupling/edit-age (terra 2026-07-22). Make rename resolution commit-time-aware, add a real-git rename-back regression test. · Done when: a rename-back sequence carries full history with a covering test · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §4, #384 · kill-candidates: none — fleet_analytics correctness fix · serialize-group: audit-py · **CLOSED 2026-11-02** — evidence a062d59d28fe553cd7941717f9da2cc7e45330b0
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-07-27 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
