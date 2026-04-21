# ADR-28: Three-Layer Architecture (Descriptive)

**Status:** Accepted
**Date:** 2026-04-21
**Type:** Descriptive — documents existing practice, not new constraint

## Context

After 6 months of incremental growth, `.dev-knowledge` has become the system of record for dev methodology without ever being formally defined. The 2026-04-21 session (tech radar → Council #27 → vision redefinition) surfaced the implicit operating model: browser chat (analysis) → `.dev-knowledge` (passive storage) → projects (execution) → reflection back to browser. See PLAYBOOK "System Architecture" section for the full diagram.

## Decision

Document the three-layer architecture as canonical in PLAYBOOK, inserted before "Project Scale Tiers". Key invariants:

- `.dev-knowledge` contains no executable orchestration — scripts do not reside here
- Write-back flows through Layer 1 (browser chat handoffs), not Layer 3 direct edits
- Execution is one-way (Layer 2 → Layer 3); knowledge flow is bidirectional

## Why no Council debate

Three-layer is **descriptive** — it names an operating pattern already in place, not a trade-off between competing alternatives. Council debate would be theater (see PLAYBOOK Section 5, "Council debate threshold"). If a future session produces evidence contradicting the model (e.g., a script genuinely must reside in `.dev-knowledge`, or execution starts flowing Layer 3 → Layer 2 directly), reopen with Council #N.

## Consequences

- **Clarifies** "where does this file belong?" (which layer) in addition to Section 12's "which domain"
- **Creates dependency on Layer 1** — handoff loss = write-back loss. Mitigated by HANDOFF_PROCESS.md.
- **Revisit triggers:** tooling genuinely needing to live in `.dev-knowledge`, execution flowing 3 → 2, or a second contributor (same trigger set as Council #27 reopen conditions).

## References

- Handoff: `docs/handoffs/2026-04-21-dev-knowledge-architecture-redefinition.md`
- ADR-27 (Council #27, scope tagging) · PLAYBOOK "System Architecture" · PLAYBOOK Section 12
