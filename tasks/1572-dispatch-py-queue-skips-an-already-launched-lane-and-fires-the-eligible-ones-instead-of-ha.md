---
id: "[#1572]"
title: "`dispatch.py queue` skips an already-launched lane and fires the eligible ones instead of halting with exit 5"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1572] [P1][S] **`dispatch.py queue` skips an already-launched lane and fires the eligible ones instead of halting with exit 5** - one-shot `queue --batch BU` halts on the first already-launched lane, so eligible lanes never fire and the seat runs the contract's Dispatch line by hand; a kept worktree also trips the OCCUPIED refusal (to-browser/SESSION-integrator-bu-2026-10-15.md:86-87,106-108,148-150) · Done when: RED first: a test with a batch of three lanes, the first already launched, asserts exit 0, lanes 2 and 3 fired, and the first reported `already-launched` (not an error); fails on 97bcd374 · touches: `scripts/dispatch.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1536]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
