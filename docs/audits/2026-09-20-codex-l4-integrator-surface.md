# Codex Review — l4-integrator-surface

**Date:** 2026-09-20
**Branch:** `worktree-lane-l4-integrator-surface`
**HEAD:** `97326c4d`
**Diff range:** `main..worktree-lane-l4-integrator-surface`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/4/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/gates.py: does every declared gate run exactly once and does a red/unstartable/raising gate always yield a RED verdict and non-zero exit? Any path where a gate failure is swallowed, or where the impacted-tests gate silently becomes the full suite or passes on an unresolvable base ref?
- scripts/review_packet.py resolve_range/merge_range/changed_in_merge: is the post-merge range really the merge's own (^1..M)? Any case where an empty range renders a packet against nothing, or a wrong merge is picked (octopus, several merges of the same tip, a tip that is not a second parent)?
- .claude/commands/lane-integrate.md: is the order merge -> moment:merge -> push -> remove -> moment:teardown coherent; does a refusal really stop the push; anything that weakens an existing check?
- tests/test_integrator_surface.py: vacuous assertions; do the RED-first tests really fail without the change?

---

## Findings
## CRITICAL

## [CRITICAL] .claude/commands/lane-integrate.md:151 — refusal does not actually block push

**What:** The sequential shell snippet runs `git push` even if the merge moment or raced suite/review exits non-zero.  
**Why:** A RED comparator/gate verdict can still be pushed and followed by teardown, despite the surrounding refusal policy.  
**Fix direction:** Make merge verification, race, push, and teardown a fail-closed conditional chain; add a regression test for a failing moment not reaching push.

## HIGH

## [HIGH] scripts/review_packet.py:111 — octopus merges are accepted as lane merges

**What:** `merge_range()` only rejects commits with fewer than two parents, so an octopus merge is accepted and rendered as `M^1..M`.  
**Why:** That range and its derived files include every non-first-parent branch, not solely the lane’s change.  
**Fix direction:** Require exactly two parents for supported lane merges, and refuse octopus merges.

## [HIGH] scripts/review_packet.py:129 — ambiguous matching merges silently select the newest one

**What:** `_merge_of_tip()` returns the first first-parent merge whose second parent matches the tip.  
**Why:** If multiple merges reference that tip, the packet may describe a different merge than the intended integration without any refusal.  
**Fix direction:** Collect all matches and refuse ambiguity unless the caller supplies the merge SHA explicitly.

## [HIGH] scripts/review_packet.py:140 — empty symmetric-difference ranges bypass refusal

**What:** `resolve_range()` returns any range containing `...` without checking whether it selects commits.  
**Why:** A valid empty range such as `main...worktree-lane-x` can render a packet against nothing.  
**Fix direction:** Validate emptiness for supported symmetric-difference ranges too, then resolve or refuse consistently.

## [HIGH] scripts/gates.py:136 — `SystemExit` from a runner bypasses the RED verdict artifact

**What:** Runner exceptions catch `Exception`, but not `SystemExit` (or other `BaseException` subclasses).  
**Why:** A runner calling `sys.exit(0)` terminates the process green before remaining gates run or a RED verdict is written.  
**Fix direction:** Normalize runner termination into a failed gate result while preserving intentional process interruption semantics as an explicit, non-green outcome.

## MEDIUM

(none)

## LOW

(none)
---

## Disposition (lane-l4-integrator-surface, 2026-09-20)

The wrapper printed a heuristic 0/0/0/0; the counted tally is **1/4/0/0** (the CRITICAL heading has a different shape from the ones the heuristic greps). All five FIXED, each RED-first in its own commit (`ee90fd41`), fix commit follows it.

| finding | disposition |
|---|---|
| CRITICAL lane-integrate.md:151 refusal does not block push | FIXED -- the walk is one `&&` chain; `test_a_refused_verification_never_reaches_push_or_teardown` runs the REAL block under bash with `uv`/`git` stubbed, with a positive control that push IS reached when all verification passes |
| HIGH review_packet.py:111 octopus accepted | FIXED -- `merge_range` requires exactly two parents |
| HIGH review_packet.py:129 ambiguous matching merges | FIXED -- more than one first-parent merge of the tip refuses and names `--merge <sha>` |
| HIGH review_packet.py:140 empty `...` range bypasses refusal | FIXED -- an empty symmetric range is refused outright |
| HIGH gates.py:136 SystemExit from a runner | FIXED -- recorded as a failed gate; the gates after it still run |

Not re-run after the fixes: a second Codex pass (the fixes are each covered by a RED-first test).
