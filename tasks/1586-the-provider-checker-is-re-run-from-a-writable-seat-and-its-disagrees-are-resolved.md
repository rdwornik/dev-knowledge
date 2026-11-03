---
id: "[#1586]"
title: "The provider checker is re-run from a writable seat and its DISAGREEs are resolved"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1586] [P2][S] **The provider checker is re-run from a writable seat and its DISAGREEs are resolved** - lane nv-929-d's provider digest is DEGRADED: 'The checker's sandbox blocks writes to user dirs, so most of its DISAGREEs are its own Access is denied' (5 of 7); OPERATOR-ACTION: re-run from a seat with a writable uv cache and network (`to-browser/DIGEST-VERIFY-providers-2026-10-14.md`; `to-browser/SESSION-lane-nv-929-d-telemetry-providers.md`). Not re-run in the night close-out by order · Done when: RED first: a regenerated `docs/audits/<date>-verification-providers-rerun.md` exists whose checker block has 0 `Access is denied` lines and each of the 7 DISAGREEs carries a verdict; a test asserts that; fails on 97bcd374 · touches: one new audit, no code · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1327]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
