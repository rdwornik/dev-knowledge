---
id: "[#1749]"
title: "the backlog per-row reconciliation organ (GO-E3.0 R10), after L2"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1749] [P2][M] **the backlog per-row reconciliation organ (GO-E3.0 R10), after L2** - a per-row reconciliation organ over the open backlog rows, with `report` and operator-ruled `apply` · Done when: RED first: `apply` refuses without an operator ruling and applies only the ruled classes; real-use witness: one `report` run over the open rows lands as an audit with its cost record. · touches: `scripts/backlog_reconcile.py`, `tests/test_backlog_reconcile.py`, `tests/fixtures/backlog_reconcile/classification.json`, `tests/fixtures/backlog_reconcile/registry.yaml`, `tests/fixtures/backlog_reconcile/tasks/1749-shipped-row.md`, `tests/fixtures/backlog_reconcile/tasks/1750-live-row.md`, `tests/fixtures/backlog_reconcile/tasks/1751-stale-refs-row.md`, `docs/audits/2026-11-01-technical-backlog-reconcile.md` · kill-candidates: none -- no open row owns per-row backlog reconciliation · refs `scripts/gen_task_tree.py` · source: to-cc/GO-E3.0.md G2 · decided-by: the operator, 2026-10-31, GO-E3.0 id grant
