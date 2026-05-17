# ADR-47 — Cross-repo BACKLOG.md organization

Status: Partially superseded — retained as convention, NOT audit-enforced
Date: 2026-05-15 (original); demoted 2026-05-16
Stream: C, governance ADR session B+C
Superseded by: Council Simplification verdict 2026-05-16 (this branch)
Related: ADR-41 (BACKLOG architecture — file mandate), ADR-46 (paired decision — also demoted)

## Status note (2026-05-16 demotion)

This ADR's mandates are withdrawn from automated enforcement:

- The audit check `check_backlog_organization` has been removed from
  `scripts/audit.py`. No `[done]`-token scan, no entry-heading regex, no
  required-fields-per-entry check, no kill-criteria warnings.
- The companion file **`BACKLOG_ARCHIVE.md` is deleted.** Done items leave
  BACKLOG and their record is git history, not a parallel archive file.

What remains, as lightweight convention (no automated enforcement):

- **One file, BACKLOG.md.** Active, cross-session, pending items only.
- **Stream-grouped** with `## Stream <name>` H2 headings if useful at the
  repo's scale. For small repos a flat list is fine.
- **Entry shape, recommended (not enforced):**

  ```
  ### [P{N}] [open] <title>
  - **What:** <one paragraph>
  - **Why:** <one paragraph>
  - **Added:** YYYY-MM-DD
  - **Status:** open
  ```

  Other fields permitted. Use what the entry needs.
- **Done items** simply leave BACKLOG. Their trace is in the commit history
  for the change that closed them. No ceremonial archive.
- **Abandoned items** — when an item is dropped without action and the
  reasoning matters — get a short note in `docs/decisions/` (an ADR or a
  decision-note), NOT a line in JOURNAL or a tombstone in BACKLOG.

## Why demoted

Two-file state (BACKLOG + BACKLOG_ARCHIVE), entry-format validation, and
per-stream kill criteria (300-line file ceiling, 15-items-per-stream,
33%-cross-stream) were designed for a multi-team ecosystem to prevent
context dilution and stream sprawl. For a solo developer with a single
co-reader LLM, the active file is small enough that the dilution risk
doesn't materialise, and the ceremony of moving items between files
exceeds the cognitive savings.

The retained convention — one file, recommended entry shape, git history
as the done-record — gives the LLM a clean handoff anchor without the
two-file dance.

## Original decision (for historical reference)

The original ADR — see git history at the commit prior to the 2026-05-16
demotion — specified Stream-grouped BACKLOG + two-file state architecture
(Option C-2): active `BACKLOG.md` for `[open]`/`[superseded]`, append-only
`BACKLOG_ARCHIVE.md` for `[done]`/`[abandoned]`, universal entry format
with 4 required fields, three kill criteria (file >300 lines,
stream >15 open, cross-stream >33% of open). All enforcement withdrawn
2026-05-16.

## References

- Council research transcript: `docs/decisions/transcripts/council-out-20260515_185730-research-research-brief-cross-repo-backlog-organization-res.md`
- Council pick transcript: `docs/decisions/transcripts/council-out-20260515_194305-pick-council-pick-cross-repo-backlog-organization-decis.md`
- ADR-41 (BACKLOG architecture — file mandate this ADR refined)
- ADR-46 (paired dated-entries decision — also demoted 2026-05-16)
