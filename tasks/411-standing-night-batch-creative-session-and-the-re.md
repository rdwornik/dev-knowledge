---
id: "[#411]"
title: "Standing night batch — creative session, and the recurring Q&A cadence"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#411] [P3][S] **Standing night batch — creative session, and the recurring Q&A cadence** — one of three standing night batches the operator dictated (code review · architecture review · creative session), produced at night and consumed by day sessions. The pattern ran twice this arc (night audit, night integration batch) and worked, including an armed Stop that correctly held a bad merge; it needs formalizing as routine. **Folded in from [#348] 2026-07-25:** its half (c) recurring Q&A sessions — same cadence question, same consumption path, so it is scoped here rather than left as a third owner. ROW ONLY this session. · Done when: the creative-session batch AND the recurring Q&A cadence are defined as routines (trigger, scope, consumption path) and ruled in or out · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE) · refs [E9], #381, #348, #412, #419 · kill-candidates: none — [#348] no longer carries a night-batch layer (decomposed to grooming only)
