# ADR-49: Consolidate past-recording documentation files

- **Status:** Accepted
- **Date:** 2026-05-17
- **Amends:** ADR-46, ADR-47 (fewer files governed)
- **Related:** ADR-48
- **Source:** AI Council debate, 2026-05-16 (`docs/decisions/transcripts/`)

## Context

Each repository carried four overlapping files recording "the past":
CHANGELOG, JOURNAL, BACKLOG_ARCHIVE, and LESSONS. For a non-released
solo-developer ecosystem with descriptive git history, this overlap was
redundant and a recurring source of format drift. An AI Council debate
assessed consolidation.

## Decision

- **CHANGELOG is removed.** The change record is git history (descriptive
  Conventional-Commits messages) plus a "Changes" line in each JOURNAL entry.
  This makes commit-message quality load-bearing — see the commit-message
  standard in `ESSENTIALS.md`.
- **BACKLOG_ARCHIVE is removed.** Done backlog items simply leave BACKLOG
  (their trace is in git). A *significant* abandoned backlog item is recorded
  as a lightweight decision-note in `docs/decisions/` — not as a JOURNAL line
  — preserving structured, discoverable rationale that git cannot hold.
- **JOURNAL** is the single human past-narrative, with a per-entry structure:
  Did / Result / Changes / Abandoned / Next. It is read by the developer and
  by AI agents (recent entries, as development context).
- **LESSONS** is kept standalone as a machine-layer, agent-consumed file.
  Lightweight scope tags remain as informal metadata.
- Net: four past-recording files reduce to two — JOURNAL and LESSONS.

## Consequences

- Roughly half the past-axis format-governance surface is removed.
- "What changed" now depends on commit-message discipline; the prescriptive
  commit standard is the mitigating dependency.
- The road-not-taken is preserved only for *significant* abandoned items;
  trivial ones are intentionally not recorded.
- Reversible: if a repository is ever released externally, a generated
  CHANGELOG can be reintroduced.
