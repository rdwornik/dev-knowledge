---
intake-id: 47
status: READY
origin: integrator, 2026-08-24 batch close; P8 probe row read against gen_handoff.py / assemble_paste.py
---

# The `SUPPLEMENT` probe passes while the consequence it states is false

## Problem / motivation

Probe **P8** (`templates/handoff/v5/PROBES.md.tmpl:99`) asks, among other things, whether
`SUPPLEMENT.md` is present and **"is its ANSWERS region empty or filled"**, answered by:

```
grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/<slug>/SUPPLEMENT.md
```

That reads fill-state **at check time**. But the thing fill-state is *for* happens at **cut
time**: the SUPPLEMENT's ANSWERS **fold into `PASTE_THIS.md`**, and three framing blocks
(`SUPPLEMENT_BANNER`, `P1_GATE_NOTE`, `PASTE_STEP6`) are rendered in their COLD or FILLED
variant by the generator (`scripts/gen_handoff.py:589` `_reflow…`, `scripts/assemble_paste.py:105`
and `:131`).

**The two moments can disagree, and P8 cannot see the disagreement.** If a bundle is generated
cold and the operator fills the SUPPLEMENT afterwards, P8 answers **"filled"** — truthfully about
the file — while `PASTE_THIS.md` still carries cold framing and no folded ANSWERS, unless the
reflow was separately run. The probe therefore **passes while its stated consequence is false**:
the boot reads "filled", and the artifact the incoming seat actually pastes says otherwise.

A reflow exists precisely because this drift is known — `assemble_paste.py:131` comments that it
flips cold framing to FILLED "when the SUPPLEMENT was FILLED after a cold generation". That
confirms the failure mode is real and handled *by a separate act*. Nothing in P8 asserts that
act ran. This is the same class as the recorded lesson that the supplement-fold reflow covers
generator sites only and needs a sweep after any fold.

**Verification limits, stated so this is not read as more than it is.** What is verified: P8's
question text and command; the existence and location of the reflow; that the fold is a
cut-time act. What is **not** verified here: how many committed bundles are currently in the
disagreeing state. That census is the first thing the fork should produce, and this intake
deliberately does not guess it.

## Scenarios (+1 view)

- A bundle is cut cold. The operator fills SUPPLEMENT and does not re-run the assembly. P8
  reports "filled"; the incoming architect pastes a `PASTE_THIS.md` with no answers in it and a
  banner saying the supplement is empty.
- A verifier runs `/handoff-verify`, gets a clean P8, and records the bundle as gated. The
  bundle is immutable, so the false record is permanent.
- Someone reads P8's row as "the ANSWERS are in the paste" — which is what it implies — and
  never opens `PASTE_THIS.md`.

## Functional requirements

- **Must:** P8 (or a sibling) asserts the fill-state of the SUPPLEMENT **and** the fold-state of
  the artifacts derived from it, and refuses when they disagree.
- **Must:** the check names the discrepancy explicitly, rather than reporting the file's state
  alone.
- **Should:** the generator makes the disagreement unrepresentable — filling a SUPPLEMENT in a
  committed bundle either reflows or is refused.
- **Could:** a census of existing committed bundles in the disagreeing state.

## Acceptance criteria (ex-ante)

1. A fixture bundle — cut cold, SUPPLEMENT filled afterwards, reflow **not** run — is REFUSED by
   the probe gate. This is the test that would have caught it, and it must fail before the fix.
2. The same bundle with the reflow run passes.
3. A committed bundle's recorded P8 evidence can no longer say "filled" while its `PASTE_THIS.md`
   carries cold framing.

## Non-goals

- Redesigning the SUPPLEMENT fold or the v6 boot.
- Retro-fixing already-committed bundles: handoffs are immutable, so any correction is a new
  record, not an edit.

## Impact sketch (4+1 lite)

- **Logical:** a probe that measures a proxy at the wrong moment is worse than an absent probe,
  because it manufactures evidence of a property nobody checked.
- **Process:** `/handoff-verify` gains a real refusal where it currently has a true-but-
  misleading answer.
- **Development:** `scripts/verify_handoff_probes.py` / `gen_handoff.py`; the fixture is the
  load-bearing part.
- **Physical:** `templates/handoff/v5/PROBES.md.tmpl` (the row), plus the verifier.

## Open questions

- **Fork: strengthen the probe (assert fold-state agreement at check time), or remove the
  disagreement at the source (generation refuses a bundle whose SUPPLEMENT and folded artifacts
  disagree).** The second is stronger but touches the cut path, which is `WINDOW = BATCH`
  constrained; the first is additive and testable today.
- Is "filled after a cold cut" a legitimate operator workflow that must keep working, or an
  accident the generator should refuse outright? The reflow's existence implies the former, but
  it has not been ruled.
- How many committed bundles are currently in the disagreeing state — and does that number
  change which fork is affordable?

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.
