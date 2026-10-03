---
id: "[#1349]"
title: "release-lint: the floor spec pin does not match its sidecar, and five tests read it"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1349] [P2][S] **release-lint: the floor spec pin does not match its sidecar, and five tests read it** - `deploy/release_lint.py` check `C5-floor-pin` fails with "spec pin 4d268f329a7e.. != sidecar e8c62d24a019..", and five tests in `tests/test_release_lint.py` (`test_live_hub_state_is_green`, `test_live_v120_state_is_green`, `test_unmutated_copy_is_green`, `test_missing_tag_is_warn_not_fail`, `test_cli_green_exit_0`) fail on it on both legs of every recent run. Registered pre-freeze with no owner · Done when: the floor spec pin and its sidecar agree by the sanctioned generator, not a hand edit, and the five tests are green on both CI legs · touches: `deploy/release_lint.py`, `tests/test_release_lint.py`, `.claude/CLAUDE-FLOOR.md` · kill-candidates: none -- [#656] is the floor-seal-report literal, not the C5 pin · refs `deploy/release_lint.py`, `tests/test_release_lint.py`, [#656] · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
