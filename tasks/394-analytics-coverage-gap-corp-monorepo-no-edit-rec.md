---
id: "[#394]"
title: "Analytics coverage gap — corp-monorepo no-edit-record blind spot"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#394] [P3][S] **Analytics coverage gap — corp-monorepo no-edit-record blind spot** — the run found 311/812 files (38%) in corp-monorepo with NO meaningful-edit record (touched only in wide commits or <3-line churn) → invisible to the rot frame (measurement blind spot, NOT rot). An L5b/reporter improvement, not a corp-monorepo defect. Decide: widen the meaningful-churn heuristic, add a diagnostic frame, or accept-and-document the limit. · Done when: the blind-spot is measured + heuristic widened or limit documented · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §5, #384 · kill-candidates: none — analytics-coverage improvement from #384 · serialize-group: audit-py
