# ADR-86: Conformance-dashboard location — `ecosystem/conformance.md` as an ADR-80 committed-generated zone

**Status:** Accepted
**Date:** 2026-06-16
**Decision tier:** Architecture (Path A — architect/operator decision, captured in the 2026-06-16 consolidation pass; originates from ADR-85 R2)

## Context
ADR-85 R2 deferred ungated-doc staleness detection (and the broader claims-vs-state conformance surface) to "the daily digest / **conformance dashboard**" — but never said *where* that dashboard lives, *in what zone class*, or *how it is maintained*. BACKLOG #169 (the ADR-85 R2 staleness signal) and any future conformance surface therefore had **no build target**: they "ride with the conformance-dashboard work" against a dashboard that was named but never located. This left the decision recorded nowhere (the 2026-06-16 consolidation survey found it absent from every ADR, the JOURNAL, and BACKLOG). The dashboard must satisfy the repo's standing invariants: deterministic, **read-only-generated** (Layer-2 never executes — `scripts/` validators only), and **committed** so it is diffable and auditable across runs rather than regenerated-on-demand.

## Decision
1. **Location.** The conformance dashboard lives at **`ecosystem/conformance.md`** — alongside the existing `ecosystem/` registry/state artifacts (the natural home for cross-repo conformance state).
2. **Zone class: ADR-80 committed-generated.** A read-only validator **generates it and commits its own output** under the ADR-80 writer policy (pathspec-bounded — never `git add -A`; fail-soft; the automation commits only its own file). This preserves the Layer-2 "validators only / never executes cross-repo" invariant (ADR-28/ADR-36): the dashboard is *produced by* a validator, it does not *drive* anything.
3. **Navigation (Ch2 pointer).** `ARCHITECTURE.md` Ch2 (organ map) gains a pointer to the dashboard — resolving the **G7** coverage-matrix gap (the organ map should point to the conformance surface). The pointer **lands with the build, not before**: a pointer to a not-yet-generated file would itself be drift, so it is part of the build item (#171), gated by the build's own freshness discipline.
4. **It is the surface ADR-85 R2 / #169's ungated-doc staleness signal lands in** — deterministic, not per-session-gated, not human memory.

**Deferred to the build (#171), not decided here:** the exact write channel (committed on `main` as a navigable surface vs. an `automation/*` branch per the ADR-84 writer-isolation pattern), the generator's check set, and the freshness/staleness hook. This ADR settles **location + zone class + navigation intent**; the mechanism is #171.

## Consequences
**Positive:** #169 and the conformance surface now have a concrete build target; the dashboard is deterministic, diffable, and Layer-2-safe; it reuses the existing ADR-80 writer pattern (no new mechanism invented). The location decision that G7 was blocked on is now recorded in the decision archive rather than living only as ADR-85's deferred R2 prose.
**Negative / accepted:** the dashboard is a **decision only** here — it is not built (the build is #171), so ADR-85 R2 staleness detection has no live home until #171 ships; the on-`main`-vs-`automation/*` channel question stays open until then.

## Alternatives rejected
- **Dedicated `automation/*` branch only (the ADR-84 nightly-digest model).** Rejected as the *primary* framing: the conformance dashboard is a durable, navigable surface that ARCHITECTURE Ch2 points to, not unattended write-output that must be isolated from `main`. (The channel may still borrow ADR-84 plumbing at build time — that is #171's call, not a reason to define the dashboard as branch-only.)
- **Generated-on-demand / not committed.** Rejected: not diffable or auditable across runs; the value is a committed artifact whose history shows conformance drift over time.
- **Folding it into the nightly digest.** Rejected: the digest is a point-in-time `docs/audits/*` record (append-one-per-night); the dashboard is a single living-but-generated surface — different lifecycle.

## Links
- ADR-85 (R2 — the originating deferral; this ADR locates the dashboard R2 named)
- ADR-80 (committed-generated zone / writer policy reused here)
- ADR-84 (automation-writer branch isolation — candidate plumbing for #171's channel choice)
- BACKLOG #169 (the staleness signal that lands here) · #171 (the build item)
- `ARCHITECTURE.md` Ch2 Organ map (the pointer target — pointer added by #171)
