# corp-monorepo Cross-Repo Coherence — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 5. **READ-ONLY** — zero modifications to
corp-monorepo (ADR-41). All findings → `.dev-knowledge/BACKLOG.md` with
`owner: corp-monorepo`.

## Health snapshot (Dimension D)

| Signal | Value |
|---|---|
| Working tree | clean |
| Branch (HEAD) | `chore/extract-p1-2-to-backlog-2026-05-28` (**not main**) |
| Tests collectable | **2554** (collected in 18.5s, not run) |
| CLAUDE.md | v2.2 (2026-05-27), ≤200-line single canonical, references `../.dev-knowledge/protocols/{ESSENTIALS,PLAYBOOK}.md` |
| Recent commits | sane — mermaid-readability-v2, ruff hook bump v0.4.0→v0.15.8, VISION routing amendment, P1-2 extraction |

Overall: **green**. The repo is healthy and correctly anchored to the universal
`.dev-knowledge` governance layer.

## Findings

| ID | Sev | Dim | Evidence | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| CM-1 | medium | C/D | corp-monorepo `git` HEAD = `chore/extract-p1-2-to-backlog-2026-05-28`; tip `a1007b1` | The P1-2 path-traversal finding **was** extracted to corp-monorepo BACKLOG (commit `a1007b1`, "extract P1-2 path traversal finding from verify branch (pre-delete gate)") — Dimension C confirmed landed. But it sits on an **unmerged feature branch**; corp-monorepo's HEAD is not on main. Operator should merge it (and confirm the source `verify` branch can be deleted). | Merge `chore/extract-p1-2-to-backlog-2026-05-28` → main in corp-monorepo; resolve the pre-delete gate. | corp-monorepo |
| CM-2 | low | A | corp-monorepo `CLAUDE.md:§1` step 4 ("Most recent `docs/handoffs/*.md`") | corp-monorepo's session-start contract still points at the **flat `docs/handoffs/*.md`** pattern (pre-ADR-42 folder format). Confirms the existing `.dev-knowledge` BACKLOG P3 item "docs/HANDOFF.md flat file deprecation (corp-monorepo, ai-council)" is still live. Not breaking — parallel pattern persists. | At next corp-monorepo handoff event, migrate to the ADR-42 folder format + update CLAUDE.md §1 step 4. (Already tracked; this re-confirms.) | corp-monorepo |

## Cross-reference validation (Dimension A)

`.dev-knowledge` references "corp-monorepo" across ARCHITECTURE.md, CLAUDE.md,
BACKLOG.md (live) and ~15 audit files (immutable, point-in-time — out of scope to
re-validate). Spot-check of the **live** references:

- `CLAUDE.md` — names corp-monorepo as a child repo / out-of-scope example. Accurate.
- `ARCHITECTURE.md` — names it as a Layer-1 code repo. Accurate.
- `BACKLOG.md` — tier-deprecation + flat-handoff items target it. Accurate (match the
  repo's actual state: CLAUDE.md v2.2 still uses tier-free framing; flat handoff per CM-2).

No broken or stale live cross-reference found.

## ADR compliance (Dimension B)

- **ADR-39 (immutability):** corp-monorepo carries `docs/decisions/ADR-*.md`; recent
  commits supersede via new docs/journal entries, not in-place edits (consistent).
- **ADR-41 (ownership):** corp-monorepo owns its own BACKLOG; the `.dev-knowledge`
  "Apply tier-deprecation to corp-monorepo" P1 is a *dissemination* directive from the
  governance layer, not a cross-repo edit — consistent with the Layer-2 prescriptive
  model. (No action; noted for the goals/ownership picture.)

## Notes

- Nothing in corp-monorepo was modified. CM-1/CM-2 are operator/own-repo actions.
- corp-monorepo's ruff-hook bump (v0.4.0→v0.15.8) is the same ruff version the
  ecosystem-hooks audit (HK-1/HK-4) found `.dev-knowledge` lacks entirely — corp-monorepo
  is ahead of `.dev-knowledge` on lint enforcement.
