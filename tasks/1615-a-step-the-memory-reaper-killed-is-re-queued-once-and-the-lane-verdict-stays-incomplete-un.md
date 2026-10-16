---
id: "[#1615]"
title: "A step the memory reaper killed is re-queued once, and the lane verdict stays INCOMPLETE until it ran"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1615] [P1][S] **A step the memory reaper killed is re-queued once, and the lane verdict stays INCOMPLETE until it ran** - no row says it (zero hits for 're-queue'); `[#1571]` covers `land` resume only. The reaper rule itself (idle threshold, Windows critical signal, no Available cross-check) has no row (`DIGEST-MEMORY-DIAG-2026-10-03.md`) · Done when: RED first: a test over `lane_digest`/`merge_receipt` asserts a receipt step with `reaped: true` yields verdict INCOMPLETE and exactly one `requeued` event; a second reap yields `SKIPPED-REAPED`; fails on a3d0ae31 · touches: `scripts/merge_receipt.py`, `scripts/lane_digest.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1571]`, `[#1012]`, `[#970]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
