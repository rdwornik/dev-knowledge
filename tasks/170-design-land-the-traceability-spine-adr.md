---
id: "[#170]"
title: "Design + land the traceability-spine ADR"
status: open
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
generates: BACKLOG.md
---

- [#170] [P3][M] Design + land the traceability-spine ADR (issue-ID↔commit anchor) that #168 depends on — the airtight, always-warranted link that promotes ADR-85's BACKLOG leg from advisory to a hard gate. The spine is the un-gameable AND always-warranted anchor the structural-marker check lacks. · absorbs #168 (harden the ADR-85 BACKLOG leg to a hard gate once this spine lands) + #243 (the #168-hard vs Fable-WARN severity conflict, resolved at the mesh consult #2) · **RE-PHRASED 2026-08-12** (operator adjudication; register `protocols/STANDING_RULINGS.md` M-7 / `N2-R1-01`): the Done-when read "#168 has a ratified anchor to depends-on", but **there is no `tasks/168-*.md` in any status** — `#168` was absorbed into this row, so the clause depended on a row that does not exist and could not be satisfied as written. The absorbed half is stated here in-row instead of pointing at a phantom: it is the promotion of **ADR-85's BACKLOG leg from advisory to a hard gate**, which this row's own spine makes possible and which has no other home. Killing this row would therefore delete the ADR-85 BACKLOG-leg promotion argument entirely, which is why the census called it keep-and-re-phrase rather than a kill candidate. · Done when: an ADR defines the issue-ID↔commit linkage, **and** the absorbed `#168` half — promoting the ADR-85 BACKLOG leg from advisory to a hard gate — is stated in this row's scope and ratified with the ADR · refs docs/decisions/ADR-85-session-lifecycle-enforcement.md (R1), #168, #8
