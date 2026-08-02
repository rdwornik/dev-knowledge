---
id: "[#476]"
title: "`session_end_backpressure`'s dirty-tree leg flags the fleet-audit dailies that are untracked-on-main BY DESIGN"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#476] [P2][S] **`session_end_backpressure`'s dirty-tree leg flags the fleet-audit dailies that are untracked-on-main BY DESIGN** — fired 4x in one session (2026-08-02) on two `ecosystem/*/history/` dailies that session never touched. They are lane-owned (ADR-80/ADR-84: the durable record lives on `automation/fleet-audit`; `.gitignore` says so), so every repair it implied was wrong: committing to `main` breaks lane ownership, deleting destroys records, stashing churns files already safe on origin. A guard that fires on correct state trains the operator to ignore it. Mechanism, not tolerance — excuse an untracked `ecosystem/*/history/` path **only when `ls-tree` proves that exact file is on the lane tip** — never a blind pattern exclude, so a stray file and an unreplicated daily both still flag. · Done when: a lane-present daily no longer flags, a stray untracked file under `history/` still flags, a daily absent from the lane still flags, and tests pin all three · refs ADR-80, ADR-84, ADR-85, scripts/session_end_backpressure.py, .gitignore · kill-candidates: none — no open row owns backpressure false-positives; [#426] covers routine consumers, a different organ
