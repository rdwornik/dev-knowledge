# State of Play — ai-council Cleanup Handoff

<!-- scope: meta -->

## What landed in .dev-knowledge

### ADR-46 + ADR-47 ratified — `ecc3211` (2026-05-15)

- **ADR-46** (`docs/decisions/ADR-46-cross-repo-dated-entries-format.md`): universal
  lightweight envelope for LESSONS.md, JOURNAL.md, CHANGELOG.md. ISO `YYYY-MM-DD`
  outer heading, reverse-chronological prepend, file-specific payloads preserved.
- **ADR-47** (`docs/decisions/ADR-47-cross-repo-backlog-organization.md`): stream-grouped
  BACKLOG + two-file state (BACKLOG.md = open only; BACKLOG_ARCHIVE.md = done/abandoned).
  Entry format: `### [P{N}] [open|superseded] <title>` heading + `What/Why/Added/Status`
  required fields. Status vocabulary: `[open]`, `[done]`, `[superseded]`, `[abandoned]`
  — four statuses, no others.

### Audit tool ADR-46+47 checks — `4344c65` (2026-05-15)

`scripts/audit.py` extended with:
- `check_dated_entries_format` — validates ISO H2 envelope, reverse-chrono ordering,
  file-specific payload sniff tests (per ADR-46)
- `check_backlog_organization` — validates BACKLOG_ARCHIVE.md present, heading pattern,
  required fields, no `[done]` in active file (per ADR-47)
- `scripts/backlog_archive.py` — deterministic extraction script for done-item archival
- First dogfood run on 2026-05-15 produced `docs/audits/2026-05-15-ecosystem-audit.md`

### .dev-knowledge own cleanup (Session D cleanup — prerequisite for this handoff)

Completed before this bundle was generated. Covered: BACKLOG_ARCHIVE.md created,
done items extracted, CHANGELOG ordering fixed, LESSONS.md headings corrected.

---

## What's pending in ai-council

### Audit findings (source: `docs/audits/2026-05-15-ecosystem-audit.md`)

Path: `C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\audits\2026-05-15-ecosystem-audit.md`

ai-council check results (2026-05-15):

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present |
| `adr38_baseline` | WARN | ARCHITECTURE.md missing (optional at M-tier, required at L-tier only) |
| `claude_md` | PASS | CLAUDE.md present |
| `dated_entries_lessons` | **FAIL** | `## Session: Phase 1 Foundation (2026-02-21)` — non-ISO H2 heading |
| `dated_entries_journal` | **FAIL** | Ordering violation: `2026-03-15` appears before `2026-05-12` (not reverse-chrono) |
| `dated_entries_changelog` | PASS | Envelope OK |
| `backlog_organization` | **FAIL** | BACKLOG_ARCHIVE.md missing |
| `backlog_organization` | **FAIL** | `[blocked]` heading — not in ADR-47 vocabulary |
| `backlog_organization` | **FAIL** | 11 entries missing required `Status:` field |

**In scope for cleanup: all 5 FAIL items.** The WARN (ARCHITECTURE.md) is out of scope
for this session — it is tracked separately in ai-council BACKLOG.

### Specific items for the cleanup session

**LESSONS.md:**
- File has one non-ADR-46-compliant outer heading: `## Session: Phase 1 Foundation (2026-02-21)`
- All other content appears as 6-field single-line entries (ADR-29 schema, grandfathered)
- Fix: rename outer heading to `## 2026-02-21`; move session label to first bullet under
  the heading as `**Session:** Phase 1 Foundation` prose line

**JOURNAL.md:**
- Entry `## 2026-03-15 | Phase 1 foundation` appears at the bottom of the file
  (after all 2026-05-11 and 2026-05-12 entries), violating reverse-chrono ordering
- Fix: move the `2026-03-15` entry block to its correct position — after all entries
  dated later than 2026-03-15 (i.e., near the bottom, but before any entries earlier
  than 2026-03-15 if any)

**BACKLOG.md:**
- BACKLOG_ARCHIVE.md: does not exist — must be created (can be empty scaffold)
- `[blocked]` heading on `### [P1] [blocked] Step 6 Phase 3 conditional implementation`:
  `[blocked]` is not in ADR-47 vocabulary. Fix: `[open]` + `**Blocked:** <reason>` in body
- All 11 entries lack `**Status:** <value>` bullet:
  - Step 5 smoke test → `**Status:** open`
  - Step 6 Phase 3 → `**Status:** open` (after [blocked] migration)
  - Codify cost-optimization → `**Status:** open`
  - openai_deep_research integration test gap → `**Status:** open`
  - CI enforcement of hyphen-only separator rule → `**Status:** open`
  - ADR-34 timestamp-underscore case → `**Status:** open`
  - DeepSeek replacement decision → `**Status:** open`
  - Synthesis quality rubric refinement → `**Status:** open`
  - AGENTS.md addition per ADR-28 → `**Status:** open`
  - ADR-02 amendment → `**Status:** open`
  - Cross-stream P2 handshake codification → `**Status:** open`

---

## Migration decisions locked

Both decisions are locked per the universalization principle (ai-council conforms to
standard; standard is not amended to accommodate deviation). The ai-council Claude Code
session must implement these decisions, not re-debate them.

### Decision A: `[blocked]` → `[open]` + body annotation

**Rationale:** `[blocked]` is not in ADR-47's four-status vocabulary
(`open / done / superseded / abandoned`). Adding a fifth status for one repo's edge case
violates cross-repo consistency. The semantic is preserved via body annotation.

**Implementation:**
- Heading: `### [P1] [open] Step 6 Phase 3 conditional implementation (ADR-01 amendment + Branch A/B)`
- Add to body: `**Blocked:** Depends on Step 5 smoke test data. Cannot proceed until operator runs smoke test and scores results.`

### Decision B: session-numbered envelope → ISO date format

**Rationale:** `## Session: Phase 1 Foundation (2026-02-21)` does not pass the
`^## \d{4}-\d{2}-\d{2}` regex required by ADR-46. The session label carries context
value — it is preserved in the entry body, not discarded.

**Implementation:**
- Outer heading: `## 2026-02-21`
- First line under heading (as prose bullet or bold line): `**Session:** Phase 1 Foundation`

---

## Architect rationale

ai-council is a **consumer** of the `.dev-knowledge` standard, not a co-author.
When the standard evolves (ADR-46 + ADR-47), ai-council migrates to comply.

The four failing checks are bounded, mechanical, and safe to fix without semantic risk:
- LESSONS.md: one heading rename + prose line addition — no content changes
- JOURNAL.md: block reorder — no content changes
- BACKLOG.md: status field additions + one heading fix + archive file creation — no entries removed

The `adr38_baseline` WARN (ARCHITECTURE.md missing) is explicitly out of scope: it is
tracked in ai-council BACKLOG (Governance stream, P3) and requires a separate decision.

---

## Cross-session verification flow

1. ai-council Claude Code session executes directives, commits, does NOT push
2. Operator signals completion (fills `09_EXECUTION_EVIDENCE.md`)
3. Operator returns to `.dev-knowledge` and runs:
   ```
   python scripts/audit.py run
   ```
4. Expected: ai-council `dated_entries_lessons`, `dated_entries_journal`, and
   `backlog_organization` all PASS
5. On clean re-audit: `.dev-knowledge` BACKLOG Stream B P1 ai-council items → `[done]`
6. Session D declared complete
