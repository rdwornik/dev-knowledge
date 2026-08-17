---
id: "[#541]"
title: "Scale-out substrate decision — unowned after two reports and a priced option set"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#541] [P3][S] **Scale-out substrate decision — unowned after two reports and a priced option set** — the v2 substrate report restates the requirements the operator added (a VS Code control plane, an hourly-to-monthly crossover rule, time-to-deploy), prices the option set, and names six defects in its own v1 — including that Codespaces was omitted entirely and the control plane was never priced, which inverts v1's "ops burden: zero" scoring. It carries a measured baseline and the compute-is-1% finding. Verified live: **no row in `tasks/` owns the decision** — the only substrate row is `[#521]`, which is the `sys.path` substrate and unrelated. A priced recommendation with no owner is how a spend decision quietly expires. · Done when: a ruling records the chosen scale-out substrate with its crossover rule and time-to-deploy, or records the decision deferred with a dated peg, citing the v2 report's option set · refs docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md, #453, #484 · kill-candidates: none — `[#453]` owns the cloud-container preflight gaps, not which substrate to rent · source: docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md
