---
id: "[#454]"
title: "`closure_ids` negation defect — the parser reads a negated closure mention as a closure"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#454] [P2][S] **`closure_ids` negation defect — the parser reads a negated closure mention as a closure** — REPRODUCED, not inferred: `closure_ids` over a negated mention returns that id, and `find_strong` over `main..HEAD` returns a STRONG proposal to close a row **from the commit body denying that closure**. The `plugins/tier1-lifecycle` twin is identically defective and parity-pinned, so both move in lockstep or the parity test breaks. Third distinct defect in this one detector after the quoting defect ([#437], fixed) and two recorded false positives on [#370] — and the organ being ACCIDENTALLY RIGHT on a row that genuinely should close is what makes it hard to catch in review. · Done when: RED-first tests cover the three recorded reproduction strings, a bounded parser change makes negated mentions non-closing in BOTH copies, and terra reviews the diff pre-merge · refs scripts/propose_closures.py, plugins/tier1-lifecycle/scripts/propose_closures.py, #277, #437, ADR-70 · kill-candidates: none — [#277] repairs the WEAK heuristic's signal ratio and its Done-when passes without ever touching negation parsing · serialize-group: audit-py
