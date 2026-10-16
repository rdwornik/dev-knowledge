---
id: "[#1623]"
title: "plan_lint refuses a batch or night order whose dependent part names no trigger and no wait mechanism, or says \"do not poll\" without an armed wake (night contract N5)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1623] [P1][M] **plan_lint refuses a batch or night order whose dependent part names no trigger and no wait mechanism, or says "do not poll" without an armed wake (night contract N5)** - `scripts/plan_lint.py` lints lane contracts only (`parse_lane_contract`, `find_serial_mismatches`) and reads no batch or night order; `to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md` passed every gate with PART 5 "waits for 1537" and "do not poll" (`to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md` N5) · Done when: RED first: `tests/test_plan_lint_order_waits.py` runs the new `plan_lint.py check-order` rule on a fixture copy of `to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md` and asserts exit 1 naming the dependent part and the "do not poll" line, and exit 0 on a corrected fixture that names the trigger and a Monitor or cron wake; fails on main · touches: `scripts/plan_lint.py`, `tests/test_plan_lint_order_waits.py` · refs `[#1573]`, `[#689]` · source: BATCH-RESUME-NIGHT-2026-10-16 PART A step 1
