---
id: "[#830]"
title: "Witness"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#830] [P2][M] Witness — the closure digest's instrument defect is that `propose_row_closures.py` can detect branch divergence but cannot ask which open rows the proving merges satisfied · Done when: task filing accepts a `witness:` frontmatter key for pytest nodes, hook ids, or `path:anchor`; closure backfill can resolve every witness; `propose_row_closures.py` has a Q2 mode that reports open rows whose witnesses pass; and the 25 Table 1 witnesses are retained as the backfill seed · refs `scripts/gen_task_tree.py`, `scripts/validate_backlog.py`, `scripts/backlog_source.py`, `scripts/propose_row_closures.py`, digest instrument defect 2026-09-16 · kill-candidates: none — this is filed as the required witness row; implementation is a later lane, not this no-code census lane
