---
id: "[#1614]"
title: "The resource organ's 'free' memory figure is named 'available' and read from the OS available counter"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1614] [P3][S] **The resource organ's 'free' memory figure is named 'available' and read from the OS available counter** - memory-diag harness row #12: `resource_lifecycle` and the admission gate say 'free' (`tasks/970`, `tasks/790`) while the quantity that matters is Available · Done when: RED first: a test asserts `memory_admission_gate.py` output and `resource_lifecycle` expose `available_mb` and no key named `free_mb`; fails on a3d0ae31 · touches: `scripts/memory_admission_gate.py`, `scripts/resource_lifecycle.py`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#970]`, `[#790]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
