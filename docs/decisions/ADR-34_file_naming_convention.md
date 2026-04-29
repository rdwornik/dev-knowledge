# ADR-34 — File naming convention (cross-repo)

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-29
Related: ADR-27 (scope tags), ADR-29 (lessons grandfathering),
         ADR-33 (VISION universalization),
         transcript council_out_20260429_190922_*

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

Council debate (council_out_20260429_190922_*) covered Q1-Q8.

## Decision

### Scope (Q1)

Mandate: .dev-knowledge repo (all markdown + configs).
Recommendation: child repos under Dev/.
Code stays per language convention (Python snake, JS kebab, etc.).

### File type conventions (Q2 + Q3)

No universal master rule. Convention per file type — table is source
of truth.

| File type | Convention | Example |
|---|---|---|
| Living docs (root) | UPPERCASE.md | README.md, VISION.md, CLAUDE.md |
| Protocols | UPPERCASE_WITH_UNDERSCORES.md | HANDOFF_PROCESS.md |
| ADRs | ADR-NN_topic_with_underscores.md | ADR-33_vision_universalization.md |
| Council transcripts (auto) | council_out_YYYYMMDD_HHMMSS_topic_with_underscores.md | council_out_20260429_190922_pick_*.md |
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
- Old versions → `docs/archive/YYYY-MM-DD_topic.md`
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

- **Mandate**: .dev-knowledge repo
- **Recommendation**: child repos under Dev/ (corp-monorepo, ai-council,
  corp-ops, corp-sca-time-automation, future repos)
- **Migration cohort**:
  - Immediate (Stream C Phase 2): ai-council, corp-monorepo
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

- transcript council_out_20260429_190922_pick_council_adr34_file_naming_convention.md
- ADR-27 (scope tags)
- ADR-29 (lessons grandfathering pattern)
- ADR-33 (VISION universalization framework)
