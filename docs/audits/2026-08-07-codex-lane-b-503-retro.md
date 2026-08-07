# Codex Review — lane-b-503-retro

**Date:** 2026-08-07
**Branch:** `worktree-lane-b-503-doc-currency`
**HEAD:** `a4f4f1e9`
**Diff range:** `5af0b33c76d1b38ab23538d779c5637d2e0463bf..a4f4f1e9`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (RETROACTIVE)
**Tally:** 0/0/0/0
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- RETROACTIVE review of an already-merged lane (batch-1 lane B, [#503]).
- scripts/audit.py: _HUB_ONLY_FRESHNESS_FILES gains protocols/DEFINITION_OF_DONE.md. Is the registry addition correct and complete? Does anything else need to move with it?
- tests/test_reverse_dep_oracle.py: line-pin updates 322->326 / 323->327 following the audit.py insertion above. Are the pins correct and is pinning by line number a latent defect?

---

## Findings
## Critical

(none)

## High

(none)

## Medium

(none)

## Low

(none)

`DEFINITION_OF_DONE.md` is correctly added as a hub-only freshness target; consumers derive their portable list from `canonical_freshness_gate.py`, so nothing else needs to move. The `Finding` pins are correct at target commit: 0-based `326` / 1-based `327`.
---

## Disposition — 2026-08-07 (PRE-2 arc)

**Tally 0/0/0/0. Nothing to act on.**

**Why this review exists at all, and a correction to the brief that commissioned it.** The
PRE-2 brief described `a4f4f1e9` as "the docs-only integration-arc merge" and directed that it
receive a cited disposition rather than a review. **That premise does not survive contact with
git:** the merge changes `scripts/audit.py` (+6/-1) and `tests/test_reverse_dep_oracle.py`
(+3/-3), so it is code-impact under the [#480] predicate and is flagged for the same reason
lanes A and C were. Dispositioning it as docs-only would have been a false disposition — the
one thing the brief's own guardrail forbids ("no dispositioning a WARN that step-2's reviews
don't genuinely cover"). It was reviewed instead. The diff is 8 lines; the review cost less
than arguing about it would have.

The brief's *instinct* was sound — this is the smallest code diff in the batch, and the review
confirms it carries nothing. The label was what was wrong, not the judgement.

**Reviewed content, for the record:** `_HUB_ONLY_FRESHNESS_FILES` gains
`protocols/DEFINITION_OF_DONE.md` (a registry addition, no logic), and two line-pins in the
reverse-dep oracle test move 322→326 / 323→327 to follow the insertion above them. terra
confirmed both: the hub-only list is the correct home (consumers derive their portable list
from `canonical_freshness_gate.py`, so nothing else moves with it), and the pins are correct at
the target commit.

**Not raised, and worth naming anyway:** line-number pinning in
`tests/test_reverse_dep_oracle.py` is a known recurring maintenance cost in this repo — an
`audit.py` insertion shifts it every time. Out of scope here (the row is closed and this is a
retroactive pass), and it is already lived knowledge rather than a new finding.
