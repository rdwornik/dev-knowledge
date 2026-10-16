---
id: "[#1605]"
title: "Each of the 70 `fates:` scripts is wired, dated or removed; the 11 with expired dates first"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1605] [P2][M] **Each of the 70 `fates:` scripts is wired, dated or removed; the 11 with expired dates first** - DECLARED-ONLY: the 70 scripts under `fates:` in `harness.yaml` are manual only, 11 with expired `manual_until` dates (process matrix, `docs/audits/2026-10-16-technical-process-matrix.md`) · Done when: RED first: a test reads `fates:` and asserts no entry has an expired date and every entry names a caller or a future-dated ruling; fails on a3d0ae31 · touches: `ecosystem/harness.yaml`, per script, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1590]`, `[#1575]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
