---
version: 1.0
owner: rob
last_reviewed: 2026-09-01
status: active
---

# .dev-knowledge
<!-- scope: meta -->
<!-- [#614] lane-e-5, 2026-09-01 review record: re-read end-to-end before the VISION.md
     relocation lands (Done-contract item 3, LANE-e-5-vision-relocation.md). Confirmed
     against live source -- ecosystem/registry.md, ecosystem/north-star.md, CONTRIBUTING.md,
     AGENTS.md and protocols/ESSENTIALS.md all exist as cited; the rest of the file (Vision,
     Strategic emphasis, Scope, Values, Relationships, Lifecycle) is unaffected by the move.
     Only the VISION.md pointers (the blockquote below + the References row) are stale as of
     the relocation; both are re-pointed in this lane's next commit. Collateral enumerated at
     docs/audits/2026-09-01-technical-dc3-split.md §4; full record in the end-of-lane artifact. -->

> **Root front door.** This file supersedes `VISION.md` as the canonical statement of what
> this repo is, per **ADR-114** (Accepted 2026-08-29, AMENDMENT 1). At the hub, `VISION.md`
> is **relocated** — `git mv` to `docs/archive/VISION.md`, byte-identical ([#614] lane-e-5,
> 2026-09-01) — the hub's own step one of ADR-114 option (C)'s sequenced nine-repo filename
> migration. It stays retired-tier, not deleted, and still tracked; it remains a `MUST` on
> eight of the nine ADR-104 fleet members (`terminal-setup` has never carried one), so the
> rest of the fleet's migration is still a sequenced program, not a flag flip.
>
> **Working here?** `CLAUDE.md` is the session contract, `AGENTS.md` the portable
> build/test/land layer every provider reads, `ARCHITECTURE.md` the structural map.

## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. Its **doctrine is host-independent**: the
conventions it defines, and the hub-local validators, generators and gates
in `scripts/` that enforce them, carry no machine-specific paths and apply
to any repo in any folder. Its **artifacts are not** — two layers bind to
this host, in different ways. The corpus *documents* the host in places
(`protocols/ENVIRONMENT.md` is a machine description by design;
`templates/prompt-template.md` and some ADR examples cite absolute paths).
The **fleet-registry and machine-automation layer** *depends* on it: the
derived `ecosystem/index.yaml`, the marketplace path in
`.claude/settings.json`, `scripts/fleet-baseline.task.xml` (Windows Task
Scheduler), and the gitignored per-repo `ecosystem/*/state.yaml`. A fresh
clone can apply the methodology; the fleet automation and the self-audit
registry must be re-seeded for their host. It is the ecosystem's knowledge
guardian and methodology author: it absorbs lessons from individual projects,
universalizes them into patterns, and disseminates those patterns back as
enforceable conventions. It also functions as auditor — verifying correct
methodology implementation against the universal governance baseline
(ADR-38 amendment A5 as superseded by ADR-114 in the single respect of the
root `README.md`; the repo-tier system was deprecated 2026-05-23).
Think of it as the LLM-development Scrum Master for the ecosystem: it
doesn't write code, it ensures the framework is applied consistently and
evolves with experience.

**Continuous improvement principle.** `.dev-knowledge` exists to
evolve. The framework absorbs lessons, refines patterns, retires what
fails. Continuous improvement is the baseline operating posture, not
an option. Sessions advance the framework; static maintenance is
exception requiring explicit justification. The methodology now
self-enforces: it applies its own conventions to its own process — the
Tier-1 lifecycle (ADR-70) holds session-boundary closure, lint, and review
to the same enforced-not-remembered bar it imposes on the artifacts it
governs, not only on those artifacts.

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
  ecosystem adheres to universal patterns (naming, repo layout, governance
  artifacts, handoff protocols). Drift detected proactively
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
- Replacement for a repo-specific `CLAUDE.md`
- Hierarchy or authority over child repos beyond methodology compliance

## Values

Core operating values (how Claude reasons, communicates, and verifies)
live in `protocols/ESSENTIALS.md` "How Claude thinks" section. This file
defers to ESSENTIALS for principles — no duplication. Key principle:
**continuous improvement** as default project posture (ESSENTIALS
"Governance frame"; canonical: PLAYBOOK Ch13 "Project-evolution posture").

## Relationships

`.dev-knowledge` is the meta-layer of the ecosystem: the hub plus a set of
child repositories under `Dev/`, declared by ADR-104. **Who the members are,
what each is for, and where each stands is `ecosystem/registry.md`** — the
human fleet registry, which is also where the fleet's shape and migration
posture live. The roster is not restated here, because a roster typed into
prose is stale at the next commit.

The children are independent projects that consume `.dev-knowledge`
methodology and conventions. There is **no hierarchy** in the authority
sense — only **functional roles**: `.dev-knowledge` produces methodology;
child repos consume and feed back lessons.

**Pattern for child repos** (per ADR-33 universalization):
every project under `Dev/` should have its own canonical purpose document
following this template (vision + scope + values + relationships +
lifecycle + references). Child purpose documents are project-specific;
this hub's is universal. The document's **filename** is mid-migration
across the fleet — the posture, and what each member owes, is in
`ecosystem/registry.md`.

**Special case — `ai-council`:** functions as a tool used by `.dev-knowledge`
to generate architectural decisions. A transcript's **sole** home is the
canonical `ai-council/output/`. The routed-mirror clause of ADR-43 was
**retired 2026-07-23** (RE-SCOPE, operator ruling 2026-07-22): transcripts
no longer route into any repo's `docs/decisions/transcripts/`, and
`target-project:` / `--target-project` are not to be set. This hub's
landing zone was deleted 2026-07-22 (`b4435fad`) and must not be
recreated — the ADR-77 immutability guard stays armed. ADR-43 still
governs ai-council's repo-local canonical-write production.

## Lifecycle

This is a **living, verifiable document** — not a one-shot statement.

**Review triggers** (not deadlines):
- Major architectural shift in `.dev-knowledge` ecosystem
- New repo joining ecosystem
- Significant scope reinterpretation in fresh AI chat (drift signal)
- When the Vision section appears realized → propose next horizon

**Verification mechanism:** the Vision is verified against other ecosystem
artifacts to detect drift:
- Backlog (story map per ADR-66) reflects what this file declares as in-scope
- JOURNAL entries trace work back to the goals stated here
- ADRs implement the decisions stated here
- Drift signal: any of above contradict this file → trigger review

**Audit support:** verification mechanism implemented via `.dev-knowledge`
auditor (`scripts/audit.py` per ADR-36 — `health`/`repo`/`run`/`registry`/
`ship-gate`/`checks` commands). It is **read-only on siblings** — the ADR-36
invariant, and the checkable one — **not read-only on this repo**: it writes
findings, pushes to `origin` and commits durable Routine
output to `automation/fleet-audit`. The cross-repo `run`/`repo` are
manually invoked; the self-audit `health` (all registered `ALL_CHECKS` — count via `scripts/audit.py checks`) runs as this repo's pre-commit gate ([#69]).
Manual session-close verification per HANDOFF_PROCESS.md complements the tool.

**Vision realized:** when the current Vision becomes current state, archive
as `docs/archive/YYYY-MM-DD-vision-vN-realized.md` (the dated-artifact
naming convention, CLAUDE.md §4) and propose next horizon. This file
stays alive — only its content evolves.

**Tier classification:** retired 2026-05-23. The repo-tier system (ADR-33
`tier:`/`scale:` frontmatter, ADR-40 algorithmic computation) is deprecated
ecosystem-wide; `.dev-knowledge` declares no tier. The universal governance
baseline (ADR-38 amendment A5) applies regardless of repo size. Historical
note: this repo was formerly classified M by architect judgment, while
ADR-40's algorithm clamped all repos to L under documented miscalibration
(F-08) — that divergence is part of what motivated the deprecation.

**Ownership:** Rob (sole authority).
**Edit process:** AI Council debate for Vision/Scope changes; conversational
edit for clarifications and the References section.

## References

- `CLAUDE.md` — the session contract for Claude Code in this repo
- `AGENTS.md` — the portable instruction layer every provider reads (ADR-115)
- `ARCHITECTURE.md` — the structural map; read before structural changes
- `docs/archive/VISION.md` — superseded by this file (ADR-114); relocated here at the hub ([#614] lane-e-5, 2026-09-01), retained and still tracked
- `protocols/ESSENTIALS.md` — operating values, daily cheat sheet
- `protocols/PLAYBOOK.md` — full process reference
- `JOURNAL.md` — session-by-session activity history (and notable-change record; replaces the retired CHANGELOG.md per ADR-49)
- `BACKLOG.md` — cross-session pending items (per ADR-41)
- `ecosystem/north-star.md` — **the arc set in dependency order: what this repo is working towards and what blocks what.** GENERATED from `tasks/` (`scripts/gen_north_star.py --write`); the arc names and their order are declared, every count and member row is derived, so it cannot drift from the backlog the way a hand-written roadmap does
- `CONTRIBUTING.md` — branch/commit/validator conventions
- `docs/decisions/` — architectural decisions (ADRs only; the `transcripts/` landing zone was deleted 2026-07-22)
- ADR-88 — File-oriented dependency management (markdown as a design pattern): repo files are the dependency unit; coherence across the declared edge-graph is held by mechanism — a conformance harness — not by memory.
