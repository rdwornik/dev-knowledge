---
id: "[#443]"
title: "Planning artifacts outside the three enforced classes carry no rent rule"
status: open
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
serialize-group: playbook
generates: BACKLOG.md
---

- [#443] [P3][S] **Planning artifacts outside the three enforced classes carry no rent rule** — "meta serves object" (North Star §5 lesson 7; LESSONS 2026-07-28, recorded as context and deliberately NOT a fourth rule) is enforced for exactly three classes: **sessions** (`DEFINITION_OF_DONE.md` journal leg — a wrap must cite ≥1 commit SHA from the session), **routines** (ADR-105 — consumer declaration judged at ACTIVATION, else "retired, not activated"), **intake docs** (`docs/intake/README.md` §7 — named consumer + survival metric). **Handoff bundles, session plans and audit docs sit outside all three**, so for them the principle is aspiration, not enforcement. Either state the rent/binding rule covering them or record — with reasons — that they are deliberately un-ruled; there is no open-ended third option. · Done when: each uncovered class carries either a stated rent/binding rule at its canonical home or a recorded deliberately-not-a-rule with its reason · refs LESSONS 2026-07-28, intake #16 §5 lesson 7, intake #20 §6 Q1, ADR-105 · kill-candidates: none — [#145] is codification COMPLETENESS, not artifact-class rent · serialize-group: playbook
