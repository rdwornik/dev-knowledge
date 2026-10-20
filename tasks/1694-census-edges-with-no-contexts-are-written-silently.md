---
id: "[#1694]"
title: "The census writes an edge that has no contexts without a warning"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1694] [P3][S] **The census writes an edge that has no contexts without a warning** - Copilot major: an edge with an empty contexts list is written to the output as if grounded, so a reader cannot tell a proven edge from an empty one · owner: a census-tool lane · Done when: (1) RED first: an edge with no contexts is flagged or refused; (2) real-use witness: the census output over this repo lists zero unflagged context-less edges · touches: `scripts/test_census.py` · kill-candidates: `[#1566]` -- the census tool · refs `[#1566]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: major finding of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
