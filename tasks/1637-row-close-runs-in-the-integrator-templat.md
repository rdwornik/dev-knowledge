---
id: "[#1637]"
title: "row_close runs in the integrator template"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "intake-118"
generates: BACKLOG.md
---

- [#1637] [P2][S] **row_close runs in the integrator template** - row_close runs in the integrator template, once per merge, all-or-none. `scripts/row_close.py` is wired into no template, command or moment although `harness.yaml:170` calls it the per-handback path; BU rows were closed by hand after the claim was released. owner: D1 lane. target batch: D1 · Done when: RED first: the integrator template's Per-handback path names `row_close.py` before teardown and a test pins the order; real-use witness: a merge receipt shows the rows closed by it · touches: see the body · kill-candidates: none -- no row wires row_close · implements: intake-118 · refs `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18-ANNEX.md` L10, `docs/intake/2026-10-18-tech-d0-rows-without-a-ratified-ruling.md` · decided-by: R137 (Q5: the plan r4 OK of 2026-10-18) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
