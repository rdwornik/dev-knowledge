---
id: "[#819]"
title: "A lane's hub half can merge while its win-tooling half sits unmerged, undetected"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#819] [P1][M] **A lane's hub half can merge while its win-tooling half sits unmerged, undetected** - Found 2026-09-16 while lane-ab-810 reconciled tracked-vs-deployed drift on win-tooling's `DispatchHelpers.psm1`. Lane `worktree-lane-u-000-dispatch-receipt-is-work` was a two-repo lane (`.dev-knowledge` + win-tooling), reviewed, tested (105/105), committed and pushed on BOTH repos on 2026-09-07. Its hub half (PLAYBOOK.md Ch8 row 5) merged to `.dev-knowledge` main the same day. Its win-tooling half did **not** merge -- `origin/worktree-lane-u-000-dispatch-receipt-is-work` sat pushed-but-unmerged for **9 days**, discovered only because this lane happened to touch the same file. Nothing in either repo's integration path checks that a two-repo lane's halves land together, or flags one landing without the other. · **WHY THIS MATTERS BEYOND THIS ONE INSTANCE.** A two-repo lane's Done-contract is written as if merge were one event; it is actually two independent merges in two independent repos with no shared gate. A partial landing is invisible from either repo alone -- `.dev-knowledge` main shows a clean merge with no sign its counterpart is missing; win-tooling main shows nothing unusual about a branch that simply hasn't been merged yet, indistinguishable from one still in review. See `[#821]` for the specific hazard this particular split produced. · Done when: a two-repo lane's contract or its HANDBACK records BOTH repos' target commits, and some surface (an integration checklist item, a scheduled probe, or a gate) can compare "is repo A's half landed" against "is repo B's half landed" and flag a split lane within one integration cycle of it appearing -- not 9 days · refs `origin/worktree-lane-u-000-dispatch-receipt-is-work` (win-tooling, merged 2026-09-16), `.dev-knowledge` JOURNAL 2026-09-07, win-tooling `docs/audits/2026-09-07-codex-lane-u-000-dispatch-receipt-is-work.md`, `H:\My Drive\CLAUDE PROMPT DIR\to-browser\archive\2026-09-07\SESSION-lane-u-000-dispatch-receipt-is-work.md`, `[#821]` · kill-candidates: none -- newly filed · source: operator ruling 2026-09-16 (third ruling), lane-ab-810
