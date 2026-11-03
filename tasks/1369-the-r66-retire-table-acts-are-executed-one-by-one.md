---
id: "[#1369]"
title: "The R66 retire-table acts are executed one by one, each under R59's dynamic-use check"
status: open
priority: P2
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1369] [P2][L] **The R66 retire-table acts are executed one by one, each under R59's dynamic-use check** - R66 (operator, 2026-10-03): the retire table is answered as the seat recommended. A1-A8: retire `propose_closures`, the never-used commands and templates, `coherence-nudge`; move the four zero-catch pre-commit hooks and `impacted-tests-guard` to CI; retire the static orphans only after the dynamic-use check; wire `read_gate`, `provider_router` and the watchdog; retire `deny_and_point` on 10-19. B1-B3: keep prompts-guard and repair it through `#863`'s root cause; retire the ADR-77 transcript guard and `logs_retention`. C1-C3: JOURNAL as a 30-day window plus a legacy file after re-measuring the 24 % figure; LESSONS frozen to a legacy file; ADR-82, -116, -117, -118 each ratified or withdrawn. E1-E3: chunked Gemini reads, a drafted agy bug report, the agy version in the registry. Deleting is the operator's act and this ruling is that act, still subject to R59. · Done when: a table in the batch digest has one row for each of A1-A8, B1-B3, C1-C3 and E1-E3 reading done or not done with its evidence (a sha or a file); every retirement row shows the dynamic-use check of `DIGEST-B2-PREP-2026-10-03` Part 1 read DEAD, and an item that read ALIVE or UNKNOWN is left in place and recorded; `deny_and_point` is retired on or after 2026-10-19 with its test pair; the 24 % figure is re-measured before the JOURNAL change; each of ADR-82, -116, -117, -118 carries a Status of Accepted or a withdrawal · owner: wave B2 W2: a retire lane; the operator files the drafted agy bug report and performs the deletions · touches: the retired scripts and their tests, `JOURNAL.md`, `LESSONS.md`, `docs/decisions/`, `ecosystem/provider-registry.yaml` · kill-candidates: `[#639]` -- it retires the verification organs that fire but never block; the R66 table is a superset it can be folded into · refs `[#639]`, `[#863]`, `protocols/STANDING_RULINGS.md` section AR (R66) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R66 in `to-browser/RATIFICATION-2026-10-03.md R66`
