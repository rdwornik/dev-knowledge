---
id: "[#457]"
title: "Two live-repo tests fail on main against green gates — test-vs-organ mismatch"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#457] [P2][S] **Two live-repo tests fail on main against green gates — test-vs-organ mismatch** — **(i)** `test_check_fleet_parity_green_on_live_repo` asserts raw findings, ignoring the disposition register: the ai-council `conftest.py` WARN (dispositioned ref [#430] in the gate path) REDs the test while ship-gate is GREEN; fix = make the test disposition-aware (assert through the gate's filter). **(ii)** `test_routine_consumers_live_backlog_governs_exactly_one_row` pins "1 declared routine row"; the live check reports 2 — VERIFY which side is right (census the six-field rows vs ADR-105) BEFORE repinning; never assume the pin. Both inherited; witnessed on bare main 2026-07-31 at the [#382] W1/W2 boundaries. RED-first when built. · Done when: both tests pass on main for verified reasons (disposition-aware assertion; census-verified pin), verification recorded in the fixing commit · refs tests/test_audit.py, scripts/audit.py, ecosystem/disposition-register.yaml, #430, #348, #426 · kill-candidates: none — [#430] owns the parity-verdict defect, not the test's disposition-blindness; no row owns the stale pin · serialize-group: audit-py
