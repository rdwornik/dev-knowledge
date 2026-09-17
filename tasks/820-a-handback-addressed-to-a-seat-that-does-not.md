---
id: "[#820]"
title: "A HANDBACK addressed to a seat that does not exist is an abandoned lane, not a dispatched one"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#820] [P2][S] **A HANDBACK addressed to a seat that does not exist is an abandoned lane, not a dispatched one** - Found 2026-09-16 while lane-ab-810 traced why `worktree-lane-u-000-dispatch-receipt-is-work`'s win-tooling half sat unmerged for 9 days despite being DONE, reviewed and pushed. Its `SESSION` HANDBACK addressed the win-tooling half to an integrator seat ("integrator-N2") that was never instantiated to receive it -- the lane did everything asked of a lane (commit, push, honest deviation log, explicit "ordering hazard" warning for whoever integrates next) and then had no receiving seat on the other end. A batch dispatched with no receiving seat is abandoned, not dispatched -- the lane cannot know its HANDBACK landed nowhere, and nothing on the integrator side alerts on a HANDBACK addressed to a seat that is not live. · Done when: a HANDBACK naming a receiving seat is checked against that seat's actual existence/liveness at handback time (or shortly after), and a HANDBACK addressed to a non-existent or already-retired seat is surfaced rather than silently sitting unread -- at minimum, a scheduled probe over open HANDBACKs vs. live seats, with a RED-first witness reproducing this instance's shape (a named seat with no matching live session) · refs `H:\My Drive\CLAUDE PROMPT DIR\to-browser\archive\2026-09-07\SESSION-lane-u-000-dispatch-receipt-is-work.md`, `[#819]`, `[#821]` · kill-candidates: none -- newly filed · source: operator ruling 2026-09-16 (third ruling), lane-ab-810
