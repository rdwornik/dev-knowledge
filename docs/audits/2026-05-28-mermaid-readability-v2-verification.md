---
date: 2026-05-28
type: verification
scope: cross-repo
status: complete
owner: Rob
supersedes: 2026-05-28-mermaid-dark-theme-verification.md (operationally)
---

# Mermaid readability v2 — root-cause diagnosis + custom-theme rollout

## Summary

The 2026-05-28 v1 fix (bare `%%{init:{'theme':'dark'}}%%`) only made
the .dev-knowledge layer-model diagram readable; the workflow / council /
handoff process diagrams still rendered gray-on-black. This session
diagnosed the root cause, replaced the bare directive with a custom
`themeVariables` block ecosystem-wide, and added explicit `color:`
overrides to every `classDef` that previously relied on theme defaults.
ADR-51 amended (v2 amendment 2026-05-28) to codify the new standard.

## Root-cause diagnosis

Comparing the block that worked (.dev-knowledge layer model, L47) to the
three that didn't (workflow L164, council L216, handoff L273):

| Block | classDefs pin `color:` ? | Result with bare `'dark'` |
|---|---|---|
| Layer model | YES — `color:#000` / `color:#222` | Readable |
| Ecosystem extended | YES | Readable |
| Workflow | **NO** | Light theme default on light pastel fill → invisible |
| Council pipeline | **NO** | Same |
| Handoff process | **NO** | Same |
| Codemap (orphan classDef) | NO | Faded |

`%%{init:{'theme':'dark'}}%%` flips Mermaid's default text color toward
light. classDefs that set `fill:` to a light pastel (`#bde0fe`,
`#fff3bf`, etc.) but omitted `color:` inherited that light default →
light-on-light → unreadable. The layer-model block worked because its
classDefs already pinned `color:#000`/`#222`.

The prompt's literal recipe ("change `color:#000` → `color:#f0f0f0`")
would have inverted the already-working blocks. The correct fix —
confirmed with operator before applying — is the opposite: keep light
pastel fills, **add** explicit dark `color:` where missing, and switch
the directive to a custom `themeVariables` form that fixes edge labels,
subgraph titles, and overall canvas contrast.

## Fix applied

1. **Directive** — every block now begins with:
   ```
   %%{init: {'theme':'base', 'themeVariables': {'darkMode':true,'background':'#1a1a1a','primaryColor':'#2d2d3d','primaryTextColor':'#f0f0f0','primaryBorderColor':'#8a86ff','lineColor':'#a0a0ff','textColor':'#f0f0f0','mainBkg':'#2d2d3d','secondaryColor':'#3d2d3d','tertiaryColor':'#22323a','clusterBkg':'#222232','clusterBorder':'#555577','edgeLabelBackground':'#1a1a1a','titleColor':'#f0f0f0','nodeBorder':'#8a86ff'}}}%%
   ```
2. **Explicit `color:` on every classDef with a light-pastel `fill:`** —
   mapping (applied uniformly across all repos):
   | Fill | Color |
   |---|---|
   | `#bde0fe`, `#a5d8ff`, `#74c0fc` | `color:#000` |
   | `#e8e8e8`, `#fff3bf`, `#d8f5a2`, `#ffe3e3`, `#fff5f5`, `#ffd8a8`, `#fff5f5` | `color:#222` |

## Per-repo result

| Repo | Mermaid blocks | Directive updated | classDef `color:` added | Branch |
|---|---:|---:|---:|---|
| .dev-knowledge | 6 | 6 | 3 process diagrams + generator's `_ALL_CLASS_DEFS` (5 classDefs) | `fix/mermaid-readability-v2-2026-05-28` |
| ai-council | 2 | 2 | 2 classDef blocks (foundation/core/orch/interface/output) | `fix/mermaid-readability-v2-2026-05-28` |
| corp-ops | 2 | 2 | 2 classDef blocks (foundation/core/interface[+parallel]) | `fix/mermaid-readability-v2-2026-05-28` |
| corp-monorepo | 2 | 2 | 2 classDef blocks (foundation/core/orch/interface) | `fix/mermaid-readability-v2-2026-05-28` |

Total: 12 Mermaid blocks across 4 repos; 12 directives swapped; ~14
classDef declarations gained explicit `color:`.

## Generator + template + ADR

- **Generator** (`.dev-knowledge/scripts/codemap/mermaid_emit.py`):
  module-level `_THEME_DIRECTIVE` constant now holds the custom-base
  themeVariables string; `_ALL_CLASS_DEFS` gained `,color:#000` /
  `,color:#222` on every entry. Test fixture
  `tests/fixtures/codemap-arch-clean/ARCHITECTURE.md` refreshed.
  85/85 tests pass; ruff clean; `scripts/audit.py health` green;
  codemap-freshness pre-commit hook passes.
- **Template** (`.dev-knowledge/templates/ARCHITECTURE-template.md`):
  canonical example uses the new directive + color-pinned classDefs.
- **ADR-51** — **Amendment 2026-05-28 (v2)** appended; supersedes the
  bare `'dark'` standard from the v1 amendment same date. Documents
  root cause, new directive, the explicit-color companion rule, and
  the fill→color mapping table.

## Verification commands

```
grep -c "theme':'base'" ARCHITECTURE.md     # equals
grep -c '```mermaid'    ARCHITECTURE.md
grep -n "fill:#" ARCHITECTURE.md | grep -v "color:#"   # must be empty
```

Run in each repo's ARCHITECTURE.md.

## Out of scope (NOT modified)

- `docs/audits/*.md`, `docs/decisions/ADR-*.md` Mermaid quotations —
  immutable dated artifacts per ADR-39 / CLAUDE.md §5.
- SVG diagrams (none in current scope).
- corp-sca-time-automation — no Mermaid blocks present (confirmed v1).

## Branches awaiting operator merge

```
.dev-knowledge   fix/mermaid-readability-v2-2026-05-28  (2 commits)
ai-council       fix/mermaid-readability-v2-2026-05-28  (1 commit)
corp-ops         fix/mermaid-readability-v2-2026-05-28  (1 commit)
corp-monorepo    fix/mermaid-readability-v2-2026-05-28  (1 commit)
```

No deferrals. Operator merges with `git merge --no-ff` in each repo.

## Operator final step — HARD METRIC

Open each `ARCHITECTURE.md` in VS Code on a black background. Every
diagram — not just the layer model — must show readable node text
**and** readable edge labels. The previous v1 gray-on-black symptom
must be gone. This is the closure test.
