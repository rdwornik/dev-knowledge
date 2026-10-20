---
id: "[#1601]"
title: "The three guards that expired 2026-10-08 are each used or removed: `block_immutable_edits.py`, the prompts-guard sweep, `logs_retention.py`"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1601] [P2][S] **The three guards that expired 2026-10-08 are each used or removed: `block_immutable_edits.py`, the prompts-guard sweep, `logs_retention.py`** - DEAD: removed from the hooks list with an expiry of 2026-10-08 that lapsed (`CLAUDE.md` section 9 'off since 2026-09-17'); `[#863]` re-armed the prompts guard on main · Done when: RED first: a test asserts none of the three is both unwired and undated: each is wired in `.claude/settings.json`, or deleted, or carries a future dated ruling; fails on a3d0ae31 · touches: `.claude/settings.json`, the three scripts, tests · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#863]`, `[#1575]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md`. Defect H19: 13 hooks are declared BROKEN by the hook registry and remain enabled (banner: Disabled: NO) (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); used in a real run with a witness by the next batch's close, else removed (operator ruling 2026-10-16: built but unused is a failure)
