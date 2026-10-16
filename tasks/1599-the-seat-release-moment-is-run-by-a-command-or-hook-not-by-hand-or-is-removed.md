---
id: "[#1599]"
title: "The `seat-release` moment is run by a command or hook, not by hand, or is removed"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1599] [P2][S] **The `seat-release` moment is run by a command or hook, not by hand, or is removed** - DECLARED-ONLY: run by hand; its only callers are prose in `.claude/commands/handoff.md` (the retired `/handoff-verify` was the other) · Done when: RED first: a test asserts some command or hook invokes `seat_release.*` organs and fails on a3d0ae31; closes with a receipt from a real release or the moment removed · touches: `ecosystem/harness.yaml`, `.claude/commands/handoff.md`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1456]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
