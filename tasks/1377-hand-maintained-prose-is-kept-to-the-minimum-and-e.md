---
id: "[#1377]"
title: "Hand-maintained prose is kept to the minimum, and each file that remains is held current by the harness"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1377] [P1][L] **Hand-maintained prose is kept to the minimum, and each file that remains is held current by the harness** - R79 item 2 (operator, 2026-10-04): "prose always loses", so prose is kept to the minimum, ideally one file; every hand-maintained prose file that remains must be part of the harness -- a generator, lint, gate or wake sweep keeps it current, or refuses when it is stale -- so that neither the next seat nor the harness can forget it; everything else is generated (R70). The survey that lists those files (path, writer, readers, generator) and recommends which become generated is in the session file of lane `b2-rulings-landing`; nothing was converted there. · Done when: for every file on that survey's list either a generator regenerates it, or a lint, gate or wake sweep refuses while it is stale, or it is deleted, shown by a re-run of the survey whose count of hand-maintained files with no such guard is 0; the seat's LEDGER is written by `gen_ledger.py` and a stale one is refused; the seat evaluates the recommendation before any conversion starts · owner: the architect seat evaluates the survey; wave B2 W2 lanes convert · touches: the files on the survey's list, `scripts/gen_ledger.py`, the lints, tests · kill-candidates: none -- `[#1331]` moves the ruling register and cross-window state into the repository, which this row extends to every remaining prose file · refs `[#1331]`, `scripts/gen_ledger.py`, `protocols/STANDING_RULINGS.md` section AR (R79) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R79 in `to-browser/RATIFICATION-2026-10-04.md R79`
