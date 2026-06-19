# Research Report

**Query:** ## Question: How do coding agents and code-assistant systems obtain reliable cross-file dependency information in large codebases, and how well does each approach work? (survey of practice and evidence, 2023-2026)

### Background

A decision is pending on how an autonomous Python code-editing agent should obtain cross-file dependency facts before editing or deleting code. The mechanisms under consideration include static call-graph indexes, language-server queries, retrieval over code, and relying on the test suite. This survey informs which approaches are real, mature, and measured before that decision is taken.

### What to find out

1. What concrete mechanisms and tools are used to give code agents structural dependency context — language-server-as-tool, static analysis / call graphs, AST tooling, code-graph retrieval — and their maturity for Python and for headless (non-IDE) use.
2. What measured evidence exists on each approach's effect on agent task accuracy and on latency and cost inside the agent loop — cross-file completion benchmarks, ablations comparing static-analysis context against plain retrieval.
3. The reported failure modes and blind spots of each approach — dynamic dispatch, config-driven wiring, intra-file context, index staleness within a session.

### Source rules

- Recency: last 3 years (2023-2026); foundational static-analysis and program-slicing references allowed as grounding.
- Source types: peer-reviewed papers, arXiv, and practitioner engineering reports; exclude vendor marketing.
- Real systems to check: CrossCodeEval, RepoGraph, LspRAG, SWE-agent, tree-sitter, Pyright / python-lsp-server, ast-grep, pydeps / import-linter, Tach.

### Output wanted

A comparison map of mechanisms against maturity (Python/headless), measured accuracy effect, latency/cost in the agent loop, and failure modes. Surface unresolved questions and disconfirming evidence explicitly — including cases where structural dependency context did not help, or where a simpler approach matched it.

**Generated:** 2026-06-19 23:06:28
**Total cost:** $0.4602
**Duration:** 1m 11s
**Sources found:** 38

## Provider Summary

| Provider | Status | Duration | Cost | Sources |
|----------|--------|----------|------|---------|
| perplexity | ok | 14s | $0.0247 | 9 |
| grok | ok | 1m 11s | $0.3923 | 21 |
| openai_mini | ok | 42s | $0.0432 | 9 |
| gemini | error | — | — | 0 |

## Summary

## Report from PERPLEXITY (perplexity) The strongest evidence since 2023 suggests that **explicit structural context**—symbol/dependency graphs, language-server queries, and scoped cross-file retrieval—can help coding agents more than plain file search alone, but the gains are inconsistent and often task-dependent. The most mature headless options for Python are **AST/tree-sitter-based indexing** and **Python language-server/Pyright-style symbol analysis**, while the best measured gains on agent tasks come from systems that combine retrieval with structure rather than relying on tests or raw search alone.[5][8] ## What mechanisms are actually used - **Language-server-as-tool**: agents query symbols, definitions, references, diagnostics, and document outlines through LSP-style APIs; this is the closest headless analogue to IDE intelligence and is practical for Python when paired with pyright/python-lsp-server or a language-server-compatible wrapper. The core advantage is that it can answer “what depends on this symbol?” without reading the whole repo, but only for statically resolvable relationships.[5] - **Static dependency graphs / call graphs**: tools such as pydeps, import-linter, and graph-oriented repo tools precompute import edges or broader symbol graphs, which is mature for Python imports and module boundaries, but weaker for call chains that depend on dynamic dispatch, monkeypatching, dependency injection, or string-based wiring.[2][5][8] - **AST / tree-sitter tooling**: tree-sitter gives syntax-accurate parsing across many languages and is now a common substrate for repo indexing and structural retrieval; it is mature and headless, but it is syntax-based rather than semantic, so it captures “where is a function/class defined?” better than “what actually runs?”[2] - **Code-graph retrieval / repo graph stores**: systems like RepoGraph-style approaches and newer MCP-backed code intelligence tools build a graph of files, symbols, imports, and references, then retrieve a subgraph around the edit target. These are the most directly aligned with your use case because they aim to surface cross-file dependency chains before edits, but their accuracy still depends on index freshness and graph completeness.[2][5] - **Plain retrieval over code**: semantic search and chunk retrieval can find relevant files quickly, but they do not reliably preserve dependency structure. Practitioner comparisons increasingly frame retrieval-only as the “middle path” for finding code, not for proving safe transitive dependencies.[2] - **Relying on the test suite**: tests are essential for validation, but they are not a dependency oracle. They can reveal breakage after the fact, but they do not systematically enumerate cross-file dependencies before an edit, and they miss untested paths and config-driven wiring.[1][4] ## Maturity for Python and headless use | Mechanism | Python maturity | Headless maturity | Practical status | |---|---:|---:|---| | Language server queries | High | High | Ready for agent tools if symbol-only limitations are acceptable | | AST / tree-sitter indexing | High | High | Mature building block for repo-wide structural indexing | | Static import graphs / module deps | High | High | Useful and lightweight, but limited to static imports | | Call graphs / full dependency graphs | Medium | High | Useful, but often incomplete for Python semantics | | Code-graph retrieval systems | Medium to high | High | Promising for agent loops; quality varies by index design | | Plain semantic retrieval | High | High | Mature, but weaker on dependency correctness | | Test-suite-driven discovery | High | High | Mature validation, not dependency inference | ## What the evidence says about effectiveness - The clearest recent evidence favors **scoped structural retrieval** over naive context packing for agentic code tasks. The CrossCodeEval line of work was specifically designed around cross-file completion and dependency-sensitive retrieval, reflecting the view that agents need dependency chains, not just nearby text.[5][8] - Practitioner measurements from 2026 code-intelligence tooling reports claim large reductions in tool calls and token use when indexed structural retrieval is available, but these are mostly vendor or practitioner reports rather than independent peer-reviewed benchmark papers, so they should be treated as suggestive rather than definitive.[2] - The strongest disconfirming pattern is that **retrieval helps most when the dependency question is explicit**. For tasks dominated by local edits, simple file context or direct search can match more elaborate structural systems, while the extra graph work adds latency without proportional accuracy gains.[2][5] - Tests improve end-to-end safety, but the evidence base does not support using them as a substitute for pre-edit dependency discovery. They are better viewed as a downstream check than as a source of structural facts.[1][4] ## Typical failure modes and blind spots - **Dynamic dispatch and monkeypatching**: static graphs and language servers miss runtime-selected implementations, Python’s dynamic imports, and framework callbacks.[5][8] - **Config-driven wiring**: dependency injection, YAML/JSON configuration, plugin registries, and reflection break static call-chain assumptions.[1][5] - **Index staleness**: repo graphs and cached symbol indexes can lag behind the working tree during an agent session, especially if the agent edits files before refreshing the graph.[2][5] - **Overfitting to import structure**: import graphs are good at module boundaries but often miss actual call paths, side effects, or dataflow that matters for safe deletion.[5][8] - **Intra-file blindness of coarse retrieval**: chunk-level semantic search can retrieve the right file but miss the exact function or dependency edge needed to judge edit impact.[2][5] - **False confidence from tests**: a passing test suite can hide untested dependency paths, so “tests passed” does not mean “dependencies understood.”[1][4] ## Best-supported design choice for an autonomous Python editing agent For your decision, the most evidence-backed pattern is a **hybrid**: - Use **AST/tree-sitter or language-server indexing** to build a fast, local structural map of symbols, imports, and references.[2][5] - Use **scoped graph retrieval** to expand from the edited symbol into upstream/downstream dependency chains before changing code.[5][8] - Use **semantic retrieval** only as a fallback for “find the relevant area” questions, not as the main dependency oracle.[2] - Use the **test suite** after edits to validate behavior, not to infer the dependency set beforehand.[1][4] ## Unresolved questions - Whether a **static dependency graph plus LSP** is enough for Python-heavy repositories, or whether a richer repo graph materially improves safety on real-world edit/delete tasks, remains underdetermined by public benchmarks.[5][8] - There is still limited independent evidence comparing **graph-first retrieval** against **plain retrieval plus tests** on the same agent loop with equal latency budgets.[2][5] - The biggest open gap is measuring how much structure is enough: in many repos, the incremental gain from deeper graphs may be small relative to engineering cost unless the codebase has heavy dynamic wiring or large blast radius risk.[2][5] ## Sources - CrossCodeEval / repo-level cross-file dependency evaluation and related arXiv work on surfacing cross-file dependency chains.[5][8] - Practitioner comparison of code-intelligence tools and agent-facing structural retrieval systems, including graph/index approaches and reported tool-call/token reductions.[2] - Stack Overflow guidance on agentic coding guidelines, emphasizing explicit conventions, tests, and codebase-specific rules for AI agents.[1] - Theia/EclipseSource practitioner guidance on project-specific info files for AI coding agents.[3] ### Sources from this provider - [Source 1](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/) - [Source 2](https://rywalker.com/research/code-intelligence-tools) - [Source 3](https://eclipsesource.com/blogs/2025/05/06/enhancing-ai-coding-with-project-info/) - [Source 4](https://www.youtube.com/watch?v=LWhayk_7Ks0) - [Source 5](https://arxiv.org/html/2606.04397v1) - [Source 6](https://dev.to/sonotommy/8-ai-coding-agents-that-actually-ship-production-code-in-2026-18ch) - [Source 7](https://blog.stackademic.com/5-ai-coding-agents-that-actually-ship-production-code-in-2026-f4954e98bc05) - [Source 8](https://github.com/YerbaPage/Awesome-Repo-Level-Code-Generation/blob/main/README.md) - [Source 9](https://www.sonatype.com/blog/when-ai-writes-code-who-governs-the-dependencies) --- ## Report from GROK (grok) **Coding agents and code assistants obtain cross-file (or repository-level) dependency information primarily through a mix of static structural tools, retrieval-augmented generation (RAG) over parsed code, language server queries, and test-based validation.** These approaches have matured significantly from 2023–2026, driven by benchmarks like CrossCodeEval and SWE-bench, agent frameworks like SWE-agent, and practitioner tools leveraging tree-sitter, LSP implementations (especially Pyright for Python), and emerging standards like the Model Context Protocol (MCP).[[1]](https://crosscodeeval.github.io/)[[2]](https://arxiv.org/abs/2310.11248)[[3]](https://arxiv.org/html/2410.14684v1)[[4]](https://arxiv.org/html/2510.22210v1) The surveyed mechanisms align with the query's options (static call-graph indexes, language-server queries, retrieval over code, test suite reliance) plus closely related AST/structural tooling and explicit code graphs. Pure LLM-based graph construction is generally disfavored. All are usable headless (non-IDE), with varying Python support. Evidence comes from arXiv papers, benchmarks, and practitioner reports (no vendor marketing). Foundational static analysis references ground limitations in dynamic languages like Python.[[5]](https://d-nb.info/1391221605/34) ### 1. Concrete Mechanisms and Tools, with Maturity for Python and Headless Use - **Language Server Queries (LSP-as-tool)**: Agents query mature LSP servers (e.g., Pyright/pyright-langserver or python-lsp-server for Python; gopls, etc. for others) for definitions (`textDocument/definition`), references (`textDocument/references`), symbols, hover/types, and diagnostics via JSON-RPC (stdio, HTTP, or wrappers). Tools: LSPRAG (LSP-Guided RAG), agent-lsp (MCP server bridging LSP to agents with 66+ tools and workflows), Lanser-CLI, and Claude Code LSP integration. Hybrid LSP + tree-sitter for semantic resolution beyond pure syntax.[[4]](https://arxiv.org/html/2510.22210v1)[[6]](https://medium.com/@vinodh.thiagarajan/lsp-the-protocol-your-ide-uses-every-day-and-now-your-ai-agent-does-too-19e74ca26ace)[[7]](https://github.com/blackwell-systems/agent-lsp)[[8]](https://huggingface.co/blog/yifAI/lanser-cli) **Maturity**: High for Python (Pyright is fast, accurate for types/refs/defs; Pylance-backed). Excellent headless support via CLI wrappers, MCP servers, or direct stdio. Real-time, language-agnostic with off-the-shelf servers; minimal per-language effort. Widely used in agents by 2025–2026.[[9]](https://thu-wingtecher.github.io/LSPRAG/) - **Static Analysis / Call Graphs / Dependency Graphs**: Build indexes or graphs using static tools for calls, imports, data/control dependencies. Tools: PyCG (strong Python call graphs), pydeps/import-linter, Tach (Rust-based enforcement of module boundaries, interfaces, no cycles, visualization), and custom analyzers. Often combined with AST parsing. LLMs are poorer at constructing these than dedicated tools.[[5]](https://d-nb.info/1391221605/34)[[10]](https://github.com/tach-org/tach) **Maturity**: Good-to-high for Python static cases (PyCG outperforms GPT-4o on benchmarks); limitations in fully dynamic code. Fully headless (CLI, libraries). Used for pre-indexing or enforcement (e.g., Tach in CI/modularization). Foundational program slicing/static analysis papers highlight Python challenges (dynamic dispatch, metaclasses, eval, dependency injection via config).[[5]](https://d-nb.info/1391221605/34) - **AST / Structural Tooling**: Parse code into trees for precise queries, chunking, or graph construction. Core tool: tree-sitter (with Python grammar; supports 60+ languages). Complementary: ast-grep (structural search/replace). Used to bootstrap graphs or improve RAG chunking (e.g., function/class-level hierarchy).[[11]](https://arxiv.org/abs/2603.27277)[[12]](https://medium.com/@shsax/how-i-built-coderag-with-dependency-graph-using-tree-sitter-0a71867059ae) **Maturity**: Very high. Deterministic, fast, headless-first. Extensively used in 2024–2026 agent stacks for indexing without LLM involvement. Persistent graphs via MCP (e.g., Codebase-Memory).[[13]](https://github.com/DeusData/codebase-memory-mcp) - **Code-Graph Retrieval / Indexes**: Build and query a repository-level graph (nodes: lines, functions, classes; edges: calls, imports, references, control flow, impact). Examples: RepoGraph (line-level ego-graphs via tree-sitter, filters non-project deps), Codebase-Memory / codebase-memory-mcp (tree-sitter + hybrid LSP into persistent SQLite/MCP graph; fast indexing, callers/callees/impact queries, auto-sync on edits), ARISE (program graph augmenting SWE-agent), graphify, and LlamaIndex CodeHierarchyNodeParser. Exposed via MCP for agents.[[3]](https://arxiv.org/html/2410.14684v1)[[14]](https://github.com/ozyyshr/RepoGraph)[[11]](https://arxiv.org/abs/2603.27277)[[15]](https://x.com/prsmdev/status/2066247685636583440) **Maturity**: Emerging-to-mature by 2026 (plug-in style for SWE-agent, Agentless, RAG pipelines). Strong Python support; extensible/multi-lang via tree-sitter. Headless-native; persistent and queryable in-session. Replaces repeated grep/read.[[16]](https://x.com/JeremyCMorgan/status/2067034582629728467) - **Plain Retrieval (RAG over Code)**: Embed files/chunks (often AST-guided for hierarchy/functions) and retrieve by similarity/keywords. Common baseline; improved by structural parsing but lacks explicit dependency edges.[[17]](https://x.com/jerryjliu0/status/1770163771740459182) **Maturity**: High, but noisier for precise deps. Headless via vector DBs. - **Relying on the Test Suite (and Dynamic Validation)**: Run tests, coverage analysis, or linters post-edit (or to guide retrieval). Core to SWE-agent (bash tools in sandbox for edit/search/test/lint; context managers for history). Implicitly surfaces breakage from cross-file changes.[[18]](https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade)[[19]](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf) **Maturity**: High and essential in real agents (SWE-bench workflows). Headless via sandbox. Dependent on test quality/coverage. Practitioner reports (X/engineering) emphasize deterministic tree-sitter/LSP graphs over LLM guesses for grounding agents, reducing tokens/greps, and enabling queries like "callers of X" or "impact of editing Y." MCP has standardized exposure of these to agents (Claude Code, Aider, etc.) by 2026.[[15]](https://x.com/prsmdev/status/2066247685636583440)[[20]](https://x.com/josevalim/status/2002312493713015160)[[13]](https://github.com/DeusData/codebase-memory-mcp) ### 2. Measured Evidence on Accuracy, Latency, and Cost **CrossCodeEval (2023, NeurIPS)**: Multilingual (incl. Python) benchmark on real repos. Constructed via static analysis (replace imports with empty classes; static analysis finds undefined names → cross-file fragments). Models perform poorly with only in-file context (CodeGen, SantaCoder, StarCoder, GPT-3.5); substantial gains with cross-file context or retrieval, but even top models/retrievers suboptimal on code-match (EM/ES) and identifier-match metrics. Also evaluates retrievers (e.g., embeddings <20 EM). Demonstrates necessity of cross-file structural understanding.[[1]](https://crosscodeeval.github.io/)[[2]](https://arxiv.org/abs/2310.11248)[[1]](https://crosscodeeval.github.io/)

*(truncated — summarizer unavailable)*

---

## Full Research Report

## Report from PERPLEXITY (perplexity)

The strongest evidence since 2023 suggests that **explicit structural context**—symbol/dependency graphs, language-server queries, and scoped cross-file retrieval—can help coding agents more than plain file search alone, but the gains are inconsistent and often task-dependent. The most mature headless options for Python are **AST/tree-sitter-based indexing** and **Python language-server/Pyright-style symbol analysis**, while the best measured gains on agent tasks come from systems that combine retrieval with structure rather than relying on tests or raw search alone.[5][8]

## What mechanisms are actually used

- **Language-server-as-tool**: agents query symbols, definitions, references, diagnostics, and document outlines through LSP-style APIs; this is the closest headless analogue to IDE intelligence and is practical for Python when paired with pyright/python-lsp-server or a language-server-compatible wrapper. The core advantage is that it can answer “what depends on this symbol?” without reading the whole repo, but only for statically resolvable relationships.[5]
- **Static dependency graphs / call graphs**: tools such as pydeps, import-linter, and graph-oriented repo tools precompute import edges or broader symbol graphs, which is mature for Python imports and module boundaries, but weaker for call chains that depend on dynamic dispatch, monkeypatching, dependency injection, or string-based wiring.[2][5][8]
- **AST / tree-sitter tooling**: tree-sitter gives syntax-accurate parsing across many languages and is now a common substrate for repo indexing and structural retrieval; it is mature and headless, but it is syntax-based rather than semantic, so it captures “where is a function/class defined?” better than “what actually runs?”[2]
- **Code-graph retrieval / repo graph stores**: systems like RepoGraph-style approaches and newer MCP-backed code intelligence tools build a graph of files, symbols, imports, and references, then retrieve a subgraph around the edit target. These are the most directly aligned with your use case because they aim to surface cross-file dependency chains before edits, but their accuracy still depends on index freshness and graph completeness.[2][5]
- **Plain retrieval over code**: semantic search and chunk retrieval can find relevant files quickly, but they do not reliably preserve dependency structure. Practitioner comparisons increasingly frame retrieval-only as the “middle path” for finding code, not for proving safe transitive dependencies.[2]
- **Relying on the test suite**: tests are essential for validation, but they are not a dependency oracle. They can reveal breakage after the fact, but they do not systematically enumerate cross-file dependencies before an edit, and they miss untested paths and config-driven wiring.[1][4]

## Maturity for Python and headless use

| Mechanism | Python maturity | Headless maturity | Practical status |
|---|---:|---:|---|
| Language server queries | High | High | Ready for agent tools if symbol-only limitations are acceptable |
| AST / tree-sitter indexing | High | High | Mature building block for repo-wide structural indexing |
| Static import graphs / module deps | High | High | Useful and lightweight, but limited to static imports |
| Call graphs / full dependency graphs | Medium | High | Useful, but often incomplete for Python semantics |
| Code-graph retrieval systems | Medium to high | High | Promising for agent loops; quality varies by index design |
| Plain semantic retrieval | High | High | Mature, but weaker on dependency correctness |
| Test-suite-driven discovery | High | High | Mature validation, not dependency inference |

## What the evidence says about effectiveness

- The clearest recent evidence favors **scoped structural retrieval** over naive context packing for agentic code tasks. The CrossCodeEval line of work was specifically designed around cross-file completion and dependency-sensitive retrieval, reflecting the view that agents need dependency chains, not just nearby text.[5][8]
- Practitioner measurements from 2026 code-intelligence tooling reports claim large reductions in tool calls and token use when indexed structural retrieval is available, but these are mostly vendor or practitioner reports rather than independent peer-reviewed benchmark papers, so they should be treated as suggestive rather than definitive.[2]
- The strongest disconfirming pattern is that **retrieval helps most when the dependency question is explicit**. For tasks dominated by local edits, simple file context or direct search can match more elaborate structural systems, while the extra graph work adds latency without proportional accuracy gains.[2][5]
- Tests improve end-to-end safety, but the evidence base does not support using them as a substitute for pre-edit dependency discovery. They are better viewed as a downstream check than as a source of structural facts.[1][4]

## Typical failure modes and blind spots

- **Dynamic dispatch and monkeypatching**: static graphs and language servers miss runtime-selected implementations, Python’s dynamic imports, and framework callbacks.[5][8]
- **Config-driven wiring**: dependency injection, YAML/JSON configuration, plugin registries, and reflection break static call-chain assumptions.[1][5]
- **Index staleness**: repo graphs and cached symbol indexes can lag behind the working tree during an agent session, especially if the agent edits files before refreshing the graph.[2][5]
- **Overfitting to import structure**: import graphs are good at module boundaries but often miss actual call paths, side effects, or dataflow that matters for safe deletion.[5][8]
- **Intra-file blindness of coarse retrieval**: chunk-level semantic search can retrieve the right file but miss the exact function or dependency edge needed to judge edit impact.[2][5]
- **False confidence from tests**: a passing test suite can hide untested dependency paths, so “tests passed” does not mean “dependencies understood.”[1][4]

## Best-supported design choice for an autonomous Python editing agent

For your decision, the most evidence-backed pattern is a **hybrid**:

- Use **AST/tree-sitter or language-server indexing** to build a fast, local structural map of symbols, imports, and references.[2][5]
- Use **scoped graph retrieval** to expand from the edited symbol into upstream/downstream dependency chains before changing code.[5][8]
- Use **semantic retrieval** only as a fallback for “find the relevant area” questions, not as the main dependency oracle.[2]
- Use the **test suite** after edits to validate behavior, not to infer the dependency set beforehand.[1][4]

## Unresolved questions

- Whether a **static dependency graph plus LSP** is enough for Python-heavy repositories, or whether a richer repo graph materially improves safety on real-world edit/delete tasks, remains underdetermined by public benchmarks.[5][8]
- There is still limited independent evidence comparing **graph-first retrieval** against **plain retrieval plus tests** on the same agent loop with equal latency budgets.[2][5]
- The biggest open gap is measuring how much structure is enough: in many repos, the incremental gain from deeper graphs may be small relative to engineering cost unless the codebase has heavy dynamic wiring or large blast radius risk.[2][5]

## Sources

- CrossCodeEval / repo-level cross-file dependency evaluation and related arXiv work on surfacing cross-file dependency chains.[5][8]
- Practitioner comparison of code-intelligence tools and agent-facing structural retrieval systems, including graph/index approaches and reported tool-call/token reductions.[2]
- Stack Overflow guidance on agentic coding guidelines, emphasizing explicit conventions, tests, and codebase-specific rules for AI agents.[1]
- Theia/EclipseSource practitioner guidance on project-specific info files for AI coding agents.[3]

### Sources from this provider
- [Source 1](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/)
- [Source 2](https://rywalker.com/research/code-intelligence-tools)
- [Source 3](https://eclipsesource.com/blogs/2025/05/06/enhancing-ai-coding-with-project-info/)
- [Source 4](https://www.youtube.com/watch?v=LWhayk_7Ks0)
- [Source 5](https://arxiv.org/html/2606.04397v1)
- [Source 6](https://dev.to/sonotommy/8-ai-coding-agents-that-actually-ship-production-code-in-2026-18ch)
- [Source 7](https://blog.stackademic.com/5-ai-coding-agents-that-actually-ship-production-code-in-2026-f4954e98bc05)
- [Source 8](https://github.com/YerbaPage/Awesome-Repo-Level-Code-Generation/blob/main/README.md)
- [Source 9](https://www.sonatype.com/blog/when-ai-writes-code-who-governs-the-dependencies)

---

## Report from GROK (grok)

**Coding agents and code assistants obtain cross-file (or repository-level) dependency information primarily through a mix of static structural tools, retrieval-augmented generation (RAG) over parsed code, language server queries, and test-based validation.** These approaches have matured significantly from 2023–2026, driven by benchmarks like CrossCodeEval and SWE-bench, agent frameworks like SWE-agent, and practitioner tools leveraging tree-sitter, LSP implementations (especially Pyright for Python), and emerging standards like the Model Context Protocol (MCP).[[1]](https://crosscodeeval.github.io/)[[2]](https://arxiv.org/abs/2310.11248)[[3]](https://arxiv.org/html/2410.14684v1)[[4]](https://arxiv.org/html/2510.22210v1)

The surveyed mechanisms align with the query's options (static call-graph indexes, language-server queries, retrieval over code, test suite reliance) plus closely related AST/structural tooling and explicit code graphs. Pure LLM-based graph construction is generally disfavored. All are usable headless (non-IDE), with varying Python support. Evidence comes from arXiv papers, benchmarks, and practitioner reports (no vendor marketing). Foundational static analysis references ground limitations in dynamic languages like Python.[[5]](https://d-nb.info/1391221605/34)

### 1. Concrete Mechanisms and Tools, with Maturity for Python and Headless Use

- **Language Server Queries (LSP-as-tool)**: Agents query mature LSP servers (e.g., Pyright/pyright-langserver or python-lsp-server for Python; gopls, etc. for others) for definitions (`textDocument/definition`), references (`textDocument/references`), symbols, hover/types, and diagnostics via JSON-RPC (stdio, HTTP, or wrappers). Tools: LSPRAG (LSP-Guided RAG), agent-lsp (MCP server bridging LSP to agents with 66+ tools and workflows), Lanser-CLI, and Claude Code LSP integration. Hybrid LSP + tree-sitter for semantic resolution beyond pure syntax.[[4]](https://arxiv.org/html/2510.22210v1)[[6]](https://medium.com/@vinodh.thiagarajan/lsp-the-protocol-your-ide-uses-every-day-and-now-your-ai-agent-does-too-19e74ca26ace)[[7]](https://github.com/blackwell-systems/agent-lsp)[[8]](https://huggingface.co/blog/yifAI/lanser-cli)

  **Maturity**: High for Python (Pyright is fast, accurate for types/refs/defs; Pylance-backed). Excellent headless support via CLI wrappers, MCP servers, or direct stdio. Real-time, language-agnostic with off-the-shelf servers; minimal per-language effort. Widely used in agents by 2025–2026.[[9]](https://thu-wingtecher.github.io/LSPRAG/)

- **Static Analysis / Call Graphs / Dependency Graphs**: Build indexes or graphs using static tools for calls, imports, data/control dependencies. Tools: PyCG (strong Python call graphs), pydeps/import-linter, Tach (Rust-based enforcement of module boundaries, interfaces, no cycles, visualization), and custom analyzers. Often combined with AST parsing. LLMs are poorer at constructing these than dedicated tools.[[5]](https://d-nb.info/1391221605/34)[[10]](https://github.com/tach-org/tach)

  **Maturity**: Good-to-high for Python static cases (PyCG outperforms GPT-4o on benchmarks); limitations in fully dynamic code. Fully headless (CLI, libraries). Used for pre-indexing or enforcement (e.g., Tach in CI/modularization). Foundational program slicing/static analysis papers highlight Python challenges (dynamic dispatch, metaclasses, eval, dependency injection via config).[[5]](https://d-nb.info/1391221605/34)

- **AST / Structural Tooling**: Parse code into trees for precise queries, chunking, or graph construction. Core tool: tree-sitter (with Python grammar; supports 60+ languages). Complementary: ast-grep (structural search/replace). Used to bootstrap graphs or improve RAG chunking (e.g., function/class-level hierarchy).[[11]](https://arxiv.org/abs/2603.27277)[[12]](https://medium.com/@shsax/how-i-built-coderag-with-dependency-graph-using-tree-sitter-0a71867059ae)

  **Maturity**: Very high. Deterministic, fast, headless-first. Extensively used in 2024–2026 agent stacks for indexing without LLM involvement. Persistent graphs via MCP (e.g., Codebase-Memory).[[13]](https://github.com/DeusData/codebase-memory-mcp)

- **Code-Graph Retrieval / Indexes**: Build and query a repository-level graph (nodes: lines, functions, classes; edges: calls, imports, references, control flow, impact). Examples: RepoGraph (line-level ego-graphs via tree-sitter, filters non-project deps), Codebase-Memory / codebase-memory-mcp (tree-sitter + hybrid LSP into persistent SQLite/MCP graph; fast indexing, callers/callees/impact queries, auto-sync on edits), ARISE (program graph augmenting SWE-agent), graphify, and LlamaIndex CodeHierarchyNodeParser. Exposed via MCP for agents.[[3]](https://arxiv.org/html/2410.14684v1)[[14]](https://github.com/ozyyshr/RepoGraph)[[11]](https://arxiv.org/abs/2603.27277)[[15]](https://x.com/prsmdev/status/2066247685636583440)

  **Maturity**: Emerging-to-mature by 2026 (plug-in style for SWE-agent, Agentless, RAG pipelines). Strong Python support; extensible/multi-lang via tree-sitter. Headless-native; persistent and queryable in-session. Replaces repeated grep/read.[[16]](https://x.com/JeremyCMorgan/status/2067034582629728467)

- **Plain Retrieval (RAG over Code)**: Embed files/chunks (often AST-guided for hierarchy/functions) and retrieve by similarity/keywords. Common baseline; improved by structural parsing but lacks explicit dependency edges.[[17]](https://x.com/jerryjliu0/status/1770163771740459182)

  **Maturity**: High, but noisier for precise deps. Headless via vector DBs.

- **Relying on the Test Suite (and Dynamic Validation)**: Run tests, coverage analysis, or linters post-edit (or to guide retrieval). Core to SWE-agent (bash tools in sandbox for edit/search/test/lint; context managers for history). Implicitly surfaces breakage from cross-file changes.[[18]](https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade)[[19]](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)

  **Maturity**: High and essential in real agents (SWE-bench workflows). Headless via sandbox. Dependent on test quality/coverage.

Practitioner reports (X/engineering) emphasize deterministic tree-sitter/LSP graphs over LLM guesses for grounding agents, reducing tokens/greps, and enabling queries like "callers of X" or "impact of editing Y." MCP has standardized exposure of these to agents (Claude Code, Aider, etc.) by 2026.[[15]](https://x.com/prsmdev/status/2066247685636583440)[[20]](https://x.com/josevalim/status/2002312493713015160)[[13]](https://github.com/DeusData/codebase-memory-mcp)

### 2. Measured Evidence on Accuracy, Latency, and Cost

**CrossCodeEval (2023, NeurIPS)**: Multilingual (incl. Python) benchmark on real repos. Constructed via static analysis (replace imports with empty classes; static analysis finds undefined names → cross-file fragments). Models perform poorly with only in-file context (CodeGen, SantaCoder, StarCoder, GPT-3.5); substantial gains with cross-file context or retrieval, but even top models/retrievers suboptimal on code-match (EM/ES) and identifier-match metrics. Also evaluates retrievers (e.g., embeddings <20 EM). Demonstrates necessity of cross-file structural understanding.[[1]](https://crosscodeeval.github.io/)[[2]](https://arxiv.org/abs/2310.11248)[[1]](https://crosscodeeval.github.io/)

**RepoGraph (2024)**: Line-level graph (tree-sitter parsed) provided as plug-in (ego-graph retrieval around keywords; integrated into SWE-agent, AutoCodeRover, RAG, Agentless). On SWE-bench-Lite: average ~32.8% relative resolve-rate boost across baselines (e.g., Agentless+RepoGraph 29.67% vs. 27.33%; new SOTA open-source in some settings); higher patch-apply rates. On CrossCodeEval: large F1 gains (e.g., GPT-4o code/identifier F1 28.7/36.0 vs. 10.5/16.8). Ablations: 2-hop ego-graphs + summarization best; flatten vs. summarize variants. Increases tokens/cost modestly but improves localization/editing accuracy.[[3]](https://arxiv.org/html/2410.14684v1)[[14]](https://github.com/ozyyshr/RepoGraph)

**LSPRAG / LSP-Guided RAG (2025/2026, ICSE)**: LSP queries (defs, refs, symbols, tokens, diagnostics) + hybrid lexical/AST-CFG key-token extraction for concise context in unit test generation. Language-agnostic (Python/Java/Go via off-the-shelf servers + tree-sitter). Large gains vs. plain RAG/CodeQA/DraCo/SymPrompt baselines: Python +16.87–31.57% line coverage, +20.16% valid rate; Java/Go even higher (up to 213% coverage, 250%+ valid). ~28s / ~4.5k tokens per focal method (real-time feasible). Handles cross-file via workspace-wide refs/defs; no compile needed. Superior due to precision vs. noisy retrieval.[[4]](https://arxiv.org/html/2510.22210v1)[[9]](https://thu-wingtecher.github.io/LSPRAG/)

**Call-graph benchmarks (e.g., SWARM-CG, 2024)**: Static tools (PyCG for Python) significantly outperform LLMs (PyCG ~83% completeness/85% soundness vs. GPT-4o ~61%/71%). LLMs struggle with Python dynamics; static tools preferred for reliability and efficiency. CoRe benchmark (2025) tests LLMs directly on dependency reasoning; they handle simple cases but falter on deep/multi-step or backward dependencies.[[21]](https://neurips.cc/virtual/2025/poster/121601)[[5]](https://d-nb.info/1391221605/34)

**SWE-agent / derivatives (2024+)**: ACI (Agent-Computer Interface) with bash tools emphasizes search/edit/test loops over upfront full graphs; context managers control history. Augmentations like ARISE (graph + tiered tools) or RepoGraph plugins improve resolve rates. Test running is critical for verification; pure retrieval baselines were ~2% on early SWE-bench.[[18]](https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade)[[19]](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)

**Practitioner / other**: Tree-sitter + graph approaches (Codebase-Memory, graphify) index large repos quickly (Linux kernel in minutes), answer structural queries in <1ms, and cut token usage by replacing grep/read cycles. MCP tools make LSP/graph queries native to agents. Latency trade-off: upfront indexing cheap; in-loop queries add tokens/prompt size but improve accuracy enough to offset via fewer turns.[[11]](https://arxiv.org/abs/2603.27277)[[15]](https://x.com/prsmdev/status/2066247685636583440)[[13]](https://github.com/DeusData/codebase-memory-mcp)

**Disconfirming / no-help cases**: Adding structural context sometimes yields only marginal gains if tests/linting catch issues (simple SWE-agent loops succeed without full graphs). Excessive context from broad refs in large projects increases noise/tokens without proportional accuracy. LLMs alone for graphs underperform static tools. Some retrieval ablations show hierarchical/AST chunking matches or exceeds naive graphs for certain tasks.[[5]](https://d-nb.info/1391221605/34)

### 3. Reported Failure Modes and Blind Spots

- **LSP Queries**: LSP server quality/variability; excess context in large repos; weaker on fully dynamic Python (runtime behaviors, monkey-patching); requires proper workspace setup. May not handle non-code wiring.[[4]](https://arxiv.org/html/2510.22210v1)

- **Static/Call Graphs / Tach**: Misses dynamic dispatch, config-driven DI, metaclasses, or framework plugins in Python; index staleness during multi-edit agent sessions (incremental updates hard); over- or under-approximation. Tach excels at boundaries but is enforcement-oriented.[[5]](https://d-nb.info/1391221605/34)

- **AST / Code-Graph Retrieval (RepoGraph, Codebase-Memory)**: Syntactic bias (misses semantic nuances); construction errors propagate; contextual misalignment, incorrect localization, regressive edits (most common failures in RepoGraph evals). Staleness if not auto-synced (some 2026 tools claim edit syncing). Query scope (k-hop) needs tuning.[[3]](https://arxiv.org/html/2410.14684v1)

- **Plain RAG**: Noisy/irrelevant results; misses non-textually-similar but dependent code; poor on implicit/cross-module deps.

- **Test Suite**: Dependent on test coverage/quality; misses untested paths or subtle cross-file breaks; high latency for full runs in inner loop. Does not provide *proactive* dependency facts before editing/deleting.

**Common**: Intra-file context often dominates, but cross-file is the gap; all struggle with config/framework wiring; session-long staleness in evolving codebases; token/cost blowup from over-inclusion. Dynamic Python remains a core blind spot for purely static approaches.[[1]](https://crosscodeeval.github.io/)

### Comparison Map (Textual)

**Maturity (Python/Headless)**: LSP (High/High), AST/tree-sitter (Very High/High), Code-Graphs (High/High by 2026 via MCP), Static Call Graphs (Good-High/High; Python dynamics limit), Plain RAG (High/High), Tests (High/High).

**Accuracy Effect**: Structured (LSP/graph/AST) consistently outperforms plain RAG (LSPRAG coverage/validity gains; RepoGraph SWE-bench/CrossCodeEval lifts; CrossCodeEval shows cross-file necessity). Graphs improve localization/editing; tests essential for verification. Static tools > LLMs for graph building.

**Latency/Cost in Agent Loop**: Upfront indexing cheap (tree-sitter/LSP fast); queries add tokens/prompt size and some latency (LSPRAG ~28s/method incl. gen; graphs reduce overall turns/greps). Tests add execution latency but are non-negotiable. Plain RAG can be cheapest but least precise.

**Failure Modes**: See section 3; dynamic Python, staleness, noise/excess context, syntactic limits prominent for structural approaches. Tests miss prevention.

### Unresolved Questions and Disconfirming Evidence

- **Unresolved**: Best incremental update mechanisms for graphs/indexes during long agent sessions with multiple edits/deletions. Optimal hybrid (e.g., LSP queries + selective graph retrieval + coverage-guided tests) vs. any single approach for Python editing safety. Quantified impact on *deletion* safety specifically. Mitigation for config-driven/dynamic wiring beyond "run more tests." How well MCP-standardized tools generalize beyond early adopters.[[13]](https://github.com/DeusData/codebase-memory-mcp)

- **Disconfirming**: Structural context does not always help proportionally (noise, token cost); simpler grep/search + test loops (core SWE-agent) can match or suffice for many real issues. LLMs are unreliable for building/maintaining graphs compared to static/AST tools—use tools, not prompting. In some cases, hierarchical RAG without explicit call graphs performs comparably. Pure static analysis has known blind spots in Python that tests partially address but do not eliminate.[[5]](https://d-nb.info/1391221605/34)

**Recommendation for Python autonomous code-editing agent**: Prioritize a hybrid of tree-sitter/AST-based persistent graphs (for structure/callers/callees) exposed via MCP or similar, augmented with on-demand LSP queries (Pyright) for precise, real-time defs/refs/diagnostics, and mandatory test/lint validation in the loop. This is mature, headless, measured to improve accuracy on relevant benchmarks, and reflects real 2025–2026 practitioner practice (e.g., agent-lsp, Codebase-Memory, graphify). Avoid sole reliance on plain RAG or LLM-built indexes; update the index on edits where possible. Static provides reliable grounding where it applies; tests catch the rest. This balances reliability, latency, and Python realities better than any singleton approach.[[15]](https://x.com/prsmdev/status/2066247685636583440)[[13]](https://github.com/DeusData/codebase-memory-mcp)

Further reading: CrossCodeEval paper/site, RepoGraph arXiv, LSPRAG arXiv, SWE-agent NeurIPS, Codebase-Memory repo, agent-lsp/tooling around MCP and Pyright.

### Sources from this provider
- [1](https://crosscodeeval.github.io/)
- [2](https://arxiv.org/abs/2310.11248)
- [3](https://arxiv.org/html/2410.14684v1)
- [4](https://arxiv.org/html/2510.22210v1)
- [5](https://d-nb.info/1391221605/34)
- [6](https://medium.com/@vinodh.thiagarajan/lsp-the-protocol-your-ide-uses-every-day-and-now-your-ai-agent-does-too-19e74ca26ace)
- [7](https://github.com/blackwell-systems/agent-lsp)
- [8](https://huggingface.co/blog/yifAI/lanser-cli)
- [9](https://thu-wingtecher.github.io/LSPRAG/)
- [10](https://github.com/tach-org/tach)
- [11](https://arxiv.org/abs/2603.27277)
- [12](https://medium.com/@shsax/how-i-built-coderag-with-dependency-graph-using-tree-sitter-0a71867059ae)
- [13](https://github.com/DeusData/codebase-memory-mcp)
- [14](https://github.com/ozyyshr/RepoGraph)
- [15](https://x.com/prsmdev/status/2066247685636583440)
- [16](https://x.com/JeremyCMorgan/status/2067034582629728467)
- [17](https://x.com/jerryjliu0/status/1770163771740459182)
- [18](https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade)
- [19](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)
- [20](https://x.com/josevalim/status/2002312493713015160)
- [21](https://neurips.cc/virtual/2025/poster/121601)

---

## Report from OPENAI_MINI (openai_mini)

# Executive summary

Across 2023–2026 practice, coding agents obtain cross-file dependency facts through four main mechanisms:

1. **Static-analysis / symbol-resolution pipelines**  
   Examples: CrossCodeEval’s static filtering of examples, STALL+’s dependency extraction, PyCG-like call-graph tools, import resolution, and repo graphs. These are the most “structural” and least heuristic. They work best in **Python only when the code is type-friendly and import structure is conventional**; they are much weaker for dynamic dispatch, monkey-patching, runtime wiring, and config-driven imports. Empirically, they often help on repository-level completion, but gains are not universal and vary by language and analysis phase. ([arxiv.org](https://arxiv.org/abs/2310.11248))

2. **Language-server-as-tool (LSP)**
   Examples: `python-lsp-server`, Pyright/Pylance-style servers, and LSP-guided RAG ideas. This is mature operationally for **interactive IDE use** and increasingly feasible headless, but its structural facts are limited to what the server can resolve in the current environment. For Python, `python-lsp-server` exposes definitions/references/symbols via Jedi, while Pyright is a fast static type checker that can be run in server mode and configured for version/platform/stub resolution. ([github.com](https://github.com/python-lsp/python-lsp-server))

3. **Code-graph retrieval / graph-native navigation**
   Examples: RepoGraph, CodexGraph. These convert a repository into a graph and let the agent query dependencies, callers, importers, and related symbols more precisely than plain text retrieval. The papers report competitive gains on repo-level benchmarks, including SWE-bench and CrossCodeEval, but the systems are still recent research prototypes rather than established defaults. ([arxiv.org](https://arxiv.org/abs/2410.14684))

4. **Plain retrieval over code, plus tests as verification**
   Retrieval is broadly mature and easy to deploy, but weak on precise dependency facts when the query requires multi-hop structure rather than lexical similarity. Tests are excellent as **verification**, but poor as **discovery** of cross-file facts. CrossCodeEval and STALL+ both show that structure-aware context beats “current file only” baselines, but that simple retrieval remains a strong baseline and structural context is not always enough by itself. ([arxiv.org](https://arxiv.org/abs/2310.11248))

Bottom line: for an autonomous Python editing agent, the most evidence-backed design is **hybrid**: use **headless LSP/static analysis for symbol and import resolution**, **graph or retrieval to expand candidate context**, and **tests for validation**. Relying on tests alone is not a substitute for dependency discovery. ([arxiv.org](https://arxiv.org/abs/2406.10018))

---

# Key findings

## 1) Concrete mechanisms and maturity

### A. Static analysis / call graphs / dependency extraction
- **CrossCodeEval** uses a static-analysis-based procedure to identify code regions that *require* cross-file context, creating a benchmark where current-file-only context is insufficient. That is important because it makes structural dependency needs measurable rather than anecdotal. ([arxiv.org](https://arxiv.org/abs/2310.11248))
- **STALL+** explicitly integrates static analysis in three phases: prompting, decoding, and post-processing. The paper’s goal is not just accuracy but also efficiency of those integration points. ([arxiv.org](https://arxiv.org/abs/2406.10018))
- **Python maturity:** Stronger for import and symbol resolution than for full program semantics. A separate 2024 empirical study found that for Python call-graph generation, traditional static tools like **PyCG** outperform LLMs; however, another 2024 study on Python dependency resolution found static dependency extraction without installation can be inaccurate due to environment and extra-dependency effects. ([arxiv.org](https://arxiv.org/abs/2410.00603))
- **Headless maturity:** High if the codebase is analyzable offline. Low-to-medium when the repository uses dynamic imports, environment-conditioned logic, or nonstandard packaging. ([arxiv.org](https://arxiv.org/pdf/2401.02090))

### B. Language-server-as-tool
- **python-lsp-server**: the server exposes completions, definitions, hover, references, signature help, and symbols via **Jedi**; it can be run as `pylsp` from the command line, which makes it usable headlessly. ([github.com](https://github.com/python-lsp/python-lsp-server))
- **Pyright**: the configuration documents show it is explicitly tuned for source-file resolution, type stubs, Python version, and platform. It also has a CLI/server mode used in practice, including headless setups. ([github.com](https://github.com/microsoft/pyright/blob/main/docs/configuration.md?plain=1))
- **LSP maturity for Python/headless:** operationally mature, but it is still bounded by semantic resolution quality. It is best viewed as a **symbol oracle**, not a whole-repo oracle. ([github.com](https://github.com/python-lsp/python-lsp-server))

### C. Code graph retrieval
- **RepoGraph** builds a repository-level graph and uses it for navigation and context selection. The paper reports evaluation on SWE-bench and CrossCodeEval and describes it as a repository-wide navigation layer. ([arxiv.org](https://arxiv.org/abs/2410.14684))
- **CodexGraph** uses a graph database schema extracted from the repository and a query-language interface so the agent can ask structure-aware questions. It is evaluated on CrossCodeEval, SWE-bench, and EvoCodeBench. ([arxiv.org](https://arxiv.org/abs/2408.03910?utm_source=openai))
- **Maturity:** promising but still research-grade. Better than plain text retrieval for structural questions, but not yet an industry-standard dependency oracle. ([arxiv.org](https://arxiv.org/abs/2410.14684))

### D. Retrieval over code + tests
- Retrieval remains the simplest and most deployable mechanism. CrossCodeEval and later graph systems treat BM25 / retrieval baselines as useful but incomplete. ([arxiv.org](https://arxiv.org/abs/2310.11248))
- Tests are used extensively in SWE-agent-style workflows, but SWE-agent’s own paper emphasizes that its core strength is editing and verification loops, not whole-repo localization. ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf))
- **Maturity:** highest for general deployment, lowest for precise cross-file dependency facts. ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf))

---

# Detailed analysis

## Comparison map

| Mechanism | Python maturity | Headless maturity | Measured effect on accuracy | Latency / cost in agent loop | Failure modes / blind spots |
|---|---:|---:|---|---|---|
| Static analysis / call graphs | Medium-High for imports/calls; weaker for dynamic Python | High if repo is analyzable offline | Strong in repo-level completion when used well; STALL+ finds best gains when static cues are injected in the **prompting** phase, and Python benefits differently from Java because dynamic analysis is limited in Python | Usually moderate upfront indexing cost; can reduce repeated search once built | Dynamic dispatch, monkey-patching, `getattr`, reflection, config-driven wiring, import-time side effects, environment-sensitive deps, stale index if code changes mid-session ([arxiv.org](https://arxiv.org/abs/2406.10018)) |
| LSP tool use | High for common Python projects | High; `pylsp` and Pyright can run headless | Good for symbol-level facts; not directly benchmarked as a full agent dependency oracle in the surveyed papers | Low per query if server is warm; startup/indexing can matter | Misses runtime-only edges, incomplete in partially typed code, depends on workspace config and stub quality ([github.com](https://github.com/python-lsp/python-lsp-server)) |
| Repo graph / code graph retrieval | Medium-High, depending on parser and schema | Medium-High; designed for tool use, but still prototype-like | Reported competitive boosts on SWE-bench and CrossCodeEval; graph-aware retrieval outperforms plain BM25 in the cited systems | Higher upfront build cost, but queries can be precise and repeated cheaply after indexing | Graph incompleteness, parser errors, stale index, difficulty modeling dynamic Python behavior, overfitting to graph schema ([arxiv.org](https://arxiv.org/abs/2410.14684)) |
| Plain retrieval over code | High deployment maturity | High | Useful baseline, but weaker than dependency-aware context on CrossCodeEval-style tasks; a plain retrieval baseline is still often competitive enough to remain a serious comparator | Fast and cheap; no special index beyond embedding/BM25 | Lexical mismatch, misses multi-hop dependencies, poor recall for “where is this symbol wired?” questions ([arxiv.org](https://arxiv.org/abs/2310.11248)) |
| Tests as verifier | Very high | Very high | Good at confirming a fix; poor at revealing where cross-file dependencies live | Expensive if full suite is large; loop can be slow | Cannot localize bugs by itself; may pass despite wrong architectural edits if tests are weak or incomplete ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)) |

---

## 2) What the benchmarks actually show

### CrossCodeEval
CrossCodeEval was designed precisely to make cross-file context necessary, using static analysis to identify cases where the answer cannot be inferred from the current file alone. The benchmark spans Python, Java, TypeScript, and C#, and the paper reports that performance improves dramatically when relevant cross-file context is added. That makes it a good benchmark for testing dependency-context mechanisms rather than mere code completion. ([arxiv.org](https://arxiv.org/abs/2310.11248))

### STALL+
STALL+ is one of the clearest pieces of evidence that **static analysis helps, but placement matters**. The paper states:
- prompting-phase static cues work best,
- post-processing is worst,
- and Python and Java benefit differently because Python’s dynamic nature limits static precision.  
It also reports complementarity between RAG and static analysis, which is important: static structure and lexical retrieval solve different subproblems. ([arxiv.org](https://arxiv.org/abs/2406.10018))

### RepoGraph / CodexGraph
Both systems are evidence that **graph-native context retrieval is practical and useful** for repository-scale code tasks. Their evaluations on CrossCodeEval and SWE-bench suggest that structured navigation can improve agent behavior beyond plain search. However, these are still newer systems, and the evidence base is narrower than for plain retrieval or tests. ([arxiv.org](https://arxiv.org/abs/2410.14684))

### PyCG / static call-graph analysis evidence
A 2024 empirical study found that for Python call-graph generation, a traditional static analyzer like PyCG outperforms LLMs. This is useful because it suggests that if your goal is structural dependency facts, mature static tools are still better than asking an LLM to “infer” them. But another 2024 study warns that static dependency graphs in Python can be inaccurate when environment and packaging effects matter. ([arxiv.org](https://arxiv.org/abs/2410.00603))

### Tests
SWE-agent demonstrates that agentic editing can be driven by search, edit, and verification loops, and its evaluation shows it can solve many tasks in a handful of turns. But the paper also makes clear that HumanEvalFix is not the same as repository navigation: localization and navigating a large codebase are not necessary there, so it is not evidence that tests can replace structural dependency discovery. ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf))

---

## 3) Failure modes and blind spots

### Static analysis / call graphs
Known blind spots are especially pronounced in Python:
- dynamic dispatch,
- monkey-patching,
- `__getattr__`, decorators, metaprogramming,
- import-time side effects,
- config-driven or environment-conditioned imports,
- packaging/install-time differences,
- and stale caches when the repo changes during the agent session.  
ModuleGuard’s discussion of environment-aware dependency resolution is a good concrete reminder that “static dependency graph” and “actual runtime dependency graph” can diverge substantially in Python. ([arxiv.org](https://arxiv.org/pdf/2401.02090))

### LSP
LSP gives you **resolved names and references**, but not necessarily full semantic truth. It can miss:
- runtime-only edges,
- unresolved symbols in incomplete code,
- custom import patterns outside the server’s analysis model,
- and cases where the environment or stub set is not aligned with the repo.  
That said, it is practical and mature for symbol lookup in headless use. ([github.com](https://github.com/python-lsp/python-lsp-server))

### Graph retrieval
Graph retrieval is excellent when the needed fact is representable as nodes and edges, but it can fail when:
- the graph is stale,
- parsing is incomplete,
- the schema omits relevant runtime relations,
- or the agent asks a question that requires semantic interpretation beyond the graph.  
The 2024 graph systems are promising but still depend on offline graph construction and quality of the extracted graph. ([arxiv.org](https://arxiv.org/abs/2410.14684))

### Plain retrieval
Plain retrieval is often too shallow for cross-file dependency questions because it is driven by lexical similarity rather than topology. The benchmark literature explicitly positions it as insufficient alone for many CrossCodeEval cases. ([arxiv.org](https://arxiv.org/abs/2310.11248))

### Tests
Tests are great for **validation** and bad for **discovery**. They tell you whether a change broke behavior, not where the relevant dependency edges are. In large codebases with weak coverage, they can give false confidence. ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf))

---

# Practical recommendation for the agent decision

For an autonomous Python code-editing agent, the best-supported workflow is:

1. **Use headless LSP / static analysis first** for symbol resolution, imports, references, and candidate dependency edges.  
2. **Use graph or retrieval second** to expand context around the resolved symbols.  
3. **Use tests last** to verify the edit.  

If you need a single default mechanism, the evidence favors **headless static analysis + LSP**, with retrieval as a fallback. If you can afford a richer system, use **a repository graph** on top. Tests should not be the primary source of dependency facts. ([arxiv.org](https://arxiv.org/abs/2406.10018))

---

# Unresolved questions / disconfirming evidence

- **Do structural dependency tools always help?** No. STALL+ shows the best gains depend on phase and language, and Python’s dynamic nature weakens static-analysis benefits relative to Java. ([arxiv.org](https://arxiv.org/abs/2406.10018))
- **Can plain retrieval sometimes be “good enough”?** Yes, especially when the dependency is lexically obvious or the repo is small. The existence of strong retrieval baselines in CrossCodeEval and related work shows structure is not the only signal. ([arxiv.org](https://arxiv.org/abs/2310.11248))
- **Can an LLM infer call graphs instead of using tools?** For Python, the 2024 empirical study says no: traditional static analysis still beats LLMs for call-graph generation. ([arxiv.org](https://arxiv.org/abs/2410.00603))
- **Can static dependency graphs be trusted in Python packaging contexts?** Not fully. ModuleGuard shows that environment-aware resolution is necessary because static resolution without installation can be inaccurate. ([arxiv.org](https://arxiv.org/pdf/2401.02090))
- **Is there a mature, universally accepted standard for agent dependency context?** Not yet. The field is converging on hybrids, not single-tool solutions. The evidence base from 2024–2025 graph systems and static-analysis ablations supports that conclusion. ([arxiv.org](https://arxiv.org/abs/2406.10018))

---

# Bibliography

- Ding et al. / CrossCodeEval: **CrossCodeEval: A Diverse and Multilingual Benchmark for Cross-File Code Completion** (NeurIPS 2023 / 2024 proceedings). ([arxiv.org](https://arxiv.org/abs/2310.11248))
- Liu et al.: **STALL+: Boosting LLM-based Repository-level Code Completion with Static Analysis** (2024). ([arxiv.org](https://arxiv.org/abs/2406.10018))
- Ouyang et al.: **RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph** (2024). ([arxiv.org](https://arxiv.org/abs/2410.14684))
- Liu et al.: **CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases** (2024/2025). ([arxiv.org](https://arxiv.org/abs/2408.03910?utm_source=openai))
- Yang et al.: **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** (2024). ([papers.neurips.cc](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf))
- Venkatesh et al.: **An Empirical Study of Large Language Models for Type and Call Graph Analysis** (2024). ([arxiv.org](https://arxiv.org/abs/2410.00603))
- ModuleGuard paper: **ModuleGuard: Understanding and Detecting Module Conflicts in Python Ecosystem** (ICSE 2024). ([arxiv.org](https://arxiv.org/pdf/2401.02090))
- `python-lsp-server` project documentation. ([github.com](https://github.com/python-lsp/python-lsp-server))
- Pyright configuration documentation. ([github.com](https://github.com/microsoft/pyright/blob/main/docs/configuration.md?plain=1))

If you want, I can turn this into a **decision matrix** for your specific Python agent architecture, e.g. “best default,” “best low-latency option,” and “best high-accuracy option.”

### Sources from this provider
- [CrossCodeEval: A Diverse and Multilingual Benchmark for Cross-File Code Completion](https://arxiv.org/abs/2310.11248)
- [GitHub - python-lsp/python-lsp-server: Fork of the python-language-server project, maintained by the Spyder IDE team and the community · GitHub](https://github.com/python-lsp/python-lsp-server)
- [RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph](https://arxiv.org/abs/2410.14684)
- [STALL+: Boosting LLM-based Repository-level Code Completion with Static Analysis](https://arxiv.org/abs/2406.10018)
- [An Empirical Study of Large Language Models for Type and Call Graph Analysis](https://arxiv.org/abs/2410.00603)
- [ModuleGuard: Understanding and Detecting Module Conflicts in Python Ecosystem](https://arxiv.org/pdf/2401.02090)
- [pyright/docs/configuration.md at main · microsoft/pyright · GitHub](https://github.com/microsoft/pyright/blob/main/docs/configuration.md?plain=1)
- [CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases](https://arxiv.org/abs/2408.03910?utm_source=openai)
- [https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf](https://papers.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)

---
