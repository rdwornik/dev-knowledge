---
id: "[#1738]"
title: "dispatch.py history read-modify-write"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1738] [P2][S] **dispatch.py history read-modify-write** - `dispatch.py` `_write_launch_records` reads the launch history, appends and writes it back under no lock, and writes the worktree copy before the primary receipt -- on a `repair` launch (`scripts/dispatch.py:1430`) the earlier `launches` are read from the slug receipt, one entry is appended (`:1431-1435`) and the whole receipt is rewritten at `:1438` with no lock between the read and the write, so two concurrent repairs of one slug lose a history entry; and the copy under the lane worktree (`:1437`) is written before the primary receipt, so a crash between the two leaves the gate's worktree lookup ahead of the primary record · owner: integrator-e2-1 (`scripts/dispatch.py`) · Done when: (1) RED first: a test running two `repair` writes for one slug concurrently ends with both launches in `launches`; (2) the read-modify-write holds one per-slug `FileLock`; (3) the primary receipt is written first and the worktree copy second, so a crash leaves primary >= copy; (4) `uv run --locked pytest -n0 tests/test_dispatch.py` passes · touches: `scripts/dispatch.py`, `tests/test_dispatch.py` · refs `[#1727]` · decided-by: the orchestrator, 2026-10-25 (three H1-X rows owed from the SH1-X review), granted by the integrator id block · source: `to-browser/SESSION-dispatcher-e2-1-2026-10-23.md:1582` (ii) · filed by the integrator from the operator grant 1737-1743 (RATIFICATION-2026-10-26.md ruling B + D-ID; S-ID: no id beyond it)
