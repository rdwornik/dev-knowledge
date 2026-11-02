---
id: "[#994]"
title: "BUILD MODE exit condition 2: one real backlog row travels row-to-merge through the whole loop"
status: open
priority: P1
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#994] [P1][L] **BUILD MODE exit condition 2: one real backlog row travels row-to-merge through the whole loop** - O-2b: the operator's BUILD MODE exit condition 2 has no backlog row; today only a toy task has driven the connection walk end to end (`docs/audits/2026-09-23-technical-state-of-the-harness.md` §3, 'Still NONE on a real row') · Done when: one non-toy OPEN backlog row travels row-to-merge through the whole 16-stage loop with operator touches limited to filing the task and giving the GO, evidenced by its receipts · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-state-of-the-harness.md` §6 Track A item 5, `docs/audits/2026-09-23-technical-handoff-readiness.md` · kill-candidates: none -- no open row tracks BUILD MODE exit condition 2
