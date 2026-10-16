---
id: "[#1584]"
title: "The `[#863]` lane's owed items are rows: CI-environment owner, audit health, funnel and proof-layer baselines, canonical_docs derived leg"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1584] [P2][M] **The `[#863]` lane's owed items are rows: CI-environment owner, audit health, funnel and proof-layer baselines, canonical_docs derived leg** - `[#863]` ROWS-OWED, none filed: 9 test ids green locally and red on CI; live audit health (2 ids); funnel baseline (269 audits); epic stub P11; canonical_docs derived leg; proof-layer baseline 243 vs 354 (`to-browser/SESSION-lane-bu-863-prompts-guard.md:50-63`) · Done when: RED first: one test per owed item reproduces its red (the 9 ids on a CI-shaped env, the 2 health ids, the baseline counts) and fails on 97bcd374; the row closes when all pass · touches: per the handback list, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#863]`, `[#912]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
