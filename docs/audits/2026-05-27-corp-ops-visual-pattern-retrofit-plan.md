---
type: retrofit-plan
scope: corp-ops visual-pattern conformance per ADR-59
date: 2026-05-27
basis: ADR-59 Universal Visual Repository Pattern
status: plan (consumed by a separate corp-ops session for execution)
contract: read-only inspection of corp-ops; writes confined to .dev-knowledge/docs/audits/
---

# corp-ops Visual-Pattern Retrofit Plan — 2026-05-27

Closes the ADR-59 gap(s) for `corp-ops`. This plan **executes nothing** — it is
consumed by a separate corp-ops Claude Code session with write access to that
repo. The `.dev-knowledge` session that authored it made zero changes to corp-ops.

## Current state (read-only inspection, 2026-05-27)

- Branch at inspection: `chore/universalization-2026-05-26` (HEAD `117f3c1`),
  clean. **Note:** not yet merged to `main` at inspection — re-verify HEAD/branch
  before executing.
- Root-level tracked files: `.gitignore`, `pyproject.toml`, `ARCHITECTURE.md`,
  `BACKLOG.md`, `CLAUDE.md`, `VISION.md`.
- **No `.code-workspace` file exists** (workspace add was deferred during the
  2026-05-26 universalization — verification report D-CO2).

## Projected ADR-59 audit findings

| Check | Status | Reason |
|---|---|---|
| `dot_prefix_discipline` | PASS | only `pyproject.toml` (exception) is an un-dotted root config; `.gitignore` already dotted |
| `canonical_md_visibility` | PASS | the four mandatory files present, ALL-CAPS |
| `workspace_settings` | **FAIL** | no `.code-workspace` file at root |

**Net gap: create the workspace file.**

## Gaps vs ADR-59

| Item | Current | Required | Action |
|---|---|---|---|
| Workspace file | absent | `.corp-ops.code-workspace` with required sort settings | Action 1 |
| Config dot-prefix | conformant | conformant | none |
| Canonical `.md` | conformant | conformant | none |

## Actions (sequenced)

### Action 1 — create the dot-prefixed workspace file
- **What:** create `corp-ops/.corp-ops.code-workspace`. Minimal content: a
  `folders` entry (`{ "path": "." }`) and a `settings` block containing the two
  required keys. Use the `.dev-knowledge` workspace (or `templates/workspace-*.code-workspace`)
  as a starting point, then add any corp-ops-specific settings/extensions on top.
- **Where:** `corp-ops/.corp-ops.code-workspace` (new file at root).
- **Required `settings` keys:**
  ```json
  "explorer.sortOrder": "default",
  "explorer.sortOrderLexicographicOptions": "upper"
  ```
- **Why:** ADR-59 Decision 3 — every repo carries a dot-prefixed workspace with
  the standard sort settings so the root looks the same across repos.
- **Verification:** from `.dev-knowledge`, `python scripts/audit.py repo corp-ops`
  → `workspace_settings` PASS (and all 6 PASS). Confirm the file parses (open in
  VS Code) and the ALL-CAPS files cluster in the Explorer.
- **Commit suggestion:** `chore: add .corp-ops.code-workspace with ADR-59 sort settings`.

## Verification gates (post-execution)

- corp-ops `git status` clean; tests green (corp-ops `pytest`).
- From `.dev-knowledge`: `python scripts/audit.py repo corp-ops` → all 6 checks PASS.

## Estimated effort

~10–15 min, Sonnet / low. New workspace file from the template + verify.

## Operator decisions

None beyond ADR-59 defaults. (Whether to add corp-ops-specific extensions to the
workspace is optional polish on top of the required baseline.)

## What this plan does NOT include

- Any change to corp-ops source, ADRs, or governance content.
- Merging the pending `chore/universalization-2026-05-26` branch.
- Cross-repo modifications.
