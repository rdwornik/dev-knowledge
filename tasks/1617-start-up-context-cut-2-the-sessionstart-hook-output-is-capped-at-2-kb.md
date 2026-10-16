---
id: "[#1617]"
title: "Start-up context cut 2: the SessionStart hook output is capped at 2 KB"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1617] [P1][S] **Start-up context cut 2: the SessionStart hook output is capped at 2 KB** - the SessionStart hook prints about 9 KB per session (hook-rate, hook-BROKEN and ADVISORY lines for every declared-broken hook, a cost line, a seat line); that text enters every turn's context · Done when: RED first: a test runs `scripts/hooks/session_start.py` on a fixture state and asserts stdout <= 2,048 B, the declared-broken list collapsed to one count line with a pointer to the log; witness: the baseline above re-measured <= 53,500; fails on a3d0ae31 · touches: `scripts/hooks/session_start.py`, its readers, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1006]`, `[#1616]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
