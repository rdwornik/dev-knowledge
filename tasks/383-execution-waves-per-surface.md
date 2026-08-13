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

- [#383] [P2][L] **Execution waves per surface** — converge the six L0/L2 surfaces one wave at a time, worktrees **singly, one in focus**. · wave record: `docs/audits/2026-08-03-technical-383-caches-wave-record.md` — **§5 caches wave EXECUTED (1/6); (c) operator read PENDING** · Done when: for every `kind: gitignore-effect` row in `ecosystem/parity-surfaces.yaml`, (a) `desired_state_report.py` shows no `diverge` cell on those rows; AND (b) `fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared / 0 must-absent / 0 tombstone-violated across them for every repo it walks, naming any repo it could not walk rather than counting it clean; AND (c) both runs are pasted verbatim into the wave record and the operator has read them. · **RE-SCOPED at ARC2 to that `kind:` selector, off line ranges** (register M-7 `N2-R1-06`): the old range had drifted onto different rows and the set had grown 8 → 9, making (a)/(b) unverdictable; a selector survives layout edits, so no count is restated above · refs docs/intake/2026-07-21-func-fleet-north-star.md §6 step 4 · serialize-group: architecture
