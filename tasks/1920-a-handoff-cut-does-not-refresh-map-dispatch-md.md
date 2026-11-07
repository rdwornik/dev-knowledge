---
id: "[#1920]"
title: "A handoff cut does not refresh to-browser/MAP-DISPATCH.md"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1920] [P2][S] **A handoff cut does not refresh to-browser/MAP-DISPATCH.md** - `scripts/gen_handoff.py --cut` says it will "regenerate the LEDGER, seat-ids, MAP-DISPATCH and the reading-path file" (its `--cut` help) and writes the map to `DISPATCH_MAP_REL = "to-browser/MAP-DISPATCH.md"` (`scripts/gen_handoff.py:4229`), yet on 2026-11-07 the transport's `to-browser/MAP-DISPATCH.md` was last written 2026-10-28, after the 2026-11-05 cut ran, so the boot reading path (`scripts/handoff_state.py:921`) points the next seat at a stale map. Candidate (d), the refresh half, of to-browser/RATIFICATION-2026-11-07.md item 5; `[#1443]` puts the map on the reading path but nothing checks that a cut refreshed it. · touches: `scripts/gen_handoff.py`, `tests/test_gen_handoff.py` · kill-candidates: none - `[#1443]` owns the reading-path half only · refs `scripts/gen_handoff.py`, `[#1443]`, to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md · Done when: RED first - a cut over a fixture transport whose MAP-DISPATCH.md predates the cut leaves it rewritten from `--dispatch-map`'s output, and the cut refuses (naming the file) when the write did not happen; the lane-branch CI run is green outside known reds · decided-by: operator, to-browser/RATIFICATION-2026-11-07.md item 5 and Amendment 1 D1 · source: to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md section 6 (d)
