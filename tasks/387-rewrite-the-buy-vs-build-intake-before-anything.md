---
id: "[#387]"
title: "Rewrite the buy-vs-build intake BEFORE anything ingests it"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#387] [P2][S] **Rewrite the buy-vs-build intake BEFORE anything ingests it** — intake **#2** (the platform buy-vs-build audit) **argued FOR the template engine that was subsequently rejected**, so consuming it as-written would re-import a dead recommendation as if it were live. This is not inert: [#371] names the buy-vs-build fleet-template ADR as the deciding **vehicle** for consumer editor-config write-through, which makes the stale argument load-bearing on open work. Rewrite it against the ruled position — **adopt the MODEL, not the tool** (Copier → regenerate-and-diff; Terraform → the reconcile loop; Splunk → the data frame, not the platform). Re-checked (night-batch L3): copier#1833 is FALSIFIED — fixed v9.5.0, 17 months pre-authorship; the fit-based rejection STANDS. · Done when: intake #2 is rewritten to the ruled position or superseded by a new intake doc, before any ADR cites it · refs docs/intake/archive/2026-07-06-platform-feature-scan.md, docs/intake/2026-07-21-func-fleet-north-star.md §5 item 5, #371, #382 · kill-candidates: none — a correctness precondition on an intake that open work already cites as its deciding vehicle · serialize-group: architecture
