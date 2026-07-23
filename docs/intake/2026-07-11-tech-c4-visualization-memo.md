---
intake-id: 10
status: DRAFT
origin: architect research memo (open-web research synthesis), 2026-07-11 — input for the deferred system-visualization work
consumers: "the deferred system-visualization work (#326 ruling / #165)"
---

> **Intake note:** Operator-accepted architect research memo; input for the deferred system-visualization work (#326 ruling / #165); recommendations narrowed by the 2026-07-11 operator ruling — ARCHITECTURE.md is CC-facing, visualization deferred wholesale.

# C4 / Codemap Visualization — Architect Research Memo

> Phase 4 deliverable (standing debt, ~4× overdue). Unblocks: #165 (Mermaid/ToC diagram-selection ruling) and #322 leg b (fleet-dashboard visualization layer).
> Requirements base: `docs/audits/2026-07-12-technical-night-c4-requirements.md` — fleet Mermaid inventory = 12 · ast_walker node-granularity root-cause · per-repo tach matrix · hub codemap = 2-orphan stub.
> Sources: open-web research 2026-07-11 (Structurizr docs, Mermaid docs + issue tracker, GitHub community discussions, 2026 tool comparisons). Synthesized, not a link dump.

## The landscape in one paragraph

Three families exist. **(1) Embedded diagrams-as-code** (Mermaid, PlantUML): text in markdown, renders where the docs live, no model semantics. **(2) Model-based C4** (Structurizr DSL — the reference implementation by the C4 author; LikeC4 as the younger Node-native alternative): one model, many derived views, no duplication between levels; Structurizr exports to Mermaid/PlantUML/DOT and now ships an MCP server aimed at LLM agents. **(3) Source-aware generators** (repowise-class tools): infer architecture from the repo. Notably, even the model-based tools have **no drift detection** — nothing checks the model against the code. Our fleet already has the missing piece the market lacks: the codemap-freshness gate. The question is what the gate should regenerate.

## Findings that bind the decision

**F1 — Mermaid's C4-specific syntax is a dead end for us.** It is officially experimental, style-fixed (no theming — our custom dark theme wouldn't apply), layout is manual-order-driven and widely reported as poor (open layout/overlap bugs as of 2026), and host rendering is inconsistent — a June 2026 GitHub community thread documents that GitHub's bundled Mermaid does not render the C4 extension. Verdict: **C4 as a Mermaid syntax: NO.**

**F2 — Plain Mermaid (flowchart/subgraph) remains the only diagram form that renders natively everywhere our docs live** (GitHub, VS Code preview), version-controls cleanly, and accepts our custom dark theme (the 2026-05-28 v2 rollout). The fleet already carries 12 of them.

**F3 — The codemap degeneration is a generator problem, not a renderer problem.** The requirements pack pins the root cause in ast_walker node granularity: walking at AST-node level yields either noise or (post-filter) the 2-orphan stub. No diagram tool fixes a wrong graph. The correct granularity source already exists per-repo: **tach.toml module boundaries** (the per-repo tach matrix) — modules and their allowed dependencies are exactly a C4 component-level graph, machine-derived and already gate-adjacent.

**F4 — C4's real value for us is the level convention, not a toolchain.** Mapping: fleet map = Context (L1), repo = Container (L2), tach module = Component (L3), code = L4 (skip — industry consensus and our own practice). This vocabulary costs nothing and structures both docs and the dashboard.

**F5 — Structurizr DSL is the best model-layer candidate *if* we ever need one**: text-based, diff-friendly, LLM-generatable (explicitly positioned for AI agents, MCP server available), model-once-render-many with Mermaid export. Costs: a new toolchain dependency (Java/Docker for rendering or the cloud), a second source of truth to keep honest, and its multi-view payoff only materializes when several views derive from one model — which our single-diagram-per-repo convention doesn't need yet. LikeC4 is lighter (Node/VS Code) but younger and non-reference.

## Recommendation (one)

**Keep Mermaid (plain flowchart + our custom dark theme) as the fleet's only embedded diagram standard, and fix the generator: rebuild codemap generation to derive the module graph from tach.toml boundaries (Component level, F3), emitted as plain Mermaid. Adopt C4 as a naming/level convention only (F4). Do not adopt Structurizr or any model layer now; re-open only on a concrete multi-view need, with Structurizr DSL as the pre-selected candidate (F5).**

Consequences:
- **#165 ruling (proposed):** Mermaid confirmed as the diagram standard; Mermaid-C4 syntax explicitly rejected (F1); ToC and codemap both stay in the existing generator+gate pattern.
- **Codemap fix becomes a bounded build ticket:** generator reads tach.toml (fallback for reposwithout tach: package-level import graph), emits flowchart Mermaid, codemap-freshness gate unchanged. This retires the 2-orphan stub and the ast_walker root cause in one move.
- **#322 leg b (dashboard):** the dashboard consumes the same generated graph data (emit JSON alongside Mermaid from the same generator run — one derivation, two renderings). Fleet level (Context) = registry + deployed-versions.yaml; repo level (Container/Component) = the per-repo generated graph. No new visualization toolchain; HTML+embedded Mermaid or a thin JS render over the JSON, decided at #322 build time.

## Trade-offs accepted
- We forgo model-once-render-many (Structurizr's strength) — acceptable while the convention is one diagram per repo per level.
- Plain-flowchart C4 conventions are less semantically explicit than C4 syntax — mitigated by classDef styling conventions (person/system/container classes) codified once in the hub and carried.
- tach-derived graphs show *declared* boundaries, not every import — that is a feature (the sanctioned architecture), with the import-edges audit check already covering the divergence.

## Operator decision requested
Approve → #165 gets ruled with the wording above; the codemap-generator rebuild gets filed as a bounded build ticket (candidate first pilot task for the Codex-producer axis, Phase 5/EPIC-H); #322b inherits the same-source-JSON design constraint.
