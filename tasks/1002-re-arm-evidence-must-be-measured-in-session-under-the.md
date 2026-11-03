---
id: "[#1002]"
title: "Re-arm evidence must be measured in-session, under the real concurrent hook set, over 20+ events"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1002] [P1][S] **Re-arm evidence must be measured in-session, under the real concurrent hook set, over 20+ events** - S2 proposed row 2: the W4B-0 re-arm evidence method (one isolated run per hook) did not predict in-session cost -- isolated runs measured 1-4s while the same hooks took 7-16s in real boots (`docs/audits/2026-09-23-technical-hook-architecture-appendix.md` A2) · Done when: a hook is admitted or re-armed only on 20 or more real events under the concurrent hook set for its event, measured from transcript attachments; `surface_triage.ps1` is folded into the S2-1 reader or re-measured this way before being trusted again · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md` · kill-candidates: none -- no open row sets an in-session admission bar for hook re-arming
