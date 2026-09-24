---
id: "[#993]"
title: "BUILD MODE exit condition 1: the connection walk is clean on main, xfail removed"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#993] [P1][M] **BUILD MODE exit condition 1: the connection walk is clean on main, xfail removed** - O-2a (`docs/audits/2026-09-23-technical-handoff-readiness.md` §6): the operator's BUILD MODE exit condition 1 has no backlog row, so its state (the strict xfail still present, per `docs/audits/2026-09-23-technical-state-of-the-harness.md` §1) is tracked only in prose · Done when: the connection walk (`tests/test_connection_loop.py`) is green on main with `EXPECTED_STOPS` empty and the strict xfail deleted · implements: ADR-120 · refs `tests/test_connection_loop.py`, `docs/audits/2026-09-23-technical-state-of-the-harness.md`, `docs/audits/2026-09-23-technical-handoff-readiness.md` · kill-candidates: none -- no open row tracks BUILD MODE exit condition 1
