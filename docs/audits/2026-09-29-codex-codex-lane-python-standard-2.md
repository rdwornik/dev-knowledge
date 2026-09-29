# Codex Review — codex-lane-python-standard-2

**Date:** 2026-09-29
**Branch:** `worktree-lane-python-standard-2`
**HEAD:** `65836465`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/1/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

consumer: the frozen contract $env:CLAUDE_PROMPTS_DIR\LANE-5B5R-9-python-standard-2.md

---

## Findings
## Critical

(none)

## High

## [HIGH] pyproject.toml:406 — Frozen contract’s 10-code Ruff set was silently reduced to seven

**What:** `SIM300`, `RET501`, and `PLR1711` from the preserved tip are removed from `extend-select`.  
**Why:** The frozen lane contract explicitly requires reusing its declared 10-code set; narrowing it changes the delivered standard rather than reporting the conflicting sibling-owned violations as a premise failure.  
**Fix direction:** Reconcile this with an explicit contract amendment, or hand back the lane as blocked/partial instead of changing the required rule set.

## [HIGH] templates/ruff-config-block.toml:49 — The shared Ruff rule set has no parity gate

**What:** The template duplicates the hub’s `extend-select` list but explicitly states that `test_fleet_parity.py` does not verify its identity.  
**Why:** A future edit can silently make the consumer-facing canonical template diverge from the active hub configuration, defeating the contract’s shared-rule-set guarantee.  
**Fix direction:** Add a test that parses both TOML files and requires their `extend-select` values to match, or derive both from one source.

## Medium

## [MEDIUM] templates/ruff-config-block.toml:67 — New template text violates the frozen wording restriction

**What:** The added comment contains “must never.”  
**Why:** The lane contract prohibits adding `must`, `shall`, or `never` under `templates/**`; this can cause the lane’s close-out contract checks to refuse the result.  
**Fix direction:** Reword the guidance descriptively without those restricted terms.

## Low

(none)