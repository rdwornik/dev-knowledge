---
intake-id: 65
status: ACCEPTED
origin: measured by the night orchestrator during the batch-E consumption sweep, 2026-09-01, as a controlled experiment inside one commit; filed as a SEED because it is a raw finding and ADR-111 gives a raw finding exactly one route
consumed-by:
decided-by: operator ruling 2026-09-01 (ruling 4 of seven on the night-window packet)
disposition: active
---

# A gate that measures a class of artifact it cannot discharge

<!-- class: tech (gate-predicate defect) · status: SEED — a pre-intake candidate, not yet worked
by a functional conversation. SEED BINDS NOTHING. -->
<!-- origin: batch-E consumption sweep, 2026-09-01 -->

> **SEED BINDS NOTHING.** This records a measured defect and proposes no fix. The fix touches a
> ratchet's measurement semantics, which forces a `DETECTOR_ID` bump plus a reviewed
> re-baseline — deliberately not a night act, and not a thing a raw finding may take on its own.

## Problem / motivation

`scripts/consumer_at_landing.py` has two legs: an artifact **declares** a consumer at landing,
and the set of artifacts **nothing cites** does not grow. The second leg resolves a citation
with

```
_STEM_RE = (?<![A-Za-z0-9._-])(\d{4}-\d{2}-\d{2}-[A-Za-z0-9._-]+)(?![A-Za-z0-9._-])
```

— **an identifier must START WITH A DATE.** Lane contracts and their siblings do not:
`LANE-a-1-vision-to-readme.md`, `PLAN.md`, `CUT.md`, `PROBE-batch-e-c-codespace-admission.md`,
`TIER-B-COPILOT-PAYLOADS.md`. So no governance surface can ever cite one in a way the module
recognises, and the artifact stays unconsumed permanently regardless of what anybody writes.

**Measured as a controlled experiment**, not inferred. One citation block, one commit, one file
(`tasks/614-vision-superseded-by-a-recreated-root-readme.md`):
`2026-08-31-census-single-file-folders.md` appears exactly once and **resolved**;
`LANE-a-1-vision-to-readme.md` appears exactly once, written the same way with the same full
path, and **did not**. Same surface, same syntax, opposite outcome; the only difference is the
date prefix. The sweep moved the unconsumed set 46 → 37 and could not move the remaining 37.

**The two halves were made to disagree by the module's own v2 bump.** `DETECTOR_ID v1 -> v2`
(2026-08-27) made the corpus RECURSIVE precisely so an artifact under
`docs/audits/<date>-...-launch-contracts/` could no longer *"sit outside BOTH legs"*. It now sits
inside the MEASUREMENT leg and outside the DISCHARGE leg — which is a strictly worse place than
where it started, because the debt is now counted and cannot be paid.

**A second, independent reason the same set can never clear.** `protocols/PLAYBOOK.md` Ch8 states
that a launch contract's consumer **is the batch close packet**. The close packet lands in
`docs/audits/`, and `docs/audits/` is deliberately EXCLUDED from the governance pool — the
diagnostic's own crux: *"a mention in a session log or a machine baseline is a record that the
file existed, not evidence that anything consumes it."* So the doctrine names a consumer the
mechanism structurally cannot accept. **Two causes, one symptom, and they want one ruling rather
than two patches.**

**If this stays unaddressed:** every batch that freezes lane contracts — the ratified way this
fleet dispatches work — permanently grows a number a gate reports as debt. The gate then trains
its readers to ignore it, which is the failure mode `[#595]` exists to end.

## Scenarios (+1 view)

- *As an integrator* closing a batch, I write the close packet that PLAYBOOK names as the
  contracts' consumer, and the unconsumed count does not move. Nothing I can write will move it.
- *As the operator* reading `audit.py health`, I see ~37 WARN lines naming files that are in fact
  fully accounted for, and learn to skim that block — the exact habit the check was built to
  prevent.
- *As the next batch's freeze seat*, I add 15 more contracts and the number rises again.

## Open questions — the ones that decide this

1. **Widen the identity, or narrow the corpus?** Admitting an artifact's own filename as an
   identifier regardless of date shape is the smaller change; excluding `*-launch-contracts/`
   from the corpus is the smaller *diff* but re-creates the v1 blind spot the v2 bump closed.
2. **Should `docs/audits/` stay out of the governance pool?** If the close packet is genuinely
   the consumer of record for a launch contract, either the pool admits a narrow slice of
   `docs/audits/` or PLAYBOOK Ch8 names a different consumer. Both are ruling-level.
3. **What does the re-baseline cost?** The module's own discipline: a corpus or predicate change
   forces a `DETECTOR_ID` bump plus *"a deliberate re-measure-and-re-stamp rather than silently
   rebasing hundreds of names"*. Whoever takes this owes that review, and it is the reason a
   night seat did not.

## What this SEED deliberately does NOT do

No code change, no `--write-baseline`, no `DETECTOR_ID` bump. Re-baselining 37 names unreviewed
is precisely the silent drain the discipline exists to prevent, and doing it to make a number
look better would be the same act with a worse motive.

---

## RULED 2026-09-01 — ACCEPTED, and the shape is narrower than the SEED proposed

> **Operator ruling 4.** *"`docs/audits/` stays OUT of the governance pool (batch machinery citing
> batch machinery is what the exclusion refuses). `consumer_at_landing` gains a declared
> PROVENANCE-CONSUMED class for audit-to-audit references, distinct from governance consumption —
> identity widened by class, pool unchanged. Accept #65 on that shape."*

**Both open questions this SEED raised are answered, and the second is answered NO.**

Q1 asked *widen the identity, or narrow the corpus*. **Widen the identity — by CLASS.** An
artifact's own filename becomes resolvable as a **PROVENANCE-CONSUMED** reference when the citing
surface is another audit, and that class is reported **separately** from governance consumption.
A launch contract read by its batch's close packet is genuinely consumed *as provenance*; it is
not consumed *as governance*, and one counter reporting both as the same thing is what made the
present number unreadable in either direction.

Q2 asked *should `docs/audits/` enter the governance pool*. **No.** The exclusion exists precisely
to refuse batch machinery citing batch machinery — admitting it would let a corpus discharge
itself, which is the failure the diagnostic's crux names. **The pool is unchanged.**

**What that leaves for PLAYBOOK Ch8.** Its sentence — a launch contract's consumer IS the batch
close packet — becomes true under the new class rather than false under the old one. No Ch8 edit
is required by this ruling; a note that the relationship is provenance-consumption, not governance
consumption, is the honest addition when the class ships.

**Still owed, and unchanged by the ruling:** the `DETECTOR_ID` bump and the deliberate
re-measure-and-re-stamp the module's own discipline requires. A class addition changes what the
ratchet measures, so it is the same reviewed act it always was.
