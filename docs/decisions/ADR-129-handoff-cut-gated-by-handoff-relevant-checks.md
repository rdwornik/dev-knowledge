# ADR-129: The handoff cut is gated by handoff-relevant checks only; the whole-repository verdict is reported, and the preflight moves to batch close

- **Status:** Accepted
- **Date:** 2026-10-01
- **Decision tier:** Path A — a `/decide` proposal for operator ratification (R14, ADR-108 §A).
- **Related:** ADR-128 (paste shape and BD-manifest ratified, kept unchanged); ADR-124 D5; ADR-120 (the spine); rows `[#1328]` `[#1329]` `[#1330]`; R26, R28, R38, R41, R42, R44, R45.
- **Decommission:** none.
- **Source:** operator ruling, `to-cc/BATCH-HANDOFF-REDESIGN-BUILD-2026-10-01.md` v2 (his paste of the batch order IS his ratification of `to-browser/PROPOSAL-ADR-HANDOFF-REDESIGN-2026-09-30.md` §9, R44: "both builds, plus the incremental `check_review_artifact_coverage`"); R45 ("A failure test before any repair"). Landed in-repo by lane `lane-handoff-redesign`, batch HANDOFF-REDESIGN-BUILD.

## Context

No handoff cut since 2026-09-10 had succeeded on its first attempt. Across six cuts: 2 to 6+
attempts each, about 1 h 21 min to 5 h 11 min, and the 2026-09-30 cut was still held at this
lane's render.
- In 4 of 6, the cut was refused by a hard-fail somewhere in the repository.
- In another 4 of 6, a repair made during the cut created new hard-fails.

Both reach the cut through one line: the preflight's row 1 ran the whole 57-organ `audit.py
ship-gate` and refused on any hard-fail (`scripts/gen_handoff.py:986` at render).

The gate ran serially:
- **Measured on 6df37302:** 877 s in-process and 17 m 08 s launcher wall time, against a 900 s
  (later 1800 s) ceiling.
- **One advisory organ was 73% of that:** `check_review_artifact_coverage` (641.8 s). By its own
  ruling it can never produce a hard-fail, so it could never change row 1's hard-fail count.
- **On CI Linux the same gate took 60 s.**

Web practice splits gates into fast pre-boundary checks and comprehensive post-boundary checks,
and keeps state in files and git rather than in a hand-carried transcript — see this ADR's lane
session, "Step 2" (Python `concurrent.futures.ThreadPoolExecutor` for independent I/O-bound
checks; `git log --name-only` / `--diff-merges=first-parent` for a single-pass incremental history
walk instead of one `git diff` per merge).

## Decision

1. **Row 1 runs the handoff organ set, not the whole registry.**
   - The set is data: `HANDOFF_ORGAN_NAMES`, one tuple in `scripts/audit.py`, resolved by name at
     call time and passed through `run_checks(checks=handoff_organs(), parallel=True)`. It holds
     `check_handoff_probes`, `check_supplement_folded`, `check_handoff_bundle_structure`,
     `check_handoff_version_stamp`, `check_residual_completeness`, `check_boot_byte_budget`,
     `check_journal_spine_anchor`, `check_dispatch_drift`, `check_dispatch_verb_agreement`,
     `check_routing_agreement` and `check_doc_claims`.
   - **Membership criterion** (G1): an organ is in the set if a hard-fail in it can block the
     incoming seat's first dispatch or first push, or can make the bundle misdescribe the
     repository. The first two tests are the dispatch and routing organs and the ADR-85 anchor
     backstop; the third is the handoff organs and `doc_claims` (the P6 failure of 09-19).
   - A hard-fail in the set refuses the cut, as before.
   - `check_doc_claims` stays the one named exception: WARN-only (`HANDOFF_ORGAN_WARN_ONLY`), its
     WARNs carried into the bundle notes rather than asserted as failable by the set-membership
     test — a ratified conflict with the set's own membership criterion, reported for the operator
     rather than resolved silently (item 10/L5 of this lane's contract).
2. **The whole-repository ship-gate verdict is reported, never refused on.**
   - Its source is read from CI — the `ship-gate` job for the cut sha when one exists, otherwise a
     named `not run` — never executed locally at the cut. It goes into the bundle's notes and the
     residual's drift flags; it never blocks.
   - "A handoff is not a release" (the 2026-09-08 amendment to row 1) is extended from WARNs to
     hard-fails outside the handoff set.
3. **Gates 1 and 2 (WINDOW=BATCH, no-leftovers) are unchanged** at the real cut. `--dry-cut` now
   runs gate 3 (the handoff organ set and the state rows) while still skipping gates 1-2 — a lane
   or integration worktree is a linked worktree, so gate 2 refuses there by construction; at
   `a38b6faf` the dry cut skipped all three gates, so it evaluated zero organs.
4. **A batch-close stage runs the preflight's state rows and a `--trial-cut`.** It runs at the
   integrator's `moment:batch-close` (`optional: true`, `manual_until: 2026-10-05`) until that
   moment is armed. The two cut-day rows (`ratification_present`, `ledger_refreshed`) are
   false-red by construction outside a real cut window, so the trial cut excludes them
   (`TRIAL_CUT_EXCLUDED_ROWS`), reporting them `n/a` (`TRIAL-CUT-EXCLUDED`) rather than evaluating
   them; every other row runs for real, and a genuine FAIL still refuses the close.
5. **`check_review_artifact_coverage` becomes incremental and single-pass.** One batched
   `git log --first-parent --diff-merges=first-parent --name-only` walk replaces the per-merge
   `git diff --name-only <first_parent> <sha>` spawn. Finding-identical, not a behavior change —
   row `[#560]` ("reads only the FIRST branch/HEAD triple") is explicitly not discharged by this
   rewrite.
6. **`[#1330]` stays required.** `[#1328]`, `[#1329]` and the proposal's A1 leave the cut path but
   stay open rows.

## Quality attributes

**Quality attribute(s):** Availability (the order's "reliability": a cut succeeds on its first
attempt), Performance, Usability (operator steps; and, for the incoming seat, the order's
"fidelity"), Testability, Modifiability — all from ADR-124 D5's closed set.

**Scenario** (six parts; one per attribute):
- **Availability.**
  - *Source of stimulus:* a lane, or a repair made during the cut.
  - *Stimulus:* it lands a hard-fail in an organ outside the handoff set, for example
    `funnel_lifecycle` leg (c) on a freshly filed row.
  - *Artifact:* `gen_handoff.py` preflight row 1.
  - *Environment:* the cut, on a shared Windows box, with lanes merged that day.
  - *Response:* the cut proceeds, and the hard-fail is printed in the residual's drift flags with
    its organ and evidence.
  - *Response measure:* 0 cut refusals caused by an organ outside the handoff set, over the next
    two cuts, read from the receipt's refusal log.
- **Performance.**
  - *Source:* the operator.
  - *Stimulus:* `/handoff`.
  - *Artifact:* the preflight.
  - *Environment:* the same shared box.
  - *Response:* the preflight completes.
  - *Response measure:* preflight ≤ 120 s wall time on that box — this lane's Step 1 acceptance
    test pins it as the Done-when.
- **Usability.**
  - *Source:* the operator.
  - *Stimulus:* a cut request.
  - *Artifact:* the `/handoff` flow.
  - *Environment:* the end of a window.
  - *Response:* one cut attempt, then the SUPPLEMENT fill.
  - *Response measure:* attempts per cut = 1 on the next two cuts. Before this ADR it was 2 to
    6+.
- **Testability.**
  - *Source:* `moment:batch-close`.
  - *Stimulus:* a batch's last merge.
  - *Artifact:* the state rows and a `--trial-cut`.
  - *Environment:* unattended.
  - *Response:* a trial cut runs by itself and its verdict is recorded.
  - *Response measure:* every batch close in the next window has a recorded trial-cut verdict, and
    none costs over 120 s.
- **Modifiability.**
  - *Source:* a new organ author.
  - *Stimulus:* a new repository organ that hard-fails.
  - *Artifact:* the handoff organ set.
  - *Environment:* ordinary development.
  - *Response:* the cut is unaffected unless the organ is added to the set, which is a one-line
    data change (`HANDOFF_ORGAN_NAMES`) reviewed as such.
  - *Response measure:* 0 operator rulings needed to unblock a cut for a non-handoff organ. Three
    were needed in three days before this ADR: R26, R28 and R42.

**Decision evidence:**
- per-organ telemetry of the serial run on 6df37302 (`to-browser/PROPOSAL-ADR-HANDOFF-REDESIGN-2026-09-30.md` §1.3);
- CI `ship-gate` job 110033621290 (`wall_seconds=60`);
- this lane's live-repo measurement: `check_review_artifact_coverage` 747.88s -> 9.23s (~81x),
  finding-identical;
- this lane's Step 1 acceptance test, GREEN against the built generator;
- the web sources cited in this lane's session file, "Step 2".

## Consequences

- A cut can proceed while the repository is RED. The next seat sees it as a drift flag, not as
  silence.
- The handoff set is a new list that has to be maintained. An organ wrongly left out turns a real
  handoff defect into a report. The mitigation is a test pinning the set's membership and a review
  of it at every ADR that adds an organ.
- The slow organ remains batched rather than per-merge, which fixes the ship-gate cost for every
  consumer of `check_review_artifact_coverage`, not only the handoff cut.

## Flip-condition

- **Revert item 2** (reported, not refused) on the first of the next two cuts where an organ
  outside the set, listed in that cut's receipt as a hard-fail, is named by the incoming seat as
  blocking its first dispatch or first push. That would show a non-handoff organ was cut-relevant
  after all.
- **Widen the set** by the organ named, rather than reverting, if one such organ is found.
- **Revisit item 4** if the batch-close stage false-reds on more than 1 of the first 5 batch
  closes.

## Alternatives considered

- **The current generator plus one-off unblock fixes.** Clears a given day's fails but not their
  class, which recurred in 4 of 6 cuts and needed three rulings in three days.
- **A thin paste with state in the repository, with no organ-set split.** Changes the boot, while
  the hours are spent at the cut; would also supersede ADR-128 item 2 with no evidence the shape
  misleads.
- **A progress file with no generator.** Would pass the four handoff-class true positives
  silently.
- **Status quo.** The cut stays held.
- **Batching the slow organ alone, without the organ-set split.** Fixes the time, not the false-blocker class.
- **Raising the ceiling alone (900 s -> 1800 s), with no organ-set split.** Treats the symptom —
  73% of the time was one advisory organ that could never change the hard-fail count.
