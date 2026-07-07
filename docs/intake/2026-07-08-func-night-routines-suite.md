---
intake-id: 8
status: SEED
origin: "operator pre-handoff themes, 2026-07-08 (this session)"
consumed-by:
---

# Night-routines suite — the Tier-2 unattended layer as proposal classes (never new autonomy)

## Problem / motivation

The revived Tier-2 night layer is filed as a single "nightly proposal loop" (#270 load-gauge first,
then #271 the loop), but the operator's actual intent is a **suite of distinct proposal classes**,
all bounded by intake brief #1 §6's frozen constraints (night executes pre-authorized deterministic
contracts; it **proposes** everything else; it **never gains new autonomy** — judgment sleeps with
the architect). Capturing them as one loop hides the per-class rent question. Separately, the
**subagent-army pattern** (Sonnet/Haiku swarms for micro-specific tasks) is currently underused and
has no home in the night suite's design. The itch: without enumerating the proposal classes and
their consumers ex-ante, the night layer either under-delivers or drifts back into the "routine with
no consumer" rot the fleet-audit lesson exists to prevent.

## Scenarios (+1 view)

- As the operator I read a morning digest of **night proposals grouped by class**: code-refactoring
  proposals (flagged, never applied), code-review findings, process-review findings,
  creative-brainstorm ideas (→ intake SEED docs), backlog-groom proposals.
- As the operator each class arrives as a **proposal I triage** — nothing was mutated overnight
  (BACKLOG untouched, no semantic refactor applied); the judgment slept with me.
- As the operator I dispatch a **Sonnet/Haiku subagent swarm** at a micro-specific, well-bounded,
  mechanically-verifiable task and get back structured results — using the pattern that is currently
  underused.
- As the operator each proposal class **states its consumer + survival metric before it runs**, so a
  class nobody triages gets killed rather than accreting.

## Functional requirements

- **Must:** the night layer is expressed as **distinct proposal classes** (code-refactoring proposals ·
  code review · process review · creative brainstorm → SEED · backlog-groom proposals), each **behind
  #270** (load-gauge live first) and **under #271 / brief #1 §6** constraints.
- **Must:** every class names its **consumer + a survival metric ex-ante** (rent rule, ADR-98 §6) —
  per class, not once for the whole suite.
- **Must:** **no class mutates state** — all propose-only (refactor candidates flagged never deleted;
  ADR drafts status Proposed; ideas → `docs/intake/` as `status: SEED`; groom = a ratify-only digest);
  **no autonomous semantic refactoring at night**.
- **Should:** the **subagent-army pattern** (Sonnet/Haiku swarms for micro-specific,
  mechanically-verifiable tasks) is a first-class element of the suite, with its own bounded-task
  contract.
- **Could:** the classes share one morning-triage funnel with §6's teeth (CAP ~5 proposals/night;
  untriaged items auto-expire in 7 days).

## Acceptance criteria (ex-ante)

1. The suite is documented as **N named proposal classes**, each with (a) its output channel, (b) its
   consumer, (c) its ex-ante survival metric — verified by a per-class table; a class missing any of
   the three is not allowed to run.
2. For each class, a run **proposes only** — a post-run tree diff shows **zero** mutations to
   BACKLOG / code / ADR content (proposals land in their declared channels only) — verified by the diff.
3. The **load-gauge (#270) is live** before any class runs — verified by the `[load]` digest line
   existing.
4. The subagent-army pattern has a written **bounded-task contract** (task is micro-specific + is
   mechanically verifiable; model tier stated) and **one demonstrated swarm run** against such a task.
5. The first **2-week survival review per class** is recorded (accept-rate < ~20% kills that class),
   per #271.

## Non-goals

- Does **not** grant any new night autonomy — §6's "judgment sleeps with the architect" is frozen, not
  renegotiable here.
- Does **not** build #270 (the load-gauge) — that is the precondition, filed separately.
- Does **not** decide which model runs each pass beyond the S/M tier note (the cost/value check is
  brief #1's open question).
- Does **not** fold in the deterministic **execute-at-night** work (full serial test suite, hygiene) —
  this doc is the **propose** classes; the execute contracts are §6's separate leg.

## Impact sketch (4+1 lite)

- **Logical:** decomposes #271's single "loop" into a suite of rent-paying proposal classes + the
  subagent-army element.
- **Process:** all output flows into the morning-triage funnel; the SEED-producing class feeds
  `docs/intake/`.
- **Development:** rides #270 → #271; no new autonomy, no state mutation (Layer-2-safe / propose-only).
- **Physical:** night compute (Tier-2); outputs land in digests + `docs/intake/` + proposal logs.

## Open questions

- Is each proposal class a **separate routine** (each paying rent) or **one routine emitting classed
  output**? (technical-architect question.)
- Where does the subagent-army pattern sit — a night class, an on-demand operator tool, or both?
- Do the classes share **one survival metric** or **one-per-class** (leaning per-class, per the rent
  rule)?
- Which model tier per class, and does the subagent swarm's cost fit the credit budget (brief #1 open
  question, unresolved)?

## Status

SEED — captured 2026-07-08 from operator themes (this session). Behind #270; under #271 / intake brief
#1 §6; refs ADR-98 §6. Awaiting the load-gauge landing, then functional elaboration + technical triage.
