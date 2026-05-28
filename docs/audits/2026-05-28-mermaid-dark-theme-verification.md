---
date: 2026-05-28
type: verification
scope: cross-repo
status: complete
owner: Rob
---

# Mermaid dark-theme directive — cross-repo verification

## Summary

Every Mermaid block in every covered repo's `ARCHITECTURE.md` (and the
`.dev-knowledge` ARCHITECTURE template) now carries
`%%{init: {'theme':'dark'}}%%` as the first line inside the fence. The
codemap generator emits the directive automatically. ADR-51 amended to
codify the standard.

Operator does the final visual render confirmation on the black VS Code
background.

## Per-repo result

| Repo | Mermaid blocks | Directives | Generator updated | Hand-edits | Notes |
|---|---:|---:|---|---:|---|
| .dev-knowledge | 6 | 6 | yes (`scripts/codemap/mermaid_emit.py`) | 5 | codemap regenerated; test fixture updated |
| ai-council | 2 | 2 | n/a | 2 | both blocks hand-authored ("not generator-managed") |
| corp-ops | 2 | 2 | n/a | 2 | both blocks hand-authored |
| corp-monorepo | 2 | 2 | n/a | 2 | both blocks hand-authored |
| corp-sca-time-automation | 0 | 0 | n/a | 0 | no Mermaid blocks present |

Total: 12 Mermaid blocks across 4 repos, 12 directives, 1 generator updated.

## Generator change (.dev-knowledge)

`scripts/codemap/mermaid_emit.py` `emit_mermaid()` now prepends
`%%{init: {'theme':'dark'}}%%` to the line list before `flowchart TD`.
Fixture `tests/fixtures/codemap-arch-clean/ARCHITECTURE.md` updated to
match the new output. All 85 tests pass.

Per-repo regeneration discovery: ai-council, corp-ops, and corp-monorepo
CODEMAP blocks are **hand-authored** (existing trailer comment:
"hand-authored Mermaid codemap per ADR-51 amendment 2026-05-22; not
generator-managed"). Running the generator on those repos would replace
the rich hand-curated structure with an orphan-only single-node graph
(because their source layouts don't produce the imports the AST walker
expects). Generator regen was reverted in all three; directive added
in-place instead.

## Template

`templates/ARCHITECTURE-template.md` canonical codemap example now
includes the directive — new repos adopting the template inherit it.

## ADR

`docs/decisions/ADR-51-architecture-doc-convention.md` — **Amendment
2026-05-28** appended. Codifies the directive as standard, names the
out-of-scope set (immutable dated artifacts per ADR-39), documents the
custom-base `themeVariables` variant as a per-block escape hatch.

## audit.py check — deferred

A `mermaid_theme_directive` check (every tracked-`.md` mermaid block in
this repo starts with the init directive) was considered. Deferred to
BACKLOG: the check needs careful scoping (exclude immutable
`docs/audits/`, `docs/decisions/` ADR bodies which legitimately quote
historic Mermaid as-was) and a fixture suite before it can be merged
safely. Tracked as P3 in BACKLOG.

## Out of scope (NOT modified)

- `docs/audits/*.md` and `docs/decisions/ADR-*.md` Mermaid quotations
  — immutable dated artifacts per ADR-39 / CLAUDE.md §5. New artifacts
  going forward should include the directive.
- SVG diagrams (none in current scope).
- corp-sca-time-automation — no Mermaid present.

## Branches awaiting operator merge

```
.dev-knowledge          fix/mermaid-dark-theme-2026-05-28  (4 commits)
ai-council              fix/mermaid-dark-theme-2026-05-28  (1 commit)
corp-ops                fix/mermaid-dark-theme-2026-05-28  (1 commit)
corp-monorepo           fix/mermaid-dark-theme-2026-05-28  (1 commit)
```

Operator merges with `git merge --no-ff` in each repo independently.

## Operator final step

Open each `ARCHITECTURE.md` in VS Code (black background) and confirm
the diagrams now render with light/readable text. If any block still
reads poorly, switch that block (or the standard) to the custom-base
`themeVariables` variant documented in the ADR-51 amendment.
