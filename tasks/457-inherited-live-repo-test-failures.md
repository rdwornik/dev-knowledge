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

- [#457] [P2][S] **Two live-repo tests fail on main against green gates — test-vs-organ mismatch** — **(i)** `test_check_fleet_parity_green_on_live_repo` asserts raw findings, ignoring the disposition register; fix = assert through the gate's filter. **2026-08-03 night batch:** the stated cause is INCOMPLETE — in a pristine clone with hooks UNARMED it fails on the `hooks_armed` WARN instead, and PASSES once armed. It is blind to WHATEVER WARN is live, not only the ai-council `conftest.py` one ([#430]). **(ii)** `test_routine_consumers_live_backlog_governs_exactly_one_row` pins "1 declared routine row"; the live check reports 2 — census DONE (JOURNAL j): 3 stale sites, not a bare repin. Both inherited; witnessed on bare main 2026-07-31 at the [#382] W1/W2 boundaries. RED-first. · Done when: both tests pass on main for verified reasons (filter-aware assertion; census-verified pin), verification recorded in the fixing commit · refs tests/test_audit.py, scripts/audit.py, ecosystem/disposition-register.yaml, #430, #348, #426 · kill-candidates: none — [#430] owns the parity-verdict defect, not the test's WARN-blindness; no row owns the stale pin · serialize-group: audit-py
