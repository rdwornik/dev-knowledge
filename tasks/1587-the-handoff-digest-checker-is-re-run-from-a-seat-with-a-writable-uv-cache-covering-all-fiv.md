---
id: "[#1587]"
title: "The handoff-digest checker is re-run from a seat with a writable uv cache, covering all five bar rows"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1587] [P2][S] **The handoff-digest checker is re-run from a seat with a writable uv cache, covering all five bar rows** - lane nv-929-c is PARTIAL: the checker re-ran 4 of 5 rows; `handoff_state.py` and `boot_frontier.py` BROKEN rows indeterminate; `verify_handoff_probes`, preflight, trial-cut and dry-cut not re-run because Codex could not run `uv run --locked` (`to-browser/SESSION-lane-nv-929-c-handoff-transport.md`; `docs/audits/2026-10-14-technical-verify-handoff-tools.md:30`) · Done when: RED first: a regenerated audit lists all five rows with command and verbatim output and no `Access is denied`; a test asserts the five row headings; fails on 97bcd374 · touches: one new audit, no code · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1456]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8 · **CLOSED 2026-11-03** — evidence 432d0d1a295a4c7a544439c5ad02fac6332b5462
sweep-close: no-fit · witnesses checked=K1 absent=K1 · Re-running a point-in-time audit from a writable seat does not create or repair a continuing TO-BE organ.
