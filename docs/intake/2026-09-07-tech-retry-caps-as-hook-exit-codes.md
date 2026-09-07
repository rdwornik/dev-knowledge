---
intake-id: 82
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-E; catalogue row A-13 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:267`, recorded there as a **shared weakness**, and row 20 of `docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md:140`
consumed-by:
---

# Retry caps and decision budgets are stated in prose the session itself owns

## Problem / motivation

A-13 is the row where the comparison stops flattering us. Their phase gates are prose telling the
model to call `AskUserQuestion`, with nothing verifying it — and their `reverify_count` is capped
at 3 **in a YAML field the model owns**. The catalogue records the inverse for our gates: ours are
mechanisms, two of them failing closed. But it refuses the easy win on the retry half and writes
it down as a **shared weakness**: *"Retry caps: ours are likewise stated, not enforced."* The
gap-analysis row is blunter — *"our decision budgets and step counts are likewise stated, not
enforced… recorded so we do not import it as a strength."*

Concretely: a lane contract states a decision budget (V-2) and a step count. A lane can exceed
either without anything noticing, because the only party measuring is the party spending. A
session that has retried a phase five times against a stated cap of three produces a diff that
looks exactly like a session that retried once. Tonight's lost turns are partly this: nothing
converted "you have retried enough" into a refusal, so retrying stayed a judgment call at the
moment judgment was most degraded.

This is the smallest of the eight rows precisely because the mechanism class already exists here.
We have a hook roster where a FAIL blocks and two hooks fail closed. Making a cap enforceable is
not a new organ — it is putting an existing number behind an existing kind of gate.

## Scenarios (+1 view)

- As a lane at retry N+1 against a cap of N, my next attempt is REFUSED by the gate with the cap
  and the observed count in the message, and the lane escalates instead of grinding.
- As `lane-boot`, I refuse to boot a lane whose recorded attempt count already exceeds its
  contract's cap — a dead lane's fourth replacement does not silently become the fifth attempt at
  the same phase.
- As the operator, "this lane retried too many times" is something the tree tells me, not
  something I reconstruct from a transcript.
- As a lane with a legitimately raised cap, my contract states the higher number and the gate
  reads it — the cap is a contract value, not a constant baked into the hook.
- As a docs-only or trivially short lane, I never approach a cap and never see the gate, which
  costs nothing.

## Functional requirements

- **Must:** the retry/reverify count is written to a durable surface the session does not solely
  own — the natural home is intake C-C's `LANE-STATE.yml`, which already needs `failed` phases.
- **Must:** the cap is read from the lane's frozen contract, not hard-coded. A contract that
  states no cap gets a declared default, and the default is stated in one place.
- **Must:** exceeding the cap is a **non-zero exit**, not a warning — `lane-boot` refuses beyond N,
  in the same posture as the hooks that already fail closed.
- **Must:** the refusal names the cap, the observed count, and where each was read from, so a
  session cannot be refused by a number it cannot see.
- **Should:** the same treatment reaches the decision budget (V-2) and step count, which the
  gap-analysis names in the same breath — one mechanism, three consumers, rather than three
  bespoke checks.
- **Could:** the count is emitted as telemetry alongside the existing gate events, so "how often do
  lanes approach their caps" becomes answerable before anyone tunes N.

## Acceptance criteria (ex-ante)

- **AC-1:** With a contract cap of N and a recorded count of N, `lane-boot` exits non-zero and the
  message quotes both numbers and their sources.
- **AC-2:** With a recorded count of N-1, the same invocation exits 0 — the pair proves the
  boundary, not just the refusal.
- **AC-3:** A contract stating no cap uses the declared default, and the test asserts the default's
  value by reading it from its single definition site rather than restating it.
- **AC-4:** The count survives a session death: killing a lane and booting a replacement in the
  same worktree preserves the observed count.
- **AC-5:** The honest limit is recorded at the gate: this enforces a cap on *recorded* attempts.
  A session that does not record an attempt is not caught, and the hook comment says so rather
  than implying the cap is airtight.

## Non-goals

- **Not** an attempt to detect retries a session declines to record. That is the residual, and it
  is stated rather than papered over.
- **Not** a change to what a retry *is* — the phase vocabulary comes from C-C, and this intake
  consumes it rather than defining it.
- **Not** an autonomous escalation. Refusing to proceed is the mechanism; deciding what happens
  next stays with the dispatcher and the operator.
- **Not** an import of the comparator's `reverify_count` schema. The catalogue's whole point is
  that their field is model-owned; copying the field without moving the ownership would import the
  weakness.

## Impact sketch (4+1 lite)

- **Logical:** a stated cap becomes an enforced one; the "shared weakness" row loses its share.
- **Process:** a lane that is grinding stops on a refusal instead of on someone noticing.
- **Development:** `lane-boot`, the contract parser that already reads tier and dispatch fields,
  and whatever module owns the lane state file.
- **Physical:** none beyond the state file C-C already introduces.

## Open questions

- Does this land before or after C-C? The count needs a durable home; if C-C is deferred, this
  intake needs its own minimal one, which is a worse shape. Sequencing is a technical-architect
  call.
- What is N? The comparator's 3 is theirs, not ours, and we have no measurement of our own retry
  distribution. Picking N before measuring would be the same mistake as importing their field.
- Do decision budget and step count share the cap mechanism, or are they different enough that one
  gate serving three consumers becomes the wrong abstraction?
- `lane-boot` is a command, not a git hook — is a command's non-zero exit the right enforcement
  surface here, or does the cap also need a commit-stage twin the way other prevent-rules do?

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
