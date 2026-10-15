---
id: "[#1603]"
title: "`hook_watchdog.py` kills a real hung hook and logs it, or is removed"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1603] [P3][S] **`hook_watchdog.py` kills a real hung hook and logs it, or is removed** - DEAD: `logs/HOOK-WATCHDOG-KILLS.jsonl` is 0 bytes; `ecosystem/harness.yaml` fate `manual_until 2026-10-14` expired · Done when: RED first: a test runs the watchdog against a fixture hung hook and asserts one JSONL kill row; the row closes with a real kill row in the log or removal; fails on a3d0ae31 · touches: `scripts/hooks/hook_watchdog.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#808]`, `[#1575]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
