---
id: "[#1678]"
title: "`write_fate` and `write_step(fate=)` are duplicate writers of the same fate record (H6)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1678] [P3][S] **`write_fate` and `write_step(fate=)` are duplicate writers of the same fate record (H6)** - `scripts/codespace_regime.py:260` `write_fate` and `scripts/dispatch.py:3156` `write_step` both write a lane fate, so a fate can be recorded two ways with different fields · owner: a codespace lane · Done when: (1) RED first: a test shows the two writers producing different records for one fate; (2) one writer, the other delegates; (3) real-use witness: a codespace-exec run writes one fate record that both readers accept · touches: `scripts/codespace_regime.py`, `scripts/dispatch.py` · kill-candidates: `[#1632]` -- one substrate protocol; `[#1551]` -- plan vs exec sequence · refs `[#1632]`, `[#1551]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H6 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
