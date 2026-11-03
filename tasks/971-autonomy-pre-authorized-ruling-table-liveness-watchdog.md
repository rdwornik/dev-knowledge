---
id: "[#971]"
title: "Autonomy: pre-authorized ruling table, liveness watchdog, and a deny-and-point guard for root writes"
status: closed
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#971] [P1][M] **Autonomy: pre-authorized ruling table, liveness watchdog, and a deny-and-point guard for root writes** - D8: this window recorded 3 human waits of 8-10 hours at night (a ruling, a permission prompt, dead lanes) because no default existed, no liveness check ran, and a permission prompt simply hung until morning · Done when: every night batch order carries a pre-authorized ruling table (a lane decides by its contract's Value line and records the decision, per this window's own BATCH-WAVE5A common rule 1); a liveness watchdog flags a lane idle beyond a threshold without a HANDBACK line; a deny-and-point guard exists for root-path writes so a permission prompt cannot silently hang a night session · implements: ADR-120 · refs `to-cc/BATCH-WAVE5A-2026-09-23.md` (rule 1, the pattern this generalizes), `docs/audits/2026-09-23-technical-window-defects.md`, `docs/audits/2026-10-05-codex-b2-integrator-liveness.md` (B2-W1 W1-5: the handback wake and its watch, the integrator's event wake; not the idle watchdog) · kill-candidates: none -- no open row builds a liveness watchdog or a deny-and-point guard for this failure mode · **CLOSED 2026-11-03** — evidence 432d0d1a295a4c7a544439c5ad02fac6332b5462
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-24 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
