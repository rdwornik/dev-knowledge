---
id: "[#1620]"
title: "A session ends only when every part is DONE or BLOCKED-WITH-OWNER, or its stop condition fires (night contract N2)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1620] [P1][S] **A session ends only when every part is DONE or BLOCKED-WITH-OWNER, or its stop condition fires (night contract N2)** - the night order said "then end the session" and carried no time window; the session ended at 01:32 after USD 9.15 with PARTs 5-6 unrun and nothing happened for 8 h (`to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md` N2) · Done when: RED first: `tests/test_night_contract_templates.py` asserts the common-rules template defines BLOCKED-WITH-OWNER as a named owner + a named event + a re-check time, states a night run's window as "until 08:00 local" unless the order says otherwise, and calls running out of parts early an END-EARLY; fails on main · touches: `templates/batch-common-rules-template.md`, tests · refs `[#1573]`, `[#689]` · source: BATCH-RESUME-NIGHT-2026-10-16 PART A step 1
