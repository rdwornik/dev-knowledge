---
version: 1.0
tier: M
owner: rob
last_reviewed: 2026-05-09
scale: M
status: active
---

# VISION — .dev-knowledge (Ecosystem Methodology Context)

<!-- scope: meta -->

> This file is `.dev-knowledge`'s own VISION.md — included in this cross-repo bundle
> as ecosystem methodology context for the ai-council Claude Code session.

## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. It works in any folder on any machine — portable,
self-contained, machine-agnostic. It is the ecosystem's knowledge guardian
and methodology author: it absorbs lessons from individual projects,
universalizes them into patterns, and disseminates those patterns back as
enforceable conventions. It also functions as auditor — evaluating each
project's scale (S/M/L) and verifying correct methodology implementation
(per ADR-40 scale tier evaluation).
Think of it as the LLM-development Scrum Master for the ecosystem: it
doesn't write code, it ensures the framework is applied consistently and
evolves with experience.

**Continuous improvement principle.** `.dev-knowledge` exists to
evolve. The framework absorbs lessons, refines patterns, retires what
fails. Continuous improvement is the baseline operating posture, not
an option. Sessions advance the framework; static maintenance is
exception requiring explicit justification.

## Strategic emphasis (current)

<!-- scope: meta -->

These are current strategic directions — emphasis areas within existing
scope, not new scope. Reviewed at session boundaries; may shift as the
ecosystem evolves.

- **Velocity in LLM technology adoption.** New models and capabilities
  emerge continuously across origins. Speed of evaluation, integration,
  and methodology adaptation is competitive advantage. Adoption pace
  tracked as an ecosystem health signal.

- **Cross-repo methodology consistency.** Every project under the
  ecosystem adheres to universal patterns (naming, scope tagging,
  governance artifacts, handoff protocols). Drift detected proactively
  via scanning; corrected via universal updates, not per-repo patches.

- **Methodology evolution as obsession.** Handoff protocols, prompt
  formats, audit mechanisms, skills definitions — all continuously
  improved based on real-usage friction. Static methodology is a
  failure mode; methodology that evolves with experience is the goal.

- **Lessons capture as default.** Every session yields generalizable
  insight when surfaced correctly. The lessons log is treated as a
  first-class artifact, not an afterthought. Patterns extracted from
  individual sessions become enforced conventions in subsequent sessions.

This section uses no fixed timeline — strategic emphasis evolves with
ecosystem maturity. Review triggers: major capability shift, new repo
joining ecosystem, sustained friction in current emphasis areas.

## Scope

**In scope:**
- Universal methodology and conventions for LLM-driven development
- Cross-repo governance patterns (AGENTS.md, CLAUDE.md, ADRs, handoffs)
- Knowledge consolidation: lessons learned, decisions, processes
- Scale assessment (S/M/L) and tier-appropriate guidance per project
- Audit and verification mechanisms ensuring child repos comply with
  applicable methodology

**Out of scope (non-goals):**
- Code-level implementation in child repos
- Project-specific business logic, schemas, or domain knowledge
- Operational data or runtime telemetry
- Replacement for repo-specific CLAUDE.md, AGENTS.md, or README files
- Hierarchy or authority over child repos beyond methodology compliance

## Relationships

`.dev-knowledge` is the meta-layer of the ecosystem. Child repositories
under `Dev/` (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation,
future repos) are independent projects that consume `.dev-knowledge`
methodology and conventions. There is **no hierarchy** in the authority
sense — only **functional roles**: `.dev-knowledge` produces methodology;
child repos consume and feed back lessons.

**Special case — `ai-council`:** functions as a tool used by `.dev-knowledge`
to generate architectural decisions. Council debate transcripts return to
`.dev-knowledge/docs/decisions/transcripts/` per Council output convention.
Operational metrics stay in `ai-council/output/`.

## Universalization principle

When an audit surfaces a deviation from a universal standard in one repo
(e.g., ai-council), the decision is: **migrate the repo to the standard**,
not amend the standard to accommodate the deviation. The standard holds;
the consumer conforms. Exceptions require an ADR — silent drift does not
earn grandfathering.

This principle governs the ai-council cleanup: ADR-46 and ADR-47 define
the universal standard. ai-council migrates to them. The migration decisions
are locked (see `07_ACTION_PLAN.md` Hard Constraints).
