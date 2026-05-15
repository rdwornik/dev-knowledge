# Governance Essences — ai-council Cleanup Session

<!-- scope: meta -->

This file contains the ADRs driving this cleanup session. ADR-46 and ADR-47 are
included in full as the binding standards. ADR-36 and ADR-31 are included as
operational excerpts explaining the audit tool's authority and read-only boundary.

Full ADR files live at:
- `C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\decisions\ADR-46-cross-repo-dated-entries-format.md`
- `C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\decisions\ADR-47-cross-repo-backlog-organization.md`
- `C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\decisions\ADR-36-audit-tool-architecture.md`
- `C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\decisions\ADR-31-authority-model.md`

---

# ADR-46 — Cross-repo dated-entries format (FULL)

Status: Accepted
Date: 2026-05-15

## Decision

Adopt a **lightweight shared envelope with file-specific payloads** for
LESSONS.md, JOURNAL.md, and CHANGELOG.md across all ecosystem repos.

### Universal envelope (all three files)

- **Date format:** ISO 8601 `YYYY-MM-DD` only. No locale-dependent or
  human-readable variants.
- **Outer heading:** `## YYYY-MM-DD` (H2) as the primary per-day record
  anchor. ISO date MUST appear in the heading text.
- **Inner heading:** `### Topic` (H3) optional, used for per-event
  subdivision within a per-day record.
- **Ordering:** Reverse-chronological. **Prepend-latest is mandatory**
  for all active dated-entries files. New entries are inserted at the
  top of the entry list, directly under the file's intro/frontmatter,
  before existing entries.
- **Scope metadata:** ADR-27 HTML comments (`<!-- scope: X -->`)
  remain the single authoritative source for scope.

### File-specific payloads

#### LESSONS.md

- 6-field canonical schema preserved (ADR-29, grandfathered):
  `### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]`
- LESSONS uses single-line entry headings as the per-event record;
  the outer `## YYYY-MM-DD` grouping is OPTIONAL when entries within
  the same day share no logical grouping.
- File-level `<!-- scope: hybrid -->` directly under H1 (per ADR-29
  amendment 2026-04-24).

#### JOURNAL.md

- Outer `## YYYY-MM-DD` mandatory per-day record OR `### YYYY-MM-DD —
  <session topic>` (H3) when the file's convention scopes entries to
  per-session rather than per-day.
- Body: free-prose bullets under topic. No required field schema.

#### CHANGELOG.md

- **Keep-a-Changelog semantics preserved.** `## YYYY-MM-DD` as the
  outer date anchor (or `## [Version] - YYYY-MM-DD` if the repo uses
  semantic versioning).
- Inner `### Added` / `### Changed` / `### Fixed` / `### Deprecated` /
  `### Removed` / `### Security` / `### Verified` / `### Notes` for
  semantic grouping.

### Per-repo flexibility

- Universal envelope is **not** subject to per-repo override.
- Per-repo deviations from the file-specific payload must be ratified
  by an ADR; silent drift is prohibited.

### Enforcement

Deterministic validator (`scripts/audit.py check_dated_entries_format`):
1. Verify ADR-27 scope tag present at file head
2. Verify each `## ` heading matches `^## \d{4}-\d{2}-\d{2}( |$)` regex
3. Verify ISO dates in headings are reverse-chronological
4. File-specific sniff tests per payload schema

### Migration decisions for ai-council (LOCKED)

**LESSONS.md:** `## Session: Phase 1 Foundation (2026-02-21)` →
`## 2026-02-21`. Session label moves to body as `**Session:** Phase 1 Foundation`.
No content changes to 6-field entry bodies.

**JOURNAL.md:** Move `2026-03-15` entry block to its correct
reverse-chrono position. No content changes to entry body text.

---

# ADR-47 — Cross-repo BACKLOG organization (FULL)

Status: Accepted
Date: 2026-05-15

## Decision

Adopt **Stream-grouped BACKLOG with a two-file state architecture**
for all ecosystem repos at tier M+ that have a BACKLOG.md per ADR-41.

### Structure

#### Active file: `BACKLOG.md`

- Contains **only `[open]` and `[superseded]` items.**
- `[done]` items are extracted to `BACKLOG_ARCHIVE.md`.
- Top-level structure: `## Stream A: <name>`, `## Stream B: <name>`,
  ..., `## Cross-stream / Ecosystem`.

#### Archive file: `BACKLOG_ARCHIVE.md`

- Append-only. **`[done]` and `[abandoned]` items only.**
- Top-level structure mirrors BACKLOG.md.
- Within each Stream, **reverse-chronological by close date** (newest
  archived item at the top, per ADR-46 prepend-latest mandate).
- Each archived entry preserves original entry block verbatim plus
  a `**Archived:** YYYY-MM-DD` line.

### Entry format (universal)

```
### [P{N}] [open] <title>
- **What:** <one paragraph>
- **Why:** <one paragraph>
- **Vision ref:** <VISION.md section or ADR-NN reference>
- **Added:** YYYY-MM-DD by <author> (<context>)
- **Status:** open
```

Required fields: `What`, `Why`, `Added`, `Status`.

### Priority semantics

- **P1** — active priority. Currently being worked or queued for the
  next session. Generally fewer than 5 per stream.
- **P2** — queued. Not yet picked up; sequenced behind P1 items.
- **P3** — someday / opportunistic. May never close.

### Status tags

`[open]`, `[done]`, `[superseded]`, `[abandoned]`. **Exactly four. No others.**

`[blocked]` is **NOT** in the vocabulary. Blocked state is expressed as
`[open]` with `**Blocked:** <reason>` body annotation.

### Kill criteria

ADR review triggers if any repo's BACKLOG.md:
- Active file exceeds **300 lines**
- Any single stream section exceeds **15 open items**
- `Cross-stream / Ecosystem` section exceeds **33%** of total open items

### Enforcement (`scripts/audit.py check_backlog_organization`)

1. **Fatal:** `[done]` token in BACKLOG.md outside fenced code blocks
2. **Fatal:** `BACKLOG_ARCHIVE.md` missing when `BACKLOG.md` present
3. **Fatal:** entry heading does not match `### [P{N}] [open|superseded] <title>`
4. **Fatal:** entry block lacks required fields (`What`, `Why`, `Added`, `Status`)
5. **Warn:** kill-criteria triggers

### Migration decisions for ai-council (LOCKED)

**`[blocked]` → `[open]` + body annotation:** All occurrences of
`[blocked]` in BACKLOG.md headings must be changed to `[open]`, with
a `**Blocked:** <reason>` bullet added to the entry body.

**`Status:` field addition:** All entries missing `**Status:** open`
must have it added.

**BACKLOG_ARCHIVE.md creation:** File must be created (empty scaffold
with scope tag and append-only header). No items to archive currently
(ai-council has no `[done]` entries in BACKLOG.md as of 2026-05-15).

---

# ADR-36 — Audit Tool Architecture (Operational Excerpt)

Status: Accepted (2026-04-30)

## Key decisions relevant to this cleanup

**`.dev-knowledge` is the ecosystem auditor.** The audit tool lives in
`.dev-knowledge/scripts/audit.py`. It reads child repos (ai-council, etc.)
but **never writes to them.** Hard constraint: tool writes ONLY to
`.dev-knowledge/` paths.

**ai-council is in the immediate audit cohort** (per ADR-33
universalization). ai-council and corp-monorepo are the first repos
subject to audit compliance checks.

**Audit findings route to repo owners.** The 2026-05-15 ecosystem audit
report (`docs/audits/2026-05-15-ecosystem-audit.md`) surfaces ai-council
FAIL findings. This handoff bundle is the routing mechanism — it delivers
the audit findings to ai-council's Claude Code session for remediation.

**Cross-session verification:** After ai-council cleanup, the `.dev-knowledge`
operator re-runs `python scripts/audit.py run` to confirm compliance. The
audit tool is the verification oracle — it confirms the fixes, not the
ai-council session itself.

---

# ADR-31 — Authority Model (Operational Excerpt)

Status: Accepted (2026-04-27)

## Key decisions relevant to this cleanup

**1B: Prescriptive with conformance audit.** `.dev-knowledge` is the
binding source of cross-repo prescriptions. Prescriptions (ADR-46,
ADR-47) are binding on all M+ tier repos.

**Universalization principle (operationalized here):** When a child repo
deviates from a `.dev-knowledge` standard, the child repo migrates to the
standard. The standard is not amended to accommodate the deviation.

This governs both migration decisions in this cleanup:
- Decision A (`[blocked]` → `[open]`): ai-council conforms to ADR-47's
  4-status vocabulary — ADR-47 is not amended to add `[blocked]`
- Decision B (session-numbered envelope → ISO): ai-council conforms to
  ADR-46's ISO date requirement — ADR-46 is not amended to grandfather
  session-numbered headings

**Enforcement mechanism:** Out-of-band, centralized, read-only audit tool
(manual invocation). The `.dev-knowledge` audit is the conformance gate.
