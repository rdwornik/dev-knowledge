---
id: "[#992]"
title: "Measure `/skill-doctor` and `/doctor`'s CLAUDE.md-trim proposal; adopt `omitClaudeMd` for bounded roles"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#992] [P2][S] **Measure `/skill-doctor` and `/doctor`'s CLAUDE.md-trim proposal; adopt `omitClaudeMd` for bounded roles** - D34: every subagent and reviewer loads this repo's large governance CLAUDE.md and unused skills cost context on every task, and the course review (`docs/audits/2026-09-21-technical-aj-all-front.md` rec #1/#5) independently confirms the same shape; the three tool changes to adopt (`/skill-doctor`, `/doctor` trim, `omitClaudeMd`) are named but not measured · Done when: `/skill-doctor` and `/doctor`'s trim proposal are run against this repo and their numbers (unused skills, proposed CLAUDE.md cut) are recorded in an audit; `omitClaudeMd` is set on at least one bounded role (reviewer or reader) and its context-cost delta is measured before/after · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-opus55-harness.md` Part B, `docs/audits/2026-09-21-technical-aj-all-front.md`, `docs/audits/2026-09-23-technical-window-defects-amend.md` · kill-candidates: none -- no open row runs this measurement or sets omitClaudeMd · **CLOSED 2026-11-02** — evidence a062d59d28fe553cd7941717f9da2cc7e45330b0
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-24 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
