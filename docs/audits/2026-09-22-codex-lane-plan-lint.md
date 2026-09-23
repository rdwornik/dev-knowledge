# Codex Review — lane-plan-lint

**Date:** 2026-09-22
**Branch:** `worktree-lane-plan-lint`
**HEAD:** `98220f38`
**Diff range:** `main..worktree-lane-plan-lint`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Consumer:** [#961] (this lane's row, `LANE-W4B-5-plan-lint.md`)

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

**Disposition:** both HIGH findings fixed in the same branch, one commit after this record's
HEAD — `cmd_report` now exits non-zero on a BLOCKING finding (matching `cmd_check`), and
`find_cycle` refuses a circular `Starts after` declaration before any finding is classified
(`is_ordered` would otherwise read every pair on the cycle as ordered, silently downgrading a
real collision to `ORDERED`). Both fixes carry a RED-first test.

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/plan_lint.py:606

**What:** `report` prints BLOCKING findings but always exits successfully.  
**Why:** Its own docstring calls it the freeze-time command, so an automated gate using it accepts invalid plans.  
**Fix direction:** Return a non-zero status whenever `lint()` yields a BLOCKING finding, and cover the CLI exit status in tests.

## [HIGH] scripts/plan_lint.py:275

**What:** Circular `Starts after` declarations are treated as valid ordering, suppressing file/moment hazards as `ORDERED`.  
**Why:** A cycle has no executable ordering; e.g., A after B and B after A makes `is_ordered()` true and can allow `check` to exit zero despite an unschedulable conflicting plan.  
**Fix direction:** Detect and refuse dependency cycles before classifying collisions or calculating the critical path; add a cyclic-contract test.

## Medium

(none)

## Low

(none)