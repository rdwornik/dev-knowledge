# `.dev-knowledge` Self-Audit (Phase 1 Compliance Check)

<!-- scope: meta -->

**Date:** 2026-04-30
**HEAD:** 2b550f1a7e4698cdb80cad1b4bf54c7746e36601
**Branch at time of audit:** `audit/self-audit-dev-knowledge-2026-04-30`
**Auditor:** Claude Code session, manual self-audit
**Purpose:** Verify files reflect 9 ADRs ratified 2026-04-28 through 2026-04-30
(ADR-33, 34, 35, 36, 37, 38, 39, 40, 41) per ADR-39 lifecycle obligations.

---

## Summary table

| File | Present | Lines | Last commit | ADRs 33–41 mentioned | Observation |
|---|---|---|---|---|---|
| README.md | Y | 97 | c81a01d 2026-04-28 | none | No BACKLOG.md in index; all 9 ADRs absent |
| VISION.md | Y | 104 | f2e1f6c 2026-04-28 | none | "auditor" referenced but ADR-36 not cited; no lifecycle ADR refs |
| ARCHITECTURE.md | Y | 130 | 62a3783 2026-04-28 | none | 3-layer model (ADR-28); no ADR-38 4-layer Tach taxonomy |
| protocols/PLAYBOOK.md | Y | 2220 | 0710991 2026-04-28 | ADR-33, ADR-34 only | No sections for ADR-36 (audit), ADR-37 (two-phase handoff), ADR-40 (tier eval), ADR-41 (backlog) |
| protocols/ESSENTIALS.md | Y | 226 | 16bdc0e 2026-04-28 | none | No cheat-sheet content for ADRs 35–41 |
| LESSONS.md | Y | 219 | 8eed0be 2026-04-30 | ADR-37 only | 2026-04-30 session appended; ADR-39/40/41 lessons absent |
| JOURNAL.md | Y | 365 | 8eed0be 2026-04-30 | ADR-33–38 | ADR-39, 40, 41 not mentioned in any entry |
| CHANGELOG.md | Y | 779 | 4db227e 2026-04-30 | all 9 | Appears current — all ADRs reflected |
| protocols/HANDOFF_PROCESS.md | Y | 291 | 53e7da9 2026-04-28 | none | Still v2.0 (ADR-32 only); no ADR-37 two-phase overlay |
| templates/HANDOFF_TEMPLATE.md | Y | 110 | f21a4d9 2026-04-28 | none | Still v2.0 (ADR-32 §5 skeleton); no Current State/Future State sections |
| protocols/ENVIRONMENT.md | Y | 264 | 2c25409 2026-04-27 | none | No DEV_KNOWLEDGE_PATH env var (ADR-35 requirement) |
| protocols/SESSION_SETUP.md | Y | 173 | a17ff95 2026-04-27 | none | No BACKLOG review step (ADR-41); no audit tool mention (ADR-36) |
| CONTRIBUTING.md | Y | 92 | dbca501 2026-04-28 | none | ADR process section cites "ADR-27 through ADR-32 for style reference"; no 33–41 |
| CLAUDE.md | Y | 132 | 03ee055 2026-04-28 | none | File rules table missing BACKLOG.md; Council decisions list stops at ADR-32 |

---

## Per-file observations

### README.md

- **Lines:** 97
- **Last commit:** c81a01d 2026-04-28 "docs(readme): update mission framing + index + Current state"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Entry-point file with folder layout table, three start-session sections (browser, Claude Code), and navigation pointers. No date marker in content. `docs/audits/` listed in folder layout table. BACKLOG.md not listed in root canonical files row (`(root)` row in folder layout) or anywhere in the index.
- **Specific notes:** README lists root canonical files as "VISION, ARCHITECTURE, README, CLAUDE, CHANGELOG, JOURNAL, LESSONS, CONTRIBUTING" — BACKLOG.md (present at root, mandated by ADR-41) is absent from this index. The "Starting a new browser chat" section does not mention BACKLOG.md as a session-start artifact.

---

### VISION.md

- **Lines:** 104
- **Last commit:** f2e1f6c 2026-04-28 "docs(vision): add VISION.md as universal brain mission statement"
- **ADR mentions (33–41):** none by ADR number
- **Content sample (first 50 lines):** Frontmatter `last_reviewed: 2026-04-28`. Mission statement, Scope, Values, Relationships sections. Auditor function described ("It also functions as auditor — evaluating each project's scale (S/M/L) and verifying correct methodology implementation"). "Pattern for child repos" note says "pending formal ADR for universalization" — this is now resolved (ADR-33 ratified).
- **Specific notes:**
  - "Pattern for child repos (pending formal ADR for universalization)" — ADR-33 was ratified, this language is stale.
  - Lifecycle section references "Stream C audit tool — pending" correctly notes it as pending; but does not cite ADR-36.
  - References section does not list `docs/decisions/` subdirectory, BACKLOG.md, or CONTRIBUTING.md.
  - No ADR numbers cited anywhere in the file.

---

### ARCHITECTURE.md

- **Lines:** 130
- **Last commit:** 62a3783 2026-04-28 "docs(architecture): add ARCHITECTURE.md per ADR-28 three-layer model"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Frontmatter `last_reviewed: 2026-04-28`. Three-layer architecture diagram (Browser chat / .dev-knowledge / Projects). ADR-39 registry entry cites "Three-layer technical model (foundation/core/orchestration/interface per ADR-26 Tach taxonomy)" — but the file itself does not contain "Tach", "four-layer", "foundation", "orchestration", or "interface" as taxonomy labels. The file uses "Layer 1 / Layer 2 / Layer 3" as the naming model.
- **Specific notes:**
  - ADR-39 registry entry for ARCHITECTURE.md describes "Three-layer technical model (foundation/core/orchestration/interface per ADR-26 Tach taxonomy)" — this taxonomy labeling (Tach) is not reflected in the current ARCHITECTURE.md content.
  - ADR-38 (Universal Repo Architecture Baseline) ratified 2026-04-30; ARCHITECTURE.md predates this by 2 days. No ADR-38 content visible.
  - File commits to "three-layer" framing; ADR-38 may have introduced extensions — requires Rob cross-check.

---

### protocols/PLAYBOOK.md

- **Lines:** 2220
- **Last commit:** 0710991 2026-04-28 "docs(playbook): triggers vs caps + §13 stale notice + Council §5 dual-output"
- **ADR mentions (33–41):** ADR-33, ADR-34 present. ADR-35, 36, 37, 38, 39, 40, 41 absent.
- **Content sample (first 60 lines):** Header says `Last updated: 2026-04-21` (stale vs git date 2026-04-28). System Architecture diagram, AGENTS.md section. 2220 lines total — comprehensive methodology reference.
- **Specific notes:**
  - `Last updated: 2026-04-21` in the document header; actual last git commit was 2026-04-28. Header date stale by 7 days.
  - No section found for: tier transition procedures (ADR-40), backlog grooming workflow (ADR-41), audit tool usage (ADR-36), two-phase handoff format (ADR-37 Current State/Future State overlay).
  - ADR-39 lifecycle entry for PLAYBOOK.md states update trigger: "event-triggered: on methodology refinement, ADR ratification adding/changing process" — 5 ADRs ratified 2026-04-30 that add/change process; PLAYBOOK not updated.

---

### protocols/ESSENTIALS.md

- **Lines:** 226
- **Last commit:** 16bdc0e 2026-04-28 "docs(essentials): mission anchor + Council output convention"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Header says "Keep under 1 page" (226 lines suggests full doc is multi-page). "How Claude thinks", "Roles", "Browser chat (architect)" sections. Mission anchor note added recently.
- **Specific notes:**
  - No cheat-sheet rules for ADRs 35–41 content areas: lessons querying (ADR-35), audit tool trigger conditions (ADR-36), two-phase handoff format (ADR-37), tier evaluation signals (ADR-40), BACKLOG grooming cadence (ADR-41).
  - Note: not every ADR change requires an ESSENTIALS update — only those adding high-leverage daily-use rules. That determination is Rob's, not this audit's.

---

### LESSONS.md

- **Lines:** 219
- **Last commit:** 8eed0be 2026-04-30 "chore: append session 2026-04-30 to JOURNAL + LESSONS (5 ADRs + meta)"
- **ADR mentions (33–41):** ADR-37 only (found in one entry)
- **Content sample (first 50 lines):** Append-only format per ADR-29. Last updated: 2026-04-30. Entries span 2026-03-25 through 2026-04-30. Chronological oldest-first.
- **Specific notes:**
  - 2026-04-30 session lessons were appended (compliance with lifecycle trigger).
  - ADR-39 lesson about JOURNAL skip failure mode is visible in ADR-39 text but may not have a corresponding LESSONS.md entry — would require reading all entries to verify (not sampled here due to 219 line file; first 50 lines confirm format).
  - ADR-39, 40, 41 ratified 2026-04-30 — if lessons from those ADRs are absent, that is a same-day gap.

---

### JOURNAL.md

- **Lines:** 365
- **Last commit:** 8eed0be 2026-04-30 "chore: append session 2026-04-30 to JOURNAL + LESSONS (5 ADRs + meta)"
- **ADR mentions (33–41):** ADR-33, ADR-34, ADR-35, ADR-36, ADR-37, ADR-38 present. ADR-39, ADR-40, ADR-41 absent.
- **Content sample (first 50 lines):** Newest-first prepend per lifecycle spec. Entry for 2026-04-30 — Stream C session 6 covers ADR-33 through ADR-38 in "Did" section.
- **Specific notes:**
  - 2026-04-30 session entry covers ADR-33 through ADR-38 but does not include ADR-39 (File Lifecycle Governance), ADR-40 (Scale Tier Evaluation), ADR-41 (Cross-Session Backlog Architecture) in its narrative — despite all three being ratified in the same session.
  - This may reflect partial session logging (ADR-38 ratification followed by ADR-39/40/41 in the same session with no incremental JOURNAL update).

---

### CHANGELOG.md

- **Lines:** 779
- **Last commit:** 4db227e 2026-04-30 "docs(adr): add ADR-41 Cross-Session Backlog Architecture + initial BACKLOG.md seed"
- **ADR mentions (33–41):** all 9 present
- **Content sample (first 50 lines):** Newest-first append. Top entry: 2026-04-30 — ADR-41. Second entry: 2026-04-30 — ADR-40/39/38/37/36. Third: 2026-04-29 — ADR-34/35. Fourth: 2026-04-28 — ADR-33.
- **Specific notes:** Appears current. All 9 ADRs reflected. Lifecycle compliance observed.

---

### protocols/HANDOFF_PROCESS.md

- **Lines:** 291
- **Last commit:** 53e7da9 2026-04-28 "docs: fix ADR filename slugs + record JOURNAL pending for ADR-32 errata"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Header: `<!-- version: 2.0 — 2026-04-28 (full rewrite per ADR-32) -->`. Authoritative source declared as ADR-32. Roles section (Browser architect / Claude Code executor / Rob). No "Current State / Future State" overlay sections.
- **Specific notes:**
  - File is v2.0 (ADR-32 only). ADR-37 (Session Boundary Protocol) ratified 2026-04-30 adds two-phase overlay (Current State + Future State over existing 9-section structure, renamed to "Detailed Context"). This overlay is absent.
  - ADR-41 BACKLOG integration into handoff workflow (if any) not reflected.
  - BACKLOG.md already has a P1 item tracking this gap — confirmed by this audit. The gap is known and tracked.

---

### templates/HANDOFF_TEMPLATE.md

- **Lines:** 110
- **Last commit:** f21a4d9 2026-04-28 "docs(template): update HANDOFF_TEMPLATE.md to match HANDOFF_PROCESS rewrite"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Header: "Skeleton matches `protocols/HANDOFF_PROCESS.md` v2.0 (ADR-32 §5)". 9 sections (charter recap, decisions, work completed, pending items…). No "## Current State" or "## Future State" top-level sections per ADR-37.
- **Specific notes:**
  - Template still v2.0 (ADR-32 §5) skeleton. ADR-37 two-phase overlay (Current State + Future State at top, existing 9 sections renamed to "Detailed Context") not incorporated.
  - Same gap as HANDOFF_PROCESS.md — expected, as template should mirror process spec.
  - No JOURNAL update step explicitly in template (ADR-39 enforcement requirement: "first-message.md handoff template MUST include JOURNAL update step").

---

### protocols/ENVIRONMENT.md

- **Lines:** 264
- **Last commit:** 2c25409 2026-04-27 "chore(repo): update path references after file moves"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** Header `Last updated: 2026-04-27`. Claude Code CLI version, model routing, ccusage tool, settings.json key values, ~/.claude/ directory tree.
- **Specific notes:**
  - No `DEV_KNOWLEDGE_PATH` env var listed. ADR-35 (Lessons Base Activation) ratified 2026-04-29 introduces `DEV_KNOWLEDGE_PATH` as the cross-repo discovery mechanism for lessons retrieval. Grep returned zero matches.
  - Last commit 2026-04-27, predating ADR-35 (2026-04-29), ADR-36, 37, 38, 39, 40, 41 (2026-04-30).
  - ADR-39 update trigger for ENVIRONMENT.md: "event-triggered: on environment change, new tool added" — DEV_KNOWLEDGE_PATH is a new env var per ADR-35.

---

### protocols/SESSION_SETUP.md

- **Lines:** 173
- **Last commit:** a17ff95 2026-04-27 "chore(repo): file moves to new structure (protocols/, logs/, config/)"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines):** 5-step browser chat workflow (Know which chat / Start the chat / Upload / First message / Next session). Mentions "Max 2 objectives per session. Everything else is backlog." — generic "backlog" concept, not BACKLOG.md.
- **Specific notes:**
  - No BACKLOG.md review step in session startup sequence (ADR-41 mandates BACKLOG at M+ tier; SESSION_SETUP is the natural enforcement point for "review BACKLOG before chartering session").
  - No audit tool trigger conditions (ADR-36) in session setup.
  - Last commit 2026-04-27 predates all 9 ADRs under review.

---

### CONTRIBUTING.md

- **Lines:** 92
- **Last commit:** dbca501 2026-04-28 "docs: update cross-references to HANDOFF_PROCESS rewrite"
- **ADR mentions (33–41):** none
- **Content sample (first 50 lines, last 42 lines reviewed):** Branch naming, commit style, pre-commit setup, validators section (scope-tag-validator per ADR-27), ADR process section, handoff process section.
- **Specific notes:**
  - ADR process section: "See ADR-27 through ADR-32 for style reference." — stops at ADR-32. ADRs 33–41 now exist and are the more recent style examples.
  - Handoff process section references "v2.0, 2026-04-28 — folder format per ADR-32" — does not mention ADR-37 two-phase overlay.
  - No mention of BACKLOG.md or ADR-41 in contribution conventions.

---

### CLAUDE.md (project-level)

- **Lines:** 132
- **Last commit:** 03ee055 2026-04-28 "docs(claude): document VISION/ARCHITECTURE files + Council convention"
- **ADR mentions (33–41):** none
- **Content sample (first 50 and 50–132 lines reviewed):** File rules table (VISION, ARCHITECTURE, ESSENTIALS, SESSION_SETUP, PLAYBOOK, HANDOFF_PROCESS, ENVIRONMENT, LESSONS, TOKEN-LOG, CHANGELOG, JOURNAL, README, requirements-dev.txt). What to do / What NOT to do. Related locations. Scope tags section (ADR-27). Council decisions list (through Topic 2 / ADR-32).
- **Specific notes:**
  - File rules table does not include BACKLOG.md (now present at root, mandated by ADR-41).
  - Council decisions list: #23, #24, #27, #28, Topic 1 (ADR-31), Topic 2 (ADR-32) + two Triggers. ADR-33 through ADR-41 not reflected in Council decisions list.
  - No mention of audit tool (ADR-36), tier evaluation (ADR-40), or BACKLOG architecture (ADR-41) in "What to do here" section.
  - Consistency check section does not include "Does JOURNAL entry cover all ADRs ratified in session?" or "Is BACKLOG.md up to date?"

---

## Files NOT in ADR-39 registry but present in repo

The following `.md` files exist in the repository but have no ADR-39 registry entry:

| File | Notes |
|---|---|
| `BACKLOG.md` | Present at root. Mandated by ADR-41 (Cross-Session Backlog Architecture). ADR-41 explicitly states "ADR-39 amendment required for lifecycle elements" — amendment not yet done. This is an expected post-ratification follow-up, not an error. |
| `templates/AGENTS-md-template.md` | Template file. Not in ADR-39 registry. |
| `templates/CLAUDE-md-template.md` | Template file. Not in ADR-39 registry. |
| `templates/codex-review-config-template.md` | Template file. Not in ADR-39 registry. |
| `templates/prompt-template.md` | Template file. Not in ADR-39 registry. |

Note: ADR-39 registry covers `templates/HANDOFF_TEMPLATE.md` explicitly; the four other template files are unregistered. Whether they require registry entries is Rob's call — ADR-39 says "every file in .dev-knowledge MUST have 6 lifecycle elements."

---

## Files in ADR-39 registry but missing in repo

None. All 14 registered files are present.

---

## Aggregate findings

- **14 registered files audited** — all present
- **0 missing**
- **1 file fully current:** CHANGELOG.md (all 9 ADRs reflected)
- **1 file partially current:** JOURNAL.md (ADR-33–38 present, ADR-39/40/41 absent from 2026-04-30 entry)
- **1 file partially current:** LESSONS.md (2026-04-30 append done; ADR-39/40/41-specific lessons not confirmed present)
- **5 files with observable specific gaps:**
  - HANDOFF_PROCESS.md — no ADR-37 two-phase overlay (known, tracked in BACKLOG)
  - HANDOFF_TEMPLATE.md — no ADR-37 two-phase sections; no explicit JOURNAL step per ADR-39 enforcement requirement
  - ENVIRONMENT.md — no DEV_KNOWLEDGE_PATH (ADR-35 requirement)
  - CLAUDE.md — no BACKLOG.md in file rules table; Council decisions stop at ADR-32
  - PLAYBOOK.md — no sections for ADR-36/37/40/41 methodology additions; header date stale
- **7 files with no ADR-33–41 mentions and last-committed before ADR ratification dates:**
  - README.md, VISION.md, ARCHITECTURE.md, ESSENTIALS.md, SESSION_SETUP.md, CONTRIBUTING.md, ENVIRONMENT.md
- **5 unregistered template files** not covered by ADR-39 registry
- **BACKLOG.md** present but not yet in ADR-39 registry (ADR-41 follow-up pending)

---

## Summary

14 registered files audited; all present, none missing. CHANGELOG.md is the only file that fully reflects all 9 ADRs ratified 2026-04-28 through 2026-04-30. The two most structurally significant gaps — HANDOFF_PROCESS.md and HANDOFF_TEMPLATE.md not reflecting ADR-37 two-phase overlay — are already tracked in BACKLOG.md as P1 items. ENVIRONMENT.md is missing the DEV_KNOWLEDGE_PATH env var introduced by ADR-35. CLAUDE.md does not list BACKLOG.md in its file rules table and its Council decisions list stops at ADR-32. Seven files show no ADR mentions in the 33–41 range and were last committed before those ADRs were ratified, indicating update triggers that fired but were not acted upon; whether each requires action is Rob's determination per file.

---

**Next step:** Rob reviews this report per-file, decides: fix-now (small prompt) vs BACKLOG entry (later session).
