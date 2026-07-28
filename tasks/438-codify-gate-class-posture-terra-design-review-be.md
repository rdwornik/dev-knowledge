---
id: "[#438]"
title: "Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs"
status: open
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
serialize-group: playbook
source: BACKLOG.md
derived: true
---

- [#438] [P3][S] **Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs** — a gate whose job is to REFUSE has an asymmetric failure mode: a **fail-open passes every test and enforces nothing**, so the test suite cannot be the thing that catches it, and a post-build review is already too late to be cheap. Evidence from the [#436] ratchet: reaching clear took a **10-pass** terra loop (`docs/audits/2026-07-27-codex-436-*.md`, 10 artifacts, `gate5`→`gate10`→`recheck`→`clear`→`final`), ~20 findings fixed, **five of them fail-opens that passed the suite** (`5e655cc1` "resolve all five terra HIGH findings"). Review placement, not review quality, is the variable. PLAYBOOK candidate: name the refusal-gate class and require its design pass before implementation. · Done when: PLAYBOOK carries the gate-class rule (which arcs it binds + what the design pass must answer) AND one arc has run under it · refs docs/audits/2026-07-27-codex-436-ratchet-final.md, `5e655cc1`, #436, #437, protocols/PLAYBOOK.md · kill-candidates: none — [#386] codifies the delivery/ship loop, not review-placement by change class · serialize-group: playbook
