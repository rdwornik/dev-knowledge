# Building One Queryable Dependency/Ontology Graph Across a Small Multi-Repo Python Fleet

## TL;DR
- **Build the graph as a committed, regenerated JSONL "edge log" that every existing validator emits into, queried through DuckDB (with recursive CTEs) or stdlib SQLite, and exposed to agents via a thin CLI plus an optional local stdio MCP wrapper — not a new database platform, not a running server, not a SaaS.** The single highest-leverage step is closing the task↔file gap (164 of 169 open rows lack `footprint:`), because it lights up the human-work-to-file layer, and combined with the already-free import graph (grimp) it makes blast-radius and orphan queries answerable immediately.
- Most of your fragments (reconciled_with edges, parity manifest, carrier manifests, serialize-groups, doc-claims, ADR-101 tokens, grimp import graph) are **already mechanisms** — the work is not to rebuild them but to make each one *also emit typed edges into one common file*, then query the union. The genuinely manual/curated pieces are the task↔file `footprint`, decision↔code, and requirement↔code links; the empirical literature is unambiguous that these hand-maintained links decay and must be guarded by CI orphan-detection to stay useful.
- Code-side extraction has a clear 2026 answer: **grimp for the durable Python import graph** (module granularity, embeddable, committable), optionally **Aider-style tree-sitter repo-map / a code-index MCP** for symbol-level def/ref, and SCIP/scip-python only if you need compiler-precise cross-repo symbol resolution. Kùzu — the obvious embedded Cypher store — was **archived on October 10, 2025 after Apple acquired the company**, so treat it as a maintenance risk and prefer DuckDB or SQLite.

## Key Findings

### The doctrine fit
Your constraints (library-first, local-first, no SaaS, no server, mechanisms-over-prose) sharply narrow the field. The winning architecture is **derive-and-commit**: source-of-truth stays in git-native markdown/YAML/JSON, and a gate regenerates a committed graph artifact from those sources. This keeps every edge reproducible from source "in seconds," avoids a running server, and makes the graph a first-class reviewable diff. It also aligns with your "input → function → output" mental model: nodes are artifacts/files/symbols/decisions/tasks; edges are typed relationships; queries are graph traversals.

### The evidence on whether this is worth it
The 2025–2026 literature has moved from hype to measured results, and it is genuinely mixed — both sides matter:
- **Pro-graph:** A controlled ablation ("Code Isn't Memory," arXiv 2606.22417) found a structural codebase index inside a fixed coding-agent harness produced a large localization gain and a statistically separated resolve gain **at no cost penalty and lower cost-per-solve** ($2.30 mean vs. OpenCode's $2.92, favorable on $/solved), with the biggest wins on multi-file changes (91.3% acc@5 ON vs. 44.9% OFF in the 3+ gold-file bucket). "Codebase-Memory" (arXiv 2603.27277) reports 83% answer quality vs 92% for a file-exploration agent at **~10× fewer tokens and 2.1× fewer tool calls**. "CodeCompass" reports a 23.2-point improvement on hidden-dependency tasks (99.4% vs 76.2%).
- **Anti-graph / nuance:** The same CodeCompass work found **plain BM25 retrieval was optimal for semantic tasks** (100% ACS, zero variance) and the graph did not beat it there. "CodeAnchor" (arXiv 2606.26979) argues in-band comment anchors that the existing grep loop finds may beat external graphs "at current model strength," treating graphs as complementary not superior. Anthropic itself still ships grep-only retrieval in Claude Code as of these reports. The honest reading: **graphs win decisively for multi-hop, cross-file, "what breaks if I change X" structural questions and lose or tie for semantic/keyword lookup** — which maps exactly onto your stated use case ("show me the network of dependencies for X").
- On traceability specifically, the strongest empirical evidence is Mäder & Egyed's controlled experiment (*Empirical Software Engineering* 20(2):413–441, 2015): with **71 subjects solving 461 real maintenance tasks, those with traceability performed on average 24% faster and created on average 50% more correct solutions**. But a 2023 survey (Ruiz et al., "Why don't we trace?", *Requirements Engineering*, DOI 10.1007/s00766-023-00408-9; 55 survey participants + 14 interviews) found traceability is "still widely perceived as a costly, manual activity," and ReqToCode (arXiv 2603.13999) warns verbatim that "stale links are not merely useless but actively harmful when they mislead developers about the system's actual structure." This is the empirical mandate for your mechanisms-over-prose doctrine: derive links where possible, and gate the hand-authored ones.

---

## Details by Research Question

### 1. Code-side graph extraction
| Tool | What it produces | Durable/committable? | Multi-repo / cross-repo | Maintenance (2025–26) | Cost |
|---|---|---|---|---|---|
| **grimp** | Directed **import graph** of modules within one or more top-level packages; rich Python API (`find_upstream_modules`, `find_descendants`, `find_shortest_chains`) | Yes — build in-process, serialize edges to JSON/JSONL yourself; default `.grimp_cache` | `build_graph` accepts multiple packages; joins by module name | **Actively maintained; grimp 3.14 is current on PyPI** ("Builds a queryable graph of the imports within one or more Python packages", BSD), powers import-linter 2.x | **S** |
| **pydeps** | Import graph, cycle detection, SVG/PNG viz | Viz-oriented; finds imports via bytecode import-opcodes (only imported/installed files) | Weak cross-repo | Maintained; 3.0.x series, Python 3.8+ | S |
| **import-linter** | Not an extractor — a *contract checker* built on grimp (layers/forbidden/independence) | Config file, not a graph artifact | Multiple root packages | Active (2.7.x) | S (as a gate) |
| **Aider repo-map / RepoMapper / code-graph MCP** | **tree-sitter** def/ref tags → NetworkX graph → **PageRank**-ranked symbol map | The map is regenerated per call; tags cached in SQLite (mtime invalidation) | Per-repo; you concatenate | Aider active; several MIT MCP re-implementations (RepoMapper, code-graph-mcp, CodeGraph) shipping in 2026 | **S–M** |
| **SCIP + scip-python** | Compiler-precise **`index.scip`** Protobuf (defs, refs, implementations) built on Pyright; **cross-repo symbol resolution with package+version metadata** | **Yes** — standalone `index.scip` file; consumable **without a Sourcegraph server** via the open-source `scip` CLI (`scip print`, `snapshot`, `stats`, `lint`, and experimental `scip expt-convert` to SQLite) or SCIP protobuf bindings | **Best-in-class**: designed for cross-repo nav via version-aware symbol IDs | scip-python is **low-activity / maintenance mode**: v0.6.0 (~2022–23), then a burst of v0.6.1→v0.6.6 in late-2025/Q1-2026, nothing since. Sourcegraph spun out its AI agent (Amp) into a separate company **Dec 2, 2025** and refocused on code search/understanding; Cody Free/Pro discontinued **July 23, 2025**; Sourcegraph source went private **Aug 2024**, now enterprise-only | **M–L** (Node/npm toolchain, Pyright env setup) |
| **stack-graphs** (github) | Incremental, file-local name-resolution graph; language-agnostic; SQLite-backed via CLI | Yes (SQLite db) | Designed for GitHub-scale cross-file, but Python cross-module resolution has **known open bugs** (issue #430); Python bindings are an unaffiliated WIP fork | Rust core maintained by GitHub; Python ruleset less mature | **L** (Rust toolchain) |
| **Joern (code property graph)** | Full CPG (AST+CFG+PDG), Scala/Gremlin query DSL; MCP servers exist (codebadger) | In-memory/custom DB; exportable | Per-codebase; security-oriented | Active, daily releases | **L** (JVM/Scala; heavy — conflicts with "no heavy frameworks") |
| **ast / symtable (stdlib)** | Whatever you extract | Yes | You build resolution | stdlib — **library-first ideal** | M (you hand-roll resolution → measured-divergence justification needed) |

**Recommendation for the fleet:** Your durable, committable, library-first backbone is **grimp** (module-level import edges, already the engine behind your import-linter usage). Add **tree-sitter symbol-level def/ref** only if agents need function-granular "who calls this" — and get it from an existing MIT repo-map/MCP rather than hand-rolling. Reserve **SCIP/scip-python** for the specific need of *precise cross-repo same-symbol resolution*, weighing its maintenance-mode status and Node toolchain against library-first. **Avoid Joern and stack-graphs** as primary tools for this fleet (heavy toolchains; stack-graphs' Python module resolution is still buggy). Cross-repo joins in practice: either (a) SCIP's version-aware symbol IDs, or (b) the cheap fleet-appropriate approach — normalize module/file paths to `repo::module` keys and join on declared package boundaries from your parity/carrier manifests.

### 2. Doc-side and traceability graph
- **sphinx-needs** is the de-facto docs-as-code requirements/traceability tool (typed need objects `req`/`spec`/`test`, typed links, needflow diagrams, MIT license, active — 8.3.x, useblocks commercial backing). **But it is Sphinx-bound and RST-first.** Adopting it wholesale means adopting Sphinx — a heavy framework you've said you don't want. Its data model (typed nodes + typed links + stable IDs) is nonetheless the right conceptual template to copy.
- **Doorstop** stores each requirement as a YAML file with markdown body under version control, review-as-code via `git diff`; intentionally minimal, no web UI. **StrictDoc** (successor lineage, own SDoc DSL + **experimental markdown support**, exports HTML/RST/ReqIF/JSON/Excel, has a web UI) is the most modern text-first option. Both collocate requirements with code in git — a good fit — but both impose their own file format/DSL rather than reading your existing frontmatter.
- **ADR tooling:** `adr-tools` (bash CLI, `adr new`/`adr link`/`adr supersede`) and **log4brains** (docs-as-code ADRs in markdown, static-site generation, models supersedes/relates edges, guesses metadata from git). log4brains is Node/JS. The ADR "supersedes/superseded-by/relates" status edges are exactly a decision↔decision edge type you want.
- **Obsidian-style wikilinks / MkDocs plugins / frontmatter link registries**: lightweight, markdown-native, but non-typed and easy to rot without validation.

**The realistic path for a plain-markdown + YAML-frontmatter fleet that won't adopt Sphinx:** *Do not adopt a requirements tool as your store.* Instead, **treat your existing frontmatter as the node/edge source** and copy sphinx-needs' *schema* (every artifact gets a stable typed id; links are typed keys in frontmatter). You already do this: `reconciled_with: <spec>@<version>` is a typed doc→spec edge with a validator and a registry. Generalize that pattern to a small fixed vocabulary of frontmatter edge keys (`reconciled_with`, `supersedes`, `governs`, `refs`, `implements`) and write one parser that reads all frontmatter into edges. This is a **mechanism** (a checker/emitter), stays library-first (PyYAML + stdlib), and needs no framework.

### 3. Joining the two sides (doc↔code, decision↔code, task↔file)
Working patterns, ranked by how derivable (mechanism) vs. hand-authored (curation) they are:
- **Derived / mechanism (prefer these):**
  - **Git-trailer linking** (`Closes:`, `Refs:`, `Reconciles:`): Git has native `git interpret-trailers` support; GitLab parses trailers from `git log`/`git show` to generate changelogs at scale. Parse the history once → commit↔task, commit↔file (from the diff), thus **task↔file derived from history** even without the `footprint` field. Caveat: trailers "are a bit of a pain to parse reliably" — use `git interpret-trailers`/the git CLI, not a regex.
  - **Import graph** (grimp) → code↔code, and file↔file.
  - **Test-to-code mapping**: `pytest-cov`/coverage.py gives line-level coverage (which tests execute which files); `pytest-testmon`-style tools track the test↔code dependency directly. This is a **derived** test↔code edge.
  - **doc-claims validator** (yours): number-in-doc ↔ computed-value — already a mechanism; emit it as a doc↔code edge.
- **Curated / manual (minimize, then gate):**
  - **Annotation comments in code referencing an ADR/requirement id** (e.g. `# ADR-101`, `# implements REQ-x`): cheap to author, greppable (the CodeAnchor argument), but must be validated so ids resolve.
  - **Manifest mapping ids → file globs** (CODEOWNERS-style): your parity manifest and carrier manifests are exactly this — declared, not derived.
  - **Backlog `footprint:` field** (task→files): the one edge that "barely exists" (5 of 169 rows).

**Anti-rot / orphan detection (the crucial mechanism):** every hand-authored link must have a CI/hook check that fails on: (a) dangling ids (link target doesn't exist), (b) orphan nodes (a rule with no enforcing check; a doc referencing a dead symbol; a task with no files), (c) stale `reconciled_with` versions. The literature is unambiguous that **un-gated manual links decay ("traceability decay") and become actively misleading** — so the mechanism is not optional. Your `validate_reconciliation` script is the template; replicate it per edge type.

**Which links are worth maintaining by hand?** Only the ones that encode *intent a machine cannot infer*: decision↔code ("this file exists because of ADR-N"), requirement↔code, and serialize-group membership. Everything structural (imports, calls, test coverage, commit-touched files) should be **derived**, never typed by hand.

### 4. Storage and query layer
For ~6 repos and tens of thousands of nodes, ranked for your constraints:

| Store | Embeddable / no server | Python-native | Query ergonomics (reachability/impact) | Regenerable in seconds | Maintenance / risk | Verdict |
|---|---|---|---|---|---|---|
| **DuckDB + recursive CTEs** (optionally **DuckPGQ** extension) | Yes (in-process file or `:memory:`) | First-class (`pip install duckdb`) | Recursive CTEs handle reachability; **DuckPGQ** adds SQL/PGQ `MATCH ... ANY SHORTEST` graph syntax | Yes | DuckDB very healthy (CWI/DuckDB Labs). **DuckPGQ, per DuckDB's official guide, "is a community extension and is still under active development. It is not available in the latest DuckDB release (1.5.x)… make sure to use DuckDB v1.4.4"** — treat PGQ as optional sugar, core CTEs as stable | **Primary recommendation** |
| **SQLite + recursive CTEs** | Yes (stdlib `sqlite3`) | stdlib — **library-first ideal** | Recursive CTEs; no native graph syntax | Yes | Rock-solid, zero-dependency | **Strong fallback / the library-first purist choice** |
| **NetworkX from committed JSONL/JSON** | Yes (in-memory) | Pure Python | Excellent algorithm library (ancestors/descendants, cycles, PageRank) but in-memory only | Yes (load JSONL) | Healthy; `node_link_data` for JSON round-trip | **Use as the in-memory analysis layer over the committed edge log** |
| **Kùzu** (embedded Cypher) | Yes | Yes | Excellent (Cypher, fast path queries) | Yes | **⚠ ARCHIVED Oct 10, 2025 after Apple acquired Kùzu Inc. (Waterloo spinoff, ~10 people, founded 2023); upstream read-only. Community forks (LadybugDB, Vela) exist but are unproven.** | **Avoid for a durable fleet asset** — the ownership change is a real risk |
| **rdflib / Oxigraph (SPARQL)** | rdflib pure-Python (in-memory/persistent); Oxigraph via pyoxigraph (RocksDB-backed, embedded) | Yes | SPARQL is powerful for typed/ontology edges | Yes | rdflib maintained (7.1.x, Jan 2025); pyoxigraph active (0.5.x) but "not stable yet, storage format may change" | **Only if you genuinely want RDF/ontology semantics** — heavier conceptual load, less agent-friendly |
| **Neo4j Community** | **No — requires a running server (JVM)** | Driver | Best-in-class Cypher | No | Healthy | **Rejected** — violates no-server constraint |

**Recommendation:** Commit the graph as **JSONL edge/node files**; load into **DuckDB** for queries (recursive CTEs for reachability today, DuckPGQ later if you want Cypher-like ergonomics — but pin the DuckDB version); use **NetworkX** in-process for algorithmic analyses (cycles, PageRank, ancestors/descendants). The purest library-first variant swaps DuckDB for stdlib **SQLite + recursive CTEs**. All three (JSONL, SQLite, NetworkX) are regenerable from source in seconds and need no server or SaaS.

### 5. Regenerate-vs-store and freshness
**Recommendation: commit a regenerated artifact (hybrid), not a purely ephemeral index.** Rationale tuned to your fleet:
- A **committed** graph (JSONL + a built DuckDB/SQLite file, or just the JSONL with the DB gitignored and rebuilt) is diff-reviewable, available offline to agents instantly, and provable-fresh via a gate. This matches your existing carrier/checksum discipline.
- **Freshness mechanism:** regenerate on **pre-commit** for cheap per-file edges (frontmatter, footprint, annotations) and on **pre-push / CI** for the whole-fleet graph (import graph, cross-repo joins). Key the incremental rebuild on changed files (mtime/content-hash, as tree-sitter repo-maps and Codebase-Memory do). **Detect staleness the way you already detect doc-claims drift:** a gate recomputes the graph and fails if the committed artifact differs from the freshly derived one (a checksum/`--check` mode). This is "instructions are requests, mechanisms are guarantees" applied to the graph itself.
- **Failure modes to design against:**
  - *Committed graph:* merge conflicts and size bloat. Mitigate by (a) storing **JSONL sorted by stable id** so diffs/merges are line-oriented and conflicts are rare; (b) gitignoring the binary DB and committing only the text edge log; (c) splitting per-repo edge files so satellites don't conflict on the hub file.
  - *Ephemeral index:* slow cold-start and **unavailability to agents** mid-task if the build breaks; non-determinism. Mitigate by making the build fast (grimp cache) and deterministic.

### 6. Agent-facing query surface
Four consumption patterns, compared:
- **Generated markdown "codemap"/index file the agent reads** (Aider repo-map style): zero infrastructure, always-available, but **costs context tokens every call** and is a static snapshot. Best for small always-relevant summaries. Repomix-style whole-repo packing is the extreme version (context-window-first).
- **CLI the agent calls** (e.g. `graph query --impact X`): library-first, deterministic, no server, trivially testable, cheap tokens (agent pulls only what it asks). **This is the best fit for your doctrine** — it's just another checker/tool the agent invokes, and Claude Code/Codex both shell out comfortably.
- **MCP server exposing graph queries** (stdio, local): the 2026 idiom — `code-graph-mcp`, `codebase-memory-mcp` (single static binary, 158 languages, sub-1ms queries, ~120× fewer tokens claimed), RepoMapper's MCP mode, Joern-backed codebadger. Stdio MCP is **local, no network server** — it does not violate "no SaaS." Reliability is good and token cost low because the agent gets structured results, not file dumps. Slightly more moving parts than a CLI.
- **Repo-native tooling / in-band anchors** (CodeAnchor): put the edge facts in comments the existing grep loop already finds; lowest friction, complementary to a graph.

**Recommendation:** Ship a **single Python CLI** (`graph …`) as the primary surface — it is the most library-first, testable, and doctrine-compliant — and wrap the *same* query functions in a **local stdio MCP server** as a thin optional adapter for agents that prefer tool-calling. Both read the committed graph. Avoid any hosted/remote MCP. Evidence that this measurably helps: the ablation and Codebase-Memory results above (token and tool-call reductions, multi-file localization gains) — with the honest caveat that for pure keyword/semantic lookup, grep/BM25 remains competitive.

### 7. Impact analysis and the payoff
Questions that become answerable once the union graph exists, with a note on which are genuinely used vs. theoretical:
- **Blast radius / impact analysis** ("what breaks if I change file/function/spec X"): forward-dependents traversal (BFS along reverse import/call edges, depth 3–5 is the practical range). **Genuinely the killer app** — every 2026 commercial entrant (Augment, Recursive, Pharaoh, LOOM, SixDegree) and the academic ablations center on this; industry anecdote of "changed one field, 417 files depended on it." Directly serves your operator's question.
- **Orphan detection**: rules with no enforcing check, docs referencing dead code, **tasks with no files** (your 164/169 gap), specs with no dependents. **Genuinely used** and cheap once edges exist; this is your existing validator philosophy generalized.
- **"Which decisions govern this file"**: decision↔code traversal. High-value for agents executing frozen contracts; used where ADR links are maintained.
- **Cycle detection**: import cycles (grimp/pydeps already do this) and doc/spec reference cycles. Used, cheap.
- **Test-to-code mapping** ("which tests exercise this file"): from coverage/testmon. Used for change-scoped test selection.
- **Reachability from spec → all dependents** (your `reconciled_with` registry inverted): used for "if this spec bumps a version, which docs/organs must update."

Evidence base: the change-impact-analysis value is well-attested in both the commercial tooling wave and the controlled agent studies; the requirements-traceability maintenance literature (Mäder & Egyed's 24%-faster/50%-more-correct experiment; a separate TraceLink industrial study reporting ~86% task accuracy with links vs. without) supports the maintenance-task value **conditional on links being fresh**.

### 8. Minimal starter path
See numbered plan and edge-type table below. **The single step that delivers the most answerable questions per unit of effort is Stage 3 (closing task↔file)** — see rationale there.

---

## Recommendations (staged, with thresholds)

**Stage 0 — Define the schema (S, mechanism).** Fix a small node/edge vocabulary and a single committed format: `nodes.jsonl` + `edges.jsonl`, each row `{id, type, ...}` / `{src, dst, edge_type, source_producer, derived|curated}`, sorted by id. Node types: repo, file, module, symbol, doc, adr/decision, spec, task, rule, check, test. This is the ontology. *Threshold to proceed:* schema covers all eight existing fragment types.

**Stage 1 — Emit edges from what's already free (S, mechanism).** Write one emitter per existing mechanism: grimp→code↔code; frontmatter parser→`reconciled_with`/`supersedes`/`governs`; parity manifest→repo↔file "must-carry"; carrier manifest→hub↔satellite "ships"; ADR-101 filename tokens→artifact↔class; doc-claims validator→doc↔computed; serialize-groups→task↔task mutual-exclusion. **Retires nothing; subsumes the scattered outputs into one file.** *Threshold:* `edges.jsonl` regenerates deterministically and a `--check` gate passes.

**Stage 2 — Stand up the query layer (S).** Load `edges.jsonl` into SQLite (stdlib) or DuckDB; ship `graph query` CLI with `impact <id>`, `orphans`, `cycles`, `governs <file>`. *Threshold:* answers "network of dependencies for X" in one command.

**Stage 3 — Close the task↔file gap (M, mostly curation + a mechanism).** This is **the single highest-value step per unit effort.** Two-pronged: (a) **derive** task↔file from git trailers (`Closes:`/`Refs:` parsed via `git interpret-trailers`) and the diffs of commits that reference a task id — free, retroactive; (b) backfill the `footprint:` field for open rows and add a **commit-msg/pre-push hook** that requires `footprint` (or a linking trailer) on task-touching commits, so the edge stops rotting. *Threshold:* >90% of open backlog rows have a task↔file edge (derived or declared). This step delivers the most newly-answerable questions (impact from a task, orphan tasks, test scoping) because it connects the human-work layer to the file layer — the one join that is currently missing.

**Stage 4 — Add symbol-level + test edges if needed (M).** If agents need function-granularity, add tree-sitter def/ref via an existing MIT repo-map/MCP (don't hand-roll — library-first). Add test↔code from coverage.py/testmon. *Threshold:* agents ask "who calls this function across repos" and get answers.

**Stage 5 — Agent surface + telemetry (M).** Wrap the query functions in a local stdio MCP; begin emitting the future telemetry (rows closed/day, test runs, arc durations, model/effort/tokens) as **timestamped node/edge attributes** into the same log, so dashboards are later just queries over the graph. *Threshold:* an agent completes a change using graph queries with fewer exploration tool-calls than grep-only (measure it, per the ablation methodology).

**Escalation triggers (what would change the plan):**
- If cross-repo *same-symbol* precision becomes essential (not just imports) → adopt **SCIP/scip-python**, accepting its maintenance-mode status and Node toolchain, and consume the `index.scip` offline via the `scip` CLI (no Sourcegraph server).
- If recursive-CTE query ergonomics become painful at scale → add **DuckPGQ** (pin DuckDB to v1.4.4) rather than moving to a server DB.
- Do **not** adopt Kùzu or Neo4j unless the no-server/maintenance constraints are explicitly lifted.

---

## Edge types → producer → mechanism/curation → cost

| Edge type | Producer | Mechanism or Curation | Folds in existing fragment | Cost |
|---|---|---|---|---|
| code↔code (import) | grimp | Mechanism | import graph / import-linter | S |
| code↔code (call/def-ref, symbol) | tree-sitter repo-map or SCIP | Mechanism | (new, optional) | M |
| doc↔spec (`reconciled_with@version`) | frontmatter parser | Mechanism | validate_reconciliation + registry | S |
| decision↔decision (supersedes/relates) | ADR frontmatter/status | Mechanism (parse) | ADRs | S |
| artifact↔ADR-class | filename ADR-101 token | Mechanism | ADR-101 tokens | S |
| repo↔file (must-carry) | parity manifest | Mechanism | parity manifest | S |
| hub↔satellite (ships/checksum) | carrier manifest | Mechanism | carrier manifests | S |
| doc↔computed-value | doc-claims validator | Mechanism | doc-claims validator | S |
| task↔task (mutual-exclusion) | serialize-groups | Mechanism | backlog serialize-groups | S |
| task↔file | git trailers (derived) **+** `footprint:` (curated) | Both | backlog footprint field | **M** |
| decision↔code | annotation comments / manifest | Curation (gated) | (new) | M |
| requirement↔code | annotation comments / manifest | Curation (gated) | (new) | M |
| test↔code | coverage.py / testmon | Mechanism | (new) | M |
| commit↔task, commit↔file | git history / `git interpret-trailers` | Mechanism | (new) | S |

**Legend:** Mechanism = a hook/gate/CI can produce or verify it. Curation = a human/agent must author and maintain it (and therefore must be guarded by an orphan/dangling-link check to prevent traceability decay).

## Caveats
- **Kùzu's ownership change is the single biggest tooling risk** in this space: archived Oct 10, 2025 after Apple's acquisition of Kùzu Inc. (per the EU DMA filing and Waterloo/BetaKit reporting), upstream read-only, forks unproven. Anything you read from mid-2025 recommending Kùzu as *the* embedded graph DB predates this.
- **scip-python is in maintenance mode**, not dead: a ~2-year gap then v0.6.1–0.6.6 in late-2025/Q1-2026, and Sourcegraph's Dec-2, 2025 corporate split (Amp spun out) refocused the company on code search/understanding. The `index.scip` artifact and open-source `scip` CLI remain usable offline, but exact release dates are approximate (npm vs Docker snapshots disagree) and third-party forks (@dev8/scip-python 0.7.0) are moving faster than the official package.
- **DuckPGQ is a community extension pinned to specific DuckDB versions** (needs v1.4.4, absent from the 1.5.x line at time of writing) and "still under active development" — do not build a hard dependency on it; recursive CTEs are the stable path.
- **The "graph beats grep for agents" claim is contested and workload-dependent.** Graphs win for multi-hop/structural/cross-file questions; BM25/grep ties or wins for semantic lookup; some researchers argue in-band comment anchors are competitive at current model strength. The token-reduction figures (10×, ~120×) come from vendor/preprint benchmarks on their own tools — directionally consistent across independent sources but not audited.
- **Traceability decay is a documented failure mode:** hand-authored links become misleading if not gated (ReqToCode: stale links are "actively harmful when they mislead"). Every curated edge needs a CI orphan/dangling check; otherwise the graph erodes trust — and the payoff figures (24% faster / 50% more correct, Mäder & Egyed) are explicitly *conditional* on links being current.
- **Windows + WSL/git-bash portability:** prefer pure-Python/stdlib producers (grimp, PyYAML, sqlite3, coverage.py) over toolchains needing Rust (stack-graphs), JVM/Scala (Joern), or heavy Node setups; the CLI/MCP should run under both WSL and native Windows Python.
- Some cited sources are engineering blogs and preprints (2026-dated arXiv IDs), not peer-reviewed; commercial blast-radius vendors have an incentive to overstate value. Treat quantified ROI claims (e.g. "$1.6M/yr prevented") as vendor marketing, not established fact.