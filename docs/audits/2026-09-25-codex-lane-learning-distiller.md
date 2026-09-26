# Codex Review — lane-learning-distiller

**Date:** 2026-09-25
**Branch:** `worktree-lane-learning-distiller`
**HEAD:** `5b8c0721`
**Diff range:** `main..worktree-lane-learning-distiller`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low. All 3 HIGH findings fixed in the next commit (see commit message): repair rows verified against the integrator's own STATE line before being kinded "repair"; every not-yet-written check is marked proposed=True instead of presented as runnable. -->

**Disposition:** all 3 HIGH findings fixed. (1) `_verify_refused_row` now checks the integrator receipt's LAST `STATE <slug> ...` line for that exact slug and only keeps `kind="repair"` when it reads `MERGED`; anything else re-kinds the row `unverified_refusal` with the actual state named in the title. (2) `CandidateRow` gained a `proposed: bool` field; `dispatcher_fault` and `failed` rows (whose checks name a regression test that does not exist yet) set it True, `render()`/`to_dict()` say so explicitly rather than let the bare command line imply it passes today. (3) The same `proposed` mechanism covers the `failed`-row case (was a `#`-comment, non-runnable; now a real command line, marked proposed).

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: lane contract `LANE-5B2-13-learning-distiller.md` (batch WAVE5B-N2 row 13). Changes:
new `scripts/learning_distiller.py` (5e v0 -- REFUSED/repair/FAILED/dispatcher-fault receipts
-> candidate rows, ruling a); `tests/test_learning_distiller.py`; one additive `fates:` line
in `ecosystem/harness.yaml` (ruling a/g).

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