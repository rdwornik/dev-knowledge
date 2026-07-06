# ADR-70 Amendment 2026-07-07 — XL routing tier: Claude Fable 5 for the browser-architect layer

- **Status:** Accepted — 2026-07-07 architect ratification session (operator ruling R4). Ratifies the addition of an **XL** routing tier (Claude Fable 5) scoped to the browser-architect layer; the CC-side fan-out S/M/L pins are affirmed unchanged.
- **Date:** 2026-07-07
- **Amends:** ADR-70 (the three-tier process layer / routing doctrine anchor). Authored as a **separate file** because ADR-70 is immutable (CLAUDE.md §5 item 3) — following the `ADR-51-amendment-2026-07-05` precedent; ADR-70's in-file "Addendum — shipped reality (2026-06-02)" stays as written, and ADR-70's body is untouched.
- **Related:** ADR-80 §5 (the `fallbackModel` doctrine — the **different mechanism** this amendment must not be conflated with), ADR-87 (architect↔CC equilibrium — the browser-architect layer this tier scopes to), ARCHITECTURE.md Ch3 "Model routing (t-shirt)" + PLAYBOOK Appendix B (the routing-doctrine surfaces; the deterministic per-task-class table is canonical in `~/.claude/ROUTING.md`, #158)
- **Decommission:** none
- **Source:** 2026-07-07 architect ratification session (operator ruling R4); consumes the routing-tier question raised in the 2026-06-15 changelog-review audit (`docs/audits/2026-06-15-changelog-review.md`, flagged architect-call). Empirical basis: weeks of Fable-5 use **including the 2026-07-07 architect arc itself.**

## Context

The routing doctrine ADR-70 anchors pins CC-side fan-out by t-shirt size — **S = Haiku · M = Sonnet · L/judgment = Opus** (ARCHITECTURE.md Ch3 "Model routing (t-shirt)", citing "Appendix B; ADR-70"; the deterministic table lives in `~/.claude/ROUTING.md` per #158). Claude Fable 5 (Mythos-class) was absent from that doctrine. The 2026-06-15 changelog-review flagged whether Fable 5 earns a routing tier as an explicit **architect call**. Weeks of Fable-5 use — including the browser-architect work of the 2026-07-07 ratification arc itself — established its fit for the **browser-architect layer**: adjudication, multi-document synthesis, and ratification sessions.

## Decision

1. **Add tier XL = Claude Fable 5**, scoped to the **browser-architect layer** — adjudication, multi-document synthesis, and ratification sessions.

2. **XL is a new browser-layer tier, orthogonal to the CC-side fan-out size pins — NOT a fourth fan-out size.** **S = Haiku / M = Sonnet / L = Opus stay untouched for CC-side builds.** The fan-out-pinning statement (ARCHITECTURE.md Ch3, "pin every fan-out stage by size") is therefore **unaffected** — XL addresses a different layer (the browser architect), not fan-out sizing.

3. **Conditional on current availability / pricing terms.** The **fallback is Opus**, and the tier is **re-evaluated on any pricing change.** XL is adopted on today's terms, not unconditionally.

4. **Anti-conflation note (mandatory).** ADR-80 §5's rule — *pinned routine/workflow stages MUST NOT set `fallbackModel`* — governs a **different mechanism**: silent model substitution on a **pinned verifier/fan-out stage** breaks **evidence comparability** across runs (the n=2 gate compares like-for-like). **This amendment does not touch that rule.** The XL tier is a routing *choice at the browser-architect layer*, and its "fallback = Opus" is a **coarse availability fallback for an interactive human-facing layer**, not a `fallbackModel` on a pinned deterministic stage. The two must not be conflated: pinned stages still forbid `fallbackModel` (ADR-80 §5); the browser-architect layer may fall back Opus↔Fable on availability.

## Consequences

- **Easier:** the browser-architect layer has a recorded, sanctioned model tier matching weeks of lived practice, instead of an undocumented default.
- **Operational landing is downstream + out of this hub-only arc's scope.** The doctrine home is this amendment; the operational surfaces are `~/.claude/ROUTING.md` (the deterministic table, a runtime-config-repo change — the #100/#189 execute-elsewhere precedent) and, if desired, an XL row on the ARCHITECTURE.md routing prose. Neither is edited by this arc (hub-only; the CC-side fan-out line stays correct as-is per Decision 2).
- **Conditional, not permanent:** if Fable-5 pricing/availability terms change, the tier is re-evaluated; the fallback to Opus keeps the browser layer functional in the interim.
- **ADR-70's body is untouched;** this is an additive amendment file, not an in-place edit (CLAUDE.md §5 item 3, the ADR-51-amendment precedent).

## Alternatives considered

- **Add Fable 5 as a fourth fan-out size (a new CC-side S/M/L/XL pin).** Rejected: it is a browser-architect-layer tier, not a fan-out size; folding it into the CC-side pins would both mis-scope it and risk conflation with the ADR-80 pinned-stage rule.
- **Adopt Fable 5 unconditionally.** Rejected: pricing/availability terms are not guaranteed; the tier is scoped conditional-on-current-terms with an Opus fallback and a re-evaluate-on-pricing-change trigger.
- **Leave the routing doctrine silent (status quo).** Rejected: weeks of Fable-5 browser-architect use (incl. this arc) is undocumented practice running ahead of doctrine — the exact enforced-not-remembered gap the methodology exists to close.
