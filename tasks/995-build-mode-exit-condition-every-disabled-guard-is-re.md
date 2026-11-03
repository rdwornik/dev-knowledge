---
id: "[#995]"
title: "BUILD MODE exit condition: every disabled guard is re-armed with a live pass/fail test"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#995] [P1][M] **BUILD MODE exit condition: every disabled guard is re-armed with a live pass/fail test** - O-2d: the operator's re-arm-every-guard exit condition has no backlog row; several BUILD-MODE-disabled guards (prompts guard, ADR-77, logs_retention, block-onedrive, deny_and_point) sit off with no dated expiry beyond the 2026-11-18 backstop (`docs/audits/2026-09-23-technical-hook-architecture-appendix.md` A5) · Done when: each guard BUILD MODE disabled is re-armed with a live test proving a legitimate lane still passes and an illegitimate action is still refused, evidenced the same way LANE-W4B-6/W4B-0 re-armed the eight SessionStart hooks; the 2026-11-18 backstop is cited as the outer bound · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md`, `docs/audits/2026-09-23-technical-handoff-readiness.md` · kill-candidates: none -- no open row tracks this BUILD MODE exit condition
