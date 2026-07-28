---
id: "[#277]"
title: "propose_closures signal repair"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#277] [P2][M] propose_closures signal repair — the 2026-07-07 /review-closures run proposed 49 items, 0 valid (a 49:0 proposal-to-valid ratio fails the ratified routine-survival metric applied to our own closure organ). Three legs: (a) PERMANENTLY SUPPRESS the two documented STRONG false positives — #5 (`closes [#5]` is example text in an audit.py test fixture) and #77 (`closes [#77]` in 77e5d7d is a voided-closure misattribution, already annotated in-line); (b) REWORK the WEAK heuristic away from bare file-churn — a task naming audit.py / PLAYBOOK.md / HANDOFF_*.md / BACKLOG.md is flagged every arc because those files change by construction (near-zero precision); candidates: require a closes-adjacent id reference, scope WEAK to non-churn files, or drop WEAK keeping STRONG-with-FP-suppression. · (c) absorbs #211: hub↔plugin closure-script parity test · Done when: the two STRONG FPs no longer surface AND the WEAK heuristic is reworked or retired so a representative run beats this run's 49:0 ratio, with tests · refs scripts/propose_closures.py, plugins/tier1-lifecycle/scripts/propose_closures.py, #211, logs/PROPOSALS-2026-07-07.md, ADR-70 · serialize-group: audit-py
