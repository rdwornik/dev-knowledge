# ADR-50: Machine-document encoding standard

- **Status:** Accepted
- **Date:** 2026-05-17
- **Related:** ADR-48 (governance-admission rule)
- **Source:** AI Council debate, 2026-05-16 (`docs/decisions/transcripts/`)

## Context

Documentation is split into a human layer and a machine layer. The machine
layer — CLAUDE.md, LESSONS, ARCHITECTURE, ADRs, handoff bundles — is read
primarily by AI agents. An AI Council debate assessed how machine-layer files
should be encoded to maximise reliable agent comprehension.

## Decision

- **Encoding:** restricted structured markdown — fixed section headers, bullet
  lists, key-value blocks, minimal prose, minimal tables. Not prose-heavy; not
  a custom compressed notation; not YAML-first.
- **Language:** English — the highest-reliability language for current LLMs.
- **Conflict rule:** when token-efficiency and comprehension-reliability
  conflict, reliability wins. Pursue concision only up to the point it begins
  to risk comprehension.
- **Human readability** is preserved — machine-layer files are still
  occasionally maintained by a human.
- **Per-file-type schemas** are a *recommended convention*, not CI-enforced.
  Enforcement would require meeting the ADR-48 governance-admission rule
  (a recurring real failure); that bar has not been met, so the schema stays
  advisory.
- **Handoff bundle — operator override of the debate.** The debate recommended
  collapsing the bundle to a single manifest. The decision is to **retain the
  multi-file (12-file) handoff structure** — operational experience shows a
  single manifest is insufficient. Optimisation happens *within* that
  structure: eliminate redundancy and ambiguity, apply the structured encoding
  above. (Follow-up task — not yet executed.)

## Consequences

- Machine-layer files become more reliably parsed across models.
- The handoff stays robust (multi-file) but is to be tightened.
- The specific schema is provisional: an empirical cross-model encoding
  benchmark is recommended before the schema is finalised.
