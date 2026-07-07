---
intake-id: 7
status: SEED
origin: "operator pre-handoff themes, 2026-07-08 (this session)"
consumed-by:
---

# AI-Council browser interface — launch a debate from one browser prompt

## Problem / motivation

Launching a Council debate today is **manual and undocumented**: the operator has no one-prompt
path from the browser to a running ai-council debate and back. ADR-67 / #70 specify a gated
question→verdict→ADR loop, but the *front door* — the operator proposes a topic, it fires into
ai-council, the debate self-starts and returns the synthesis — is not a captured requirement. The
itch: architectural decisions that genuinely warrant a debate get deferred or handled ad-hoc
because the friction of hand-wiring a Council run is too high, which is exactly the "run a debate
before writing a line" discipline the methodology asks for going unspent.

## Scenarios (+1 view)

- As the operator, in a browser chat, I state a debate topic and get back a **single paste/command**
  that fires it into ai-council.
- As the operator I paste/run that one thing and the debate **self-starts** (personas, rounds) with
  no further hand-wiring.
- As the operator, when the debate completes, the **synthesis** (verdict + rationale) returns to me —
  I don't go archaeology through the transcript body.
- As the operator I want the topic→debate→synthesis round-trip to feel like one move, so a genuine
  fork actually gets a Council debate instead of an ad-hoc call.

## Functional requirements

- **Must:** a single operator action in the browser turns a stated topic into a fired ai-council
  debate (one prompt/paste/command, not a multi-step hand-wire).
- **Must:** the debate **self-starts** from that action — no per-run manual persona/round setup.
- **Must:** the synthesis returns to the operator (verdict + one-line rationale surfaced), reusing the
  machine-readable VERDICT block (#96) so the operator reads the block, not the debate body.
- **Should:** the loop is **documented** in one place (it is undocumented today) so it is repeatable.
- **Could:** the returned synthesis is shaped to drop straight into an ADR (the ADR-67 return path).

## Acceptance criteria (ex-ante)

1. Given the operator states a debate topic in the browser, exactly **one** fire-artifact
   (one prompt/paste/command) is produced — verified by counting the operator actions between topic
   and running debate (must be one).
2. Executing that artifact starts an ai-council debate end-to-end with **no further manual setup** —
   verified by a run that reaches synthesis after the single fire.
3. The synthesis returns to the operator as a readable **verdict + rationale** (the VERDICT block),
   without the operator reading the debate body — verified against #96's producer-side block.
4. The full topic→debate→synthesis path is **documented** in one place a fresh session can follow —
   verified by that runbook/section existing.

## Non-goals

- Does **not** re-architect the debate engine (rounds, blind-vote isolation, prompt caching) — those
  are ai-council-owned (#110 / #128, ADR-41 routing).
- Does **not** auto-author or auto-ratify an ADR — the operator still ratifies (ADR-28 authority
  model); this is the interface, not the decision.
- Does **not** change *which* questions warrant a debate (the convene-vs-Path-A criterion is #18).

## Impact sketch (4+1 lite)

- **Logical:** a browser front-door onto the existing ADR-67 gated loop.
- **Process:** collapses topic→fire→synthesis into one operator move; the return path is #70's
  deterministic `council.return_dir`.
- **Development:** implementation lands in **ai-council via its dedicated chat** (ADR-41) — the hub
  captures the requirement only.
- **Physical:** crosses the browser ↔ ai-council boundary; touches the verdict return channel.

## Open questions

- What is the "one prompt/paste/command" mechanism — a hub-generated `/council-question` artifact (#70),
  a CC command, or a claude.ai-side action? (technical-architect + ai-council question — recorded.)
- Where does the debate physically run (local ai-council CLI vs a cloud/scheduled agent) and how does
  the synthesis get back to the browser surface?
- How much of the ADR-67 / #70 gated loop is already live vs unbuilt — verify before treating any leg
  as new (witnessed behaviour outranks the spec).
- Trust/data boundary: what leaves the machine when a topic is fired (mirrors intake doc #2's open
  question)?

## Status

SEED — captured 2026-07-08 from operator themes (this session). Relates to ADR-67, #70, #96, #18.
Awaiting functional-architect elaboration, then technical triage. Build lands in ai-council (ADR-41).
