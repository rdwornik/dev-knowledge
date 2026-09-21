# Codex Review — lane-repo-housekeeping

**Date:** 2026-09-21
**Branch:** `worktree-lane-repo-housekeeping`
**HEAD:** `573e436e`
**Diff range:** `main..worktree-lane-repo-housekeeping`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/0/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- ecosystem/disposition-register.yaml: the renewed warn-review-artifact-lane-c-504-no-tally entry now keys its match on a long contiguous string ending '(+1 more)'. Does that match the real WARN evidence produced by scripts/audit.py check_review_artifact_coverage, and can it wave through unrelated drift (whole-Finding contract)?
- the two removed entries (warn-doc-rot-accretion-backlog-241, warn-doc-rot-grooming-cadence-hold): is the removal justified, and does the YAML still parse?
- ecosystem/doc-counts.md: are the regenerated counts honest?
- tasks/929: the appended citation line must not break the task-file parse.

---

## Findings
## CRITICAL

### ecosystem/disposition-register.yaml:563 — truncated aggregate match suppresses unrelated WARNs

**What:** The renewed match keys only on the first five untallied artifacts plus `(+1 more)`, not the hidden sixth artifact it claims to disposition.  
**Why:** Replacing the hidden sixth with any unrelated untallied artifact leaves this exact evidence prefix unchanged, so the one aggregate Finding remains suppressed—violating the whole-Finding contract.  
**Fix direction:** Make the audit emit one Finding per untallied artifact (or include complete identity-stable evidence), then match the specific legacy artifact.

## HIGH

(none)

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (lane-repo-housekeeping, 2026-09-21)

**Finding 1 (CRITICAL, register :563) -- ACCEPTED.** The renewed `warn-review-artifact-lane-c-504-no-tally` match keyed on five visible pairs plus `(+1 more)`, so the hidden sixth artifact could be swapped for any other and the aggregate Finding would stay suppressed. Verified against `check_review_artifact_coverage`, which prints `named[:5]` and a count. Fixed in the following commit by REMOVING the entry rather than renewing it: the WARN is live and stays an undispositioned WARN, as before this lane. The real fix (one Finding per untallied artifact) is a script change this lane may not make. Doc-counts, the two other removals and the task-row citation drew no finding.

## Disposition ledger

Ledger of the 2026-09-20 build reviews (batch `worktree-lane-l1`..`l8` and `lane-loop-eval`). Each row's locator is the merge that landed the record together with its fixes; the record's own disposition section is where each finding is decided. Consumed by row `[#929]`.

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-20-codex-l1-spine-moments.md | ACTIONED | `5a1a404b` -- lane-l1 merge; the three HIGH are fixed in that range and dispositioned in the record's own `## Dispositions` section |
| 2026-09-20-codex-l2-dispatch-guards.md | ACTIONED | `5dbd9527` -- lane-l2 merge; fixes and per-finding dispositions in the record's `## Dispositions` section |
| 2026-09-20-codex-l3-organ-truth.md | ACTIONED | `b8727474` -- lane-l3 merge; all three HIGH fixed in `e00b69f2`, RED first in `643dc4d7` (the record's own Disposition line) |
| 2026-09-20-codex-l4-integrator-surface.md | ACTIONED | `16d9defa` -- lane-l4 merge; the record's `## Disposition` table marks each finding FIXED, including the octopus-merge HIGH |
| 2026-09-20-codex-l5-no-leftovers.md | ACTIONED | `71be4ace` -- lane-l5 merge; three HIGH ACCEPTED and fixed per the record's `## Dispositions` |
| 2026-09-20-codex-l6-test-pairing.md | ACTIONED | `1dc1ca41` -- lane-l6 merge; 5 ACCEPT / 0 REJECT, each with a test, per the record's `## Disposition` |
| 2026-09-20-codex-l6-test-pairing-fixes.md | ACTIONED | `1dc1ca41` -- lane-l6 merge, second pass; 4 ACCEPT / 0 REJECT per the record's `## Disposition` |
| 2026-09-20-codex-l7-prior-art.md | ACTIONED | `cdea9bdb` -- lane-l7 merge; all six findings accepted and fixed per the record's `## Disposition` |
| 2026-09-20-codex-l8-lane-end.md | ACTIONED | `d24d0535` -- lane-l8 merge; all five HIGH fixed, each with a test, per the record's `## Disposition` |
| 2026-09-20-codex-loop-eval-mapping-adversary.md | ACTIONED | `29cc3cbb` -- lane-loop-eval merge; the record carries an accept/reject reason per finding and ADR-120 cites it |
| 2026-09-21-codex-lane-repo-housekeeping.md | ACTIONED | `573e436e` -- the reviewed head; its one finding is fixed in the commit that follows it (see Finding 1 above) |
