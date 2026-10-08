---
id: "[#1429]"
title: "The handoff preflight and the batch-close trial cut cannot see P13 because they judge the previous bundle"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1429] [P1][M] **The handoff preflight and the batch-close trial cut cannot see P13 because they judge the previous bundle** - `verify_handoff_probes._undisposed_decisions` returns nothing for a sealed bundle (`verify_handoff_probes.py:1018`), and the preflight's ship_gate row runs the organ set against the active bundle, which before a cut is the previous, committed one. So the twelve undisposed decisions of 2026-10-07 surfaced only after the cut existed, at the last step (readiness digest F1) · Done when: the preflight and the batch-close trial cut evaluate `decision_coverage.onboarding_findings` against the live decision population as their own row, failing on any in-era undisposed decision before a cut exists; a RED-first test with one undisposed in-era decision and a sealed previous bundle · owner: the handoff generator · touches: `scripts/gen_handoff.py`, tests · kill-candidates: `[#1437]` -- batch close disposes each batch's decisions; this row is the cut-time backstop · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
