---
id: "[#911]"
title: "A gate whose precondition is passing that same gate -- the silent-rule ratchet cannot accept an operator-approved raise until the raise is already pushed"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "BUILD MODE B2 integration order 2026-09-19"
generates: BACKLOG.md
---

- [#911] [P1][S] **A gate whose precondition is passing that same gate -- the silent-rule ratchet cannot accept an operator-approved raise until the raise is already pushed** - `check_silent_rule_ratchet` takes its previous value from `min(origin/main, main)` (`scripts/audit.py` `_BASELINE_REFS`, `_target_baseline_state`), and `validate_transition` fails any same-detector increase. An operator-ruled raise therefore fails on every branch and on local main until it is on origin/main, and getting it onto origin/main is the act a review gate blocks. At B2 integration (2026-09-19) the ruled 447 -> 452 raise drew a Codex terra HIGH for exactly this, which held the push until the operator withdrew the blocking condition. The same trap is recorded for 428 -> 441, 443 -> 447 and the 2026-09-16 aa-14 recurrence (memory `commensurable-ratchet-raise-has-no-landing-path`). This is the **sixth instance this window** of a check that is green on its own test and blind to the case it was built for. The ratchet tests prove it refuses an unauthorised raise, and none proves it can land an authorised one · Done when: the ratchet accepts a same-detector raise that carries a recorded operator authorisation in `ecosystem/silent-rule-baseline.yaml` (ruling reference, date, cause, one-off statement) and passes it **on the branch and on local main before any push**; an unauthorised raise still fails; a RED-first test lands the authorised raise on a tree whose origin/main still holds the old value and asserts PASS; and the baseline file's header no longer states that "a branch-side check may read raise-rejected" as expected behaviour · implements: BUILD MODE B2 integration order 2026-09-19 · refs `scripts/audit.py` (`check_silent_rule_ratchet`, `_target_baseline_state`), `scripts/silent_rule_detector.py::validate_transition`, `ecosystem/silent-rule-baseline.yaml`, `docs/audits/2026-09-19-codex-b2-regressions-fix.md`, `[#805]` · kill-candidates: [#805] -- its Done-when includes "ratchet accepts a raise carrying a recorded authorisation"; if [#805] carries that leg, this row folds into it
