# Codex Review — lane-landing-probe

**Date:** 2026-09-27
**Branch:** `worktree-lane-landing-probe`
**HEAD:** `bf504755`
**Diff range:** `main..worktree-lane-landing-probe`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

## [HIGH] .github/workflows/conductor.yml:94 — Matrix job names no longer match the declared required check

**What:** The matrix emits `pytest (ubuntu-latest)` and `pytest (windows-latest)`, while the required-check payload still requires `pytest`; the existing agreement test compares job IDs rather than emitted check names.  
**Why:** If the declared ruleset is enabled, GitHub will wait for a `pytest` check that the workflow no longer reports, blocking landings.  
**Fix direction:** Update the required contexts and test their matrix-expanded names together with the workflow.

## [HIGH] .github/workflows/conductor.yml:94 — Matrix conversion breaks CI verdict’s suite-gate reader

**What:** The workflow no longer produces a job named exactly `pytest`, but `scripts/ci_verdict.py` selects that exact job name to read the suite-gate log.  
**Why:** CI verdicts from matrix runs lose the baseline and test-level regression data, falling back to coarse job-level failures.  
**Fix direction:** Make the verdict reader handle both matrix job instances and add a matrix-shaped regression fixture.

## Medium

(none)

## Low

(none)