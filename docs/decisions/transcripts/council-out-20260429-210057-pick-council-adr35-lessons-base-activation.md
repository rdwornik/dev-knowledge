# AI Council Debate: Lessons base activation — retrieval, promotion, querying mechanism for LESSONS.m

**Date:** 2026-04-29 21:00:57
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20, gpt-5.4
**Synthesizer:** claude-sonnet (non-participant)
**Rounds:** 2
**Duration:** 430.9s
**Panel Mode:** full (5-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council_adr35_lessons_base_activation.md
**Cost:** ~$0.7550 (143,293 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position

Build **retrieval first** as the highest-leverage activation layer: a SessionStart hook that surfaces scope-tagged + evergreen lessons from LESSONS.md, backed by a derived `lessons-index.json`. Defer querying CLI and formalized promotion until retrieval proves the format works — promotion already happens implicitly via corrections.jsonl, so don't double-build it.

## Alternatives Considered

1. **Full activation now (retrieval + promotion + querying simultaneously)** — Rejected: three coupled mechanisms built without usage data produces over-engineered scaffolding. Rob's own diagnosis ("nic z tego nie wynika") is about *outcomes*, not missing features. Build the one layer that changes outcomes, observe, then extend.

2. **Restructure LESSONS.md into per-topic files or SQLite** — Rejected: violates Rob's stated preference for human-readable canonical, breaks the append-only invariant from ADR-29, and creates migration cost for 70+ entries before we know the access pattern. Derived index gives 90% of the benefit at 10% of the risk.

## Decision Criteria

1. **2am test** — when on-call (or Rob at low-energy moment) hits a known-mistake situation, does the system surface the prior lesson without manual action?
2. **Cognitive load** — number of new mental models / commands / files Rob must remember. Hard ceiling: ≤1 new interface.
3. **Reversibility** — can we abandon a layer in 3 months without data loss or migration pain?
4. **Leverage per unit of build effort** — retrieval at session start affects every session; querying CLI affects only deliberate lookup moments.
5. **Don't duplicate existing infrastructure** — corrections.jsonl + Stop hook + /evolve already form a promotion pipeline. LESSONS.md activation must not fork it.

## Assumptions

1. SessionStart hook context budget can absorb ~2-5KB of filtered lessons without degrading other priming (if false: must compress harder or move to on-demand tool).
2. Scope tags in existing 70+ entries are consistent enough to filter on (if false: need a one-time backfill pass before retrieval works).
3. Rob queries "what lessons about X" <2x/week currently (if false: querying becomes higher priority than retrieval).
4. The implicit promotion pipeline (correction → 2x repeat → learned-rules.md) is actually working. If /evolve reveals it isn't, promotion priority rises.

## Recommendation

**Now (Phase 1 — Retrieval, ~1 session):**
- Generate `lessons-index.json` from LESSONS.md via a parser script (read-only, idempotent, regenerable). Fields: date, scope, category, action, evergreen-flag, tags.
- Add `evergreen: true` flag to ~10-15 highest-value lessons manually (Rob's call which ones).
- SessionStart hook: load lessons matching `scope:current OR scope:hybrid OR evergreen:true`, capped at 15 entries, recency-weighted.
- Cross-repo discovery: **walk-up from cwd to find `.dev-knowledge/`**, fallback to `$DEV_KNOWLEDGE_PATH`. No symlinks (maintenance trap), no hardcoding per-repo (drift trap).
- Single ADR-35 covering activation strategy, storage decision, retrieval mechanism, connection model. ~130 lines.

**Not now:**
- No SQLite/YAML migration. LESSONS.md stays canonical markdown.
- No vector/embedding retrieval. Scope-tag + evergreen flag is sufficient at 70 entries; revisit at ~300.
- No new `lessons query` CLI. `grep` + the index file are enough until proven otherwise.
- No new auto-promotion from LESSONS.md → ~/.claude/rules. The path `correction → corrections.jsonl → /evolve → learned-rules.md` already exists; LESSONS.md is the *narrative companion*, not a parallel pipeline.

**Defer (decision triggers below):**
- Phase 2 (querying CLI / MCP tool): build when Rob notices himself grepping LESSONS.md ≥3x/week.
- Phase 3 (formal LESSONS→rules promotion): build when /evolve reveals lessons that weren't captured as corrections (i.e., the implicit pipeline has a gap).

## Connection Model (Q6)

**Asymmetric, mostly one-directional, formalized:**

```
runtime events → corrections.jsonl → [Stop hook: 2x rule] → learned-rules.md
                       ↓                                          ↓
                       └──── /evolve Friday ──────────────────────┤
                                     ↓                            ↓
                              LESSONS.md (narrative) ←────────────┘
                                     ↓
                              lessons-index.json (derived)
                                     ↓
                              SessionStart hook (retrieval)
```

- **~/.claude/ is source of truth for *enforcement*** (executable rules, verify: lines).
- **LESSONS.md is source of truth for *narrative + rationale*** (why a rule exists, context, what was tried).
- Promotion flows runtime→narrative during /evolve (manual write to LESSONS.md) and narrative→runtime only when a lesson lacks a corresponding rule (manual, rare).
- This is the current implicit model — ADR-35 just names it.

## Universalization Pattern (Q7, per ADR-33/34)

- Discovery: **upward walk from cwd for `.dev-knowledge/` marker**, then `$DEV_KNOWLEDGE_PATH`, then fail loud.
- Each child repo's CLAUDE.md/AGENTS.md gets a single line: `Lessons base: resolved via .dev-knowledge discovery (see ADR-35)`.
- No per-repo configuration. No symlinks. Single resolution function lives in `.dev-knowledge/bin/resolve-knowledge-root.sh` and is sourced by hooks.

## Rationale

- **Retrieval changes every session; querying changes maybe one session/week.** ~20-50x leverage difference for similar build cost.
- **Index-on-top preserves the append-only invariant** from ADR-29. Regenerating `lessons-index.json` from LESSONS.md is idempotent — if it corrupts, delete and rebuild. Zero migration risk for 70+ entries.
- **Scope-tag filtering is good enough at N=70.** Embeddings only justify their operational complexity (model deps, cache, drift) past several hundred entries. Premature RAG is the new premature optimization.
- **Walk-up discovery beats env vars and symlinks** because it works regardless of how the session was launched (terminal, IDE, hook). Symlinks break on clone; env vars break when forgotten.
- **The "no LESSONS→rules auto-promotion" decision is the important one.** Rob already has a working promotion pipeline through corrections.jsonl. Building a second pipeline from LESSONS.md would create two sources of truth and a sync problem at 2am.

## Trade-offs

- **Give up:** semantic retrieval quality (scope-tag misses lessons that *are* relevant but tagged differently). Mitigated by `evergreen` flag for cross-cutting wisdom.
- **Give up:** queryability for Rob in the short term — he still greps. Acceptable cost given <2x/week assumption.
- **Give up:** symmetry. The bidirectional model is conceptually cleaner; the asymmetric one is operationally honest.
- **Cost:** ~15 min one-time backfill to add `evergreen` flags + audit scope tag consistency on existing 70 entries.

## Risks

- **Scope tags inconsistent across 70 entries** (likelihood: medium; impact: medium) — retrieval surfaces noise or misses. Mitigation: one-time normalization pass before hook ships; log retrieval hit-rate for first 2 weeks.
- **SessionStart context budget pressure** (likelihood: low; impact: medium) — lessons crowd out other priming. Mitigation: hard cap 15 entries / ~3KB; make budget configurable.
- **Index drift from LESSONS.md** (likelihood: medium; impact: low) — index regenerated on every session start or via pre-commit hook. Cheap to fix.
- **Rob ignores surfaced lessons** (likelihood: medium; impact: high — defeats the whole exercise). Mitigation: after 4 weeks, audit whether retrieved lessons influenced session decisions. If not, the problem isn't activation — it's lesson quality, and we should prune aggressively before adding more machinery.

## Signals to Revisit

- LESSONS.md crosses ~250 entries → reconsider embedding-based retrieval.
- Rob greps LESSONS.md ≥3x/week (self-reported or shell history) → build querying CLI (Phase 2).
- /evolve session reveals lessons in LESSONS.md that never became rules despite being applicable → build formal promotion (Phase 3).
- Retrieved-lesson-influence audit at week 4 shows <20% relevance → problem is lesson quality/tagging, not mechanism; pause Phase 2/3.
- Cross-repo session-start hook fails discovery >5% of sessions → revisit walk-up strategy.

## ADR-35 Skeleton (~130 lines)

1. **Context** (15 lines) — Rob's "nic z tego nie wynika", three gaps, two-layer distinction.
2. **Decision** (25 lines) — Retrieval-first; LESSONS.md canonical; derived index; asymmetric connection to ~/.claude/.
3. **Connection Model** (15 lines) — diagram above + one-paragraph explanation of why asymmetric.
4. **Retrieval Mechanism** (20 lines) — scope-tag + evergreen + recency; 15-entry cap; walk-up discovery.
5. **Storage Format** (10 lines) — LESSONS.md unchanged; lessons-index.json derived & regenerable.
6. **Promotion** (10 lines) — explicitly *not* built; defer to existing corrections→/evolve pipeline.
7. **Querying** (5 lines) — explicitly deferred; grep + index file sufficient for now.
8. **Cross-repo (Universalization)** (10 lines) — walk-up + $DEV_KNOWLEDGE_PATH fallback.
9. **Phasing & Revisit Triggers** (15 lines) — Phase 1 now, Phase 2/3 trigger conditions.
10. **Open Questions for Rob** (5 lines, see below).

## Flagged for Rob's Decision

1. **Which ~10-15 lessons get `evergreen: true`?** Cannot be automated; this is taste.
2. **15-entry retrieval cap acceptable, or tighter?** Depends on what else SessionStart loads.
3. **Single ADR-35 (recommended) vs. split with ADR-36 for tooling?** Recommend single since Phase 2/3 are deferred — splitting now creates an empty ADR.
4. **Confirm: no LESSONS→rules auto-promotion.** This is the most consequential call; if Rob believes the corrections.jsonl pipeline has gaps, Phase 3 moves up.

*Latency: 67.08s | Tokens: 7400*

### Gemini (gemini-3.1-pro-preview)

## Position
Implement a decoupled, read-optimized retrieval mechanism driven by a secure environment variable (`$DEV_KNOWLEDGE_PATH`) and scope tags, maintaining a strict human-in-the-loop promotion boundary from the `LESSONS.md` narrative archive to the `~/.claude/` executable runtime.

## Alternatives Considered
- **Vector Embeddings / RAG for Retrieval & Querying:** Rejected. Introducing external dependencies, embedding models, or local vector DBs for ~70 text entries creates unnecessary supply chain risk, expands the attack surface via new local services, and introduces non-deterministic retrieval. 
- **Auto-Promotion of Lessons to Executable Rules:** Rejected. Automatically converting narrative text into active system prompt rules (`verify:`) without a strict human-controlled gate creates a severe prompt injection/corruption risk. A bad lesson could permanently poison agent behavior across the entire machine.

## Decision Criteria
- **Blast Radius & Context Integrity:** Preventing context window overload or prompt poisoning during session start.
- **Supply Chain & Dependency Minimization:** Eliminating the need for third-party databases, parsers, or complex MCP tools.
- **Architectural Decoupling:** Ensuring the narrative methodology archive cannot spontaneously mutate the system's executable runtime.
- **Frictionless Cross-Repo Execution:** Enabling secure reference to `.dev-knowledge` from any monorepo without path traversal vulnerabilities.

## Assumptions
- `DEV_KNOWLEDGE_PATH` can be reliably set in the host environment (e.g., `~/.zshrc` or `~/.bashrc`) and passed to Claude sessions.
- The user adheres strictly to the ADR-29 format (`### YYYY-MM-DD | source | lesson | category | scope: X | action`), making it securely parsable via standard POSIX tools (`awk`/`grep`).
- The volume of `LESSONS.md` entries will remain in the hundreds, not tens of thousands, meaning sequential file scanning has negligible compute/time overhead.

## Recommendation

**What to do now (Phase 1: Retrieval & Architecture):**
- **Draft ADR-35 (Single ADR):** Create one comprehensive ADR covering Activation & Connection. Skeleton: Context (Dormant lessons), Decision (Scoped retrieval via `awk`, decoupled runtime), Architecture (Env-var routing, one-way promotion), and Security (Preventing context poisoning). Estimated length: ~120 lines.
- **Build Connection Model (LESSONS.md ↔ ~/.claude/):** Formalize a unidirectional flow with gates. `~/.claude/memory/corrections.jsonl` -> (Threshold Trigger) -> Logged to `LESSONS.md` (Archive). Then `LESSONS.md` -> (Manual Friday `/evolve` Review) -> Promoted to `~/.claude/rules/` (Executable). They remain isolated layers.
- **Establish Universalization Pattern:** Rely entirely on an injected environment variable `$DEV_KNOWLEDGE_PATH`. At SessionStart, a lightweight bash hook reads this variable, extracts lessons matching the current repository's explicitly declared `scope`, and injects only those.
- **Flagged Ambiguity for Rob (Must Decide Before Code Execution):** Determine the exact maximum token count or lesson limit (e.g., "Top 5 most recent per scope") that SessionStart is allowed to inject, to guarantee prompt invariants are not diluted.

**What not to do now:**
- Do not restructure `LESSONS.md` into multiple fragmented files or a JSON database. Keep the human-readable canonical single file.
- Do not build an MCP tool for querying. 
- Do not use relative path traversal (`../../.dev-knowledge`) or symlinks in child repos. These are high-risk patterns for sandbox escapes and accidental commits.

**What to defer until later (Phase 2 & 3):**
- **Phase 2 (Promotion Tools):** Building automated CLI scripts to surface "frequently mentioned" lessons during the Friday `/evolve` session.
- **Phase 3 (Querying Tools):** Building a dedicated `lessons query "topic"` CLI. For now, standard `grep` is the lowest-friction, zero-dependency solution.

## Rationale
- **Isolation of Executable Context:** Treating `LESSONS.md` as an untrusted or semi-trusted archive and `~/.claude/rules` as an active executable runtime minimizes the blast radius. If `LESSONS.md` is bloated or corrupted, core AI agent behavior remains protected.
- **Attack Surface Reduction:** Resolving `.dev-knowledge` via `$DEV_KNOWLEDGE_PATH` completely eliminates directory traversal vulnerabilities ("walking up the tree") which a compromised agent could abuse to read sensitive host files.
- **Deterministic Context Loading:** Scope-based regex extraction (e.g., `awk '/scope: dev/' LESSONS.md`) is 100% deterministic, mathematically auditable, and requires zero extra package installations, maximizing supply chain integrity.
- **Phased Implementation Controls Scope:** By tackling retrieval first, you gain immediate ROI on task context without committing to complex and fragile promotion/querying engineering upfront.

## Trade-offs
- **Semantic Search Capability:** You give up the ability to query by "vibe" or semantic similarity. Strict keyword/scope matching is rigid and depends heavily on accurate manual tagging during lesson creation.
- **Automation Convenience:** You give up the convenience of "zero-touch" rule creation by enforcing manual review on Fridays, trading development speed for system stability and security.

## Risks
- **Risk:** Format drift in `LESSONS.md` breaks the `awk`/`grep` retrieval silently, leading to empty context injection.
  - *Mitigation:* Implement a lightweight pre-commit hook in the `.dev-knowledge` repo that validates new lines in `LESSONS.md` against the strict ADR-29 regex pattern. (High impact, low likelihood).
- **Risk:** Unset `$DEV_KNOWLEDGE_PATH` in a new shell or repo leads to fallback failure.
  - *Mitigation:* The SessionStart hook must explicitly check for the variable and output a visible warning ("Lessons activation skipped: DEV_KNOWLEDGE_PATH not set") rather than failing silently or assuming a default path.

## Signals to Revisit
- The raw file size of `LESSONS.md` surpasses ~1,000 entries, resulting in noticeable context bloat even when filtered by scope, necessitating a move to SQLite or chronological sharding.
- The human operator skips the `/evolve` Friday review for three consecutive weeks, indicating the manual promotion gate is too high-friction and requires frequency-based automation for critical rules.

*Latency: 34.17s | Tokens: 5849*

### Deepseek (deepseek-v4-pro)

## Position
Adopt a hybrid storage model for LESSONS.md: it remains the canonical human-readable narrative; an auto-generated `lessons-index.json` provides structured retrieval and querying. Phase implementation with retrieval first, using scope-tag filtering at session start. Formalize a bidirectional connection between LESSONS.md and the `~/.claude/` runtime infrastructure. Split the ADR: ADR-35 covers the activation architecture, storage, retrieval mechanism, cross-repo discovery, and the connection model; ADR-36 will cover promotion tooling and query CLI.

## Alternatives Considered
- **RAG / vector embedding retrieval**: rejected because it introduces deployment complexity, inference latency, and requires an embedding model and vector store for 70+ entries. Scope tags plus a small evergreen subset provide enough signal with near-zero overhead.
- **Splitting LESSONS.md into per-topic files**: rejected because it fragments the single source of truth, adds friction for Rob to decide where to write, and complicates cross-cutting lessons (scope: hybrid). ADHD-optimized means a single scannable file.

## Decision Criteria
1. **Immediate utility**: does it surface relevant lessons at session start to prevent repeated mistakes?
2. **Friction for Rob**: does the workflow stay low-friction, no extra steps to write or query?
3. **Implementation complexity**: can it be built and maintained with a shell script and a JSON index, no new services?
4. **Leverage**: does it close the gap between the 70+ entries in LESSONS.md and actual developer behavior?
5. **Integrity**: does it keep the runtime enforcement (`~/.claude/rules`) as the hard safety net while making the narrative archive actionable?

## Assumptions
1. `.dev-knowledge` contains a single `LESSONS.md` with entries following ADR-29 format consistently, and scope tags are maintained over time.
2. `DEV_KNOWLEDGE_PATH` environment variable can be set once in the shell config; all repos will use it to locate LESSONS.md without per-repo hardcoding.
3. Claude Code `SessionStart` hooks can execute a script that reads a file, filters entries, and injects them into the system prompt or hook context.
4. The current volume (70+ lessons) stays below the threshold where full-text parsing becomes a performance problem (unlikely before 10k entries).

## Recommendation
### What to do now (ADR-35 scope)
- **Storage**: Keep a single `LESSONS.md`. Generate `lessons-index.json` via a script (`gen-lessons-index`) that parses each entry into `{date, source, lesson, category, scope, tags, evergreen}`. Run it manually or as a pre-commit hook.
- **Scope-aware retrieval**: Create a `session-start` hook script that:
  1. Resolves `.dev-knowledge` path via `$DEV_KNOWLEDGE_PATH` (fallback: walk up from `cwd`).
  2. Reads `lessons-index.json`.
  3. Determines the active context scope from a file like `active-context-tags` in the current repo (or `CLAUDE.md` metadata), e.g., `corp-monorepo, git`.
  4. Filters lessons where `scope` matches any active tag OR `evergreen: true`.
  5. Includes always lessons with `scope: hybrid` and any manually flagged `evergreen`.
  6. Prints a summary of the most relevant lessons (limit to N entries sorted by recency, e.g., 10) into the session context.
- **Evergreen flag**: Add an optional `action: evergreen` line in LESSONS.md entries to mark critical lessons that bypass scope/recency filters.
- **Connection model formalization**: Document the bidirectional pipeline:
  - `~/.claude/memory/corrections.jsonl` auto-promotes to `~/.claude/rules` after 2 repetitions (already active).
  - During the `/evolve Friday` review, Rob may:
    - Promote a LESSONS.md lesson to a `~/.claude/rules` entry (manual).
    - Convert a notable correction into a new LESSONS.md entry (manual).
  - No automatic feed from corrections → LESSONS.md; the review is the gate.
- **Cross-repo discovery**: Use `DEV_KNOWLEDGE_PATH` as primary; session hook falls back to walking upward; add a line in each repo’s `CLAUDE.md` referencing this variable.

### What not to do now
- Do not split LESSONS.md into multiple files or migrate to a database.
- Do not implement RAG, vector search, or an MCP tool.
- Do not auto-populate LESSONS.md from corrections without human review (risks noise).
- Do not build a `lessons query` CLI; that’s deferred.

### What to defer until later (ADR-36)
- A `lessons` CLI that searches by keyword or tag using the index (e.g., `lessons query "git push --force"`).
- Automated promotion checklist tooling (e.g., marking lessons as “candidate for promotion” with a decision date).
- Integration with MCP for Claude web interface sessions.

## Rationale
- **Retrieval is the highest-leverage activation**: The primary complaint is “nothing comes of it” – making lessons visible at session start directly closes that gap. Even a 50% hit rate on surfacing a relevant past mistake saves rework.
- **Scope-tag filtering reduces noise cost**: Without filtering, dumping all 70+ lessons into every session start would train Claude to ignore them. A 10-lesson filtered list has far better attention economics.
- **Derived index enables future tooling without sacrificing human readability**: JSON is trivially queryable by jq and can power a future CLI; regenerating it is a single command. The canonical LESSONS.md stays a comfortable markdown record.
- **Explicit bidirectional connection prevents drift**: Formalizing that corrections can become lessons (and vice versa) ensures the two layers reinforce each other rather than diverge. The Friday review already exists; adding explicit checkboxes costs near zero additional time.
- **Cross-repo discovery via env var is simple and failsafe**: One environment variable set once versus symlinks or per-repo config minimizes maintenance and works across all current and future repos.

## Trade-offs
- **Giving up fully automated promotion**: Less lessons become executable rules without Rob’s manual review. This is acceptable because existing auto-promotion from corrections.jsonl already catches repeated runtime mistakes; LESSONS.md promotion addresses strategic patterns that benefit from human judgment.
- **No semantic search**: A simple scope filter won’t surface lessons where the topic isn’t covered by existing scope tags or where the connection is conceptual (e.g., “deployment lesson” when working on CI). Mitigation: add broader tags over time and rely on evergreen flagging for critical cross-cutting lessons.
- **Index maintenance dependency**: If the generation script breaks or someone forgets to run it, retrieval may use stale data. Mitigation: a validity check in the session hook that warns if index is older than LESSONS.md.

## Risks
- **Scope tag rot**: If scope tags aren’t updated, relevant lessons won’t surface. Likelihood: medium. Mitigation: during weekly review, include a quick scan for mis-scoped lessons; add a validation script that detects lessons with no recognized scope tag.
- **Hook execution failure**: If `DEV_KNOWLEDGE_PATH` is unset or the index is missing, session start might break or silently skip retrieval. Likelihood: low after setup. Mitigation: hook script must fail gracefully and fall back to reading only the last N lessons from LESSONS.md, outputting a warning.
- **Over-indexing cognitive load**: Too many “evergreen” lessons could defeat filtering. Likelihood: low (lessons are added slowly). Mitigation: cap total injected lessons to 15; always show a count of omitted ones so Rob can adjust.
- **Corrections → lessons flood**: During review, if Rob adds too many correction-derived lessons, LESSONS.md could bloat. Likelihood: low. Mitigation: keep the bar high for a lesson to be more than a one-time correction; a lesson must represent a pattern.

## Signals to Revisit
- **Retrieval proves insufficient**: If the filtered lessons at session start still lead to repeated mistakes (tracked via corrections.jsonl occurrences within 30 days of seeing a related lesson), consider adding lightweight semantic similarity (e.g., TF-IDF on index) or vector search.
- **LESSONS.md exceeds 300 entries**: At that scale, a full parse per session might become noticeably slow; revisit index design (maybe pre-filter by scope at index generation time) or split into sections internally while keeping a single file.
- **Multiple repos without `DEV_KNOWLEDGE_PATH`**: If the walk-up fallback fails too often, consider standardizing a global config file (like `~/.claude/global-context`) that points to `.dev-knowledge`.
- **Query frequency spikes**: If Rob starts asking “lessons about X” multiple times a week, accelerate ADR-36 to provide the query CLI earlier.

*Latency: 133.64s | Tokens: 6197*

### Openai (gpt-5.4)

## Position
Adopt a hybrid activation model now: keep `LESSONS.md` as the human-readable canonical archive, add a derived machine index plus lightweight CLI, and implement session-start retrieval based on scope/tags/evergreen—not embeddings. Formalize promotion as bidirectional but asymmetrical: `~/.claude/` remains the active enforcement layer, while `.dev-knowledge/LESSONS.md` remains the narrative memory and promotion source.

## Alternatives Considered
1. **Full semantic/RAG activation with embeddings as the primary retrieval/query path**  
   Rejected because it is operationally heavier than the problem warrants for a 70-entry archive, introduces model/index maintenance, and is hard to debug when retrieval misses. A small team can ship tagged/indexed retrieval in 1-2 sessions; a good local RAG setup is likely 3-5x the implementation and maintenance cost.

2. **Do nothing structurally; keep a single append-only `LESSONS.md` and rely on grep/manual review**  
   Rejected because it does not solve the stated problem: write-heavy, read-light knowledge. Without retrieval at session start and a query interface, the archive remains inert regardless of how good the content is.

## Decision Criteria
1. **Can a small team build and operate this quickly** — likely 1-3 focused sessions, no fragile infrastructure.
2. **Improves activation at the moment of work** — relevant lessons must surface automatically at session start.
3. **Preserves human-readable canonical knowledge** — Rob prefers narrative Markdown as source material.
4. **Connects cleanly to existing runtime infrastructure** — must integrate with `corrections.jsonl`, `learned-rules.md`, and promotion flows already in `~/.claude/`.
5. **Works cross-repo with low friction** — must function from `corp-monorepo`, `ai-council`, and other repos without per-repo manual hacks multiplying over time.

## Assumptions
1. Existing lesson entries are parseable enough from the ADR-29 header format to build a derived index with modest cleanup.
2. SessionStart hooks can call a local script/CLI and inject a compact summary into startup context.
3. Scope values are limited enough (`dev`, `llm`, `hybrid`, etc.) that rule-based filtering will be useful immediately.
4. Rob is willing to add minimal metadata going forward, specifically topic tags and an `evergreen`/`severity` marker if needed.

## Recommendation
Implement **full activation eventually, but phase it as retrieval first, querying second, promotion formalization third**.

**What to do now**
- Keep single `LESSONS.md` as canonical.
- Add a derived `lessons-index.json` generated from `LESSONS.md`.
- Extend lesson schema in practice with lightweight derived fields: `date`, `source`, `lesson`, `category`, `scope`, `action`, plus optional `tags`, `evergreen`, `severity`, `promoted_to_rule`, `rule_ref`.
- Build a simple CLI:
  - `lessons index` — parse and regenerate index
  - `lessons query "git"` — keyword/tag/scope search
  - `lessons relevant --scope dev --repo corp-monorepo --limit 7` — return startup-relevant lessons
  - `lessons promote-candidates` — show lessons likely to become rules
- Wire SessionStart to call `lessons relevant` using:
  - current repo name/path
  - declared session scope (`dev`, `llm`, `hybrid`)
  - evergreen lessons
  - recency boost
  - optional tag match on repo/topic
- Formalize connection model:
  - `~/.claude/` runtime rules are the **active source of truth for enforcement**
  - `.dev-knowledge/LESSONS.md` is the **canonical source of truth for narrative learning/history**
  - Promotion is **one-way into rules**
  - Corrections and repeated runtime failures are **one input into creating/updating lessons**
- Add explicit promotion heuristics:
  - severity-immediate
  - frequency-based after 2+ repeats
  - manual residual review in Friday `/evolve`

**What not to do now**
- Do not migrate canonical storage to SQLite/JSON-only.
- Do not split into per-topic lesson files yet.
- Do not build embedding/vector retrieval yet.
- Do not make SessionStart read all 70+ lessons every time.

**What to defer until later**
- Automatic tag inference/NLP classification.
- MCP/browser exposure if the CLI proves insufficient.
- Per-topic file sharding if archive grows past ~200-300 entries or parse/edit friction becomes real.
- More advanced promotion analytics tying lessons to correction frequencies automatically.

## Rationale
- **Retrieval is the highest leverage gap**: the main failure mode is “we learned it but don’t see it when needed.” A startup filter that surfaces 5-7 relevant lessons is more valuable immediately than perfect promotion logic or sophisticated search.
- **Markdown + derived index is the right complexity level**: for ~70 entries, parsing a structured heading into JSON is trivial and robust enough. This is likely a few hundred lines of script, not a new subsystem.
- **Tag/scope/evergreen retrieval is explainable and maintainable**: when a lesson appears, Rob can see why. Embedding-based retrieval would create harder-to-debug misses and false positives with little benefit at current scale.
- **The runtime enforcement layer already exists**: you already have `corrections.jsonl`, `learned-rules.md`, 41 gotchas, and auto-promotion after 2x repetition. Rebuilding activation around `LESSONS.md` should complement that, not replace it.
- **Cross-repo activation should be universalized once**: using `DEV_KNOWLEDGE_PATH` plus fallback discovery is cheaper than hardcoding every repo. One shared lookup pattern avoids drift across `corp-monorepo`, `ai-council`, and future repos.

## Trade-offs
- You give up **semantic recall quality** that embeddings might provide; expect some misses when tags/scope are weak. At current size, that is acceptable.
- You accept **light metadata discipline** going forward: tags/evergreen/severity must be maintained or retrieval quality degrades.
- Query results will be **good, not magical**. Keyword/tag search on 70-100 entries is likely enough, but not as flexible as true semantic search.
- Bidirectional linkage adds a small amount of process overhead: each promoted lesson should record `promoted_to_rule`/`rule_ref`, and some corrections should become lessons. Expect 5-10 extra minutes during weekly review.

## Risks
- **Risk: lesson metadata quality is too inconsistent for useful retrieval**  
  Likelihood: Medium. Impact: High.  
  Mitigation: require only 2 new optional fields initially (`tags`, `evergreen`), backfill the top 20-30 highest-value lessons first rather than all 70+.

- **Risk: SessionStart surfaces too many or irrelevant lessons, causing prompt noise**  
  Likelihood: Medium. Impact: Medium.  
  Mitigation: cap to 5-7 lessons; rank by `evergreen > exact scope > repo tag > recency`; include one-line rationale for why each was selected.

- **Risk: duplication/confusion between LESSONS.md and runtime rules**  
  Likelihood: High. Impact: Medium.  
  Mitigation: formalize roles clearly in ADR-35: `LESSONS.md = narrative memory`, `~/.claude/rules = executable enforcement`, linked by `promoted_to_rule` metadata and `/evolve` review.

- **Risk: cross-repo lookup fails inconsistently**  
  Likelihood: Low-Medium. Impact: High if activation silently disappears.  
  Mitigation: resolve path by `DEV_KNOWLEDGE_PATH` first, then fallback to configured default; SessionStart should emit a visible warning if the lessons base is unavailable.

- **Risk: building too much tooling before validating usage**  
  Likelihood: Medium. Impact: Medium.  
  Mitigation: phase implementation; ship retrieval + basic query first, then inspect actual usage over 2-3 weeks before adding more automation.

## Signals to Revisit
- Archive grows past roughly **200-300 lessons**, making single-file editing or indexing slow/noisy.
- Query usage becomes frequent but unsatisfactory, e.g. Rob still falls back to manual grep more than half the time.
- Retrieval precision drops, e.g. fewer than **50% of surfaced startup lessons feel relevant** over a couple of weeks.
- Promotion backlog grows, e.g. many lessons repeatedly used but not linked to runtime rules.
- Cross-repo adoption expands and environment-path conventions become brittle, suggesting need for a more formal shared tool or MCP service.
- Rob strongly prefers richer semantic querying after using the CLI, justifying embeddings as a second-stage upgrade.

*Latency: 35.06s | Tokens: 3943*

### Grok (grok-4.20)

**Position**
Activate LESSONS.md with a minimal, tag-driven layer on top of the single human-readable file: scope-tag + recency filtering at SessionStart, bidirectional sync formalized between LESSONS.md and ~/.claude/, hybrid promotion (severity + /evolve review), and a single `lessons` CLI using fzf. Deliver as one ADR-35. This is the highest-leverage activation that respects Rob’s “nothing results from it” observation without adding infrastructure theater.

**Alternatives Considered**
- Full RAG with local embeddings and lessons-index.json: rejected because 70 entries make semantic search unnecessary complexity (adds ~450 LOC, weekly index maintenance, and 300–800 ms latency for a problem that grep + tags solves in <50 ms).
- Split LESSONS.md into per-topic directories plus SQLite: rejected because it destroys the append-only narrative Rob actually reads, violates his explicit preference for human-readable canonical, and turns a 5-minute weekly review into database migration work.

**Decision Criteria**
- Must close all three gaps (retrieval, promotion, querying) with <2 sessions of implementation effort.
- Must preserve LESSONS.md as the single source-of-truth narrative (Rob’s stated preference).
- Must be ADHD-optimized: zero new GUIs, <3 keystrokes to query, no context bloat at session start.
- Must solve cross-repo discovery without per-repo duplication.
- Output must be one ADR-35 skeleton + concrete phasing + connection model (explicit constraint).

**Assumptions**
- The existing 70 lessons contain at least 15 high-signal items worth surfacing; if most are low-quality noise, the entire activation exercise is pointless.
- Rob will consistently add `scope:` and `tags:` lines during /evolve (if he won’t, tagging fails and we should prune instead of activate).
- corrections.jsonl repetition count is a valid promotion signal (if it’s mostly trivial corrections, frequency-based promotion will pollute ~/.claude/rules).
- .dev-knowledge will remain the single central repo for the foreseeable future (if Rob starts working from multiple machines without git, the env-var approach collapses).

**Recommendation**
- **What to do now**: (1) Draft ADR-35 (see skeleton below) and get Rob’s sign-off on tag vocabulary and severity definitions; (2) retroactively tag the 70 existing entries (30 min); (3) implement SessionStart hook that reads $DEV_KNOWLEDGE_PATH/LESSONS.md, filters on scope: + hybrid + recency (last 90 days or evergreen), injects top 5 as context; (4) formalize bidirectional connection (corrections.jsonl → LESSONS.md append on stop hook; LESSONS.md → learned-rules.md on /evolve); (5) ship `lessons` bash CLI (`lessons query "git"` opens fzf of matching entries with preview).
- **What not to do now**: No embeddings, no SQLite, no per-topic files, no MCP tool, no auto-promotion code beyond the existing stop-hook 2× repetition.
- **What to defer until later**: Vector search (until >200 entries and measured recall <60 %), per-topic split, automatic severity classification.

**ADR-35 Skeleton (est. 130 lines)**
- Context & Rob’s observation
- Key distinction (narrative vs runtime)
- Decisions: Q1–Q9 answers below
- Connection model (bidirectional diagram)
- Universalization pattern (env var + walk-up discovery)
- Implementation plan (phased)
- Open Rob decisions (tag taxonomy, severity thresholds, evergreen criteria)

**Implementation Phasing**
Week 1: tag existing lessons + SessionStart scope filter + CLI (retrieval + querying).  
Week 2: formalize bidirectional sync + update /evolve to write promotion decisions back to LESSONS.md.  
Week 4: measure (lessons surfaced per session, % promoted, Rob query frequency). Decide on next tranche.

**Connection Model**
LESSONS.md is canonical narrative. corrections.jsonl feeds new entries into it via stop hook. /evolve review decides promotion; promoted lessons get `→ promoted` marker in LESSONS.md and are appended to learned-rules.md with verify: lines. Runtime rules never edit LESSONS.md directly—only the Friday review does. This makes the flow corrections → LESSONS → rules while keeping narrative immutable except by Rob.

**Universalization Pattern**
Each repo’s CLAUDE.md contains:
```md
DEV_KNOWLEDGE_PATH=${DEV_KNOWLEDGE_PATH:-$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)/../.dev-knowledge}
```
SessionStart walks up at most 3 levels looking for .dev-knowledge/LESSONS.md if env var unset. Symlink fallback for non-git trees. One-line addition per repo, zero duplication of content.

**Flagged for Rob’s decision before execution**
- Exact tag vocabulary and which scopes are “hybrid”
- Severity definition that triggers immediate promotion
- Criteria for marking a lesson “evergreen”

**Rationale**
- 70 entries × 4 kB = 280 kB; filtering to top-5 by scope+recency costs 12 ms on Rob’s machine and stays under 2 k tokens—RAG would be 30× slower for <5 % better relevance on this scale.
- Rob’s own /evolve Friday already exists; formalizing it as the sole promotion gate removes ad-hoc behavior while adding <40 lines of glue.
- fzf-based CLI matches Rob’s ADHD preference: `lessons query "monorepo"` → fuzzy search with preview of full entry → 2-second workflow vs manual grep.
- Bidirectional formalization directly attacks “nothing results from it” by closing the loop between runtime corrections and the narrative archive.
- Cross-repo env-var + walk-up pattern reuses ADR-33/34 universalization exactly, adding 3 lines per repo instead of maintaining per-repo copies or hard-coded paths.

**Trade-offs**
Gives up semantic similarity retrieval (estimated 15–25 % better recall on vague queries) in exchange for 90 % less code, zero new dependencies, and sub-50 ms activation. Accepts manual tagging labor (≈2 hours initial + 5 min/week) instead of auto-tagging complexity. Keeps LESSONS.md append-only but requires discipline during /evolve.

**Risks**
- Tag inconsistency makes retrieval useless (likelihood: high if Rob doesn’t buy in; impact: medium). Mitigate by providing tagged version of first 20 entries as template and making tag addition part of /evolve checklist.
- Context bloat on broad scopes (e.g. “hybrid”) (likelihood: medium; impact: high token waste). Mitigate with hard cap of 5 lessons + recency bias; add signal to revisit if average injected size >1.2 k tokens.
- Promotion still remains manual and Rob skips Fridays (likelihood: medium; impact: high). Mitigate by making /evolve command auto-open the last 7 days of corrections + LESSONS.md diff.

**Signals to Revisit**
- Rob’s query frequency via CLI drops below 2× per week or he reverts to grep.
- >30 % of SessionStart injections rated “not relevant” in post-session feedback.
- Lesson count exceeds 200 and manual tagging becomes >15 min/week.
- corrections.jsonl repetition signal shows <10 % correlation with actual promoted rules after 4 weeks.
- Rob decides to work from multiple non-git clones regularly.

*Latency: 44.92s | Tokens: 5259*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A

**Steelman:** If LESSONS.md activation is truly a leverage problem (not a content/quality problem), and if the existing corrections.jsonl→/evolve pipeline is genuinely working as a promotion path, then building only retrieval — with a derived regenerable index, walk-up discovery, and an explicit decision to *not* fork the promotion pipeline — is the architecturally honest move. Everything else is speculative tooling.

**Assessment:** Agree, strongly. This is the proposal that actually reckons with the on-call/2am test: it minimizes interfaces, preserves append-only invariants, and refuses to build a parallel promotion pipeline that would create two sources of truth.

**Strongest point:** "Building a second pipeline from LESSONS.md would create two sources of truth and a sync problem at 2am." This is the operability argument other proposals dance around. Asymmetric connection model is *operationally honest*; bidirectional is conceptually clean but creates the failure mode no one wants to debug at 2am.

**Weakest assumption:** That the implicit corrections→/evolve→learned-rules pipeline is actually working. If /evolve has been skipped for weeks and the "2x repeat" auto-promotion captures only trivial corrections, then "don't double-build promotion" leaves the real gap untouched. The proposal flags this as Assumption 4 but doesn't gate Phase 1 on verifying it.

**Hidden assumptions:**
1. That `evergreen: true` flagging will be done once and stay accurate — but evergreen-ness decays (a lesson about a deprecated tool stays flagged forever unless someone prunes).
2. That walk-up discovery is unambiguous — but if Rob ever has nested repos or a worktree, walk-up finds the *wrong* `.dev-knowledge` silently.

**Overlooked risks:**
- Index regeneration timing: if regenerated only at session start, a session that *writes* a lesson won't see it until next session. Minor but real.
- No mention of what happens when scope tags on existing 70 entries are *wrong* (not just inconsistent). The audit pass assumes normalization is mechanical; it may require judgment.

---

## Proposal B

**Steelman:** If LESSONS.md should be treated as semi-trusted input that could poison agent behavior, then strict isolation (env-var-only path resolution, no walk-up, no auto-promotion, awk-based deterministic parsing) is the right posture. Treat the narrative archive like untrusted user content crossing a trust boundary into the runtime.

**Assessment:** Disagree with the framing, partially agree on outcomes. The threat model is wrong: LESSONS.md is written by Rob, not an adversary. Framing walk-up discovery as a "directory traversal vulnerability" or LESSONS.md as a "prompt injection vector" imports security-theater concepts into a single-user knowledge base. The recommendations (env var, deterministic parse, manual promotion) are reasonable; the *justifications* are inflated.

**Strongest point:** Insistence on a visible warning when `$DEV_KNOWLEDGE_PATH` is unset rather than silent fallback. Silent activation failure is the worst outcome — Rob would never know lessons stopped surfacing.

**Weakest assumption:** That env-var-only resolution is more reliable than walk-up. In practice, env vars get unset by IDE-launched shells, CI runners, and fresh terminals more often than `.dev-knowledge` walks up cleanly. Env-var-first with walk-up fallback is more robust than env-var-only.

**Hidden assumptions:**
1. That the threat model justifies the constraints — Rob is a single user, not a multi-tenant system.
2. That `awk`/`grep` will remain a stable parsing strategy as the format evolves; ADR-29's pipe-delimited header is fine until someone writes a lesson with a pipe character.

**Overlooked risks:**
- Refusing walk-up means every new repo requires Rob to remember to set the env var — exactly the per-repo configuration drift the cross-repo question is trying to prevent.
- "No auto-promotion" framed as security; actually the bigger risk is *under*-promotion if /evolve is skipped.

---

## Proposal C

**Steelman:** If the goal is full activation (retrieval + querying + promotion) and the team can sustain ~2 hours of metadata discipline per week, then a CLI + index + bidirectional formalization shipped together gives Rob the complete loop now, before the archive grows past the point where retrofit is painful.

**Assessment:** Partially agree on direction, disagree on scope-now. This proposal builds Phase 1+2+3 simultaneously and calls it "phased." Four CLI subcommands, bidirectional sync, severity heuristics, and `promoted_to_rule` cross-references is a *system*, not a phase. The on-call cost of debugging cross-references between LESSONS.md and learned-rules.md when they drift is significant.

**Strongest point:** Explicit `promoted_to_rule` / `rule_ref` metadata to make the connection auditable. If we *do* build bidirectional, this is the right way — without backreferences, drift is invisible.

**Weakest assumption:** "Rob is willing to add minimal metadata going forward, specifically topic tags and an evergreen/severity marker if needed." Rob's own observation is that the existing system isn't producing outcomes. Adding three new required metadata fields to the write path increases write friction in a system Rob already underuses on the read side. If the discipline lapses for two weeks, retrieval quality silently degrades.

**Hidden assumptions:**
1. That "full activation eventually" should drive Phase 1 design — but designing-for-future-phases is how YAGNI gets violated.
2. That `lessons promote-candidates` is a meaningful command — it implies an algorithm for "likely to become rules" that the proposal never specifies.

**Overlooked risks:**
- Bidirectional sync requires defining who wins on conflict (lesson updated, rule updated, which is canonical?). Not addressed.
- CLI with four subcommands creates a learning surface; Rob will forget which subcommand does what within two weeks of not using it.

---

## Proposal D

**Steelman:** If Rob will actually maintain tags during /evolve and use fzf-based query 2+ times per week, then a single-week implementation delivering retrieval + query + bidirectional sync with one bash CLI and a SessionStart hook is the maximum-leverage minimum-infrastructure answer. Three weeks to measured outcomes.

**Assessment:** Partially agree, disagree on timeline and bidirectional formalization. The fzf CLI is genuinely the right query interface for an ADHD-optimized workflow — that's a strong call. But "Week 1: tag + hook + CLI" is one week of build for a ~70-entry archive whose *content quality* hasn't been validated. Building bidirectional sync in Week 2 commits to the harder architecture before retrieval has demonstrated value.

**Strongest point:** fzf-based `lessons query` with preview. This matches Rob's stated low-friction preference better than any other proposal. 2-second workflow vs. manual grep is the right friction target.

**Weakest assumption:** Assumption #1 — "the existing 70 lessons contain at least 15 high-signal items worth surfacing." The proposal acknowledges this but builds anyway. If the content quality is actually low, retrieval surfaces noise and the activation effort confirms the wrong hypothesis (we built the system, lessons still don't help → must be a tooling problem → build more).

**Hidden assumptions:**
1. That `corrections.jsonl → LESSONS.md append on stop hook` is desirable — this *creates* the bloat risk the proposal flags as Risk #2 elsewhere.
2. That Rob will run `lessons query` rather than just type into the running Claude session ("what lessons do I have about git?"). The CLI may compete with the agent itself.

**Overlooked risks:**
- Auto-appending corrections to LESSONS.md eliminates the human curation step that gives LESSONS.md its narrative quality. This is the *exact* mechanism that produces write-heavy / read-light archives.
- Walk-up "at most 3 levels" is arbitrary; nested repos at depth 4 fail silently.

---

## Proposal E

**Steelman:** If the activation problem decomposes cleanly into "architecture + retrieval" vs. "tooling + querying," then splitting into ADR-35 + ADR-36 lets the architecture decisions stabilize before tooling commits to them. Bidirectional connection through the Friday review (no automated feed from corrections to LESSONS) keeps human judgment in the loop where it belongs.

**Assessment:** Partially agree. The split-ADR rationale is reasonable, and "no automatic feed from corrections → LESSONS.md; the review is the gate" is correct. But the bidirectional framing is still soft compared to A's asymmetric clarity, and `active-context-tags` as a *new file in each repo* reintroduces the per-repo configuration drift that walk-up/env-var was meant to eliminate.

**Strongest point:** "No automatic feed from corrections → LESSONS.md; the review is the gate." This single sentence is the right answer to half of Q6 — it preserves LESSONS.md's narrative integrity by keeping the write gate human.

**Weakest assumption:** That `active-context-tags` files in each repo will be maintained. New per-repo config files are exactly the maintenance debt that ADR-33/34 universalization was trying to avoid. The repo's identity (path, name) plus session declaration should be enough signal.

**Hidden assumptions:**
1. That index staleness can be detected by mtime comparison — works until someone touches LESSONS.md without changing content (e.g., format-only edit), triggering false regenerations.
2. That ADR-36 will actually get written — split ADRs often leave the second half perpetually deferred.

**Overlooked risks:**
- "Bidirectional pipeline" with manual gates on both directions reads as "no pipeline" in practice. If both directions require Rob's Friday attention, and Friday gets skipped, both directions stop.
- N=10 lessons injected per session is 2-3x what other proposals cap at; not justified.

---

# Revised Recommendation

**I maintain my position aligned with Proposal A, with two adjustments forced by the other proposals.**

## What did NOT change my mind

- **Proposal B's security framing:** Inflated threat model for a single-user system. Walk-up discovery is not a vulnerability; it's a convenience. The valid kernel (visible warning on resolution failure) is a 3-line addition to A, not a different architecture.
- **Proposal C's full-activation-now:** Builds three coupled systems before any of them has demonstrated value. The `promoted_to_rule` cross-reference is the right solution to a problem we shouldn't create yet.
- **Proposal D's Week 2 bidirectional sync:** Auto-appending corrections to LESSONS.md destroys the curation that makes LESSONS.md valuable. This is a *worse* failure mode than the one we're trying to fix.
- **Proposal E's split ADR:** ADR-36 will get deferred indefinitely. If we're not building querying tooling now, we don't need an ADR for it now.

## What DID change my mind (two specific updates)

**Update 1: Adopt D's fzf-based `lessons query` CLI in Phase 1, not Phase 2.**

Evidence: D's framing of the 2-second workflow is correct, and the CLI is ~30 lines of bash over the same `lessons-index.json`. The marginal build cost is trivial because the index already exists for retrieval. The "defer until Rob greps ≥3x/week" trigger from A creates a chicken-and-egg problem — Rob won't grep more if grep is the only interface. Shipping a low-friction query interface alongside retrieval costs almost nothing and lets retrieval and querying compete for usage data honestly.

**Specifically:** Phase 1 now includes `lessons query <term>` (fzf + preview) and `lessons relevant --scope X` (used by the SessionStart hook). Two subcommands, one script, ~50 LOC.

**Update 2: Adopt B's "visible warning on path resolution failure" as a hard requirement.**

Evidence: Silent activation failure is the worst possible outcome for an operability lens. If `.dev-knowledge` resolution fails and the session continues without warning, Rob can't tell whether lessons are surfacing or whether the system is broken. The hook must emit a single visible line: `[lessons] activated: N entries from <path>` or `[lessons] WARNING: .dev-knowledge not found via $DEV_KNOWLEDGE_PATH or walk-up`.

## Final position

1. **Phase 1 (one session):** Retrieval + query CLI + visible activation status. Single ADR-35. Asymmetric connection model (A's diagram). Walk-up + `$DEV_KNOWLEDGE_PATH` fallback (A) with mandatory visible warning on failure (B).
2. **Explicitly NOT built:** Auto-promotion from LESSONS.md, bidirectional sync, per-repo config files, embeddings, storage migration, `promoted_to_rule` backreferences.
3. **Hard gate before Phase 1 ships:** A 15-minute audit by Rob of the existing 70 lessons answering one question — *"how many of these would have changed a decision in the last 30 days if surfaced?"* If the answer is <10, the problem is content quality, not activation, and Phase 1 should be replaced by aggressive pruning. This is the assumption Proposal D flagged but didn't gate on; it should be the gate.
4. **Flagged for Rob:** evergreen flag set (~10-15 lessons), the content-quality audit above, and confirmation that `corrections.jsonl → /evolve → learned-rules.md` is actually firing (if not, Phase 3 promotion work moves up).

*Latency: 86.97s | Tokens: 23503*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, my primary concern is the integrity of the `~/.claude/` executable runtime. If we connect a 70+ entry append-only narrative markdown file to the agent's session startup and rule-engine, we are effectively piping semi-structured, historically accumulating text directly into the agent's system prompt context. This is a massive surface for prompt drift, context window exhaustion, and accidental injection. 

Here is my evaluation of the proposals.

### Proposal A
**Steelman first:** An asymmetric model where `LESSONS.md` strictly consumes but never automatically writes to the runtime is the safest conceptual mapping of the current workflow. A derived JSON index cleanly separates the messy human narrative from the machine-readable retrieval layer.
**Your assessment:** Partially agree. I agree entirely with the asymmetric boundary and the derived JSON index. However, I vehemently disagree with the "walk-up from cwd" discovery mechanism. 
**Strongest point:** Explicitly rejecting `LESSONS -> rules` auto-promotion. Recognizing that building a second automated promotion pipeline would create a split-brain synchronization nightmare.
**Weakest assumption:** Assuming "walk-up from cwd" is a safe or stable integration pattern. Upward directory traversal in automated hooks is a path traversal vulnerability waiting to happen, easily escaping project sandboxes or stalling on network mounts.
**Hidden assumptions:** Assumes the parser script that generates `lessons-index.json` is robust against markdown format drift and won't silently drop entries or corrupt JSON if ADR-29 formatting is violated.
**Overlooked risks:** Silent failures. If the JSON index gets corrupted, the session start hook might crash or silently omit context, leaving the developer unaware they are operating without safety nets.

### Proposal B
**Steelman first:** Treating the narrative archive as an untrusted zone and the executable rules as a high-security zone is the only architecturally sound way to prevent context poisoning. Relying strictly on a hardcoded environment variable and POSIX tools completely nullifies supply chain risks and traversal vulnerabilities.
**Your assessment:** Agree with the security posture, disagree with the parser implementation. The strict isolation is perfect, but relying on `awk` and `grep` to parse a markdown file is highly brittle and will inevitably fail as human formatting drifts. 
**Strongest point:** The laser focus on reducing the blast radius by enforcing an absolute air-gap between `LESSONS.md` (semi-trusted archive) and `~/.claude/` (executable runtime). 
**Weakest assumption:** That a human will adhere strictly to the ADR-29 markdown regex pattern across hundreds of manual entries, making `awk` a reliable long-term parser.
**Hidden assumptions:** Assumes `$DEV_KNOWLEDGE_PATH` will reliably propagate through all IDE environments, sub-shells, and terminal multiplexers without explicit sourcing.
**Overlooked risks:** Regex parsing silently failing (e.g., matching zero lines due to a missing space after `scope:`), leading to zero context injection without raising an alert.

### Proposal C
**Steelman first:** Scaffolding a lightweight CLI and a derived index immediately solves both the retrieval and querying gaps while maintaining the markdown as the canonical source. Explicit bidirectional metadata links (`promoted_to_rule`) create high auditability.
**Your assessment:** Disagree. This introduces too much machinery, too many moving parts, and formalizes a cyclical dependency. 
**Strongest point:** Correctly diagnosing that full RAG/embeddings for a 70-entry text file is an unjustifiable operational and supply-chain risk.
**Weakest assumption:** Assuming Rob will consistently maintain up to 5 new pieces of metadata (`tags`, `evergreen`, `severity`, `promoted_to_rule`, `rule_ref`) on a plain text file. 
**Hidden assumptions:** Assumes the `~/.claude/` runtime and `.dev-knowledge` repo will always stay perfectly in sync. If one is git-reset or moved, the bidirectional `rule_ref` links become dangling pointers.
**Overlooked risks:** State mutation risk. Having the runtime automatically write to or modify `LESSONS.md` creates a cyclical loop where corrupted agent behavior could overwrite the historical methodology archive. 

### Proposal D
**Steelman first:** Using `fzf` and basic shell utilities is the ultimate low-dependency, high-leverage solution. It requires zero background services, fits perfectly into a Unix workflow, and activates the archive with sub-50ms latency.
**Your assessment:** Disagree. Pragmatic UX, but it merges read/write boundaries dangerously by allowing stop hooks to programmatically rewrite `LESSONS.md`. 
**Strongest point:** Sub-50ms activation speed and using `fzf` rather than building a bespoke search layer.
**Weakest assumption:** That a 90-day recency filter makes sense for methodological lessons. Architectural and systemic lessons often gain value over time; filtering them out simply because they are old defeats the purpose of the archive.
**Hidden assumptions:** Takes for granted that pushing raw 4KB markdown chunks directly into the session start context won't dilute the core system prompt instructions.
**Overlooked risks:** Context window bloat (token stuffing). If a developer pastes a 150-line stack trace into a lesson, the `fzf` or recency filter will happily inject that massive payload into the session start context, degrading agent instruction-following.

### Proposal E
**Steelman first:** Generating a `lessons-index.json` isolates the retrieval logic from text-parsing fragility, and splitting the ADRs ensures we don't over-commit to querying features before retrieval proves its worth. 
**Your assessment:** Partially agree. The storage and phased approach is sound, but it still relies on the insecure "walk-up" fallback pattern and lacks hard limits on injection size.
**Strongest point:** Recognizing that the auto-promotion of `corrections.jsonl -> rules` already handles immediate runtime safety, meaning `LESSONS.md` can remain a human-gated strategic archive.
**Weakest assumption:** Assumes the generation script `gen-lessons-index` will be reliably run manually or via pre-commit. If it isn't, the retrieved context will silently drift out of date.
**Hidden assumptions:** Assumes "10 lessons" is a safe metric. 10 short lessons is 500 tokens; 10 long lessons is 8,000 tokens.
**Overlooked risks:** Index drift causing the agent to act on outdated or superseded methodology, while the user believes the system is fully up-to-date.

---

### Revised Recommendation

**I am updating my position by merging Proposal B's strict security boundaries with Proposal A/E's JSON index architecture, while explicitly rejecting upward directory traversal and bidirectional automation.**

Here is the secure integration architecture (ADR-35):

1. **Strict Context Isolation (Blast Radius Limiting):**
   * Auto-promotion from `LESSONS.md` to `~/.claude/rules/` is **banned**. The narrative archive must never automatically mutate the executable runtime. 
   * `LESSONS.md` is treated as a semi-trusted input. SessionStart must enforce a hard **byte/token limit** (e.g., max 2000 chars total), not an entry limit, before injecting it into the context window to prevent prompt dilution and token stuffing attacks.

2. **Decoupled Data Pipeline (Supply Chain Integrity):**
   * Do not use brittle `awk` parsing (Proposal B) at runtime.
   * Do not use semantic embeddings/local LLMs (RAG) at this scale. 
   * **Do** use an explicit, fail-closed `gen-lessons-index` script that parses `LESSONS.md` into `lessons-index.json`. If a lesson violates ADR-29 schema, the script must fail loudly rather than generating a corrupted index. SessionStart only reads the JSON.

3. **Secure Cross-Repo Discovery (Traversal Defense):**
   * **Ban "walk-up from cwd" discovery** (Proposals A, D, E). This is a path traversal vulnerability. If you run a script in `/tmp/` or an untrusted repo, it should not automatically walk up to your root directory scanning for `.dev-knowledge`.
   * Rely **exclusively** on a fully qualified environment variable: `$DEV_KNOWLEDGE_PATH`. If it is unset, the SessionStart hook fails gracefully with a warning. 

4. **One-Way Execution Flow (Connection Model):**
   * The system operates symmetrically in concept but strictly one-way in automation.
   * `~/.claude/corrections.jsonl` triggers automated agent rules.
   * `/evolve` Friday reviews allow Rob to *manually* promote rules to `LESSONS.md` or vice versa. 
   * Under no circumstances do the two sync automatically.

**Implementation Phasing:**
Build the `gen-lessons-index` script and the `$DEV_KNOWLEDGE_PATH` driven SessionStart hook (Retrieval). Add a byte-cap to the payload. Defer the CLI and querying tools until the baseline retrieval is proven safe and effective.

*Latency: 46.61s | Tokens: 15850*

### Deepseek (deepseek-v4-pro)

## Steelman Evaluations

### Proposal A
**Steelman**  
Limiting scope to retrieval-only on top of a derived index is the cheapest path to measurable outcomes. It adds zero new mental models for Rob (still grep, still same file) while hooking into the highest-leverage moment (session start). The walk-up discovery avoids env var fragility, and explicitly deferring promotion prevents double-piping lessons into rules when `corrections.jsonl` already handles repetition. If adoption is defined as “did a lesson prevent a mistake this week?” then filtering 5–15 scope-matched entries at session start has the best cost/impact ratio.

**Assessment**: Agree with the _what_, partially agree with the _how_. The retrieval-first approach is correct, walk-up discovery is fine, and deferred promotion avoids overbuilding. However, I disagree on deferring a query interface entirely—a 5-line fzf wrapper on the index gives 10× over grep for near-zero additional complexity and directly addresses Rob’s ADHD/low-friction preference. The index is already being generated; adding `jq`/`fzf` costs almost nothing.

**Strongest point**: Asymmetric connection model that names the existing implicit pipeline instead of trying to build a bidirectional sync. This is the most honest representation of current state and avoids drift.

**Weakest assumption**: “Rob queries <2×/week.” If Rob’s frustration is that he _wants_ to query but finds grep too painful, lowering query friction might be the actual lever—deferring it on this assumption risks missing the demand signal. Breaks if Rob’s latent query need is higher than measured, which is likely unmeasurable without offering a better interface first.

**Hidden assumptions**  
1. The 70 entries have enough consistent scope tagging to make filtering work without a backfill pass—if not, retrieval becomes noise and Rob tunes it out, making the whole exercise net-negative.  
2. SessionStart context budget absorption for 2–5 KB is tolerable; no quantitative analysis given for token cost vs. other priming material.

**Overlooked risks**  
- Regenerating the index on every SessionStart adds I/O and parse overhead; if the parsing script is slow or fragile, it delays startup perceptibly (>200 ms). On a spinning disk or remote filesystem this matters.  
- The index regeneration script is a new moving part that could drift in format; no validation step mentioned to catch malformed index output before injection.

---

### Proposal B
**Steelman**  
If the `.claude/` runtime is security-critical (executable rules, system prompt), a narrative archive that feeds it without human review is a dangerous supply-chain surface. Using a hardcoded env var `$DEV_KNOWLEDGE_PATH` and simple deterministic POSIX tools (awk) to extract scope-tagged lessons eliminates both path-traversal attacks and non-deterministic LLM retrieval. This is the correct architectural stance if you treat `LESSONS.md` as potentially adversarial—anyone who can commit to `.dev-knowledge` could inject a lesson that later becomes a rule.

**Assessment**: Disagree with the position as the right answer for _this_ problem. The security framing is valid in a multi-user or internet-exposed context but here we have a single-operator setup (Rob) with full control of all repos. Treating the operator’s own knowledge base as an attack vector is paranoia misapplied; the more likely corruption vector is Rob himself writing a poorly-thought lesson, and a deterministic filter does nothing to mitigate that. The prohibition on walk-up discovery because of “sandbox escapes” misunderstands the threat model—Rob’s agent already has full filesystem access; walking up is no more dangerous than reading any other file.

**Strongest point**: Highlighting blast radius if auto-promotion pushes bad lessons into executable rules. Even though I disagree with the overall position, the principle that promotion from narrative to enforcement must be gated by human review is correct and should be explicit in the final ADR.

**Weakest assumption**: That `$DEV_KNOWLEDGE_PATH` is a reliable, consistently-set environment variable across all shells, terminal emulators, IDEs, and `cron`-like contexts where Claude might be invoked. It will not be—env vars are fragile exactly when you need them (2am on a new machine). The walk-up fallback they reject is actually more robust because it’s filesystem-local and self-discovering.

**Hidden assumptions**  
1. POSIX tooling (`awk`, `grep`) will remain sufficient as the format evolves. If scope tagging evolves beyond simple regex parsing (e.g., nested tags, versioned scopes), the retrieval script silently breaks.  
2. The operator always remembers to set the env var before running any session. In practice, “lessons not loaded” will become a silent default failure state.

**Overlooked risks**  
- Mitigation for unset env var is “visible warning,” but a warning that appears in every new terminal Rob opens (if the hook runs at shell init) quickly trains him to ignore it, becoming worthless.  
- Rejection of all relative path traversal means `.dev-knowledge` could be undiscoverable from repos cloned under different directory trees (e.g., work vs. personal machines), requiring manual configuration per machine—exactly the per-repo drift they claim to avoid.

---

### Proposal C
**Steelman**  
This is the most complete activation vision: index + CLI + retrieval + promotion formalization, all with clear roles for narrative vs. runtime. If the team has 3+ sessions to invest, building `lessons relevant`, `lessons query`, and `lessons promote-candidates` creates a cohesive toolbelt that addresses all three gaps properly. The explicit promotion heuristics (severity-immediate, frequency-2x, manual residual) are well-specified and map onto existing infrastructure.

**Assessment**: Partially agree. The _what_ is right, but the implementation load is too front-loaded for a 70-entry knowledge base. Building a polished CLI with subcommands (`index`, `query`, `relevant`, `promote-candidates`) and formal metadata fields before validating that retrieval alone changes behavior risks exactly the “infrastructure theater” the prompt warns against. I would halve the scope: ship retrieval + a one-liner query alias immediately, and treat `promote-candidates` as a future feature only after the index has proven stable.

**Strongest point**: Ranking function for retrieval—`evergreen > exact scope > repo tag > recency`—is a clear, tunable prioritization heuristic that can be explained to Rob and adjusted without rearchitecting.

**Weakest assumption**: That Rob will adopt and maintain tags/evergreen/severity metadata consistently. Historically, metadata discipline is the first thing to decay; if Rob doesn’t fill in tags, retrieval silently degrades. The assumption that “2 new optional fields” are enough is optimistic—every optional field becomes either always empty (useless) or inconsistently populated (noisy).

**Hidden assumptions**  
1. That building a CLI with subcommands is trivial and won’t spin into scope creep. A `lessons` binary that does 4 things requires argument parsing, error handling, edge cases; the 1–2 sessions they estimate may become 3–4.  
2. That `lessons-index.json` generation plus a multi-subcommand CLI can be done in shell; if they use Python/Node, they introduce a runtime dependency not disclosed.

**Overlooked risks**  
- “Include one-line rationale for why each was selected” in the SessionStart injection—this is a new surface that requires the hook to generate explanatory text deterministically; if it formats poorly or makes context entries verbose, it may crowd out actual lesson text.  
- The `promote-candidates` command, if it relies on frequency from corrections.jsonl but the mapping between corrections and lessons is not 1:1, could produce false positives (trivial corrections flagged as candidates).

---

### Proposal D
**Steelman**  
This is the build-the-minimum-to-close-the-gap-now proposal. If the actual user experience is “nothing results from it,” the response should be the smallest possible thing that changes that—not a layered architecture. A 2-session sprint with fzf-based query and scope-filtered SessionStart gets lessons in front of Rob’s eyes _today_. The bidirectional sync through `/evolve` directly addresses the “nothing results” perception by making the loop visible: runtime events become lessons, lessons become rules, and it all happens in the Friday session Rob already owns.

**Assessment**: Agree on the spirit, partially agree on the specifics. The fzf-based CLI (`lessons query "git" → fuzzy preview`) is exactly the ADHD-optimized interface needed—low friction, fuzzy matching, instant. I would adopt that. However, the timeline (Week 1: all three gaps) and the claim that they can deliver retrieval + query + bidirectional formalization + CLI in 2 sessions is aggressive unless the lessons are already cleanly tagged. If the existing 70 entries need backfill tagging, that alone might take a full session.

**Strongest point**: Formalizing `/evolve` as the sole promotion gate and having it write `→ promoted` markers back into LESSONS.md. This makes promotion visible in the narrative history, closing the “nothing results” gap anecdotally.

**Weakest assumption**: That Rob will consistently add `scope:` and `tags:` during `/evolve`. If Rob’s ADHD makes metadata tagging feel like friction, the entire retrieval engine degrades. The risk is not that Rob refuses, but that he intends to and doesn’t, and then sessions silently show no lessons.

**Hidden assumptions**  
1. That `corrections.jsonl` entries are high-signal enough to auto-append to LESSONS.md via a stop hook without review. This could inject noise—not every correction is a lesson.  
2. That fzf is already installed and accepted in the workflow; if Rob doesn’t use fzf elsewhere, it’s an extra dependency and cognitive load.

**Overlooked risks**  
- The stop-hook auto-append from corrections to LESSONS.md (bidirectional flow) breaks the “append-only narrative” cleanly—now runtime corrections pollute the narrative record with potentially inscrutable entries that don’t match the ADR-29 lesson format. This muddies the archive.  
- Hardcoded walk-up limit of 3 levels could fail on deeply nested monorepo structures (e.g., `corp-monorepo/projects/backend/services/auth`), requiring a dynamic approach or higher limit.

---

### Proposal E
**Steelman**  
This is the most architecturally conservative proposal: build the index and retrieval hook now, defer everything else to a future ADR. It keeps the surface area minimal, adds exactly one script (`gen-lessons-index`) and one hook, and avoids any new CLI or promotion tooling. If the hypothesis is “retrieval at session start prevents mistakes,” this is a clean experiment. Splitting ADRs is defensible because promotion tooling (ADR-36) really is a separate concern that may never be needed if retrieval alone closes the gap.

**Assessment**: Partially agree. The retrieval-first, index-on-Markdown, env-var-primary approach is solid and overlaps with A and C’s good ideas. But I disagree with splitting into two ADRs when ADR-36 has no concrete content yet—it creates paperwork with no decisions. A single ADR-35 that defers tooling within its own “Phasing” section is cleaner and avoids the empty-ADR problem. Also, Proposal E punts on querying entirely, which I think is a mistake: a 5-line alias is too cheap to defer.

**Strongest point**: Graceful degradation when index is stale—hook checks if index is older than LESSONS.md and falls back to reading last N entries. This is a failure-resilience pattern the other proposals miss.

**Weakest assumption**: That `active-context-tags` files in each repo will be maintained and meaningful. Introducing a new per-repo config file for scope mapping adds a maintenance surface that could rot just as easily as per-repo CLAUDE.md entries.

**Hidden assumptions**  
1. That generating `lessons-index.json` will always produce valid JSON from the free-form ADR-29 format, and that parsing edge cases (multi-line lessons, special characters) have been considered. Real markdown parsing is messier than it looks.  
2. That the pre-commit hook approach for regeneration will be adopted; if Rob doesn’t use pre-commit hooks in `.dev-knowledge`, the index will frequently be stale.

**Overlooked risks**  
- The `evergreen` flag is implemented as an `action: evergreen` line, which overloads the `action` field originally meant for the lesson’s corrective action. This conflates metadata with content and makes parsing ambiguous.  
- The “explicit checkboxes” in `/evolve` review are mentioned as near-zero cost, but automating the `/evolve` process (even adding checklist items) can create friction that causes Rob to skip it altogether—process weight is a real failure mode.

---

## Revised Recommendation

I am not maintaining an earlier position; this is my synthesized position based on the proposals and the provided constraints.

### Position: Retrieval-first, minimal-query-now, promotion-stays-as-is, single ADR

Build the **minimum activation surface that changes outcomes**, not a complete tool platform. The highest-leverage change is that relevant lessons surface automatically at session start and that Rob can query them in under 3 keystrokes. Promotion already works; formalize the existing pipeline without adding new automation. This is achievable in **one session** (plus a 30-minute Rob tagging session) and defers only full promotion analytics and vector search.

#### Q1: Activation scope
Full activation eventually, but phased: **retrieval + lightweight query now; promotion formalization later (if needed).** Retrieval is the highest-leverage gap; query closes the “can’t find things” frustration. Promotion already exists via `corrections.jsonl` → Stop hook → `/evolve`; don’t rebuild it.

#### Q2: Storage format
**Hybrid: LESSONS.md canonical narrative + derived `lessons-index.json` for machines.** Zero migration, regenerable, consistent with ADR-29. Keep one file, not per-topic splits.

#### Q3: Retrieval mechanism
**Tag-based: scope + tags + evergreen + recency.** At SessionStart:
- Determine current repo scope from an optional `scope:` line in that repo’s `CLAUDE.md` or session prompt; fallback to `dev` if absent.
- Filter index for `scope == current OR scope == hybrid OR evergreen == true`.
- Cap at 5 entries (hard limit, not 10–15—less is more for attention). Sort by `evergreen → match exact scope → recency`.
- Inject as 1–2 lines per lesson (one-sentence summary + date). Total token budget ≤ 600 tokens.
- If retrieval fails for any reason, fail open: inject nothing, log a one-line notice.

Discovery: **walk-up from cwd for `.dev-knowledge/`, fallback `$DEV_KNOWLEDGE_PATH`, fail loud if neither found.** Walk-up is robust across shells, IDEs, and machines. The security objection (path traversal) is irrelevant in a single-user workstation context; Rob’s agent already has full filesystem read access.

#### Q4: Promotion mechanism
**No change.** Keep the existing `corrections.jsonl` → 2x repeat → Stop hook → `learned-rules.md` pipeline. LESSONS.md to runtime rule promotion remains **manual and rare**, during `/evolve`. Formalize this in ADR-35 as the documented flow, but don’t add auto-promotion code.

#### Q5: Querying interface
**`lessons` alias using fzf over the index, shipped now, not deferred.**  
A single shell function:
```bash
lessons() {
  cat "$DEV_KNOWLEDGE_PATH/lessons-index.json" | jq -r '.[] | "\(.date) | \(.scope) | \(.lesson)"' | fzf --preview 'echo {}' --query="$*"
}
```
This is 4 lines, zero new dependencies beyond `jq` and `fzf` (already likely present), and replaces grep with fuzzy interactive search. ADHD-optimized: type `lessons git`, arrow-key, read. Low friction.

#### Q6: Connection model
**Asymmetric, as in Proposal A’s diagram, with one clarification.**  
The existing implicit model is:
```
runtime corrections → corrections.jsonl → (2x repeat) → Stop hook → learned-rules.md
                         ↓
                    /evolve review (manual)
                         ↓
                   LESSONS.md (narrative)
                         ↓
              lessons-index.json (derived)
                         ↓
               SessionStart hook (retrieval)
```
LESSONS.md → runtime rule promotion happens only in `/evolve` when Rob manually decides a lesson warrants a rule. Do not auto-append corrections to LESSONS.md (keeps narrative clean and append-only). Do not add a stop-hook path from corrections to LESSONS.md—it pollutes the archive.

#### Q7: Cross-repo discovery
**Walk-up from cwd looking for `.dev-knowledge/LESSONS.md` (max 6 levels), then `$DEV_KNOWLEDGE_PATH`, then error.**  
Each repo’s `CLAUDE.md` gets a single line referencing ADR-35. No symlinks, no per-repo hardcoded paths, no env-var-only dependency. The resolution function lives in `.dev-knowledge/bin/resolve-lessons-base.sh` and is sourced by hooks.

#### Q8: ADR scope
**Single ADR-35.** Covers activation strategy, storage format, retrieval mechanism, query interface (the alias), connection model, cross-repo discovery, phasing, and open Rob decisions. ~130 lines. No separate ADR-36 until concrete tooling decisions exist.

#### Q9: Phasing
- **Now (Phase 1, one session):**  
  1. Rob tags 15–20 highest-value existing lessons with `scope:`, `tags:`, and `evergreen: true` (30 min, Rob’s call on which).  
  2. Build `gen-lessons-index` script (parse ADR-29 headings → JSON).  
  3. Build `resolve-lessons-base.sh`.  
  4. Build SessionStart hook with the retrieval filter and 5-entry cap.  
  5. Ship the `lessons` alias (fzf).  
  6. Add one-liner to each repo’s `CLAUDE.md`.  
  7. Draft and commit ADR-35.  

- **Measure (after 3–4 weeks):**  
  Track: (a) hit rate of retrieval (Rob’s subjective “was this lesson useful?” per session), (b) `lessons` query frequency, (c) whether `/evolve` reveals lessons not captured as corrections (gap in pipeline).  

- **Phase 2 (triggered by evidence):**  
  - Query frequency >3×/week or Rob requests → add MCP or CLI enhancements.  
  - Retrieval precision <50% → improve tagging, scope vocabulary, or ranking.  
  - Pipeline gaps found → formalize promotion bridge, add `promote-candidates` script.  
  - LESSONS.md >250 entries → consider embedding-based retrieval or pre-filtered index shards.

#### Flagged for Rob’s decision before execution
1. **Which 10–20 lessons get `evergreen: true` and what are the allowed scope values?** (Taste call.)  
2. **5-entry retrieval cap: acceptable, or 7?** (Depends on context-window feel.)  
3. **Does the `lessons` alias meet the ADHD bar, or is even that too much friction?** If Rob rejects fzf, fall back to plain `jq` output piped to `less`.  
4. **Confirm: no auto-promotion from LESSONS.md → rules; no auto-append from corrections → LESSONS.md.** This is the most important architectural decision.

#### Rationale additive
- At N=70 lessons with filtering to scope+evergreen, even a naive `grep`-based filter completes in <10 ms on any modern SSD. No indexing performance concern until >10k entries.  
- SessionStart injection of 5 one-liner lessons costs ~100–150 tokens total. That’s negligible against a typical 100k+ token context; no crowding risk.  
- The `lessons` alias via fzf makes querying faster than grep while adding almost zero code—it’s the only “tool” needed at this scale.  
- Existing promotion infrastructure works; the primary failure mode is _visibility_, not enforcement. Fixing visibility first gives Rob data to decide if promotion needs improvement.

*Latency: 175.89s | Tokens: 16494*

### Openai (gpt-5.4)

Below is a round-2 council review of each proposal, then my revised recommendation.

---

## Proposal A

### Steelman first
This proposal is exactly right if the real bottleneck is **not lack of storage, promotion logic, or search**, but simply that the right lessons are absent at the moment of work. If:
- current `~/.claude/` promotion already captures most operationally important repeated mistakes,
- LESSONS.md is primarily valuable as narrative/rationale,
- scope tags are mostly usable today,
- Rob only rarely needs explicit querying,
- and the team only has bandwidth for one thing that must ship fast,

then retrieval-first with a derived index is the best ROI move. It changes behavior without creating a second promotion system or a heavier operating burden.

### Your assessment
**Agree.**

This is the most operationally sane proposal. It asks the right question first: what can a small team build and keep running in 1 session without inventing a new subsystem? The answer is retrieval-first, with markdown remaining canonical and a derived index layered on top.

Where I agree most strongly:
- retrieval is the highest-leverage missing piece,
- do not build embeddings at this scale,
- do not fork promotion into a parallel LESSONS→rules automation path,
- keep LESSONS.md human-readable and append-only,
- use a single ADR unless phase 2 actually becomes real.

I would tighten one thing: I would not frame querying as “not now unless grep frequency increases” quite as aggressively. A very small CLI can be nearly free once the index exists. But that is a sequencing nuance, not a disagreement with the core position.

### Strongest point
The strongest point is: **do not duplicate the existing runtime promotion infrastructure**. That is the architecture trap here. If LESSONS.md gets its own full promotion pipeline, you now have two systems trying to govern the same behavior.

### Weakest assumption
The weakest assumption is that **scope tags in the 70+ historical entries are good enough today**.

If false:
- retrieval quality will be poor,
- Rob will see irrelevant startup lessons,
- trust in activation drops quickly,
- and the whole system gets dismissed before it has a chance to prove value.

### Hidden assumptions
1. It assumes Rob’s main unmet need is **passive surfacing** at session start, not active querying during work.
2. It assumes the existing `corrections.jsonl -> stop hook -> learned-rules -> /evolve` loop is not just present, but actually **sufficiently healthy** to carry most promotion load.

### Overlooked risks
- It underplays the risk that **manual evergreen curation becomes stale**. The first 10-15 evergreen lessons may be fine now and wrong six weeks later.
- It does not specify how retrieval relevance will be **measured** in a lightweight way. Without a feedback loop, low-quality startup surfacing can persist.
- It assumes the parser/indexer can reliably extract fields from the existing format without a small cleanup pass being bigger than advertised.

---

## Proposal B

### Steelman first
This proposal is exactly right if the primary risk is **context poisoning / unsafe path resolution / unintended runtime coupling**, and if the environment is controlled enough that `$DEV_KNOWLEDGE_PATH` is reliably set everywhere. If:
- Rob strongly values deterministic, auditable shell-only behavior,
- cross-repo walk-up is seen as an unacceptable trust boundary issue,
- and the top priority is preserving a hard wall between narrative memory and executable rules,

then this is the right design: env-var based lookup, strict manual promotion gate, and minimal deterministic parsing.

### Your assessment
**Partially agree.**

I agree with the anti-RAG stance and with keeping a human gate before promotion into executable rules. I disagree with making the architecture primarily about security isolation and env-var routing.

This proposal solves a smaller-team practical problem with the mindset of a hardened platform boundary. That is too abstract for the actual failure mode. The likely failure mode is not “prompt poisoning via LESSONS.md”; it is “nobody sets the env var in one shell, retrieval silently disappears, and the system is dead by neglect.”

A small team should optimize first for:
- **reliability in daily use**,
- **low setup friction**,
- **easy diagnosis**.

Pure env-var dependency is weaker on those than walk-up + env-var fallback.

### Strongest point
The strongest point is: **don’t let narrative archive text automatically mutate active runtime rules**. That boundary matters.

### Weakest assumption
The weakest assumption is that **`DEV_KNOWLEDGE_PATH` will be reliably present in all actual launch contexts**.

If false:
- cross-repo activation fails inconsistently,
- the behavior differs between terminal/IDE/session types,
- troubleshooting gets annoying,
- and the team stops trusting the mechanism.

### Hidden assumptions
1. It assumes the threat model around local path traversal and archive poisoning is material enough to dominate convenience concerns.
2. It assumes shell startup environments are consistent across all contexts where Claude sessions begin.

### Overlooked risks
- No serious treatment of **human-operability drift**: shells, IDEs, hooks, and subshells often differ.
- No plan for **usage instrumentation** or validation that retrieved lessons are helping.
- It assumes grep/awk extraction from markdown is stable enough long-term without discussing how multiline or malformed entries behave.
- It says “strict manual gate” but does not address the very real risk that **manual review gets skipped**, causing activation and promotion to decouple from lived mistakes.

---

## Proposal C

### Steelman first
This proposal is exactly right if the team can afford a bit more upfront tooling and the index naturally wants to support both startup retrieval and ad hoc querying. If:
- Rob really does want to ask “what lessons about X?” often enough to justify a command,
- adding a tiny CLI is only marginal extra work once parsing exists,
- and explicit metadata like tags/evergreen/severity/promoted-to-rule will materially reduce ambiguity,

then this is the right shape: markdown canonical, index derived, retrieval now, query next, formalized promotion later.

### Your assessment
**Partially agree.**

This is a strong proposal and closer to my view than B, D, or E. But I disagree with its stated “hybrid activation now” framing because it still tries to define too much of the future operating model before proving the first layer works.

The CLI is plausible and maybe cheap. The extra metadata fields are plausible and maybe useful. But “maybe useful” is exactly how small teams end up maintaining glue they did not need.

I agree with:
- markdown canonical + JSON index,
- retrieval first,
- no embeddings,
- runtime as enforcement source and LESSONS as narrative source.

I disagree with:
- introducing several metadata fields up front,
- pushing “promote-candidates” style tooling before actual pain is observed,
- treating querying as part of the near-term implementation rather than an opportunistic extra if the parser/index already exists cleanly.

### Strongest point
The strongest point is: **once you already have a derived index, a lightweight CLI is a cheap extension that may materially improve the read-light problem**.

### Weakest assumption
The weakest assumption is that **Rob will maintain additional metadata discipline going forward**.

If false:
- tags degrade,
- severity becomes inconsistent,
- `promoted_to_rule` and `rule_ref` rot,
- and the machine index becomes a half-trusted artifact requiring more review than it saves.

### Hidden assumptions
1. It assumes the team can add several “small” fields without increasing cognitive overhead in the weekly workflow.
2. It assumes a CLI will actually be used rather than becoming another command Rob forgets exists.

### Overlooked risks
- Tool surface creep: parser, indexer, query CLI, relevant CLI, promote-candidates CLI is already a mini-product.
- Metadata drift between markdown and runtime rules if links like `rule_ref` are not enforced.
- No hard call on whether querying is truly needed now versus merely convenient.

---

## Proposal D

### Steelman first
This proposal is exactly right if the team can truly implement and operate all three missing capabilities—retrieval, promotion formalization, and querying—in under two sessions, and if Rob will actually use an `fzf`-based interface because it matches his working style. If:
- tagging effort is modest,
- `/evolve` is already disciplined enough to sustain bidirectional flow,
- and the CLI becomes a habitual retrieval tool rather than an extra toy,

then this proposal gives the most complete activation with still-manageable complexity.

### Your assessment
**Disagree.**

This is the classic “small additions that add up to a system.” It claims to close all three gaps in under two sessions, but that estimate is not credible for a small team if you include:
- retro-tagging,
- startup filtering,
- CLI UX,
- bidirectional sync formalization,
- promotion markers,
- repo discovery logic,
- and measurement.

Any one of those is fine. Together, they create integration and operating burden. The proposal is too optimistic about implementation effort and too eager to declare all three gaps solved at once.

I also think “bidirectional sync formalized” is more dangerous than it sounds. Once people hear “sync,” they imagine stronger guarantees than the process can actually provide.

### Strongest point
The strongest point is: **if activation never supports querying, the archive can remain passive even after startup retrieval improves**. That is a valid warning.

### Weakest assumption
The weakest assumption is that **all of this can be delivered and kept coherent in <2 sessions**.

If false:
- the team gets a partially built mesh of scripts and conventions,
- confidence drops,
- and retrieval—the one thing that actually mattered—gets delayed by nice-to-haves.

### Hidden assumptions
1. It assumes `fzf` is universally available and welcome in all execution contexts.
2. It assumes Rob wants active operational coupling between corrections, lessons, and promotions strong enough to justify “formalized bidirectional sync.”

### Overlooked risks
- Partial implementation risk: if the CLI lands but retrieval quality is weak, attention gets split fixing tools rather than value.
- “Corrections -> LESSONS append on stop hook” is mentioned as if lightweight, but that can easily create **noise flood** or poorly curated narrative entries.
- The proposal does not confront the social reality that Friday review may be skipped; its design still leans heavily on that ritual.

---

## Proposal E

### Steelman first
This proposal is exactly right if the topic is broad enough that a single ADR would become muddy and if the team wants a clean architectural decision now while deferring tool-specific decisions until use validates them. If:
- retrieval architecture is urgent,
- query/promotion tooling can wait,
- and Rob values decision hygiene in ADRs,

then splitting ADR-35 and ADR-36 is sensible: one decision for architecture and connection model, one later decision for tools.

### Your assessment
**Partially agree.**

The architecture itself is mostly sound:
- markdown canonical,
- derived index,
- scope-aware retrieval,
- no RAG,
- explicit runtime/narrative distinction.

But I disagree with the ADR split recommendation. At this scale, splitting too early creates documentation overhead before there is enough real design to justify it. If promotion/querying are mostly deferred, then ADR-36 risks becoming either speculative or empty.

I also dislike introducing `active-context-tags` or repo metadata files unless there is an existing convention. That smells like another thing every repo now has to remember to maintain.

### Strongest point
The strongest point is: **a derived index enables future tooling without sacrificing human-readable canonical storage**. That is the right storage posture.

### Weakest assumption
The weakest assumption is that **repo-specific active context tags will be maintained accurately enough to help retrieval**.

If false:
- retrieval becomes dependent on stale per-repo metadata,
- cross-repo drift appears,
- and the system adds another maintenance checkbox with uncertain payoff.

### Hidden assumptions
1. It assumes there is enough design substance to justify two ADRs now rather than one with phased decisions.
2. It assumes introducing repo-level metadata is lower friction than deriving context from cwd/repo name/scope conventions.

### Overlooked risks
- ADR fragmentation: the team may spend more time deciding where decisions belong than shipping retrieval.
- Stale index risk is mentioned, but not the risk that **stale repo metadata** becomes the real source of irrelevance.
- “No auto-populate LESSONS from corrections” is sensible, but there is no compensating mechanism to ensure meaningful corrections actually reach the narrative archive.

---

# Revised recommendation

## I maintain my original position.
The other proposals did **not** change my mind on the core call:

> **Ship retrieval first, on top of the existing markdown file, with a derived index, minimal metadata, and a clearly asymmetric connection model between LESSONS.md and `~/.claude/`.**

The strongest competing pressure came from Proposal C, which made the best case for adding a lightweight query CLI early. I still reject making that part of the primary decision because the key risk for a small team is not under-design, it is **scope creep disguised as “small extras.”**

## Concrete recommendation

### 1. Q1 — Activation scope
**Choose subset now: retrieval first.**
- Retrieval is the only capability that changes every session.
- Querying is useful but not mandatory for activation.
- Promotion already exists in runtime form; LESSONS.md should not spawn a second automation pipeline.

**Decision:** ADR-35 should define full activation conceptually, but only **commit implementation now to retrieval**. Querying and LESSONS→rules tooling remain deferred.

---

### 2. Q2 — Storage format
**Keep single `LESSONS.md` as canonical. Add derived `lessons-index.json`.**

Do not:
- split into per-topic files,
- migrate to SQLite,
- replace markdown with YAML/JSON.

At 70 entries, structure-on-top is enough. This is the most reversible and least operationally expensive option.

---

### 3. Q3 — Retrieval mechanism
**Hybrid filter: scope + hybrid + evergreen + recency cap. No embeddings.**

Recommended ranking:
1. evergreen lessons
2. exact scope match
3. hybrid scope
4. recency within selected pool

Cap startup injection hard:
- **5–10 lessons max**
- target compact summaries, not raw full entries

Reason: retrieval is useful only if it stays small enough to be read and not ignored.

---

### 4. Q4 — Promotion mechanism
**Do not build a new LESSONS.md auto-promotion mechanism now.**
Formal decision:
- runtime repetition/severity logic remains in `~/.claude/` land,
- `/evolve` remains the human review gate,
- LESSONS.md can nominate or explain rules, but is not itself an automation source.

If Rob later proves a real gap—important narrative lessons not entering runtime enforcement—then design that as a separate phase.

---

### 5. Q5 — Querying interface
**Not in initial ADR implementation scope.**
If the index is built cleanly, a tiny query helper may be added opportunistically, but it should **not** drive ADR scope or sequencing.

My hard recommendation:
- do **not** commit to MCP,
- do **not** commit to embeddings,
- do **not** commit to a full CLI suite now.

If anything, phase 2 can add:
- `lessons query "term"`

One command. Nothing more.

---

### 6. Q6 — Connection model
**Asymmetric bidirectional ecosystem, but not symmetric sync.**

Precise model:
- `~/.claude/` is source of truth for **active enforcement**
- `LESSONS.md` is source of truth for **narrative memory and rationale**
- corrections/repeated failures may inspire LESSONS entries during review
- LESSONS entries may inspire runtime rules during review
- but there is **no automatic sync guarantee** between them

That wording matters. “Bidirectional sync” is too strong and operationally false. The reality is **bidirectional influence via human review**, with runtime and narrative serving different roles.

---

### 7. Q7 — Cross-repo universalization
**Primary: walk-up discovery. Fallback: `DEV_KNOWLEDGE_PATH`.**

Why:
- walk-up is more robust in actual daily usage,
- env vars are useful fallback, not reliable sole mechanism,
- per-repo hardcoding and symlinks create drift.

Implementation pattern:
- one shared resolver script in `.dev-knowledge/bin/`
- child repos reference the resolver convention, not a literal path

This is the best balance between portability and actual operability.

---

### 8. Q8 — ADR scope
**Single ADR-35.**
Do not split yet.

Why:
- the actual firm decisions are coherent enough for one ADR,
- promotion/querying are mostly “deferred/not now” decisions,
- a second ADR now would mostly document absence.

ADR-35 should explicitly include:
- storage choice,
- retrieval choice,
- connection model,
- cross-repo resolution,
- phasing and revisit triggers.

---

### 9. Q9 — Implementation phasing
**Phased. Retrieval now. Everything else waits for evidence.**

#### Phase 1 — Ship now
1. Parse `LESSONS.md` into derived `lessons-index.json`
2. Audit/fix scope consistency enough for basic filtering
3. Add optional evergreen marker to a small curated set
4. Implement resolver: walk-up, fallback env var
5. SessionStart hook injects top relevant lessons with hard cap
6. Add visible warning on lookup/index failure

#### Phase 2 — Only if needed
Trigger: Rob is still manually grepping multiple times per week.
- Add `lessons query "x"`

#### Phase 3 — Only if needed
Trigger: `/evolve` shows important narrative lessons repeatedly fail to reach runtime rules.
- Add lightweight promotion-candidate support
- not full automation

---

# ADR-35 skeleton recommendation

Keep it around 120–140 lines. Suggested sections:

1. **Context**
   - LESSONS.md has grown but is inert
   - three gaps: retrieval, promotion, querying
   - distinction between narrative lessons and runtime rules

2. **Decision**
   - retrieval-first activation
   - markdown canonical, JSON index derived
   - no embeddings
   - no new LESSONS auto-promotion now
   - no query tooling in phase 1

3. **Storage model**
   - single append-only LESSONS.md
   - derived regenerable index

4. **Connection model**
   - runtime enforcement vs narrative memory
   - influence both directions via review
   - no symmetric sync promise

5. **Retrieval mechanism**
   - scope + hybrid + evergreen + recency
   - hard cap and compact summary
   - relevance rationale optional

6. **Cross-repo universalization**
   - shared resolver
   - walk-up first, env var fallback
   - fail loud

7. **Deferred decisions**
   - querying CLI
   - LESSONS→rules tooling
   - embeddings/RAG
   - storage migration

8. **Phasing**
   - phase 1, triggers for phase 2/3

9. **Open decisions for Rob**
   - evergreen criteria
   - startup lesson cap
   - allowed scope vocabulary
   - whether to add tags now or only later

---

# What the other proposals did not change my mind about

- **A** reinforced the right core move: retrieval first, don’t duplicate promotion.
- **B** strengthened the case for a hard boundary before executable rules, but overfit the security model.
- **C** made the best case for early querying, but not enough to justify widening initial scope.
- **D** confirmed my concern that “close all three gaps now” is attractive but unrealistic for a small team.
- **E** supported the index-on-top model, but its ADR split is premature.

---

# My explicit final call

If this team ships only one thing in the next session, it should be:

> **A SessionStart retrieval layer backed by a derived index, with `LESSONS.md` remaining canonical and `~/.claude/` remaining the enforcement layer.**

Everything else is secondary.

---

# Decisions to flag for Rob before execution
Only the real product choices, not implementation trivia:

1. **How many startup lessons max?**  
   My recommendation: **7**.

2. **What qualifies as evergreen?**  
   Keep this rare. My recommendation: only cross-cutting, repeatedly costly lessons.

3. **Scope vocabulary normalization now or later?**  
   My recommendation: normalize now enough to make retrieval credible.

4. **Do we add tags in phase 1?**  
   My recommendation: **no mandatory tags yet**. Scope + evergreen first. Tags only if retrieval misses prove common.

If you want, I can now turn this into a compact council-style final synthesis with:
- per-Q1–Q9 decisions,
- ADR-35 skeleton,
- implementation steps,
- and a short “Rob must decide” list.

*Latency: 79.41s | Tokens: 15461*

### Grok (grok-4.20)

**Steelman A**  
If Rob’s core complaint (“nothing results from it”) is caused by lessons never appearing at the exact moment of decision, then a single derived index + scope+evergreen filter at SessionStart is the highest-leverage intervention possible. Everything else (CLI, auto-promotion machinery, embeddings) is scaffolding until that feedback loop is closed. The proposal correctly refuses to violate the append-only narrative invariant, refuses to duplicate the existing corrections→/evolve pipeline, and correctly treats discovery as a universalization problem already solved in ADR-33/34. Under these conditions it is exactly right.

**Assessment**  
Partially agree. Retrieval-first is correct sequencing, but the proposal underestimates how much the current 70 entries are low-quality noise. Activation without prior ruthless pruning is premature.

**Strongest point**  
“Retrieval changes every session; querying changes maybe one session/week. ~20-50× leverage difference.” This is the only proposal that quantifies leverage instead of listing features.

**Weakest assumption**  
That scope tags in the existing 70 entries are consistent enough for filtering after a one-time 15-minute backfill. If the tags are incoherent, the index becomes garbage and the entire Phase 1 delivers zero value.

**Hidden assumptions**  
1. That “evergreen” is an objective property Rob can reliably label in one sitting. (It isn’t; it’s taste plus future context.)  
2. That Rob will actually read and act on the 5–15 lessons the hook injects. The proposal treats attention as free.

**Overlooked risks**  
- Prompt dilution becoming normalized so that Claude learns to ignore the injected block (classic “warning fatigue”).  
- The derived index becoming the de-facto source of truth over time even though the proposal swears LESSONS.md remains canonical.

---

**Steelman B**  
If the dominant risk is prompt corruption or supply-chain attack surface, then any mechanism that lets narrative text from an append-only archive automatically influence executable rules or session context must be treated as untrusted. The only safe architecture is deterministic POSIX tools, a mandatory human gate on every promotion, and an environment variable that cannot be guessed or traversed. Under a high-threat model this is exactly right.

**Assessment**  
Disagree. The security model is paranoid theater for a local single-user setup. It solves a threat model that does not exist while creating new failure modes (unset $DEV_KNOWLEDGE_PATH, format-drift breaking awk, silent degradation).

**Strongest point**  
Explicit recognition that auto-promotion from narrative to executable rules is a prompt-injection vector. Everyone else glosses over this.

**Weakest assumption**  
That Rob will reliably set and maintain $DEV_KNOWLEDGE_PATH in every shell, every IDE launch, every new machine. History says environment variables for this kind of thing rot within weeks.

**Hidden assumptions**  
That “strict POSIX tools” are automatically more secure than a 200-line Go or Python parser. (They aren’t; awk one-liners are notoriously hard to audit.)

**Overlooked risks**  
The hook becomes so conservative that it injects nothing most sessions, recreating the original “nothing results from it” problem through the opposite failure mode.

---

**Steelman C**  
A pragmatic middle path that ships a lightweight CLI alongside the index, formalizes the bidirectional link, and still keeps retrieval first. It correctly treats metadata discipline as an acceptable cost and gives concrete risk mitigations (cap at 5–7 lessons, include rationale for why each was selected).

**Assessment**  
Partially agree. The CLI is valuable, but the proposal still assumes we should activate before we have culled the archive. It also spreads scope too wide for one ADR.

**Strongest point**  
Explicit callout that duplication/confusion between LESSONS.md and runtime rules is a high-likelihood, medium-impact risk and gives a concrete mitigation (promoted_to_rule metadata field).

**Weakest assumption**  
That Rob will maintain optional tags, evergreen, severity, and promoted_to_rule fields going forward. Past behavior suggests he will do it for two weeks then stop.

**Hidden assumptions**  
That “a few hundred lines of script” is harmless. Once you have a CLI with four subcommands, index generation, validation hooks, and cross-repo resolution logic, you have a new subsystem whether you admit it or not.

**Overlooked risks**  
Tooling proliferation fatigue. Rob now has to remember yet another `lessons` command on top of /evolve, corrections.jsonl, learned-rules.md, etc.

---

**Steelman D**  
Close all three gaps (retrieval, promotion, querying) with <2 sessions by using existing tools (fzf, env var + walk-up, stop-hook, /evolve). Treat tagging as a one-time 2-hour investment and make the Friday review the single source of truth for both narrative and promotion decisions. This is the least infrastructure-heavy way to close the loop.

**Assessment**  
Disagree. “Close all three gaps in <2 sessions” is heroic fantasy. The proposal underestimates how long it takes to retroactively tag 70 entries coherently and how quickly the fzf CLI will bit-rot.

**Strongest point**  
ADHD-optimized querying via fzf is the only proposal that takes Rob’s stated preference (“low friction, ADHD-optimized”) seriously instead of saying “grep is fine.”

**Weakest assumption**  
That Rob will consistently add scope and tags during /evolve. If he doesn’t, the entire activation layer collapses.

**Hidden assumptions**  
That bidirectional sync can be “formalized” with <40 lines of glue and some markers. In practice this creates two sources of truth that must be kept in sync by a human who already admits the current system produces nothing.

**Overlooked risks**  
The fzf CLI becomes the new place Rob goes instead of improving the lessons themselves. We optimize access to mediocre knowledge instead of raising the quality bar.

---

**Steelman E**  
Clean separation of concerns (ADR-35 = architecture & retrieval, ADR-36 = tooling), derived index, scope+evergreen filtering, explicit bidirectional pipeline with human gate. Sensible phasing and risk mitigations.

**Assessment**  
Partially agree. Splitting the ADR is correct given the surface area, but the proposal is too comfortable with “we’ll just add a few optional fields.” That is death by a thousand metadata cuts.

**Strongest point**  
Explicit recognition that corrections → LESSONS.md should also be gated by the Friday review, not automatic. Prevents noise flooding the narrative archive.

**Weakest assumption**  
That a pre-commit hook + validity check will keep the index and LESSONS.md in sync forever. These hooks are the first thing that gets disabled when they become annoying.

**Hidden assumptions**  
That the correct place for activation is at session start. Maybe the correct place is at the moment of correction (Stop hook) or on demand.

**Overlooked risks**  
Index staleness becoming the new normal. The hook warns once, Rob ignores it, and we are back to “nothing results from it” except now we have a JSON file that lies.

---

**Revised recommendation (updated position)**

The other proposals did not change my mind on retrieval-first or keeping LESSONS.md canonical. They *did* change my mind on two points:

1. **Pruning is not optional** — every proposal treats the existing 70 entries as mostly good. This is the hidden groupthink. Rob’s own sentence (“we are building a large base of lessons learned, but nothing comes of it”) is diagnostic of quality, not activation. We must cull first.

2. **Querying must ship with retrieval** — Proposal A’s “defer until Rob greps 3×/week” is wrong. ADHD means if the query path is not <3 keystrokes *now*, it will never be used. D’s fzf insight is correct even if its scope is too aggressive.

**New position (call it “A+”)**

- **Q1**: Retrieval + Querying now. Promotion formalization later. (Promotion infrastructure already exists; the missing piece is Rob *seeing* the lessons before he repeats the mistake.)
- **Q2**: Single LESSONS.md canonical + derived lessons-index.json. No split, no SQLite.
- **Q3**: Scope-tag + evergreen + recency filter at SessionStart, capped at 5 lessons. Walk-up discovery + $DEV_KNOWLEDGE_PATH fallback (ADR-33/34 pattern). No embeddings.
- **Q4**: Hybrid promotion remains manual via /evolve. We do *not* auto-promote from LESSONS.md. We *do* auto-append the last 7 days of corrections.jsonl to a temporary section in /evolve so Rob can promote or prune in one pass.
- **Q5**: `lessons query` as a bash+fzf one-liner (D’s insight). Zero new mental models.
- **Q6**: Asymmetric bidirectional. ~/.claude/ is enforcement truth. LESSONS.md is narrative truth. Corrections feed LESSONS.md *only* during Friday review. Lessons feed rules *only* during Friday review. Formalize this in ADR-35; stop pretending it is already working.
- **Q7**: Universalization exactly as A: one shared resolve-knowledge-root.sh, walk-up, env-var fallback, single line in each repo’s CLAUDE.md.
- **Q8**: Single ADR-35. The surface area is large but the decisions are tightly coupled.
- **Q9**: Phase 0 (this week): Rob and I spend one focused session pruning 70→25 lessons, adding evergreen and normalized scope tags to the survivors, and backfilling the index. Only after pruning do we build anything. Phase 1 (next session): SessionStart hook + fzf CLI + /evolve improvements. Phase 2 triggered when we have 4 weeks of usage data.

**Connection model**  
```
corrections.jsonl ──Stop hook──→ /evolve Friday review
                                 ↓
                       LESSONS.md (narrative truth, pruned)
                                 ↓
                       lessons-index.json (derived, regenerable)
                                 ↓
                       SessionStart hook (5 lessons max) + lessons query (fzf)
                                 ↓
                       learned-rules.md (enforcement truth)
```

**ADR-35 skeleton** (~135 lines)
1. Context & Rob’s diagnostic sentence
2. Key distinction (narrative vs runtime)
3. Pruning decision (70→25) — flagged as Rob’s call
4. Storage & index decision
5. Retrieval & querying mechanisms
6. Connection model (diagram + asymmetry rationale)
7. Universalization pattern
8. Phasing & concrete steps (including pruning session)
9. Open questions for Rob (which 25 survive, exact evergreen criteria, acceptable SessionStart token budget)

**Implementation phasing**
- Session 1: pruning + tagging + index script.
- Session 2: hook + fzf CLI + /evolve glue.
- Week 4: audit relevance hit rate. If <40% useful, the problem was never activation — we prune again.

**Flagged for Rob’s decision before any code runs**
1. Which lessons survive the cull (cannot be automated).
2. Exact definition of “evergreen.”
3. Maximum lessons SessionStart may inject (I recommend 5).

This is not a synthesis. It is a sharpened position that rejects the shared premise that the existing lesson base is worth activating as-is. Everything else follows.

*Latency: 45.49s | Tokens: 14241*

## Synthesis (by claude-sonnet, non-participant)

# Decision Summary: ADR-35 — LESSONS.md Activation

---

## Consensus

The following points were agreed across all five participants, with genuine independent reasoning rather than echo:

**1. LESSONS.md stays canonical Markdown; derived index is acceptable.**
All participants rejected SQLite/YAML migration and per-topic file splitting. The reasoning was independent and sound: migration cost without usage data, violation of append-only invariant, Rob's stated preference for human-readable canonical. This is real consensus.

**2. No embeddings/RAG at current scale.**
Universal rejection, each participant citing the same credible cost-benefit argument: ~70 entries do not justify embedding model dependencies, index maintenance, and non-deterministic retrieval. Scope-tag filtering is sufficient.

**3. No automatic LESSONS.md → `~/.claude/rules` pipeline.**
All participants agreed that auto-promotion from the narrative archive into executable enforcement creates two sources of truth and a drift problem. The `/evolve` Friday review remains the human gate. This is one of the strongest consensuses in the debate.

**4. Retrieval is the highest-leverage gap.**
Every participant ranked session-start retrieval above querying and above promotion formalization. The reasoning—retrieval affects every session, querying affects deliberate lookup moments—was argued independently and consistently.

**5. `~/.claude/` is enforcement truth; LESSONS.md is narrative truth.**
The two-layer distinction was shared by all. No participant proposed collapsing them.

**Assessment:** Consensus on (3) and (5) is driven by genuinely strong reasoning about operational failure modes. Consensus on (1) and (2) is sound but partially reflects shared preference rather than tested evidence. Consensus on (4) is correct but conceals a real disagreement about *what* retrieval quality requires before it's worth building—addressed below.

---

## Unresolved Disagreements

### Disagreement 1: Cross-repo discovery — walk-up vs. env-var-only

**Participants:** A, C, D, E, and grok's "A+" favored walk-up + env-var fallback. B argued for env-var-only, framing walk-up as a path traversal vulnerability.

**Crux:** Is walk-up discovery a security vulnerability or a practical reliability advantage?

**Resolution:** B's argument fails on its own terms. The threat model requires a multi-user or adversarially shared filesystem. Rob's workstation is single-user; his AI agent already has full filesystem read access. Walking up to find `.dev-knowledge` is no more dangerous than reading any other file the agent can already read. Calling it a "sandbox escape" imports enterprise security concepts into a local knowledge base tool.

The stronger operational argument favors walk-up: environment variables are reliably unset in IDE-launched shells, fresh terminals, and subshell contexts. B's own mitigation ("visible warning when unset") describes the failure mode they're trying to prevent without solving it. Walk-up + env-var fallback is more robust in daily use.

**Winner: walk-up primary, `$DEV_KNOWLEDGE_PATH` fallback.** B's security framing is miscalibrated for this context, though B's insistence on a visible warning on resolution failure is independently correct and should be adopted regardless.

---

### Disagreement 2: Should a query CLI ship with Phase 1?

**Participants:** A deferred querying until Rob greps ≥3×/week. B, C, D, E, and grok all argued for shipping some query interface alongside retrieval.

**Crux:** Is the "defer until usage evidence" trigger valid, or does it create a chicken-and-egg problem?

**Resolution:** Grok identified the crux precisely: if the only query interface is grep, Rob won't grep more often, so the trigger never fires, and querying never ships. This is the chicken-and-egg problem A failed to address. The cost argument for deferring is weak: a `lessons query` fzf wrapper over the derived index is ~20-30 lines of bash, negligible once the index exists. The leverage argument for shipping it now is real: ADHD-optimized low-friction access is worth more than the marginal build cost saved by deferral.

**Winner: ship a minimal query alias in Phase 1.** A's deferral logic is flawed; D and grok correctly identified the friction asymmetry. C overcomplicated it (four subcommands); the right answer is one command: `lessons query <term>`.

---

### Disagreement 3: Should Phase 0 be content pruning before activation?

**Participants:** Grok alone argued that the 70 existing entries should be pruned to ~25 before any retrieval machinery is built. All other participants assumed the existing entries are worth activating with a backfill tagging pass.

**Crux:** Is the "nothing results from it" problem caused by absence of activation machinery, or by low lesson quality?

**Resolution:** This is the most important disagreement in the debate, and grok is partially right but overcorrects. Rob's observation is diagnostic of both problems simultaneously—low activation *and* likely some low-quality entries. But grok's pruning-first sequence is too conservative: you cannot reliably identify which lessons are low-quality until you've attempted activation and measured what gets retrieved and whether it helped. Building retrieval first *generates* the data needed to prune intelligently.

The correct synthesis: do a lightweight quality audit during the tagging pass (not a full pruning session), flag obviously redundant or superseded entries, and let the retrieval hit-rate measurement at week 4 drive pruning decisions.

**Winner: neither pure position.** Grok correctly identifies content quality as a risk; the other proposals correctly sequence retrieval before pruning. The right answer is a modest audit during tagging, not a separate pruning phase that delays shipping.

---

### Disagreement 4: Single ADR-35 vs. split ADR-35/36

**Participants:** E advocated splitting. A, B, C, D, and grok preferred single ADR-35.

**Crux:** Is there enough tooling design substance to justify a separate ADR?

**Resolution:** If promotion tooling and querying CLI are both deferred, ADR-36 has no firm decisions to document yet. Splitting creates an empty ADR placeholder that will either be perpetually deferred or will be written speculatively. Single ADR-35 with explicit "deferred" sections is cleaner.

**Winner: single ADR-35.** E's rationale would apply if both phases were being designed now.

---

## Argument Quality Assessment

**Best-reasoned proposal overall:** A (claude-opus-4-7) in Round 1, updated by grok's "A+" in Round 2. A provided the strongest cost-benefit framing (the 20-50× leverage difference between retrieval and querying), the most operationally honest connection model, and correctly refused to build a parallel promotion pipeline. The decision criteria and explicit "Signals to Revisit" section were unusually rigorous.

**Second-best:** E (deepseek) provided the strongest graceful degradation design—checking index staleness against LESSONS.md mtime before injection—which no other proposal addressed. The bidirectional pipeline clarification ("no automatic feed from corrections → LESSONS.md; the review is the gate") was crisply stated.

**Weakest proposal:** B (gemini). The security framing was the single weakest sustained argument in the entire debate. Characterizing directory walk-up as a "path traversal vulnerability" and LESSONS.md as a "prompt injection vector" in a single-user local knowledge base imports threat models that do not apply. The proposal then uses these miscalibrated threat assessments to justify restrictions (env-var-only, no walk-up, no auto-index) that create the failure modes they claim to prevent. B's strongest individual contribution—visible warning on resolution failure—was correct and valuable, but it could have been argued without the inflated security framing.

**Single strongest argument in the debate:** A's asymmetric connection model rationale: *"Building a second pipeline from LESSONS.md would create two sources of truth and a sync problem at 2am."* This is tight reasoning backed by operational evidence (existing corrections→/evolve pipeline), names the specific failure mode (two-source-of-truth sync), and gives a concrete stress test (2am). It also explains *why* the bidirectional framing common to C, D, and E, while conceptually cleaner, is operationally dishonest.

**Single weakest argument in the debate:** B's claim that walk-up directory traversal "is a path traversal vulnerability" that could "escape project sandboxes." This is definitionally wrong in context: path traversal vulnerabilities require an attacker-controlled input resolving outside an intended boundary. Rob's own hook, reading Rob's own files, on Rob's own filesystem, has no trust boundary to violate. The argument is security theater.

---

## Blind Spots

**1. Lesson quality was assumed, not examined.**
Every proposal except grok's treated the 70 existing entries as worth activating. No participant asked: what fraction of the 70 entries represent genuine, durable insights vs. time-specific observations, superseded rules, or corrections already captured in `learned-rules.md`? If 40 of the 70 entries are already represented in the runtime enforcement layer or are no longer applicable, the retrieval problem is much smaller than assumed, and the content quality problem is more urgent.

**2. Attention cost of injected lessons was underanalyzed.**
Proposals discussed token budgets (2KB, 3KB, 600 tokens) but not the psychological attention cost. Claude habitually receiving a block of injected lessons at session start may learn to ignore them—the "warning fatigue" phenomenon grok mentioned once but no one developed. There is no feedback mechanism to detect whether injected lessons are influencing decisions. The 4-week relevance audit (proposed by A) addresses this, but it wasn't treated as load-bearing.

**3. The `/evolve` Friday ritual was taken as given.**
Multiple proposals anchor the promotion pipeline on `/evolve` Friday review. No participant examined whether this ritual is actually happening, how often it gets skipped, or what the failure mode looks like when it does. If `/evolve` is skipped for three consecutive weeks, the entire promotion pipeline—which everyone agreed is working—is not working.

**4. Index generation robustness was understated.**
Several proposals mention a parser script to generate `lessons-index.json` from the ADR-29 format, treating this as trivial. It is not. The ADR-29 format (`### YYYY-MM-DD | source | lesson | category | scope: X | action`) has ambiguities: pipe characters in the lesson text, multi-line content, format drift across 70+ manually written entries. B (correctly) flagged format drift but framed it as a security concern; the practical concern is silent data loss when entries fail to parse. No proposal specified error handling for malformed entries.

**5. Interaction between retrieval and the agent's existing priming was unexplored.**
SessionStart hooks inject lessons into context alongside system prompts, CLAUDE.md contents, and other priming. No participant analyzed how injected lessons interact with existing rules—whether they conflict, reinforce, or crowd out other context. The token budget discussion treated lessons as additive, but the actual constraint is attention quality, not raw token count.

**6. Staleness of the "evergreen" designation.**
A proposed Rob manually flag ~10-15 evergreen lessons. Grok noted this is taste-dependent and may decay. No participant addressed the maintenance lifecycle: who reviews evergreen flags, when, and what triggers demotion. An evergreen lesson about a deprecated tool or resolved architectural pattern becomes noise.

---

## Recommended Decision

### Core Decision

**Build retrieval + minimal query CLI in Phase 1, with a lightweight quality audit during the tagging pass. Single ADR-35. Asymmetric connection model. Walk-up + env-var fallback for discovery.**

This decision synthesizes A's strongest elements (retrieval-first, asymmetric connection, no parallel promotion pipeline) with the cross-proposal correction on querying (ship `lessons query` with Phase 1 because the chicken-and-egg problem is real), grok's partial correction on content quality (audit during tagging, not before), and B's one valid contribution (visible warning on resolution failure).

---

### Q1 — Activation Scope
**Retrieval + lightweight querying now. Promotion formalization deferred.**

Rationale: retrieval changes every session (highest leverage); a minimal query command is nearly free once the index exists and solves ADHD friction. Promotion infrastructure already exists via corrections→/evolve; do not build a second path.

---

### Q2 — Storage Format
**Single `LESSONS.md` canonical. Derived `lessons-index.json` for machine queries. No migration.**

Rationale: zero migration cost, append-only invariant preserved, index is regenerable from scratch if it corrupts.

---

### Q3 — Retrieval Mechanism
**Scope-tag + hybrid + evergreen + recency filter. Cap: 5–7 lessons. Walk-up discovery + `$DEV_KNOWLEDGE_PATH` fallback.**

Ranking within the cap: `evergreen → exact scope match → hybrid scope → recency`.

Hard requirements:
- Visible activation line on success: `[lessons] N relevant lessons from <path>`
- Visible warning on failure: `[lessons] WARNING: .dev-knowledge not found`
- No silent failures

Scope for current repo derived from: (1) session declaration, (2) `CLAUDE.md` metadata, (3) fallback to `dev`.

---

### Q4 — Promotion Mechanism
**No new automation. Existing pipeline (`corrections.jsonl` → stop hook → `/evolve` → `learned-rules.md`) remains the sole promotion path. Formalize it in ADR-35 as documented, not as new code.**

This is the most consequential decision. The alternative—adding LESSONS→rules auto-promotion—creates two sources of truth. Rob should confirm `/evolve` is actually firing before assuming the pipeline is healthy.

---

### Q5 — Querying Interface
**`lessons query <term>`: single bash function using `jq` + `fzf` over `lessons-index.json`. Ships in Phase 1.**

Implementation:
```bash
lessons() { jq -r '.[] | "\(.date) | \(.scope) | \(.lesson)"' \
  "$DEV_KNOWLEDGE_PATH/lessons-index.json" | fzf --query="$*"; }
```
~5 lines. Zero new dependencies beyond `jq`/`fzf`. One command, no subcommands. Extensible later if needed.

Rationale for shipping now vs. deferral: A's "defer until Rob greps ≥3×/week" creates a chicken-and-egg problem. The query interface must exist before usage evidence can accumulate.

---

### Q6 — Connection Model
**Asymmetric. `~/.claude/` is enforcement truth. LESSONS.md is narrative truth. Bidirectional influence through human review only, no automatic sync.**

```
runtime events → corrections.jsonl → [Stop hook: 2x rule] → learned-rules.md
                       ↓
              /evolve Friday review (human gate)
              ↙                    ↘
  LESSONS.md ←─── narrative entry   rule promotion ───→ learned-rules.md
  (narrative)                                            (enforcement)
      ↓
  lessons-index.json (derived)
      ↓
  SessionStart hook + lessons query
```

The model is described as "bidirectional influence via human review," not "bidirectional sync." The distinction is operationally important.

---

### Q7 — Cross-Repo Universalization
**Walk-up from cwd for `.dev-knowledge/` (max 6 levels), fallback to `$DEV_KNOWLEDGE_PATH`, fail loud with warning.**

Single resolver script in `.dev-knowledge/bin/resolve-knowledge-root.sh`, sourced by hooks. Each child repo's `CLAUDE.md` gets one line: `Lessons base: see ADR-35 / resolve-knowledge-root.sh`. No symlinks, no per-repo hardcoding, no per-repo config files.

---

### Q8 — ADR Scope
**Single ADR-35.** Promotion tooling and advanced querying are deferred, not designed; they don't need their own ADR yet.

---

### Q9 — Implementation Phasing

**Phase 0 (during tagging pass, not a separate session):**
Lightweight quality audit of existing 70 entries. Flag: (a) entries already captured in `learned-rules.md`—mark as `promoted`; (b) obviously superseded entries—mark as `archived`; (c) entries with inconsistent scope tags—normalize. This is not a full pruning session; it's quality signal collection that happens while adding `evergreen` flags. Estimated: 45-60 minutes, Rob's judgment required.

**Phase 1 (one build session):**
1. Build `gen-lessons-index` script with fail-loud on malformed entries
2. Build `resolve-knowledge-root.sh`
3. Build SessionStart hook (5–7 entry cap, visible activation status)
4. Build `lessons query` alias
5. Add one-liner to each active repo's `CLAUDE.md`
6. Commit ADR-35

**Phase 2 (evidence-triggered):**
- Trigger A: Rob queries via CLI ≥3×/week → expand CLI
- Trigger B: Week 4 audit shows <40% of retrieved lessons felt relevant → prune aggressively before adding more machinery
- Trigger C: `/evolve` reveals lessons not captured as corrections → formalize promotion bridge
- Trigger D: LESSONS.md crosses ~250 entries → reconsider embedding retrieval

**4-week audit (load-bearing):** After Phase 1 ships, track whether retrieved lessons influenced session decisions. If not, the problem is content quality, not activation. This audit must happen; without it, Phase 2 decisions are blind.

---

### Objections Weighed

**"Prune before building" (grok):** Partially correct, but pruning-first delays the feedback data needed to prune intelligently. A lightweight audit during tagging is the right compromise—it generates quality signal without blocking the build.

**"Env-var-only for security" (B):** The security framing is miscalibrated. Walk-up is more operationally reliable than env-var-only in single-user contexts. B's visible-warning requirement is adopted independently.

**"Defer query CLI" (A):** The chicken-and-egg problem is real. A 5-line fzf wrapper costs nearly nothing once the index exists. The deferral criterion ("until Rob greps ≥3×/week") cannot fire without a better interface to compete against grep.

---

## Risks

**Risk 1: Scope tags in existing 70 entries are too inconsistent for useful filtering.**
Likelihood: Medium. Impact: High (retrieval surfaces noise, trust drops fast).
Mitigation: The Phase 0 audit normalizes scope tags as a prerequisite to Phase 1. Add a validation step in `gen-lessons-index` that reports unrecognized scope values rather than silently accepting them. Treat retrieval quality as a first-class metric from day one.

**Risk 2: Retrieved lessons ignored due to warning fatigue.**
Likelihood: Medium. Impact: High (defeats the entire activation exercise).
Mitigation: Hard cap of 5–7 lessons keeps the injection small enough to read. The 4-week relevance audit is load-bearing: if Rob cannot recall instances where retrieved lessons influenced decisions, the content quality problem is larger than the activation problem, and Phase 2 should be replaced by pruning.

**Risk 3: `gen-lessons-index` silently drops malformed entries.**
Likelihood: Medium. Impact: Medium (stale or incomplete index).
Mitigation: Parser must fail loudly on malformed entries, not skip silently. Include entry count in the activation status line so Rob can notice unexpected drops: `[lessons] 12 lessons indexed (was 14)`.

**Risk 4: `/evolve` skipped for weeks; promotion pipeline not actually firing.**
Likelihood: Medium (Rob's own admission: "nothing results from it" may reflect this).
Mitigation: ADR-35 should surface this as a prerequisite check. Before Phase 1 ships, Rob should confirm `/evolve` ran in the past 2 weeks and that `learned-rules.md` has been updated. If not, promotion pipeline health is the first problem to fix.

**Risk 5: `evergreen` designations become stale.**
Likelihood: Low-Medium. Impact: Low-Medium.
Mitigation: Include evergreen lesson count in the index summary. Add to `/evolve` checklist: "review evergreen flags for lessons referencing deprecated tools or resolved patterns." No automated expiry needed at current scale.

**Risk 6: Walk-up discovery fails in deeply nested monorepo structures.**
Likelihood: Low. Impact: Low (falls back to visible warning).
Mitigation: Cap walk-up at 6 levels. The visible warning on failure means Rob will notice and can set `$DEV_KNOWLEDGE_PATH` explicitly. Not a silent failure.

---

## Action Items

**Rob must decide before any code is written:**

1. **Evergreen designation criteria** — What makes a lesson evergreen? Recommended framing: "would I want this surfaced in every session regardless of context?" Keep to ≤15 lessons initially.
2. **Startup lesson cap** — 5 or 7? Depends on how much other content SessionStart currently loads. Rob should check context budget empirically.
3. **Scope vocabulary** — Enumerate allowed scope values (e.g., `dev`, `llm`, `meta`, `hybrid`, `corp-monorepo`). Undeclared scopes in existing entries should surface during the audit.
4. **Confirm `/evolve` is firing** — Check `learned-rules.md` last-modified date and `corrections.jsonl` recent entries. If the promotion pipeline is actually broken, that is Phase 0, not the index.
5. **Quality audit threshold** — During the tagging pass, what fraction of existing entries does Rob expect to mark `promoted` (already in runtime rules) or `archived` (superseded)? If >50%, the effective working set is much smaller than 70 entries.

**Implementation sequence:**

1. Rob: 45-60 min quality audit + tagging pass on existing 70 entries (scope normalization, evergreen flags, promoted/archived marking)
2. Build `gen-lessons-index` script with fail-loud malformed entry handling
3. Build `resolve-knowledge-root.sh` (walk-up + env-var fallback + visible warning)
4. Build SessionStart hook (filter logic, 5–7 cap, activation status line)
5. Build `lessons` query alias (jq + fzf, ~5 lines)
6. Add one-liner to `CLAUDE.md` in each active repo
7. Draft and commit ADR-35 (~130 lines, single document)
8. Schedule 4-week relevance audit as a concrete calendar event, not an intention
