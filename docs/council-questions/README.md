# council-questions/ — INPUTS for the AI Council Debate Pipeline

Per ADR-60 folder taxonomy.

## Purpose

Staging area for AI Council debate **question sets, evidence files, and set indexes**. These are the INPUTS to the Council pipeline — distinct from research OUTPUTS (`../research/` is the WORKING scratchpad; finished outputs live in `../audits/` and `../decisions/`).

## Lifecycle

1. Question set drafted here (format per `ai-council/docs/council-question-guide.md`).
2. Files copied to `ai-council/council_inbox/` for invocation (the inbox is gitignored in ai-council).
3. Council debate runs (multi-provider deliberation via the `ai-council` CLI).
4. Transcripts auto-route to `../decisions/transcripts/` via ADR-43 when the question carries `target-project: .dev-knowledge`.
5. ADRs distilled from transcripts → `../decisions/`.
6. The question set stays here as historical reference, or moves to `../archive/` once its ADRs are finalized.

## Naming convention

- Question files: `YYYY-MM-DD-{topic}-council-Q[N]-{slug}.md`
- Evidence: `YYYY-MM-DD-{topic}-failures-evidence.md` (or `-evidence.md`)
- Set index: `YYYY-MM-DD-{topic}-council-index.md`

## Required frontmatter (Council CLI contract)

Each question file carries the frontmatter the Council CLI reads:

```yaml
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick
target-project: .dev-knowledge
```

`target-project:` is what triggers ADR-43 transcript routing back to `../decisions/transcripts/`.

## Contents

The 2026-05-25 handoff-methodology debate set (5 questions Q1–Q5 + evidence + set index), migrated here from `../research/` on 2026-05-27 per ADR-60. Their transcripts are in `../decisions/transcripts/` (ADR-55..58 distilled from Q1–Q4).
