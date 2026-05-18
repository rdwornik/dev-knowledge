# Governance Essences — .dev-knowledge (session-sync 2026-05-18)

Operational ADR rules for ADRs explicitly cited in `07_ACTION_PLAN.md`.
These are 2–4 sentence essences — not full ADR copies.

---

## ADR-51 — Architecture Documentation Convention

M- and L-scale repositories must have a dedicated `ARCHITECTURE.md` at the
repository root; S-scale repositories are exempt. The document has a mandatory
core (bird's-eye purpose statement, auto-generated codemap, explicit layer
boundaries and invariants) plus optional sections for larger repositories. The
codemap is auto-generated and CI-enforced to prevent staleness; only the
narrative (purpose, invariants) is hand-written. A single canonical template
lives in `.dev-knowledge` — no per-repository copies.

Two open questions are NOT settled by ADR-51 and must be resolved before the
template can be finalized: (1) the codemap generator's exact output specification
(directory tree? package graph? CLI inventory?), and (2) the existing
`corp-monorepo` `ARCHITECTURE.md` and its C4 Mermaid→SVG pipeline have not
been inspected — both must be reviewed as read-only reference input before
authoring the template.

Full ADR: `.dev-knowledge/docs/decisions/ADR-51-architecture-doc-convention.md`

---

## ADR-36 — Audit Tool Architecture (read-only contract)

The `.dev-knowledge` audit tool writes ONLY to `.dev-knowledge` paths
(`.dev-knowledge/ecosystem/{repo}/`, `.dev-knowledge/docs/audits/`,
`.dev-knowledge/docs/handoffs/`) and NEVER touches child repositories directly.
This read-only contract with child repos is a hard constraint enforced by tool
architecture — not a convention that can be overridden per session.

Full ADR: `.dev-knowledge/docs/decisions/ADR-36-audit-tool-architecture.md`

---

## ADR-38 — Universal Repo Architecture Baseline

Every repository must have `src/`, `tests/`, and `pyproject.toml` (or
language equivalent) at minimum; `ARCHITECTURE.md` is optional for M-scale
and required for L-scale. Amendment A3 (2026-05-11) mandates `ARCHITECTURE.md`
placement at the repository root — not nested in `docs/`. Amendment A4
(2026-05-18) closed the corp-monorepo root-placement deferral: all repos now
comply with A3 immediately, no exceptions.

`.dev-knowledge` itself has an open ADR-38 self-compliance gap (no `src/` or
`pyproject.toml`) — the resolution path (governance-only-repo exemption vs.
minimal `pyproject.toml` creation) was not settled in the session that produced
this handoff; verify the ADR for the current decision.

Full ADR: `.dev-knowledge/docs/decisions/ADR-38-universal-repo-architecture.md`
