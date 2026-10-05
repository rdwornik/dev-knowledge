---
id: "[#1362]"
title: "A removal engine finds what is no longer current and brings it to removal, and it outranks new features"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1362] [P1][L] **A removal engine finds what is no longer current and brings it to removal, and it outranks new features** - R56 (operator, 2026-10-03): the largest problem is that nothing continuously finds what has stopped being current -- mechanisms that never run, gates that catch nothing, superseded decisions, stale rows and documents -- and brings it to removal. It is built as code with an outcome test and ranks above new features. R66.2 adds the discipline: "no caller" by census is never enough; the dynamic-use check must read DEAD, and ALIVE or UNKNOWN is left in place and recorded. · Done when: (1) one command lists, from recorded data, the four classes (a mechanism with no recorded trigger, a gate with zero catches over its window, a superseded decision still cited, a stale row or document), each listing line ending in a proposed removal act; (2) an outcome test seeds one dead item per class into a fixture and the engine names all four, and a seeded ALIVE item is left in place and recorded; (3) the engine's own trigger is recorded in the harness (it is not an orphan); (4) the batch order ranks its row above new feature rows · owner: wave B2 W2 or later: a removal-engine lane; the operator performs the deletions (R66.2) · touches: a new removal-engine script and test (path TBD at build), `ecosystem/harness.yaml` (its fate line) · kill-candidates: `[#639]` -- it retires the verification organs that fire but never block, by measurement; this row is the standing engine that finds such organs, and `[#639]` becomes its first batch of input · refs `[#639]`, `protocols/STANDING_RULINGS.md` section AR (R56, R66) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R56 in `to-browser/RATIFICATION-2026-10-03.md R56`
