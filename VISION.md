---
version: 1.0
tier: M
owner: rob
last_reviewed: 2026-05-09
scale: M
status: active
---

# VISION — .dev-knowledge
<!-- scope: meta -->

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

## Values

Core operating values (how Claude reasons, communicates, and verifies)
live in `protocols/ESSENTIALS.md` "How Claude thinks" section. VISION
defers to ESSENTIALS for principles — no duplication. Key principle:
**continuous improvement** as default project posture (see ESSENTIALS
"Continuous Improvement" section).

## Relationships

`.dev-knowledge` is the meta-layer of the ecosystem. Child repositories
under `Dev/` (corp-monorepo, ai-council, corp-ops, corp-sca-time-automation,
future repos) are independent projects that consume `.dev-knowledge`
methodology and conventions. There is **no hierarchy** in the authority
sense — only **functional roles**: `.dev-knowledge` produces methodology;
child repos consume and feed back lessons.

**Pattern for child repos** (per ADR-33 universalization):
every project under `Dev/` should have its own `VISION.md` following this
template (vision + scope + values + relationships + lifecycle + references).
Child repo VISION files are project-specific; `.dev-knowledge` VISION is
universal.

**Special case — `ai-council`:** functions as a tool used by `.dev-knowledge`
to generate architectural decisions. Council debate transcripts return to
`.dev-knowledge/docs/decisions/transcripts/` per Council output convention.
Operational metrics stay in `ai-council/output/`.

## Lifecycle

VISION is a **living, verifiable document** — not a one-shot statement.

**Review triggers** (not deadlines):
- Major architectural shift in `.dev-knowledge` ecosystem
- New repo joining ecosystem
- Significant scope reinterpretation in fresh AI chat (drift signal)
- When Vision section appears realized → propose next horizon

**Verification mechanism:** VISION is verified against other ecosystem
artifacts to detect drift:
- Stream backlog reflects what VISION declares as in-scope
- JOURNAL entries trace work back to VISION goals
- CHANGELOG describes movement toward VISION
- ADRs implement VISION decisions
- Drift signal: any of above contradict VISION → trigger review

**Audit support:** verification mechanism implemented via `.dev-knowledge`
auditor (Stream C audit tool — pending, per ADR-36). Until tool exists,
manual verification at session-close per HANDOFF_PROCESS.md.

**Vision realized:** when current Vision becomes current state, archive
as `docs/archive/VISION_v{N}_realized_YYYY-MM-DD.md` and propose next
horizon. VISION file stays alive — only its content evolves.

**Tier classification:** M (architect judgment, 2026-05-09).

Algorithm-classified tier per ADR-40 currently L — all repos clamp to L
under current coefficients due to documented miscalibration (F-08,
cross-ecosystem calibration concern). Architect judgment balances: single
developer, no SLA, no team (argues against L); multi-repo governance
authority, ADR producer for ecosystem (argues against S); moderate
complexity (~42 ADRs, governance + audit + handoff infrastructure). M is
most defensible under calibration uncertainty. Revisit post audit tool P1
multi-repo data collection (BACKLOG Stream C P1).

**Ownership:** Rob (sole authority).
**Edit process:** AI Council debate for Vision/Scope changes; conversational
edit for clarifications and References section.

## References

- `protocols/ESSENTIALS.md` — operating values, daily cheat sheet
- `protocols/PLAYBOOK.md` — full process reference
- `README.md` — current capability + file index
- `JOURNAL.md` — session-by-session activity history
- `CHANGELOG.md` — notable changes timeline
- `BACKLOG.md` — cross-session pending items (per ADR-41)
- `CONTRIBUTING.md` — branch/commit/validator conventions
- `docs/decisions/` — architectural decisions (ADRs + transcripts)
