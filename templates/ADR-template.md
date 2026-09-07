# ADR-NN: Title

- **Status:** Proposed | Accepted | Superseded
- **Date:** YYYY-MM-DD
- **Decision tier:** <the route this decision took — e.g. "Architecture (Path A — direct architect/operator ruling)", "Council-ratified", or "Path A — operator ruling, session YYYY-MM-DD"; names how it was decided, not the topic>
- **Amends:** <ADR-NN if this amends an earlier decision; omit if not applicable>
- **Supersedes:** <ADR-NN if this replaces an earlier decision; omit if not applicable>
- **Related:** <ADR-NN or other refs for context; omit if none>
- **Intake:** <intake-id(s) this ADR was born from — e.g. "#3"; omit if not intake-born. RULE: an ADR born from an intake doc MUST cite its intake-id — the docs/intake/ ↔ ADR traceability edge (ADR-98).>
- **Decommission:** <files, folders, or sections made obsolete by this decision and therefore to be removed; write "none" if nothing>
- **Source:** <provenance line — AI Council debate / session debate / operator ruling, with date + ref (branch, transcript, session, or brief)>

<!-- Decommission: if non-empty, each listed item becomes a BACKLOG entry and stays open until removed. A decision is not complete while its Decommission items remain. -->

## Context

<What is the situation that motivated this decision? What forces are at play?>

## Decision

<What was decided? Use bullet points for multi-part decisions. Be specific.>

## Consequences

<What becomes easier or harder as a result? Positive and negative trade-offs.>

## Flip-condition

<!-- REQUIRED SECTION — every ADR names its flip. scripts/validate_adr_status.py FAILS an ADR
     numbered above FLIP_GRANDFATHER_MAX_ADR that carries no `## Flip-condition` section, and
     fails one whose body is still the `<...>` placeholder below — a copied-but-unanswered
     section names no flip. ADRs at or below the mark predate the requirement and WARN with a
     per-file disposition path instead. This instruction is an HTML comment on purpose: the
     validator lexes comments out, so leaving it in place cannot itself satisfy the rule. -->

<What would make us reverse this decision? Name the observable — a measurement that comes back
the other way, a dependency that lands or dies, a cost that crosses a threshold, a load-bearing
assumption that is falsified. Where nothing would flip it, write "none — <why>", so the section
reads as an answer rather than as an omission. A decision nobody can imagine reversing is a
claim about the world, and that claim is what belongs here.>

## Alternatives considered

<!-- REQUIRED SECTION (operator, DECLARE-F-2-2026-09-07 §A, thesis T-04 — "the architect must
     ALWAYS justify"). Same enforcement shape as Flip-condition above: FAIL above
     FLIP_GRANDFATHER_MAX_ADR, WARN with a disposition path at or below it. The word "Always"
     was already in this prompt and bought nothing, because nothing checked it; what changed
     is that something now does. `Rejected alternatives` / `Alternatives rejected` are accepted
     spellings — the corpus writes all three and they are the same section. -->

<Always filled. What else was evaluated, and why was it not chosen? Where nothing else was evaluated, record that — "none considered", plus the reason — so the section reads as an answer rather than as an omission.>
