---
intake-id: 108
status: SEED
origin: "BATCH-GREEN-MAIN-PILOT-2026-10-14 Part C, the hand-landed /map refresh record (map_sha 88f1bc52, branch worktree-system-map-2026-10-14, c2953534)"
consumed-by:
---

# SEED -- the system-map refresh is not a closed loop

The `/map` refresh (`scripts/system_map.py`, `.claude/commands/map.md`) wrote `ecosystem/system-map-record.json` for map_sha 88f1bc52 on branch `worktree-system-map-2026-10-14` (c2953534, 2026-10-14) in worktree `.claude/worktrees/system-map-2026-10-14` and stopped. Nothing merged, landed or tore it down, so the record sat unmerged while main moved. BATCH-GREEN-MAIN-PILOT-2026-10-14 Part C landed it by hand and recorded this GAP.

Carrier row: [#1533]. A row decides nothing: it asks for the refresh to land through `merge_path.py land` and tear down after itself, or to write nothing outside gitignored scratch (ADR-111).
