> **What was asked:** portable cross-vendor agent-instruction layers (AGENTS.md as canonical), prompt/instruction distillation with measured compression, and unattended night-agent runs -- what is a real standard, what compresses without losing rule-adherence, and what should be a mechanism rather than prose
> **Provenance:** BROWSER-PRODUCED external research, commissioned and landed 2026-08-17 from `compass_artifact_wf-50111a08-00b6-5e12-b6e0-a27951ea51b8_text_markdown.md`. Body is a BYTE-FAITHFUL copy of the source artifact -- this header is the only addition. Home derived per ADR-101 section 1 Tier-2 (`archive/` is in `SANCTIONED_GENRES`) + ADR-60 (`docs/archive/` = pending-classification holding zone); the ADR-101 Rule B audit-class enum has no class for an external research memo. Derivation recorded in full at `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` section 2.
> **EXTERNAL EVIDENCE -- ADVISORY UNTIL RATIFIED. THIS DOCUMENT BINDS NOTHING.** It is not doctrine, not an ADR, not a ruling, and not this repo's own audit evidence. Nothing here becomes binding by virtue of having landed in the tree. Its ratification channel is the intake spine (`docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md`, currently `status: DRAFT`) -- DRAFT -> READY -> ACCEPTED, per `docs/intake/README.md` section 5.

# Portable Agent-Instruction Layers, Prompt Distillation, and Night-Agent Runs: A Buildable Field Guide (August 2026)

## TL;DR
- **Build on AGENTS.md as your one canonical instruction file** — an open standard stewarded by the Linux Foundation's Agentic AI Foundation, "read natively by Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, Zed, Factory, Jules, and over 20 other tools… adopted by more than 60,000 repositories." Keep it under ~30 always-on lines and make every other vendor file (CLAUDE.md, GEMINI.md, copilot-instructions) a generated or pointer file to it — a "lane-role → model" swap then becomes a one-table edit plus a regenerate step, not a rewrite.
- **Distillation is real and measured** (LLMLingua reaches up to 20× compression with GSM8K Exact-Match dropping only 1.44 and 1.52 points at 14× and 20×; Anthropic Agent Skills load ~80–100 tokens/skill until activated), but the durable win is moving hard rules OUT of prose into mechanisms (hooks, linters, tests, CI gates) — instruction-following measurably degrades under load (Distyl AI's IFScale: "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions"), so a prompt should carry judgment, not enforceable invariants.
- **Unattended runs are buildable this week** with Claude Code headless (`claude -p`), the official `anthropics/claude-code-action@v1` on cron, and git worktrees for isolation; 3–6 concurrent agents is the real (review-bound) sweet spot, and moving off a Windows laptop onto GitHub Codespaces ("compute fees starting at $0.18/hr and storage fees at $0.07/GB per month") or a rented VPS is cheap — the gotchas are locking, secret handling, and pinned toolchains, not price.

## Key Findings

**AGENTS.md is now the closest thing to a real cross-vendor standard, but it is a convention, not a rigid schema.** It emerged in August 2025 from OpenAI Codex, Amp, Google Jules, Cursor, and Factory; was donated to the Linux Foundation's Agentic AI Foundation (AAIF) in December 2025; and by mid-2026 is used in 60,000+ repos and read by 20–30+ tools. It is just Markdown with no required fields. The official conflict rule: **the closest AGENTS.md to the edited file wins; explicit user prompts override everything.**

**Every major agent still reads a *different* default file — this is the core portability problem.** Claude Code reads CLAUDE.md (not AGENTS.md natively — issue #6235 "Feature Request: Support AGENTS.md," opened by DylanLIiii on Aug 21, 2025, has 5,200+ reactions and 300+ comments and remains open with no roadmap signal as of Claude Code 2.1.201, with Anthropic having declined native support). Codex reads AGENTS.md. Gemini CLI reads GEMINI.md (but can be pointed at AGENTS.md). Copilot reads `.github/copilot-instructions.md` plus path-scoped `*.instructions.md`. Cursor reads `.cursor/rules/*.mdc` but its CLI also reads AGENTS.md and CLAUDE.md.

**The winning multi-vendor pattern is "one source + thin per-vendor pointers," and real tooling exists to do it** — symlinks, `@import`, Gemini's `context.fileName` setting, and generator CLIs like rulesync and ai-rules-sync/agentsync.

**Distillation techniques are measured mostly on QA/reasoning benchmarks, not on "did the agent still obey the rule."** You must close that gap yourself with a small eval harness (promptfoo).

**Night agents are a solved-enough problem** with headless mode + Actions + worktrees, plus a growing set of purpose-built orchestrators (amux, Cyrus, container-use, Conductor, Vibe Kanban).

## Details

### QUESTION 1 — The Portable Agent-Instruction Layer

#### 1(a) Status of AGENTS.md as a standard

**VERIFIED (vendor/primary):**
- **Origin & governance.** agents.md states it "emerged from collaborative efforts across the AI software development ecosystem, including OpenAI Codex, Amp, Jules from Google, Cursor, and Factory" and "is now stewarded by the Agentic AI Foundation under the Linux Foundation." Formalized August 2025; donated to AAIF December 2025.
- **No formal schema.** Official FAQ: "Are there required fields? No. AGENTS.md is just standard Markdown." Recommended sections: project overview, setup/build commands, code style, testing instructions, security considerations, PR/commit rules.
- **Nesting/conflict.** Official: "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." Monorepo pattern is nested files (OpenAI's own main repo has 88 AGENTS.md files).
- **Officially-listed readers** (on agents.md's own supported-agents list): Codex (OpenAI), Jules (Google), Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin (Cognition), UiPath, Junie (JetBrains), Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot coding agent, Ona, Windsurf, Augment Code. (One tracker notes only nine are on a strict LF list — Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, VS Code — and treats Claude Code/Windsurf as "reported.")
- **Claude Code.** Anthropic docs still center CLAUDE.md; native AGENTS.md read is not shipped (issue #6235 open, Anthropic declined). Some secondary sources claim a fallback read; treat native support as NOT vendor-confirmed. The reliable workaround is a one-line `@AGENTS.md` import inside CLAUDE.md, or a symlink.
- **Gemini CLI.** Official docs: default context file is GEMINI.md; set `context.fileName` in `.gemini/settings.json` to `"AGENTS.md"` (or a list) to read it directly. Supports `@file.md` imports and `/memory show|refresh`.
- **Codex.** Official OpenAI docs: reads `~/.codex/AGENTS.md` (global) + repo-root + cwd, concatenated root→leaf; cwd wins conflicts; **32 KiB cap** (`project_doc_max_bytes`), truncates silently beyond it; `project_doc_fallback_filenames` can add CLAUDE.md/CONTRIBUTING.md; `AGENTS.override.md` replaces (not extends) at a level.
- **Copilot.** Official GitHub docs: `.github/copilot-instructions.md` (repo-wide) + `.github/instructions/NAME.instructions.md` with `applyTo` glob frontmatter (path-scoped). Copilot CLI discovers files at repo root, cwd, intermediate and nested dirs; combines and de-dupes but "does not define a general precedence order."

**Competing/overlapping standards:**
- **CLAUDE.md** (Claude Code native; three-level memory + `@` imports + `.claude/rules/` with `paths:` frontmatter).
- **.cursorrules** (legacy) → **.cursor/rules/*.mdc** (glob-scoped).
- **.github/copilot-instructions.md** + **.instructions.md** (Copilot).
- **GEMINI.md** (Gemini CLI).
- **Kiro steering files** (Kiro IDE; a rulesync target).
- **GitHub Spec Kit** — spec-driven-development toolkit that itself ships an AGENTS.md documenting agent integration.
- **Agent Skills / SKILL.md** (Anthropic open standard, Dec 18 2025; adopted by Codex, Gemini CLI, Cursor, VS Code, Copilot via `.github/skills` and `.claude/skills`) — progressive-disclosure instruction delivery.
- **MCP-based instruction delivery** — instructions/tools surfaced via MCP servers rather than files.

**Default-file + precedence cheat sheet (VERIFIED from vendor docs unless noted):**
- **Claude Code:** `~/.claude/CLAUDE.md` (user) → repo `CLAUDE.md` (walk up, concatenated) → subdir `CLAUDE.md`; managed/enterprise policy > project > user for *settings*; for memory files, later-read (closer) wins as a soft weighting, not strict override. Keep main file <~200 lines.
- **Codex:** `AGENTS.override.md` > `AGENTS.md` > fallback filenames at each level; global `~/.codex/AGENTS.md` → root → cwd; 32 KiB combined cap.
- **Gemini CLI:** global `~/.gemini/GEMINI.md` → project (walk up) → subdirs (scan down), all concatenated; filename configurable.
- **Copilot:** repo-wide + path-scoped `applyTo`; no defined precedence between them (combined, de-duped).

#### 1(b) Layering across scopes, size limits, and what happens past them

- **Scopes that actually exist:** user/global (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`), repo-root, subdirectory (nearest-file-wins), and session/task (Claude `--append-system-prompt`, Codex `AGENTS.override.md`, chat prompts).
- **Conflict resolution differs by tool** and is the biggest portability trap: Codex = later/closer file wins on concatenation; Claude Code = concatenated with soft "closer wins" weighting (NOT strict override) — Anthropic's own guidance is that non-contradictory rules matter more than relying on load order; Copilot = no defined precedence.
- **Measured/stated size limits:** Codex hard-caps combined instructions at **32 KiB** and *truncates silently* past it (raise via `project_doc_max_bytes`, or split by directory — the durable fix). Claude Code guidance: keep main CLAUDE.md **<200 lines**; MEMORY.md auto-memory capped at 200 lines, topic files ~120 lines. AGENTS.md guidance: **~20–30 line root file** — and per research cited in Morph's AGENTS.md spec guide, "LLM-generated AGENTS.md files reduced success rates by 2% and increased cost by 23%, primarily because they duplicated content already available in the repository." Gemini has no hard cap but concatenates everything each prompt.
- **What happens when exceeded:** silent truncation (Codex), context-window pressure compacting away/ignoring older instructions (Claude Code), and measured instruction-following degradation (see 2c).

#### 1(c) One corpus, many vendors — concrete patterns and REAL tooling

Ordered simplest → most robust:

1. **Symlinks** (zero-dependency, Unix): `ln -s AGENTS.md CLAUDE.md; ln -s AGENTS.md GEMINI.md`. Tradeoff: **breaks on Windows without Developer Mode/admin** — a real problem for a Windows-laptop operator. `.claude/rules/` supports symlinks and detects circular links.
2. **Import/pointer file** (the Anthropic-documented method): a one-line `CLAUDE.md` containing `@AGENTS.md`. No drift, Windows-safe, and you can add Claude-only rules below the import. Gemini equivalent: `context.fileName: "AGENTS.md"` in `.gemini/settings.json`. Aider: `read: AGENTS.md` in `.aider.conf.yml`.
3. **Generator CLIs from a single source (REAL, with links):**
   - **rulesync** (github.com/dyoshikawa/rulesync) — Node CLI; keep unified rules in `.rulesync/`; `rulesync generate` emits CLAUDE.md, `.cursor/rules`, `.github/instructions`, GEMINI.md, Kiro, etc. for 20+ tools; also `import` and `convert`. Covers rules/ignore/mcp/commands/subagents/skills.
   - **ai-rules-sync / agentsync** (github.com/PanisHandsome/ai-rules-sync) — zero-dependency; `agentsync sync --check` exits non-zero in CI if targets drift from AGENTS.md; also `lint` for stale commands/missing paths.
   - **amtiYo/agents** (github.com/amtiYo/agents) — `.agents/` single source syncing MCP servers, skills, and instructions across Codex, Claude Code, Gemini CLI, Cursor, Copilot; splits secrets (placeholders committed, real values gitignored); bridges `.claude/skills → .agents/skills`.
   - **Agent Smith** (Mac App Store) — GUI exporting AGENTS.md/CLAUDE.md/GEMINI.md from one master brief. Mac-only.
4. **Build-time templating / shared package** — publish conventions as an internal npm package consumed via workspaces, or a build-output/mirror repo (Symfony's subtree-split is the canonical production case: develop in one repo, CI pushes read-only mirrors on each push).

**Recommendation:** Use **AGENTS.md as canonical + `@import`/`context.fileName` pointers** as the day-one default (Windows-safe, no build step). Add **rulesync or agentsync with a `--check` CI gate** the moment you have >2 vendors or >1 repo — the only way to make "regenerate on change" enforceable rather than aspirational.

#### 1(d) Per-repo vs fleet-wide governance across many repos

- **Shared config package + pull-based distribution:** rulesync/ai-rules-sync run in CI or `postinstall` so every checkout regenerates current rules; keeps files identical across repos.
- **Drift detection:** The strongest documented pattern comes from Nx — **Nx Sync Generators** (fail-fast when local config diverges from source of truth), **Nx Conformance** (global rules all repos must follow, failing PRs with clear errors), and **Nx Migrations** (automated codemods to roll breaking changes across repos). For polyrepo, a hand-rolled sync script + drift audit is the documented reality (e.g., the Antigravity multi-repo governance write-up: a canonical AGENTS.md distributed to N repos with a scheduled drift audit).
- **Onboarding a new repo:** template repositories (GitHub) to scaffold instructions; Copilot's own onboarding prompt ("onboard this repository… add `.github/copilot-instructions.md`… no longer than 2 pages, not task-specific") is a reusable pattern.
- **Enforcement:** CI `--check` from your generator; pre-commit hooks; a conformance job that fails when AGENTS.md is missing/oversized or generated files are stale.

**Recommendation:** Model your methodology-hub repo as the single source, publish rules via rulesync, and add an **Nx-style conformance/`--check` job** to every repo's CI. Drift becomes a red build, not a discovery six weeks later.

### QUESTION 2 — Prompt / Instruction Distillation

#### 2(a) Measured compression techniques

- **LLMLingua family (Microsoft Research):** LLMLingua (EMNLP 2023, arXiv 2310.05736) "allows for up to 20x compression with little performance loss" — GSM8K Exact-Match drops only **1.44 and 1.52 points at 14× and 20×** respectively. LongLLMLingua reports up to **+21.4% performance with fewer tokens** on long-context (NaturalQuestions/LongBench) via question-aware compression. LLMLingua-2 (BERT-size token-classification via GPT-4 data distillation) is task-agnostic, cutting end-to-end latency up to **2.9× at 2–5× compression**. A third-party summary: 2–5× on instruction prompts, 5–20× on RAG context, under ~2% quality drop on CoQA/HotpotQA/TriviaQA. **Caveat:** gains are task-dependent (best on reasoning/RAG, weaker on conversational/summarization), and these are QA/reasoning benchmarks, not "did the coding agent still obey the rule."
- **Progressive disclosure / lazy loading (Anthropic Agent Skills, open standard Dec 18 2025):** three tiers — discovery (~80–100 tokens/skill: name+description at startup), activation (full SKILL.md body, recommended <5,000 tokens), execution (referenced files/scripts on demand). Measured footprint across Anthropic's 17 official skills: body size ~275→~8,000 tokens, median ~2,000. This is the most directly applicable technique for a lane system: keep the always-on layer tiny, push everything conditional into skills.
- **Context pruning / retrieval-based delivery:** perplexity-based token dropping (LLMLingua), chunk-then-token (LongLLMLingua), and RAG-style instruction retrieval; EFPC reports outperforming LLMLingua-2 by ~20–40% at 5× on some LongBench splits.

#### 2(b) Testing that a distilled set still enforces what the original did

- **promptfoo (MIT, ~22–23k stars, ~1.2M monthly npm downloads; v0.121.15 released June 5 2026)** is the solo-operator answer: declarative `promptfooconfig.yaml`, deterministic assertions (`is-json`, `contains`, regex, `javascript`) + model-graded assertions, side-by-side matrix of prompt versions, CLI exit codes for CI, and a GitHub Actions gate that fails the build when quality drops below a threshold. Also does red-teaming.
- **Practical solo pattern (buildable):** (1) build a small **seeded-defect corpus** — inputs where the original instructions produced a known-correct behavior (e.g., "refuses to push to main," "adds a test"); (2) encode each as a promptfoo assertion; (3) run original vs distilled side-by-side; (4) require a threshold (~95%) rather than 100% because model-graded checks are non-deterministic/flaky; (5) gate merges on it. Alternatives named in the ecosystem: DeepEval (pytest-native, 20+ metrics, Python), Braintrust (teams/dashboards), Ragas (RAG), Phoenix (observability).
- **Versioning/diffing:** treat prompts as code (files in git), diff versions in the promptfoo matrix, keep the eval report as release evidence.

#### 2(c) Prose vs mechanism — what should NOT live in a prompt

**Empirical basis that long/dense instructions degrade:**
- **IFScale (Distyl AI, arXiv 2507.11538, NeurIPS 2025):** measured instruction-following as required instructions scale **10→500** — "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions." Three degradation patterns: threshold decay (reasoning models like o3, gemini-2.5-pro hold then fall), linear decay (gpt-4.1, claude-sonnet-4), exponential decay (gpt-4o, llama-4-scout).
- **LIFBench (ACL 2025, arXiv 2411.07037):** 2,766 instructions, 11 tasks, 20 LLMs across six length intervals — instruction-following and *stability* degrade as context length grows; complexity + length compound.
- **LongGenBench / "lost-in-the-middle":** severe loss of adherence for complex (range/periodic) instruction sets in long generation; single-step instructions degrade less.

**Practical rule (established practice, not a single vendor claim):** rules that are **deterministic, safety-critical, or verifiable** should be **mechanisms, not prose** — git hooks/branch protection (never push to main), linters/formatters (style), type checks, tests and CI gates (the invariant), and `allowedTools`/permission modes (capability limits). Prose should carry **judgment, context, and taste** that cannot be mechanized. This is why AGENTS.md's README-duplication penalty ("reduced success rates by 2% and increased cost by 23%") and Codex's "split instructions rather than raise the cap" guidance point the same way: shrink the always-on prose, mechanize the invariants.

### QUESTION 3 — Unattended / Night Agent Runs

#### 3(a) How unattended multi-agent runs actually work today

**VERIFIED (vendor):**
- **Claude Code headless (`claude -p` / `--print`)** runs the full agent loop non-interactively, prints result, exits. Supports `--output-format text|json|stream-json` (parse with `jq`), reads stdin, and pre-approves tools with `--allowedTools` / `--permission-mode` so runs never block. Note the **resume-dialog stall** trap: a prior session in the dir triggers an interactive "resume?" prompt with no timeout — pre-pipe `echo "1" | claude -p …` or use a control plane that auto-answers.
- **`anthropics/claude-code-action@v1` (GA early 2026)** — official GitHub Action; runs on a GitHub-hosted runner via the Claude Agent SDK; two auto-detected modes (interactive `@claude` mention; automation via workflow prompt). **Scheduled runs via `cron`** work (e.g., `on: schedule: - cron: "0 7 * * 1-5"`). Guardrails: write-access + human-actor checks (scheduled runs are attributed to the last user who edited the cron; list bots in `allowed_bots`), `timeout-minutes`, `--max-turns` (default 10). **Billing:** as of the June 16 2026 support note, `claude -p`/Agent SDK/Actions usage still draws from your subscription limits (the planned June 15 split into a separate credit pool was paused) — for predictable pay-as-you-go, use an API key at standard rates.
- **Codex cloud tasks** (developers.openai.com/codex/cloud) — "Run tasks in isolated cloud environments, work in parallel, and start work from the web, GitHub, Linear, or Slack." Each task in its own sandbox preloaded with the repo. `codex cloud exec --attempts N` submits N parallel candidates. Third-party guides report Plus ≈1 concurrent task / Pro ≈3, daily quotas resetting midnight UTC, and a ~5× credit premium vs local — treat those specific numbers as unofficial.
- **Claude Code on the web / cloud sessions** (code.claude.com/docs; anthropic.com/news) — Anthropic-managed cloud infra, "run multiple tasks in parallel across different repositories," each in an isolated environment, persists after browser close, monitor from mobile. Terminal: `claude --cloud "task"`, `--teleport` to pull local, `/tasks` to monitor. Vendor note: "Running multiple tasks in parallel consumes more rate limits proportionately."

**Purpose-built orchestrators (exist, with links; mostly single-vendor/community docs — flag accordingly):**
- **amux** (github.com/mixpeek/amux; amux.io) — open-source (MIT + Commons Clause) self-hosted control plane by Mixpeek for dozens of parallel headless sessions over tmux, with web dashboard/iOS/CLI. **Correction to a circulating claim: it is a single Python file (requires Python 3.10+, tmux 3.2+), NOT a "single Rust binary"** — the README says "Single file — one Python file with inline HTML/CSS/JS." Confirmed features: **atomic task claiming (SQLite CAS)** (`POST /api/board/PROJ-5/claim`), fleet-wide auto-answer of the `/rate-limit-options` and resume dialogs (watchdog presses "1," parses reset time, auto-resumes), YOLO auto-approve for overnight runs, cron-style scheduler, git-conflict detection/isolation, `AMUX_RATE_LIMIT_MODE` (capped default = 3 auto-resumes/session/UTC day). Security: no built-in auth — bind to localhost / Tailscale, never expose the port.
- **Cyrus** (github.com/cyrusagents/cyrus, "backgroundclaude") — watches Linear/GitHub/GitLab/Slack issues, spins an isolated worktree per issue; supports Claude Code, Codex, Cursor, Gemini.
- **container-use** (github.com/dagger/container-use) — Dagger MCP server/CLI giving each agent an isolated container on its own `container-use/<env>` branch; "Run multiple agents on different tasks simultaneously, and they won't conflict."
- **Conductor** (conductor.build, Mac-only), **Vibe Kanban** (vibekanban.com — now community-maintained/sunsetting), **Sculptor** (Imbue, local Docker), **OpenHands** (self-hostable), **Claude Squad** (TUI). Aggregated lists: github.com/andyrewlee/awesome-agent-orchestrators.

**Mechanics:** dispatch by issue/task queue (Kanban with atomic claim), branch/worktree per task, collect via PRs + structured JSON output, surface failures via exit codes/stop reason (never text parsing) and dashboard/mobile notifications.

#### 3(b) Isolation & safety patterns

- **Git worktrees** are the best cost-to-isolation ratio for code-only parallel work: each worktree has private HEAD/index/working dir sharing one object store, so uncommitted edits don't collide and `.git/index.lock` contention disappears — but **conflicts move to the PR/merge stage**, they don't vanish. Known trap: **parallel `git worktree add` races on `.git/config.lock`** (Claude Code issues #34645, #47266) — serialize creation or add retry/backoff.
- **Containers / ephemeral VMs** when you need runtime/dependency isolation (container-use, Sculptor's Docker, a 32 GB cloud VM). Containers are also the only safe place for `--dangerously-skip-permissions`.
- **Branch protection / never-push-to-main** = a mechanism, not a prompt: GitHub branch protection + `--allowedTools` allowlist + require PRs.
- **Secret handling:** pass `ANTHROPIC_API_KEY`/tokens as env/CI secrets, never bake into images; split committed placeholders vs gitignored real values (amtiYo/agents pattern); the Action's write-access + human-actor checks prevent fork/loop abuse.
- **Single-flight / locking:** atomic task claiming (amux SQLite CAS) so two agents never grab the same task; per-worktree MCP server instances for stateful servers; WIP/board guards.

#### 3(c) Economics of moving off a Windows laptop to cloud/rented compute for 8–32 agents

**VERIFIED current pricing:**
- **GitHub Codespaces:** GitHub's official pricing page confirms "compute fees starting at $0.18/hr and storage fees at $0.07/GB per month." The **$0.18 rate is per core-hour** and constant regardless of machine size, so a 2-core = $0.36/hr, 16-core = $2.88/hr, 32-core = $5.76/hr. The GitHub Free personal plan "includes 120 core-hours and 15 GB-months of storage per month." Billed per active minute; stopped = storage only; auto-suspends after inactivity (default 30 min). Prebuilds cut startup time.
- **Hetzner Cloud (cheapest credible rented compute) — PRICING RECENTLY ROSE SHARPLY.** Shared vCPU still starts low (~€3.79–7.99/mo; CPX22 2 vCPU/4 GB rose to €7.99/mo on April 1 2026). But **Hetzner's June 15 2026 repricing raised the CCX dedicated-vCPU lines 113–169%**: e.g., CCX63 jumped from €374.49 to **€853.49/mo (+127.9%)**, and US CCX13 rose from $19.99 to **$50.99/mo (+155%)** (Hetzner official price-adjustment notice, via WZ-IT and PrivateDevOps). Dedicated vCPU is still far cheaper than hyperscalers, but the "€12.49 dedicated / €1.37/hr CCX63" figures circulating in older guides are now stale — reconfirm on Hetzner's selector before budgeting. Shared vCPU remains the value tier for agent lanes; hourly billing with a monthly cap makes burst use cheap.
- **GitHub Actions runners** for stateless one-shot jobs (billed in Actions minutes); good for GitHub-centric work, not a long-lived fleet.

**Practical concurrency (real-world, mostly third-party):** the review bottleneck, not compute, is the ceiling — **3–6 concurrent agents is the repeated sweet spot** (Codex guidance "3–5"; six a "soft ceiling"; Claude Code desktop "4–6"). Hardware rule of thumb: ~6–8 agents on 16 GB, 15–20 on a 32 GB VM; beyond that, distribute across hosts. Rate limits bind before hardware if you use a subscription: parallel Claude sessions share one account's 5-hour/weekly bucket — use an API key for 5+ agents / overnight bursts.

**Operational gotchas:** pinned toolchains (per-worktree `dotnet restore`/`npm ci`, pinned Node/CLI in the image); shallow clones for speed but beware missing history for agents that diff against main; hook arming (worktree-create hooks, resume-dialog auto-answer, `CC_AUTO_CONTINUE`); VS Code remote/control-plane surfaces (Codespaces, Claude Code Remote Control, cloud sessions) as the way you supervise from a phone; and the Codespaces idle-suspend/storage-billing model so stopped envs don't quietly accrue cost.

## Recommendations

**Stage 1 — This week (portability spine):**
1. Make **AGENTS.md the canonical file** in your methodology hub and every repo; keep the root file ≤~30 lines of always-on rules, push everything conditional into Skills (`SKILL.md`) and path-scoped rules.
2. Add per-vendor **pointers, not copies**: `CLAUDE.md` = `@AGENTS.md`; `.gemini/settings.json` `context.fileName: ["AGENTS.md"]`; `.aider.conf.yml` `read: AGENTS.md`; keep your existing `~/.codex/AGENTS.md` reviewer config. Avoid raw symlinks because your laptop is Windows.
3. Encode "lane roles" (producer/reviewer/adversarial/fan-out) as a **small table mapping role → model → tool-config**, with the *instructions* identical across lanes (from AGENTS.md) and only the model/flags swapped. That table is your one-edit swap surface.

**Stage 2 — Next (enforcement & distillation):**
4. Adopt **rulesync** (or agentsync) with a **CI `--check` gate** so generated vendor files can't drift; add an **Nx-style conformance job** per repo (fail build if AGENTS.md missing/oversized).
5. Stand up **promptfoo** with a **seeded-defect corpus** (10–30 cases encoding your non-negotiables) and gate merges at a ~95% threshold; run original-vs-distilled side-by-side before you trust any compression.
6. **Mechanize the invariants:** branch protection + `--allowedTools` allowlists + linters/tests in CI. Anything safety-critical leaves the prose.

**Stage 3 — Then (night fleet):**
7. Start with **`anthropics/claude-code-action@v1` on cron** for scheduled stateless jobs; use **`claude -p --output-format json`** in scripts for anything custom.
8. Introduce **git worktrees** with serialized creation (retry/backoff to dodge the `.git/config.lock` race), one branch per task, PRs as the collection mechanism.
9. When you exceed ~3–4 parallel lanes or want overnight autonomy, run a **control plane (amux)** on a **Hetzner shared/dedicated-vCPU VPS** or **Codespaces**, bound to localhost/Tailscale, with API-key auth (not subscription) and atomic task claiming.

**Thresholds that change the plan:** if you routinely need >6 concurrent productive agents, the bottleneck is human review — invest in fan-out/reviewer automation before more compute. If Codex-cloud/Claude-cloud concurrency limits or subscription rate caps throttle you, switch those lanes to API-key billing. If instruction files creep past ~30 lines always-on (or Codex's 32 KiB), split into Skills before adding compute.

## Caveats
- **Adoption counts and tool lists are largely from secondary guide sites,** anchored to the primary agents.md supported-agents list and vendor docs. The "20–30+ tools / 60,000+ repos" figures are widely repeated but vendor-attributed only loosely.
- **Claude Code native AGENTS.md support is NOT vendor-confirmed;** issue #6235 remains open with Anthropic having declined native support as of Claude Code 2.1.201. Build on the documented `@import`/symlink workaround.
- **Distillation benchmarks measure QA/reasoning/summarization, not agent rule-adherence.** Do not assume a 20× LLMLingua ratio transfers to "the agent still refuses to push to main." Your own eval is mandatory.
- **Concurrency "sweet spot" numbers (3–6), RAM-to-agent ratios, and Codex Plus=1/Pro=3 concurrency are third-party**, not vendor-published; verify against your own account limits.
- **Pricing moves fast:** Hetzner raised shared-plan prices April 1 2026 and dedicated CCX prices 113–169% on June 15 2026; Codespaces rates and Anthropic's billing model (the paused June 15 2026 credit-pool split) can change — reconfirm on the vendors' own selectors before committing budget.
- **amux is Python, not Rust** (correcting a claim in one of its own blog posts); it has no built-in auth.
- Several orchestrators are **early or sunsetting** (Vibe Kanban community-maintained; Terragon shut down) — treat the orchestrator layer as fast-moving.

## The Smallest First Build
- **Q1 (portable layer):** In your hub repo, write one **AGENTS.md** (≤30 lines: build/test commands, boundaries, PR rules) + a one-line **`CLAUDE.md` = `@AGENTS.md`** + a **`.gemini/settings.json`** with `context.fileName: ["AGENTS.md"]`. That single trio makes Claude Code, Codex, and Gemini read the same rules today, Windows-safe.
- **Q2 (distillation):** A **10-case `promptfooconfig.yaml`** encoding your non-negotiable behaviors, run as `npx promptfoo eval` original-vs-distilled with a ~95% pass gate — the minimum that proves a shorter instruction set still enforces the rules.
- **Q3 (night run):** One **`.github/workflows/nightly.yml`** using `anthropics/claude-code-action@v1` on `cron`, with a scoped `--allowedTools`, `timeout-minutes`, and branch protection on `main` — one scheduled, guard-railed, unattended agent run you can watch succeed before you scale to a worktree fleet.