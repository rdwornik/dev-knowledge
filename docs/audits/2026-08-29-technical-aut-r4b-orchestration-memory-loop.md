> **PROVENANCE — harvested cloud artifact, body VERBATIM below this header.**
> Lane `AUT-R4-B orchestration-memory-loop` | receipt id `cse_01YC8vD5KoxU66fwKZavMtL1` | dispatched 2026-08-29, harvested 2026-08-29 by `Save-CloudSessionReport` (the `Harvest-Cloud` alias).
> Selection rule: the LONGEST assistant text, not the last — longest assistant text.
> Bytes written unchanged: **68,070**. See harvester log for deviation status.
> Nothing below this line was edited, reflowed or trimmed.

---

# AUT-R4-B — machinery: orchestration · local memory/index · loop optimization

**Lane:** AUT-R4-B (CLOUD, READ-ONLY) · **Repo:** `.dev-knowledge` @ `main` (`66662c7`) · **Date:** 2026-08-29
**Rows birthed:** ZERO. No commit, no push, no `tasks/` edit, no intake, no ADR draft. Working tree untouched.

---

## §0 — Method, and the honesty envelope

**Interpreter, declared as the brief requires.** Every command ran under `python3` (**CPython 3.11.15**, the cloud image's system interpreter) directly. **`uv` was never invoked**; no gate was run; **no gate result is reported anywhere below.** Where I needed a package the repo does not install (`rustworkx`, `sqlite-vec`), I built a throwaway venv under `/tmp` — the repo checkout was not mutated and `pyproject.toml`/`uv.lock` were read-only inputs.

**A caveat that qualifies every closure number I report.** Dependency closures were resolved with `pip install --dry-run --report` on **Linux / CPython 3.11**, not Windows / CPython 3.12.10 (the repo's `.python-version`). Marker-conditional deps differ across those two axes. The numbers are *measured*, but they are measured on the wrong platform, and the right platform is the operator's. Treat them as a **correctly-ordered ranking with approximately-correct magnitudes**, not as a Windows bill of materials.

**What the network refused me.** `arxiv.org`, `huggingface.co`, `semanticscholar.org`, `emergentmind.com` and `alexgarcia.xyz` are **blocked by this session's egress proxy** (verified: `curl` returns `CONNECT tunnel failed, response 403`; WebFetch returns `EGRESS_BLOCKED`). `api.github.com` is gated to this session's single allowed repo. So: **I could not read a single arXiv abstract at source.** Paper claims below are marked `search-relayed` and are explicitly *not* primary-verified. `github.com` HTML *was* reachable and I used it. PyPI and npm registry JSON were reachable and are the backbone of the maturity evidence.

**Evidence tiers used throughout:** **measured** (a study, a benchmark, or a number I produced this session) · **practiced** (organisations do it, no measurement) · **asserted** (someone recommends it).

---

## §1 — THE SHELF 4 VERDICT (lead, as the brief requires)

> **Can a LangGraph-class state machine replace our hand-rolled lane plumbing while the gates stay?**
>
> **No — and the reason is not the one the hypothesis anticipates.**

The hypothesis on the table was *our moat is gates and contracts, not call-orchestration*, with the implication that the call-orchestration half is therefore commodity and swappable. **The first half of that is right and the second half does not follow**, because of a structural fact I had to measure to state:

**Our "lane plumbing" is not a call graph. It is a git-topology protocol.** Read PLAYBOOK Ch8's five per-lane requirements (`protocols/PLAYBOOK.md:1878-1901`) and count what a runtime would actually have to own:

1. a **frozen contract** — a *committed repo artifact*, frozen against mid-flight instruction injection (`STANDING_RULINGS` D2);
2. a **V-2 decision budget** — three named escalation classes, everything else decided-and-reported;
3. **`uv run --locked` on every test invocation** — because a bare `pytest` in a worktree inherits `VIRTUAL_ENV` from the primary tree and reports green about code the lane never touched (`STANDING_RULINGS` D4);
4. **commit-and-STOP with `git stash list` empty** — because `refs/stash` lives in the **common git directory**, not the worktree's private ref space, and therefore survives `git worktree remove`, `prune`, the branch delete, and all four of the other refuse-to-finish items (`PLAYBOOK.md:1889-1898`);
5. **one worktree = one branch = one contract file**, checkable by `scripts/validate_branch_naming.py`.

Not one of those five is a node, an edge, or a state transition. Four of the five are **assertions about the git object database and the filesystem**; the fifth is a governance rule about which decisions a seat may take. LangGraph's `StateGraph` + checkpointer would replace **none** of them, because LangGraph does not know what a worktree is.

**Now argue it the other way, honestly, because there is a real case.** What LangGraph genuinely offers is **durable execution**: state is persisted per step, and an interrupted run resumes from its last checkpoint ([LangChain changelog, LangGraph 1.0 GA 22 Oct 2025](https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available); [durable-execution docs](https://docs.langchain.com/oss/python/langgraph/durable-execution) — *practiced*). And there **is** a resumability hole in the night batch: PLAYBOOK's five night phases (`:2200-2225`) have no mechanism for a lane that dies at 03:00 to resume at the step it died on. That is a real gap and it is the strongest thing the pro-LangGraph side has.

Three things kill it anyway, and the third is the decisive one:

- **The Layer-2 invariant.** `CLAUDE.md` §5 rule 4: *"Layer 2 never executes — no orchestration scripts: no script drives state in a child repo."* A `StateGraph` whose nodes invoke lanes is, definitionally, a script that drives state. This does **not** kill the *class* of candidate — it **relocates** it. A durable-execution runtime is legitimate in `corp-monorepo` or `ai-council`, which run things. It is illegitimate *here*, in the repo whose defining property is that it does not run. (More precisely: it is illegitimate as an **organ**. Nothing stops the hub from *documenting* the pattern for a child.)
- **The dispatch surface is a human at a terminal, by ruling.** `PLAYBOOK.md:2416` — *"Dispatch visibility — Agent View shows DISPATCHED sessions only"* (STANDING_RULINGS B7), whose stated consequence is that *"a lane is dispatched by the operator rather than spawned from a session, a spawned session having no Agent View row of its own."* A graph runtime's whole value proposition is spawning nodes programmatically. Here, a programmatically-spawned lane is **invisible to the operator's board** — which is precisely the failure mode the ruling exists to prevent. The framework's core feature is this repo's recorded anti-feature.
- **The plumbing is already durable, in a substrate LangGraph cannot checkpoint into.** A lane's state *is* its branch. `git log`, `git worktree list`, `git stash list` and the branch-name grammar are the checkpoint store, and they survive machine death, process death and session death with no runtime at all. LangGraph would add a **second, weaker** durability layer (SQLite checkpointer, `langgraph-checkpoint-sqlite` 3.1.1, 2026-07-30 — *measured*, PyPI) that does not know about the first one and cannot be reconciled with it. Two sources of truth for "where is this lane" is worse than one.

**The falsifier, stated so this verdict is not unfalsifiable.** If lane count ever exceeds what one operator can dispatch by hand — the 2026-04-24 verdict's own reopening trigger was *"team grows beyond solo"* — the dispatch-visibility argument weakens, because a board nobody reads is not a constraint. Widen past roughly 10 concurrent lanes (`templates/prompt-template.md`'s stated ceiling) and re-take this. Below that, no.

**Verdict: `partial` on the underlying need, `absent`-and-should-stay-absent on the framework.** The organ is `protocols/PLAYBOOK.md` Ch8 "The batch protocol" (`:1846`) + "The lane lifecycle" (`:2046`) + `/lane-boot` + `/lane-integrate` + `scripts/validate_branch_naming.py`. **What is genuinely missing is one thing and it is small:** mid-lane resumability — a lane that dies has no recorded resume point. That is a **checkpoint file convention**, not a graph runtime.

---

## §2 — SHELF 4: AGENT ORCHESTRATION

### 2.0 RECONCILE FIRST — the prior LangChain verdict is **located**, and it carries a reopening trigger

The brief anticipated I might not find it. I found it twice, and the second is a re-affirmation of the first.

**Primary verdict — `docs/audits/2026-04-24-council-28-29-consolidated-actions.md:117-120`**, verbatim:

> `### P3-3: LangGraph / AutoGen / CrewAI frameworks`
> `**Source:** Multi-agent debate research`
> `**Status:** Skip — AI Council already implements proposer-critic-synthesizer pattern at solo-dev scale`
> `**Reopening trigger:** team grows beyond solo, or AI Council proves insufficient`

**Re-affirmation — `docs/audits/2026-08-23-technical-research-model-bus.md:243-245`**: *"`langchain` / LangGraph — REJECT, already measured… the prior outcome stands."*

**The re-assessment at today's scale, which is the part that matters.** The 2026-04-24 verdict answered a **different question** from the one this brief asks. It scored these frameworks as **multi-agent debate orchestrators** — the research it cites is `docs/archive/2026-04-24-multi-agent-debate-patterns.md`, whose subject is agents arguing to consensus. Today's question is whether a state machine can carry **lane plumbing**. That is not the same candidate wearing the same name, and treating the 2026-04-24 Skip as dispositive would be exactly the "relitigate silently" failure inverted — resting on a prior verdict that never reached the question.

So: the prior verdict **stands on debate orchestration** (trigger unfired — still solo, AI Council not shown insufficient), and **does not reach lane plumbing**, which §1 answers freshly and negatively. Both statements are needed; either alone misreports the record.

One further note on that 2026-04-24 file: its own findings include *"errors in one agent can cascade"* and *"standard metrics (ROUGE, BLEU) fail to capture debate quality"* (`:44` region — *asserted*, LLM-provider-generated research from Perplexity/Gemini, and it says so in its header). Its "40–50% cost reduction" figure for LangGraph is attributed to `[Perplexity]` with no primary citation. **I would not carry that number forward.** It is the weakest evidence in the in-repo record on this shelf and it has been cited twice since.

### 2.1 LangChain / LangGraph — `partial` (need), framework **absent by design**

**Maturity (measured, PyPI JSON, 2026-08-29):** `langgraph` **1.2.11**, uploaded **2026-08-11**; 276 releases since 2024-01-08; `requires-python >=3.10`. `langchain` **1.3.18** (2026-08-27), with `1.4.0a2` already out (2026-08-28) — **514 releases**, i.e. a release roughly every 2.5 days over its life. That cadence is a two-sided signal: alive, and a moving target for a repo whose `uv` pin is a *deliberately gated change*.

**Installability under the hard constraint (measured, this session):** `langgraph` resolves to a **35-package closure** — **exactly the size of this repo's entire current lock** (`grep -c '^\[\[package\]\]' uv.lock` → **35**). With the SQLite checkpointer: **38**. Pure-Python wheels (`py3-none-any`), no Windows-specific hazard. **Self-hosted-friendly: yes** — the SQLite checkpointer means no server and no LangSmith account is *required*. That is genuinely better than the shape the constraint excludes, and I want to be fair about it: LangGraph is not a heavyweight server stack. **It is excluded here on the Layer-2 invariant and on dispatch visibility, not on installability.**

**Negative result, first-class.** There is a well-documented "orchestration framework trap" literature: teams adopting LangChain, gaining early velocity, then rewriting to raw SDKs. Octomind (a YC company that had built its product on LangChain) published the canonical postmortem in 2024; the pattern recurred through 2025-2026 ([TianPan, "The Orchestration Framework Trap", 2026-04-19](https://tianpan.co/blog/2026-04-19-orchestration-framework-trap-langchain-production); [Ravoid, "The LangChain Exit", 2026](https://ravoid.com/blog/langchain-exit-raw-sdk-migration-2026/) — *practiced*, secondary; I could not reach octomind.dev directly — DNS failure — so the primary postmortem is **unverified at source**). The specific complaint most relevant here: *no way to inspect or modify agent state mid-run*. This repo's V-2 decision budget is precisely a mid-run state-inspection protocol.

**Cheapest experiment that would settle it (Tier S, ~1 window):** don't install LangGraph. **Write the resume-point convention instead** — a lane emits `<worktree>/.lane-state.json` after each numbered step (step index, last commit SHA, footprint touched); `/lane-boot` reads it and offers resume. Kill it if two consecutive batches show zero lane deaths. That buys the *only* thing LangGraph offers here, at zero packages, inside the invariant.

### 2.2 AutoGen — **`absent`, and it is now abandonware in the precise sense**

**This is the strongest negative result on the shelf, and it is verified at two independent sources.**

- **PyPI (measured):** `autogen-agentchat` and `autogen-core` both sit at **0.7.5, last uploaded 2025-09-30** — **eleven months** with no release. `pyautogen` (the older distribution) last released **2025-07-15** — thirteen months.
- **GitHub README (verified at source, github.com/microsoft/autogen):** *"AutoGen is now in maintenance mode. It will not receive new features or enhancements and is community managed going forward."* Microsoft Agent Framework is named *"the enterprise-ready successor to AutoGen."* 60.7k stars, 547 open issues.

**This directly falsifies the in-repo record.** `docs/archive/2026-04-24-multi-agent-debate-patterns.md:116` still describes AutoGen as a leading production framework with *"54,600+ GitHub stars"* and *"best-in-class human-in-the-loop"*. That file is `retention: exempt-permanent` and immutable, so it cannot be corrected in place — but anything citing it forward should carry this correction. **A framework whose Python packages have been silent for eleven months and whose README says "maintenance mode" is not a candidate.**

**Verdict: `absent`** — searched `autogen|AutoGen` repo-wide (hits only in the 2026-04-24 archive, ADR-42:196, and the 2026-04-24 P3-3 Skip). No organ, and none wanted.

### 2.3 Microsoft Agent Framework — **the successor, and it is the exact shape the constraint excludes**

**The "current leader we are missing" on the Microsoft axis.** `agent-framework` **1.16.0**, uploaded **2026-08-28**; 57 releases; actively shipping (*measured*, PyPI).

**And it is disqualified on the carried constraint by a wide margin: a 205-package closure** (*measured*) — **5.9× this repo's entire lock**. Compare the recorded precedent: the model-bus audit REJECTED `pydantic-ai` at **103 packages** as *"cost-for-purpose"* (`docs/audits/2026-08-23-technical-research-model-bus.md:230-233`). MAF is twice that. **Score against it explicitly: heavyweight, enterprise-oriented, and the migration target for a framework this repo already declined.** No further work owed.

### 2.4 CrewAI — **`absent`, and the release hygiene is its own finding**

`crewai` **1.15.18** (2026-08-27), **425 releases**, and — the part worth noticing — **dated dev builds published to PyPI daily**: `1.15.17.dev20260825`, `.dev20260826`, `.dev20260827`, `1.15.18.dev20260828`, `1.15.18.dev20260829` (*measured*, PyPI, 2026-08-29). A project that publishes a nightly to the public index every day is alive, but it is also a project whose version surface a `--locked` discipline has to work hard against. **134-package closure** (*measured*) — above the `pydantic-ai` rejection bar. Role-based crews solve a problem (multi-agent team simulation) this repo does not have: its lanes are file-disjoint by construction and communicate through git, not through conversation. **Verdict `absent`, and correctly so.**

### 2.5 Leaders the brief asked me to look for — the honest sweep

| Candidate | State (measured, PyPI 2026-08-29) | Read |
|---|---|---|
| **OpenAI Agents SDK** (`openai-agents`) | 0.22.0, 2026-08-19; 119 releases; **38-pkg closure** | Genuinely light. Vendor-locked to OpenAI's loop; this repo's routing is Claude-first with a registry (`ecosystem/provider-registry.yaml`). Wrong vendor, right weight. `absent`, no action. |
| **Google ADK** (`google-adk`) | 2.8.0, 2026-08-26; 25 unconditional deps | Same shape, different vendor lock. `absent`, no action. |
| **`pydantic-ai`** | 2.36.0, 2026-08-29 (shipping daily) | **Already rejected in-repo** at `docs/audits/2026-08-23-technical-research-model-bus.md:230`. Reconciled, not relitigated. |
| **Durable-execution class** (`temporalio` 1.32.0; `dbos` 2.31.0) | Both actively released Aug 2026 | This is the *category* that actually addresses §1's real gap. **`temporalio` needs a Temporal server** — squarely the "always-running server" shape the model-bus audit flagged (`:255-258`), and note that audit's own honest caveat: **it could not locate the no-always-running-servers rule in any canonical doc.** I re-ran that search and **confirm the finding: `grep -rn "always-running\|daemon\|127\.0\.0\.1" protocols/ docs/decisions/ ARCHITECTURE.md VISION.md` finds no such rule.** The constraint is real in practice and **ungated in doctrine**. Worth knowing. |
| **The boring answer nobody lists** | `git worktree` + `just`/`make` + the branch-name grammar | **This is what the repo already runs**, and §1 argues it is the correct substrate. Naming it as a candidate is not a joke — it is the incumbent, and no surveyed framework beat it on this repo's actual requirements. |

---

## §3 — SHELF 5: LOCAL MEMORY / INDEX

### 3.0 First, the need — measured, because a verdict against an imagined need is worthless

**The corpus (measured, this session, `git ls-files`):**

- **2,701** tracked files · **2,252** markdown files · **32,723,562 bytes (31.2 MiB)** · **418,512 lines** of markdown
- **324** Python files · **124,835** lines
- Concentration: `docs/audits` **828** files · `docs/handoffs` **710** · `docs/decisions` **91** · `docs/intake` **64**

**The FPG, as actually built (measured — I ran `scripts/file_purpose_graph.py stats` under a scratch venv with `rustworkx` installed, since the repo env is not built in this container):**

```
nodes    : 1666
edges    : 10745
  doc-code-edge          45
  audits-index          798
  consumer-at-landing  9467
  tasks-depends-on      391
  deploy-manifest        44
```

**Read those two blocks together and the gap is arithmetic.** The FPG has **1,666 nodes** against **2,701 tracked files**. Its own module header states the limit in terms that make it a feature, not a bug (`scripts/file_purpose_graph.py:60-64`): *"A path is governed iff at least one of the five inputs names it. Nothing else confers it… measured against the live tree, most of `scripts/` and all of `tests/` are UNKNOWN to this graph, and `why` refuses them. That refusal is the finding, not a gap in the query."*

**So the actual need is precise, and it is not "vector search over the repo."** The FPG answers *"who declared/enforces/indexes this file"* **deterministically and completely, for the 62% of the tree that a governance surface names**. What no organ answers is: *"of the 828 audits and 710 handoff files, which three bear on the thing I am about to do?"* — a **ranking** problem over an **ungoverned** corpus, not a graph-reachability problem. And **9,467 of 10,745 edges are one kind** (`consumer-at-landing`), which means the graph's discriminating power is already concentrated in a single relation; adding more deterministic edge kinds has diminishing returns where adding a *ranking* signal does not.

That is the honest framing for this shelf. Everything below is scored against it.

### 3.1 What local models are actually good for — the empirical core

**Good for — retrieval and ranking, at a quality that is measurably close to large models and orders of magnitude cheaper:**

- **`potion-base-32M` (Model2Vec static embeddings) reaches 94.66% of `all-MiniLM-L6-v2`'s performance, MTEB average 52.83** (*measured*, search-relayed from [MinishLab/model2vec results](https://github.com/MinishLab/model2vec/blob/main/results/README.md); I could not open the HuggingFace model card — egress-blocked — so the figure is **not primary-verified**). Throughput reported in the **20,000-30,000 sentences/sec** range on CPU vs low hundreds for MiniLM; model on disk **~30 MB**, smallest variants 4-8 MB retaining ~80-90%.
- **Retrieval-specific variants exist** (`potion-retrieval-32M`), which matters: a general-purpose static embedder underperforms on retrieval more than on classification, and the retrieval-tuned checkpoint is the one to test.

**Not good for — and this is the load-bearing negative:**

- **Decision-making and generation quality.** No local embedder ranks, judges, or decides. A static embedder has no notion of *"what matters"* — it has a notion of *"what is textually similar."* For a governance corpus where the important document is frequently the one that **contradicts** the current draft, similarity and importance are not the same signal, and a similarity index will confidently rank the near-duplicate above the contradiction.
- **The importance-learning claim is where I want to be most careful.** "Learned importance" implies supervision, and this repo's only labels are the ones the operator already writes by hand (`refs`, `kill-candidates`, `serialize-group`, the funnel triage verdicts). **No source I found demonstrates learned importance ranking over a single-operator governance corpus.** That is a **hypothesis**, and I am labelling it one: *no source found*.

### 3.2 `sqlite-vec` — **`partial`, and it is the right first probe — I measured it**

**The R-A grounding is correct and I verified it.** `protocols/STANDING_RULINGS.md:3267` records that at **11,684 edges** stdlib `sqlite3` answers reachability/orphan/degree in **1-4 ms**, and a graph library wins on **cycles/SCC only**. sqlite is already the repo's measured store of record for graph-shaped questions, plus telemetry v1 runs a WAL-mode SQLite store (`ecosystem/conformance.md:26`, `[#529]`, closed 2026-08-22).

**Maturity (measured, PyPI):** **0.1.9**, uploaded **2026-03-31**; 69 releases since 2024-04-27. **The stable line has not moved in five months** — the only newer artifacts are alphas (`0.1.10a4`, 2026-05-18). GitHub (verified at source): **8.1k stars**, **155 open issues**, README carries *"sqlite-vec is a pre-v1, so expect breaking changes!"*, backed by **Mozilla Builders** with Fly.io / Turso / SQLite Cloud sponsorship. Pure C, no dependencies.

**Installability under the hard constraint — this is where the brief's `rustworkx` bar gets met, and it is the best result on this shelf:**

- **`sqlite_vec-0.1.9-py3-none-win_amd64.whl` exists on PyPI** (*measured*). Prebuilt, no toolchain — the same shape as the `rustworkx-0.18.1-cp310-abi3-win_amd64.whl` precedent recorded at `pyproject.toml:47-48`.
- **Closure: 1 package.** Not 1 plus deps — **one**. Against a 35-package lock, this is the cheapest candidate in the entire survey by an order of magnitude.
- **The scary-looking blocker is a false alarm, and I chased it down.** [asg017/sqlite-vec issue #284, "sqlite-vec cannot be installed via uv on Windows", opened 2026-04-18, still open](https://github.com/asg017/sqlite-vec/issues/284) — the reporter used **`uv tool install`**, which requires console entry points; sqlite-vec is a library and has none. The error is *"No executables are provided by package"*. **`uv add` / `uv pip install` are not implicated.** Anyone grepping for "sqlite-vec uv Windows" will hit this issue and draw the wrong conclusion; it is a user error with an alarming title.
- **The real Windows risk is different and is `enable_load_extension`.** CPython's Windows build historically shipped `sqlite3` with extension loading disabled; [cpython issue #95656 "Enable sqlite extensions in the Windows build"](https://github.com/python/cpython/issues/95656) is **closed**, resolved by PR #95662 — but the page I could reach **does not state which release carried it**, so **I could not pin the version**. Mitigating evidence: this repo runs uv-managed Python (python-build-standalone), and sqlite-vec's own CI uses `uv run --managed-python` (*search-relayed*). **This is the single fact I would insist on verifying on the operator's actual machine before adopting.**

**Measured probe (this session, Linux, stock CPython 3.11 venv):**

```
sqlite_vec version: 0.1.9        vec_version: v0.1.9
insert 5,000 × 384-d vectors:                 0.08 s
brute-force kNN, k=10, mean of 20 queries:    3.43 ms
```

**Why that number settles the shelf's architecture question.** sqlite-vec is **brute-force only — no HNSW, no IVF, no DiskANN** (*measured*, corroborated across sources; FAISS/usearch outperform it, and HNSW gives ~10-40× over brute force at scale). At **2,252 markdown files**, even a generous 10 chunks/file is **~22,000 vectors** — roughly 4× my probe, so **~15 ms per query, single-threaded, in-process**. **The corpus is three to four orders of magnitude below where an ANN index earns its complexity.** sqlite-vec's headline limitation is irrelevant *at this repo's size*, and every heavier candidate on this shelf is paying for an index this corpus will never need.

**Verdict `partial`:** the *store* is `already-have-it` in kind — stdlib `sqlite3` is the ruled mechanism (R-A) and telemetry already runs a WAL store. What is missing is a vector column and an embedding producer. **Cheapest experiment (Tier S, half a window):** embed the 828 `docs/audits/*.md` titles + first-200-words with `potion-retrieval-32M`, load into one `vec0` table, and answer *"which prior audit bears on this brief?"* for **five real briefs whose right answer the operator already knows**. Keep iff ≥4/5 put the known-right document in the top 3. That is a real acceptance criterion, frozen ex-ante, in the ADR-108 §B shape.

### 3.3 ChromaDB — `absent`, and it loses to `sqlite-vec` on this repo's own scoring rules

**Maturity (measured):** 1.5.9, 2026-05-05; 130 releases; Rust core; **`chromadb-1.5.9-cp39-abi3-win_amd64.whl` exists** — Windows is fine. **Closure: 79 packages** — 2.3× the lock, and past the `pydantic-ai`/103 rejection bar's spirit. The Rust rewrite introduced breaking changes (settings ignored, env vars replaced by config files — *practiced*, [Chroma migration docs](https://docs.trychroma.com/docs/overview/migration)).

**It loses on the constraint, per candidate as the brief demands: 79 packages to get a feature `sqlite-vec` delivers in 1, on a corpus small enough that the extra 78 buy nothing measurable.** Chroma is also historically server-shaped (client/server mode is its production story), which scores against it here. **Note the in-repo prior:** `docs/handoffs/2026-07-17-corp-monorepo-executor-product-execution/PROMPT_arc-b-execution.md:95` lists *"ChromaDB fallbacks"* as a **DEFER-field row explicitly not to be executed** — a prior disposition, in a child-repo context, pointing the same way.

### 3.4 LanceDB — `absent`, but it is the **best of the heavyweights** and I want that on record

**Maturity (measured):** **0.37.1, uploaded 2026-08-10** — the most recently-released store on this shelf; 100 releases; `lancedb-0.37.1-cp310-abi3-win_amd64.whl` present. **Closure: 17 packages** — *half* of LangGraph's, and the smallest of any real vector database here. Embedded/serverless, Rust, columnar Lance format, **disk-based rather than memory-resident** (*practiced*).

**Where it would beat `sqlite-vec`:** datasets exceeding RAM, real ANN indexing, multimodal. **None of those describe a 31 MiB markdown corpus.** So `absent`, on scale rather than on quality — and if this repo ever *did* outgrow brute force, **LanceDB, not Chroma, is the successor to test**. Worth saying plainly because the two are usually listed as peers and on this repo's constraint they are not: 17 packages vs 79.

### 3.5 `sentence-transformers` — **`absent`, and it is the clearest constraint kill in the survey**

**Maturity (measured):** 6.0.0, 2026-08-18 — extremely healthy, 82 releases since 2019, the reference implementation.

**And it is disqualified on Windows weight, measured rather than asserted.** Its unconditional dependencies are `transformers>=5.0.0`, `tokenizers`, `huggingface-hub`, **`torch>=2.2`**, `numpy`, `scikit-learn`, `scipy`. **Closure: 58 packages.** And the decisive number: **`torch-2.13.0-cp312-cp312-win_amd64.whl` is 122.1 MB** for that one wheel (*measured*, PyPI file metadata).

Set that against the recorded standard of care. `pyproject.toml:55-59` documents, as a cost worth writing three sentences about, that `rustworkx` **moves `numpy` from the opt-in analytics group into the default dev group** — *"That is the real price of the library-first call and it is on the record rather than in a diff nobody reads."* A repo that documents one already-locked package moving groups **cannot** absorb PyTorch into `uv sync --locked` without a ruling. **Score against it explicitly, per the brief: heavyweight, and excluded.**

**The replacement, and this is the shelf's most actionable finding:**

- **`model2vec` — 22-package closure, pure-Python wheel, NO torch at inference** (*measured*). Static embeddings; `potion-retrieval-32M` at ~94.7% of MiniLM quality (*measured, search-relayed*). **This is the embedder to pair with `sqlite-vec`.**
- **`fastembed` — 28 packages, ONNX-based**, pure-Python wheel + `onnxruntime` whose **win_amd64 cp312 wheel is 14.0 MB** — not 122 (*measured*). The middle option if static embeddings underperform on retrieval.

`sentence-transformers` 58 + torch 122 MB → `model2vec` 22 + ~30 MB, at ~95% of the quality, on a corpus that fits in RAM. **That trade is not close.**

### 3.6 Mem0 / Letta / Zep — `absent` **all three**, and two of them are negative results worth more than the candidates

**Zep — the OSS product no longer exists.** Verified at source (github.com/getzep/zep README): *"Zep Community Edition is no longer supported. Its code has been moved to the `legacy/` folder."* PyPI corroborates precisely: **`zep-python` last released 2024-09-26** (dead), while **`zep-cloud` 3.28.0 ships 2026-08-11** with a `4.0.0a5` alpha (2026-08-26). **Zep is SaaS-only.** Under "self-hosted-friendly scores above SaaS-only," it does not score — it is **excluded outright**. Anything in the in-repo record naming Zep as a self-hostable memory layer (`docs/handoffs/2026-07-02-ai-council-architect/SUPPLEMENT.md:77` names Mem0/Zep/Letta as real systems in options guidance) is describing a product that has since changed shape.

**Letta (MemGPT) — self-hostable, and unaffordable.** The server `letta` 0.16.8 last released **2026-05-14** (3.5 months), with **69 unconditional direct dependencies** and a **251-package closure** (*measured*) — **7.2× this repo's entire lock, and the largest in the survey.** The thin `letta-client` (1.12.1, 2026-06-02) is fine but is a client *for a server you must run*. **Server-dependent + 251 packages: scores against it on both halves of the constraint.**

**Mem0 — actively maintained, and its evidence base is contested.** `mem0ai` 2.0.19, 2026-08-24; 188 releases; 35-package closure — by far the lightest of the three. But its headline "+26% over OpenAI on LOCOMO" is a **relative** LLM-as-judge delta, and the LOCOMO literature is in open dispute: Mem0 reported Zep at 58.44% after replication, Zep claimed 75.14% and argued misconfiguration ([getzep/zep-papers issue #5](https://github.com/getzep/zep-papers/issues/5) — *measured-but-contested*), and an independent audit reports **6.4% of the answer key wrong, the LLM judge accepting 63% of intentionally-wrong answers, and 56% of per-category comparisons statistically indistinguishable from noise** (*search-relayed, secondary — I could not open the audit at source*).

**That last item is the most decision-useful thing on this shelf, and it generalises past Mem0:** the agent-memory field's flagship benchmark **does not reliably measure what its title says**. Any adoption argument on this shelf resting on LOCOMO numbers rests on contested ground. Combined with the structural mismatch — all three are **conversational-turn memory** for chat agents, where this repo's memory is `JOURNAL.md` + append-only `LESSONS.md` + immutable handoff bundles, i.e. **already durable, already ordered, already human-authored** — the verdict is `absent` with no reopening trigger I can construct.

**Searched, for the absence declaration:** `sqlite-vec|chromadb|LanceDB|sentence-transformers|Mem0|Letta|MemGPT|Zep` repo-wide, case-insensitive. Hits are commentary only (two handoff supplements naming Mem0/Zep/Letta as examples in options guidance; one child-repo DEFER row on ChromaDB). **No organ, no dependency, no row.**

---

## §4 — SHELF 6: LOOP EVALUATION / OPTIMIZATION

### 4.0 Two locator corrections the brief needs back, before any verdict

**(a) `[#617]` — unlocatable, and more specifically it does not exist.** I searched `\[#617\]|#617` repo-wide: **zero matches** (the only `617` substring in the tree is inside a sha256 in `tasks/archive/491.md:38`). The `tasks/` ledger tops out at **`[#615]`** (`tasks/615-model-attribution-signature-trailer-on-every.md`); `BACKLOG.md` likewise ends at `[#615]`. **There is no `[#616]` either.** So `[#617]` is not a row I failed to find — it is **a row that has not been born**, and the brief's "adjacent to `[#617]`" is a forward reference to an id the ledger has not yet issued. Per the enum: **unlocatable**, with the stronger fact attached.

**(b) The promptfoo/DeepEval instruction is real, but SDA-1 is not where it lives.** I read `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` and grepped it for `promptfoo|deepeval|library-first|hand-roll|off-the-shelf`: **zero hits**. SDA-1 is a *seeded-defect provider-admission* benchmark design (16 (provider, role) pairs, §9 severity tally, §10 verdict); it never mentions an eval harness product. The instruction the brief is reaching for exists at **two** locators, and the shared phrase "seeded-defect corpus" is almost certainly the source of the conflation:

> `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md:84-90` — **PROPOSED ROW R3 — Rule-adherence eval harness (promptfoo + seeded-defect corpus)**. Done-when: *"`npx promptfoo eval` runs >=10 cases encoding non-negotiables from `~/.claude/rules/core-invariants.md` and exits non-zero below a declared threshold; a deliberately-weakened instruction set FAILS the run."* kill-candidates: *"overlaps the seeded-defect-corpus spec already gating [#491]/[#492] — propose FOLDING into that corpus rather than birthing a second one."*

> `docs/audits/2026-08-19-technical-n3-ratification-pack.md:308-312` — **§3.4 "Not born, and why"**: *"**R3** (promptfoo rule-adherence harness) — accepted in principle, **not born**, on the intake's own kill-candidates line… Filing a second eval corpus alongside it is the duplication ADR-111 outcome (a) exists to prevent."*

**That is the reconcile-first result for this shelf, and it changes the shape of every verdict below: promptfoo was evaluated, accepted in principle, and deliberately not born — not from doubt about the tool, but to avoid a second eval corpus.** The blocker is **corpus duplication**, not tool selection. Any recommendation that proposes standing up promptfoo *as a new thing* re-opens a decision that was made deliberately eleven days ago.

### 4.1 The SkillsBench finding — verified as far as this session's network permits, and then applied

**What I could verify:** two independent search passes return the same figures from what are presented as the arXiv abstracts. **SkillsBench** (arXiv **2602.12670**, Feb 2026): *"On SkillsBench, human-authored skills improve pass rates by **16.2 percentage points**, while LLM-authored skills provide **no measurable gain**."* **SkillAxe** (arXiv **2606.10546**, Jun 2026, *"Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement"*): four diagnostic dimensions — quality impact, trigger precision, instruction compliance with fault attribution, solution-path coverage — **fully unsupervised, no ground-truth labels, test suites, or environment rewards**; reported **+28% relative** over unimproved LLM skills, closing **47-67%** of the gap to human-authored.

**What I could NOT verify, stated plainly rather than smoothed:** **arxiv.org is egress-blocked from this container**, as are HuggingFace papers and Semantic Scholar. **I did not read either abstract at source.** The figures are consistent across two independent queries and the identifiers resolve to real-looking titles, but **this is search-relayed evidence, not primary.** I am accepting the brief's instruction to treat the finding as given; I am **not** representing it as primary-verified, and re-verifying both abstracts is the first item on my limits list.

**Applying it, which is the part the brief says a DSPy verdict cannot skip.** The consequence — *a prompt/skill distiller without an eval loop ships a useless library* — lands with unusual force here, because **this repo is a distiller factory**. It ships 8 repo commands, a skill roster, a plugin, a floor, and a deployed methodology corpus to child repos. If LLM-authored skills give **no measurable gain**, then **every organ this repo generates rather than hand-authors is unevidenced until an eval loop says otherwise.**

**And there is a second-order reading the brief did not ask for but which follows directly.** SkillAxe's mechanism is *"run the agent on the same task with and without the current skill, and diagnose the behavioral difference."* **That is an A/B ablation, and it is exactly the design of the `[#491]`/`[#492]` seeded-defect corpus and of SDA-1's own "with-skill vs without-skill" shape.** The repo's existing instrument is **structurally the same instrument** the published fix uses. It is not missing a technique; it is missing a *run*.

### 4.2 DSPy — **`absent`, and my verdict is: not the backbone, and here is what is**

**Maturity (measured, PyPI):** **3.3.1, uploaded 2026-08-21**; 108 releases; `requires-python >=3.10,<3.15`; pure-Python wheel. **Closure: 63 packages** — 1.8× the lock, below the 103-package rejection bar but well above `sqlite-vec`'s 1.

**GEPA, the optimizer that makes DSPy interesting for this shelf** (*measured, search-relayed*): "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning" (Agrawal et al., 2025), **ICLR 2026 oral**; reported **93% on MATH vs 67% unoptimized ChainOfThought**; **+12% over MIPROv2** on AIME 2025; **outperforms GRPO by up to 20% using 35× fewer rollouts**. It also ships **standalone** (`pip install gepa`, [gepa-ai/gepa](https://github.com/gepa-ai/gepa)) — you do not need DSPy to use GEPA. **Same primary-source caveat: arXiv blocked, figures search-relayed.**

**Why it is nonetheless the wrong backbone *here*, and this is where I disagree with the framing rather than restate it.**

DSPy optimizes **a metric over a labelled dataset**. Its whole loop is: signature → module → **metric** → trainset → compile. **This repo's distiller problem has no trainset and no scalar metric.** The thing being distilled is `CLAUDE.md` and the floor — an instruction surface whose success criterion is *"does the agent still obey the rule after compression?"*, which is **binary rule-adherence over a seeded-defect corpus**, not accuracy over QA pairs. The in-repo record already says this, and said it first: `docs/archive/2026-08-17-research-agent-instruction-layers-and-distillation-wf-50111a08.md:20` — *"Distillation techniques are measured mostly on QA/reasoning benchmarks, not on 'did the agent still obey the rule.' You must close that gap yourself with a small eval harness."*

**The order of operations is therefore fixed, and DSPy is not first.** You cannot run a metric-driven optimizer before you have a metric. The metric here **is** the R3 corpus. **Build the corpus, run it, and only then ask whether an optimizer is worth 63 packages** — at which point **GEPA standalone**, not DSPy-the-framework, is the thing to try, because the optimizer is the part with the evidence and the framework is the part with the closure.

**Negative results on DSPy in production, first-class:** *no production runtime, no observability surface, no inline guardrails; the optimizer runs offline in a notebook and then disappears, leaving a plain Python object production must manage; a steep learning curve driven by heavy meta-programming* ([Skylar Payne, "If DSPy is So Great, Why Isn't Anyone Using It?"](https://skylarbpayne.com/posts/dspy-engineering-patterns/); [FutureAGI, 2026](https://futureagi.com/blog/best-dspy-alternatives-2026/) — *practiced*, secondary). **Two of those four are irrelevant here** (Layer 2 has no production runtime to lack, and being Python-only is a *feature* in a `uv`-pinned repo). **The meta-programming learning curve is not irrelevant** — it lands on a single operator whose stated constraint is decision load, instrumented at `logs/OPERATOR-LOAD.csv` (`ARCHITECTURE.md` Ch6). A framework whose adoption cost is *"the first quarter is mostly internal teaching"* is expensive for a team of one.

**Cheapest experiment (Tier L — evaluate, do not try):** **do not install DSPy.** Take **five** `CLAUDE.md` invariants, write them as promptfoo assertions, run original-vs-a-deliberately-weakened instruction set, and check the weakened one **fails**. If that harness works, *then* ask whether GEPA-standalone beats hand-editing on the same corpus. Cost of the DSPy question until then: **zero packages.**

### 4.3 promptfoo — **`partial`, and it is the single highest-value item in this entire artifact**

**Maturity (measured, npm registry JSON, 2026-08-29):** **0.122.2, published 2026-08-28**; **421 versions** since 2023-05-03; releases roughly weekly through Aug 2026. ~21k GitHub stars as of mid-2026 (*search-relayed*). MIT.

**Installability — read this carefully, because it inverts the usual constraint analysis.** promptfoo is a **Node/npm** tool, run as `npx promptfoo eval`. **It therefore adds ZERO packages to `uv.lock`.** The pinned-`uv` constraint — the thing that kills `sentence-transformers` and Microsoft Agent Framework — **does not apply to it at all**, because it never enters the Python resolution graph. And **this repo already has Node**: `package.json` and `package-lock.json` are tracked at root (*measured*, `git ls-files`). The runtime is already present.

**Trap, and it is a real one I nearly walked into.** There **is** a PyPI package literally named `promptfoo` — version **0.1.4**, 5 releases, last uploaded 2026-04-06 (*measured*). **It is not the tool.** The real promptfoo is at 0.122.2 on npm with 421 versions. Anyone reaching for `uv add promptfoo` gets a near-empty package with a matching name. Worth recording where the fleet can see it.

**Self-hosted:** yes, fully — YAML config, CLI, deterministic assertions (`is-json`, `contains`, regex, `javascript`) plus model-graded ones, exit codes for CI, any OpenAI-compatible endpoint including local (*practiced*).

**Verdict `partial`, and the missing piece is named precisely.** The **decision** is already made — R3 accepted in principle (`docs/audits/2026-08-19-technical-n3-ratification-pack.md:311`) with a **done-when already written as an executable criterion** (`docs/intake/2026-08-17-...:85-87`), in exactly the ADR-108 §B ex-ante shape. What is missing is **the run**, and the recorded reason it has not happened is **corpus duplication with `[#491]`/`[#492]`**, not tool doubt.

**Cheapest experiment (Tier S, and it is genuinely small):**

```
npx promptfoo eval  # zero uv.lock packages, zero Python deps
```

over **10 cases folded into the existing `[#491]`/`[#492]` corpus** — not a new one, per the kill-candidates line — encoding non-negotiables from `~/.claude/rules/core-invariants.md`, with a deliberately-weakened instruction set that **must FAIL**. Keep iff the weakened set fails and the intact set passes; delete the config if it does not discriminate. **This is the only candidate in the survey whose adoption decision is already ratified, whose success criterion is already written, whose runtime is already installed, and whose package cost is zero.** If the architect acts on one line of this artifact, this is the line.

### 4.4 DeepEval — `absent`, and it loses to promptfoo on this repo's exact axis

**Maturity (measured, PyPI):** **4.2.0, 2026-08-24**; **519 releases** since 2023-08-15 — the most prolific release cadence in the survey. ~15k stars (*search-relayed*). Pure-Python wheel.

**The case for it is real:** **pytest-native**. This repo has a 2,400+ test suite (`pyproject.toml` mutmut comment) and `uv run --locked pytest -x --tb=short` is the canonical cadence, so an eval that *is* a pytest test would land inside existing machinery rather than beside it. That is a genuine architectural fit and I do not want to undersell it.

**The case against, on this repo's own scoring rules: 65 packages** (*measured*) — 1.9× the entire lock, for a capability promptfoo delivers at **zero**. And its 50+ research-backed metrics (G-Eval, faithfulness, answer relevancy, hallucination) are **RAG/agent-output quality metrics**. This repo's question is **rule adherence**, which is a deterministic assertion — `contains`, regex, exit code — and needs none of them.

**Verdict `absent`.** 65 packages of RAG-metric machinery to answer a binary compliance question that a YAML file already answers for free. **The reopening trigger is specific:** if the eval need ever becomes *generation quality* rather than *rule adherence* — judging whether a generated handoff bundle is *good*, not whether it *obeys* — DeepEval's pytest-native shape becomes the better fit and this verdict should be re-taken.

---

## §5 — CONSOLIDATED VERDICT TABLE

Ranked by **fit × value**, best first. Flat and fenced per `CLAUDE.md` §4 output-formatting (so it copies into browser chat without border glyphs). All package counts measured this session via `pip install --dry-run --report` on Linux/py3.11 — see §0 caveat. Repo baseline: **`uv.lock` = 35 packages**.

```
RANK 1 -- promptfoo                                              SHELF 6
  provides    : YAML-declarative rule-adherence eval; deterministic +
                model-graded assertions; CLI exit codes; red-teaming
  maturity    : npm 0.122.2, published 2026-08-28; 421 versions since
                2023-05-03; weekly cadence; MIT; ~21k stars
  win / uv    : ZERO uv.lock packages -- it is npm, not Python. Node
                already present (package.json tracked at repo root).
                TRAP: PyPI "promptfoo" 0.1.4 is a DIFFERENT package.
  hosting     : fully self-hosted, no account, no server
  verdict     : PARTIAL -- decided, not born
                organ  : docs/intake/2026-08-17-tech-agent-instruction-
                         layers-and-distillation.md:84 (PROPOSED ROW R3)
                         docs/audits/2026-08-19-technical-n3-
                         ratification-pack.md:311 ("not born")
                missing: THE RUN. Blocked on corpus duplication with
                         [#491]/[#492], not on tool doubt.
  experiment  : Tier S. `npx promptfoo eval`, 10 cases FOLDED into the
                [#491]/[#492] corpus, from ~/.claude/rules/core-
                invariants.md. Keep iff a deliberately-weakened
                instruction set FAILS and the intact set passes.

RANK 2 -- sqlite-vec  (+ model2vec as the embedder)               SHELF 5
  provides    : vector column inside the sqlite store the repo already
                runs; brute-force kNN, no ANN index, no server
  maturity    : 0.1.9, 2026-03-31 (stable line static 5 months; only
                alphas since -- 0.1.10a4, 2026-05-18). 69 releases.
                8.1k stars, 155 open issues. README: "pre-v1, so expect
                breaking changes". Mozilla Builders + Fly.io/Turso.
  win / uv    : sqlite_vec-0.1.9-py3-none-win_amd64.whl EXISTS --
                prebuilt, the rustworkx precedent met. CLOSURE = 1 pkg.
                Issue #284 ("cannot install via uv on Windows") is a
                `uv tool install` misuse, NOT a real blocker.
                UNRESOLVED: which CPython release enabled Windows
                loadable sqlite extensions (cpython#95656 closed, ver
                not stated). Verify on the operator's machine.
                Embedder: model2vec = 22 pkgs, NO torch.
  hosting     : in-process, self-hosted by construction
  verdict     : PARTIAL -- store already-have-it in kind
                organ  : ruling R-A, protocols/STANDING_RULINGS.md:3267
                         (sqlite3 answers reachability in 1-4 ms at
                         11,684 edges); telemetry WAL store,
                         ecosystem/conformance.md:26 [#529]
                missing: a vector column + an embedding producer
  measured    : this session, stock CPython 3.11 venv --
                5,000x384-d insert 0.08 s; kNN k=10 mean 3.43 ms /20.
                Repo needs ~22k vectors => ~15 ms. Brute force is
                CORRECT at this scale; ANN buys nothing.
  experiment  : Tier S. Embed 828 docs/audits titles + first 200 words
                with potion-retrieval-32M into one vec0 table; answer
                "which prior audit bears on this brief?" for 5 briefs
                whose right answer the operator already knows. Keep
                iff >=4/5 rank the known-right doc top-3.

RANK 3 -- lane resume-point convention  (NOT a framework)         SHELF 4
  provides    : the ONE thing LangGraph would genuinely add here --
                mid-lane resumability after an unattended death
  maturity    : n/a -- it is a file convention, not a dependency
  win / uv    : ZERO packages
  hosting     : n/a
  verdict     : ABSENT -- searched protocols/PLAYBOOK.md Ch8, the five
                per-lane requirements (:1878-1901), the lane lifecycle
                (:2046), the night phases (:2200); NO resume mechanism
                found. A lane that dies mid-step restarts from zero.
  experiment  : Tier S. Lane writes <worktree>/.lane-state.json after
                each numbered step (step index, last SHA, footprint);
                /lane-boot offers resume. Delete if two consecutive
                batches record zero lane deaths.

RANK 4 -- LangGraph  (the arc's live question)                    SHELF 4
  provides    : StateGraph orchestration + durable execution via a
                persisted checkpointer
  maturity    : 1.2.11, 2026-08-11; 276 releases since 2024-01-08;
                1.0 GA 2025-10-22; langchain 1.3.18 (2026-08-27) with
                514 releases (~1 per 2.5 days -- a moving target for a
                deliberately-pinned toolchain)
  win / uv    : 35 pkgs (38 with sqlite checkpointer) = the size of the
                ENTIRE current lock. Pure-python wheels; no Win hazard.
  hosting     : self-hosted OK -- SQLite checkpointer, LangSmith is
                NOT required. Fairer on this axis than most.
  verdict     : ABSENT, and correctly so -- excluded on the Layer-2
                invariant (CLAUDE.md §5 rule 4) and on dispatch
                visibility (PLAYBOOK:2416 / STANDING_RULINGS B7), NOT
                on installability. Lane plumbing is git topology
                (refs/stash lives in the COMMON git dir), which a
                graph runtime cannot checkpoint into.
  prior       : LOCATED. docs/audits/2026-04-24-council-28-29-
                consolidated-actions.md:117 -- "Skip ... Reopening
                trigger: team grows beyond solo, or AI Council proves
                insufficient". Re-affirmed 2026-08-23-technical-
                research-model-bus.md:243. NOTE: the prior scored
                DEBATE orchestration, not lane plumbing -- a different
                question, answered fresh in §1.
  experiment  : none. Run RANK 3 instead; it buys the same gap free.

RANK 5 -- DSPy (+ GEPA standalone)                                SHELF 6
  provides    : prompt-as-program with metric-driven optimization
  maturity    : 3.3.1, 2026-08-21; 108 releases. GEPA: ICLR 2026 oral;
                93% vs 67% on MATH; +12% over MIPROv2 on AIME 2025;
                beats GRPO by up to 20% at 35x fewer rollouts.
                [search-relayed -- arXiv EGRESS-BLOCKED this session]
  win / uv    : 63 pkgs (1.8x the lock). Pure-python wheel, Win fine.
                GEPA also ships standalone (`pip install gepa`).
  hosting     : self-hosted; optimizer runs offline
  verdict     : ABSENT -- searched dspy|DSPy repo-wide: ZERO hits.
                And WRONG ORDER, not wrong tool: DSPy optimizes a
                metric over a trainset; this repo's distiller problem
                is binary rule-adherence with NO metric yet. The
                metric IS the R3 corpus. Build that first.
  negative    : no production runtime/observability/guardrails; the
                optimizer runs in a notebook then disappears; steep
                meta-programming learning curve ("the first quarter is
                mostly internal teaching") -- expensive for one seat.
  experiment  : Tier L (evaluate, do not try). Cost until RANK 1
                lands: ZERO packages. Then test GEPA-STANDALONE, not
                the framework, against hand-editing on that corpus.

RANK 6 -- LanceDB                                                 SHELF 5
  provides    : embedded serverless vector DB, disk-based columnar
  maturity    : 0.37.1, 2026-08-10 -- freshest store on the shelf;
                100 releases since 2023-03-18; Rust
  win / uv    : lancedb-0.37.1-cp310-abi3-win_amd64.whl present.
                17 pkgs -- smallest real vector DB here, HALF of
                LangGraph's and a QUARTER of Chroma's.
  hosting     : embedded, self-hosted
  verdict     : ABSENT on scale, not on quality. Beats sqlite-vec only
                past RAM / real ANN need; the corpus is 31.2 MiB.
                If this repo ever outgrows brute force, LanceDB --
                NOT Chroma -- is the successor to test.
  experiment  : none now. Revisit only if a probe shows >1M vectors.

--- SCORED AGAINST, per the hard constraint (named, not caveated) ---

sentence-transformers   SHELF 5  ABSENT.  58 pkgs + torch. The cp312
   win_amd64 torch wheel alone is 122.1 MB. Against a repo that
   documents numpy MOVING GROUPS as a cost worth 3 sentences
   (pyproject.toml:55-59), this cannot enter `uv sync --locked`
   without a ruling. REPLACEMENT: model2vec (22 pkgs, no torch,
   ~94.7% of MiniLM at ~30 MB) or fastembed (28 pkgs, ONNX;
   onnxruntime cp312 win wheel = 14.0 MB, not 122).
   Maturity is EXCELLENT (6.0.0, 2026-08-18) -- weight is the kill.

ChromaDB                SHELF 5  ABSENT.  79 pkgs (2.3x the lock) for a
   feature sqlite-vec gives in 1, on a corpus too small to need an
   index. Win wheel fine (cp39-abi3-win_amd64), 1.5.9 2026-05-05.
   Rust rewrite brought breaking changes; server-shaped in prod.
   In-repo prior: a DEFER-field row, NOT to be executed --
   docs/handoffs/2026-07-17-corp-monorepo-executor-.../PROMPT_arc-b-
   execution.md:95.

DeepEval                SHELF 6  ABSENT.  65 pkgs (1.9x the lock) for a
   binary compliance question promptfoo answers at ZERO. Genuinely
   the better ARCHITECTURAL fit (pytest-native, and this repo lives
   in pytest) -- but its 50+ metrics are RAG/agent-output QUALITY
   metrics, not rule adherence. 4.2.0 2026-08-24, 519 releases.
   REOPEN IF: the need becomes generation quality, not rule
   adherence.

Microsoft Agent Frmwk   SHELF 4  ABSENT.  205 pkgs = 5.9x the lock, and
   TWICE the 103-package closure on which pydantic-ai was already
   REJECTED (2026-08-23-technical-research-model-bus.md:230).
   Actively shipping (1.16.0, 2026-08-28). Excluded on weight.

Letta / MemGPT          SHELF 5  ABSENT.  251 pkgs -- LARGEST in the
   survey, 7.2x the lock -- AND server-dependent. Fails BOTH halves
   of the constraint. Server 0.16.8 last shipped 2026-05-14; the
   thin letta-client 1.12.1 is a client for a server you must run.

Mem0                    SHELF 5  ABSENT.  Lightest of the three memory
   layers (35 pkgs, 2.0.19 2026-08-24, healthy). Excluded on
   EVIDENCE and on shape: the "+26%" is a relative LLM-judge delta
   on LOCOMO, a benchmark in open dispute (Zep 58.44% vs 75.14%,
   getzep/zep-papers#5); an independent audit reports 6.4% of the
   answer key WRONG and the judge accepting 63% of intentionally-
   wrong answers. And it is conversational-turn memory; this repo's
   memory is JOURNAL + append-only LESSONS + immutable bundles.

--- NEGATIVE RESULTS: dead, deprecated, or SaaS-captured ---

AutoGen                 SHELF 4  ABANDONWARE (verified two sources).
   autogen-agentchat / autogen-core: 0.7.5, LAST RELEASE 2025-09-30
   -- ELEVEN MONTHS. pyautogen: 2025-07-15 -- thirteen months.
   README verbatim: "AutoGen is now in maintenance mode. It will not
   receive new features or enhancements and is community managed
   going forward." Successor named: Microsoft Agent Framework.
   THIS FALSIFIES the in-repo record: docs/archive/2026-04-24-multi-
   agent-debate-patterns.md:116 still calls it a leading production
   framework with "best-in-class human-in-the-loop". That file is
   immutable + exempt-permanent, so carry the correction forward.

Zep (OSS)               SHELF 5  DEPRECATED -> SaaS-ONLY.
   README verbatim: "Zep Community Edition is no longer supported.
   Its code has been moved to the `legacy/` folder."
   zep-python LAST RELEASE 2024-09-26 (dead); zep-cloud 3.28.0
   2026-08-11 ships on. Under "self-hosted above SaaS-only" it does
   not score -- it is EXCLUDED. Any in-repo text naming Zep as a
   self-hostable memory layer describes a product that changed shape.

CrewAI                  SHELF 4  ABSENT.  134 pkgs (above the pydantic-
   ai rejection bar) AND publishes a dated dev build to PyPI EVERY
   DAY (1.15.17.dev20260825 ... 1.15.18.dev20260829). Alive, but a
   hostile version surface for a `--locked` discipline. Solves
   multi-agent team simulation; lanes here are file-disjoint and
   talk through git, not conversation.

promptfoo ON PyPI       SHELF 6  NAME TRAP, not a candidate.
   PyPI "promptfoo" = 0.1.4, 5 releases, last 2026-04-06. The real
   tool is npm promptfoo 0.122.2 with 421 versions. `uv add
   promptfoo` gets you a near-empty lookalike.

LOCOMO benchmark        SHELF 5  A BENCHMARK THAT DOES NOT MEASURE
   WHAT ITS TITLE SAYS -- the most decision-useful negative result
   here, and it generalises past Mem0 to the whole agent-memory
   shelf. Contested replication + a wrong answer key + a permissive
   judge + 56% of category comparisons indistinguishable from noise.
   Any adoption argument resting on LOCOMO rests on sand.
```

---

## §6 — MY OWN LIMITS

**Could not verify at source (network, not effort).** `arxiv.org`, `huggingface.co`, `api.semanticscholar.org`, `emergentmind.com`, `alexgarcia.xyz` and `octomind.dev` were all unreachable — the first five **egress-blocked by the proxy** (`CONNECT tunnel failed, response 403` / `EGRESS_BLOCKED`), the last a DNS failure. Consequently **every paper claim in §4 is search-relayed, not primary-verified**: SkillsBench (2602.12670) 16.2 pp, SkillAxe (2606.10546) +28% / 47-67% gap closure, and the GEPA figures. **To settle:** re-fetch those three abstracts from an unblocked host and confirm the numbers and the paper identifiers.

**Unlocatable, stated with the enum's precision.** `[#617]` — searched `\[#617\]|#617` repo-wide, zero matches; the `tasks/` ledger and `BACKLOG.md` both top out at `[#615]`, and `[#616]` does not exist either. It is not a row I missed; it is a row not yet born. **To settle:** the architect names what `[#617]` is intended to be, or issues it.

**A brief premise I could not confirm, and corrected instead.** SDA-1 does **not** contain the promptfoo/DeepEval instruction — grepped `promptfoo|deepeval|library-first|hand-roll|off-the-shelf` against `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md`, zero hits. The live locators are intake R3 (`docs/intake/2026-08-17-...:84`) and the N3 ratification pack (`docs/audits/2026-08-19-...:311`). The shared phrase "seeded-defect corpus" is the likely source of the conflation. **To settle:** nothing — the instruction is real and I have given you its address.

**The one fact that could change a top-3 verdict, and I could not measure it from here.** Whether `sqlite3.Connection.enable_load_extension` is available on **the operator's Windows CPython 3.12.10 under uv**. cpython#95656 is closed via PR #95662 but the page I could reach does not name the release. My probe proves the mechanism on **Linux/3.11**, which is not the target. **To settle — one line, on the operator's machine:** `uv run --locked python -c "import sqlite3; sqlite3.connect(':memory:').enable_load_extension(True); print('OK')"`. If that raises, RANK 2 changes shape entirely and `lancedb` (17 pkgs, real Windows wheel, no extension loading) becomes the fallback rather than a "revisit later".

**Measured on the wrong platform.** All 15 closure counts are Linux/py3.11 resolutions. Windows/py3.12 numbers will differ at the margins. The **ranking** is robust (1 vs 17 vs 35 vs 63 vs 205 vs 251 is not a rounding question); the exact integers are not. **To settle:** `uv pip compile --dry-run` on the operator's host for the two candidates that survive.

**Not attempted, and named rather than left to be discovered.** I did not measure commit cadence or open-issue *shape* (stale-vs-active) for any candidate — `api.github.com` is gated to this session's single allowed repo, so I have release cadence and issue *counts* but not issue *health*. Where I report a star count or an open-issue count it came from GitHub HTML, and where I report nothing I had nothing.

---

## §7 — WHERE I WENT DEEPER THAN A SURVEY WOULD

The architect asked how to tell this artifact from AUT-R3's appendix on the same three shelves. Six places, and each is a thing an appendix structurally cannot afford:

**1. I ran the code.** The `sqlite-vec` verdict rests on a probe I executed in this container — 0.08 s to insert 5,000 × 384-d vectors, **3.43 ms** mean kNN — not on a claim about brute-force performance. That measurement is what converts sqlite-vec's headline weakness (*no ANN index*) into a non-issue **at this repo's specific size**, and no survey that has not multiplied the corpus out to ~22k vectors can make that call. I also ran `file_purpose_graph.py stats` under a scratch venv to get the real graph — **1,666 nodes / 10,745 edges, 9,467 of them one kind** — because the FPG's coverage against 2,701 tracked files is the whole Shelf-5 need statement, and it is not written down anywhere.

**2. I counted the closures, in the repo's own idiom.** Fifteen `pip --dry-run --report` resolutions against the measured 35-package lock. That is what makes the constraint operate *per candidate* rather than as a caveat: **205** for Microsoft Agent Framework and **251** for Letta are not "heavyweight", they are 5.9× and 7.2× the lock and **twice** the closure on which `pydantic-ai` was already rejected in this repo's own record. And it is what surfaced the finding I did not expect — **promptfoo's cost under the pinned-`uv` constraint is exactly zero, because it is npm and the repo already tracks `package.json`.**

**3. I chased the scary issue and found it was nothing.** [sqlite-vec#284, "cannot be installed via uv on Windows"](https://github.com/asg017/sqlite-vec/issues/284), open, unresolved, and **a `uv tool install` misuse**. A survey grepping for installability risk hits that title and marks sqlite-vec down. The real risk is somewhere else entirely — `enable_load_extension` on the Windows CPython build — and I would have missed it if I had stopped at the first alarming result.

**4. I falsified two things the repo currently believes.** AutoGen's Python packages have been silent for **eleven months** and its README says *"maintenance mode"* — while `docs/archive/2026-04-24-multi-agent-debate-patterns.md:116` still calls it a leading production framework, and that file is immutable and `exempt-permanent`, so the correction has to travel forward by hand. And **Zep's open-source edition no longer exists** — `zep-python` dead since 2024-09-26, CE moved to `legacy/` — while in-repo options guidance still names Zep as a real self-hostable system.

**5. I did the reconcile work in both directions, including against the brief.** The LangChain prior verdict is **located** (`2026-04-24-council-28-29-consolidated-actions.md:117`) *with its reopening trigger*, and I then showed it **does not reach the question actually asked** — it scored debate orchestration, not lane plumbing — so the §1 verdict is taken fresh rather than inherited. And I established that `[#617]` **has not been born** (ledger stops at 615) and that the promptfoo instruction **is not in SDA-1** but at two other addresses I supply. An appendix pass would either have accepted both premises or reported them missing; the useful move was to find where each one actually lives.

**6. I found the recommendation nobody was looking for, and it is the cheapest thing here.** The highest-value item in the survey is not a new adoption at all — it is that **promptfoo was already accepted in principle, already has an executable ex-ante done-when, already has its runtime installed, costs zero packages, and was deliberately not born for a reason (corpus duplication with `[#491]`/`[#492]`) that a *fold* dissolves and a *new corpus* would violate.** That is not a survey finding; it is a reconciliation finding, and it only appears if you read the ratification pack's §3.4 "Not born, and why" — which exists precisely so that omissions stay visible, and which worked.

**Where to trust AUT-R3 over me:** on any candidate I marked thin — I have real depth on sqlite-vec, promptfoo, LangGraph, AutoGen, Zep and the closure economics, and comparatively little on ChromaDB's and LanceDB's *operational* behaviour under load, on Mem0's actual API ergonomics, and on anything requiring the arXiv sources this session could not reach.

**Sources:** [LangGraph 1.0 GA changelog](https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available) · [LangChain durable-execution docs](https://docs.langchain.com/oss/python/langgraph/durable-execution) · [microsoft/autogen README](https://github.com/microsoft/autogen) · [getzep/zep README](https://github.com/getzep/zep) · [asg017/sqlite-vec](https://github.com/asg017/sqlite-vec) · [sqlite-vec issue #284](https://github.com/asg017/sqlite-vec/issues/284) · [cpython issue #95656](https://github.com/python/cpython/issues/95656) · [MinishLab/model2vec results](https://github.com/MinishLab/model2vec/blob/main/results/README.md) · [getzep/zep-papers issue #5](https://github.com/getzep/zep-papers/issues/5) · [gepa-ai/gepa](https://github.com/gepa-ai/gepa) · [DSPy GEPA docs](https://dspy.ai/api/optimizers/GEPA/overview/) · [Skylar Payne on DSPy](https://skylarbpayne.com/posts/dspy-engineering-patterns/) · [TianPan, orchestration framework trap](https://tianpan.co/blog/2026-04-19-orchestration-framework-trap-langchain-production) · [Ravoid, the LangChain exit](https://ravoid.com/blog/langchain-exit-raw-sdk-migration-2026/) · [Chroma migration docs](https://docs.trychroma.com/docs/overview/migration) · [promptfoo vs DeepEval, QASkills 2026](https://qaskills.sh/blog/promptfoo-vs-deepeval-2026) · [arXiv 2602.12670 SkillsBench](https://arxiv.org/abs/2602.12670) *(blocked — search-relayed)* · [arXiv 2606.10546 SkillAxe](https://arxiv.org/abs/2606.10546) *(blocked — search-relayed)* · PyPI JSON API and npm registry JSON, queried 2026-08-29 (primary, measured).