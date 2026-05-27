# research/ — Exploratory Pre-Decision Scratchpad
<!-- scope: meta -->

Per ADR-60 folder taxonomy.

## Purpose

WORKING-state scratchpad for exploratory drafts and pre-decision investigation: AI Council research-mode outputs (multi-model research with web citations), standalone research reports, and debates that inform practice without committing `.dev-knowledge` to a decision. Files here are in-flight; when their role resolves they mature into:

- `../audits/` — when becoming a finished audit / report / validation
- `../decisions/` — when becoming an ADR
- `../council-questions/` — when becoming a Council debate input
- `../archive/` — when superseded or dormant

## Distinction from neighbours

- `../decisions/` = ADRs + transcripts for decisions affecting `.dev-knowledge` itself (OUTPUTS)
- `../audits/` = finished audit OUTPUTS (point-in-time state analysis)
- `../council-questions/` = Council debate INPUTS (question sets, evidence, indexes)
- `research/` = reference material that informs decisions but does not commit to one (WORKING)

## Lifecycle

1. Draft here when work is exploratory and the destination is not yet known.
2. When the destination is clear: `git mv` to the appropriate folder (preserves history).
3. If superseded: archive.

## When NOT to use research/

- Finished artifacts → go directly to `audits/`, `decisions/`, `handoffs/`, or `council-questions/`.
- Active work with a known destination → start in the destination folder.
- Transient snapshots → consider `archive/` directly.

## Naming convention

`YYYY-MM-DD-{descriptive-slug}.md`

## Current contents (newest first)

- 2026-05-17-kimi-k2-scoping.md — Kimi K2 model scoping
- 2026-04-27-handoff-patterns-external-research.md — external research on handoff patterns
- 2026-04-27-handoff-patterns-council-research.md — Council research on handoff patterns
- 2026-04-24-council-29-spec-kit-kiro.md — Spec Kit and Kiro evaluation
- 2026-04-24-multi-agent-debate-patterns.md — multi-agent frameworks research
- 2026-04-24-claude-md-best-practices.md — CLAUDE.md structuring research
- 2026-04-23-council-28-community-patterns.md — community LLM dev patterns review
- 2026-04-23-llm-dev-patterns-2026.md — general LLM dev patterns
- 2026-04-15-council-26-tach-adoption-corp-monorepo.md — Tach adoption for corp-monorepo
- 2026-03-30-council-25-diagrams-corp-monorepo.md — diagram format for corp-monorepo
- 2026-03-29-council-research-new-models.md — new LLM models/APIs research
- 2026-03-29-council-browser-handoff.md — browser chat handoff patterns

> Debates #25 (diagrams) and #26 (Tach) decided corp-monorepo architecture; transcripts are kept here for reference and may mirror to `corp-monorepo/docs/decisions/transcripts/` in future.

## History

This folder pre-dates ADR-60 and historically conflated INPUTS + OUTPUTS + WORKING artifacts (pipeline-audit finding A1). Cleaned 2026-05-27: the 2026-05-25/26 Council pipeline inputs, audit outputs, and transient snapshot were reclassified to `council-questions/`, `audits/`, and `archive/`. The folder now holds WORKING/exploratory content only.
