---
id: "[#410]"
title: "Standing night batch — ARCHITECTURE review (formalize as routine)"
status: closed
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#410] [P3][S] **Standing night batch — ARCHITECTURE review (formalize as routine)** — the structure-facing member of the same dictated trio, produced at night and consumed by day sessions. Its subject is SHAPE, not diff: ADR coherence, boundary/ownership drift, and whether the living docs still describe the tree. Shares [#409]'s twice-run precedent but reads a different surface, which is why both rows exist rather than one. ROW ONLY this session. · Done when: the architecture-review night batch carries an ADR-105 `· routine:` block with all six fields populated (`trigger`/`scope`/`consumer`/`consumption_path`/`verified_by`/`review_date`) that `routine_consumers` passes — or it is ruled out in `protocols/STANDING_RULINGS.md` by a `###` section whose heading names `[#410]`, or by a line where `[#410]` carries a disposition token · activation gate: ADR-105 (consumer + consumption_path required to ACTIVATE) · refs [E9], #381, #348, #412, JOURNAL night-audit + night-integration entries · kill-candidates: none — [#348] no longer carries a night-batch layer (decomposed 2026-07-25 to grooming only); the configured fan-out that would host this now lives in [#412]
