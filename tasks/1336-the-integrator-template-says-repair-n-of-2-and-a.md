---
id: "[#1336]"
title: "The integrator template says \"repair N of 2\" and \"a lane refused twice is FAILED\" two lines apart"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1336] [P3][S] **The integrator template says "repair N of 2" and "a lane refused twice is FAILED" two lines apart** - `templates/integrator-order-template.md:73` has the refusal file carry `repair N of 2`, and `:74` says "A lane refused twice is `FAILED`"; `templates/dispatcher-order-template.md:88` repeats `repair N of 2`. A lane refused twice has used both repairs only if the second refusal is not itself repaired -- the two sentences give a seat no way to tell whether a third attempt exists or whether repair 2 is attempted after refusal 2. Filed by lane foundation-1-honest-green, which does not edit those lines (N9) · Done when: both templates state one rule -- how many repairs a lane gets and which refusal marks it FAILED -- in the same words, and a test pins the two templates to the same number · touches: `templates/integrator-order-template.md`, `templates/dispatcher-order-template.md` · kill-candidates: none -- no open row tracks the refusal-count wording · refs `templates/integrator-order-template.md`, `templates/dispatcher-order-template.md`, `scripts/dispatch.py` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
