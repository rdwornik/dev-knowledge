# Multi-Provider Portability for AI Coding Agents on One Repository: A Decision-Ready Architect's Report (2026)

## TL;DR
- **The portability bet is defensible but narrow: a single canonical AGENTS.md now travels natively across almost every major tool EXCEPT Claude Code, which still reads only CLAUDE.md — so the instruction-file layer ports cleanly, but everything richer (slash commands, hooks, subagents, permissions, skills) must be re-authored per tool.** MCP is the one deep component with a genuine cross-tool standard; slash commands and hooks are not.
- **The recommended shape works: one canonical `AGENTS.md`, a thin `CLAUDE.md` that does `@AGENTS.md` (Claude Code's import), Gemini pointed at AGENTS.md via `settings.json`, and a generation-plus-checksum drift guard in CI. Avoid symlinks as the primary mechanism on your Windows + git-bash fleet — they degrade to plain-text stub files when `core.symlinks=false`.** Prefer a generation build step with a CI drift check over symlinks or hand-duplication.
- **A Claude Code → Kimi swap is real and cheap to wire (env-var base-URL override) but carries documented breakage (prompt caching, WebFetch, tool-name mangling) and a ToS landmine: pointing Claude Code at Kimi via a Moonshot API key is fine, but routing a Claude Pro/Max subscription through any third-party harness violates Anthropic's Consumer Terms.** Treat the swap as a validated fallback, not a daily driver.

## Key Findings

1. **AGENTS.md is now a real, foundation-governed standard.** Created by OpenAI with Google, Cursor, Factory, Sourcegraph and Amp in August 2025; contributed to the Linux Foundation's new Agentic AI Foundation (AAIF) on December 9, 2025, alongside Anthropic's MCP and Block's Goose. More than 60,000 open-source projects use it; 20–30+ tools read it. It mandates almost nothing — plain Markdown, no schema, nearest-file-wins precedence, explicit user prompts override.
2. **Claude Code is the portability exception.** As of mid-2026 Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The idiomatic fix is a one-line `@AGENTS.md` import inside CLAUDE.md (imports resolve up to 4 hops deep). This is contested online — several blogs claim native fallback; Anthropic's own docs say flatly "Claude Code reads CLAUDE.md, not AGENTS.md."
3. **MCP is the only deep cross-tool standard.** MCP *servers* are interchangeable; the *config files* are not (Claude `.mcp.json` JSON, Codex `config.toml` TOML tables, Cursor/Copilot/VS Code JSON variants with schema differences). Converting is mechanical but has silent-failure modes.
4. **Hooks, slash commands, subagents, skills, permissions do NOT port** — each tool has its own file format, location, event set, and blocking semantics. Codex CLI's hooks are a near-direct port of Claude Code's protocol (JSON-on-stdin, exit codes) but with a smaller event set; Gemini CLI added hooks in Jan 2026; Copilot CLI has no simple slash-command file convention.
5. **The swap mechanism (env-var base-URL / proxy) works but degrades silently** — prompt caching breaks, tool-calling formats mismatch, and long sessions drift. Empirically, instruction files themselves do not generally improve task success and add 20%+ token cost (ETH Zurich study, arXiv:2602.11988, Feb 2026).
6. **The honest counter-case:** standardizing on one vendor's richer feature set (Claude Code's 30 hook events, subagents, skills, prompt-cache economics) may beat portability for a mechanisms-heavy methodology. Portability's real payoff is insurance against pricing/ToS/availability shocks, not day-to-day capability.

## Details

### Q1 — AGENTS.md as a standard: actual status

**Governance (VERIFIED).** AGENTS.md was formalized as an open spec in **August 2025**, led by OpenAI with participation from Google, Cursor, Factory, Sourcegraph and Amp. On **December 9, 2025** (per TechCrunch, 9:28 AM PST), it was contributed to the **Linux Foundation's Agentic AI Foundation (AAIF)** — Anthropic donated MCP, OpenAI contributed AGENTS.md, and Block contributed Goose to the newly formed foundation. Per OpenAI's announcement, AAIF was co-founded by OpenAI, Anthropic and Block "with the support of Google, Microsoft, AWS, Bloomberg, and Cloudflare"; the eight platinum sponsors are AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI. The canonical site (agents.md) is now footed "AGENTS.md a Series of LF Projects, LLC." This is a genuine multi-vendor foundation, not a single-vendor project — a meaningful de-risking signal for a strategic bet.

**What the spec mandates (VERIFIED).** Almost nothing. Per agents.md: "AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide." No required fields, no YAML, no schema. Precedence: "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." Monorepos nest files (OpenAI's own repo ships 88). This looseness is itself a risk — a peer study documents that the community has NOT converged on whether AGENTS.md is the governance document, a pointer to one, or a hybrid; open spec issue agentsmd/agents.md #66 (Sept 2025) acknowledges but doesn't resolve the "redirect problem."

**Adoption (VERIFIED).** The Linux Foundation press release (Dec 9, 2025) states: "AGENTS.md has already been adopted by more than 60,000 open source projects and agent frameworks including Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code among others." The agents.md site links a live GitHub code-search corroborating the 60k+ figure. Independent academic work estimates 15–19% of GitHub projects showed coding-agent traces by mid-October 2025 and growing steeply — so the install base for the tools that read AGENTS.md is large and real. Bug-reduction figures ("35–55% fewer agent bugs," "setup 20–40 min → under 2 min") circulate widely but trace to marketing/Medium posts, not controlled studies — treat as REPORTED/unverified.

**Native support & precedence (VERIFIED per vendor docs unless noted):**

| Tool | Reads AGENTS.md natively? | File(s) it reads / precedence | Nested/subdir? |
|---|---|---|---|
| **OpenAI Codex CLI** | Yes (native) | `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` (global) → repo-root → intermediate dirs → cwd; `AGENTS.override.md` beats `AGENTS.md` at each level; concatenated, later wins; 32 KiB cap (`project_doc_max_bytes`); `project_doc_fallback_filenames` for alternates | Yes, walks tree |
| **Gemini CLI** | Via one-line config | Default `GEMINI.md`; set `context.fileName: ["AGENTS.md",...]` in `.gemini/settings.json`; supports `@file.md` imports | Yes |
| **GitHub Copilot (CLI/coding agent/VS Code)** | Yes | `AGENTS.md` plus `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` (YAML `applyTo` frontmatter, path-scoped); combines, dedups, no defined precedence between them; `@path` includes supported | Yes |
| **Cursor** | Yes (added natively by 2026-06) | `AGENTS.md` at root + `.cursor/rules/` (or legacy `.cursorrules`) for tool-specific | Yes |
| **Claude Code** | **No** | `CLAUDE.md` only (+ `~/.claude/CLAUDE.md`, `MEMORY.md`); use `@AGENTS.md` import or symlink | Yes (walks up tree) |
| **Aider** | Yes (config) | `.aider.conf.yml`: `read: AGENTS.md` | — |
| **Windsurf, Cline** | Yes (added by 2026-06) | `AGENTS.md` + `.windsurf/rules/`, `.clinerules/` | Yes |
| **Zed, Warp, RooCode, Kilo Code, Jules, Devin, Amp, Junie, Factory, opencode, Semgrep, Amazon Q** | Yes (listed on agents.md) | AGENTS.md | varies |
| **Kimi Code CLI** | Yes | Follows AGENTS.md convention; MCP compatible with `.mcp.json` | Yes |
| **Qwen Code** | Reported yes (Qwen ecosystem) | AGENTS.md / QWEN.md | — |

**OpenCode nuance (VERIFIED):** OpenCode reads AGENTS.md first, falls back to CLAUDE.md in the same directory; `OPENCODE_DISABLE_CLAUDE_CODE=1` disables that fallback. This is the only tool with documented two-way fallback.

### Q2 — Mechanics of a one-canonical-file setup

Four patterns, assessed for your Windows + git-bash/WSL, library-first constraints:

**(a) Symlinks (`ln -s AGENTS.md CLAUDE.md`).** Git stores a symlink as mode `120000` with the target path as blob content. On Windows, checkout as a real symlink requires `core.symlinks=true` AND either Administrator or Developer Mode; otherwise **git silently checks out a plain text file containing the link target string** — a broken stub the agent will read as literal text. GitHub/GitLab web UIs render symlinks as text files. **Verdict: reject as primary mechanism** on a Windows-heavy fleet — it's the single most common way this setup breaks silently. It also can't carry Claude-specific deltas (the file *is* the other file).

**(b) Claude Code `@import` (`@AGENTS.md` on line 1 of CLAUDE.md).** VERIFIED in Anthropic docs. Imports expand at session start, up to **4 hops deep**, relative or absolute paths, one approval dialog on first sight. Keeps CLAUDE.md a real file so you can append Claude-only deltas beneath the import. **Windows-clean, git-clean, no server.** This is the Anthropic-recommended pattern and the correct base for your CLAUDE.md stub. Limitation: `@import` is Claude-specific; no other tool has an identical mechanism (Gemini has `@file.md`, Copilot has `@path`, Codex concatenates nested files instead).

**(c) Generation/templating at commit time.** A build step renders each provider file from the canonical AGENTS.md (+ per-provider delta fragments), with a CI check that fails on drift. **Best fit for "mechanisms not prose" and library-first.** Windows-clean, git-clean, explicit, auditable. Cost: you own a small renderer + check. Library-first note: don't hand-roll a bespoke templating engine — use stdlib (`string.Template`/`str.format` or Jinja2 if already a dependency) and enforce with `pre-commit` + a GitHub Actions job; the "OSS project that covers it" is `pre-commit` itself plus a trivial checksum comparison.

**(d) Duplication with a checksum/verification gate.** Copy content into each provider file, embed a checksum of the canonical block, and a pre-commit/CI hook fails if any copy's embedded hash ≠ recomputed canonical hash. Simplest to reason about; highest raw drift risk but the gate makes drift *loud* rather than silent.

**Real documented setups:** The chezmoi-based "one MCP config for Codex, Claude, Cursor, Copilot" writeup (dev.to/dotwee, mirrored prodsens.live, March 2026) explicitly recommends **generate-from-template, never edit generated targets** and treats adapters as "projection layers, not permanent schemas." The MCP.Directory converter tool documents the 8-format matrix. A Gemini CLI discussion (#1471) shows a practitioner hardlinking CLAUDE.md/AGENTS.md/GEMINI.md/.cursorrules to the most-recent one — an illustration of how ugly the ad-hoc approach gets ("It's ridiculous :)").

### Q3 — Capability matrix: what ports, what doesn't

**Instruction files:** de-facto standard (AGENTS.md) everywhere except Claude Code (bridge via `@import`). PORTS.

**Custom slash commands:** NO cross-tool standard, must re-author.
- Claude Code: `.claude/commands/*.md`.
- Codex CLI: `~/.codex/prompts/*.md` with YAML frontmatter (`description`, `argument-hint`, `$1..$9`, `$ARGUMENTS`) — but OpenAI now marks custom prompts **deprecated in favor of skills**.
- Cursor: `.cursor/commands/*.md` (Markdown prompts).
- Gemini CLI: custom commands supported (TOML-based).
- Copilot CLI: **no documented .md-file→/command convention**; use custom agents or skills instead.

**Hooks:** NO cross-tool standard; partial convergence.
- Claude Code: the richest — as of July 1 2026 the reference documents **30 hook events** (SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse, PostToolBatch, Stop, SubagentStop, PermissionRequest, PreCompact, TeammateIdle, etc.). Configured in `settings.json`; JSON-on-stdin; **exit code 2 blocks** on PreToolUse/Stop/PermissionRequest and others; observe-only on PostToolUse. Five handler types (command, http, mcp_tool, prompt, agent).
- Codex CLI: hooks shipped 2026; "almost a direct port of Claude Code's" protocol (same JSON/exit-code shape) but **6 events** (SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop), command hooks only.
- Gemini CLI: hooks launched **v0.26.0, Jan 27 2026**.
- Cursor: cloud-agent hooks (`beforeSubmitPrompt`, `afterAgentResponse`, `afterAgentThought`, `stop`, `subagentStart`).
- Copilot CLI / Kimi Code CLI: limited/none documented as blocking gates.
- **Consequence for "mechanisms not prose":** your enforcement layer should live in **provider-agnostic git hooks + pre-commit + GitHub Actions**, NOT in tool-specific agent hooks, so the gate holds regardless of which agent runs. Use tool hooks only as an in-session convenience mirror.

**Subagents + per-subagent model selection:** Claude Code (subagents with per-agent model), Codex CLI (native subagents), Kimi Code CLI (coder/explore/plan subagents), Cursor (subagents). Gemini CLI historically sequential/no subagents. NO portable definition format — re-author.

**MCP:** servers interchangeable (open protocol; Anthropic's Mike Krieger cited "more than 10,000 published MCP servers" in the LF release); configs NOT (JSON vs TOML, `mcpServers` vs `servers` vs `[mcp_servers.x]`, `type` field required for VS Code). Best-covered by a generator/converter; treat `.mcp.json` as the shareable project surface.

**Permission/approval & sandboxing:** all differ. Codex: explicit `--sandbox` (read-only/workspace-write/full) + `--ask-for-approval`; `--yolo`/`--dangerously-bypass-approvals-and-sandbox` disables both. Claude Code: 5-level settings cascade + permission modes. Copilot CLI: standard/plan/autopilot via Shift+Tab. Re-author.

**Headless/non-interactive:** Claude Code `claude -p`; Codex `codex exec` (with `--json`, `--output-last-message`, `resume`); Gemini/Copilot have headless/CI modes. Flags differ; concept ports.

**Background execution & worktrees:** Copilot CLI has `/worktree` (auto-creates git worktree) and background subagents; Cursor 2.0 (Oct 2025) runs parallel agents via git worktrees; Claude Code has Agent Teams / background tasks. Git-worktree parallelism is itself provider-agnostic (it's just git) — your lanes port for free.

**Session persistence/resume:** Codex `codex exec resume`; Copilot `--resume`/`/resume`; Cursor sessions; Claude Code resume. Concept common, storage/format tool-specific.

**Skills:** Anthropic's `SKILL.md` (YAML frontmatter + bundled scripts) is emerging as a semi-standard — Claude Code `.claude/skills/`, Codex `.agents/skills/` (also `~/.codex/skills/`), Cursor supports Agent Skills / SKILL.md. There's an interop ask for a shared `.agents/skills/` path (Claude issue #31005). Partially portable, path-dependent.

### Q3b — Kimi / Moonshot specifically

**What exists in 2026 (VERIFIED):**
- **Kimi Code CLI** (successor to `kimi-cli`): Moonshot's own terminal agent, **MIT-licensed**, rewritten from Python/uv to **Node/TypeScript**, `npm install -g @kimi-code/cli` (Node ≥22.19). Reached ~9.7K GitHub stars around its v1.49 release (July 16 2026). Built-in coder/explore/plan subagents; MCP via conversational `/mcp-config`; **follows the AGENTS.md convention and is compatible with `.mcp.json`** — a deliberate Claude-Code-lookalike (same tool names Bash/Read/Write/Edit). **Naming trap:** the old Python `kimi-cli` pip package is deprecated; install the new one.
- **Models:** Kimi K2 Thinking (256K context, 1T MoE / 32B active, OpenRouter ~$0.60 in / $2.50 out); K2.6 (Apr 20 2026, 256K, multimodal, ~$0.58–0.95 in / $2.50–4.00 out); K2.7 Code (June 2026, always-thinking, 256K, ~$0.68 in / $3.40 out, SWE-bench Pro 58.6 vendor-reported); K3 (July 16 2026, 2.8T MoE, up to 1,048,576-token context, native vision).
- **Anthropic-compatible endpoint (VERIFIED):** `https://api.moonshot.ai/anthropic` (global) or `https://api.moonshot.cn/anthropic` (China), plus OpenAI-compatible `https://api.moonshot.ai/v1`. Point Claude Code via `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_MODEL=kimi-k2.7-code` (set all model slots: OPUS/SONNET/HAIKU/SUBAGENT — Claude Code calls all three slots, and a proxy that only maps one produces "model not found" errors). Kimi also has a dedicated coding endpoint `https://api.kimi.com/coding/` for the Kimi-for-Coding subscription.
- **Subscription:** Kimi Code included in Kimi membership (community-cited ~$19/mo coding tier); pay-per-token via Moonshot platform; K3 needs higher membership tiers, 1M context needs the top tier; Moonshot temporarily paused new subs after K3 launch (July 18 2026) citing capacity.

**Realism of Claude Code → Kimi swap:** Wiring is trivial (env vars, ~5 min). **Documented gotchas (VERIFIED/REPORTED):** on the Kimi endpoint, `WebFetch` is unsupported (returns "temporarily unavailable"); `WebSearch` fails with "400 invalid thinking" on kimi-k2.7-code unless Thinking is enabled (model-version-dependent — the K3 blog reports WebSearch working but WebFetch still failing); Tool Search unsupported; Anthropic `cache_control` markers are ignored (Kimi does its own prefix caching — changing the system field, tools array, or any image reference invalidates the messages cache entirely). K2.6 has been independently reported to sustain 4,000+ tool calls over a 13-hour session — genuinely strong agentic stability for an open model.

### Q4 — The provider-swap mechanism itself

**Paths:**
1. **Env-var base-URL override** (`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`, or `~/.claude/settings.json` `env` block). Simplest; official for Bedrock/Vertex and used by Kimi. No server.
2. **Local proxy/router** — `claude-code-router` (~31k stars; task-type routing to DeepSeek/Gemini/Ollama/OpenRouter; local port 127.0.0.1:3456), `claude-code-proxy` (Python, ~3.3k stars; Anthropic→OpenAI/Gemini via LiteLLM), **LiteLLM proxy** (general gateway, Anthropic-compatible endpoint, fallback chains, Vertex/Bedrock). **These run a local server** — flag against your "no always-running servers unless justified" rule; justified only transiently for a swap test or if you need task-type cost routing.
3. **Bedrock/Vertex** — first-party supported for Claude models (env vars / LiteLLM), enterprise-grade but still Claude.
4. **OpenAI-compatible endpoints** for non-OpenAI models (Kimi, GLM, MiniMax, local via Ollama/vLLM).

**What breaks (VERIFIED where cited):**
- **Prompt caching.** Anthropic's own docs: with a custom base URL/gateway, "whether the cache takes effect depends on the gateway. If the gateway rejects the cache breakpoint on that block, Claude Code retries the request without it and leaves that block uncached for the rest of the conversation" — i.e., **silent, session-long cache loss**. LiteLLM strips `cache_control` for non-Claude/Gemini models (its `CacheControlSupportedModels` enum "only includes Claude and Gemini"; issues #19923, #20418). **GitLab hit this in production** on Vertex + LiteLLM (MR #3800, Nov 6 2025: `cache_creation: 0` on the litellm path vs `cache_read: 21911` on the native Anthropic path). A community fix-repo cites "up to 20x cost increase" on resumed sessions, and Claude Code changelog 2.1.181 fixed a per-request attestation token that had broken caching specifically for custom-base-URL/proxy clients. Cost impact is the single biggest hidden tax of the swap.
- **Tool-calling format.** Proxies that lowercase/underscore Claude Code's case-sensitive tool names (Bash, Glob, Edit) break it — the client rejects with "No such tool available" and loops (CLIProxyAPI #1741). Streaming `input_json_delta` fragments dropped → `Bash.command` becomes `undefined` (#3776). Multi-step tool calls break under OpenAI-format translation ("text part not found," silently dropped deltas; LiteLLM #26529). Edit search-and-replace format tuned for Claude produces malformed hunks on other models → failed edits + retries (morphllm). Local backends silently no-op tool calls with wrong parser flags (renezander.com, tested Apr 2026).
- **System-prompt assumptions, token accounting, rate limits** all shift per backend.

**ToS (VERIFIED, critical):** Pointing Claude Code at a non-Anthropic model **using a third-party (e.g. Moonshot) API key does NOT violate Anthropic's terms** — you aren't using Anthropic's service. What DOES violate: using a **Claude Free/Pro/Max OAuth subscription token** through any non-Anthropic harness. Anthropic's legal-and-compliance page (updated Feb 19 2026; quoted verbatim by The Register, Feb 20 2026, "Anthropic clarifies ban on third-party tool access to Claude"): "Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — including the Agent SDK — is not permitted and constitutes a violation of the Consumer Terms of Service." Underlying clause: Consumer ToS §3.7 (bars automated/non-human access except via an Anthropic API key). Enforcement began Jan 2026 (server-side block: "This credential is only authorized for use with Claude Code"); OpenCode removed subscription support in a commit citing "anthropic legal requests." **Rule for your fleet: swaps must use API keys, never subscription OAuth through a foreign harness.**

**Stability:** These paths are actively maintained but fragile and version-sensitive (a Claude Code update broke LiteLLM caching in #20418; the attestation-token change broke custom-base-URL caching until 2.1.181). Treat any proxy path as needing a pinned, tested combination.

### Q5 — What the swap costs in practice

- **Instruction-file portability is empirically weak as a *quality* lever.** The ETH Zurich study "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (Gloaguen, Mündler, Müller, Raychev & Vechev; SRI Lab / LogicStar.ai; **arXiv:2602.11988, Feb 12–13 2026**; 138 tasks / 12 repos across SWE-bench Lite + AGENTbench) states in its abstract: "we find that providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average." Developer-written files improved success ~4% on AGENTbench; LLM-generated files reduced it ~0.5% (SWE-bench Lite) to ~2% (AGENTbench); agents spent 14–22% more reasoning tokens and 2–4 extra steps. The mechanism: "agents dutifully process every instruction, whether it helps or not." A separate study on instruction adherence reports **within-session compliance attenuation** — each additional function the agent generates lowers adherence — and found structural variables (file size, position, conflict) had no detectable effect. **Implication: keep AGENTS.md short and high-signal (a ~150-line threshold is widely cited), and do NOT rely on it to carry enforcement.**
- **Migration is "largely mechanical" (REPORTED).** A Towards AI writeup (Rick Hightower, 2026) describes converting a Claude Code repo into dual Claude+Codex or Claude+Gemini runtimes with master prompts, preserving `.claude/` and adding the parallel runtime alongside — calling the April-2026 convergence real. Tembo/DeployHQ/DataCamp comparisons (June 2026, checked against vendor docs) converge on: Claude Code = cleanest multi-file changes; Codex = best reviewer + GitHub story; Gemini = big-context reads (but Google moved consumer Gemini CLI to Antigravity CLI, **individual tier ended June 18 2026** — a live churn example).
- **Same AGENTS.md, comparable behavior?** No published head-to-head proves equal instruction-following across tools. The consistent qualitative finding is that models differ more in *posture/defaults* than in whether they read the file.

### Q6 — Designing for portability: what lives where

- **Canonical `AGENTS.md` (root, + nested per satellite):** project overview, build/test/lint commands (`uv`, `ruff`, `pytest`, `pre-commit`), code-style conventions, architectural constraints, security "never do" rules, PR/commit conventions. Prose that any model can parse. Keep <150 lines; push detail into referenced files.
- **Provider stubs (thin):** `CLAUDE.md` = `@AGENTS.md` + Claude-only deltas (plan-mode rules, subagent/model routing). Gemini: `.gemini/settings.json` `context.fileName:["AGENTS.md","GEMINI.md"]`. Copilot: rely on native AGENTS.md read; `.github/copilot-instructions.md` only for Copilot-specific deltas. Codex: reads AGENTS.md directly, `.codex/config.toml` for fallback filenames/size.
- **Repo-enforced, provider-agnostic mechanisms (the real teeth):** `pre-commit` hooks, `ruff`/`pytest` gates, and **GitHub Actions** are your "mechanisms not prose" layer. They run identically no matter which agent authored the change — this is where frozen-contract enforcement belongs, NOT in tool-specific agent hooks.
- **Tool-specific config that must be re-authored:** slash commands, agent hooks, subagent definitions, skills, permission/sandbox modes, MCP config files (generated from one canonical MCP spec).
- **Layout (avoids single-file folders where possible):**
```
hub-repo/
  AGENTS.md                # canonical doctrine
  CLAUDE.md                # @AGENTS.md + Claude deltas (real file, not symlink)
  .gemini/settings.json    # points contextFileName at AGENTS.md
  .mcp.json                # canonical MCP surface (Claude/Kimi read directly)
  tools/
    render_provider_files.py   # generation build step (stdlib/Jinja2)
    check_drift.py             # checksum/generation drift gate
    mcp/servers.yaml           # single MCP source -> renders .mcp.json, config.toml, .cursor/mcp.json
  .pre-commit-config.yaml  # runs check_drift + ruff + pytest gates
  .github/workflows/ci.yml # fails on drift; provider-agnostic enforcement
  .agents/skills/          # shared skills (Codex/Cursor); symlink/generate .claude/skills
```
Single-file tool folders (`.claude/commands/` with one file, etc.) are only created when a tool truly requires that path; where a tool reads a root file (AGENTS.md), keep it at root.
- **Drift-guard mechanism (recommendation):** a **spec registry with version stamps + a generation check**. Each generated provider file carries a header comment with the canonical AGENTS.md content hash and a spec-version stamp; `check_drift.py` recomputes and fails CI if any stub's stamp/hash disagrees. This is stronger than a bare checksum because it also catches spec-version skew across the satellite fleet, and it satisfies library-first (stdlib `hashlib` + `pre-commit`, no hand-rolled framework).

### Q7 — Risks and the honest case against

- **Lowest-common-denominator methodology.** If the doctrine must express only what all tools share, you lose Claude Code's 30 hook events, prompt-cache economics, subagent model-routing, and skills. For a methodology whose whole premise is "mechanisms not prose," that's a real amputation — many of those mechanisms ARE tool-specific.
- **N-stub maintenance cost.** Every provider stub + every re-authored hook/command/skill/MCP-config is ongoing surface. The generation+drift-guard contains this but doesn't eliminate re-authoring of behavior (hooks/commands).
- **Young-standard churn (evidenced).** AGENTS.md spec is <1 year old and unresolved on core semantics (redirect problem, #66). Tools change what they read (Cursor/Windsurf/Cline added native AGENTS.md only by June 2026; Claude Code still hasn't). Whole tools pivot (Gemini CLI → Antigravity, consumer tier killed June 18 2026). Proxy caching breaks on version bumps.
- **Instruction files only partially obeyed regardless of format** (ETH Zurich arXiv:2602.11988; within-session attenuation). Portability of the *file* doesn't buy portability of *behavior*.
- **The counter-argument (steelman):** Standardize on Claude Code, exploit its full mechanism surface, and treat portability as a documented escape hatch you validate quarterly rather than a daily constraint. Evidence for: richer enforcement, best-reported multi-file quality, mature hooks. Evidence against: ToS/pricing/availability shocks are real (Anthropic's Jan 2026 subscription-harness crackdown; Gemini consumer sunset), and a fleet locked to one vendor has no cheap exit. **The balanced position: keep the doctrine and enforcement provider-agnostic (they cost little to keep portable), but do NOT sacrifice Claude-specific mechanisms to the lowest common denominator — express them as Claude deltas and accept they won't port.**

### Q8 — Minimal starter path

Smallest sequence from "CLAUDE.md + Claude-specific config" to "canonical AGENTS.md + thin stubs + drift guard + demonstrated swap":

1. **Split CLAUDE.md → AGENTS.md + CLAUDE.md stub (S).** Move tool-agnostic doctrine into `AGENTS.md`; reduce `CLAUDE.md` to `@AGENTS.md` + Claude-only deltas. *Buys:* native portability to Codex/Cursor/Copilot/Kimi immediately; Claude unchanged via import.
2. **Point Gemini at AGENTS.md (S).** Add `.gemini/settings.json` `context.fileName`. *Buys:* Gemini CLI parity.
3. **Add the drift guard (M).** `check_drift.py` (stdlib `hashlib`) + `.pre-commit-config.yaml` + a GitHub Actions job that fails on stub/canonical hash or version-stamp mismatch. *Buys:* the "no second copy can silently disagree" guarantee.
4. **Canonicalize MCP (M).** One `tools/mcp/servers.yaml` → generate `.mcp.json` (Claude/Kimi), `.codex/config.toml`, `.cursor/mcp.json`. *Buys:* MCP portability without hand-editing N formats.
5. **Move enforcement into provider-agnostic gates (M).** Port any Claude-hook-enforced rules that are truly universal into `pre-commit`/CI checkers; keep only convenience mirrors as tool hooks. *Buys:* enforcement that holds under any agent — the core of "mechanisms not prose."
6. **Demonstrate the swap (S–M).** Run the SAME repo/task under a second tool.

**Minimal proof (smallest task that demonstrates a real swap):** On one satellite repo, take a single frozen-contract task — e.g. "add a validated function + tests until `pytest` and `ruff` are green under the pre-commit gate." Run it end-to-end **twice**: once with Claude Code (Anthropic), once with the identical repo under **Codex CLI** (reads AGENTS.md natively, no bridge) OR **Claude Code pointed at Kimi via `ANTHROPIC_BASE_URL` + Moonshot API key**.

**What to measure:** (1) did the second tool read and obey the canonical AGENTS.md (ask it to quote a distinctive line); (2) did the provider-agnostic gates (pre-commit/CI) pass identically; (3) instruction-compliance deltas (did it violate a "never do" rule); (4) tool-call breakage (esp. on the Kimi path: WebFetch/WebSearch, edit-hunk failures); (5) token cost + latency vs Claude (watch for the silent prompt-cache loss); (6) whether hooks/commands had to be re-authored and how long it took. Success = green gates + AGENTS.md obeyed + quantified cost delta. This proves the doctrine + enforcement port even though tool-specific mechanisms don't.

## Recommendations

1. **Adopt the canonical AGENTS.md + thin-stub shape now (S).** It is low-cost, low-risk, and the standard is foundation-governed. Use `@AGENTS.md` import for CLAUDE.md — **not** a symlink (symlinks degrade to broken text stubs on Windows without Developer Mode / `core.symlinks=true`).
2. **Make the drift guard a generation-plus-version-stamp check enforced by pre-commit + GitHub Actions (M).** Library-first: `hashlib` + `pre-commit`, optionally Jinja2 if already a dependency. Never hand-roll a templating framework.
3. **Keep all frozen-contract enforcement in provider-agnostic gates**, not tool hooks. Tool hooks are convenience mirrors, not the source of truth.
4. **Treat the provider swap as a validated fallback, not a daily driver.** Validate one swap path (recommend Codex CLI for a no-bridge native path, plus Claude Code→Kimi as the cost/availability hedge) quarterly. Budget for silent prompt-cache loss and tool-call breakage on any proxy path.
5. **Hard rule: swaps use API keys only.** Never route a Claude Pro/Max subscription through a non-Anthropic harness — it violates Anthropic's Consumer Terms (§3.7; legal page updated Feb 2026) and is now actively enforced.
6. **Do not flatten to a lowest-common-denominator methodology.** Express Claude-specific mechanisms (hooks, subagents, skills, prompt-cache) as deltas and accept they don't port. Portability's payoff is insurance, not feature parity.

**Thresholds that change the recommendation:** If Claude Code ships native AGENTS.md reading (tracked in issue #6235; a prediction market put ~61% on 2026), drop the CLAUDE.md import and read AGENTS.md directly. If a genuine cross-tool hook/command standard emerges under AAIF, move enforcement mirrors into it. If your token bill on the primary vendor exceeds the measured cost of a Kimi/GLM sidecar by a wide margin AND the swap proof shows acceptable tool-call reliability, promote the swap from fallback to routed production (background/bulk tasks to the cheap model, critical path to the primary).

## Caveats
- **Dates and model names:** Several 2026 model versions (Opus 4.8, Kimi K3, GLM-5.2) and events appear only in vendor/blog sources; treat exact version specifics as REPORTED. Governance, spec semantics, precedence rules, prompt-caching behavior, and ToS clauses are VERIFIED against primary docs (agents.md, Linux Foundation/OpenAI announcements, Anthropic docs, OpenAI Codex docs, Gemini CLI docs, LiteLLM docs/issues, GitHub issues).
- **Adoption numbers (60k repos; bug-reduction %):** the 60k figure is from the Linux Foundation release and a live GitHub code-search (credible); the "35–55% fewer bugs / 20–40 min → 2 min" figures are marketing/Medium claims, unverified.
- **arXiv identifiers:** The context-file efficacy study is confirmed as arXiv:2602.11988 (ETH Zurich, Feb 2026); other arXiv numbers cited during research were not reliably verifiable and are described by finding rather than ID.
- **Kimi WebSearch/WebFetch:** support differs by model version (K2.7 vs K3) and by endpoint; confirm against platform.kimi.ai at swap time.
- **Proxy stability:** version-sensitive; any working combination must be pinned and re-tested on tool upgrades.
- **The instruction-file efficacy studies** measured test-pass rates, not code quality/maintainability/style — AGENTS.md may help in unmeasured dimensions (noted by study critics on Hacker News).