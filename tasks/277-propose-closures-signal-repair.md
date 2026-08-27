---
id: "[#277]"
title: "propose_closures signal repair"
status: deferred
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#277] [P2][M] propose_closures signal repair — the 2026-07-07 /review-closures run proposed 49 items, 0 valid — a 49:0 ratio failing the routine-survival metric applied to our own closure organ. Three legs: (a) PERMANENTLY SUPPRESS the two documented STRONG false positives **#5** and **#77**; (b) REWORK the WEAK heuristic away from bare file-churn — a task naming audit.py / PLAYBOOK.md / BACKLOG.md is flagged every arc because those files change by construction; candidates: require a closes-adjacent id reference, scope WEAK to non-churn files, or drop WEAK keeping STRONG-with-FP-suppression. · (c) absorbs #211: hub↔plugin closure-script parity test · Done when: the two STRONG false positives no longer surface (pinned by a test seeding each), and a single run over the last 30 days of `main` yields a STRONG:WEAK-actioned ratio better than 49:0 with the run's numbers recorded in the closing commit, with tests · refs scripts/propose_closures.py, plugins/tier1-lifecycle/scripts/propose_closures.py, #211, ADR-70 · serialize-group: audit-py · **RE-MEASURED 2026-08-16 — degraded 3x+; row stays OPEN** · source: docs/audits/2026-08-15-technical-night3-decision-queue.md D3 (161:0 night-3 clone, 154:0 this host, cited side by side) + docs/audits/2026-06-21-audit-ops-findings.md · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
