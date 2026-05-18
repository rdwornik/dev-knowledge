# Action Plan — .dev-knowledge (session-sync 2026-05-18)

## Next session goal

The primary goal is to author `templates/ARCHITECTURE-template.md`, the
canonical shared template mandated by ADR-51 [architecture-doc-convention].
ADR-51 is settled; the template is the immediate, ready-to-execute deliverable.
Before drafting, the next session must inspect (read-only) the existing
`corp-monorepo` `ARCHITECTURE.md` and its C4 Mermaid→SVG diagram pipeline —
ADR-51's open questions section explicitly flags both as required reference input.
The codemap generator output specification is also unresolved; the template may
depend on it, and that dependency must be either resolved or explicitly recorded
as a remaining open item.

The second paired goal is to establish the AGENTS.md convention. `templates/AGENTS-md-template.md`
exists in the repo (10 sections), but there is no decision record (ADR or
equivalent) specifying what the template should implement. The session must
settle the AGENTS.md convention — scope, mandatory content, relationship to
CLAUDE.md — then verify the existing template conforms to that convention (or
update it if it does not). Simultaneously, PLAYBOOK.md and ESSENTIALS.md must
state explicitly that AGENTS.md is Codex-facing and outside the scope of
Claude-oriented handoffs; the handoff templates must no longer present AGENTS.md
as Claude-side handoff content.

The ARCHITECTURE template comes first because its design questions are already
settled in ADR-51. The AGENTS.md convention work may be executed alongside
or immediately after (the two are independent), with both Directives 2 and 3
treated as a coupled pair.

## Action plan

1. **Inspect corp-monorepo reference material, then author `templates/ARCHITECTURE-template.md`.**
   Read (do not write) `corp-monorepo/ARCHITECTURE.md` and its C4 Mermaid→SVG
   pipeline as read-only reference input per ADR-51 open questions. Then draft
   the canonical template encoding the ADR-51 convention: mandatory core
   (bird's-eye purpose statement, codemap placeholder, layer boundaries and
   invariants) plus optional sections; graphical codemap notation for M/L,
   text-only module overview for S. If the codemap generator output spec is
   still undefined after the inspection, record it explicitly as a remaining
   open item in the template's header.
   *Verification:* `templates/ARCHITECTURE-template.md` exists; it encodes the
   ADR-51 mandatory core; the codemap spec dependency is either resolved or
   explicitly noted as open.

2. **Decide the AGENTS.md convention, verify the existing template, and record the decision.**
   `templates/AGENTS-md-template.md` already exists with 10 sections — do NOT
   assume it is absent. Treat the convention itself as undecided (no decision
   record exists). Settle: AGENTS.md scope, mandatory content, relationship to
   CLAUDE.md. Verify whether the existing template conforms to the decided
   convention; update it if it does not. Author a decision record (ADR or
   conversational decision note) for the convention.
   *Verification:* a decision record for the AGENTS.md convention exists;
   `templates/AGENTS-md-template.md` conforms to it.

3. **State the AGENTS.md scope explicitly in PLAYBOOK.md and ESSENTIALS.md,
   and correct the handoff templates.**
   Record that AGENTS.md is Codex-facing and outside the scope of Claude-oriented
   handoffs. Claude-side handoff chats must not treat AGENTS.md as a repo-descriptive
   artifact to narrate or manage. Update `protocols/PLAYBOOK.md`,
   `protocols/ESSENTIALS.md`, and any handoff template files that currently
   present AGENTS.md as Claude-side handoff content.
   *Verification:* PLAYBOOK.md and ESSENTIALS.md state the AGENTS.md scope
   explicitly; no handoff template presents AGENTS.md as Claude-side content.

## Hard Constraints

- **Do NOT write to child repositories.** Per ADR-36 [audit-tool-architecture],
  `.dev-knowledge` has a read-only contract with child repos. Reading
  `corp-monorepo` files as reference is permitted; writing to any child repo
  is not.
- **Do NOT author the AGENTS.md template as if it does not exist.** The file
  `templates/AGENTS-md-template.md` exists with 10 sections. Establish the
  convention, verify conformance, update if needed — do not recreate from scratch.
- **Do NOT author the ARCHITECTURE template before inspecting corp-monorepo.**
  ADR-51 explicitly requires the existing `corp-monorepo` `ARCHITECTURE.md` and
  C4 pipeline to be reviewed as read-only input first.
- **Do NOT commit to `main` without running pre-commit hooks.** All commits go
  through the pre-commit gate.
- **Do NOT recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`.** Both were deleted
  deliberately per Council Simplification 2026-05-16; git history + JOURNAL
  `Changes:` line replace them.

## Narrow scope rules

- Do NOT pull in Kimi K2 model implementation, corp-monorepo implementation
  work, or any other repo's execution work. Those have their own repositories
  and handoffs.
- Do NOT treat any individual repository's AGENTS.md *content* as Claude-side
  handoff material. Building the AGENTS.md *template and convention* (Directive 2)
  is in scope as governance work; narrating or managing AGENTS.md content inside
  a Claude-oriented handoff is not.
- Do NOT edit existing LESSONS.md entries — that file is append-only.
- Do NOT create new top-level markdown files without first checking the README.md
  growth triggers.

## Fallback contingencies

- If the corp-monorepo `ARCHITECTURE.md` read-only inspection reveals that the
  existing document does not align with ADR-51's mandatory core, record the
  discrepancy as a finding for the corp-monorepo universalization effort —
  do not resolve it in this session (that is child-repo work per ADR-36).
- If the codemap generator output spec cannot be resolved within this session,
  record it explicitly as an open item in the template header and in BACKLOG.md —
  do not block the template on an undefined dependency.
- If the AGENTS.md convention debate requires an AI Council vote rather than a
  conversational decision, initiate the Council debate — do not author the
  template against an undecided convention.

## Success criteria

- `templates/ARCHITECTURE-template.md` exists, encodes the ADR-51 convention,
  and the codemap spec dependency is either resolved or explicitly noted as open.
- A decision record for the AGENTS.md convention exists.
- `templates/AGENTS-md-template.md` conforms to the decided convention.
- PLAYBOOK.md and ESSENTIALS.md explicitly state that AGENTS.md is Codex-facing
  and outside Claude-side handoff scope.
- No handoff template presents AGENTS.md as Claude-side handoff content.
- All changes committed with pre-commit hooks passing.
- JOURNAL entry prepended for this session.
