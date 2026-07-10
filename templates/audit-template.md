# <Title — what was audited, not the verdict>

- **Class:** <class> (ADR-101 enum) · **Date:** YYYY-MM-DD
- **Source-session:** <run / lane / HEAD or session context>
- **Status:** <PROPOSAL-ONLY | complete | …>
- **Model:** <model-in-effect — recommended for unattended runs, ADR-80 §5 silent-swap doctrine>

<!--
  Audit-file template — ADR-101 (Accepted 2026-07-11, ratification amendment §R3–R6).
  Peer of `templates/intake-template.md`. Copy this file to
  `docs/audits/<YYYY-MM-DD>-<class>-<slug>.md` and fill it in. The refusal-gate
  (scripts/validate_hermetization.py, §3 — filed #306) enforces the filename shape
  prospectively; this template is the author-facing skeleton.

  ── Filename grammar (ADR-101 §2 + ratification §R3–R4) ────────────────────────
  `<YYYY-MM-DD>-<class>-<slug>.md`  — or the degenerate `<YYYY-MM-DD>-<class>.md`
  for a pure recurring report with no slug (e.g. `2026-06-14-ecosystem-audit.md`).

  Casing rule (§R4): ALL-LOWERCASE KEBAB-CASE everywhere — date, class, slug.
  No UPPERCASE, no _underscore_, no CamelCase. Sole carve-out: a literal `.` inside
  the slug when it is a meaningful repo/version token (`.dev-knowledge`, `v3.4`);
  a rename there would be lossy (S3-1).

  <class> ∈ the CLOSED 11-class enum (whole-token LONGEST-MATCH, never split on the
  first hyphen — the multi-word tokens require it):
    · semantic:           technical · functional · qa · census · verification
    · recurring/automated: ecosystem-audit · conformance-nightly-digest · changelog-review
    · reviewer-origin:     codex · fresh-eyes
    · incident:            incident-evidence
  Adding a class is a one-line ADR-101 amendment (deliberate), never convention drift.

  <slug>: kebab-case, lowercase, optional (omit for recurring reports). No date-in-slug
  redundancy. `.` allowed only for repo/version tokens.

  The header block above (Title + Class/Date + Source-session + Status) is the minimal
  REQUIRED block for every audit file (§R5). Keep it first.

  Genre reminder (ADR-100): an audit is evidence *about* state — separate lifecycle
  from intake (a request to *change* state, ADR-98). Every claim carries a SHA /
  file:line / URL, or an explicit UNVERIFIED flag.
-->

## Executive so-what

<!-- Bottom line first. What did the audit find, and what should the operator do? -->

## Findings

<!-- One row/section per finding. Each carries: what · evidence (SHA/file:line/URL) ·
     verdict (DONE / OPEN / KILL / NO-ACTION) · disposition. Flat markdown or a
     code-fenced table (render-layer discipline, CLAUDE.md §4). -->

## Recommendations / routing

<!-- Proposals for the operator — filings, closes, kills, routes. Nothing here is
     executed by the audit itself unless the run's mandate says so. -->

## Scope / method

<!-- What was and was not covered; how it was checked; any UNVERIFIED residue. -->
