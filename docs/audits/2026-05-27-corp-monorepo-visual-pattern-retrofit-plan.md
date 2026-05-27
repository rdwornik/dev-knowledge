---
type: retrofit-plan
scope: corp-monorepo visual-pattern conformance per ADR-59
date: 2026-05-27
basis: ADR-59 Universal Visual Repository Pattern
status: plan (consumed by a separate corp-monorepo session for execution)
contract: read-only inspection of corp-monorepo; writes confined to .dev-knowledge/docs/audits/
---

# corp-monorepo Visual-Pattern Retrofit Plan — 2026-05-27

Closes the ADR-59 gap(s) for `corp-monorepo`. This plan **executes nothing** — it
is consumed by a separate corp-monorepo Claude Code session with write access to
that repo. The `.dev-knowledge` session that authored it made zero changes to
corp-monorepo. corp-monorepo is the only one of the four with a real conformance
**FAIL** (the un-dotted `ruff.toml`).

## Current state (read-only inspection, 2026-05-27)

- Branch at inspection: `chore/universalization-2026-05-26` (HEAD `498590d`),
  clean. **Note:** not yet merged to `main` at inspection — re-verify HEAD/branch
  before executing. corp CLAUDE.md §4 forbids committing to `main` directly: use a
  feature branch.
- Root-level tracked files: `.corp-monorepo.code-workspace`, `.gitattributes`,
  `.gitignore`, `.pre-commit-config.yaml`, `pyproject.toml`, `ruff.toml`,
  `tach.toml`, `ARCHITECTURE.md`, `BACKLOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  `JOURNAL.md`, `VISION.md`.
- `ruff.toml` is present at root, **un-dotted**, lenient (`select = ["E","F","I"]`,
  `ignore = ["E501"]`). `pyproject.toml` **also** carries `[tool.ruff]` /
  `[tool.ruff.lint]` (lines 69/73) — a stricter, currently-dead config. This is the
  open CM-CF12 (duplication) + CM-D5 (`.ruff.toml` dot-prefix) pair from the
  2026-05-26 corp-monorepo audit; the ruff **strictness** decision was deferred
  (verification report D-CM3).
- `.corp-monorepo.code-workspace` exists and is dot-prefixed, but its `settings`
  block has **no `explorer.*` sort keys**.
- `tach.toml` is an ADR-59 dot-prefix **exception** (verified 2026-05-27: tach
  0.34.0 does not read `.tach.toml`) — leave it un-dotted.

## Projected ADR-59 audit findings

| Check | Status | Reason |
|---|---|---|
| `dot_prefix_discipline` | **FAIL** | `ruff.toml` is an un-dotted root config and is NOT on the exception list (`pyproject.toml`, `tach.toml` are exceptions; `.gitattributes`/`.gitignore`/`.pre-commit-config.yaml` already dotted) |
| `canonical_md_visibility` | PASS | VISION/ARCHITECTURE/CLAUDE/BACKLOG present, ALL-CAPS; CONTRIBUTING/JOURNAL correctly cased |
| `workspace_settings` | **WARN** | `.corp-monorepo.code-workspace` is dot-prefixed but missing both `explorer.sortOrder` and `explorer.sortOrderLexicographicOptions` |

**Net gap: ruff config (dot-prefix, entangled with the pending strictness decision) + workspace sort settings.**

## Gaps vs ADR-59

| Item | Current | Required | Action |
|---|---|---|---|
| `ruff.toml` | un-dotted standalone (lenient) + dead `[tool.ruff]` in pyproject | single ruff config source; if standalone kept, dot-prefixed `.ruff.toml` | Action 1 (gated on operator strictness decision) |
| Workspace sort settings | absent | `explorer.sortOrder: default` + `explorer.sortOrderLexicographicOptions: upper` | Action 2 |
| `tach.toml` | un-dotted | un-dotted (exception) | none |
| Config dot-prefix (others) | conformant | conformant | none |
| Canonical `.md` | conformant | conformant | none |

## Actions (sequenced)

### Action 1 — resolve the ruff config (closes CM-CF12 + CM-D5 + ADR-59 dot_prefix)
- **What:** pick ONE ruff config source, per the operator's strictness decision
  (still open from 2026-05-26):
  - **Path A — consolidate into `pyproject.toml`:** delete `ruff.toml`; keep the
    `[tool.ruff]` / `[tool.ruff.lint]` block as the single source. This **moots**
    the dot-prefix entirely (no standalone ruff config to dot-prefix) and satisfies
    `dot_prefix_discipline`. If the pyproject block is the stricter `E,F,I,W,B,UP`
    set, expect new lint findings — fix or re-scope in a **separate** commit, do not
    bundle a large lint diff with the consolidation.
  - **Path B — keep a standalone config:** `git mv ruff.toml .ruff.toml` (ruff reads
    `.ruff.toml`) and delete the dead `[tool.ruff]` block from `pyproject.toml` to
    remove the duplication. This satisfies `dot_prefix_discipline` via the dotted name.
- **Where:** `corp-monorepo/ruff.toml` and `corp-monorepo/pyproject.toml`.
- **Why:** ADR-59 Decision 1 (`ruff.toml` is not an exception — it must be dotted or
  removed) + CM-CF12 (duplication) + CM-D5 (dot-prefix).
- **Verification:** `git -C corp-monorepo ls-files | grep -E "ruff"` shows exactly
  one ruff config source (either `.ruff.toml` or none + pyproject block);
  `ruff check` passes under the chosen rule set; from `.dev-knowledge`
  `python scripts/audit.py repo corp-monorepo` → `dot_prefix_discipline` PASS.
- **Dependencies:** **gated on the operator strictness decision** (see Operator
  decisions). Use `git mv` for the rename path to preserve history.
- **Commit suggestion:** `chore: single ruff config + dot-prefix per ADR-59 (closes CM-CF12/CM-D5)`.

### Action 2 — add workspace sort settings
- **What:** add `"explorer.sortOrder": "default"` and
  `"explorer.sortOrderLexicographicOptions": "upper"` to the `settings` block of
  `.corp-monorepo.code-workspace`. Preserve all existing settings; add only these
  two keys. Remove any no-op `"explorer.sortOrderReverse"` if present (not a real
  VS Code setting — ADR-59 D4).
- **Where:** `corp-monorepo/.corp-monorepo.code-workspace` (`settings` object).
- **Why:** ADR-59 Decision 3.
- **Verification:** from `.dev-knowledge`, `python scripts/audit.py repo corp-monorepo`
  → `workspace_settings` PASS; ALL-CAPS files cluster in the Explorer.
- **Dependencies:** none.
- **Commit suggestion:** `chore: add explorer sort settings to workspace per ADR-59`.

## Verification gates (post-execution)

- corp-monorepo `git status` clean; tests green (corp `pytest -x --tb=short`);
  `tach check` still 0 violations; `ruff check` passes under the chosen rule set.
- From `.dev-knowledge`: `python scripts/audit.py repo corp-monorepo` → all 6 checks PASS.

## Risk register

- **ruff strictness flip (Action 1, Path A).** Consolidating to a stricter pyproject
  rule set may surface real lint errors across `src/corp/`. Decide strictness first;
  split any lint-fix diff from the config-consolidation commit.
- **`tach.toml` is an exception — do NOT dot-prefix it.** Renaming it to `.tach.toml`
  would break tach (verified: tach 0.34.0 cannot find `.tach.toml`).

## Estimated effort

~20–30 min, Sonnet / medium (more if Path A surfaces lint to fix). Largest of the
four retrofits because of the ruff entanglement.

## Operator decisions required before execution

1. **ruff strictness + config source (gates Action 1).** Path A (consolidate into
   `pyproject.toml`, possibly stricter — fix lint) or Path B (keep standalone, rename
   to `.ruff.toml`, delete dead pyproject block, lenient). Either resolves ADR-59
   `dot_prefix_discipline`; the strictness is the open question carried from 2026-05-26.

## What this plan does NOT include

- Any corp-monorepo source change other than ruff-strictness-driven lint fixes
  (Action 1, Path A) the operator opts into.
- The deferred CM-CF4 VISION routing-authority resolution (Council-gated — separate track).
- Merging the pending `chore/universalization-2026-05-26` branch.
- Cross-repo modifications.
