# Scrum-Master Review: ai-council

<!-- scope: meta -->

**Date:** 2026-05-11 (executed 2026-05-12)
**Reviewer:** .dev-knowledge ecosystem strażnik (Prompt L)
**Subject:** ai-council (Scale M — operator-declared)
**Review type:** Cross-repo scrum-master review (first empirical instance of pattern)
**Baseline:** April 2026 audit (2026-04-30-ai-council-audit-report.md); re-verified current state 2026-05-12

---

## Executive summary

ai-council is in good operational health with active, recent maintenance. All P1 governance gaps from the April 2026 audit (VISION.md, DEV_KNOWLEDGE_PATH config) have been resolved. The repo shows a high cadence of feature delivery and disciplined documentation upkeep through 2026-05-12.

Ten findings identified: 1 critical, 6 important, 3 minor. The critical item is a stale task-tracking file with a wildly incorrect test count that misleads any agent or human starting work. The important items are primarily ADR-34 filename compliance misses (including a fresh violation added today) and a missing BACKLOG.md mandated by ADR-41. No dead code was identified; the codebase is actively maintained across all 35 source files.

**Top 3 priority items:** (1) retire/rewrite `tasks/todo.md` — actively misleading; (2) create BACKLOG.md per ADR-41 mandate; (3) rename two docs/ files to ADR-34-compliant hyphen format.

---

## Findings by area

### A. Governance files (ADR-38 compliance)

Scale M mandatory set per ADR-38 + ADR-41: CLAUDE.md, README.md, CHANGELOG.md, JOURNAL.md, VISION.md, BACKLOG.md.
ARCHITECTURE.md is mandatory at L, optional at M. AGENTS.md per ADR-28 is ecosystem standard but not in ADR-38 M-tier mandatory list.

| File | Present | State | Action |
|---|---|---|---|
| CLAUDE.md | ✓ | Current — updated 2026-05-12; reflects 5-model panel, routing, ADR-43, 362 tests | None |
| README.md | ✓ | Partially stale — architecture section shows pre-ADR-38 flat `src/` layout; test count 354 vs 362 | Update architecture section + test count |
| CHANGELOG.md | ✓ | Current — maintained through 2026-05-12; well-structured | None |
| JOURNAL.md | ✓ | Current — updated 2026-05-12; recent cadence | None |
| VISION.md | ✓ | Present since 2026-05-09; content current; `last_reviewed` not updated post 5/11-5/12 work | Bump `last_reviewed` to 2026-05-12 |
| ARCHITECTURE.md | ✗ | Absent — optional at M tier per ADR-38 | No action required; CLAUDE.md Architecture section serves equivalent purpose |
| AGENTS.md | ✗ | Absent — per ADR-28, ecosystem standard for cross-tool governance | Recommend adding per ADR-28 (low urgency) |
| LESSONS.md (root) | ✗ | Absent — by design; project-local lessons in `tasks/lessons.md`; cross-ecosystem flow to `.dev-knowledge` per ADR-35 | No action; configuration is intentional and documented in CLAUDE.md |
| BACKLOG.md | ✗ | Absent — **ADR-41 mandates BACKLOG.md at M+ tier; ai-council declared Scale M** | Create BACKLOG.md per ADR-41 schema |

---

### B. Filename compliance (ADR-34 amended — universal hyphen mandate)

**Non-compliant docs/ files (require rename):**

| File | Current name | Compliant form | Age |
|---|---|---|---|
| `docs/COUNCIL_QUESTION_GUIDE.md` | UPPERCASE + underscore | `docs/council-question-guide.md` | pre-ADR-34 |
| `docs/SYNTHESIS-QUALITY-RUBRIC.md` | UPPERCASE + underscore | `docs/synthesis-quality-rubric.md` | **added 2026-05-12 — fresh violation** |

**Legacy audit files (should be archived, not renamed):**

| File | Issue | Recommendation |
|---|---|---|
| `docs/audits/2026-03-15_CODE_REVIEW_REPORT.md` | Underscore + UPPERCASE slug — pre-ADR-34 Codex audit format | Move to `docs/audits/archive/legacy/` (same pattern as .dev-knowledge DECISION_NN archival) |
| `docs/audits/2026-03-26_CODE_REVIEW_REPORT.md` | Same | Same |

**Compliant or exempt:**

- ai-council ADRs (`ADR-01-synthesizer-selection.md` etc.) — grandfathered kebab-case per ADR-29 ✓
- `council_inbox/archive/` files — ISO 8601 timestamp data files, exempt from doc naming convention ✓
- `output/council_out_*` historical transcripts — pre-ADR-34, explicitly preserved per CHANGELOG 2026-05-12 ✓
- `docs/decisions/` ADR files — hyphen-compliant ✓
- `docs/audits/` recent files — all 2026-05 files use correct hyphen format ✓

---

### C. Documentation maintenance

| File | Last modified | Assessment |
|---|---|---|
| CLAUDE.md | 2026-05-12 | Current; 362 unit tests; transcript routing documented; ADR-43 cycle 1 reflected |
| README.md | 2026-05-11 | **Stale in two places:** (1) Architecture section shows pre-ADR-38 flat `src/` layout — should show `src/ai_council/` namespace; (2) test count "354" not updated after 5/11-5/12 additions (CLAUDE.md shows 362) |
| CHANGELOG.md | 2026-05-12 | Current; well-maintained |
| JOURNAL.md | 2026-05-12 | Current; all recent work entries present |
| VISION.md | 2026-05-09 | Content current; `last_reviewed` date not bumped after significant feature work 5/11-5/12 |

---

### D. Operator-specific folders (tasks/lessons/todo)

No standalone `lessons/` or `todo/` directories exist. Tracking lives in `tasks/`:

**`tasks/todo.md`** (last modified 2026-03-29) — **CRITICAL: severely stale and misleading**
- States "Phase 1 + Phase 2 complete. 255 unit tests passing" — actual count is 362
- Shows checklist of open items from March 2026; all substantively addressed since
- Any agent or human reading this for task context gets false state
- Recommended action: either (a) retire this file — BACKLOG.md per ADR-41 supersedes it, or (b) rewrite as a minimal "current focus" doc with correct state
- Note: CLAUDE.md Folder Governance section documents `tasks/` as legitimate and names `todo.md` — this reference needs updating once file is retired

**`tasks/lessons.md`** (last modified 2026-04-30) — minor staleness
- 3 entries total; last is from 2026-04-30 (mock.patch string literals gotcha)
- Significant feature cycles 5/11-5/12 (transcript routing, ADR-43 amendment, observability) produced no new entries
- Not a hard mandate (by-design local lessons); architect's call whether to append post-5/12 cycle lessons

---

### E. Dead code / obsolete content

No dead code identified. All 35 source files in `src/ai_council/` show recent git activity or are stable modules with clear active use:

- All modules in CLAUDE.md architecture table map to existing files ✓
- `routing.py` added 2026-05-11 (new feature) ✓
- `orchestrator.py` added 2026-04-30 (ADR-38 extraction) ✓
- 2 scripts in `scripts/`: `check.ps1` (active — run before every merge) and `council-ask.ps1` (last modified 2026-04-26; utility script, low priority to verify)
- `eval/` folder: empty (no files observed; CLAUDE.md documents `eval_history.jsonl` — may be gitignored or not yet populated)
- No commented-out blocks or deprecated module candidates observed in file listing

One flag for architect investigation: `eval/` appears empty but CLAUDE.md references `eval_history.jsonl`. Verify whether this file exists (gitignored) or documentation is ahead of implementation.

---

### F. Folder structure consistency vs ecosystem baseline

| Folder | Present | Assessment |
|---|---|---|
| `docs/audits/` | ✓ | 10 files; current; good cadence through 5/12 |
| `docs/decisions/` | ✓ | 7 ADRs + README; all reviewed and current as of 5/11 governance sweep |
| `docs/decisions/transcripts/` | ✓ | 14 CLI-generated `council-out-*` transcripts; empty is fine (routing just activated) |
| `docs/handoffs/` | ✓ | 1 active handoff + `_archive/` subfolder; compliant with ADR-32/37 |
| `src/ai_council/` | ✓ | Namespace package per ADR-38; 14 files + 2 subpackages |
| `tests/` | ✓ | 21 test files; 362 unit tests per CLAUDE.md |
| `config/` | ✓ | `settings.yaml` + `config_loader.py`; single source of truth per CLAUDE.md |
| `council_inbox/` | ✓ | Gitignored; archive populated; `.gitkeep` present |
| `output/` | ✓ | Gitignored; 23 historical `council_out_*` transcripts (pre-ADR-34); 0 `council-out-*` (new format not yet exercised post-change) |

No unexpected folders. Ecosystem baseline structure well-maintained.

---

## Findings summary

| Severity | Count | Items |
|---|---|---|
| **Critical** | 1 | C1: `tasks/todo.md` severely stale — wildly incorrect test count (255 vs 362); misleads agents |
| **Important** | 6 | I1: BACKLOG.md missing (ADR-41 M+ mandate); I2: README.md architecture section shows pre-ADR-38 flat `src/` layout; I3: README.md test count stale (354 vs 362); I4: `docs/COUNCIL_QUESTION_GUIDE.md` non-compliant ADR-34 (UPPERCASE+underscore); I5: `docs/SYNTHESIS-QUALITY-RUBRIC.md` non-compliant ADR-34 (added 2026-05-12 — fresh violation); I6: 2 legacy `_CODE_REVIEW_REPORT.md` audit files should be archived |
| **Minor** | 3 | M1: VISION.md `last_reviewed` not bumped post 5/11-5/12; M2: AGENTS.md absent; M3: `tasks/lessons.md` not updated since 2026-04-30 |
| **Total** | **10** | |

---

## Recommended actions (for ai-council architect)

**C1 — Retire or rewrite `tasks/todo.md`** *(critical; do first)*
The file states 255 unit tests and March 2026 open items. Every agent starting a session risks acting on false state. Options: (a) delete the file and capture its surviving items in BACKLOG.md (preferred — BACKLOG.md supersedes), or (b) rewrite with correct current state. Update CLAUDE.md Folder Governance if `todo.md` reference is removed.

**I1 — Create BACKLOG.md** *(important; ADR-41 mandate)*
Scale M declared by operator → ADR-41 mandates BACKLOG.md. Seed with: surviving items from `tasks/todo.md`, the `openai_deep_research` integration test gap (currently in todo.md), and any known future roadmap items. ADR-41 schema: Stream sections, P1/P2/P3 priorities, grooming cadence.

**I2+I3 — Update README.md** *(important; two related fixes)*
(a) Architecture section: replace flat `src/` tree with `src/ai_council/` namespace layout (matches CLAUDE.md); (b) test count: update "354" → "362" (or current `pytest --collect-only` count).

**I4+I5 — Rename two docs/ files to ADR-34-compliant form** *(important; one is a fresh violation)*
- `docs/COUNCIL_QUESTION_GUIDE.md` → `docs/council-question-guide.md`
- `docs/SYNTHESIS-QUALITY-RUBRIC.md` → `docs/synthesis-quality-rubric.md`
Update any internal cross-references (CLAUDE.md references `docs/COUNCIL_QUESTION_GUIDE.md`).

**I6 — Archive legacy code review reports** *(important; same class as .dev-knowledge DECISION_NN archival)*
Move `docs/audits/2026-03-15_CODE_REVIEW_REPORT.md` and `docs/audits/2026-03-26_CODE_REVIEW_REPORT.md` to `docs/audits/archive/legacy/`. Keep underscore filenames as-is (historical accuracy in archive). Update `docs/audits/README.md` archive convention note.

**M1 — Bump VISION.md `last_reviewed`** *(minor)*
Update `last_reviewed: "2026-05-09"` → `"2026-05-12"`. Two significant cycles (transcript routing + observability) shipped since last review.

**M2 — Add AGENTS.md** *(minor; per ADR-28)*
Per ADR-28, AGENTS.md is the canonical cross-tool governance doc (Codex, Claude Code, Cursor, etc.). Not in ADR-38 M-tier mandatory list but ecosystem standard. Low urgency; include in a future maintenance cycle.

**M3 — Append to `tasks/lessons.md`** *(minor)*
Five significant lessons from 5/11-5/12 cycles not captured: target resolver fail-loud pattern, inbox code-path parity (now established as recurring blind spot — third time), ADR-43 amendment schema DRYness, synthesis_metrics field design. Architect's call.

---

## Out of scope for this review

- ai-council CLI emitter format change (`council_out_*` → `council-out-*`) — already implemented in cycle 2, in flight
- ADR-40 algorithm recalibration — ongoing ecosystem concern, deferred per Rob's Path 3 strategy (requires audit tool P1 data)
- ARCHITECTURE.md gap — optional at Scale M; CLAUDE.md Architecture section provides equivalent coverage; no action warranted
- Methodology proposal review (deferred per operator) — separate scope, not a scrum-master review item
- `council_inbox/archive/` ISO timestamp underscore filenames — data files, exempt from ADR-34 doc naming convention

---

## April 2026 baseline: resolved items

For completeness — findings from `2026-04-30-ai-council-audit-report.md` that are now resolved:

| Finding | Status |
|---|---|
| F-01 VISION.md absent | ✓ Resolved — created 2026-05-09 |
| F-02 Lessons discovery not configured | ✓ Resolved — CLAUDE.md Lessons Discovery section added with DEV_KNOWLEDGE_PATH config |
| F-05 ADR naming divergence | ✓ Resolved — existing 7 ADRs grandfathered per ADR-29; documented in CLAUDE.md |
| F-03 BACKLOG.md absent (deferred) | Still open — now actionable since Scale M declared by operator (ADR-41 mandate) |
| F-04 ARCHITECTURE.md absent (deferred) | Remains deferred — optional at M; CLAUDE.md covers equivalent content |
| F-08 ADR-40 calibration | Still open — ecosystem-wide, deferred to audit tool P1 |

---

## Process note

This is the first empirical instance of the scrum-master review pattern. `.dev-knowledge`-as-strażnik produces this audit report; operator routes report to ai-council architect; architect implements. Distinct from cross-repo handshake (which is for bilateral decisions); this review is unilateral audit + recommendation.

Pattern codification: BACKLOG `Cross-stream P2` entry added (awaits N=2 empirical grounding before ADR-level codification).
