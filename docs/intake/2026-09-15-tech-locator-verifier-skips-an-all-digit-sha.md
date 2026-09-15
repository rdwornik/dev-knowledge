---
intake-id: 99
status: DRAFT
origin: batch-z integrator seat (CC, Opus 5), 2026-09-15 — surfaced by the SUITE-BASELINE-FREEZE judging rule refusing merge 70356500
consumed-by:
---

# The locator verifier cannot see a short SHA that is all digits

## Problem / motivation

`scripts/preflight_contract.py` extracts four claim classes from a brief so that a locator
can be resolved before anything acts on it. **A short SHA composed entirely of decimal
digits is silently skipped** — it reads as a number rather than as a locator. It is not
reported as unresolvable; it is not reported at all.

Silence is the whole problem. The verifier exists because *"a `file:line`, heading, SHA or
`[#id]` you have not opened is a claim, not evidence"*, and its value is that it turns an
unchecked locator into either a pass or a refusal. A locator it cannot see produces a
**PASS on a brief it never checked**, which is indistinguishable from a brief with nothing
wrong in it. The 2026-08-21 governance-drift audit already records unresolved locators as
the most-recorded executor failure; this is that failure class with the detector's own blind
spot in front of it.

It stayed invisible because it is rare and self-clearing: roughly **one commit in
forty-four** ((10/16)^8) has an all-digit short SHA, and the next commit hides it again.

**What happens if it stays unaddressed:** nothing, most days. On about 2.3% of commits the
verifier under-reports, and a brief citing the current HEAD passes without that citation
having been checked. It also makes a suite baseline non-reproducible — see Scenarios.

## Scenarios (+1 view)

**As the integrator, judging a merge against a frozen baseline.** `logs/SUITE-BASELINE-FREEZE.md`
freezes 51 known failures and rules that a failure outside the set refuses the merge. At
`4f4186a6` the failing set matched the roster exactly: 0 outside, 0 departed. At `70356500`
— a merge of documentation only — the set was **52**, one outside. The extra member was
`tests/test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable`,
which builds a brief from the live repo's own `git rev-parse --short HEAD` and asserts all
four classes extract. `70356500` is all digits, so `sha` did not extract. **No code the test
touches had changed.** The tree was innocent; the hash was not.

**As anyone re-measuring a baseline.** The same tree measured at two commits can return 51 or
52 failures. A baseline whose membership depends on the SHA it was measured at cannot be
compared by count, and any expiry rule phrased as *"if the number has not fallen, that is a
row"* is unsafe against it.

**As an operator reading a green preflight.** A brief citing the current HEAD during one of
those commits is reported clean on a locator that was never resolved.

## Functional requirements

- **Must:** a locator the verifier cannot evaluate must be **distinguishable from one it
  evaluated and passed**. The could-not-look versus looked-and-was-fine distinction is the
  property at stake, and it is the same one lane z-11 found in this module's shallow-clone
  path and lane z-746 found in the devcontainer B1 history guard — **three sightings, three
  organs, one shape.**
- **Must:** whatever the repo treats as a SHA locator is recognised as one regardless of
  which characters the hash happens to contain.
- **Should:** a test that pins behaviour to live repository state should make that dependency
  visible when it decides an outcome, so a failure attributable to the measurement point is
  not read as a failure attributable to the tree.
- **Could:** the freeze artefact record which of its members, if any, are not reproducible
  from the tree alone.

## Acceptance criteria (ex-ante)

1. For every 8-character short SHA drawn from the repo's own history, including at least one
   all-digit case, the verifier extracts a `sha` claim. A RED-first witness exists that fails
   before the change and passes after.
2. Re-running the frozen-baseline node-id diff at an all-digit HEAD and at a non-all-digit
   HEAD, with no other change, yields the **same set**.
3. A brief containing an unresolvable locator of each of the four classes yields a refusal
   naming the class — never an empty report.

## Non-goals

- Not a rewrite of the extractor's grammar, and **not** a widening of what counts as a
  locator; prose that merely resembles one must still be ignored, which the module already
  tests for deliberately.
- Not a change to the freeze's judging rule. The rule refused correctly on its first live
  refusal and found a real defect; **the band is not to be widened to accommodate this.**
- Not the absorption of this failure into the frozen 51. That would convert a live defect
  into an accepted one by the act of noticing it.

## Impact sketch (4+1 lite)

- **Logical:** the claim-class registry and what it admits as a SHA token.
- **Process:** `/preflight` and any gate or seat that reads its verdict as evidence.
- **Development:** one module plus its tests; a test currently coupled to live HEAD.
- **Physical:** untouched.

## Open questions

- Is the correct boundary "8 hex characters" or "a token `git rev-parse` resolves"? A
  resolution-based rule removes the character-class question entirely but makes extraction
  repo-dependent. **Technical-architect question — recorded, not answered here.**
- Should a test be permitted to derive a fixture from live HEAD at all, or should it draw a
  fixed historical SHA? This trades a flaky coupling against a fixture that can rot.
- Are there other claim classes with a silently-unrepresentable value?

## Status

**Claimed by `[#763]`** — the batch-Z freeze expiry row. That row already rules that
*"membership is by test node id, never by count"*; this intake is the evidence for **why** that
clause is load-bearing rather than careful, and it constrains how `[#763]` may be discharged: a
set that can move by ±1 from the measurement SHA alone cannot be judged on its total.

DRAFT — CANDIDATE under the ADR-111 funnel. Not ratified: the path from finding to row is
CANDIDATE → intake → ratification, and ratification is the operator's act. Evidence and
reproduction are recorded in `logs/SUITE-BASELINE-FREEZE.md` (AMENDMENT 2026-09-15) and
JOURNAL 2026-09-15 (g).
