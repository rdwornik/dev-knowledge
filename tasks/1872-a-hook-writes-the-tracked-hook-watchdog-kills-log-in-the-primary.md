---
id: "[#1872]"
title: "A hook writes the tracked logs/HOOK-WATCHDOG-KILLS.jsonl in the primary"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1872] [P2][S] **A hook writes the tracked logs/HOOK-WATCHDOG-KILLS.jsonl in the primary** - audit A2 of 2026-11-04: the primary checkout is permanently dirty with ` M logs/HOOK-WATCHDOG-KILLS.jsonl`; the file is tracked (`git ls-files`) and `scripts/hooks/hook_watchdog.py` appends to it (`RECORD_RELPATH` at `scripts/hooks/hook_watchdog.py:117`) on every session, so the operator's checkout never shows clean. Fix: either untrack it and gitignore it (machine record), or move the record to the state home of ADR-140 I2; decide in the row, test that a session leaves the primary's tracked tree clean. Related `[#1603]` (the watchdog's fate), which this row does not close. · touches: scripts/hooks/hook_watchdog.py, .gitignore, logs/HOOK-WATCHDOG-KILLS.jsonl · kill-candidates: none - [#1603] owns the watchdog's existence, not the tracked record · refs ADR-140 (out-of-scope item A2), `[#1603]`, `scripts/hooks/hook_watchdog.py` · Done when: after a session the primary's `git status --porcelain` shows no hook-written tracked file · decided-by: night order N2(b) · source: P0 audit A2
