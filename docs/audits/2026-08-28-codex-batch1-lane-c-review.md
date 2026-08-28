# Terra pre-merge review — batch-1 lane L3 (`lane-c-491-fanout-acceptance`)

- **Reviewer:** `gpt-5.6-terra` via `codex exec` (codex-cli 0.145.0)
- **Lane:** L3 — SDA-1 fan-out acceptance + provider preflights
- **Date:** 2026-08-28
- **Consumer:** `[#491]` (Gemini scanning lane — ruling R-G plus an acceptance contract) and
  `[#492]` (Grok review-lane acceptance), the fan-out acceptance rows this lane's preflights
  serve; plus the batch-1 manifest `docs/audits/2026-08-28-technical-batch-1-manifest.md`,
  which names this lane and is closed by the end-of-batch packet.

## TALLY (as returned by the reviewer)

```
TALLY: critical=0 high=1 medium=0 low=0
```

## The question this review was pointed at

The lane **stopped instead of producing its headline deliverable**, so the review was asked the
only question that matters about such a lane: is the stop justified by the contract it quotes,
or is it *a lane dressing up an incomplete job* — and, above all, **does the artifact anywhere
fabricate a measurement, a provider result, or an artifact it did not have?** That is the exact
failure mode L3's own subject matter is about, which is why it was put to the reviewer directly.

## The reviewer's honesty audit

> *"The SDA-1 stop is justified: the contract requires verbatim persistence as the first act and
> makes it the lane's accepted frame; inventing or reconstructing an absent artifact would be
> fabrication. The provider stop is also justified: the quoted Q0–Q7 rule explicitly prevents
> starting the run when preconditions fail… It labels rate shape unknown rather than converting
> OAuth into proof, and it does not invent a served model ID or run an unattributable C-10
> measurement. **Nothing in the artifact itself establishes fabrication.**"*

## Finding, with the lane's disposition

### HIGH-1 — the artifact used an architect-reserved verdict word

> *"It emits the architect-reserved verdict word 'INDETERMINATE' despite claiming no verdict
> word is emitted. An integrator can treat the lane's C-9 conclusion as the architect's ruling,
> bypassing the required architect decision boundary."*

**Disposition: VALID. FIXED.**

The contract is explicit — *"No verdicts are emitted by the lane… ADMIT/REFUSE/INDETERMINATE is
the architect's ruling on the evidence"* — and the artifact used the word while asserting it did
not. The intent was to name C-9's mechanism, but intent is not the test: the failure scenario is
real, and a lane that quietly imports the architect's vocabulary is doing the thing the clause
forbids regardless of what it meant.

The artifact now names **C-9's ceiling** without using any of the three words, and the
no-verdict clause states plainly that naming a mechanism is not applying a ruling. **Verified
mechanically:** `grep -c "INDETERMINATE\|ADMIT\|REFUSE"` over the artifact returns **0**. The
correction is recorded in the artifact rather than silently reworded.

## Also raised, and acted on

Terra noted the observations *"lack raw receipts"* while correctly declining to treat that as
evidence of invention. Fair, and cheap to fix: the artifact now embeds the verbatim probe output
— the full `agy` JSON envelope (which is the evidence for the served-id finding, since there is
no model field to omit), the `head -3` of the corrupt `glm` binary showing `<!DOCTYPE html>`,
its `rc=0`, and the empty `which` results.

## Verdict

**MERGE-ELIGIBLE.** No critical findings. The single HIGH is fixed and mechanically verified.
The lane's stop is confirmed by the reviewer as contract-conformant rather than a dressed-up
shortfall, and no fabrication was found — which, for this lane in particular, is the finding
that matters.
