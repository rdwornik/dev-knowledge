---
id: "[#301]"
title: "Session-plan artifact class"
status: deferred
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
source: BACKLOG.md
derived: true
---

- [#301] [P2][M] Session-plan artifact class — architect-mode bundles gain a bundle-resident PLAN.md, completing the mode→artifact symmetry (functional→intake · architect→PLAN+retrospective · developer→EPIC_BOOT+RETURN; operator-directed, plan-v3 2026-07-09): (i) `/handoff --mode architect` seeds a PLAN.md skeleton (objective · epics/stories bound to live ids · traceability · decisions · risks); (ii) in-file changelog versioning v1→vN + supersedes chain; (iii) session-close fills a RETROSPECTIVE (done/not-done/incidents/carry-forward) — advisory Stop-gate beat first, hardening later (ADR-85 path); (iv) cross-generation plan-continuity carrier (night proposal): a `prior_plan:` bundle field + gen_handoff discover-step + a RETROSPECTIVE plan-vs-execution subsection carrying the PREVIOUS plan forward; (v) bundle-resident only, no new top-level docs class (#300). · Done when: an architect bundle renders a PLAN.md skeleton, session-close fills the RETROSPECTIVE, and the v1→vN supersedes chain is exercised, each with a test · refs scripts/gen_handoff.py, templates/handoff/, #298, #300, ADR-81, ADR-98 · serialize-group: handoff · DEFER — peg: #298 generator-polish arc
