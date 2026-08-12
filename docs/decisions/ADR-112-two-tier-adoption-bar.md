# ADR-112: Two-tier adoption bar — Tier L evaluates, Tier S tries and keeps or deletes

- **Status:** Proposed
- **Date:** 2026-08-12
- **Decision tier:** Architecture (Path A — architect promotion at the 2026-08-12 adjudication hour; **ratification is a separate operator act and has not happened**)
- **Related:** ADR-108 (§B standing engineering standards), ADR-110 (batch protocol — the process-lane cap this bar keeps out of the eval queue), ADR-81 (organ definition-of-done — what a Tier S item is exempted from, and what it is not), ADR-98 (intake → ADR traceability)
- **Intake:** #28 (§A) — `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md`
- **Decommission:** none
- **Source:** Night-2 promotion assessment `N2-D1-01`, ruled PROMOTE at the 2026-08-12 adjudication hour (operator `OK` en bloc against `PICKER-2026-08-12-annotated.md`; register `protocols/STANDING_RULINGS.md` L-10 / M-5). The fork-test argument is transcribed below rather than re-derived.

## Status note — read this before citing the ADR

This ADR is **Proposed**, not Accepted. It was authored because the promotion was ruled;
**ratification is a later operator act.** Until the status line reads Accepted, this document
records a decision that was ruled worth writing down as an ADR — it does not yet bind. Per ADR-94
the status line is editable in place on ratification, so accepting it is a one-line edit here and
one line in `docs/decisions/README.md`; nothing else moves.

## Context

The fleet spent this window building a corpus whose purpose is to stop unmeasured dependencies from
entering it. The single adoption bar that corpus implies — measured-divergence evaluation, ADOPT or
REJECT on numbers, consuming a gap-week slot (`STANDING_RULINGS` E1) — is proportionate to a
library that ships into `scripts/` and disproportionate to a skill that adds a prompt template.

The cost of the mismatch is not theoretical. Intake #28 §C classified fourteen concrete candidates;
most of them are skills, plugins and commands with no code impact whatsoever. Under one bar each
one either consumes an evaluation slot the fleet has few of, or — the realistic outcome — never
gets tried at all, which is adoption paralysis wearing the costume of rigour.

The opposing position is real, and it is the reason this is an ADR rather than a row. A single bar
is defensible precisely because **Tier S's try-then-keep path is how an unmeasured dependency walks
into a fleet.** A reasonable person can hold that the fleet should not have built an anti-drift
corpus and then opened a side door. That is leg 1 of the fork test, and it passes.

Leg 2 passes for a different reason: **reversal is asymmetric and expensive.** Retiring this bar
later means re-evaluating an *installed* surface — every Tier S item already kept, already woven
into sessions — rather than declining an uninstalled one. Both legs, so an ADR.

## Decision

**Adoption runs at two tiers, and the tier is determined by code impact rather than by the
artifact's format.**

### Tier L — libraries and code

Unchanged from current practice: measured-divergence evaluation, ADOPT or REJECT **on numbers**,
consuming a gap-week slot per `STANDING_RULINGS` E1 ("gap-weeks consume P-B evals").

### Tier S — skills, plugins, commands

Install → **30-minute sandbox try** → **KEEP or DELETE** → **one ledger line either way**. No
evaluation ceremony. **No births** — a Tier S trial does not open a BACKLOG row, which is the
property that keeps it out of the open-set arithmetic §B clause 3 is trying to reduce.

The ledger line is the whole of the record, and it is written in both directions: a DELETE is as
much a result as a KEEP, and recording it is what stops the same candidate being re-tried every
quarter by a seat that does not know it was already tried.

### The guard sentence

> **Tier S never touches gates, hooks that block, or `scripts/` — anything that would, is Tier L
> by definition.**

This is the load-bearing clause and it is quoted verbatim from intake #28 §A. It is stated as a
*definition* rather than a restriction, which matters: an artifact is not "a Tier S item that
happens to touch a gate." If it touches a gate, a blocking hook, or `scripts/`, it was Tier L from
the start and the 30-minute path was never available to it.

### The graduation trigger

**A kept Tier S item that later steers code-impact behavior graduates to Tier L review.** Tier
membership is therefore a property of what the item currently does, re-evaluated when its behavior
changes — not a label assigned once at install time and inherited forever.

## Sequencing

This bar is **the entry gate that BRIEF §3 items 3 and 4 both route through**, so it is cheapest
ratified *before* them. Running those items first means classifying their candidates under a bar
that is still Proposed, and then either re-classifying or grandfathering — the shape this ADR
exists to prevent.

## Consequences

**Easier.** Skills and commands can be tried at their real cost, which is minutes. The
fourteen candidates in intake #28 §C become actionable without fourteen evaluation slots. The open
set stops absorbing trial rows, because Tier S births none. Genuine code dependencies keep the full
measured bar with a smaller queue in front of them.

**Harder, and named rather than minimized.** Two bars mean a classification decision at every
adoption, and a misclassification routes a code-impacting dependency down the 30-minute path — the
exact failure the single bar prevents by construction. The guard sentence is the mitigation and it
is only as good as its application; it is deliberately phrased as a definition so that a
misclassification is a *factual* error about what the artifact touches, which is checkable, rather
than a judgment call, which is not.

**Also harder:** "steers code-impact behavior" in the graduation trigger is a judgment, and this
ADR does not mechanize it. That is stated as an honest limit rather than left for a reader to
discover.

## Honest limits

- **No mechanism is proposed here.** No gate reads the tier, no check enforces the guard sentence,
  and the ledger is a written line rather than a validated surface. This ADR records a decision
  about process; mechanizing it would be separate work with its own fork test.
- **The 30 minutes is a budget, not a measurement.** It comes from intake #28 §A as authored and
  has not been calibrated against a real trial.
- **The ledger has no declared home in this ADR.** Intake #28 §C routes its verdicts into ledger
  #27 as a cross-referenced amendment; a standing home for Tier S ledger lines is left to the
  ratifying act rather than invented here.

## Alternatives considered

**Keep the single bar.** The position with a real argument, recorded above as leg 1 of the fork
test. Rejected because the bar's cost is paid per-candidate while its benefit accrues only to
code-impacting candidates, so a fleet applying it uniformly buys rigour it does not need at a price
it demonstrably will not pay — the observed outcome being that the low-impact candidates simply do
not get tried.

**Three or more tiers.** Not argued by any source and not adopted. Two tiers with a definitional
guard is the smallest split that separates the code-impact case, and adding a middle tier would
reintroduce the classification ambiguity the guard sentence exists to remove.

**A row instead of an ADR.** Rejected by the fork test: leg 2 turns on reversal cost against an
installed surface, which is precisely the asymmetry an ADR exists to record.
