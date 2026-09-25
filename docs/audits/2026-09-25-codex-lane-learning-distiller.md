# Codex Review — lane-learning-distiller

**Date:** 2026-09-25
**Branch:** `worktree-lane-learning-distiller`
**HEAD:** `5b8c0721`
**Diff range:** `main..worktree-lane-learning-distiller`
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
## CRITICAL

(none)

## HIGH

## HIGH scripts/learning_distiller.py:184 — FAILED rows have no runnable regression check

**What:** Every `failed` candidate sets `check` to a comment rather than an executable command.  
**Why:** Consumers cannot run the promised regression check for exactly the lane-failure cases this tool is intended to surface.  
**Fix direction:** Derive a concrete check from the failure receipt, or represent missing checks separately instead of populating `check` with a comment.

## HIGH scripts/learning_distiller.py:247 — Dispatcher-fault rows point to a nonexistent test

**What:** The generated command always invokes `tests/test_dispatch_repair_launch.py`, which is not present in the repository.  
**Why:** Every dispatcher-fault candidate emits a command that fails immediately, despite being presented and tested as runnable.  
**Fix direction:** Reference an existing regression test, add the intended test, or explicitly model this as a pending test rather than a runnable check.

## HIGH scripts/learning_distiller.py:265 — REFUSED artifacts are labeled repaired without verifying repair completion

**What:** Any supplied parseable REFUSED file becomes a `repair` row; the integrator receipt is never consulted to establish that its lane repaired and merged.  
**Why:** A closed batch containing an uncompleted or failed repair is silently reported as a successful repair learning.  
**Fix direction:** Correlate each REFUSED slug with the integrator’s terminal state and distinguish uncompleted/failed repairs from merged ones.

## MEDIUM

(none)

## LOW

(none)