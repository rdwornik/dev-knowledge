# ADR-108: Decision-routing doctrine + standing engineering standards (ratifies intake #22 §A + §B)

**Status:** Accepted (ratified 2026-07-31 — operator word, relayed via the outgoing browser seat)
**Date:** 2026-07-31
**Decision tier:** Methodology (doctrine — routing of decision authority + standing build expectations)
**Decided-by:** operator (ratification 2026-07-31, via outgoing seat relay)
**Related:** [#446] (the window whose close this ratification was sequenced after) · [#382] → [#383] → [#385] (the fleet-management chain §E states functionally — **not** ratified here) · ADR-98 (intake pipeline — the genre this promotes from) · ADR-105 (named-consumer discipline) · ADR-107 (the pilot-precedes-contract precedent)
**Intake:** #22 (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md`) — **§A and §B only**
**Amends:** none.
**Decommission:** none. Nothing is removed by this decision.
**Source:** Operator design input dictated 2026-07-30/31 in the outgoing browser-seat window, ingested verbatim as intake #22 (SEED). The intake's own §I.3 sequences this ratification: *"First ruling batch after [#446]: ratify §A (decision routing) + §B (standing standards) — these are XS prose rulings."*

## Context

Intake #22 was ingested SEED at the [#446] window close. Its §I.3 names §A + §B as the first
ruling batch after [#446] lands. [#446] landed and the window sealed, so the precondition is met.

**Ratification is by PROMOTION, not by status flip.** The intake `status:` field is
**doc-level** — one token for the whole document — so it cannot express "§A and §B are ruled,
§C–§H are not." Flipping it to `ratified` would over-claim six unratified sections. The ruled
content is therefore transcribed into this ADR, which becomes its citable home, and the intake
doc stays `status: SEED`. The mechanism gap this exposes is filed, not resolved here.

## Decision

### §A — Decision-routing doctrine (standing rule)

Transcribed verbatim from intake #22 §A, items 1–4:

1. **The operator rules FUNCTIONAL questions only** — what the system should do, how output
   should look, priorities between outcomes. Plain-language briefs, no technical vocabulary.
2. **The architect rules TECHNICAL questions in its own lane** — makes the call, records it
   (git + changelog + record), and relies on revertability instead of escalation. Uncertainty
   is not a reason to ask the operator; it is a reason to decide, record, and mark revertable.
   Continuous improvement: decide → test → revert-if-wrong is the sanctioned loop.
3. **AI Council is the distillation organ for genuinely contested technical decisions** — not
   the operator. Endstate the operator wants: finish/deploy ai-council once the methodology
   lands, and keep it as the standing organ for "we have a technical question" moments.
4. Anti-pattern to retire: presenting the operator with option menus of technical forks
   (R1/R2-style). If a brief cannot be written functionally, it is not the operator's decision.

### §B — Engineering standards (standing, every build arc)

Transcribed verbatim from intake #22 §B:

- **Clean architecture** — layer model as specification (declared edges, mechanized check;
  the ai-council layer-edge review is the precedent), file-size equilibrium as a design value.
- **TDD** — RED-first witnesses and failing tests before build code, frozen after freeze.
- **Spec-driven development** — rule-first, spec before build, acceptance contract ex-ante.
- These are expectations the harness enforces, not per-arc negotiations. Target operating
  model: operator states requirements; the harness (methodology + agents) implements —
  Cursor-like, "the operator should not have to think about the how".

## Scope boundary — what this ADR does NOT ratify

**Intake #22 remains `status: SEED`; §C–§H are NOT ratified by this ADR.** Specifically
unratified and still SEED-class (non-citable as ruled doctrine):

- **§C** model-fleet timeline (grok R-S shadow review, Gemini R-G large-context lane)
- **§D** context-distiller pre-phase (repomix `--compress`, pyadr, copier/cruft)
- **§E** fleet-management requirement (the functional statement of the #382→#383→#385 chain)
- **§F** backlog equilibrium / the 08-26 cluster's rank
- **§G** handoff v6 scope note (informational by the intake's own declaration)
- **§H** portability probe (provider-independence, witnessed not declared)

§E in particular asks to "ratify this paragraph as the chain's functional requirement" — that
ask is **live and unanswered**; this ADR does not grant it.

## Consequences

**§A is doctrine, not mechanism.** It routes authority; it arms no gate. Nothing in this repo
mechanically detects an option-menu brief or an escalated technical question. Enforcement is
by the architect seat honoring the routing, and by review catching violations after the fact.
That limit is stated rather than papered over — a green gate set does not mean §A was followed.

**§B's clean-architecture leg names a precedent with no hub organ.** The layer model is
declared as specification with a "mechanized check", and the ai-council layer-edge review is
named as the precedent — but no Layer-2 enforcement organ exists in this repo today. The
standard is ratified as a standing expectation; the missing organ is the gap, filed separately.

**§B's TDD and spec-driven legs are already exercised, not new.** The [#446] window ran a
RED-first frozen contract (`tests/test_v6_frozen_contract.py`, 9 tests RED at freeze) and a
spec-before-build sequence. This ADR records the practice as standing expectation rather than
introducing it.

**The per-section ratification gap is real and recurs.** Any future intake that is partially
ruled hits the same doc-level-status limitation and needs the same promotion workaround.
Filed as a candidate row rather than fixed here.

---

## AMENDMENT — 2026-08-19 · §B gains the fleet Python paradigm + naming stance (discharges `[#407]`)

> **In-file amendment marker.** ADR bodies are immutable (`CLAUDE.md` §5 rule 3); nothing above is
> edited and no clause above changes meaning. This section ADDS a standing standard to §B, which is
> where `[#407]` was re-routed when it was filed — the row's own Done-when names *"an architect
> ruling (ADR-108 §A; re-routed)"* as its home. Landed by the S-1 night-adjudication seat under
> `docs/audits/2026-08-19-technical-s1-seat-arc-contract.md` act 7.

**Decided-by:** architect ruling **2026-08-19**, item `#407` of the eight-ruling L-5 block:
*"fleet Python doctrine = functional-first + dataclasses; classes only for stateful lifecycles;
naming = PEP 8. File as an ADR-108 amendment (its re-routed home), then CLOSE."*

### §B-4 — Python paradigm and naming (fleet-wide, standing)

- **Functional-first, with dataclasses for structured data.** The default unit of code is a
  function over explicit inputs; the default unit of *data* is a `dataclass`, not an ad-hoc dict
  and not a class that exists only to hold fields.
- **Classes only for stateful lifecycles.** A class earns its existence when an object owns state
  across calls and has a lifecycle to manage. A class used as a namespace for functions, or as a
  container for values a `dataclass` would carry, is the shape this stance rules out.
- **Naming is PEP 8**, without a fleet-local dialect: `snake_case` for modules, files, functions
  and variables; `CapWords` for classes; `UPPER_SNAKE` for module constants. The point of naming
  the standard rather than inventing one is that PEP 8 is already what every tool in the stack
  assumes, so the fleet inherits its tooling instead of teaching it.

### What this settles, and what it does not

- **Settles `[#407]`.** Its Done-when asked that a ruling record the functional-vs-OOP stance
  **and** that a uniform naming convention be documented as fleet doctrine. Both are above; the
  row closes on this amendment. The 2026-07-19 ruff/pytest parity arc covered TOOLING only — this
  is the paradigm-and-naming half it left unfiled, which is exactly how `[#407]` described itself.
- **Arms no gate.** `ruff` is configured for lint, not for paradigm; nothing mechanically refuses a
  class that should have been a function. This is a standing expectation of the kind §B already
  carries, and it is stated as such rather than implied to be enforced.
- **Prospective, not a refactor mandate.** No existing module is out of compliance by this
  amendment, and nothing here schedules a conversion pass. It binds what gets written next.
