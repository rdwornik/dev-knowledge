# Taxonomy Simplification — Verification Report

**Date:** 2026-05-27
**Session type:** Autonomous cross-repo cleanup (operator-driven; single Claude Code session, no `.dev-knowledge` orchestration script per Layer-2 invariant)
**ADR change:** ADR-60 amendment 2026-05-27 — Simplification + repo-type variants
**Branches (5 total, awaiting operator merge):**

| Repo | Branch |
|---|---|
| `.dev-knowledge` | `docs/taxonomy-simplification-2026-05-27` |
| `ai-council` | `chore/docs-taxonomy-cleanup-2026-05-27` |
| `corp-ops` | `chore/docs-taxonomy-cleanup-2026-05-27` |
| `corp-sca-time-automation` | `chore/docs-taxonomy-cleanup-2026-05-27` |
| `corp-monorepo` | `chore/docs-taxonomy-cleanup-2026-05-27` |

---

## Empirical findings vs prompt expectations

The prompt was built on a 2026-05-26 universalization rollout assumption that over-propagated `.dev-knowledge`'s docs taxonomy to all child code repos. Verification at session start (per-repo `ls docs/`) revealed the over-propagation was **not** as broad as the prompt assumed:

| Repo | Folders present at session start | Over-propagation? |
|---|---|---|
| `.dev-knowledge` | `archive/`, `audits/`, `council-questions/`, `decisions/`, `handoffs/`, `research/` | (source — to simplify) |
| `ai-council` | `audits/`, `decisions/` + 2 root .md files | **No** — already clean |
| `corp-ops` | (no `docs/` folder at all) | **No** — never had docs/ |
| `corp-sca-time-automation` | `archive/`, `handoffs/` | Partial (handoffs/ only) |
| `corp-monorepo` | `archive/`, `audits/`, `decisions/`, `diagrams/` | **No** — already aligned with child-repo variant |

This narrowed the cleanup substantially. The bulk of the work landed in `.dev-knowledge` (Phase B). Each child repo's primary deliverable was archive/ + README per the amendment's new pending-zone semantics.

## Pre-flight outcomes

| Check | Result |
|---|---|
| All repos on `main`, working trees clean | ✅ |
| Concurrent CC/Python sessions | None |
| Retrofit branches from 2026-05-27 already merged | ✅ All 5 (Pre-flight 0b skipped — nothing to merge) |

## Phase A — `.dev-knowledge` ADR-60 amendment + PLAYBOOK + ESSENTIALS

**Commits (3):**
- `fae0d73` ADR-60 amendment — simplify taxonomy + repo-type variants
- `d336c14` PLAYBOOK taxonomy section per ADR-60 amendment (also updated File type taxonomy + File presence table + folder-structure cross-reference + Council debate routing line)
- `4226253` ESSENTIALS taxonomy line per ADR-60 amendment

**Amendment defines:**
- `.dev-knowledge` taxonomy: `decisions/` + `audits/` + `handoffs/` + `archive/`
- Child code repos taxonomy: `decisions/` + `audits/` + `archive/` + `diagrams/`
- Retires `research/` and `council-questions/` (didn't earn permanence)
- `archive/` is a documented pending-classification zone with periodic-review lifecycle
- File-placement rules: entry-scripts → `scripts/`; root-exception configs are `pyproject.toml`, `tach.toml`, `requirements.txt`

## Phase B — `.dev-knowledge` cleanup

**Commits (3):**
- `71febc1` retire `research/` (12 files → `archive/`; README.md `git rm`d)
- `81e57e5` retire `council-questions/` (5 Q-files `git rm`d; 2 cross-file artifacts → `archive/`; README.md `git rm`d)
- `2ed72c5` clean `archive/` + add pending-zone README

### B1 — research/ reclassification (12 content files + README)

All 12 files moved to `docs/archive/` (flat) — they are substantial exploratory artifacts that never matured into ADRs or audits and remain reference-worthy. Operator decision: ambiguous content → archive (not delete). Per-file disposition:

| File | Disposition |
|---|---|
| `2026-03-29-council-browser-handoff.md` | → archive/ |
| `2026-03-29-council-research-new-models.md` | → archive/ |
| `2026-03-30-council-25-diagrams-corp-monorepo.md` | → archive/ |
| `2026-04-15-council-26-tach-adoption-corp-monorepo.md` | → archive/ |
| `2026-04-23-council-28-community-patterns.md` | → archive/ |
| `2026-04-23-llm-dev-patterns-2026.md` | → archive/ |
| `2026-04-24-claude-md-best-practices.md` | → archive/ |
| `2026-04-24-council-29-spec-kit-kiro.md` | → archive/ |
| `2026-04-24-multi-agent-debate-patterns.md` | → archive/ |
| `2026-04-27-handoff-patterns-council-research.md` | → archive/ |
| `2026-04-27-handoff-patterns-external-research.md` | → archive/ |
| `2026-05-17-kimi-k2-scoping.md` | → archive/ (BACKLOG #243 pending) |
| `README.md` | `git rm` (lifecycle description no longer applies) |

`docs/research/` removed.

### B2 — council-questions/ retirement (8 files)

Q1-Q5 content verified verbatim in `docs/decisions/transcripts/council-out-20260526_*-Q{1-5}-*.md` (direct head-to-head comparison: same `## Question` header, same body text, same questions/constraints — the Council CLI embeds the full question into the transcript). Per operator decision: `git rm` Q-files. Cross-file artifacts (evidence + index) preserved to archive.

| File | Disposition |
|---|---|
| `2026-05-25-handoff-council-Q1-internalization-assurance.md` | `git rm` (content in Q1 transcript) |
| `2026-05-25-handoff-council-Q2-bundle-content-composition.md` | `git rm` (content in Q2 transcript) |
| `2026-05-25-handoff-council-Q3-procedural-competence-transfer.md` | `git rm` (content in Q3 transcript) |
| `2026-05-25-handoff-council-Q4-sender-verification-symmetry.md` | `git rm` (content in Q4 transcript) |
| `2026-05-25-handoff-council-Q5-delivery-custody-abstraction.md` | `git rm` (content in Q5 transcript) |
| `2026-05-25-handoff-failures-evidence.md` | → archive/ (potentially-unique structured empirical record cited by all 5 Q-files) |
| `2026-05-25-handoff-methodology-council-index.md` | → archive/ (set index) |
| `README.md` | `git rm` (folder retired) |

`docs/council-questions/` removed.

### B3 — archive/ cleanup + README

Operator-flagged deletions:
- `docs/archive/tech-radar/2026-Q2.md` — `git rm`
- `docs/archive/tech-radar/README.md` — `git rm`
- `docs/archive/2026/2026-05-26-consolidation-preflight.md` — `git rm`

Empty subfolders `tech-radar/` and `2026/` removed. `docs/archive/` is now flat: 14 dated `.md` files + `README.md`.

`docs/archive/README.md` created documenting the pending-classification zone semantics, current contents (newest first), and the periodic-review lifecycle.

### Final `.dev-knowledge` `docs/` state

```
docs/
├── archive/       (14 dated files + README — pending-classification zone)
├── audits/        (audit reports, validation, forensics)
├── decisions/     (ADRs + transcripts/)
└── handoffs/      (handoff bundles + centralized 2026-04-15 corp-sca legacy import)
```

Matches the `.dev-knowledge` variant of the ADR-60 amendment exactly.

## Phase C — `ai-council`

**Commit (1):**
- `82528c5` seed `docs/archive/` + README per ADR-60 amendment

ai-council had no over-propagated folders (no `research/`, no `council-questions/`, no `handoffs/`). The 2 root `.md` files (`council-question-guide.md`, `synthesis-quality-rubric.md`) are operational guides, left in place — not in this session's scope. Only delta: `docs/archive/` seeded with the pending-zone README to materialize the amendment's contract.

**Final `ai-council/docs/` state:** `audits/`, `decisions/`, `archive/` + 2 root .md files. Matches child-repo variant (no `diagrams/` because none exist; `diagrams/` is optional per amendment).

## Phase D — `corp-ops`

**Commit (1):**
- `4cb83ca` seed `docs/archive/` per ADR-60 amendment

corp-ops had no `docs/` folder at all (extreme version of "clean"). The amendment was operator-explicit on `archive/` in every repo, so `docs/archive/` + README was created to seed the convention.

**Final `corp-ops/docs/` state:** `archive/` only. The taxonomy contract is materialized for when content classification work begins; no over-application of empty `decisions/`/`audits/` folders.

## Phase E — `corp-sca-time-automation`

**Commits (2 in corp-sca, 1 in `.dev-knowledge`):**
- (corp-sca) `1961d33` remove `docs/handoffs/`, seed `docs/archive/` + README
- (.dev-knowledge) `955409a` centralize 2026-04-15 corp-sca legacy handoff to `.dev-knowledge/docs/handoffs/`

`docs/handoffs/2026-04-15-handoff.md` was a substantive 2026-04-15 architecture-review + features handoff bundle (pre-2026-04-27 single-file legacy format). Migrated to `.dev-knowledge/docs/handoffs/2026-04-15-corp-sca-legacy-handoff.md` with provenance frontmatter; `docs/handoffs/` folder removed in corp-sca.

`docs/archive/` already existed with one legacy UPPERCASE-TYPE file (`2026-03-15_CODE_REVIEW_REPORT.md` — BACKLOG P3 "retire opportunistically"). Left in place; archive/README added documenting it as legacy.

### `run.py` move — DEFERRED

Per operator's autonomy contract ("DEFER if can't verify"), the `run.py` → `scripts/` move was deferred. Reasons:

1. **corp-sca venv lacks pytest+ruff.** Direct check (`python -c "import pytest, ruff"`) → `ModuleNotFoundError`. Before/after test verification (mandatory per operator decision table) cannot run without installing dev tooling. Network/policy state not confirmed.
2. **Structural complexity of the move.** `run.py:88` uses `Path(__file__).parent / "scripts" / "calendar_export.vbs"` — moving `run.py` to `scripts/` requires changing this to `.parent.parent / "scripts"` to keep VBS path resolution correct.
3. **~6 user-facing instruction strings** in `run.py` print `python run.py <command>` (in help text + `cmd_export`, `cmd_preview`, `cmd_upload`, `cmd_catchup` docstrings/messages). All would need rewriting to `python scripts/run.py <command>`.
4. **pyproject.toml entry-point** (if any) would need updating; not yet verified.

Per operator's "DEFER → flag" decision, a dedicated session with `pip install pytest ruff` first, then before/after test runs surrounding the move + reference-update, is the safe path. Captured as new BACKLOG item below.

**Final `corp-sca-time-automation/docs/` state:** `archive/` only. No `handoffs/`. Matches child-repo variant. (`decisions/` and `audits/` not pre-created — added on first need per the "no empty scaffolding" rule.)

## Phase F — `corp-monorepo`

**Commit (1):**
- `ca089c9` seed `docs/archive/README` per ADR-60 amendment

corp-monorepo `docs/` was already aligned with the child-repo variant: `archive/`, `audits/`, `decisions/`, `diagrams/`. No folders to remove. `tach.toml` stays at root (root-exception config per amendment).

Existing 33 UPPERCASE-TYPE legacy files in `archive/` (BACKLOG P3 "retire opportunistically") documented in the new README, left in place.

**Final `corp-monorepo/docs/` state:** `archive/` + `audits/` + `decisions/` + `diagrams/`. Matches child-repo variant exactly.

## Architectural contract verification

| Invariant | Status |
|---|---|
| No `.dev-knowledge` orchestration script (Layer-2 / ADR-28) | ✅ Operator-driven cd into each repo |
| All deletes via `git rm` (history preserved) | ✅ |
| Content-bearing files reclassified (audits/decisions) or archived; never blind-deleted | ✅ |
| Handoff history preserved (corp-sca bundle centralized) | ✅ |
| ADR-60 amended, not rewritten | ✅ (`fae0d73`: amendment appended) |
| Each repo committed to its own `.git/` | ✅ |
| No push, no auto-merge | ✅ |

## Test results

- `.dev-knowledge`: `pytest -x --tb=short` → **85 passed** (previous "known pre-existing failure" note in CLAUDE.md is stale; all green, consistent with BACKLOG P3 finding 2026-05-24).
- Child repos: no code-affecting changes (docs-only additions); existing test suites unaffected. ai-council 407 tests and corp-monorepo 2524 tests not re-run because no source was touched.
- corp-sca: tooling unavailable (`pip install pytest ruff` not run this session — see Deferrals).

## Deferrals

| Item | Reason | Captured |
|---|---|---|
| `corp-sca-time-automation` `run.py` → `scripts/` | venv lacks pytest+ruff; ~6 user-facing strings + `__file__.parent` resolution + possible pyproject entry-point need rewriting; before/after tests cannot run | BACKLOG (new item this session) |
| `corp-sca` legacy archive `2026-03-15_CODE_REVIEW_REPORT.md` UPPERCASE rename | BACKLOG P3 "retire opportunistically" — out of this session's scope (cosmetic-only) | Already in BACKLOG |
| `corp-monorepo` 33 legacy UPPERCASE-TYPE archive files | BACKLOG P3 "retire opportunistically" — out of this session's scope | Already in BACKLOG |

## Branches awaiting operator merge

```
cd C:\Users\1028120\Documents\Dev\.dev-knowledge
git checkout main && git merge --no-ff docs/taxonomy-simplification-2026-05-27

cd C:\Users\1028120\Documents\Dev\ai-council
git checkout main && git merge --no-ff chore/docs-taxonomy-cleanup-2026-05-27

cd C:\Users\1028120\Documents\Dev\corp-ops
git checkout main && git merge --no-ff chore/docs-taxonomy-cleanup-2026-05-27

cd C:\Users\1028120\Documents\Dev\corp-sca-time-automation
git checkout main && git merge --no-ff chore/docs-taxonomy-cleanup-2026-05-27

cd C:\Users\1028120\Documents\Dev\corp-monorepo
git checkout main && git merge --no-ff chore/docs-taxonomy-cleanup-2026-05-27
```

No Codex `/review` recommended — all changes are docs/governance only (no executable code touched).

## Cross-references

- ADR-60 + 2026-05-27 amendment: `docs/decisions/ADR-60-docs-folder-taxonomy.md`
- Updated taxonomy guidance: `protocols/PLAYBOOK.md` "docs/ folder taxonomy" (v2.0)
- Updated session-start cheat: `protocols/ESSENTIALS.md` "docs/ taxonomy (ADR-60)"
- Predecessor work (2026-05-26 universalization): `docs/audits/2026-05-27-cross-repo-retrofit-verification.md`
- ADR-59 sibling: visual repository pattern (unchanged by this amendment)
