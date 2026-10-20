---
id: "[#1695]"
title: "The census maps UNKNOWN to KEEP, so an unclassifiable test is kept silently instead of surfaced"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1695] [P2][S] **The census maps UNKNOWN to KEEP, so an unclassifiable test is kept silently instead of surfaced** - Copilot major: a test the classifier cannot place becomes KEEP, hiding the gap; the removal decision then rests on a default, not on evidence · owner: a census-tool lane · Done when: (1) RED first: an unclassifiable test stays UNKNOWN in the output; (2) real-use witness: the census report counts UNKNOWN as its own line · touches: `scripts/test_census.py` · kill-candidates: `[#1566]` -- the census tool · refs `[#1566]`, `[#1568]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: major finding of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
