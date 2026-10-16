---
id: "[#1602]"
title: "`deny_and_point.py` is wired and fires on a real denied call, or is removed"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1602] [P3][S] **`deny_and_point.py` is wired and fires on a real denied call, or is removed** - DEAD: PreToolUse `[#727]` deny-and-point unwired 2026-09-18 (script kept) · Done when: RED first: a test asserts the script is referenced by a wired hook or does not exist; fails on a3d0ae31 · touches: `scripts/hooks/deny_and_point.py`, `.claude/settings.json`, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#727]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
