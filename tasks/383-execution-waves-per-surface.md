---
id: "[#383]"
title: "Execution waves per surface"
status: open
priority: P2
size: L
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
serialize-group: architecture
generates: BACKLOG.md
---

- [#383] [P2][L] **Execution waves per surface** — once the schema exists, converge each L0/L2 surface (caches, the `.claude` surface incl. skills, archives-inside-each-folder, docs layout, Python parity, colours-via-carrier) one wave at a time, worktrees **singly, one in focus** (intake #16 §6 step 4). Replication-first: manifest/carrier material, never per-repo fixes. · wave record: `docs/audits/2026-08-03-technical-383-caches-wave-record.md` — surface naming, alias retirement, §4 correction; **§5 caches wave EXECUTED (1/6); (c) operator read PENDING** · Done when: for every row selected by `kind: gitignore-effect` in `ecosystem/parity-surfaces.yaml` (**the selector is the subject** — not a line range and not a count; 9 rows at the 2026-08-12 measurement, `:910-978`), (a) `python scripts/desired_state_report.py` shows no `diverge` cell on any of the 8 rows; AND (b) `python scripts/fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared, 0 must-absent and 0 tombstone-violated across those same selected rows for every repo it walks, with any repo it could not walk named in the wave record rather than counted as clean; AND (c) both runs are pasted verbatim into the wave record and the operator has read them. · **RE-SCOPED 2026-08-12** (operator adjudication; register `protocols/STANDING_RULINGS.md` M-7 / `N2-R1-06`): legs (a)/(b) were the finest-phrased clauses in the corpus and still unverdictable, because their **subject was pinned by line range** — `:834-899` holds different rows entirely, and the `kind: gitignore-effect` rows had moved to `:910-978` and grown from 8 to 9. The repair is a **selector**, not a location: the clauses now name what the rows *are*, so the subject survives every future edit to the file's layout. · refs docs/intake/2026-07-21-func-fleet-north-star.md §6 step 4 · serialize-group: architecture
