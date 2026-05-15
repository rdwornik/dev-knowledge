# PLAYBOOK Reference — ai-council Cleanup Session

<!-- scope: meta -->

> The full PLAYBOOK.md (2,441 lines) lives at:
> `C:\Users\1028120\Documents\Dev\.dev-knowledge\protocols\PLAYBOOK.md`
>
> This file contains the sections most relevant to this cleanup session.
> For the full methodology reference, read the full PLAYBOOK if needed.

---

## Commit conventions (relevant to this session)

From PLAYBOOK §Commit conventions:

- **Format:** `<type>(<scope>): <description> [<tag>]`
- **Types:** `feat`, `fix`, `docs`, `chore`, `test`, `refactor`
- **Scope:** file or area affected (e.g., `lessons`, `journal`, `backlog`, `changelog`)
- **Tag:** BACKLOG stream tag (e.g., `[cleanup]`, `[P1]`)

Examples for this session:
```
docs(lessons): migrate session envelope to ISO format per ADR-46 [cleanup]
docs(journal): restore reverse-chrono ordering per ADR-46 [cleanup]
chore(backlog): create BACKLOG_ARCHIVE.md scaffold per ADR-47 [cleanup]
chore(backlog): migrate [blocked] → [open] + add Status fields per ADR-47 [cleanup]
docs(changelog): ADR-46+47 compliance cleanup [cleanup]
docs(journal): 2026-05-15 ADR-46+47 compliance cleanup [cleanup]
```

---

## LESSONS.md authoring (per ADR-29 + ADR-46)

From PLAYBOOK §File conventions:

```
### YYYY-MM-DD | [source] | [lesson title] | [category] | [scope: X] | [action taken]
```

- ADR-29: 6-field single-line heading is the canonical schema (grandfathered)
- ADR-46: outer `## YYYY-MM-DD` grouping is OPTIONAL when entries within the same day share no logical grouping
- This session: LESSONS.md already has 6-field entries; only the outer `## Session: Phase 1 Foundation (2026-02-21)` heading requires migration to `## 2026-02-21`
- Do NOT rewrite any 6-field entry bodies

---

## JOURNAL.md authoring (per ADR-46)

From PLAYBOOK §File conventions:

- Outer heading: `## YYYY-MM-DD — <session topic>` OR `## YYYY-MM-DD` (both forms accepted per ADR-46)
- Ordering: **prepend-latest mandatory** — newest entry at top
- Body: free-prose bullets under topic. No required field schema.

---

## BACKLOG.md authoring (per ADR-41 + ADR-47)

From PLAYBOOK §BACKLOG management:

- **Active file (BACKLOG.md):** `[open]` and `[superseded]` items only
- **Archive file (BACKLOG_ARCHIVE.md):** `[done]` and `[abandoned]` items only; append-only
- **Entry format:**
  ```
  ### [P{N}] [open] <title>
  - **What:** <one paragraph>
  - **Why:** <one paragraph>
  - **Added:** YYYY-MM-DD by <author> (<context>)
  - **Status:** open
  ```
- **Status vocabulary:** `[open]`, `[done]`, `[superseded]`, `[abandoned]` — exactly 4
- **No other status tags:** `[blocked]` is NOT in the vocabulary

---

## CHANGELOG.md authoring (per ADR-46 + Keep-a-Changelog)

From PLAYBOOK §File conventions:

- Outer heading: `## YYYY-MM-DD` (reverse-chronological, prepend-latest)
- Inner grouping: `### Added`, `### Changed`, `### Fixed`, `### Deprecated`, `### Removed`, `### Security`, `### Verified`, `### Notes`
- Keep-a-Changelog 1.1.0 semantics preserved

---

## Scope tagging (per ADR-27)

All section headings in living files require a scope tag as an HTML comment directly under the heading:

```
## Section Title
<!-- scope: meta -->
```

Tag vocabulary: `dev | llm | hybrid | runtime | meta`

New BACKLOG_ARCHIVE.md scaffold must have `<!-- scope: meta -->` under H1.

---

## Session boundary rules (per ADR-42)

- Do NOT push to remote without operator approval
- Do NOT merge to main without explicit operator `merge approved`
- Fill `09_EXECUTION_EVIDENCE.md` at session end before signaling completion
- Working tree must be clean before signaling done
