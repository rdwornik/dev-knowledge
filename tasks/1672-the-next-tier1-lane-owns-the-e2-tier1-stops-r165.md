---
id: "[#1672]"
title: "The next tier1 lane owns tests/test_conductor.py and scripts/gen_handback.py to finish the [#1560] remainder and the [#1563] removal (R165, interim)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1672] [P1][M] **The next tier1 lane owns tests/test_conductor.py and scripts/gen_handback.py to finish the [#1560] remainder and the [#1563] removal (R165, interim)** - The e2-tier1 lane STOPped (`to-browser/REFUSED-e2-tier1.md`): the [#1560] remainder is four assertions in `tests/test_conductor.py`; [#1563] is `tests/test_conductor.py:647-692` and `scripts/gen_handback.py:813-891` · owner: the next tier1 lane · Done when: (1) the [#1560] remainder (the four assertions) is done with the RED shown first; (2) the [#1563] removal is done in both files; (3) the tier1 job's wall time and the both-OS pytest legs are re-measured on a real push run and the run id recorded · touches: `tests/test_conductor.py`, `scripts/gen_handback.py` · kill-candidates: `[#1563]` -- this row carries its removal; `[#1560]` -- this row carries its remainder · refs `[#1560]`, `[#1563]`, `[#1561]`, `[#703]` · decided-by: the operator, 2026-10-20, R165 (RATIFICATION-2026-10-20 v1), INTERIM under R166; OQ3 GO given by R155 · source: lane e2-rows-r164 (`BATCH-E2-NIGHT-2026-10-19` v3)
