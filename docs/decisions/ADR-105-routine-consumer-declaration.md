# ADR-105: Routine consumer declaration — a six-field row shape, gated at ACTIVATION not at filing

**Status:** Accepted
**Date:** 2026-07-26
**Decision tier:** Architecture (Path A — direct operator ruling in-thread, 2026-07-26, across three review rounds of the session plan; the lane never self-accepts, ADR-94)
**Related:** [#419] (the defect this answers — *we run routines whose output nobody consumes*; stays OPEN, see Consequences), [#426] (the live-routine retrofit this does NOT perform), [#382] (the desired-state contract these rows fold into as row-shape when it lands), ADR-80 (two-tier automation adoption — the tier this governs), ADR-28/36 (Layer-2 read-only posture the checker keeps), ADR-66 (the BACKLOG row grammar the marker extends as an in-line clause)

## Context

The fleet runs standing routines whose output no one reads. The precipitating evidence: the
nightly conformance routine has emitted a digest every night onto `claude/conformance-*`
branches — **six of them unmerged** at the time of this decision — and the single High finding
among them (07-21 F1) was fixed on `main` by a session that never opened the branch that found
it, so the finding's second half went unfixed as a direct result.

A read-only enumeration performed for this decision found the defect is not confined to that
routine:

- The `nightly-triage` GitHub Action was **retired 2026-07-09** (`.github/` deleted at
  `82227f08`, present on no branch). Its last Issue was opened **2026-06-25**. **Fifteen remain
  open**, and `scripts/surface_triage.ps1` still reports at every session start that they
  "await" — a dead producer with a live nag.
- `surface_triage.ps1`'s own header already records the same class, diagnosed under #255: two
  earlier surfacings were retired because "a PR-triggered organ under a local-merge workflow
  was vacuous — it never fired."

The class has therefore been found in this repo before, fixed locally, and never generalized
into a rule. That is the argument for a citable authority rather than a remembered practice: a
rule recorded only in a session log is not something a future commit can be held to.

## Decision

### 1. The six-field routine row shape

A routine is declared as an in-line clause on its BACKLOG row (ADR-66 grammar — a bullet with
`·`-delimited clauses; **not** a continuation line, which the row parsers do not support and
no convention sanctions):

```
· routine: trigger=<what fires it> · scope=<what it covers> · consumer=<who reads it>
  · consumption_path=<how the output reaches a decision> · verified_by=<what proves it>
  · review_date=<YYYY-MM-DD>
```

`consumer` names a reader. `consumption_path` names the **mechanism** by which the output
reaches a decision — the field the conformance routine would have failed, since branches nobody
opens are a path in name only.

### 2. The gate is at ACTIVATION, not at filing — both halves are normative

**The bar.** A routine **may not ACTIVATE** without a named `consumer` and `consumption_path`.
A routine that cannot name them at activation is **retired, not activated**.

**The permission — equally binding.** **Filing a proposal for a routine is explicitly permitted
without them.** A proposed routine has produced no artifact, and an artifact that does not exist
has no consumer; requiring the fields at filing would demand either tautology or invention.

Both halves are recorded because either alone misleads. Read as a filing gate, this rule would
block the very tickets that exist to answer the question it asks — which is how `[#409]`,
`[#410]` and `[#411]` are treated: they carry a one-clause reference to this ADR so the
activation gate is discoverable when they are ruled in, and they carry **no** six-field marker,
because they propose routines that do not yet run.

### 3. Fold-forward, not a new registry

These rows are a **row-shape**, not a registry. When `[#382]`'s desired-state contract lands,
they fold into it as rows. Nothing in this decision creates a new `ecosystem/` file, and
nothing in it should be read as licence to.

### 4. Coverage boundary — read this before reading a green check

At acceptance this rule governs **one row** (`[#348]`, backlog grooming — a routine that runs
and emits output, so it has a consumer to name). The enumeration for this decision counted
**30 live routines** — session hooks (SessionStart, Stop, PreToolUse, Notification, across the
global, project and plugin layers), 15 commit-time gates, and 3 scheduled/remote jobs. **None of
them is a BACKLOG row, so none carries a marker and none is checked.**

`[#426]` carries that retrofit. It is filed, not built.

**A green check does not mean the fleet's routines have consumers.** It means the one governed
row declares one. The enforcing check states this boundary in its own docstring so the
distinction survives without this ADR in hand.

## Consequences

- The rule is citable. A future commit can be held to it; previously it could not.
- `[#419]` **stays OPEN.** Its `Done when` — *every standing routine has a named consumer and a
  consumption path* — is not met while 30 live routines are undeclared. Its row records that the
  rule and its gate landed and pegs the remaining coverage to `[#426]`. Closing it on this
  decision would be closing on the easy proxy, which is the failure `[#419]` names.
- The enforcement surface is one row wide. This is a deliberate, stated staging, not an
  oversight; the retrofit is scoped and owned rather than assumed.
- A routine that reaches activation unable to name a consumer is surfaced to the operator for a
  retire decision. Neither the executor nor the check retires it, and neither invents a consumer
  to avoid the surface.

## Ratification

Operator ruling in-thread, 2026-07-26, across three review rounds of the session plan. The
activation-vs-filing distinction was the operator's correction to an earlier filing-gate
formulation, made after the four candidate rows proved non-homogeneous: one runs, three are
proposals.
