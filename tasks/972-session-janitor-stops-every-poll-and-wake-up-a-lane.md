---
id: "[#972]"
title: "Session janitor stops every poll and wake-up a lane leaves running at batch close"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#972] [P2][S] **Session janitor stops every poll and wake-up a lane leaves running at batch close** - D9: sessions left polls and scheduled wake-ups running after their work was done, 3 times this window, because "stop your own monitors" is a prose rule with no enforcement point · Done when: a batch-close step (the integrator's own close routine) enumerates and stops every Monitor, poll and background shell a batch's lanes started, and a witness batch shows 0 orphaned polls after close · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `to-cc/BATCH-WAVE5A-2026-09-23.md` (rule 6, Close) · kill-candidates: none -- no open row enumerates and stops lane-started background processes at batch close
