### 2026-10-24 (n) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): lane land-lane-receipt-anchor (P1, `[#1721]`, H1-X) -- the M2 receipt merge of a `land_lane.py` landing no longer leaves main's first-parent spine unanchored, and a failed baseline push is surfaced; landed through `merge_path.py` as a recorded FALLBACK because it fixes `land_lane` itself

**Anchors:** `7919fc261` (the lane tip), `fb5f8872b` (receipt rule append-only, iterative, failed baseline push surfaced), `c8ce1d67a` (a `land_lane` landing keeps main's spine anchored: the receipt merge is covered by its landing's anchor)

**Did:** merged `origin/worktree-land-lane-receipt-anchor` @ `7919fc261` (10 lane commits, base `36b14291e` = main, clean merge, 8 files: `scripts/journal_anchor.py`, `scripts/merge_path.py`, `scripts/land_lane.py`, `tests/test_land_lane.py`, three new `tests/test_land_lane_receipt_anchor*.py`, task 1721). Registered `[#1721]` in `tasks/manifest.json` after `[#1716]` (story `[S28]`), regenerated `BACKLOG.md` and `ecosystem/doc-counts.md`, re-bound the `ecosystem/process-binding.yaml` anchors the edit moved. Dispatcher order (orchestrator-e2-1-cycle-2, operator rulings RATIFICATION-2026-10-24 (b), H1-X): this lane lands first, through `merge_path.py`, one merge; then the integrator's landing hold lifts.

**Result:** the lane's witness is the NEXT `land_lane.py` landing (`journal_anchor.unanchored_on_spine origin/main` == `[]` with no hand anchor, and `refs/heads/worktree-integrate-<batch>` == main); this landing itself runs the OLD code and is made by `merge_path.land` with no M2, so its merge-receipt ledger line is carried by that next landing. `[#1721]` stays OPEN (Done-when 4 is that witness).

**Changes:** `scripts/journal_anchor.py`, `scripts/merge_path.py`, `scripts/land_lane.py`, `tests/`, `tasks/1721-*.md`, `tasks/manifest.json`, `BACKLOG.md`, `ecosystem/doc-counts.md`, `ecosystem/process-binding.yaml`, `JOURNAL.md`.

**Next:** known-reds-extend and KR-1 (deadline 2026-10-30), then ci-one-verdict-2 (parked, redo on the new main), then the queued lanes.

