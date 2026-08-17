---
id: "[#556]"
title: "`[#505]` is closed-but-present — the ADR-65 done-items-leave grooming close"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#556] [P3][S] **`[#505]` is closed-but-present — the ADR-65 done-items-leave grooming close** — `validate_git_backlog` flags it live: `[#505]` was closed by merge `25ff8ec37` (*"docs/consolidate-batch2-lessons — batch-2 lessons become mechanisms; 3 rows filed, 0 closed"*) yet its row is still in `BACKLOG.md`, and its record still carries `status: open`. This is the single `git_backlog_drift` WARN in the current ship-gate. ADR-65's done-items-leave rule is that a closed item LEAVES the backlog and is referenced by id afterwards, so the row is drift rather than a live commitment — it reads as work outstanding when the work shipped. **Filed rather than fixed in place, deliberately:** the close is a `tasks/` status transition plus a `gen_task_tree.py --emit-source` regen, and the retire-not-delete convention keeps the record with a TERMINAL `status:` instead of deleting the file, so doing it as a drive-by would bury a governance act inside an unrelated arc. Surfaced by probes **P4 and P10** of the 2026-08-17 architect handoff gate, which is also the evidence that the detector works and only the action is missing. · Done when: `validate_git_backlog` reports zero closed-but-present items, `tasks/505-*` carries a terminal `status:` rather than `open`, and `[#505]` is referenced by id wherever the shipped work is recorded · refs scripts/validate_git_backlog.py, ADR-65, tasks/505-batch-protocol-encoding-parallel-execution-wow.md, 25ff8ec37, #557 · kill-candidates: none — no open row owns closed-but-present backlog drift; [#534] owns stale line-locators INSIDE rows, which is a different defect class, and [#555]'s campaign closes rows that are still open rather than rows already closed · source: /handoff-verify P4 + P10, 2026-08-17 architect gate
