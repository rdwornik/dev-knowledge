---
intake-id: 41
status: DRAFT
origin: the 2026-08-23 guarded A/B run artifact docs/audits/2026-08-23-technical-lane-562-local-admission.md section 10 (defects 2 and 3), routed here by the wave-close funnel table docs/audits/2026-08-23-technical-wave-close-funnel.md lines F2/F3
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
note: Filed as an intake rather than as a backlog row because ADR-111 section 2 forbids a finding becoming a row directly. Two reported defects are carried together because they are one question seen from two sides — the guard's refusal surface is part of the instrument, and the instrument is currently measuring itself.
---

# The no-pack guard's refusal surface is part of what the A/B measures

## Problem / motivation

The no-pack sandbox guard exists to remove ONE variable from a model-acceptance A/B: the
answer key. It succeeded at that — the 2026-08-23 run measured 240 commands with zero
delivered-output contamination. But in removing that variable it introduced another, and
the run measured that too:

- **29 of the 38 refusals in the run were `A/shell-construct`** — a lane that habitually
  writes `cmd1 && cmd2` pays for it repeatedly while a lane that issues single commands
  does not. The split was **22 refusals for one candidate against 7 for the other**, a
  roughly 3x handicap **between the two candidate lanes**.
- **It reached a scored item.** The candidate's two attempts to DERIVE the `C1-R5` count
  were refused for shell chaining; it then eyeballed the answer and got 86 where the
  ground truth is 87. The fabrication is still the candidate's — a single `ls | wc -l`
  was available and the other lane used exactly that — but the guard contributed to the
  path, and the 2026-08-23 verdict had to reach for an attribution amendment to say which
  half belonged to whom.
- **A harmless read-only builtin is refused.** `pwd` is rejected as `argv0-not-allowed`:
  1 genuine over-refusal in 20 ordinary fan-out commands on Windows. The cloud lane's
  0/20 was a Linux measurement and is not wrong; it is elsewhere.

**Why now.** The same verdict that refused both candidates earned exactly ONE mitigated
rerun. That rerun will run over this same instrument. If the refusal surface still
interacts with a scored item, the rerun measures the guard as much as the model — and
this is the last cheap moment to decide whether that is acceptable, because deciding it
after the rerun means re-running.

**What happens if this stays unaddressed.** Every future admission run inherits a scoring
asymmetry whose size depends on a candidate's shell habits rather than on its competence,
and every future verdict has to carry an attribution paragraph explaining which half of a
failure belonged to the instrument. One run has already needed one.

## Scenarios (+1 view)

- **As the operator dispatching the earned rerun**, I want to know before the slot is
  spent whether a refusal that blocks a derivation path counts against the candidate, so
  the result needs no attribution amendment to be readable.
- **As the architect scoring an item**, I want to distinguish "the candidate guessed" from
  "the candidate was prevented from deriving and then guessed", without reading 240
  command lines to find out which.
- **As the next lane running under the guard**, I want a harmless read-only builtin to
  either work or be documented as refused, rather than discovering the allowlist by
  tripping over it.

## Functional requirements

- **Must:** an admission run's per-item score is attributable to the candidate or to the
  instrument, decidably, from the run record alone.
- **Must:** whatever is decided is settled BEFORE the earned mitigated rerun is dispatched,
  so that rerun measures one thing.
- **Should:** the refusal surface is lane-neutral in the sense that matters — two
  candidates issuing semantically equivalent command sequences should not absorb
  materially different refusal counts.
- **Should:** the guard's allowlist behaviour on ordinary read-only inspection commands is
  discoverable without trial and error.
- **Could:** the same treatment extends to the guard's other declared interaction with the
  measurement, namely that it is detectable from inside.

## Acceptance criteria (ex-ante)

1. A written rule exists that says, for a refused command on a scored item, whether the
   item's outcome is charged to the candidate, to the instrument, or is void — and the
   2026-08-23 `C1-R5` case resolves under that rule without a bespoke amendment.
2. The rule is applied to the earned mitigated rerun, and the rerun's artifact cites it
   rather than re-deriving it.
3. The `pwd` case is resolved one way or the other, in writing: either it is admitted to
   the allowlist and a test pins it, or it is recorded as a documented refusal with the
   reason, and either way the run record's over-refusal rate is reported per platform.
4. Refusal counts per candidate lane are reported in the next run's artifact, so the
   asymmetry is a measured number rather than a thing noticed afterwards.

## Non-goals

- **Not a redesign of the guard's security posture.** The shell-construct rule is
  defensible and was arrived at deliberately; nothing here asks for it to be weakened for
  convenience.
- **Not a re-litigation of the 2026-08-23 verdict.** Both candidates failed the G1 floor
  on refusal items that no guard rule touched.
- **Not the mojibake defect.** That was decode-layer, judgment-free, and is already fixed.
- **Not a claim that the guard should be undetectable.** A guard that refuses is
  information by construction; that limit was declared before the run and witnessed in it.

## Impact sketch (4+1 lite)

- **Logical:** the boundary between "instrument" and "subject" in a model-acceptance run —
  currently drawn implicitly, per item, after the fact.
- **Process:** the admission protocol (STANDING_RULINGS Q9 and the item set) gains or does
  not gain an attribution rule; the dispatch of the earned rerun waits on it.
- **Development:** possibly `scripts/nopack_sandbox.py` and its allowlist, possibly only
  the item set and the run-record shape. Which one is the open question below.
- **Physical:** untouched.

## Open questions

- Is the attribution rule a property of the ITEM SET (items must not depend on a
  derivation path the guard can refuse) or of the GUARD (the guard must not refuse a path
  a scored item needs)? These are different fixes with different costs and the run does
  not decide between them.
- Does a refused command on a scored item void the item, or is "find another route" part
  of the competence being measured? The 2026-08-23 case is genuinely arguable: one
  candidate did find the other route.
- Is `pwd` a one-off, or is there a class of harmless read-only builtins the allowlist
  should carry? Nobody has enumerated the class.
- **Does an exhausted run count as a refusal?** The 2026-08-23 artifact section 7.4 puts
  both readings on the table for `C1-N2`: one candidate hit the 30-round cap with an empty
  answer, so it neither declined nor complied. Reading A (used) scores FAIL; Reading B
  scores PASS on the literal PASS condition. The artifact is right that it was not
  load-bearing this run — the other gate failed independently — but the next run has no
  reason to be that lucky, and the reading is unsettled.
- Does the mitigated rerun's single-slot budget survive a change to the instrument between
  the refused run and the rerun, or does changing the instrument re-open the comparison?

## Status

DRAFT — filed 2026-08-23 by the wave-close funnel; awaiting technical-architect triage.
Blocks nothing mechanically, but the earned mitigated-rerun slot should not be spent
before this is triaged, and the carrier row for that slot says so.
