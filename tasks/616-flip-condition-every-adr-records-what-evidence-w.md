---
id: "[#616]"
title: "FLIP-CONDITION — every ADR records what evidence would reverse it"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#616] [P2][S] **FLIP-CONDITION — every ADR records what evidence would reverse it** — ADR-108 §A (promoted from intake #22 §A) binds the architect to *"decide, record, and **mark revertable**"* and **never said what the mark IS** — revertability-instead-of-escalation rests on an undefined term at its only enforcement point. Operator direction 2026-08-29: the mark is a **FLIP-CONDITION**, the evidence that would reverse the decision, recorded in the ADR at decision time. Provenance is the operator's MSc thesis principle 5, sensitivity analysis — a decision that cannot name its own flip has not been sensitivity-tested. **Fenced:** a sibling lane is making the template's *"Alternatives considered"* section non-optional — a different requirement (weighed BEFORE vs reverses AFTER), cited not absorbed. · Done when: `templates/ADR-template.md` carries a **Flip-condition** section, ADR-108 §A's *mark revertable* clause resolves to it by name, the posture on a missing flip-condition is ruled (WARN or block), and one worked instance exists on a real ADR · refs docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §A item 2, templates/ADR-template.md, #242 · kill-candidates: none — no open row owns ADR body structure; `[#242]` checks status-flip coherence, metadata not decision content
