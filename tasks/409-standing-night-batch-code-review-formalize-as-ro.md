---
id: "[#409]"
title: "Standing night batch — CODE review (formalize as routine)"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
source: BACKLOG.md
derived: true
---

- [#409] [P3][S] **Standing night batch — CODE review (formalize as routine)** — the diff-facing member of the three standing batches the operator dictated (code · architecture · creative), produced at night and consumed by day sessions. Its subject is what CHANGED: `scripts/`, tests, gate implementations — unattended defect-hunting under the terra/codex lens. Precedent it works: the pattern ran twice this arc (night audit, night integration batch), including an armed Stop that correctly held a bad merge; formalizing is what remains. ROW ONLY this session. · Done when: the code-review night batch is defined as a routine (trigger, scope, consumption path) and ruled in or out · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE) · refs [E9], #381, #348, #412, JOURNAL night-audit + night-integration entries · kill-candidates: none — [#348] no longer carries a night-batch layer (decomposed 2026-07-25 to grooming only); the configured fan-out that would host this now lives in [#412]
