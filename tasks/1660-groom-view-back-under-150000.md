---
id: "[#1660]"
title: "GROOM: the BACKLOG view returns under 150,000 B by closing done rows (R148)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1660] [P2][M] **GROOM: the BACKLOG view returns under 150,000 B by closing done rows (R148)** - R148 raised the view budget to 160,000 B until 2026-11-15; this row returns it to 150,000 B by closing done rows through the ADR-111 funnel (a row closes by its own Done-when, never by deletion) · owner: E2 lane. target batch: E2.1 (before 2026-11-15) · Done when: (1) done rows are closed through the funnel; (2) `scripts/view_budget.yaml` is set back to `value: 150000`; real-use witness: `uv run --locked python scripts/gen_task_tree.py --check` reports the view under 150,000 B on the merged tree · touches: `tasks/`, `scripts/view_budget.yaml` · kill-candidates: none -- it is the groom itself · refs `scripts/view_budget.yaml`, `to-browser/LEDGER-dev-knowledge.md` v238 R148 · decided-by: R148 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
