---
type: retrofit-plan
scope: ai-council visual-pattern conformance per ADR-59
date: 2026-05-27
basis: ADR-59 Universal Visual Repository Pattern
status: plan (consumed by a separate ai-council session for execution)
contract: read-only inspection of ai-council; writes confined to .dev-knowledge/docs/audits/
---

# ai-council Visual-Pattern Retrofit Plan — 2026-05-27

Closes the ADR-59 gap(s) for `ai-council`. This plan **executes nothing** — it is
consumed by a separate ai-council Claude Code session with write access to that
repo. The `.dev-knowledge` session that authored it made zero changes to
ai-council.

## Current state (read-only inspection, 2026-05-27)

- Branch at inspection: `chore/universalization-2026-05-26` (HEAD `bd06523`),
  clean. **Note:** that universalization branch was not yet merged to `main` at
  inspection — re-verify HEAD/branch before executing (work on top of whatever is
  current on `main`).
- Root-level tracked files: `.ai-council.code-workspace`, `.gitignore`,
  `.pre-commit-config.yaml`, `pyproject.toml`, `ARCHITECTURE.md`, `BACKLOG.md`,
  `CLAUDE.md`, `JOURNAL.md`, `LESSONS.md`, `VISION.md`.
- Workspace `.ai-council.code-workspace` carries `"explorer.sortOrder": "default"`
  but **not** `"explorer.sortOrderLexicographicOptions"`.

## Projected ADR-59 audit findings

| Check | Status | Reason |
|---|---|---|
| `dot_prefix_discipline` | PASS | only `pyproject.toml` (exception) is an un-dotted root config; `.gitignore` / `.pre-commit-config.yaml` already dotted |
| `canonical_md_visibility` | PASS | VISION/ARCHITECTURE/CLAUDE/BACKLOG present, ALL-CAPS; JOURNAL/LESSONS correctly cased |
| `workspace_settings` | **WARN** | `.ai-council.code-workspace` is dot-prefixed but missing `explorer.sortOrderLexicographicOptions: upper` |

**Net gap: one workspace setting.** ai-council is the closest to conformant of the four.

## Gaps vs ADR-59

| Item | Current | Required | Action |
|---|---|---|---|
| Workspace lexicographic sort | absent | `explorer.sortOrderLexicographicOptions: "upper"` | Action 1 |
| `explorer.sortOrder` | `"default"` | `"default"` | none (already correct) |
| Config dot-prefix | conformant | conformant | none |
| Canonical `.md` | conformant | conformant | none |

## Actions (sequenced)

### Action 1 — add lexicographic sort setting to the workspace
- **What:** add `"explorer.sortOrderLexicographicOptions": "upper"` to the
  `settings` block of `.ai-council.code-workspace`. Preserve all existing settings;
  add only this key. If a no-op `"explorer.sortOrderReverse"` is present, remove it
  (it is not a real VS Code setting — ADR-59 D4).
- **Where:** `ai-council/.ai-council.code-workspace` (`settings` object).
- **Why:** ADR-59 Decision 3 — `upper` is what clusters ALL-CAPS canonical `.md`
  ahead of lowercase configs; `default` alone mixes case.
- **Verification:** from `.dev-knowledge`, `python scripts/audit.py repo ai-council`
  → `workspace_settings` PASS; or open the Explorer and confirm the ALL-CAPS files
  cluster together.
- **Commit suggestion:** `chore: add explorer.sortOrderLexicographicOptions=upper per ADR-59`.

## Verification gates (post-execution)

- ai-council `git status` clean; tests green (ai-council `pytest -m "not integration and not envcheck"`).
- From `.dev-knowledge`: `python scripts/audit.py repo ai-council` → all 6 checks PASS.

## Estimated effort

~5–10 min, Sonnet / low. Single-line workspace edit + verify.

## Operator decisions

None beyond ADR-59 defaults. No deviations expected.

## What this plan does NOT include

- Any change to ai-council source, ADRs, or governance content.
- Merging the pending `chore/universalization-2026-05-26` branch (separate decision).
- Cross-repo modifications.
