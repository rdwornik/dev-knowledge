---
id: "[#1619]"
title: "A dependency on another session's event is a WAIT, never a skip (night contract N1)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1619] [P1][S] **A dependency on another session's event is a WAIT, never a skip (night contract N1)** - the 2026-10-15 night order said "Part 5 waits for 1537 on main; check once per finished part and do not poll" and "land nothing while an INTEGRATOR claim is live ... otherwise leave them pushed"; the seat skipped PART 5/6 and left both branches unlanded (`to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md` N1; `to-browser/DIGEST-NIGHT-CLOSEOUT-2026-10-15.md` section 1). `templates/batch-common-rules-template.md` section 4 says "No cron, no scheduled wake-ups" and names no rule for a part blocked on an outside event · Done when: RED first: `tests/test_night_contract_templates.py` asserts `templates/batch-common-rules-template.md` carries a rule that a part blocked on another session's event arms a Monitor or cron wake on that event and resumes, that the section-4 ban is scoped to wakes that outlive the session, and that the dispatcher, integrator and lane templates point at it; fails on main · touches: `templates/batch-common-rules-template.md`, `templates/dispatcher-order-template.md`, `templates/integrator-order-template.md`, `templates/lane-contract-template.md`, tests · refs `[#1573]`, `[#689]` · source: BATCH-RESUME-NIGHT-2026-10-16 PART A step 1
