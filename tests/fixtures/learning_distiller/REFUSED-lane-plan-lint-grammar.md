<!-- fixture provenance: copied verbatim (2026-09-25) from
     H:\My Drive\CLAUDE PROMPT DIR\to-browser\REFUSED-lane-plan-lint-grammar.md
     for tests/test_learning_distiller.py (LANE-5B2-13-learning-distiller). Content below is
     unmodified except for this header. -->

from: the INTEGRATOR
repair 1 of 2
date: 2026-09-25
batch: WAVE5B-N1
lane: lane-plan-lint-grammar (LANE-5B-6-plan-lint-grammar.md), branch worktree-lane-plan-lint-grammar @ a5bb0e4c

# REFUSED — lane-plan-lint-grammar, repair 1 of 2

## What failed

A **hard-fail organ introduced by this lane's merge**:

```
[!!] silent_rule_ratchet: silent-rule pool GREW: live 454 > baseline 452 (+2) under detector
     silent-rule-v5 across 78 file(s) -- drain the additions or record an operator ruling;
     the baseline does not rise on a commit
```

Attribution by measurement (`silent_rule_detector.measure` on each tree of the integration
stack): the three merges before yours read 452; your merge reads 454. The +2 is yours alone.
CI agrees: run 36079008845 names `tests/test_silent_rule_ratchet.py::test_committed_baseline_matches_live_measurement`
and `::test_check_registered_and_green_on_live_repo` red (`live 454 exceeds committed baseline 452`).
Your session file reports the ratchet at 52 passed — the detector reads committed blobs
(`git ls-files -s` + `git cat-file`), so a run before the second commit, or on an uncommitted
tree, reads the old count.

Everything else was green: `tests/test_plan_lint.py` on the merged tree 55 passed; the other
ship-gate differences are WARN-tier findings on your own Codex record.

## Cure (the lane's to make; nothing weakened)

- Find the two new silent-rule tokens (`must` / `shall` / `never`-class words in scope of
  `scripts/silent_rule_detector.py`) your diff adds in `scripts/plan_lint.py`,
  `templates/lane-contract-template.md` or `tests/test_plan_lint.py`, and reword them (the
  registry lane did the same: "must not call it" -> "does not call it"). Do not touch the
  baseline file.
- Commit, then run `uv run --locked pytest tests/test_silent_rule_ratchet.py -q` on the
  COMMITTED tree and paste the live count (<= 452).

## Sync rule

Sync from origin only: `git fetch origin` then `git merge origin/main` (main is now 4fab7aea).
Never `git merge main`. Purity before handback: `git log origin/main..HEAD` = your commits and
merges of origin/main only. Hand back with the machine line
`HANDBACK worktree-lane-plan-lint-grammar @ <sha> code` in `to-browser/SESSION-lane-plan-lint-grammar.md`.
