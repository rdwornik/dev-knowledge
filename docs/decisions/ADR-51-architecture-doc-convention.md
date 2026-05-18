# ADR-51: Architecture Documentation Convention for the `.dev-knowledge` Ecosystem

- **Status:** Accepted
- **Date:** 2026-05-18
- **Amends:** —
- **Decommission:** none
- **Source:** AI Council debate (`pick` mode, 4-model panel + synthesizer, 2026-05-18). Transcript: `docs/decisions/transcripts/council-out-20260518_215241-pick-2026-05-18_council-debate-architecture-doc.md`

## Context

The `.dev-knowledge` ecosystem is maintained by a single developer across repositories of varying scale (`Project Scale: S / M / L`, declared in each repo's `CLAUDE.md`). Re-orientation after weeks away from a repository is slow and unsupported, and architecture documentation today is inconsistent — `corp-monorepo` has an `ARCHITECTURE.md`, most repositories have none.

A prior manual-upkeep document — a single-file handoff — went roughly five weeks stale before being retired. This establishes the dominant constraint: any convention that relies on remembered manual updates has already been empirically falsified in this ecosystem.

An AI Council debate was run to settle a standard convention. This ADR records its outcome.

## Decision

1. **Coverage.** A dedicated `ARCHITECTURE.md` is mandatory for **M-** and **L-scale** repositories. **S-scale** repositories are exempt; an S repo may add an optional "Architecture" section to its `README.md` if re-entry friction appears.

2. **Artifact.** The document is a dedicated `ARCHITECTURE.md` at the repository root. Architecture content is **not** folded into `CLAUDE.md` — agent instructions and human re-orientation remain separate artifacts with disjoint contracts (`README.md` = what this is; `CLAUDE.md` = how to work with it; `ARCHITECTURE.md` = what exists and why; `docs/decisions/` = decision history).

3. **Template and depth.** A single canonical template lives in `.dev-knowledge` — no per-repository copies (ADR-36/38). It defines a mandatory core that every covered repository completes, plus optional sections larger repositories add. Optional sections are expected mainly at L scale.

4. **Mandatory minimum content.** Every covered `ARCHITECTURE.md` contains: a bird's-eye purpose statement; a codemap (named modules/directories and how they relate); and explicit layer boundaries and architectural invariants.

5. **Staleness control — hybrid.** The structural codemap is **auto-generated** from the codebase; only narrative (purpose, invariants) is hand-written. A **CI check** regenerates the codemap and fails if the committed output differs — enforced from day one. The weekly `/evolve` review aggregates these checks and reviews whether hand-written invariants still match the current architecture.

6. **Graphical depth — tiered.** M- and L-scale repositories use a **graphical** codemap (diagram). Where an S-scale repository documents architecture at all, it uses a **text-only** general module overview — no diagram.

## Consequences

- The ecosystem commits to building and maintaining two shared tools in `.dev-knowledge`: a codemap generator and a CI freshness check. Because the codemap is part of the mandatory minimum (Decision 4), the generator is **load-bearing** — it must exist before any M/L repository can satisfy the convention.
- Hand-written invariants remain the human-authored heart of the document. The codemap is the *map*; the invariants are the *policy*. Generation never overwrites the invariants — a generated map would otherwise normalise architectural drift by drawing a breach as truth.
- Each covered repository's `CLAUDE.md` gains a one-line pointer to `ARCHITECTURE.md`.
- Initial rollout targets the current M/L repositories: `corp-monorepo`, `ai-council`, `corp-ops`.
- S repositories receive less structured re-entry support; this is accepted because an S repo is small enough that the README and the code itself are the document, and a near-empty `ARCHITECTURE.md` rots fastest and trains the author to ignore the file.

## Open questions — not settled by this ADR

- **Codemap generator output spec.** The debate did not define what the generated codemap should contain — directory tree, package graph, CLI/module inventory. Under-generation fails orientation; over-generation produces noise. This needs a separate design pass.
- **The existing `corp-monorepo` `ARCHITECTURE.md`.** `corp-monorepo` already has an `ARCHITECTURE.md` and a C4 Mermaid→SVG pipeline; neither was inspected during the debate. Both should be reviewed as input to the template and the generator before either is authored.
- **Shared-tooling versioning.** How repositories consume the `.dev-knowledge` generator and linter safely (pinning by tag/SHA) is undefined.
- **Pilot criteria.** Pilot duration, success metrics (did re-orientation get faster? did CI catch drift?), and revert conditions are not defined.

## Alternatives considered

- **Universal coverage** — `ARCHITECTURE.md` in every repository regardless of scale. Rejected: S repos are single-purpose; a near-empty document rots fastest and erodes trust in the convention.
- **Architecture content inside `CLAUDE.md`.** Rejected: conflates agent-instruction and human-re-orientation audiences, bloats agent context, and complicates drift detection.
- **Manual upkeep only** (with or without link-checking). Rejected: directly falsified by the five-week-stale handoff precedent.
- **Per-tier templates** (separate S/M/L documents). Rejected: triples the maintenance surface in `.dev-knowledge` for marginal benefit; incompatible with the single-canonical-template rule.
- **One-time codemap generation without ongoing CI.** Rejected: recreates the staleness problem in slower motion.
