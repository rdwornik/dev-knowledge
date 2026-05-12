# ADR-34 — File naming convention (cross-repo)

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-29
Related: ADR-27 (scope tags), ADR-29 (lessons grandfathering),
         ADR-33 (VISION universalization),
         transcript council-out-20260429-190922-*

## Context

.dev-knowledge ecosystem accumulated heterogeneous file naming over
time. ADRs use snake_case, transcripts use snake_case, configs vary,
templates use kebab-case, living docs use UPPERCASE, protocols use
UPPERCASE_WITH_UNDERSCORES. This ADR codifies existing de-facto
patterns where they work, resolves true inconsistencies, and avoids
costly migration.

Per ADR-33 universalization pattern, this convention is mandate for
.dev-knowledge and recommendation for child repos with dependents,
verifiable via Phase 3 cross-repo audit tool.

Council debate (council-out-20260429-190922-*) covered Q1-Q8.

## Decision

### Scope (Q1)

Mandate: universal across .dev-knowledge AND all child repos under Dev/.
Code stays per language convention (Python snake, JS kebab, etc.).

> **[Amended 2026-05-11]** Scope changed from mandate (.dev-knowledge) /
> recommendation (child repos) to universal mandate. Recommendation-tier
> scope demonstrated as failure mode per 2026-05-11 cross-repo audit —
> inconsistency across repos (ADRs hyphen in corp-monorepo, underscore in
> .dev-knowledge) surfaced immediately. See Amendments section below.

### File type conventions (Q2 + Q3)

No universal master rule. Convention per file type — table is source
of truth.

**Separator rule (universal):** Use **hyphen** (`-`) as separator in ALL
filenames AND foldernames. Applies to both .dev-knowledge and all child
repos under Dev/. This rule is independent of date-token format (date
shape `YYYYMMDD` vs `YYYY-MM-DD` is a separate question per Q4 below).

**Canonical examples:**
- `ADR-27-scope-tagging.md`
- `2026-05-11-cross-repo-pattern-audit.md`
- `council-out-YYYYMMDD-HHMMSS-topic.md`

> **[Amended 2026-05-11]** ADR and transcript entries changed from
> underscore to hyphen per Council decision. See Amendments section below.

| File type | Convention | Example |
|---|---|---|
| Living docs (root) | UPPERCASE.md | README.md, VISION.md, CLAUDE.md |
| Protocols | UPPERCASE_WITH_UNDERSCORES.md | HANDOFF_PROCESS.md |
| ADRs | ADR-NN-topic.md | ADR-27-scope-tagging.md |
| Council transcripts (auto) | council-out-YYYYMMDD-HHMMSS-topic.md | council-out-20260429-190922-pick-adr34.md |
| Legacy decision transcripts | DECISION_NN_topic.md (grandfathered) | DECISION_27_*.md |
| Audits / handoffs | YYYY-MM-DD-topic-with-dashes.md | 2026-04-27-deep-cleansing-diagnostic.md |
| Templates | kebab-case-template.md | CLAUDE-md-template.md |
| Code modules | per language convention | snake_case.py |
| Configs | kebab-case.yaml | dev-knowledge.yaml |
| Append-only files | single file (LESSONS.md, CHANGELOG.md, JOURNAL.md) | one each, no suffix |

### Date prefix usage (Q4)

- YYYY-MM-DD: narrative date prefix for human-authored artifacts (audits, handoffs)
- YYYYMMDD_HHMMSS: machine-generated timestamps (Council CLI auto outputs)
- No date prefix: living docs, ADRs (numbered), templates, code, configs

### Versioning (Q5)

- NO filename versioning (no `_v2`, `_final`, `_old`)
- Old versions → `docs/archive/YYYY-MM-DD-topic.md`
- Git history is canonical version-of-record

### Migration (Q6: hybrid, scoped)

- **Immediate fix**: configs only if mixed conventions exist (audit needed)
- **Grandfather**: DECISION_NN_*.md legacy transcripts (3 files, meaningful
  numbering, historical artifacts; per ADR-29 grandfathering pattern)
- **No action needed**: ADRs, living docs, protocols, templates, audits/
  handoffs, Council CLI transcripts (all already compliant)

### Enforcement (Q7: hybrid baseline)

- **Now (passive)**: AGENTS.md / CLAUDE.md in .dev-knowledge note
  "follow ADR-34 file naming convention"
- **Now (active)**: pre-commit hook validates new file paths against
  conventions table (separate task, follow-up)
- **Future (Phase 3)**: cross-repo auditor tool checks compliance across
  all repos with dependents (per ADR-33 enforcement model). Auditor
  validates BOTH ADR-33 VISION presence AND ADR-34 naming compliance.

### Universalization (per ADR-33 pattern)

> **[Amended 2026-05-11]** Scope changed to universal mandate. See Amendments section.

- **Mandate**: .dev-knowledge AND all child repos under Dev/ (corp-monorepo,
  ai-council, corp-ops, corp-sca-time-automation, future repos)
- **Migration cohort**:
  - Immediate (Prompt K): .dev-knowledge (~31 file renames, link rewrites,
    `_archive/` → `archive/` folder rename)
  - Phase 2: corp-monorepo, ai-council (per cross-repo handshake, ADR-43)
  - Trigger-based: corp-ops, corp-sca-time-automation, future repos
    — next session touching repo for >1 commit, OR by 2026-06-30
- **Cross-repo audit (Phase 3)**: auditor tool validates naming
  compliance across all repos with dependents
- **Passive enforcement**: child repo AGENTS.md / CLAUDE.md links
  to ADR-34 in "Read first" sections

## Consequences

### Positive
- File type → location → convention is deterministic
- New contributors (AI agents, future Rob) derive correct name from type
- Existing files mostly compliant — minimal migration
- Convention codifies what works, doesn't invent
- Mirrors ADR-33 universalization for consistency

### Negative
- Master rule absent — must consult table for each new file type
- Carve-outs (ADRs snake, transcripts snake, templates kebab) feel
  inconsistent at first read
- Configs migration scope unknown until audit completes
- Cross-repo enforcement deferred to Phase 3 audit tool

### Follow-ups
- Configs audit in .dev-knowledge (small task, separate session)
- Pre-commit hook implementation in .dev-knowledge (small task, separate session)
- AGENTS.md / CLAUDE.md updates in .dev-knowledge linking ADR-34
- ai-council VISION.md + naming compliance check (Stream C Phase 2)
- corp-monorepo VISION.md + naming compliance check (Stream C Phase 2)
- Cross-repo audit tool spec must include naming convention validator
  (Phase 3 — auditor checks BOTH ADR-33 VISION compliance AND ADR-34
  naming compliance)
- Re-audit at 2026-06-30 for trigger-based cohort compliance

## References

- transcript council-out-20260429-190922-pick-council-adr34-file-naming-convention.md
- ADR-27 (scope tags)
- ADR-29 (lessons grandfathering pattern)
- ADR-33 (VISION universalization framework)

## Amendments

### 2026-05-11 — Cycle 1: Universal hyphen mandate

- **Source:** AI Council debate, transcript at
  `docs/decisions/transcripts/council-out-20260511-205022-pick-2026-05-11-council-question-ecosystem-separator.md`
- **Council vote:** Q1-A, Q2-A, Q3-A, Q4-A (all 4 panel models converged:
  claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3)
- **Decision:** Separator changes from underscore (with split
  mandate/recommendation scope) to **hyphen universal mandate**. Separator
  rule applies to BOTH filenames AND foldernames across .dev-knowledge and
  all child repos. CLI output format (`council-out-*`) treated as in-scope.
- **Original text superseded:**
  - Scope: was "Mandate: .dev-knowledge / Recommendation: child repos"
  - ADR row: was `ADR-NN_topic_with_underscores.md`
  - Transcript row: was `council_out_YYYYMMDD_HHMMSS_topic_with_underscores.md`
- **Migration scope:** .dev-knowledge atomic migration deferred to Prompt K
  (separate atomic PR: ~31 file renames + link rewrites + `_archive/` →
  `archive/` folder rename). Child repos handled via cross-repo handshake
  per ADR-43.
- **AI Council implementation:** ai-council CLI output format change via
  cross-repo cycle 2 (cross-repo notification artifact generated 2026-05-11,
  operator routing to ai-council pending).
