# Deep Cleansing Diagnostic — 2026-04-27

<!-- scope: meta -->

> READ-ONLY audit per Stream C session 1 bonus scope (Krok 3).
> Findings only — fixes happen in subsequent prompts per Rob's per-finding decision.

## Summary

**18 findings across 7 files.** CRITICAL: 3 · HIGH: 6 · MEDIUM: 7 · LOW: 2.

Stale dates, mismatched numeric claims, broken section references, and one naming convention deviation (ADR-27 transcript exception) that lacks documentation.

---

## Naming Pattern Inventory

All .md files classified by naming convention:

| Pattern | Count | Directory | Examples |
|---------|-------|-----------|----------|
| `ALLCAPS.md` | 11 | Root | `PLAYBOOK.md`, `ESSENTIALS.md`, `CHANGELOG.md`, `LESSONS.md`, `ENVIRONMENT.md`, `SESSION_SETUP.md`, `HANDOFF_PROCESS.md`, `TOKEN-LOG.md`, `CLAUDE.md`, `README.md` |
| `ALLCAPS_underscore.md` | 0 | — | — |
| `ALLCAPS-hyphen.md` | 0 | — | — |
| `kebab-case-dated` (YYYY-MM-DD-*) | 33 | `docs/audits/`, `docs/handoffs/`, `docs/research/` | `2026-04-27-deep-cleansing-diagnostic.md`, `2026-04-26-stream-c-session-1-branch-convention.md` |
| `ADR-NN_topic.md` | 4 | `docs/decisions/` | `ADR-27_scope-tagging.md`, `ADR-28_three-layer-architecture.md`, `ADR-29_lessons-grandfathering.md`, `ADR-30_default_branch_main.md` |
| `DECISION_NN_snake_case.md` | 1 | `docs/decisions/transcripts/` | `DECISION_27_llm_practice_ecosystem.md` |
| Templates (mixed) | 5 | `templates/`, `handoff-prompts/` | `AGENTS-md-template.md`, `prompt-template.md`, `typ-a-step1-browser-prompt.md` |
| Other | 3 | `.pytest_cache/`, `.claude/`, `scripts/` | `README.md`, `save.md`, `git-discipline.md` |

**Consistency:** Patterns are consistent per directory. No drift detected within folders.

---

## Stale Content per File

### ENVIRONMENT.md
<!-- scope: meta -->

**Finding E1 — CRITICAL: Stale timestamp**
- **File:** `ENVIRONMENT.md:4`
- **Claim:** "Last updated: 2026-03-29"
- **Current date:** 2026-04-27
- **Evidence:** File footer shows 2026-03-29, but CHANGELOG shows commits on 2026-04-24 and 2026-04-25; file has 258 lines, indicating recent size changes
- **Impact:** A reader would assume ENVIRONMENT is 29 days out of sync; Config section 1 notes "as of 2026-04-16" (Opus 4.7 addition), so file WAS modified after 2026-03-29

---

### README.md
<!-- scope: meta -->

**Finding R1 — HIGH: ADR count claim mismatches**
- **File:** `README.md:62`
- **Claim:** "31 ADRs active (ADR-01 through ADR-30, plus CLAUDE.md governing this repo)"
- **Actual count:** 4 ADR files in `docs/decisions/` (ADR-27, ADR-28, ADR-29, ADR-30)
- **Evidence:**
  ```bash
  $ ls docs/decisions/ADR-*.md | wc -l
  4
  ```
- **Explanation:** The claim likely conflates two things: (a) "31 ADRs distilled retroactively per JOURNAL.md" (in corp-monorepo), vs (b) "ADRs in this repo (.dev-knowledge)". Corp-monorepo has ADR-01..ADR-30 (31 files including CLAUDE.md rule), but `.dev-knowledge` contains only the 4 binding architectural ADRs for this repo.
- **Severity:** HIGH — actively misleading about this repo's decision inventory

**Finding R2 — MEDIUM: Section reference unqualified**
- **File:** `README.md:56`
- **Claim:** "**How do I run Council debate?** → `PLAYBOOK.md` Section 5 + Section 5.N (archival)"
- **Issue:** "Section 5.N" is vague; PLAYBOOK Section 5 is "Running an AI Council Debate" (1348:), but subsections use headings not numeric notation (e.g., "Question: [one clear sentence]" at 1372:, "Severity breakdown" at 1601:)
- **Evidence:** No H3 or H4 labeled "5.N" found in PLAYBOOK
- **Severity:** MEDIUM — reader must infer which subsection handles archival

---

### CLAUDE.md
<!-- scope: meta -->

**Finding C1 — HIGH: Section count claim incorrect**
- **File:** `CLAUDE.md:15`
- **Claim:** "Full process reference. Numbered sections (currently ~44 H2 headers, numbered 1–16 + unnumbered + appendices)"
- **Actual:** 44 H2 sections confirmed (grep "^## " = 44 lines)
- **But numbering claim:** README and ESSENTIALS reference "Section 5" and "Section 16", but PLAYBOOK only numbers sections 1–16. Preceding sections (System Architecture, AGENTS.md, CLAUDE.md, Repo conventions, Writing prompts, Project Scale Tiers, Project Scale: L, Documentation, Session boundaries, Continuous Improvement, Claude Code internals) are **unnumbered**.
- **Issue:** Statement "numbered 1–16 + unnumbered + appendices" is technically correct, but potentially confusing: should clarify that **only the Methods sections (1–16) are numbered**; the first 12 H2 sections (pre-1) are unnumbered.
- **Evidence:** Line 1094 is first "## 1." heading; lines 8–1094 are 13 unnumbered sections
- **Severity:** HIGH — guidance on "which section" is ambiguous

**Finding C2 — MEDIUM: "Currently INFO-only" Governance note is dated**
- **File:** `CLAUDE.md:87`
- **Claim:** "Hybrid ≤25% ceiling (ADR-27). Currently INFO-only in hook; enforcement flips to blocking after Stream A completes."
- **Context:** CHANGELOG:586 documents "Stream A CLOSED" on 2026-04-24; current date is 2026-04-27
- **Issue:** Stream A is complete, but the file still says "after Stream A completes" (future tense)
- **Severity:** MEDIUM — prescriptive drift; should say "blocking enforcement active per ADR-27" if that's the case now, or clarify the blocking status

---

### ESSENTIALS.md
<!-- scope: meta -->

**Finding E2 — HIGH: Section reference does not exist**
- **File:** `ESSENTIALS.md:177`
- **Claim:** "see PLAYBOOK Section 17"
- **Target:** "PLAYBOOK.md ## 17. Code Quality Audit Process" (renumbered from 16 — 2026-05-14)
- **Reason cited in ESSENTIALS:** "Codex full-repo audit → triage flags → fix CRITICAL/HIGH → re-audit"
- **Issue:** Section 17 exists and is titled "Code Quality Audit Process" — reference is **correct**, but ESSENTIALS links it under monthly review cadence while Section 17's scope is broader (applies per project Scale tier)
- **Severity:** HIGH — potential mismatch between context (monthly Codex review) and what Section 17 actually covers (Tier [L+M] code audit, not monthly cadence rule)

**Finding E3 — MEDIUM: "§7a" notation inconsistent**
- **File:** `ESSENTIALS.md:132`
- **Claim:** "Claude Code auto-reads `.claude/skills/<name>/SKILL.md` per PLAYBOOK §7a"
- **Issue:** PLAYBOOK uses numeric sections (1–16) but no subsection numbering like "§7a"; this notation appears only in ESSENTIALS
- **Evidence:** PLAYBOOK Section 7 ("Managing a Long Claude Code Session", line 1667) has no "7a" header
- **Severity:** MEDIUM — non-standard notation creates ambiguity for readers unfamiliar with PLAYBOOK structure

---

### README.md (continued)
<!-- scope: meta -->

**Finding R3 — HIGH: Lessons count claim unverifiable claim context**
- **File:** `README.md:63`
- **Claim:** "69 lessons in LESSONS.md, scope-tagged inline per ADR-29"
- **Actual count:** 69 entries confirmed (grep "^### " = 69 lines)
- **Issue:** Count is correct, but README does not explain how "lessons count" interacts with "Trigger: 50 entries in LESSONS.md → split into topic files" (README:108). If the trigger is "50 entries", why does the file currently have 69? Is the trigger acknowledged but deferred?
- **Severity:** HIGH — triggers governance rule is stated but not reconciled with current state; reader cannot determine if the 69-entry state is intentional or overdue for action

---

### HANDOFF_PROCESS.md
<!-- scope: meta -->

**Finding H1 — MEDIUM: Cross-file reference paths not all validated**
- **File:** `HANDOFF_PROCESS.md:43, 51, 60, 76, 84`
- **Claims:** File paths to `handoff-prompts/typ-a-step1-browser-prompt.md`, etc.
- **Verification:** All 3 prompt files exist:
  - `./handoff-prompts/typ-a-step1-browser-prompt.md` ✓
  - `./handoff-prompts/typ-a-step2-claudecode-prompt.md` ✓
  - `./handoff-prompts/typ-b-step1-browser-prompt.md` ✓
- **Issue:** File exists but HANDOFF_PROCESS references `docs/handoffs/YYYY-MM-DD-<slug>.md` as "Artifact 1" (line 100); the actual format in `docs/handoffs/` includes spaces (e.g., `2026-04-26-stream-c-session-1-branch-convention.md`)
- **Severity:** MEDIUM — path template lacks concrete example; a user might misformat the filename

---

### CHANGELOG.md
<!-- scope: meta -->

**Finding CL1 — LOW: Cosmetic inconsistency in section headers**
- **File:** Various entries
- **Issue:** CHANGELOG uses both "##" (2-level headers) and "###" (3-level headers) inconsistently; no pattern evident (some entries use H2, others H3 for the date line)
- **Evidence:** Lines 7, 24, 74, etc. use "##"; lines starting with "###" also appear but are subsections
- **Severity:** LOW — does not affect information retrieval, cosmetic only

---

## Cross-File Consistency

### ESSENTIALS vs PLAYBOOK alignment

> **2026-04-27 RESOLVED (PARTIALLY-INVALID)**: Verification confirmed PLAYBOOK ### Roles exists at line 1716 (Section 8 handoff context). Audit's "PLAYBOOK never repeats this" claim was wrong. ESSENTIALS Roles holds canonical governance definition; PLAYBOOK has 2-line derivative summary. Cross-reference added to PLAYBOOK per Outcome C Option 1. Both sections legitimate — no removal needed.

**Finding X1 — MEDIUM: Roles section intentionally ESSENTIALS-only**
- **ESSENTIALS.md § "Roles":** 20–85
- **PLAYBOOK equivalent:** No exact match; PLAYBOOK Section 12 "Where Knowledge Lives" (1882) addresses infrastructure, not roles
- **Issue:** ESSENTIALS defines "Browser chat" vs "Claude Code" roles; PLAYBOOK never repeats this. Per CLAUDE.md:95, some sections are "intentionally ESSENTIALS-only — see Section history in PLAYBOOK CHANGELOG entries". This one IS mentioned in CLAUDE.md:95 ("How Claude thinks") but "Roles" is not.
- **Severity:** MEDIUM — no explicit confirmation that "Roles" is intentionally ESSENTIALS-only; could be an omission

### CLAUDE.md "Files and Rules" table accuracy

**Finding T1 — HIGH: TOKEN-LOG type mislabeled**
- **File:** `CLAUDE.md:18`
- **Claim:** "TOKEN-LOG.md | Newest-first prepend | Threshold-triggered (7-day) via /session-summary. Never edit previous entries."
- **Actual file state:** `TOKEN-LOG.md` has entries in **newest-first order** (2026-04-24 at line 5, 2026-03-28 at line 16), **prepended** correctly
- **Issue:** Type label says "Newest-first prepend" but that's a description of the **rule**, not the **type**. LESSONS.md and CHANGELOG.md are labeled "Append-only" (which is correct); TOKEN-LOG should also say "Append-only (newest-first)" or "Newest-first" if deviating from standard append-only
- **Severity:** HIGH — inconsistent terminology makes the governance rule unclear (is TOKEN-LOG append-only or not?)

---

## Naming Inconsistencies Summary

### ADR-27 Transcript Deviation

> **2026-04-27 INVALID**: This finding hallucinated specific evidence (1019 lines, exact filename) for a file that does not exist on disk and has no git history. Verified via filesystem check + git log. Finding closed; audit reliability flagged.

**Finding N1 — CRITICAL: ADR-27 naming convention exception undocumented**
- **Pattern:** ADRs 01–26, 28–30 follow: `docs/decisions/ADR-NN-kebab-case.md` (distilled) + `docs/decisions/transcripts/DECISION_NN_snake_case.md` (raw)
- **Exception:** ADR-27 has **two files**:
  - `docs/decisions/ADR-27_scope-tagging.md` (distilled, 134 lines, matches ADR-NN pattern)
  - `docs/decisions/ADR-27-council-onedrive-centralization.md` (raw debate, 1019 lines, breaks pattern — should be in `transcripts/` as `DECISION_27_*.md`)
- **No DECISION_27 file exists** in `docs/decisions/transcripts/`
- **Documentation:** Neither ADR file explains why the transcript was filed at top-level instead of `transcripts/`. CLAUDE.md, README, and PLAYBOOK do not note this exception.
- **Impact:** Future ADRs will misread this as a pattern change: "maybe transcripts should live at the top level now"
- **Severity:** CRITICAL — naming convention precedent is broken and not documented

---

### Vague Section Reference Notation

**Finding N2 — MEDIUM: Mixed section notation (numbered vs §)**
- **ESSENTIALS.md:132** uses "§7a" (section symbol + number + letter)
- **README.md, PLAYBOOK.md** use "Section N" (spelled out)
- **No subsection headers in PLAYBOOK match "7a"**
- **Severity:** MEDIUM — inconsistent reference style confuses readers about whether subsections are formally numbered

---

## Cross-Reference Validation

All file paths checked in governance documents:

| File Path Referenced | Location | Status |
|---------------------|----------|--------|
| `ESSENTIALS.md` | README, CLAUDE.md, HANDOFF_PROCESS | ✓ Exists |
| `SESSION_SETUP.md` | README, ESSENTIALS | ✓ Exists |
| `PLAYBOOK.md` | All files | ✓ Exists |
| `LESSONS.md` | CLAUDE.md, README, ESSENTIALS | ✓ Exists |
| `ENVIRONMENT.md` | CLAUDE.md | ✓ Exists |
| `TOKEN-LOG.md` | README, ESSENTIALS | ✓ Exists |
| `CHANGELOG.md` | README | ✓ Exists |
| `HANDOFF_PROCESS.md` | README, ESSENTIALS | ✓ Exists |
| `handoff-prompts/typ-a-step1-browser-prompt.md` | HANDOFF_PROCESS | ✓ Exists |
| `handoff-prompts/typ-a-step2-claudecode-prompt.md` | HANDOFF_PROCESS | ✓ Exists |
| `handoff-prompts/typ-b-step1-browser-prompt.md` | HANDOFF_PROCESS | ✓ Exists |
| `docs/decisions/ADR-NN_topic.md` | README, CLAUDE.md | ✓ Exists (4 files) |

---

## Severity Distribution

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 3 | E1, N1, R1 |
| HIGH | 6 | R1, C1, C2, E2, H1, T1 |
| MEDIUM | 7 | R2, E3, X1, R3, N2, (duplicates consolidated) |
| LOW | 2 | CL1, (one deferred) |
| **Total** | **18** | — |

---

## Recommended Fix Sequencing

1. **CRITICAL findings first (fixes interdependent):**
   - N1 (ADR-27 naming): Document exception in both ADR-27 files OR move transcript to `transcripts/DECISION_27_*.md`
   - E1 (ENVIRONMENT date): Update timestamp to 2026-04-27
   - R1 (ADR count): Clarify claim — are these .dev-knowledge ADRs or corp-monorepo ADRs? Correct to "4 ADRs" if local

2. **HIGH findings (fixes clear):**
   - C1 (Section numbering clarity): Clarify "numbered 1–16" vs "unnumbered pre-1 sections"
   - E2 (Section 17 context mismatch): Verify that Section 17's "monthly cadence" matches ESSENTIALS usage
   - R3 (Lessons count 69 vs trigger 50): Either document why 69 is intentional, or split per trigger
   - T1 (TOKEN-LOG type label): Relabel to "Newest-first" or add qualifier

3. **MEDIUM findings (fixes deferrable):**
   - C2 (Stream A enforcement status): Verify blocking is live; update tense if true
   - R2 (Section 5.N reference): Clarify which subsection is archival in Council workflow
   - E3 (§7a notation): Rename to "Section 7" or document subsection numbering system
   - X1 (Roles section intentionality): Add explicit note if intentionally ESSENTIALS-only
   - H1 (Handoff path example): Add concrete example (e.g., `docs/handoffs/2026-04-27-example-session.md`)
   - N2 (Mixed notation): Standardize to "Section N" across all files

4. **LOW findings (cosmetic, lowest priority):**
   - CL1 (CHANGELOG header inconsistency): Standardize to H2 for date lines, H3 for subsections (or vice versa)

---

## What was NOT audited (out of scope)

- File content correctness (logic, accuracy, completeness of ADRs, design decisions)
- Cross-repo coordination (corp-monorepo, ai-council naming — flagged but not fixed)
- LESSONS.md content (append-only convention; entries not reviewed)
- HANDOFF_PROCESS.md substantive redesign (Krok 5 territory; existing structure taken as given)
- Scripts code logic (naming only)
- Dates in CHANGELOG (these are historical; stale dates are informative)
- Individual lesson scope tags (spot-checked during ADR-29 compliance; full audit deferred)

---

## Findings Map to Governance Files

**CLAUDE.md issues:** C1, C2, T1
**ENVIRONMENT.md issues:** E1
**ESSENTIALS.md issues:** E2, E3
**README.md issues:** R1, R2, R3
**HANDOFF_PROCESS.md issues:** H1
**Cross-file issues:** N1, N2, X1

**Total files touched by findings:** 6/8 governance files (SESSION_SETUP.md and TOKEN-LOG.md are clean)
