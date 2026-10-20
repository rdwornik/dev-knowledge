---
id: "[#1692]"
title: "The census `_live_edges` and `classify` compare with posix separators, so Windows paths do not match"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1692] [P2][S] **The census `_live_edges` and `classify` compare with posix separators, so Windows paths do not match** - Copilot major: `_live_edges`/`classify` build and compare paths with '/' while Windows inputs carry '\', so edges are missed and tests fall to the wrong bucket · owner: a census-tool lane · Done when: (1) RED first: a Windows-style path classifies like its posix twin; (2) real-use witness: the Windows census run reports the same bucket counts as ubuntu · touches: `scripts/test_census.py` · kill-candidates: `[#1566]` -- the census tool · refs `[#1566]`, `[#1568]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: major finding of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
