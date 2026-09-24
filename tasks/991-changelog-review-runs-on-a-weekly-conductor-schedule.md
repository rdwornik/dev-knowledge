---
id: "[#991]"
title: "`/changelog-review` runs on a weekly conductor schedule instead of an operator-invoked one-off"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#991] [P2][S] **`/changelog-review` runs on a weekly conductor schedule instead of an operator-invoked one-off** - D33: `/changelog-review` ran after a 2.5-month gap (77 CC versions, ~30 codex versions) because it is purely operator-invoked, matching the same "standing request went unactioned" shape the Copilot admission also shows · Done when: a conductor schedule (`.github/workflows/conductor.yml` or an equivalent cron surface) runs `/changelog-review` weekly; its ADOPT findings seed `docs/intake/` automatically rather than waiting for a manual paste; a witness scheduled run produces an intake seed with no operator invocation · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-opus55-harness.md` Part B, `.github/workflows/conductor.yml`, `docs/audits/2026-09-23-technical-window-defects-amend.md` · kill-candidates: none -- no open row schedules changelog-review
