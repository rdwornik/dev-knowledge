# C4 / codemap-generator requirements pack — fleet Mermaid inventory + generator degeneration root cause

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-12
- **Source-session:** night-batch N3
- **Status:** requirements-inventory

> Read-only inventory. Built for a human architect's open-web research on codemap/diagram
> generation (the "C4 repo-side half"). Every claim below carries a `file:line` / SHA / ticket-text
> cite, or is explicitly flagged `UNVERIFIED`. Repos in scope: hub `.dev-knowledge`; consumers
> `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation` (all under
> `C:\Users\1028120\Documents\Dev\`). No file was written or edited inside any git repo to produce
> this pack.

---

## 1. Fleet Mermaid diagram inventory

Method: fleet-wide search for `` ```mermaid `` fenced blocks (all 5 repos) + fleet-wide glob for
`*.mermaid` / `*.mmd` files. **12 live diagram instances** found; 0 in ai-council, 0 in
corp-sca-time-automation.

| Repo | File : line(s) | Purpose (1 line) | Complexity |
|---|---|---|---|
| corp-monorepo | `ARCHITECTURE.md:72-119` | Package/module codemap — canonical "what exists and how it relates" graph, hand-authored (10 nodes, 17 edges: cli/ingest/extractor/retrieve/project/opportunity/rfp/ops/schema/extraction) | branching |
| corp-monorepo | `ARCHITECTURE.md:275-291` | Tach 4-layer dependency-boundary diagram (interface → orchestration → core → foundation, 3 edges) | trivial linear |
| corp-monorepo | `docs/diagrams/container-module.mermaid` (88 lines, whole file) | C4-style container/module diagram: 4 layer subgraphs (L0-L3) + CLI node + 3 DB cylinders, ~19 nodes | multi-lane |
| corp-monorepo | `docs/diagrams/magistrala-pipeline.mermaid` (93 lines, whole file) | 4-phase data-pipeline diagram (Intake&Classify → Route&Record → Knowledge Extraction → Store&Query), ~20 nodes incl. side-channel DBs | multi-lane |
| corp-monorepo | `docs/diagrams/system-context.mermaid` (49 lines, whole file) | C4 system-context diagram: `corp` cluster (4 nodes) + external actors (Gemini, Claude, Obsidian Vault, MyWork, OneDrive, ops.db, index.db) | branching |
| corp-ops | `ARCHITECTURE.md:33-62` | Package/module codemap, hand-authored (6 nodes: tools/onedrive/gdrive/auth/common/config, 8 edges) | branching |
| corp-ops | `ARCHITECTURE.md:81-96` | Informal 3-layer diagram (interface → core → foundation, 2 edges) + 1 disconnected "parallel manual surfaces" annotation node | trivial linear |
| ai-council | — none — | Migrated OFF Mermaid to hand-authored compact text 2026-07-08 (commit `d5c4e25`, per BACKLOG `[#262]`); verified 0 `` ```mermaid `` hits and 0 `.mermaid`/`.mmd` files repo-wide | n/a |
| corp-sca-time-automation | — none — | Verified 0 `` ```mermaid `` hits and 0 `.mermaid`/`.mmd` files repo-wide | n/a |
| .dev-knowledge (hub) | `docs/handoffs/README.md:124-137` | LIVE/current operator-onboarding "sequence at a glance" run-loop diagram (8-step chain A→H + 2 dashed self-loops). Explicitly named as the sanctioned human-facing exception to the ADR-51 amendment 2026-07-05 Mermaid-leaves-canonical-docs rule (see comment at `:121-123`) | trivial linear |
| .dev-knowledge (hub) | `docs/handoffs/2026-06-12-dev-knowledge-session-3/README.md:62-75` | Same run-loop diagram shape, immutable older handoff-bundle snapshot (references `HANDOFF_BOOT.md`/`PROBES.md` instead of `PASTE_THIS.md`) | trivial linear |
| .dev-knowledge (hub) | `tests/test_coherence_integration.py:72-77` | 4-node toy fixture (`session start → boot → work → handoff`) embedded in a mock "Boot runbook" doc, used to test the coherence-doc enumerator | trivial linear |
| .dev-knowledge (hub) | `docs/audits/2026-06-25-dependency-architecture-coverage-audit.md:98-121` | "Visual dependency graph" — Specs/Dependents/Code edge map, 3 subgraphs, 8 nodes, solid=gated vs dotted=unenforced edge styling | multi-lane |
| .dev-knowledge (hub) | `docs/audits/2026-06-26-corpus-graph-justify-or-retire.md:284-316` | "Operational invocation spine" — trigger→script hook-firing graph fleet-wide, ~26 nodes, multi-target fan-out edges (`PC --> a & b & c & d & e`); densest diagram in the fleet | large-graph |

**Fleet count by repo:** corp-monorepo 5 · hub 5 · corp-ops 2 · ai-council 0 · corp-sca-time-automation 0.

**Non-diagram Mermaid-adjacent hits** (matched the search pattern, excluded from the count above —
recorded so the architect doesn't need to re-derive why):
- `scripts/codemap/mermaid_emit.py:115` — the retained-but-unwired generator function that emits a
  `` ```mermaid `` fence; this is tooling CODE, not a diagram instance.
- `tests/test_codemap.py:128,136` — `assert out.startswith("```mermaid\n")` string-prefix
  assertions on generator output; test code, not diagram content.
- `tests/test_coherence_enumerator.py:38` — a docstring sentence referencing the fenced-block
  pattern, no diagram.
- 6 `docs/audits/*.md` files (`2026-05-23-ai-council-deep-audit.md:67`,
  `2026-05-25-ai-council-universalization-audit-refresh.md:70`,
  `2026-05-25-ai-council-universalization-execution-plan.md:94`,
  `2026-05-26-corp-monorepo-execution-plan.md:113`,
  `2026-05-28-mermaid-readability-v2-verification.md:94`,
  `2026-05-28-final-state-and-process-diagrams-verification.md:65,101`) — immutable historical
  prose that quotes the literal string `` ```mermaid `` (usually inside a quad-backtick escape) while
  describing another file's state at audit time; not live fenced blocks in these files themselves.

Derived `.svg` artifacts (not separate diagram sources, rendered FROM the `.mermaid` files above):
`corp-monorepo/docs/diagrams/{container-module,magistrala-pipeline,system-context}.svg`, produced by
`corp-monorepo/scripts/render-diagrams.ps1` (invokes `mmdc`, the `@mermaid-js/mermaid-cli` CLI) —
see §4.

---

## 2. #262 / #295 codemap-generator limits — verbatim + code-level root cause

### 2a. Verbatim BACKLOG text

**`[#262]`** — `.dev-knowledge/BACKLOG.md:160` (P3, M):

> Child-repo codemap migration to compact-text form — the ADR-51 amendment 2026-07-05 moved the hub
> ARCHITECTURE codemap from Mermaid to compact text (the generator now emits text), but child repos
> (ai-council, corp-monorepo, corp-ops, corp-sca-time-automation) still carry legacy Mermaid
> codemaps... **corp child-leg (2026-07-11, G11 / #295 x-ref): corp-monorepo is the SECOND concrete
> failing layout — key correction to the plan-v3 premise: tach-presence does NOT rescue #262. The
> blocker is node-granularity: the generator's node = top-level dir under `src/`, and corp has
> exactly one (`src/corp/`), collapsing 13 subpackages to a single orphan node (0 edges). The fix
> must derive sub-module nodes from `src/<pkg>/<subpkg>/` and match `tach.toml` `corp.<subpkg>`
> layer keys (or use the AST import graph at that granularity), handling BOTH flat (ai-council #295)
> and single-package-with-subpackages (corp). Kill-candidate: if generator-managed codemaps are only
> ever pursued for genuinely multi-top-level-package repos, close #262/#295 for single-package and
> flat layouts and keep them HAND-AUTHORED by policy (corp ARCH L120 already says so).**

**`[#295]`** — `.dev-knowledge/BACKLOG.md:165` (P3, M):

> Codemap generator flat-layout support (ai-council pilot G4) — the codemap generator is
> package/`tach.toml`-based; on a flat single-package layout (e.g. ai-council `src/ai_council/*.py`,
> no `tach.toml`) `codemap generate` degenerates to a 2-orphan-module stub, discarding the real
> node/edge structure (`--write` would REGRESS the doc), so #262's generator-MANAGED intent is
> unreachable without adopting Tach (rejected — ai-council ARCHITECTURE L130). Derive module edges
> from the import graph (the AST walker already exists) instead of requiring `tach.toml`. Recurs at
> demo-prep / life-architect in Wave-2, not just corp-monorepo. Kill-candidate (per the gap-note): if
> only tach-bearing repos adopt generator-management, close this and let flat-layout repos stay
> HAND-AUTHORED by policy.

### 2b. Code walkthrough (generator internals)

Files: `.dev-knowledge/scripts/codemap/{ast_walker.py, generator.py, text_emit.py}`.

**Node (package) detection — `ast_walker.py:23-27`, inside `analyze_repo()`:**
```python
packages = sorted(
    p.name
    for p in src_dir.iterdir()
    if p.is_dir() and (p / "__init__.py").exists()
)
```
Two structural properties, both load-bearing for the degeneration:
1. **Non-recursive** — only `src_dir.iterdir()`, the immediate (depth-1) children of `source_root`.
   A package tree nested two-plus levels below `source_root` collapses to whichever directory sits
   at depth 1.
2. **Directory-with-`__init__.py` only** — a standalone top-level `.py` FILE is never a node, at any
   `source_root` depth.

**Edge detection — `ast_walker.py:44-46` (plain `import`) and `:56-58` (`from ... import`):**
```python
top = alias.name.split(".")[0]          # / node.module.split(".")[0]
if top in package_set and top != pkg_name:
    edge_set.add((pkg_name, top))
```
Matches only the FIRST dotted segment of an import statement against `package_set` (the depth-1
directory names). An edge is recorded only if that first segment is itself a recognized depth-1
package name, different from the importing file's own package.

**Orphan math — `generator.py:61-68`:**
```python
connected = set()
for src, dst in edges:
    connected.add(src); connected.add(dst)
orphans = [p for p in packages if p not in connected]
```
Whenever `len(packages) == 1`, the `top != pkg_name` guard in `ast_walker.py` is unsatisfiable for
*any* internal import (the only `top` that could be `in package_set` is the package itself, which
then always equals `pkg_name`) — so `edges` is **always `[]`**, so the single node is **always**
orphaned. This is a mathematical inevitability of the algorithm, not an edge-case bug: any repo with
exactly one depth-1 source directory produces a 1-node/0-edge graph by construction.

**Layer lookup — `generator.py:15-45` `_load_tach_layers()`:** builds `{tach.toml [[modules]].path:
layer}` keyed on the LITERAL dotted `path` string (e.g. `"corp.schema"`). `generate_codemap()` then
does `layers.get(pkg, "-")` where `pkg` is the depth-1 directory name (e.g. `"corp"`) — this never
matches a dotted key, so layer renders as `-` whenever node granularity differs from tach.toml's
module-key granularity.

### 2c. Why each layout degenerates, in code terms

**(a) ai-council — flat layout:** Confirmed live via `Glob` — `ai-council/src/` has exactly one
directory-with-`__init__.py` (`ai_council/`; the sibling `ai_council.egg-info/` has no
`__init__.py`). 13 real modules (`cli.py`, `debate.py`, `orchestrator.py`, `output.py`, `policy.py`,
`routing.py`, `runner.py`, `synthesis.py`, `models.py`, `metrics.py`, `healthcheck.py`, `inbox.py`,
`mode_detector.py`) are flat top-level `.py` FILES — invisible to the directory-only package filter
at any `source_root`. `ai-council/ARCHITECTURE.md:20-27` (hand-authored today) states the generator
"degenerates to a 2-orphan-module stub (providers, research)" — consistent with re-pointing
`--source-root` one level deeper to `src/ai_council` (ai-council's only two directories WITH
`__init__.py` below the flat layer: `providers/`, `research/`, confirmed via `Glob`). But
ai-council's internal imports are fully-qualified (`ai_council.providers...`), so the edge-match's
first-dotted-segment test yields `top="ai_council"`, never `in package_set={"providers","research"}`
→ 0 edges, both nodes orphaned. **Two independent failures compound:** flat `.py` files are
invisible to the node detector regardless of `source_root`, and re-pointing `source_root` to reach
the 2 real subpackages breaks edge-matching because internal imports are not written relative to the
new root.

**(b) corp-monorepo — single-top-level-package-with-subpackages:** Witnessed directly in G11 (§3,
verbatim) — default `source_root="src"` finds exactly ONE directory-with-`__init__.py`
(`src/corp/`), collapsing all 13 real subpackages (cli, ingest, extractor, retrieve, project,
opportunity, rfp, ops, schema, extraction, cleanup, overnight, …) into a single node `corp`; by the
orphan-math inevitability above, 0 edges follow automatically. Layer lookup fails too: `tach.toml`'s
`[[modules]]` are keyed `corp.schema`, `corp.extractor`, etc. (dotted, one level below the collapsed
node — see `corp-monorepo/tach.toml:32-179`), so `layers.get("corp", "-")` never matches → layer
`-`. Output: `| corp | - | src/corp/ | orphan |`, byte-identical to the G11 dry-run.

**(c) Bonus / previously-unnamed third instance — the hub's own self-hosted codemap:**
Live-witnessed at `.dev-knowledge/ARCHITECTURE.md:71-82` (current, in-repo, canonical per ADR-51
amendment 2026-07-05):
```
Modules (source root: `scripts/`; layer from tach.toml, `-` = unassigned):
| module | layer | path | flags |
|---|---|---|---|
| codemap | - | scripts/codemap/ | orphan |
| toc | - | scripts/toc/ | orphan |
Dependencies (`from -> to`; `[cycle]` marks an edge on an import cycle):
- (none)
```
`source_root="scripts"` (per `.pre-commit-config.yaml:30`, `entry: python -m scripts.codemap.cli
check . --source-root scripts`) finds only 2 directories-with-`__init__.py` directly under
`scripts/` — `codemap/` and `toc/` — and renders BOTH as orphans, 0 edges. `scripts/hooks/` is
excluded too (confirmed: `scripts/hooks/block_immutable_edits.py` exists but the directory has no
`__init__.py`). The 40+ flat top-level `.py` files under `scripts/` (`audit.py`, `fleet_health.py`,
`validate_backlog.py`, `reverse_dep_oracle.py`, etc. — the actual bulk of the hub's own tooling) are
entirely invisible to the generator, for the same structural reason as ai-council's flat files. **Not
named in #262, #295, or G11 as of this inventory** — flagged here as a directly-witnessed,
previously-undocumented finding: the hub's own "generator-managed, canonical" reference deployment
is itself a 2-orphan stub.

**Exported default confirms this is not an edge case:** `.dev-knowledge/.pre-commit-hooks.yaml:23-30`
(the `codemap-freshness` hook every consumer opts into) hard-codes `args: [--source-root, src]` as
the DEFAULT for every consumer — i.e. the setting that produces the degenerate 1-orphan (corp) /
flat-file-blind (ai-council-shaped) outcome is the shipped default, not a misconfiguration.

---

## 3. Corp G11 requirement text — verbatim

Source: `corp-monorepo/docs/intake/2026-07-10-runbook-gap-notes.md:57-92`
(section header `### G11 — #262 generator-managed codemap unreachable on a single-package layout
(NAMED / requirement-input)`):

> The plan-v3 premise was: *corp is tach-bearing (unlike ai-council's flat layout), so it can close
> the generator-MANAGED codemap owe #295 blocked on (n≥1)*. **Recon + this witness falsify it.**
> Running the generator (dry-run, no `--write`) against corp's `src/corp/` single-package layout:
> ```
> warning: orphan modules (no edges): corp
> | module | layer | path      | flags  |
> | corp   | -     | src/corp/ | orphan |
> Dependencies: (none)
> ```
> The generator collapses corp's **13 subpackages** (cli, ingest, extractor, retrieve, project,
> opportunity, rfp, ops, schema, extraction, cleanup, overnight, …) into a **single orphan `corp`
> node, 0 edges, layer `-`**. corp's hand-authored Mermaid codemap (`ARCHITECTURE.md` L71-121) is
> **10 nodes / ~17 edges / 4 layers**; `--write` would catastrophically regress it. So corp's config
> correctly **does not consume the codemap hooks** (`.pre-commit-config.yaml` note).
> - **Root cause:** the generator's module granularity is "top-level dir under `src/`". corp has ONE
>   such dir (`corp`), and its `tach.toml` layers are keyed at `corp.<subpkg>` (dotted, one level
>   BELOW the generator's node granularity), so every layer label is unassigned (`-`) and there are
>   no inter-module edges to draw.
> - **Same OUTCOME as ai-council G4/#295, different MECHANISM:** ai-council = flat, no `tach.toml`
>   (2-orphan stub); corp = single-package WITH `tach.toml` (1-orphan). **Being tach-bearing does not
>   rescue #262** — the blocker is node-granularity, not tach-presence. This is the key correction to
>   the plan-v3 assumption.
> - **Operator ruling this session:** contract item 5 → **BLOCKED / honest-partial**; the premise was
>   falsified by recon. corp does NOT close #262 this session. **Nothing written** (ARCHITECTURE.md
>   untouched; D4 codemap dimension stays deferred per the surface-only ruling — see below).
> - **Requirement input to the hub-side #262 fix (the deliverable):** the generator must derive
>   sub-module nodes from the package tree *below* the single `src/<pkg>/` root — i.e. treat
>   `src/corp/<subpkg>/` as the node granularity and match `tach.toml` `corp.<subpkg>` layer keys —
>   OR derive edges from the AST import graph (the existing `ast_walker`) at that sub-package
>   granularity. Then a tach-bearing single-package repo (corp) can be the n≥1 close. File alongside
>   ai-council's **#295** as the second concrete failing layout: **flat (ai-council)** AND
>   **single-package-with-subpackages (corp)** both degenerate; the fix must handle both.
> - **Kill-candidate per backpressure:** if generator-management is only ever pursued for genuinely
>   multi-top-level-package repos, close #295/#262 for single-package + flat layouts and let them
>   stay HAND-AUTHORED by policy (corp's L120 marker already says so). Decide before building the fix.

Cross-referenced by the same doc's D4 surfacing note (`:184-186,191`): "**Codemap dimension** —
coupled to **G11 / #262**: generator-managed codemap is BLOCKED on corp's single-package layout... The
codemap sub-dimension should wait on the #262 generator fix (G11) so the refresh and the
generator-adoption land coherently rather than twice."

Predates G11 (earlier corroborating record): `corp-monorepo/JOURNAL.md:112-117`
(`### 2026-06-03 — Consume hub doc-tooling hooks (ADR-71 pilot, first consumer)`) already documented
the same failure a month earlier: "the hub generator produces a strictly-worse 13-node ALL-orphan
graph (0 edges, 0 layers) on corp's single-package `src/corp/` layout — edge match keys on first
dotted import component (`corp` ≠ bare names) and tach layer keys are dotted vs bare nodes."

---

## 4. Existing fleet dependency-data machinery

Per-repo availability matrix:

| Repo | `tach.toml` | Own import-graph/AST tooling | ecosystem/ state (hub-side) | Pre-commit codemap hooks consumed |
|---|---|---|---|---|
| .dev-knowledge (hub) | absent | `scripts/codemap/ast_walker.py` (the generator itself — fleet's only AST import-edge extractor) + `scripts/reverse_dep_oracle.py` + `scripts/scan_undeclared_edges.py` (doc/code edge tooling, not a code/code graph) | n/a — is the hub | Self-consumes `codemap-freshness` at `--source-root scripts` (`.pre-commit-config.yaml:28-30`) — produces a 2-orphan stub live (§2c) |
| ai-council | absent (confirmed: no `tach.toml` at repo root) | none found | `ecosystem/ai-council/state.yaml` | None — no `codemap` reference in `ai-council/.pre-commit-config.yaml`; codemap is hand-authored compact text |
| corp-monorepo | **present** — 4 layers (`interface`/`orchestration`/`core`/`foundation`), keyed dotted `corp.<subpkg>`, `forbid_circular_dependencies = true`, `exact = true`; enforced via local `tach-check` pre-commit hook (`entry: tach check`) + CI | `tach` itself is an import-boundary CHECKER, not a graph EMITTER; `scripts/find_orphans.py` is a reference/dead-file scanner (AST-adjacent, not an import-edge graph) | `ecosystem/corp-monorepo/state.yaml` | Explicitly NOT consumed — `.pre-commit-config.yaml:53-60` comment names the identical degeneration reason; only `toc-freshness`/`toc-generate` consumed from the hub |
| corp-ops | absent | none found | `ecosystem/corp-ops/state.yaml` | No `.pre-commit-config.yaml` file exists at all (confirmed absent) |
| corp-sca-time-automation | absent | none found | `ecosystem/corp-sca-time-automation/state.yaml` | `.pre-commit-config.yaml` exists (373 bytes) but has zero `codemap` references |

**tach / import-graph summary:** only **1 of 5** repos has `tach.toml` (corp-monorepo); **0 of 5**
have a repo-owned import-graph EMITTER — the only import-graph-capable tool fleet-wide is the hub's
shared `scripts/codemap/ast_walker.py`, consumed optionally via the hub's exported
`.pre-commit-hooks.yaml` (`codemap-freshness` / `codemap-generate`, `language: script`, no pip
package — pure-stdlib, per `.pre-commit-hooks.yaml:14-17` "Generation stays LOCAL to the consumer:
each hook reads the consumer's own source tree and writes the consumer's own doc").

**Adjacent-but-distinct machinery worth flagging (do not conflate with an import/code graph):**
- `ecosystem/doc-code-edge.yaml` (hub-only) — a DOC↔CODE **rule-ID** edge registry: resolves
  `<!-- rule: ID -->` annotations in a curated `declaration_docs:` list against `# rule: ID` code
  annotations under `scripts/` (identity/AST resolution, move-safe). This is a doc-to-code
  traceability index, NOT a file→file or code→code dependency graph. Consumed by
  `scripts/validate_doc_code_edge.py` / `audit.py::check_doc_code_edge`.
- `ecosystem/<repo>/state.yaml` (hub-side, one per consumer + the hub's own conceptual record) —
  per-repo audit-check snapshot (floor integrity hash, canonical-freshness, deployed methodology
  version, etc.) as of `last_audit:`. Confirmed NOT replicated inside the consumer repos themselves
  (`ai-council/ecosystem/` and `corp-monorepo/ecosystem/` both absent) — it is hub-tracked-only. No
  file/code dependency content.
- corp-monorepo's diagram-RENDERING pipeline (distinct from graph EXTRACTION): `scripts/render-diagrams.ps1`
  (invokes `mmdc`, the `@mermaid-js/mermaid-cli` CLI, to render the 3 legacy `.mermaid` files under
  `docs/diagrams/` to paired `.svg` files) + `docs/diagrams/conventions.yaml` (hand-authored style
  budget: `max_nodes_per_layer: 4`, `max_edges_per_diagram: 15`, theme colors per layer — read by an
  LLM/human when hand-drawing, not consumed by any script).

---

## Summary for the architect (dense recap)

- **Fleet Mermaid count:** 12 live diagrams — corp-monorepo 5, hub 5, corp-ops 2, ai-council 0,
  corp-sca-time-automation 0.
- **Root cause (one sentence):** the generator's node = "directory with `__init__.py` directly
  under `source_root`" (non-recursive) and its edge-matcher keys on an import's first dotted
  segment against that same depth-1 name set — so any repo with exactly one depth-1 package
  (corp-monorepo, and the hub's own `scripts/`) is mathematically forced to 0 edges, and any repo
  whose real modules are flat top-level `.py` files (ai-council, and again the hub's own `scripts/`)
  never gets those files counted as nodes at all, regardless of `source_root`.
- **G11 quote:** `corp-monorepo/docs/intake/2026-07-10-runbook-gap-notes.md:57-92`, verbatim in §3
  above — key line: "corp's config correctly **does not consume the codemap hooks**"; "**Being
  tach-bearing does not rescue #262** — the blocker is node-granularity, not tach-presence."
- **tach/import-graph matrix:** corp-monorepo = tach present (checker only, no emitter); ai-council /
  corp-ops / corp-sca-time-automation = neither tach nor any import-graph tooling; hub = no tach, but
  owns the fleet's only AST import-edge extractor (`scripts/codemap/ast_walker.py`), which is itself
  degenerate on the hub's own layout (§2c).
