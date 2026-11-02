---
id: "[#1604]"
title: "The CI job `terra` runs with a credential or is removed"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1604] [P2][S] **The CI job `terra` runs with a credential or is removed** - DEAD: 'terra review NOT RUN -- no provider credential' on every run (`docs/audits/2026-10-15-technical-verified-harness-map.md:86`) · Done when: RED first: a test over `.github/workflows/conductor.yml` asserts the `terra` job either has its secret reference and a real-run run id in `logs/`, or is absent; fails on a3d0ae31 · touches: `.github/workflows/conductor.yml`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1581]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
