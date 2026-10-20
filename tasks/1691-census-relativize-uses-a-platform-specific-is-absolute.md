---
id: "[#1691]"
title: "The census `relativize` uses a platform-specific `is_absolute`, and backslash relative paths slip through (test_census.py:462)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1691] [P2][S] **The census `relativize` uses a platform-specific `is_absolute`, and backslash relative paths slip through (test_census.py:462)** - Copilot's major and Codex's major at `scripts/test_census.py:462`: a backslash relative path is judged absolute or relative by the running OS, so the same tree buckets differently on Windows and Linux · owner: a census-tool lane · Done when: (1) RED first: a backslash relative path is relativized the same on both OSes; (2) real-use witness: the census over this repo gives identical ids on Windows and ubuntu · touches: `scripts/test_census.py` · kill-candidates: `[#1566]` -- the census tool; `[#1568]` -- same · refs `[#1566]`, `[#1568]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: major finding of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
