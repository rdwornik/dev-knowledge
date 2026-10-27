### 2026-10-25 (q) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): lane seat-cycle-fix lands: a cycled orchestrator seat now takes its successor model from the registry row `seat-dispatcher` (D9) and is named `<role>-<batch>-cycle-<n>`

**Anchors:** `0ab396f04` (the lane tip: successor model from the seat-dispatcher row, successor named `<role>-<batch>-cycle-<n>`), `3676b43ff` (RED seat-cycle contract tests)

**Did:** merged `origin/worktree-seat-cycle-fix` @ `0ab396f04` onto main `36e14d01f` (2 lane commits, base `c8fd7e08c`, clean, no generated-file conflict; `scripts/seat_cycle.py` and four seat-cycle test files, two of them new). Regenerated `ecosystem/doc-counts.md` (the lane's handback names that as the integrator's). The lane's own tests (`test_seat_cycle*.py`, `test_model_id_single_source.py`) pass here, 60 of 60.

**Result:** `successor_model("orchestrator")` reads `seat-dispatcher` and `successor_model("integrator")` reads `seat-integrator`, so no model literal sits in `scripts/`. The `bound --cycle` value stays the handed-over cycle while the name carries cycle+1; both reviewers flagged that and the lane kept it (DECIDED-BY-LANE).

**Changes:** `scripts/seat_cycle.py`, `tests/test_seat_cycle.py`, `tests/test_seat_cycle_bound.py`, `tests/test_seat_cycle_model_row.py`, `tests/test_seat_cycle_name.py`, `ecosystem/doc-counts.md`, `logs/MERGE-RECEIPTS.jsonl`, `JOURNAL.md`.

**Next:** registry-grok-share, then the box lanes once their rulings are recorded.

