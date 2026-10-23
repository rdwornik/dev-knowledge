---
id: "[#1719]"
title: "Anchor gate: range-level discharge lets one anchored entry clear a push"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1719] [P2][S] **Anchor gate: range-level discharge lets one anchored entry clear a push** - `scripts/block_unanchored_push.py:156` calls `journal_anchor.range_is_anchored`, which is `any(is_anchored(...))` over the range (`scripts/journal_anchor.py:571-580`), so one anchored entry discharges the whole push; the per-entry `unanchored_on_spine` backstop exists but is only a scan · Done when: a RED-first test shows a push whose range holds an unanchored entry beside an anchored one is surfaced by the backstop (or refused), and the row names which · touches: `scripts/journal_anchor.py`, `scripts/block_unanchored_push.py` · kill-candidates: none -- no open row covers the range-vs-every-entry gap · refs `scripts/journal_anchor.py`, `scripts/block_unanchored_push.py` · source: PLAN-HARNESS-2026-10-23 gap 13, lane ci-one-verdict
