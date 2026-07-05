# ADR-51 Amendment 2026-07-05 — LLM-first canonical docs: Mermaid leaves canonical root docs

- **Status:** Proposed (authored in epic lane `llm-first-docs` [#259] under root conditional grant, ADR-97; the ROOT ratifies at integration — the lane does not self-accept)
- **Date:** 2026-07-05
- **Amends:** ADR-51 — authored as a **separate file** because this epic's grant treats ADR-51 as immutable (CLAUDE.md §5 item 3); ADR-51's in-file amendments 2026-05-22 / 2026-05-23 / 2026-05-28 / 2026-05-28-v2 / 2026-06-03 are point-in-time records and stay as written
- **Related:** ADR-39 (immutable dated artifacts), ADR-59 (visual repository pattern), ADR-97 (tree orchestration — the lane/grant mechanics this amendment was authored under)

## Context

ADR-51 and its amendments standardized a **graphical** (Mermaid) codemap as the canonical
form for `ARCHITECTURE.md`, then spent two follow-up amendments (2026-05-28 and
2026-05-28 v2) plus an audit check (#7 `mermaid_theme_directive`) making that Mermaid
*render legibly for a human on a black background*. The dominant reader of canonical root
docs has since shifted: they are consumed primarily by LLM agents (session boot, handoff
lanes, cross-repo audits), for whom a Mermaid block is the worst of both worlds — it costs
tokens for syntax and theme directives the reader ignores, encodes no fact that the
adjacent tables and prose don't already carry (verified for the hub: the two live blocks
are redundant with the codemap prose and the layer-role table), and drags a styling
enforcement surface (check #7) behind it.

Epic [#259] ("Epic 4 — LLM-first canonical docs") executes the shift. The direction was
frozen by root ruling in this epic's lane: the codemap **remains generated** —
derive-don't-maintain is not weakened by the format change.

## Decision

1. **Canonical root docs are LLM-first.** The canonical living docs (`VISION.md`,
   `ARCHITECTURE.md`, `CLAUDE.md`, `BACKLOG.md`, `CONTRIBUTING.md`, `JOURNAL.md`,
   `LESSONS.md`, `protocols/*`) are optimized for machine reading: flat prose, lists, and
   plain markdown tables. Constructs that carry meaning only through a human render layer
   — Mermaid and any other graphical-only encoding — **leave canonical docs**.

2. **The codemap stays GENERATED; only its output format changes.** The canonical codemap
   form (ADR-51 amendment 2026-05-22) becomes **compact text**: a module/layer list plus a
   dependency list (`from -> to`), carrying every fact the Mermaid form carried — modules,
   layer assignments from `tach.toml`, import edges, orphan and cycle classification, and
   per-module source paths. It is still written only by `scripts/codemap/cli.py
   generate --write` between the same `CODEMAP` markers; **hand-authoring the block is
   refused**; the `codemap-freshness` gate is retained and stays coherent with the new
   form (the check regenerates and diffs, format-agnostic). `mermaid_emit.py` is retained,
   no longer wired into the generator, as the natural emitter for the visualization
   surface in Decision 3.

3. **Visualization is a separate, human-facing surface (future Tier-4).** Diagrams are a
   rendering *of* canonical facts, produced on demand or stored outside canonical docs
   (ADR-59's visual repository pattern continues to govern that surface). The Mermaid
   high-contrast theme standard (amendment 2026-05-28 v2) is **not revoked** — it is
   re-scoped to that surface, as guidance rather than an audited gate.

4. **Audit check #7 (`mermaid_theme_directive`) is retired.** It asserts a styling
   standard for a construct canonical docs no longer carry. Retirement includes its
   pinning tests and fixtures. No replacement check asserts Mermaid absence: child-repo
   `ARCHITECTURE.md` files still carry legacy Mermaid codemaps until their per-repo
   migration (root-scheduled, out of this epic), and a presence-ban check would red every
   child on day one.

5. **The template follows.** `templates/ARCHITECTURE-template.md`'s codemap example and
   codemap note switch to the compact text form; a repo scaffolded from it carries no
   Mermaid codemap.

## Consequences

- Hub `ARCHITECTURE.md` renders zero Mermaid and carries the same dependency facts in
  text (the epic's done-contract hard metric).
- Child repos' existing Mermaid codemaps become legacy-form, tolerated (no gate asserts
  against them after #7 retires); each child migrates by regenerating with the updated
  tool — per-repo, root-scheduled.
- Consumer-facing carriers (`.pre-commit-hooks.yaml` exported `codemap-freshness` /
  `codemap-generate`, `deploy/manifest-v*.yaml` precommit carriers) are untouched by this
  epic; consumers pick up the text form when they bump their pinned rev / corpus version
  (root follow-up, ADR-91 territory).
- `CLAUDE.md` §4 ("Persistent diagrams in ARCHITECTURE.md are mermaid") and the §9
  `codemap-freshness` hook description go stale on merge; reconciled by root at
  integration (recorded ARCHITECT-REVIEW-PENDING in the epic return).

## Out of scope

Immutable dated artifacts keep their Mermaid as written (ADR-39). Non-canonical living
docs (e.g. `docs/handoffs/README.md`, which carries one Mermaid block) are not covered —
listed in the epic return for root disposition. No change to ADR-28/ADR-36 Layer-2
boundaries (the generator/validator distinction of amendment 2026-05-22 carries over
unchanged).
