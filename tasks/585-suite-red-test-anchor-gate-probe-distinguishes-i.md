---
id: "[#585]"
title: "Suite RED — `test_anchor_gate_probe_distinguishes_installed_from_absent` does not discriminate: repair it, retire it, or fix the organ"
status: open
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: gates
generates: BACKLOG.md
---

- [#585] [P2][S] **Suite RED — `test_anchor_gate_probe_distinguishes_installed_from_absent` does not discriminate: repair it, retire it, or fix the organ** — The probe REFUSES an anchored push in the synthetic consumer too, so it does not discriminate — a constant refusal enforces nothing. Pre-existing since 2026-08-20 with nobody obliged to decide; this row assigns that owner. · Full body as born: `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: `test_anchor_gate_probe_distinguishes_installed_from_absent` is green, or it is retired with the reason recorded and `block_unanchored_push`'s demonstrated enforcement scope restated wherever it is claimed, and `[#569]` is re-scoped to the PLAYBOOK census with this row named as item (A)'s carrier · refs tests/test_enforcement_coverage.py, scripts/block_unanchored_push.py, protocols/STANDING_RULINGS.md sections U and W, ADR-85, #583, #569 · source: packet row C18 (ARC-E), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — `[#569]` was this row's kill-candidate, CONSUMED 2026-08-26 (closed under W5); a spent id may not sit in a kill-candidates VALUE, so it is in refs. That closure did NOT discharge its PLAYBOOK census, which no open row owns · serialize-group: gates
