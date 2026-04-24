# ADR-29: LESSONS.md Grandfathering Under Scope Tagging

**Status:** Accepted
**Date:** 2026-04-21
**Type:** Binding — derivative of ADR-27 Council decision
**Parent decision:** ADR-27 (Council #27 scope tagging)

## Context

ADR-27 mandates `<!-- scope: X -->` tags on all sections. LESSONS.md is append-only (CLAUDE.md rule: "NEVER edit old entries. NEVER delete. Only append new entries at the bottom"). Phase 2 audit lists LESSONS.md as a single section "Entries" with `[hybrid]` tag because existing 123 lines mix `prompt-craft` + `token-optimization` (llm), `gotcha` + `architecture` (dev), `process` + `tooling` (both) categories.

Retroactive per-entry tagging would edit existing content, violating append-only. Council #27 brief flagged this as an open question with three options: grandfather, explicit rule exception, or split.

## Decision

**Grandfather existing entries. Tag going forward only.**

### Specific rules

1. **Existing 123 lines remain untouched.** No per-entry tags added retroactively. No reformatting of the entry format.

2. **New entries include inline scope tag** as part of the entry format. Updated format:

   ```
   ### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]
   ```

   Where `[scope: X]` uses the ADR-27 vocabulary: `dev | llm | hybrid | runtime | meta`.

3. **File-level section tag.** The LESSONS.md "Entries" section gets a single file-level `<!-- scope: hybrid -->` comment (consistent with Phase 2 audit classification). This satisfies the pre-commit hook's section-tag requirement. Entry-level scope lives within entries per rule 2.

   **2026-04-24 amendment:** insertion point is directly under H1 (`# Lessons Learned — Append-Only Log`), not under `## Entries`. Rationale: validator uses 3-line H1 detection window; H1 placement satisfies the "file-level" intent more literally than `## Entries` placement (which fell outside the detection window). No change to decision intent — only insertion point clarified.

4. **Append-only preserved.** No exception to append-only rule is created. Retroactive tagging would require such an exception; grandfathering sidesteps it entirely.

### Consequences

- **Pre-ADR-27 entries are unfilterable by scope.** Acceptable: entries older than the tagging architecture predate the filter concept.
- **New-entry filtering works from first tagged entry forward.** `grep "scope: llm" LESSONS.md` returns all LLM-scoped lessons added after ADR-27 adoption.
- **Format migration is one-time.** The next entry written after ADR-27 acceptance uses the new format. No bulk migration session.

## Rejected alternatives

- **Explicit rule exception (one-time retroactive migration, documented as ADR):** rejected because append-only is a load-bearing invariant; carving an exception weakens the rule for future edge cases.
- **Split going forward (LESSONS_DEV.md / LESSONS_LLM.md):** rejected because it fragments the single-log property without clear read-time benefit; current LESSONS.md is short (123 lines) and single-file grep serves filtering adequately.

## Consequences — operational

- Pre-commit hook treats LESSONS.md specially: satisfied by file-level `<!-- scope: hybrid -->` under the "Entries" section header. Hook does NOT validate per-entry scope tags (those are within the entry format, not a separate hook concern).
- The entry-format change is documented in ESSENTIALS.md (lesson-extraction section) and PLAYBOOK Section 4 during Stream A rollout. Not in this ADR.

## References

- ADR-27: scope tagging architecture (parent decision)
- CLAUDE.md: append-only rule for LESSONS.md
- Phase 2 audit LESSONS.md section: `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`
