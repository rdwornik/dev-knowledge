---
id: "[#409]"
title: "Standing night batch — code review (formalize as routine)"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
source: BACKLOG.md
derived: true
---

- [#409] [P3][S] **Standing night batch — code review (formalize as routine)** — one of three standing night batches the operator dictated (code review · architecture review · creative session), produced at night and consumed by day sessions. The pattern ran twice this arc (night audit, night integration batch) and worked, including an armed Stop that correctly held a bad merge; it needs formalizing as routine. ROW ONLY this session. · Done when: the code-review night batch is defined as a routine (trigger, scope, consumption path) and ruled in or out · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE) · refs [E9], #381, #348, #412, JOURNAL night-audit + night-integration entries · kill-candidates: none — [#348] no longer carries a night-batch layer (decomposed 2026-07-25 to grooming only); the configured fan-out that would host this now lives in [#412]
