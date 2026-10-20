---
id: "[#1693]"
title: "The census reads the dead and collected files without handling a BOM, so the first id is corrupted"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1693] [P3][S] **The census reads the dead and collected files without handling a BOM, so the first id is corrupted** - Copilot major: `dead.txt` and the collected list are read with the default codec, a UTF-8 BOM prefixes the first line and that id never matches · owner: a census-tool lane · Done when: (1) RED first: a BOM-prefixed file yields the same ids as a clean one; (2) real-use witness: the census over a PowerShell-written `dead.txt` matches its first id · touches: `scripts/test_census.py` · kill-candidates: `[#1566]` -- the census tool; `[#1341]` -- encoding · refs `[#1566]`, `[#1341]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: major finding of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
