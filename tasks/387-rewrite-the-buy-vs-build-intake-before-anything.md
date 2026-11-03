---
id: "[#387]"
title: "Rewrite the buy-vs-build intake BEFORE anything ingests it"
status: closed
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#387] [P2][S] **Rewrite the buy-vs-build intake BEFORE anything ingests it** — intake **#2** (the platform buy-vs-build audit) **argued FOR the template engine that was subsequently rejected**, so consuming it as-written would re-import a dead recommendation as if it were live. This is not inert: [#371] names the buy-vs-build fleet-template ADR as the deciding **vehicle** for consumer editor-config write-through, which makes the stale argument load-bearing on open work. Rewrite it against the ruled position — **adopt the MODEL, not the tool** (Copier → regenerate-and-diff; Terraform → the reconcile loop; Splunk → the data frame, not the platform). Re-checked (night-batch L3): copier#1833 is FALSIFIED — fixed v9.5.0, 17 months pre-authorship; the fit-based rejection STANDS · Done when: `docs/intake/archive/2026-07-06-platform-feature-scan.md` either carries the ruled position (with an amendment marker) or a superseding intake doc exists and the old one's `status:` names it, and no `docs/decisions/ADR-*.md` cites the un-rewritten doc · refs the archived platform-feature-scan intake, the fleet-north-star intake §5 item 5, #371, #382 · kill-candidates: none — a correctness precondition on an intake that open work already cites as its deciding vehicle · serialize-group: architecture · **CLOSED 2026-11-03** — evidence 41df0087b3cff012aaf2a7075d038520fb4cb1f6
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-07-27 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
