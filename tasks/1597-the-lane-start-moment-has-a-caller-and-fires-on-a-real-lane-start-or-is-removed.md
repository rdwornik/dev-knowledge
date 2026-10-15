---
id: "[#1597]"
title: "The `lane-start` moment has a caller and fires on a real lane start, or is removed"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1597] [P2][S] **The `lane-start` moment has a caller and fires on a real lane start, or is removed** - DECLARED-ONLY: no caller anywhere (grep over scripts, hooks, commands and workflows finds none) · Done when: RED first: a test over `harness.yaml` asserts every declared moment has at least one caller reachable from a command, hook or workflow, and fails naming `lane-start`; fails on a3d0ae31; the row closes with a receipt from a real lane start or the moment removed · touches: `ecosystem/harness.yaml`, `.claude/commands/lane-boot.md`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1007]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
