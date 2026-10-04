---
id: "[#1367]"
title: "The integrator merges only on a green CI verdict for the exact sha, and main is protected by an enabled ruleset"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1367] [P1][L] **The integrator merges only on a green CI verdict for the exact sha, and main is protected by an enabled ruleset** - R64 (operator, 2026-10-03): MERGE-PATH M4 is ratified. The integrator merges only on a green CI verdict for the exact sha bound for `main`, compared test by test against `main`'s baseline; IN-PROGRESS, cancelled, skipped and not-run are distinct non-pass states and IN-PROGRESS fails closed; `main` is protected by a GitHub ruleset that requires the CI check, with the correct context name and enforcement on; the rehearsal on protected `main` comes first. · Done when: tests show the merge path refuses each of IN-PROGRESS, cancelled, skipped, not-run (and timed_out) and refuses a test red on the merge and green on the base; `gh api repos/{owner}/{repo}/rulesets` shows the ruleset with enforcement `active` and a required-check context that matches the CI job name; the rehearsal on protected `main` is recorded as passed before the ruleset is armed · owner: lane `b2-merge-gate` (W1-2) builds the merge path; the integrator arms the ruleset at B2-W1 close (BATCH-COMMON section 2 (m)) · touches: `scripts/merge_path.py` (W1-2), `deploy/conductor-required-checks.ruleset.json`, tests · kill-candidates: none -- `[#966]` makes CI's verdict the merge gate and `[#964]` runs every check once; neither arms the ruleset · refs `[#966]`, `[#964]`, `deploy/conductor-required-checks.ruleset.json`, `protocols/STANDING_RULINGS.md` section AR (R64) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R64 in `to-browser/RATIFICATION-2026-10-03.md R64`
