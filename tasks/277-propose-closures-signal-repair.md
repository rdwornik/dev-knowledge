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

- [#277] [P2][M] propose_closures signal repair — the 2026-07-07 /review-closures run proposed 49 items, 0 valid (a 49:0 proposal-to-valid ratio fails the ratified routine-survival metric applied to our own closure organ). Three legs: (a) PERMANENTLY SUPPRESS the two documented STRONG false positives — #5 (`closes [#5]` is example text in an audit.py test fixture) and #77 (`closes [#77]` in 77e5d7d is a voided-closure misattribution, already annotated in-line); (b) REWORK the WEAK heuristic away from bare file-churn — a task naming audit.py / PLAYBOOK.md / HANDOFF_*.md / BACKLOG.md is flagged every arc because those files change by construction (near-zero precision); candidates: require a closes-adjacent id reference, scope WEAK to non-churn files, or drop WEAK keeping STRONG-with-FP-suppression. · (c) absorbs #211: hub↔plugin closure-script parity test · Done when: the two STRONG false positives no longer surface (pinned by a test seeding each), and a single run over the last 30 days of `main` yields a STRONG:WEAK-actioned ratio better than 49:0 with the run's numbers recorded in the closing commit, with tests · refs scripts/propose_closures.py, plugins/tier1-lifecycle/scripts/propose_closures.py, #211, logs/PROPOSALS-2026-07-07.md, ADR-70 · serialize-group: audit-py · **Ratio evidence (2026-08-16, D3):** this host's live SessionStart closure-proposal count is **154** proposed, **0** actioned (154:0) — the ratio the row's own Done-when asks for, against the 2026-07-07 baseline of 49:0. `docs/audits/2026-08-15-technical-night3-decision-queue.md` D3 records the night-3 lane's own clone-measured run at 161:0 (STRONG 2 proposed/0 actioned, WEAK 159 proposed/0 actioned, dismissed as a class); the two counts are cited side-by-side rather than reconciled, per `JOURNAL.md` 2026-08-16(a)'s own precedent for disagreeing per-clone SessionStart numbers. Either reading shows the ratio has degraded 3x+ since this row was written; the row stays OPEN and its priority is a live question.
