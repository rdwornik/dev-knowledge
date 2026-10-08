---
id: "[#1432]"
title: "The post-fill order of the handoff cut lives in prose: --filled before assemble_paste refuses"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1432] [P2][S] **The post-fill order of the handoff cut lives in prose: --filled before assemble_paste refuses** - Running the finalising `--filled` re-render before re-running `assemble_paste` refuses with 8 hard-fails (`supplement_folded`, `residual_completeness`). The only order that works -- fill, assemble, verify, `--filled` -- is written in the runbook and the plan, and nothing runs it (readiness digest F9) · Done when: one command runs fill-check, assemble, verify and the `--filled` re-render in that order (or `--filled` re-assembles first), and the runbook names only that command; a test of the order · owner: the handoff generator · touches: `scripts/gen_handoff.py`, `scripts/assemble_paste.py`, `docs/handoffs/README.md`, tests · kill-candidates: `[#1436]` -- the readiness command runs the same sequence · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
