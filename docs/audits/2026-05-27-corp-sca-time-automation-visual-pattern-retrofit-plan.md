---
type: retrofit-plan
scope: corp-sca-time-automation visual-pattern conformance per ADR-59
date: 2026-05-27
basis: ADR-59 Universal Visual Repository Pattern
status: plan (consumed by a separate corp-sca-time-automation session for execution)
contract: read-only inspection of corp-sca-time-automation; writes confined to .dev-knowledge/docs/audits/
---

# corp-sca-time-automation Visual-Pattern Retrofit Plan — 2026-05-27

Closes the ADR-59 gap(s) for `corp-sca-time-automation`. This plan **executes
nothing** — it is consumed by a separate corp-sca-time-automation Claude Code
session with write access to that repo. The `.dev-knowledge` session that authored
it made zero changes to corp-sca-time-automation.

## Current state (read-only inspection, 2026-05-27)

- Branch at inspection: `chore/universalization-2026-05-26` (HEAD `7d0dddc`),
  clean. **Note:** not yet merged to `main` at inspection — re-verify HEAD/branch
  before executing.
- Root-level tracked files: `.gitignore`, `requirements.txt`, `run.py`,
  `ARCHITECTURE.md`, `BACKLOG.md`, `CLAUDE.md`, `VISION.md`.
- **No `.code-workspace` file exists** (workspace add was deferred during the
  2026-05-26 universalization — verification report D-CO2 / same rationale).
- This repo uses `requirements.txt` (no `pyproject.toml`); `requirements.txt` is
  an ADR-59 dot-prefix **exception** (stays un-dotted).

## Projected ADR-59 audit findings

| Check | Status | Reason |
|---|---|---|
| `dot_prefix_discipline` | PASS | `requirements.txt` is an exception; `run.py` is not a config; `.gitignore` already dotted |
| `canonical_md_visibility` | PASS | the four mandatory files present, ALL-CAPS |
| `workspace_settings` | **FAIL** | no `.code-workspace` file at root |

**Net gap: create the workspace file.**

## Gaps vs ADR-59

| Item | Current | Required | Action |
|---|---|---|---|
| Workspace file | absent | `.corp-sca-time-automation.code-workspace` with required sort settings | Action 1 |
| Config dot-prefix | conformant | conformant | none |
| Canonical `.md` | conformant | conformant | none |

## Actions (sequenced)

### Action 1 — create the dot-prefixed workspace file
- **What:** create `corp-sca-time-automation/.corp-sca-time-automation.code-workspace`
  with a `folders` entry (`{ "path": "." }`) and a `settings` block containing the
  two required keys. Seed from `templates/workspace-*.code-workspace`, then add any
  repo-specific settings on top.
- **Where:** `corp-sca-time-automation/.corp-sca-time-automation.code-workspace` (new file).
- **Required `settings` keys:**
  ```json
  "explorer.sortOrder": "default",
  "explorer.sortOrderLexicographicOptions": "upper"
  ```
- **Why:** ADR-59 Decision 3 — dot-prefixed workspace + standard sort settings.
- **Verification:** from `.dev-knowledge`,
  `python scripts/audit.py repo corp-sca-time-automation` → `workspace_settings`
  PASS (and all 6 PASS). Confirm the file parses in VS Code.
- **Commit suggestion:** `chore: add .corp-sca-time-automation.code-workspace with ADR-59 sort settings`.

## Verification gates (post-execution)

- corp-sca-time-automation `git status` clean; tests green (`pytest`).
- From `.dev-knowledge`: `python scripts/audit.py repo corp-sca-time-automation` → all 6 checks PASS.

## Estimated effort

~10–15 min, Sonnet / low. New workspace file from the template + verify.

## Operator decisions

None beyond ADR-59 defaults.

## What this plan does NOT include

- Any change to corp-sca-time-automation source, ADRs, or governance content.
- Merging the pending `chore/universalization-2026-05-26` branch.
- Cross-repo modifications.
