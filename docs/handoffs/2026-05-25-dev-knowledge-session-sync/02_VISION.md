---
version: 1.0
owner: rob
last_reviewed: 2026-05-24
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
enforceable conventions. It also functions as auditor — verifying correct
methodology implementation against the universal governance baseline
(ADR-38 amendment A5; the repo-tier system was deprecated 2026-05-23).
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
- Cross-repo governance patterns (CLAUDE.md, ADRs, handoffs)
- Knowledge consolidation: lessons learned, decisions, processes
- Universal methodology-appropriate guidance per project (repo-tier
  assessment retired 2026-05-23 — guidance is universal, calibrated by
  judgment of repo complexity)
- Audit and verification mechanisms ensuring child repos comply with
  applicable methodology

**Out of scope (non-goals):**
- Code-level implementation in child repos
- Project-specific business logic, schemas, or domain knowledge
- Operational data or runtime telemetry
- Replacement for repo-specific CLAUDE.md or README files
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
- ADRs implement VISION decisions
- Drift signal: any of above contradict VISION → trigger review

**Audit support:** verification mechanism implemented via `.dev-knowledge`
auditor (`scripts/audit.py` per ADR-36 — `health`/`repo`/`run`/`registry`
commands, read-only, manual invocation). Manual session-close verification
per HANDOFF_PROCESS.md complements the tool.

**Vision realized:** when current Vision becomes current state, archive
as `docs/archive/VISION_v{N}_realized_YYYY-MM-DD.md` and propose next
horizon. VISION file stays alive — only its content evolves.

**Tier classification:** retired 2026-05-23. The repo-tier system (ADR-33
`tier:`/`scale:` frontmatter, ADR-40 algorithmic computation) is deprecated
ecosystem-wide; `.dev-knowledge` declares no tier. The universal governance
baseline (ADR-38 amendment A5) applies regardless of repo size. Historical
note: this repo was formerly classified M by architect judgment, while
ADR-40's algorithm clamped all repos to L under documented miscalibration
(F-08) — that divergence is part of what motivated the deprecation.

**Ownership:** Rob (sole authority).
**Edit process:** AI Council debate for Vision/Scope changes; conversational
edit for clarifications and References section.

## References

- `protocols/ESSENTIALS.md` — operating values, daily cheat sheet
- `protocols/PLAYBOOK.md` — full process reference
- `JOURNAL.md` — session-by-session activity history (and notable-change record; replaces the retired CHANGELOG.md per ADR-49)
- `BACKLOG.md` — cross-session pending items (per ADR-41)
- `CONTRIBUTING.md` — branch/commit/validator conventions
- `docs/decisions/` — architectural decisions (ADRs + transcripts)
