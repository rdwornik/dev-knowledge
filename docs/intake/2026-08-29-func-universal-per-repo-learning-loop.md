---
intake-id: 63
status: DRAFT
origin: operator direction, stated verbatim mid-flight during the 2026-08-29 post-night reconcile-and-file pass; filed by the integrator under ADR-111's only path from a CANDIDATE, and explicitly evidence-gated on the AUT-R3 cloud lane
consumed-by:
---

# Universal per-repo learning loop — the hub deploys the mechanism, never the managed state

<!-- class: func (operator design input) · status: DRAFT — NOT ratified; DRAFT BINDS NOTHING.
Non-citable as doctrine until ratified; the repo wins on any conflict. -->
<!-- origin: operator direction, 2026-08-29 -->

> **DRAFT BINDS NOTHING.** This file records operator direction and the question it raises. It
> authorises no build, no dependency, and no change to any consumer repo. Nothing below is doctrine
> until this intake is ratified — and its ratification is **gated on measurement**, see §3.

## 1. The direction, in the operator's terms

> **"UNIVERSAL PER-REPO LEARNING LOOP — every consumer repo ships with an isolated self-learning
> layer (event loop → local index/memory → boot surface), hub deploys the MECHANISM never the
> managed state."**

Three properties are load-bearing in that sentence and each is a separate decision:

1. **Isolated per repo.** The learning layer's state belongs to the repo that produced it. No
   cross-repo state pool, and no consumer reading another consumer's index.
2. **Event loop → local index/memory → boot surface.** A closed loop: the repo's own events feed an
   index, and the index surfaces at boot where it can change what the next session does. A loop that
   does not reach the boot surface is a log, not a learning layer.
3. **The hub deploys the MECHANISM, never the managed state.** This is the ADR-28 Layer-2 invariant
   restated for a new organ class: the hub ships the carrier, and the state stays the consumer's.
   A hub that shipped the index would be driving state in a child repo.

## 2. Why this is not already covered

Reconciled before filing (2026-08-29): a search of `docs/intake/` for learning loops, per-repo
memory, local indexes and embeddings returned **no existing object**. The adjacent live objects are
related but distinct, and none of them owns this:

- the telemetry → trends → rulings loop is a **hub-local** feedback path, not a per-consumer one
- `LESSONS.md` is append-only prose, read by humans and agents, with **no index and no ranking**
- the funnel gates enforce lifecycle; they do not learn
- the C3 typed multi-layer graph (filed this same day) is the **substrate this would learn over**,
  not the learning layer itself

## 3. THE GATE — this intake does not ratify on argument

Ratification is **evidence-gated on the `AUT-R3` cloud lane** (dispatched 2026-08-29, read-only,
session `cse_01FteQFHM1VuYdQLypkwogGq`), whose deliverable is a survey of repo-as-reinforcement-
environment practice plus a **blind-spot list scored against our live organs** and a library-first
BUY-vs-BUILD sweep. Three of that lane's outputs bear directly here:

- axis **(b)** — what small local models are *actually* good at (retrieval, ranking, "where is
  what") versus not (decision-making, generation quality). If the evidence says the useful band is
  narrow, this intake narrows with it rather than being argued wider.
- axis **(d)** — the ABSENT column. If a property this intake assumes is already PRESENT, the scope
  shrinks; the blind-spot list is the scoping instrument.
- the **library-first sweep** — `sqlite-vec` is the natural first probe because this repo already
  runs sqlite by ruling R-A. ADR-112 Tier-L applies: evaluate before adopting, and the Windows-wheel
  + pinned-`uv` installability constraint (the `rustworkx` precedent) is first-class, not a footnote.

**A negative result from AUT-R3 is a valid outcome for this intake** and would properly close it
REJECTED with the reason recorded, which is the standing precedent for declined work here.

## 4. Open questions this intake does NOT answer

- What the index actually indexes, and whether "importance" is learned or declared.
- Whether the boot surface is a new organ or an extension of an existing generated surface — a new
  boot-time read has a byte cost paid every session, and the paste/boot-bytes panel is currently the
  only WORSENING trends panel (+11,232 B), so any addition argues against a measured headwind.
- Whether a per-repo model is a model at all, or an index plus ranking with no learned parameters.
  The operator's phrase is "small local models"; the evidence may say "index".
- The carrier shape: which deploy manifest component ships it, and what a consumer that declines it
  looks like.

## 5. Provenance and related objects

- North Star: the operator's MSc thesis, per the ruled THESIS-COMPARE input
  (`docs/audits/2026-08-29-technical-thesis-compare-out.md`)
- Substrate it would learn over: the C3 typed multi-layer graph
- Sibling governance question: intake #62 (L0 as a governed layer) — that one asks *who governs the
  global layer*; this one asks *what each repo learns for itself*. They meet at the boot surface.
- Layer invariant: ADR-28 (Layer 2 never executes), which property 3 above restates rather than
  amends.
