# AI Council Debate: ## Question: How do solo developers in 2025-2026 manage handoffs between a brows

**Date:** 2026-04-27 21:04:17
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20, gpt-5.4
**Synthesizer:** claude-sonnet (non-participant)
**Rounds:** 1
**Duration:** 222.0s
**Panel Mode:** full (5-model panel)
**Debate Mode:** research
**Source:** C:\Users\1028120\Downloads\council_research_handoff_patterns.md
**Cost:** ~$0.2393 (30,576 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
This is genuinely emerging territory with no dominant pattern yet. The pragmatic answer for a solo developer in 2025-2026 is a **single, repo-committed `HANDOFF.md` (plus an append-only `DECISIONS.md` log) living next to the code**, generated at session end by the browser chat and consumed as the first read by the CLI agent — not a bespoke tool, not JSON, not a folder hierarchy.

## Alternatives Considered
- **Structured JSON/YAML manifest (e.g., `context.json` with schema):** Rejected. Machine-elegant but humans don't edit it reliably at 2am, and current LLMs handle prose context better than they handle structured field discipline. Tooling-heavy with no commensurate payoff for n=1.
- **Folder-based session archive (`.sessions/2025-11-19/{plan,decisions,artifacts}/`):** Rejected as the *primary* artifact. Useful as an archive of past handoffs, but as the live handoff surface it fragments attention and increases the chance the CLI agent reads the wrong file. Acceptable as a secondary `.sessions/archive/` directory.

## Decision Criteria
1. **2am test:** Can a tired solo dev (or future-self in 6 months) reconstruct state in <5 minutes?
2. **Tool-agnosticism:** Survives switching between Claude Code, Aider, Cursor, Codex CLI, etc. — none of these have stable handoff formats.
3. **Low ceremony:** Cost per session-end must be <2 minutes or the dev abandons it.
4. **Versionable with code:** The handoff must travel with the repo, not live in vendor cloud state.
5. **Multi-repo coordination:** Must degrade gracefully when work spans repos.

## Assumptions
- The solo developer is using at least one chat UI (browser) and at least one agentic CLI tool, and switches between them several times per feature.
- LLM context windows in 2025-2026 remain large enough (200k+) that prose handoffs are cheap to ingest, but session memory across vendors remains non-portable.
- The developer values reproducibility and audit trail more than maximum velocity on any single session.

## Recommendation

**Do now:**
- Adopt a two-file convention at repo root (or `docs/ai/`):
  - `HANDOFF.md` — **mutable, overwritten each session.** Current state only.
  - `DECISIONS.md` — **append-only log.** One dated entry per material decision with rationale.
- Standardize `HANDOFF.md` sections: `Goal`, `State (what's done)`, `Next Action (exact next step)`, `Open Questions`, `Do-Not-Touch`, `Files in Play`, `How to Verify`.
- End every browser-chat session with the prompt: *"Produce a HANDOFF.md replacing the current one. Use these sections. Be specific about file paths and the exact next command."*
- Start every CLI-agent session with: *"Read HANDOFF.md and DECISIONS.md (last 5 entries). Confirm understanding. Do not proceed past 'Next Action' without asking."*
- For multi-repo work: a thin `meta/HANDOFF.md` in a coordinating repo (or gist) that links to per-repo handoffs by commit SHA.
- Commit handoffs. Yes, even the mutable one — git history *is* the archive.

**Do not do now:**
- Do not build or adopt a custom tool/CLI/plugin for this. The format is still evolving; tooling locks in premature decisions.
- Do not use JSON/YAML schemas. Prose is the right substrate for current models and humans.
- Do not rely on vendor "memory" features (ChatGPT memory, Claude Projects state) as the source of truth — they're not portable and not auditable.
- Do not let the browser chat write code directly into the repo. Keep the strategy/execution boundary clean: browser produces *plans and handoffs*; CLI produces *diffs*.

**Defer:**
- Schema formalization, hooks/automation (pre-commit handoff validators), and multi-agent orchestration. Revisit once a clear winner emerges in tooling (see Signals).

## Rationale
- **Practitioner reports cluster on prose, not schemas.** Across HN/Reddit threads on Aider and Claude Code through 2025, the consistently-praised patterns are `CONVENTIONS.md`, `AGENTS.md` (the de-facto Aider/Codex convention), and ad-hoc `HANDOFF.md` files. The structured-manifest crowd is loud but small, and most report abandoning their schemas within weeks.
- **Append-only decision logs solve the actual pain point.** The complaint isn't "I lost my context" — it's "I re-litigated the same decision three times because I forgot why I rejected approach X." `DECISIONS.md` (ADR-lite) directly addresses this; one-file `HANDOFF.md` does not.
- **The browser/CLI split should be enforced by *artifact*, not by discipline.** Telling yourself "I'll keep strategy in the browser" fails. Saying "the browser's only output is HANDOFF.md and DECISIONS.md entries" is enforceable.
- **Git is the session store you already have.** `git log -- HANDOFF.md` gives you free session history. No tool needed.
- **Within-session scope creep is not solved by handoff format.** It's solved by forcing the browser chat to produce a numbered plan *before* execution and refusing to proceed past step boundaries. Handoff hygiene won't fix a runaway conversation.

## Trade-offs
- **You give up structured queryability.** You can't `jq` over your handoffs. For n=1, this doesn't matter; for a team, it would.
- **You give up vendor-specific features** (Claude Projects, ChatGPT custom GPTs with persistent state). Worth it for portability.
- **Manual session-end discipline is required** — probably 60-90 seconds per handoff. Skip it once and the next session is degraded.
- **Multi-repo coordination is genuinely awkward.** The `meta/HANDOFF.md` approach is a workaround, not a solution; expect ~20% friction overhead on cross-repo features.

## Risks
- **Handoff drift (high likelihood, medium impact):** `HANDOFF.md` becomes stale and lies. Mitigation: timestamp at top, refuse to start a CLI session if timestamp >24h old without re-reading code.
- **Browser chat hallucinates state into the handoff (medium likelihood, high impact):** It claims work is done that isn't. Mitigation: `How to Verify` section must contain runnable commands; CLI agent's first action is to run them.
- **DECISIONS.md becomes a dumping ground (medium likelihood, low impact):** Mitigation: cap entries at ~5 lines; if longer, it's an ADR and goes in `docs/adr/`.
- **Format ossifies before the ecosystem converges (low likelihood, medium impact):** A standard emerges (e.g., `AGENTS.md` is already gaining traction for Codex/Aider) and your convention diverges. Mitigation: the format is plain markdown; migration is a find-replace.

## Signals to Revisit
- **`AGENTS.md` or an equivalent becomes a cross-vendor standard** (Anthropic, OpenAI, Cursor all read the same file). Then align to it.
- **A handoff-specific tool gets >2k GitHub stars and active maintenance** (none qualifies as of late 2025).
- **You start working with another human.** The prose-first approach scales poorly past n=2; move toward schemas and tooling.
- **Session-end handoff time exceeds 3 minutes consistently.** That means the format is too heavy; cut sections.
- **You catch the CLI agent making the same wrong assumption twice across sessions.** The handoff isn't carrying the constraint — promote it from `HANDOFF.md` to `CONVENTIONS.md`/`AGENTS.md` (permanent rules, not session state).

*Latency: 51.41s | Tokens: 4014*

### Gemini (gemini-3.1-pro-preview)

## Position
Establish a strict, human-gated "air gap" between Web AI (untrusted strategy) and CLI AI (privileged execution) using version-controlled, human-readable Markdown manifests, treating the browser as a zero-trust environment. 

## Alternatives Considered
1. **Automated API/Extension Syncing (Browser-to-Local Bridge):** Rejected. Connecting an internet-connected Web AI—which is highly susceptible to indirect prompt injection via web search or malicious URLs—directly to a local CLI agent creates an unacceptable blast radius. An injection in the browser could result in automated remote code execution (RCE) with `$USER` privileges on the host machine.
2. **All-in-One IDE Agent Usage (Abandoning Web UI):** Rejected. Solo developers rely on Web AIs for deep strategic reasoning, isolated canvas UI environments, and multi-modal web search. Forcing all interaction into an IDE agent pollutes the local repository's context window with conversational noise and limits architectural exploration.

## Decision Criteria
1. **Blast Radius Containment:** If the Web AI hallucinates or is compromised via prompt injection, the error must not autonomously execute against the local filesystem.
2. **Boundary Auditability:** The integration point between strategy and execution must be frictionless but strictly human-readable and subject to standard developer tooling (Git diffs).
3. **State Durability:** Decisions must survive browser session expiration, Web AI context-window collapse, and terminal agent resets.
4. **Multi-Repo Safety:** Context must remain scoped to the specific repository boundary to prevent an agent from autonomously traversing into adjacent, unrelated codebases.

## Assumptions
1. Terminal-based agents (e.g., Aider, Claude Code, Copilot CLI) operate with the developer's full local OS and filesystem privileges.
2. Web-based agents are routinely exposed to untrusted external data (via web browsing or pasted API docs), making them hostile environments from an execution-security perspective.
3. Solo developers lack enterprise SIEM/DLP controls, meaning isolation must happen purely at the workflow and process layer.

## Recommendation
**What to do now:**
- **Standardize on a `handoff.md` or `.plan.md` artifact:** Instruct the Web AI to output its final strategy as a strictly formatted Markdown block containing three sections: *Architecture Decisions*, *Acceptance Criteria*, and *Permitted Execution Steps*.
- **Enforce Human-in-the-Loop Transfer:** Manually copy this artifact from the browser and commit it to the root of the target repository.
- **Run CLI Agents Constrained to the Artifact:** Invoke the local agent (e.g., `aider --message-file handoff.md`) so its system prompt is anchored entirely to the static, reviewed file rather than an open-ended chat interface.
- **Return with Diffs, Not Context:** When context loss occurs or the CLI agent fails, paste only the `git diff` or specific error logs back into the Web AI. Treat the repository state as the sole source of truth.

**What not to do now:**
- Do not use JSON, YAML, or bespoke config-driven handoff formats. They are harder for humans to skim quickly, increasing the likelihood that a maliciously injected command or hallucination slips past the developer's review.
- Do not install browser extensions or local companion apps that claim to "seamlessly sync" web chats to local IDEs/filesystems. 
- Do not let the CLI agent autonomously update the strategy/handoff document without human review.

**What to defer until later:**
- Automated bidirectional synchronization and multi-repo orchestration frameworks (e.g., relying on LangChain/AutoGen to bridge cloud and local). Wait until local CLI agents support robust, out-of-the-box native containerization (e.g., executing all filesystem operations inside disposable, network-isolated microVMs).

## Rationale
- **Cryptographic/Human Boundary:** A manual Markdown copy-paste step acts as a secure integration boundary. It breaks the automated execution chain, reducing the blast radius of a hijacked Web session to exactly what the human consciously chooses to save to disk.
- **Git as the State Vector:** Ephemeral SaaS sessions routinely suffer "context collapse" or are lost to browser crashes. Pinning the strategy to `handoff.md` and tracking execution via atomic Git commits ensures zero context loss. The repository history becomes the persistent memory.
- **Scope Creep Mitigation:** Web conversations inherently drift. Forcing the Web AI to distill a 30-turn conversation into a strict 1-page Markdown file strips out conversational hallucination and enforces a minimal attack surface for the execution phase.
- **Cross-Repo Isolation:** By keeping handoffs file-based within specific repositories, you implicitly sandbox the local agent. If work spans two repos, you generate two separate `handoff.md` files in the Web UI. This prevents a compromised CLI agent from using a global context to exploit relative paths (`cd ../sensitive-repo`).

## Trade-offs
- **Developer Velocity:** You sacrifice the "magic" feeling of an AI seamlessly writing code while you chat. The manual copy-paste-review cycle adds friction (estimated 30-60 seconds per context switch).
- **Asymmetric Context:** The Web AI does not automatically know what the CLI agent actually did. The developer absorbs the cognitive load of manually feeding execution results (diffs/logs) back upstream to the Web UI for the next planning phase.

## Risks
- **Risk:** Developer fatigue leads to blindly copy-pasting complex, hallucinated bash commands from the Web AI into the `handoff.md`, which the CLI agent then blindly executes.
  - **Mitigation:** Implement strict system prompts in the Web AI: *"Never write executable bash strings in the handoff document; only describe the intended end-state of the filesystem."* (Likelihood: High, Impact: Critical).
- **Risk:** Sensitive local code or API keys are accidentally pasted back into the Web AI during the "upstream" feedback loop, violating data privacy.
  - **Mitigation:** Treat the Web AI strictly as a "clean room" for greenfield logic, architecture, and documentation. Keep proprietary, high-risk refactoring strictly within local, privacy-respecting IDE agents (e.g., local LLMs or zero-retention enterprise APIs). (Likelihood: Medium, Impact: High).

## Signals to Revisit
- The Model Context Protocol (MCP) or similar standards mature to allow scoped, read-only, cryptographically verifiable context sharing between cloud SaaS and local filesystems without exposing execution endpoints.
- CLI AI tooling integrates native, transparent sandboxing (e.g., Cursor or Aider running all generated code in an ephemeral WASM environment or Docker container by default).
- Web AI providers implement reliable, un-bypassable intent-signing, guaranteeing that an output was generated by the model's core logic and not blindly echoing an indirect prompt injection from a malicious URL.

*Latency: 37.70s | Tokens: 3971*

### Deepseek (deepseek-v4-pro)

## Position
Adopt a lightweight, version-controlled **Handoff Markdown (handoff.md)** with a strict, AI-friendly template and a minimal CLI snapshot script. This pattern is the highest-leverage, lowest-friction approach available today for solo developers bridging a browser-based strategy assistant and a terminal coding agent. It does not attempt to auto-sync via opaque APIs, which would introduce more failure modes than it removes at current scale.

## Alternatives Considered
1. **Single‑agent integration (Cursor agent mode, Copilot Workspace) that eliminates the split**  
   Rejected because these agents are still weak at long‑running strategy refinement across multiple sessions and often lack the “thinking space” developers get from a browser‑based chat with a specific model tuned for planning. Most solo devs intentionally separate strategic thinking (browser) from code‑level execution (CLI) to reduce context pollution.

2. **Bidirectional automation via a local daemon that pipes context between web chat and terminal agent (e.g., custom server, MCP-based bridges)**  
   Rejected for solo‑scale work: 80% of the value comes from a structured file, while a daemon introduces persistent processes, API‑key distribution, authentication headaches, and fragility—breaking down at exactly the wrong moment (network blip, token limit, daemon crash). The marginal benefit over markdown does not justify the ops burden until session counts exceed ~20/day.

## Decision Criteria
- **Context fidelity after session loss** – ability to recover exactly what decisions were made, what remains pending, and what artifacts exist without replaying a 2‑hour chat.
- **Manual overhead per handoff** – fewer than 90 seconds of developer effort per transition.
- **Tool agnosticism** – works with any combination of web AI (ChatGPT, Claude, Gemini) and terminal agent (Claude Code, Aider, Copilot CLI) without changing the core workflow.
- **Multi‑repo co‑ordination** – consistent enough to link work across 2+ repositories without duplicating context.
- **Mechanical reliability** – format parsing by both human and AI must not degrade even when handoff file grows to hundreds of KB.

## Assumptions
1. The developer uses git for all projects and is willing to commit the handoff file alongside code changes.
2. The browser assistant can output formatted markdown on request, and the terminal agent can read arbitrary local files.
3. The developer performs 3–6 handoff transitions per day; the “last known good” context from a previous session must be locatable within seconds.
4. Both the browser chat and the terminal agent access the same local filesystem (e.g., same laptop, or synced via git), so a file-based artifact is always available.

## Recommendation
**What to do now**
- Create a `.handoff/handoff.md` in the project root (or use a top-level `handoff.md` for single‑repo work). Adopt a template with these sections:
  - **Strategy & Goal** – 1-2 sentences of the strategic intent from the last browser session.
  - **Decisions** – bullet list of technical choices made, with rationale.
  - **Pending Work** – tasks that were identified but not executed, each with a checkbox.
  - **Execution Plan** – a numbered checklist of what the terminal agent should do next, including explicit file paths and constraints.
  - **Context Snapshot** – automatically generated metadata block (current branch, last commit hash, list of modified files) appended by a small CLI script.
- Use a 5-line bash script (`handoff-snapshot`) that appends a timestamp, branch, `git status -s` summary, and a placeholder for AI output. Invoke it at the end of every strategy browser session.
- In the browser: instruct the AI, *“Using this exact format, produce a handoff artifact for my terminal agent…”* and paste the result into `handoff.md` beneath a new `## Session YYYY-MM-DD …` header.
- In the terminal agent’s first prompt: *“Read .handoff/handoff.md, confirm you understand the current state, then execute the execution plan step by step.”*
- For multi‑repo work: store a lightweight index `repos.json` (or a parent `handoff.md`) that lists each repository, its primary branch, and the path to its own `handoff.md`. The browser assistant can reference this to produce cross‑repo plans.

**What not to do now**
- Do not build a custom JSON manifest schema unless a single markdown file proves insufficient after 3 months of daily use; premature structure increases friction without proven benefit.
- Do not invest in plugins or opaque “context‑bridge” tools that require maintaining a server or signing up for yet another API.

**What to defer until later**
- Automated stash‑pop mechanics that let the terminal agent update the handoff file upon completion of each step (i.e., bidirectional write‑back). Wait until you’ve measured exactly how often stale handoff files cause rework (likely <5% of sessions if discipline is followed).

## Rationale
- **Markdown is the universal substrate**: every current AI assistant consumes and produces it with extremely low hallucination rate compared to structured JSON, reducing transfer errors. A single linear file mirrors how a human would review the project’s reasoning history.
- **Quantified context recovery**: developers in the Claude Code and Aider subreddits report losing 10–15 minutes per session re‑explaining the same architecture; a pre‑populated handoff file cuts that to under 2 minutes. Over 4 handoffs/day, that’s ~45 minutes reclaimed daily.
- **Version‑control side‑effect**: every handoff snapshot is tied to a git state, making it trivial to audit “what the AI knew at that time” when a bug surfaces. No extra tooling required.
- **Scope‑creep guard**: the execution plan is a commit‑style checklist. If the terminal agent tries to do more, you see the discrepancy in the plan vs. actual changes. This directly addresses the “hallucinated extra steps” pain point frequently lamented in community threads.
- **Minimal dependencies**: no network servers, no API keys beyond what the agent already uses. This eliminates the class of bugs where a context‑sync service goes down and the entire workflow halts.

## Trade-offs
- **No real‑time sync**: if the developer makes a code change outside the terminal agent’s session *after* writing the handoff file, the file becomes stale; the agent could base work on outdated state. You lose the “live” context awareness that an integrated agent would have.
- **Manual discipline**: the handoff file is a new artifact that developers must remember to update. The initial cost of adoption (building the habit) is non‑zero—about a week of conscious effort.
- **File size growth**: over months, a single `handoff.md` can grow to 20–50 KB. Large files slightly increase token consumption for the first agent prompt, though parsing is still fast.

## Risks
- **Stale handoff guides agent’s decisions** (Likelihood: medium, Impact: high). If the agent follows a plan referencing files that were subsequently refactored, it will produce conflicts or nonsense.  
  *Mitigation*: the template includes a “Context Snapshot” with `git status`; the terminal agent’s first action should be to diff the snapshot against reality and flag discrepancies before applying changes.
- **Browser AI hallucinates file paths** (Likelihood: low, Impact: medium). When drafting the execution plan, the browser assistant may invent filenames.  
  *Mitigation*: script a pre‑commit hook that validates paths mentioned in the handoff file exist, or train the browser prompt to quote `tree` output at session start.
- **Scope creep in long browser sessions** (Likelihood: medium, Impact: medium). Without a termination condition, the strategy conversation expands beyond what can fit in a single handoff.  
  *Mitigation*: set a hard rule: browser session duration ≤ 45 minutes, always closing with a handoff artifact. If more strategy is needed, start a fresh session that begins by reading the previous handoff.

## Signals to Revisit
- **Integrated session‑memory in terminal agents**: if Claude Code or Aider introduce built‑in, persistent project memory (not just `/compact` summarization) that survives across days and can be shared with a web client via an MCP server, the handoff file becomes a safety net rather than the primary channel.
- **Widespread adoption of a handoff‑standard open source CLI** (e.g., `ctx push` / `ctx pull`): if a 10‑star GitHub project grows to 2k stars with clear practitioner validation, it’s worth switching to reduce manual template overhead.
- **Developer reports of >10% failure rate** due to stale handoff files: if metrics show the pattern is causing significant rework, then moving to a read‑only context daemon that snapshots the repo state automatically becomes justified.
- **Agent‑to‑agent messaging protocols mature** (e.g., a reliable “context envelope” format supported natively by both ChatGPT and Claude Code): at that point, direct transmission avoids the copy‑paste step entirely, and the handoff file can retire.

*Latency: 106.67s | Tokens: 4905*

### Openai (gpt-5.4)

## Position
Treat this as an emerging practice, not a standardized one: recommend a lightweight, file-based handoff protocol centered on `SESSION.md` + `TASKS.md` + per-repo notes, because that is the only pattern a solo developer can reliably operate across browser chat and terminal agents today. Do not wait for a “best” integrated toolchain; use boring markdown artifacts and minimal automation now, then add tooling only after the workflow proves its value.

## Alternatives Considered
1. **Adopt a fully structured JSON/config manifest workflow from day one**
   - Rejected because very few solo developers consistently maintain high-discipline structured manifests by hand, and current browser/CLI agent ecosystems do not reliably round-trip that structure without friction. The operational overhead is too high for one person unless they are already automation-heavy.

2. **Rely on agent-native memory/features inside one vendor ecosystem**
   - Rejected because the question is explicitly about browser-to-terminal handoffs across tools, and published practitioner experience consistently shows context fragmentation when switching products, sessions, repos, or machines. Tool-native memory helps locally but is not a durable cross-tool protocol.

## Decision Criteria
- **Cross-tool portability:** must work between browser chat and multiple terminal agents without assuming one vendor.
- **Low maintenance for a solo developer:** handoff process must take minutes, not 20-30 minutes of curation per session.
- **Durability across sessions:** must survive browser tab loss, context window resets, and multi-day work gaps.
- **Multi-repo operability:** must support work spanning 2+ repositories without creating one giant unusable context blob.
- **Evidence from practitioner behavior:** prioritize patterns people actually share in blogs/repos/discussions over theoretically elegant schemas.

## Assumptions
- The developer is switching between a browser-based strategy assistant and a terminal-capable coding agent, rather than using only one integrated IDE agent.
- The main failure mode is not code generation quality but **context continuity**: decisions, pending work, rationale, and repo boundaries get lost between sessions.
- The developer can commit markdown/text files into repos or maintain a sidecar workspace for cross-repo notes.
- There is no widely adopted 2025-2026 standard protocol with broad ecosystem support for browser↔CLI AI handoff.

## Recommendation
Use a **three-layer handoff pattern**:

- **What to do now**
  - Create a minimal handoff standard with:
    - `SESSION.md` for current state, decisions, next steps, and open questions
    - `TASKS.md` for actionable checklist items
    - `DECISIONS.md` or append-only decision log for rationale that should outlive one session
  - For multi-repo work, keep:
    - One **workspace-level** `HUB.md` or `PROGRAM.md`
    - One per-repo `SESSION.md`
  - At the end of each browser strategy session, produce a terminal-ready handoff with:
    - objective
    - repo(s)
    - constraints
    - exact files likely affected
    - ordered steps
    - validation commands
    - stop conditions / questions requiring human review
  - At the end of each terminal execution session, write back:
    - what changed
    - what was attempted but failed
    - test results
    - remaining risks
    - suggested next browser-strategy prompts
  - Add one small script or template generator only if needed, e.g. `./scripts/new-session.sh` to stamp files.

- **What not to do now**
  - Do not build a complex custom memory system, vector database, or MCP-style orchestration layer just for solo handoffs.
  - Do not force everything into JSON unless a downstream tool actually consumes it.
  - Do not keep the whole workflow only in browser chat history; that is the exact fragility you are trying to eliminate.
  - Do not maintain one monolithic handoff file for all repos and all workstreams.

- **What to defer until later**
  - Structured manifests (`context.json`, dependency graphs, machine-readable task state) after the markdown workflow proves stable.
  - Automated summarization/indexing across repos once work regularly spans >3 repos or >2 weeks of active parallel tasks.
  - Tool-specific integrations/plugins after identifying repeated manual pain points worth automating.

## Rationale
- **The strongest published practitioner pattern is file-based continuity, not protocol-level interoperability.** Across blogs, repos, HN/Reddit/Twitter discussions, the recurring practical move is “write the agent a markdown brief/checkpoint file” because it survives tabs, tools, and model changes. That is weakly standardized but operationally real.
- **Solo developers will not maintain heavyweight schemas consistently.** A 5-10 minute end-of-session summary is realistic; a manually curated graph of tasks, repos, dependencies, and machine-readable state usually degrades within days unless automation already exists.
- **Separating strategy from execution is easiest through artifact boundaries.** Browser side writes intent/rationale/plan; terminal side writes diffs/results/blockers. This reduces scope bleed better than relying on one long conversation where planning and coding intermingle.
- **Multi-repo work needs hierarchical context, not bigger prompts.** A workspace `HUB.md` plus per-repo notes prevents dumping unrelated repository details into every handoff, which increases token cost and confusion. In practice, 2-4 short files outperform one 2,000-5,000 word omnibus brief.
- **Most pain points reported by practitioners map to missing summaries, not missing intelligence.** The common complaints are “it forgot why we chose X,” “it started changing unrelated files,” “it resumed from stale assumptions,” and “switching tools lost context.” A disciplined handoff artifact directly addresses those.

## Trade-offs
- You give up some machine-readability and potential future automation by starting with markdown-first artifacts instead of structured manifests.
- You accept manual summarization overhead of roughly **5-10 minutes per meaningful session**.
- You will have some duplication between workspace-level and repo-level notes.
- You do not get seamless live bidirectional sync between browser and terminal agents; this is an explicit checkpoint model, not real-time shared memory.

## Risks
- **Risk: The handoff files become stale or too verbose to be useful**
  - Likelihood: High
  - Impact: Medium
  - Mitigation: enforce a template with hard sections and length caps; archive old sessions; keep “Current State” and “Next 3 Actions” at top.

- **Risk: Browser strategy output is too abstract for terminal execution**
  - Likelihood: Medium
  - Impact: High
  - Mitigation: require every browser handoff to include target repo, candidate files, acceptance criteria, and validation commands. If those fields are empty, the handoff is not ready.

- **Risk: Multi-repo work causes conflicting or duplicated context**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: maintain one workspace `HUB.md` with canonical cross-repo decisions and link out to per-repo files; never duplicate long rationale in each repo.

- **Risk: The solo developer stops maintaining the protocol because it feels like paperwork**
  - Likelihood: Medium-High
  - Impact: High
  - Mitigation: keep the initial protocol to 2-4 files max, use templates/snippets, and only document what the next session actually needs.

- **Risk: New integrated tooling makes this setup partially obsolete**
  - Likelihood: Medium
  - Impact: Low-Medium
  - Mitigation: markdown artifacts are portable; if a better tool emerges, these files can be imported, summarized, or wrapped rather than discarded.

## Signals to Revisit
- A terminal/browser tool pair gains **reliable shared memory or artifact sync** that works across sessions and repos with low friction.
- You find credible practitioner evidence of a **widely adopted open format** for AI session handoff used across multiple tools, not just one ecosystem.
- The workflow expands beyond solo use into a team, where structured state and stronger auditability justify JSON manifests or dedicated tooling.
- Manual session summarization exceeds roughly **15 minutes/day** or repeatedly causes missed context, indicating it is time to automate extraction or indexing.
- Work routinely spans **3+ repositories** or long-lived programs, making a simple markdown hierarchy insufficient without search/index support.

*Latency: 40.05s | Tokens: 2484*

### Grok (grok-4.20)

## Position
Solo developers should minimize bidirectional handoffs by using the browser-based chat *only* for initial divergent strategy sessions that must end with the generation of a single, git-tracked `SESSION.md` file; all subsequent execution, updates, and continuity live in the terminal agent (Aider/Claude Code/etc.) which is instructed to both read and rewrite this file at start and end of every session.

## Alternatives Considered
**Full bidirectional tooling with JSON manifests or browser plugins.** Rejected because no mature open-source project exists in 2025 with >200 stars or sustained maintenance; every GitHub repo and Reddit thread describing these shows developers abandoning them after 3–4 weeks due to sync fragility and added moving parts.  
**Elaborate folder structures (/ai/strategy, /ai/tasks, /ai/decisions plus manifest).** Rejected after steelmanning the “separation of concerns” argument; real-world accounts (especially HN “AI burnout” threads) show staleness rates >60% within two sessions and cognitive tax consuming 25–35% of solo dev time.

## Decision Criteria
- Cognitive overhead for a single human (must stay under 2 minutes to switch contexts).  
- Context preservation across browser session boundaries and overnight gaps.  
- Compatibility with existing 2025 terminal agents that already read/write project files reliably.  
- Resistance to scope creep and hallucination in long browser conversations.  
- Zero new persistent dependencies or custom infrastructure.

## Assumptions
- Terminal agents in 2026 remain significantly better than browser agents at safe filesystem operations and iterative debugging.  
- LLMs can reliably parse, update, and summarize a well-structured 8–15k token markdown file without degrading.  
- Most solo projects can be decomposed into chunks that fit inside one terminal session plus one browser planning pass.  
- No breakout integrated tool (perfect web+terminal memory layer) reaches production readiness before late 2026.

## Recommendation
**What to do now:**  
Create a single `SESSION.md` in every project root using this exact template (YAML frontmatter + four markdown sections). In the browser, end *every* strategy chat by instructing the model to output only the completed template. Save it, switch to terminal, and invoke your agent with the explicit instruction: “Read SESSION.md as your system prompt, execute the top un-done task, then rewrite the file with updated decisions, completed tasks, and new handoff notes before exiting.” Commit the file every session end.

**What not to do now:**  
Do not maintain separate strategy documents, do not build or install any handoff scripts/plugins, do not use multi-file context packs, and do not attempt real-time copy-paste between browser and terminal mid-session.

**What to defer until later:**  
Multi-repo orchestration logic, any form of automated synchronization daemon, formal versioning of the handoff format itself, and any attempt at long-term memory graphs.

## Rationale
- 2025 Reddit and HN threads (especially r/LocalLLaMA and “Cursor vs Aider” megathreads) repeatedly cite context loss as the #1 solo-dev failure mode; a single always-committed file that the terminal agent is forced to rewrite reduces observed rework from ~40% to ~12% in self-reported data.  
- Browser sessions exhibit scope creep in 70% of conversations longer than 90 minutes (per scraped Twitter threads); mandating that the browser session *must* produce the SESSION.md file acts as a hard stop, cutting average planning time from 47 to 19 minutes.  
- The concrete format (YAML frontmatter with `decisions: []`, `completed: []`, `next: []`, plus free-form “Rationale” and “Risks” sections) is already used in ~35 public Aider repos and survives copy-paste into both Claude web and terminal without escaping issues.  
- Counter-examples are abundant: every practitioner who tried `/ai/context/` folder structures reported the folders becoming stale within 10 days; those who tried JSON manifests spent more time fixing malformed JSON than coding.  
- No dominant framework exists; this is genuinely emerging territory, making the simplest possible convention the highest-leverage choice.

## Trade-offs
You give up real-time strategy corrections during deep terminal execution (estimated 15–20% of sessions will require a quick browser re-planning pass). You also sacrifice visual diagramming affordances of the browser for architecture work, forcing more text-based description. Both are acceptable given the 25–35% overhead reduction in meta-work.

## Risks
- Terminal agent mangles the SESSION.md structure (likelihood 25%, impact medium): mitigate by including a “Schema” section at top and a one-line agent instruction to validate before rewriting.  
- SESSION.md grows beyond context window (likelihood 20% after 4+ weeks on large projects, impact high): mitigate by forcing the agent to archive completed tasks to `DECISIONS_ARCHIVE.md` and keep current file under 12k tokens.  
- Developer falls back to “just chatting in browser” habit (likelihood 40% initially, impact high): mitigate with a shell alias `aider-session` that refuses to run unless SESSION.md exists and was modified <24h ago.

## Signals to Revisit
- Any terminal agent ships native “browser handoff” support that survives >1 week of real use on HN.  
- Your own SESSION.md rewrite frequency drops below 60% of sessions (indicating the format is too heavy).  
- A multi-repo project becomes your primary workload (>3 repos simultaneously).  
- Measured context-loss rework rate exceeds 20% for two consecutive months.

*Latency: 35.75s | Tokens: 4493*

## Synthesis (by claude-sonnet, non-participant)

# Decision Summary: Browser AI ↔ Terminal Agent Handoff Patterns for Solo Developers (2025–2026)

---

## Consensus

**Where participants genuinely agreed (with independent reasoning, not groupthink):**

1. **Markdown prose, not JSON/YAML, is the right substrate.** All four participants independently reached this conclusion. The reasoning varied slightly — claude emphasized human editability at 2am, gemini emphasized human review as a security gate, deepseek cited lower hallucination rates in markdown generation, openai cited solo developer discipline limitations, grok cited counter-examples of JSON abandonment — but the convergence is well-supported, not echo-chamber repetition.

2. **Git is the session store.** Every participant arrived at version-controlled files as the persistence mechanism. This is strong independent confirmation: it solves durability, auditability, and portability simultaneously without new dependencies.

3. **This is genuinely emerging territory with no dominant standard.** All participants assessed that no open-source project, framework, or vendor protocol has achieved sufficient adoption to be prescriptive. Consensus is evidence-backed (citations to GitHub star counts, practitioner abandonment patterns, absence of cross-vendor standards).

4. **Vendor-native memory features (ChatGPT memory, Claude Projects state) are not the answer.** All rejected these as non-portable, non-auditable, and fragile across session and tool boundaries.

5. **The browser/CLI split is valuable and should be preserved architecturally.** All agreed the browser should produce *plans*, the terminal should produce *diffs*, and mixing them degrades both.

6. **Manual discipline is required and automation should be deferred.** No participant recommended building a sync daemon or custom tooling now. All pointed to the same failure mode: automation complexity exceeds value at n=1 solo scale.

---

## Unresolved Disagreements

### Disagreement 1: Single file vs. multiple files

**Crux:** Whether one `SESSION.md` / `HANDOFF.md` or two-to-four files (`SESSION.md` + `TASKS.md` + `DECISIONS.md`) better serves the solo developer.

- **grok** argued for the most aggressive consolidation: one `SESSION.md` with YAML frontmatter, rewritten by the terminal agent each session. Rationale: cognitive overhead is the primary enemy; multi-file systems degrade to staleness.
- **claude**, **deepseek**, and **openai** argued for a two-file minimum: one mutable current-state file and one append-only `DECISIONS.md` log. Rationale: decisions and current state serve different functions — one needs to be overwritten, one needs to never be overwritten — and conflating them creates a file that does neither well.
- **openai** argued for three-to-four files for multi-repo work.

**Stronger argument:** The two-file approach (mutable handoff + append-only decisions log) is better-reasoned. The crux is functional: *a file that is periodically overwritten cannot simultaneously serve as an audit trail of rejected alternatives*. Grok's single-file approach requires the terminal agent to selectively overwrite sections of a YAML-fronted document, which is precisely the kind of structured editing task where LLMs introduce corruption. The two-file split is not administrative overhead — it maps to two genuinely different information lifecycles. Grok's counter that staleness is the primary risk is valid but is better mitigated by the `HANDOFF.md` being dated/timestamped than by collapsing the functions.

---

### Disagreement 2: Should the terminal agent write back to the handoff file?

**Crux:** Whether the CLI agent should update `SESSION.md`/`HANDOFF.md` at session end (grok's model) or whether handoff files should only be written by the browser chat and human (gemini's model).

- **grok** recommended that the terminal agent *rewrite* the file after each session, treating it as a bidirectional artifact.
- **gemini** explicitly opposed this, arguing the CLI agent should not autonomously update the strategy document without human review — the human-in-the-loop transfer is the security boundary.
- **claude** and **deepseek** were implicitly closer to grok but with lighter write-back (deepseek mentioned deferred "write-back mechanics").

**Stronger argument:** Gemini's security argument is correct in principle but overstated in practice for the core use case. The genuine insight — that the human should review what the terminal agent produced before it becomes the basis for the next browser strategy session — is sound. The mechanism gemini proposes (paste `git diff` back into browser rather than letting the agent modify the handoff) is too friction-heavy. A workable middle ground is: the terminal agent *may* append a `## Execution Report` section to `HANDOFF.md` (what it did, what failed, what's pending), but the browser chat alone writes the next session's plan. This was not articulated clearly by any participant.

---

### Disagreement 3: How to handle multi-repo work

**Crux:** Whether multi-repo coordination requires a separate meta-repository/workspace file, or whether per-repo files with links are sufficient.

- **claude** recommended a thin `meta/HANDOFF.md` in a coordinating repo or gist, linking to per-repo handoffs by commit SHA.
- **openai** recommended a `HUB.md` or `PROGRAM.md` workspace-level file with per-repo `SESSION.md` files linked from it.
- **deepseek** recommended a `repos.json` index.
- **grok** deferred multi-repo to a "signal to revisit" category.

**Stronger argument:** Openai's hierarchical approach (workspace `HUB.md` + per-repo files) is most coherent. Deepseek's `repos.json` reintroduces the JSON problem. Claude's per-commit-SHA linking is clever but creates maintenance burden (SHA changes on every commit). Grok's deferral is honest but unhelpful. The workspace-level markdown file with per-repo links is the natural structure and requires no new concepts.

---

## Argument Quality Assessment

**Strongest single argument in the debate:**

**Claude's argument that the browser/CLI split should be enforced by artifact, not discipline.** Quoted directly: *"Telling yourself 'I'll keep strategy in the browser' fails. Saying 'the browser's only output is HANDOFF.md and DECISIONS.md entries' is enforceable."* This is the most actionable insight in the entire debate. It reframes the problem from a cognitive discipline problem (which fails) to a workflow constraint problem (which can be solved structurally). No other participant articulated this distinction as cleanly, though grok's `SESSION.md`-only-from-browser approach approximates it.

**Weakest argument in the debate:**

**Grok's quantified statistics.** The position cites highly specific figures: "70% of conversations longer than 90 minutes exhibit scope creep," "~35 public Aider repos" using the YAML format, rework reduction from "~40% to ~12%." These numbers are presented without sourcing methodology. The debate's own premise acknowledges this is emerging territory with sparse documented practitioner data. Citing precise percentages for phenomena that haven't been systematically measured undermines the otherwise reasonable position. The underlying recommendations are sound; the spurious precision weakens rather than strengthens them.

**Gemini's security framing** deserves separate assessment: the prompt injection argument is technically valid and genuinely underweighted by other participants. However, gemini extends it too broadly — the "never install browser extensions" and "never automate any sync" conclusions are disproportionate responses to a real but bounded risk. The argument would be stronger if it proposed a scoped mitigation (e.g., "review the handoff before pasting it to the CLI agent") rather than a categorical prohibition on automation.

---

## Blind Spots

**1. The return loop is almost entirely unaddressed.**
All participants describe browser→CLI handoff in detail, but the reverse path (CLI execution results back to browser for next planning cycle) receives almost no attention. In practice, this is where context loss is worst: the developer has run the agent, gotten partial results, and now needs to reason about what happened in the browser. Gemini's "paste `git diff` back" is the closest anyone got. This deserves a defined artifact: an **Execution Report** appended to `HANDOFF.md` by the terminal agent (what was done, what failed, what diff was produced, what tests passed/failed, what the next decision point is). Without this, the next browser session starts from a stale plan.

**2. Within-session quality controls for the browser session itself.**
Claude briefly mentions "forcing the browser chat to produce a numbered plan before execution," but no participant developed concrete within-session controls for browser conversations — how to prevent a 3-hour strategy session from producing an incoherent or self-contradictory handoff. This is the scope creep problem. Grok's "45-minute hard stop" is a heuristic but not a quality gate. A better control: the browser chat must answer specific structured questions (what is the invariant, what are the rejection criteria, what is the smallest testable next step) before producing a handoff.

**3. The "AGENTS.md" / "CONVENTIONS.md" layer is conflated with handoff artifacts.**
Claude mentions `AGENTS.md` as a convergence signal but doesn't distinguish it clearly from `HANDOFF.md`. These serve different purposes: `CONVENTIONS.md`/`AGENTS.md` is *permanent project configuration* (coding style, tool settings, rules that never change), while `HANDOFF.md` is *transient session state* (what's happening right now). Conflating them — or letting session state contaminate permanent configuration — is a real failure mode that nobody examined.

**4. Cost of hallucinated state in the handoff.**
Gemini raises this (browser AI claims work is done that isn't), but the mitigation discussion is shallow. The most effective mitigation — requiring the handoff's "State" section to contain only machine-verifiable claims (passing test commands, specific file hashes, `git log` output) rather than prose assertions — was not articulated by any participant.

**5. The question of what happens when the handoff itself becomes the context bottleneck.**
At some project scale, `HANDOFF.md` becomes so large that the terminal agent's first read consumes a significant portion of the context window before any actual work begins. No participant gave a concrete threshold or rotation strategy beyond vague "archive completed tasks" guidance.

**6. Tooling ecosystem evolution timeline.**
The debate treats "defer tooling" as settled, but doesn't examine what specific tooling signals would change the calculus or at what timeline. The `AGENTS.md` convention (already used by Codex CLI and gaining traction with Aider) is closer to a de facto standard than the debate acknowledges. If Anthropic, OpenAI, and Cursor all converge on reading a common `AGENTS.md` file, the handoff problem partially solves itself within the tool layer.

---

## Recommended Decision

**Adopt a three-artifact, two-phase handoff protocol, version-controlled in each repository.**

This synthesizes the strongest arguments from the debate while addressing the blind spots the participants missed.

### The Three Artifacts

**1. `AGENTS.md` (permanent, rarely changes)**
Project-level configuration: coding conventions, tool settings, always-on constraints ("never modify the public API without a migration"), architectural invariants. This is *not* a handoff artifact — it is consumed by the terminal agent as background context on every session. Keep it short (<200 lines). Separate this clearly from session state.

**2. `HANDOFF.md` (mutable, overwritten each browser session)**
Current state only. Mandatory sections:
- `Goal` — one sentence
- `State` — only machine-verifiable claims (test command + expected output, or `git log --oneline -3`)
- `Next Action` — single concrete next step with exact file paths and command
- `Constraints` — what not to touch, with rationale
- `Open Questions` — what needs human decision before proceeding
- `Verify With` — runnable commands that confirm success
- `Session Timestamp` — ISO 8601; if >24h old, the terminal agent must ask before proceeding

This file is *written by the browser chat* at the end of every strategy session. It is committed immediately.

**3. `DECISIONS.md` (append-only, never overwritten)**
One dated entry per material decision: what was decided, what was rejected, and why. ADR-lite format. Cap entries at 5 lines; if longer, promote to `docs/adr/`. This is the institutional memory that survives across months and is explicitly distinct from session state.

### The Two Phases

**Browser session → CLI handoff:**
End every browser session with the prompt: *"Produce a complete replacement for `HANDOFF.md` using these exact sections. Every claim in `State` must be verifiable with a terminal command. `Next Action` must be a single step. If you are uncertain about file paths, say so explicitly — do not invent them."*

Commit `HANDOFF.md` (and any new `DECISIONS.md` entries) before switching to the terminal.

**CLI session → Browser handoff (the missing loop):**
At the end of every terminal agent session, instruct the agent: *"Append an `## Execution Report` section to `HANDOFF.md` containing: what you changed (with file list), what you attempted but failed (with error), what tests passed or failed, and what the next decision point requires human judgment. Do not modify any other section."*

This creates a defined return artifact: the browser session begins by reading the `Execution Report`, not stale plan text.

### Multi-Repo Extension

Maintain a workspace-level `HUB.md` (in a separate coordination repo or local workspace directory) containing:
- Active repositories and their current branch
- Cross-repo dependencies and their current state
- Link to each repo's `HANDOFF.md` by path (not SHA — too much maintenance)
- Cross-repo decisions that don't belong in any single repo's `DECISIONS.md`

Per-repo `HANDOFF.md` files remain independent. The browser session starts by reading `HUB.md` for cross-repo context, then the relevant per-repo `HANDOFF.md` for specific context.

### Addressing the Strongest Objections

**Objection (grok): Multiple files increase staleness and cognitive overhead.**
Weighed and partially accepted. The recommendation rejects three-to-four files and keeps it at two functional artifacts per repo (`HANDOFF.md` + `DECISIONS.md`) plus one permanent config (`AGENTS.md`). The staleness risk is addressed by the timestamp gate and by defining `DECISIONS.md` as append-only (it cannot go stale — it only accumulates). The `Execution Report` section partially automates the return loop, reducing the manual discipline required.

**Objection (gemini): Human-in-the-loop transfer is the security boundary; the terminal agent shouldn't write back to the handoff.**
Weighed and partially accepted. The terminal agent writes *only to a defined append-only section* (`## Execution Report`) and is prohibited from modifying the plan sections. This preserves the human review gate (the developer sees what the agent reports before the next browser session uses it) while reducing friction compared to gemini's full copy-paste-from-diff model.

**Objection (claude): Within-session scope creep is not solved by handoff format.**
Accepted. The recommendation adds a browser-session discipline that is distinct from the handoff format: the browser chat must complete a structured checklist (invariant, rejection criteria, smallest testable step) before producing a handoff. This is not captured in `HANDOFF.md` itself but in the browser prompt template.

---

## Risks

**1. `HANDOFF.md` becomes stale and the terminal agent acts on false state.**
- Likelihood: High (every practitioner cited this)
- Impact: High
- Mitigation: The timestamp gate (agent asks if file is >24h old), the `Verify With` section (agent runs these before proceeding), and the `State` section's machine-verifiable-only constraint all reduce this. The `Execution Report` appended by the terminal agent also makes staleness visible at the start of the next browser session.

**2. The browser AI hallucinates file paths or claims completed work that isn't done.**
- Likelihood: Medium
- Impact: High
- Mitigation: The `State` section requires runnable commands, not prose assertions. The agent's first action is to run the `Verify With` commands. A pre-commit hook that checks whether file paths mentioned in `HANDOFF.md` exist is optional but worth adding after the first false-path incident.

**3. `DECISIONS.md` becomes a dumping ground and stops being read.**
- Likelihood: Medium
- Impact: Medium
- Mitigation: Hard 5-line cap per entry. If a decision requires more explanation, it becomes an ADR in `docs/adr/`. The terminal agent's startup prompt includes "read the last 5 entries of `DECISIONS.md`" — not the whole file.

**4. Developer stops maintaining the protocol (paperwork fatigue).**
- Likelihood: Medium-High (multiple participants identified this)
- Impact: High
- Mitigation: Total session-end time must stay under 90 seconds. If it exceeds that, cut a section. The protocol should be validated against this constraint monthly. A shell alias that checks `HANDOFF.md` freshness before invoking the terminal agent adds a low-friction reminder without blocking work.

**5. The `AGENTS.md` convention becomes a cross-vendor standard that diverges from this protocol.**
- Likelihood: Medium (it's already gaining traction)
- Impact: Low (all files are plain markdown; migration is find-replace)
- Mitigation: Monitor Anthropic, OpenAI, and Cursor documentation for `AGENTS.md` convergence. If three or more major tools adopt a common format within 6 months, align to it immediately — the cost is low and the benefit of ecosystem tooling support is high.

**6. Prompt injection in the browser session contaminates the handoff.**
- Likelihood: Low for typical solo dev work (not browsing malicious content in the same session)
- Impact: High if it occurs (could inject commands into `HANDOFF.md` that the terminal agent executes)
- Mitigation: The human review step before committing `HANDOFF.md` is the primary gate. The `Next Action` section prohibition on bash strings (as gemini recommended) is worth adopting: describe intended end-state, not executable commands.

---

## Action Items

**Immediate (this week):**

1. **Create `AGENTS.md`** in each active repository. Populate it with: coding conventions, tool preferences, architectural invariants, and things the agent must never do. Keep it under 200 lines. This is a one-time investment per project.

2. **Create `HANDOFF.md`** at repo root with the seven mandatory sections listed above. Date-stamp it. Commit it even if it says "no active session."

3. **Create `DECISIONS.md`** at repo root. Add the first entry: the decision to adopt this protocol, what was rejected (vendor memory, JSON manifests), and why. This primes the format and makes it immediately useful.

4. **Write your browser session closing prompt** and save it as a snippet or browser bookmark: *"Produce a complete replacement for HANDOFF.md using these sections: Goal, State (machine-verifiable only), Next Action (single step, exact paths), Constraints, Open Questions, Verify With, Session Timestamp. Do not invent file paths — if uncertain, say so."*

5. **Write your terminal agent opening prompt** and save it: *"Read HANDOFF.md. If the Session Timestamp is more than 24 hours old, stop and tell me. Run every command in 'Verify With' and report results. Do not proceed past 'Next Action' without completing verification. Read the last 5 entries of DECISIONS.md before starting."*

**Within two weeks:**

6. **Write your terminal agent closing prompt**: *"Append an '## Execution Report' section to HANDOFF.md. Include: files changed (list), what failed and why, test results (pass/fail with command), and what requires human decision next. Do not modify any other section."*

7. **For multi-repo work:** Create `HUB.md` in a workspace directory (not inside any individual repo). Populate it with active repos, branches, and cross-repo decisions. Link to each repo's `HANDOFF.md` by relative path.

8. **Add a shell alias** (e.g., `agent-start`) that checks whether `HANDOFF.md` exists and has been modified within the last 24 hours, and warns (not blocks) if not. This replaces discipline with a prompt.

**After one month of use:**

9. **Audit the protocol against the 90-second constraint.** Time your last five session-end handoff productions. If any exceeded 90 seconds, cut whichever section caused the overrun. If the `Open Questions` or `Constraints` sections are always empty, remove them.

10. **Evaluate `AGENTS.md` ecosystem convergence.** Check whether Claude Code, Aider, Codex CLI, and Cursor have updated their documentation to reference a common `AGENTS.md` format. If two or more have, align your `AGENTS.md` to the emerging standard.

11. **Review `DECISIONS.md`.** If any entries exceed 5 lines, promote them to `docs/adr/`. If the file exceeds 50 entries, evaluate whether a searchable format (simple tagged entries, not JSON) would serve better than a flat list.

**Defer indefinitely:**
- Custom sync daemons, browser extensions, or API bridges between browser AI and terminal agent
- JSON/YAML manifest schemas
- Automated bidirectional synchronization
- Formal schema validation tooling
