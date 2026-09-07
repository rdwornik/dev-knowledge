---
id: "[#641]"
title: "Declare a MEMORY.md byte budget, or rule that none is owed"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---

- [#641] [P3][S] **Declare a MEMORY.md byte budget, or rule that none is owed** — The ratified pre-handoff hygiene register (SUPPLEMENT ANSWERS Q7) carries a row 8 reading "MEMORY.md within cap". **There is no cap.** Measured 2026-09-07 over `scripts/`, `protocols/` and `tests/`: no MEMORY byte budget is declared anywhere in this repo, while the live file measures ~23,851 B. A budget is a DECISION and no lane owns it, so `gen_handoff._row_memory_within_cap` reads `canonical_docs.MEMORY_BYTE_BUDGET` via `getattr` and renders `[n/a-reason:NO-DECLARED-BUDGET]` while that name is absent — visible, never a silent pass, and it arms itself with no code change the moment the constant is declared. The operator's call is which of the two this is: a number (the repo's other byte budgets are decimal — `PASTE_BYTE_CEILING` 20,000, `HANDOFF_BOOT_BYTE_BUDGET` 18,000, `STATUS_BYTE_BUDGET` 5,000), or a ruling that an auto-maintained index needs no ceiling, in which case row 8 leaves the register rather than sitting n/a forever. · Done when: either `canonical_docs.MEMORY_BYTE_BUDGET` is declared with the measurement behind the number and the row is witnessed FAILing over it, or the row is struck from the register with the reason recorded · refs `scripts/gen_handoff.py` `_row_memory_within_cap`, `tests/test_gen_handoff_preflight.py::test_memory_row_is_not_applicable_while_no_budget_is_declared`, `protocols/HANDOFF_PROCESS.md` §5 (the 5,000-decimal precedent) · kill-candidates: none — the register's row 8 has no other carrier, and an n/a row with no owner is how a mis-specified row survives
