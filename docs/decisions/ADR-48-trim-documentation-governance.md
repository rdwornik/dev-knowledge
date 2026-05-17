# ADR-48: Trim documentation governance to structural enforcement

- **Status:** Accepted
- **Date:** 2026-05-17
- **Amends:** ADR-46, ADR-47 (demoted); ADR-27 (scope-tagging system retired)
- **Source:** AI Council debate, 2026-05-16 (`docs/decisions/transcripts/`)

## Context

The documentation-governance machinery — an audit tool with format-detail
checks, ADR-46/47 enforced formats, a scope-tagging system with pre-commit
validation, and an evolution infrastructure — grew disproportionate for a
solo-developer ecosystem. A multi-session effort was spent purely on
documentation-format hygiene. An AI Council debate assessed proportionality.

## Decision

- **Audit tool** is trimmed to structural checks only — file and section
  presence (binary, deterministic). Format-detail checks (header levels,
  entry ordering, blank lines, heading-text patterns) are removed.
- **ADR-46 and ADR-47** are demoted to non-enforced conventions.
- **The scope-tagging system** (vocabulary + pre-commit validation) is
  retired. Existing inline scope tags remain as informal metadata.
- **Governance-admission rule:** a new check or rule is admitted only if it
  (1) solves a recurring real failure, (2) is fully automatable, and (3) has
  low ongoing cost. Otherwise it remains a non-binding convention.
- Cosmetic consistency that is still wanted (e.g. uniform header levels) is
  handled by a deterministic auto-format normalizer, not by an audit check.

The disposition of the evolution infrastructure was raised in the debate but
is **not decided here** — deferred to a separate decision.

## Consequences

- Less format-correction thrashing; the audit is a thin structural boundary.
- Cross-repo cosmetic uniformity is no longer machine-enforced — accepted.
- The audit fails only on missing structure, not on cosmetic drift.
- Reversible per check: a removed check may return if it later meets the
  governance-admission rule.
