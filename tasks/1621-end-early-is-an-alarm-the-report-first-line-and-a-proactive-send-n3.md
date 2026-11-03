---
id: "[#1621]"
title: "END-EARLY is an alarm: first line of the report plus a proactive send to the operator (night contract N3)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1621] [P1][S] **END-EARLY is an alarm: first line of the report plus a proactive send to the operator (night contract N3)** - no early-end alarm existed; the report was on the transport at 01:32 and was read at about 02:50 only because the operator was in the browser seat (`to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md` N3) · Done when: RED first: `tests/test_night_contract_templates.py` asserts the common-rules template orders `END-EARLY <reason>` as the first line of the report and a SendUserFile `status: proactive` send, and `transport_lint.py check` accepts a report whose first body line is `END-EARLY <reason>`; fails on main · touches: `templates/batch-common-rules-template.md`, `scripts/transport_lint.py` if the lint refuses the line, tests · refs `[#1573]`, `[#689]` · source: BATCH-RESUME-NIGHT-2026-10-16 PART A step 1
