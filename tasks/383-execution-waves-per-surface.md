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

- [#383] [P2][L] **Execution waves per surface** — once the schema exists, converge each L0/L2 surface (caches, the `.claude` surface incl. skills, archives-inside-each-folder, docs layout, Python parity, colours-via-carrier) one wave at a time, worktrees **singly, one in focus** (intake #16 §6 step 4). Replication-first: manifest/carrier material, never per-repo fixes. · wave record: `docs/audits/2026-08-03-technical-383-caches-wave-record.md` — surface naming, alias retirement, §4 correction; **§5 caches wave EXECUTED (1/6); (c) operator read PENDING** · Done when: for the 8 gitignore-effect rows at `ecosystem/parity-surfaces.yaml:834-899`, (a) `python scripts/desired_state_report.py` shows no `diverge` cell on any of the 8 rows; AND (b) `python scripts/fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared, 0 must-absent and 0 tombstone-violated across those same 8 rows for every repo it walks, with any repo it could not walk named in the wave record rather than counted as clean; AND (c) both runs are pasted verbatim into the wave record and the operator has read them. · refs docs/intake/2026-07-21-func-fleet-north-star.md §6 step 4 · serialize-group: architecture
