### 2026-10-24 (k) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): ADR-131 status flip Proposed -> Accepted, landed through the K1 operator-act class (`land_lane.py --operator-act K1`) as the real-use witness for `[#1716]` Done-when 5

**Anchors:** `5e19b777b` (the held commit `89e23db1b`, tag `archive/adr-131-accept-2026-10-22`, cherry-picked clean onto main c8fd7e08c: ADR-131 status line, the `docs/decisions/README.md` index row, the generated `recent-adrs.md` roster line)

**Did:** the dispatcher (`7f9cba41-c2`) relayed the operator's 2026-10-24 ruling (Tech-Architect-47, item 2) to land the flip that K1 of `to-browser/RATIFICATION-2026-10-22.md` held "to land first through an operator-act landing class keyed by a ratification id". The flip applies to main without conflict (3 files, 3 lines, ADR-94 status-line exception only); the row `| K1 |` exists in the ratification file. K1's second clause (the landing adds a `DECISION_DISPOSITIONS` entry or an OPEN row with `implements: ADR-131`) is met by the already-landed open row `[#1716]`, whose body carries `implements: ADR-131`.

**Result:** recorded in the receipt (exit code, merge sha, CI run, the `Ratified-by:` line). `[#1716]` is NOT closed here: its Done-when 3 names a receipt `ratification` field that needs `scripts/merge_receipt.py`, which is not delivered; this landing is evidence for Done-when 1, 2, 4 and 5 only.

**Changes:** `docs/decisions/ADR-131-*.md` (status line), `docs/decisions/README.md`, `.claude/generated/recent-adrs.md`, `JOURNAL.md`.

**Next:** the operator-owned items in the dispatcher's receipt; batch E2.1 close 2026-10-31.

