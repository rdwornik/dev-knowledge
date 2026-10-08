---
id: "[#1436]"
title: "One handoff-readiness command runs the whole cut pipeline in a scratch clone and gates every real cut"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1436] [P1][L] **One handoff-readiness command runs the whole cut pipeline in a scratch clone and gates every real cut** - Every blocker of the 2026-10-06/07 cut surfaced at the last step, after the seat had finished its part, and the first cut attempts stopped one failure at a time. The readiness dry run of 2026-10-07 (a scratch clone, a scratch transport, every stage run whatever the previous one did) listed all of them at once. R90 (a) makes that a command and a gate · Done when: `gen_handoff.py readiness` (or its own module) clones origin/main into a scratch folder, copies the transport, then runs the preflight, the cut, the SUPPLEMENT fill from PLAN-HANDOFF section 4 with the five-label check, assemble, residual completeness, every probe including P13, the organ set, the `--filled` re-render, the row filing and the commit gates -- never stopping at the first failure -- and prints every failure with its raw exit code; it writes a READY receipt keyed to the source sha, a digest of the transport files it read and the cut date; the real cut refuses without a matching receipt, and the batch-close moment runs it in place of the trial cut; tests · owner: the handoff generator · touches: `scripts/gen_handoff.py` or a new module, the batch-close moment, tests · kill-candidates: `[#1432]`, `[#1433]` -- both close inside this command · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
