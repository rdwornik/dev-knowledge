# Action Plan — ai-council Cleanup Session

<!-- scope: meta -->

## Next session goal

Bring ai-council into full compliance with ADR-46 (dated-entries format) and
ADR-47 (BACKLOG organization). All 5 FAIL checks in the 2026-05-15 ecosystem
audit must pass on re-audit from `.dev-knowledge`.

## Rationale

ai-council is a consumer of the `.dev-knowledge` universal standard. The audit
tool (Session E) surfaced 5 FAIL checks. The migration decisions are locked
(universalization principle): ai-council conforms to the standard — the standard
is not amended for ai-council's prior conventions. The fixes are bounded and
mechanical: heading rename, block reorder, status field additions, archive file
creation. No semantic content is changed.

---

## Directives

### Directive 1 — Pre-flight

Before any edits:

```
git rev-parse HEAD
git status --porcelain
```

Expected HEAD: `0f069554b894802504aa4e5ce140b1d481ae9ec8`
Expected: working tree clean.

If HEAD mismatch: STOP. Report both SHAs to operator. Do not proceed until
operator confirms.

Read the following files in ai-council before starting work:
- `CLAUDE.md` — repo standards and conventions
- `LESSONS.md` — understand current structure
- `JOURNAL.md` — understand current structure
- `BACKLOG.md` — understand current structure

Read the following files in this bundle for ADR authority:
- `05_GOVERNANCE_ESSENCES.md` — ADR-46 + ADR-47 full text

---

### Directive 2 — LESSONS.md: migrate session-numbered envelope to ISO

**Problem:** `## Session: Phase 1 Foundation (2026-02-21)` is a non-ISO H2 heading.
ADR-46 requires `## YYYY-MM-DD` as the outer heading.

**Action:**
1. Read LESSONS.md
2. Find the heading: `## Session: Phase 1 Foundation (2026-02-21)`
3. Replace heading with: `## 2026-02-21`
4. Immediately under the new heading, add a line:
   `**Session:** Phase 1 Foundation`
   (This preserves the session label as prose context in the body, per the locked migration decision.)
5. No other changes to LESSONS.md — existing 6-field single-line entries are
   ADR-29 grandfathered and DO NOT require modification.

**Verify:** `## Session:` no longer appears anywhere in LESSONS.md.

**Commit:** `docs(lessons): migrate session envelope to ISO format per ADR-46 [cleanup]`

---

### Directive 3 — JOURNAL.md: restore reverse-chronological ordering

**Problem:** The `2026-03-15` entry block appears after 2026-05-12 entries,
violating ADR-46 reverse-chrono ordering.

**Action:**
1. Read JOURNAL.md in full
2. Locate the entry block starting with `## 2026-03-15` (or the equivalent
   heading — verify the exact heading text before editing)
3. Move the entire entry block (heading + all body content until the next `## ` heading)
   to its correct reverse-chronological position: after all entries with dates later
   than 2026-03-15, and before any entries with dates earlier than 2026-03-15
4. Verify the final ordering is strictly reverse-chronological (newest entry first)

**Verify:** Dates in H2 headings descend from top to bottom of file.

**Commit:** `docs(journal): restore reverse-chrono ordering per ADR-46 [cleanup]`

---

### Directive 4 — BACKLOG.md: create BACKLOG_ARCHIVE.md

**Problem:** ADR-47 requires BACKLOG_ARCHIVE.md to exist alongside BACKLOG.md.
ai-council has no `[done]` entries to archive — the archive file starts empty.

**Action:**
1. Create `BACKLOG_ARCHIVE.md` at the repo root with the following content:

```markdown
# BACKLOG_ARCHIVE — ai-council

<!-- scope: meta -->

<!-- schema: ADR-47 | append-only | done and abandoned items only -->

Archived closed items. Append-only. Do not edit existing entries.
Items are moved here from BACKLOG.md when closed (status: done or abandoned).
Reverse-chronological within each stream section.

---
```

2. No items to migrate from BACKLOG.md (no `[done]` entries currently exist).

**Commit:** `chore(backlog): create BACKLOG_ARCHIVE.md scaffold per ADR-47 [cleanup]`

---

### Directive 5 — BACKLOG.md: migrate `[blocked]` + add `Status:` to all entries

**Problem (two combined in one directive):**

A. `### [P1] [blocked] Step 6 Phase 3 conditional implementation` — `[blocked]` not in
   ADR-47 vocabulary. Must become `[open]` with body annotation.

B. All 11 entries missing `**Status:** <value>` bullet (required field per ADR-47).

**Action for (A):**
1. Change heading from `### [P1] [blocked] Step 6 Phase 3 conditional implementation (ADR-01 amendment + Branch A/B)`
   to `### [P1] [open] Step 6 Phase 3 conditional implementation (ADR-01 amendment + Branch A/B)`
2. Add to the entry body (after the `**Why:**` bullet, before or after `**Added:**`):
   `**Blocked:** Depends on Step 5 smoke test data — cannot proceed until operator scores ~15 historical transcripts with synthesis rubric.`

**Action for (B) — add `**Status:** open` to all 11 entries:**

Add `- **Status:** open` as the last bullet in each entry block (after `**Added:**`).
Apply to all entries listed below:

1. `### [P1] [open] Step 5 smoke test execution (Gemini synth scoring on ~15 transcripts)`
2. `### [P1] [open] Step 6 Phase 3 conditional implementation` (after (A) fix above)
3. `### [P1] [open] Codify cost-optimization principle in ADR-01 amendment`
4. `### [P2] [open] openai_deep_research integration test gap`
5. `### [P2] [open] CI enforcement of hyphen-only separator rule (ADR-34)`
6. `### [P3] [open] ADR-34 timestamp-underscore case in council-out emitter output`
7. `### [P3] [open] DeepSeek replacement decision`
8. `### [P3] [open] Synthesis quality rubric refinement — faithfulness sub-clarification`
9. `### [P3] [open] AGENTS.md addition per ADR-28`
10. `### [P3] [open] ADR-02 amendment (panelist/synthesizer overlap policy)`
11. `### [P3] [open] Cross-stream P2 — handshake = 1 round trip codification`

**Verify:** No `[blocked]` appears in BACKLOG.md. All entries have `**Status:**` bullet.

**Commit:** `chore(backlog): migrate [blocked] → [open] + add Status fields per ADR-47 [cleanup]`

---

### Directive 6 — ai-council BACKLOG / CHANGELOG / JOURNAL close-out

After directives 2–5 are committed:

1. **CHANGELOG:** add an entry documenting this cleanup session. Use Keep-a-Changelog
   format (`## YYYY-MM-DD` outer heading, `### Changed` inner group):
   ```
   ## 2026-05-15
   ### Changed
   - LESSONS.md: session-numbered envelope migrated to ISO date format per ADR-46
   - JOURNAL.md: reverse-chronological ordering restored per ADR-46
   - BACKLOG.md: [blocked] migrated to [open] + Blocked annotation; Status field added to all 11 entries per ADR-47
   - BACKLOG_ARCHIVE.md: created per ADR-47 (empty initial scaffold)
   ```

2. **JOURNAL:** prepend a new entry:
   ```
   ## 2026-05-15 — ADR-46+47 compliance cleanup (cross-repo handoff)

   **Did:**
   - LESSONS.md: migrated ## Session: Phase 1 Foundation (2026-02-21) → ## 2026-02-21 + Session label in body
   - JOURNAL.md: moved 2026-03-15 entry to correct reverse-chrono position
   - BACKLOG.md: [blocked] → [open] + Blocked annotation on Step 6; Status field added to all 11 entries; BACKLOG_ARCHIVE.md created
   - Driven by .dev-knowledge cross-repo audit (2026-05-15-ecosystem-audit.md) + handoff bundle

   **Result:** ai-council compliant with ADR-46 + ADR-47. Re-audit from .dev-knowledge expected to clear all 5 FAIL checks.

   **Next:** Operator runs `python scripts/audit.py run` in .dev-knowledge to confirm. Stream B P1 items flip to [done] on clean audit.
   ```

3. **Commit:** `docs(changelog): ADR-46+47 compliance cleanup [cleanup]`
4. **Commit:** `docs(journal): 2026-05-15 ADR-46+47 compliance cleanup [cleanup]`

---

### Directive 7 — Fill 09_EXECUTION_EVIDENCE.md and signal completion

Fill the execution evidence template at:
`C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\handoffs\2026-05-15-ai-council-cleanup\09_EXECUTION_EVIDENCE.md`

Fields to fill:
- Execution date
- ai-council HEAD SHA after all commits (run `git rev-parse HEAD` in ai-council)
- Commits made (list with SHA + message)
- Files changed (list)
- Blockers encountered (if any)
- Verification note ("Re-audit requested from .dev-knowledge operator")

Signal to operator: "Execution complete. Return to .dev-knowledge and run `python scripts/audit.py run`."

---

## Hard constraints

- **Read-only on .dev-knowledge.** Do NOT write any file to `.dev-knowledge`. The bundle
  files are read-only context. All writes go to ai-council only.
- **Migration decisions are locked.** Do NOT re-debate `[blocked]` vs ADR-47 amendment.
  Do NOT re-debate session-numbered envelope vs ISO. Both are decided per universalization
  principle. Implement as specified.
- **No content changes in payload bodies.** LESSONS.md 6-field entry bodies are unchanged.
  JOURNAL.md entry body text is unchanged (only the block position moves). BACKLOG.md entry
  bodies gain `**Status:**` and `**Blocked:**` bullets only.
- **Do NOT push to remote.** Commits stay local until operator reviews.
- **Do NOT merge to ai-council main** without explicit operator approval.
- **Do NOT touch ai-council source code**, tests, config, or any file outside LESSONS.md,
  JOURNAL.md, BACKLOG.md, BACKLOG_ARCHIVE.md, CHANGELOG.md.
- **adr38_baseline WARN is out of scope.** ARCHITECTURE.md missing is a separate tracked
  item — do not create it in this session.

---

## Narrow scope rules

- Only the 5 FAIL checks are in scope. The WARN is explicitly excluded.
- Only the files listed in the directives may be modified.
- Directives execute in order (1 → 7). Do not skip or reorder.
- If an unexpected file state is found (e.g., JOURNAL.md has additional non-ISO headings
  not surfaced in the audit), surface to operator before editing.
