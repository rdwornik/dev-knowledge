---
id: "[#964]"
title: "One verification stage -- every check runs once at merge, results reused"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#964] [P1][M] **One verification stage -- every check runs once at merge, results reused** - D1 (`docs/audits/2026-09-23-technical-window-defects.md`): a wave-4b merge costs 77-207 min pickup-push because `gates.py`, `test_pairing.py compare` and ad-hoc re-runs each re-verify overlapping ground -- no single stage owns total verification time, so the same tests run 2-3x per merge (`docs/audits/2026-09-23-technical-verify-time.md`) · Done when: one verification stage exists where each check (health, ship-gate, ruff, impacted-tests, compare) runs exactly once per merge and every consumer reads its recorded result rather than re-invoking it; a witness merge shows 0 duplicate check invocations against today's 2-3x · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-verify-time.md`, `docs/audits/2026-09-23-technical-window-defects.md`, `scripts/gates.py`, `scripts/test_pairing.py` · kill-candidates: none -- no open row owns total per-merge verification time as a single stage
