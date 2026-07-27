---
id: "[#436]"
title: "`silent_rule_ratchet` — gate the GROWTH of silently-unenforced rules"
status: open
priority: P1
size: M
theme: "[E8] ARC-5 execution"
story: "[S21] Discharge the ARC-5 carried items that no wave has yet absorbed"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#436] [P1][M] **`silent_rule_ratchet` — gate the GROWTH of silently-unenforced rules** (operator ruling F1, discharging R12; **D4 semantics**, operator-adopted 2026-07-27): an `audit.py` registry check + ship-gate leg comparing a live count against a **committed detector-measured baseline** — **428 @ `silent-rule-v2`**, NOT the census's 176, which is not reproducible by code (regex + file filter unrecorded). **Ratchet-down only** — lowered as rules drain, never raised; a raise is an operator ruling, not a commit. Honest limit: it counts normative-keyword OCCURRENCES, a proxy for the pool, not a rule census — a green ratchet is NOT a drained pool. · Done when: registered in `ALL_CHECKS`, the leg FAILs above baseline and passes at or below it, baseline committed, tests pin both directions, terra CODE review recorded · refs docs/audits/2026-07-27-census-silent-rule-ratchet-arm-measurement.md + its D4 amendment, scripts/silent_rule_detector.py, ecosystem/silent-rule-baseline.yaml, [E8] clause (b) + its R12 row, #357, #362 · kill-candidates: none — [#357] completes the denominator and [#358]–[#362] are drain items; none gates the growth of the pool · serialize-group: audit-py
