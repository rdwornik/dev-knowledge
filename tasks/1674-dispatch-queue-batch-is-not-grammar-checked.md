---
id: "[#1674]"
title: "`dispatch.py queue --batch` launches without the contract grammar checks that `launch`, `codespace-exec` and `repair` run"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1674] [P2][S] **`dispatch.py queue --batch` launches without the contract grammar checks that `launch`, `codespace-exec` and `repair` run** - `queue_cmd` (`scripts/dispatch.py:4094`) calls `launch_lane` directly (`:4122`), so the four checks that sit in `launch_cmd`, `codespace_exec_cmd`, `repair_cmd` and `repair_lane` never run on a queued lane; a malformed contract fires from a queue (`to-browser/SESSION-e2-orchestrator-2026-10-18.md` REVIEW e2-subst-gate-2 successor delta, ORCHESTRATOR-CHECK queue finding) · owner: a dispatch.py lane · Done when: (1) RED first: a queue over a contract that `launch` refuses fires today; (2) `queue` runs the same four checks per lane and refuses with the same message; (3) real-use witness: `queue --batch <B>` over a deliberately malformed contract exits non-zero before any spawn · touches: `scripts/dispatch.py` · kill-candidates: `[#1572]` -- also edits `queue_cmd`; sequence the two · refs `[#1572]`, `[#1632]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-e2-orchestrator-2026-10-18.md` item ORCHESTRATOR-CHECK queue (owed row 1, queue --batch)
