# Codex Review — lane-handback-fixes

**Date:** 2026-09-24
**Branch:** `worktree-lane-handback-fixes`
**HEAD:** `b6b2038c`
**Diff range:** `main..worktree-lane-handback-fixes`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low, as found (pre-fix); all 3 High findings below were fixed in this lane's own follow-up commit. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

no-consumer: lane-scoped self-review of this lane's own D10/D11/D14/D23 fix, no separate governance row filed here — DECLARE-WINDOW-DEFECTS-2026-09-23 items are LANE-5A-5's row-filing job, not this lane's

---

## Focus

- D11: scripts/ship_gate_diff.py's (check_name, status) comparator vs the old bare-check_name diff -- does it correctly resolve the wave-4B organ_truth false negative and avoid new false positives (e.g. evidence-text-only drift under an existing status)?
- D10: scripts/handback.py now writes to-browser/HANDBACK-REFUSED-<lane>.md instead of REFUSED-<lane>.md -- confirm no remaining path collision with the integrator's REFUSED-<lane>.md and no stale references.
- D23: scripts/seat_registry.py's fresh-bind-reads-live change and scripts/worktree_occupancy.py's state/status fallback -- correctness and any missed edge cases.
- D14: scripts/plan_lint.py's new find_new_organs_without_fate (class 5) -- correctness, false positive/negative risk, and whether the fate-mention regex is too permissive or too narrow.
- Purity: does this diff weaken any existing check the handback organ calls (explicitly forbidden by the lane contract)?

---

## Findings
## Critical

(none)

## High

### scripts/ship_gate_diff.py:88 — Comparator still hides new failures sharing an existing `(check_name, status)`

**What:** Multiple distinct `fail` findings under the same check name collapse to one identity.  
**Why:** A baseline `organ_truth` fail plus a branch-added unfated organ remains `("organ_truth", "fail")`, so the new failure is silently treated as pre-existing.  
**Fix direction:** Compare a stable per-concern identity, preserving tolerance for known volatile evidence while distinguishing newly affected subjects.

### scripts/plan_lint.py:153 — Fate regex accepts unrelated prose as a fate declaration

**What:** Any occurrence of `fate`, `moment`, `manual_until`, or `retire_candidate` anywhere in a contract suppresses findings for every new script it owns.  
**Why:** Text such as “the handback moment” or “this has no fate yet” lets an unfated new organ pass the new class-5 gate.  
**Fix direction:** Require a parseable, script-associated `fates:` entry or a recognized harness-moment ownership declaration.

### scripts/worktree_occupancy.py:135 — Conflicting `status` and `state` records can be read as free

**What:** `_status_of()` silently prefers `status`; e.g. `{status: "idle", state: "busy", cwd: <tree>}` is treated as non-live.  
**Why:** During an external-shape transition or partial update, a busy session can be missed and the dispatcher may reuse its worktree.  
**Fix direction:** Fail closed on conflicting liveness fields, or treat either field reporting `busy` as busy and require its `cwd`.

## Medium

(none)

## Low

(none)