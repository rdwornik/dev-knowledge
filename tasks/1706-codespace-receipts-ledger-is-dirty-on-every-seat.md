---
id: "[#1706]"
title: "CODESPACE-RECEIPTS.jsonl keeps every seat's tree dirty and the Stop hook says commit it"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1706] [P2][S] **CODESPACE-RECEIPTS.jsonl keeps every seat's tree dirty and the Stop hook says commit it** - `logs/CODESPACE-RECEIPTS.jsonl` is a tracked file (`git ls-files` lists it) that the primary carries modified all day, so `check_dirty_tree` (`scripts/session_end_backpressure.py:470`) sees a dirty tree on every seat, fires the Stop nudge (the trigger of `[#1700]`) and tells each seat to commit a peer's work-in-progress (the case `[#739]` records); `.gitignore` has no entry for it and the hook has no exclusion for it (`_is_lane_owned_daily` covers `ecosystem/*/history` dailies only); the name is undated on purpose (`scripts/codespace_regime.py:70-78`) so `logs_retention.py` does not move it · owner: a Stop-hook or ledger-home lane · Done when: (1) RED first: a test shows the hook reports a dirty tree when only `logs/CODESPACE-RECEIPTS.jsonl` changed; (2) the receipts live where a seat never sees them as dirty (untracked and ignored, or a path `check_dirty_tree` excludes) and the integrator's carry of the ledger is kept; (3) real-use witness: on the primary with a new receipt line written, `git status --porcelain` and the Stop hook both read clean · touches: `scripts/session_end_backpressure.py`, `.gitignore`, `scripts/codespace_regime.py`, `tests/test_session_end_backpressure.py` · kill-candidates: `[#739]` -- the authorship half, left open; `[#1658]` -- writes the close row into this same ledger, so the new home must keep its Done-when 1 witness · refs `[#739]`, `[#1700]`, `[#1658]`, `[#417]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-e2-startup-bisect.md` Item 5 and the memory topic stop-backpressure-orders-you-to-commit-a-peers-wip

Lane startup-tokens 2026-10-23 took the hook-exclusion route (`check_dirty_tree` skips exactly `logs/CODESPACE-RECEIPTS.jsonl`; RED tests in tests/test_session_end_backpressure.py): on a throwaway clone with a new receipt line the Stop hook is silent. Done-when (3) is only half met: `git status --porcelain` still lists the ledger as modified, so the row stays OPEN for that leg (the untrack/ignore route is not taken while [#1658] writes close rows into the ledger).
