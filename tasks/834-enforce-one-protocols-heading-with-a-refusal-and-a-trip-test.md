---
id: "[#834]"
title: "Enforce one protocols/ rule-bearing heading with a refusal and a trip-test"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#834] [P2][S] **Enforce one protocols/ rule-bearing heading with a refusal and a trip-test** - Operator ruling 2026-09-16 (batch AB, plan: "one `protocols/` heading enforced"; standing constraint: "no new commit-tier gate without a measured cost"), following the `[#786]` `validate_prepend_order.py` pattern already on main. `protocols/*.md` carries multiple rule-bearing headings (a heading whose body states a MUST/NEVER/refuse-shaped rule) with no organ enforcing them, each carried by prose alone the way "### Order conventions" was before `[#786]`. Method: enumerate every rule-bearing heading in `protocols/*.md`, record per heading whether any organ enforces it (cite the organ, or `none`), exclude PLAYBOOK "### Order conventions" (already gated by `validate_prepend_order.py` under `[#786]`), then rank the `none` set by breaches found in `git log` (commit SHAs) and pick the top one · Done when: (1) the heading x organ x breach table is in the end-of-lane artifact; (2) the enforcement stage is chosen for its cost -- an existing stage (an `audit.py` check, an existing validator's rule, a PreToolUse deny) is preferred over a new pre-commit hook, and a new commit-tier hook is admitted only with its wall time measured on this box over a typical commit's staged set; (3) a RED-first trip-test that fails the moment the refusal stops raising, a passing-path test, and one test replaying a real historical breach SHA as a fixture; (4) the heading's prose gains one line naming its enforcement point (organ + stage), so the rule and its organ cite each other; (5) targeted `uv run --locked pytest` green, `ruff` clean · refs `protocols/PLAYBOOK.md`, `[#786]` (`scripts/validate_prepend_order.py`, the sibling gate this pattern extends), `protocols/STANDING_RULINGS.md` "The decision budget" · kill-candidates: none -- this row is the first heading picked off a larger `none` set; further headings are separate rows filed under `## To file` · source: batch AB manifest, lane `lane-ab-834-protocols-heading-gate`
