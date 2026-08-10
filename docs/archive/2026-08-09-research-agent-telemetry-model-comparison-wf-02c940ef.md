# Instrumenting and Measuring LLM Coding-Agent Work: A Decision-Ready Guide for a Hub-and-Satellite Python Fleet

## TL;DR
- **Most of what you want is already recorded.** Claude Code writes a complete per-session JSONL transcript (`~/.claude/projects/<encoded-path>/<session-id>.jsonl`) with per-message model id, per-request token usage (input/output/cache-read/cache-creation), timestamps, tool_use/tool_result entries, and subagent sidechains — and it emits native OpenTelemetry metrics/events (session, token, cost, LOC, code-edit decisions, active-time) with no SaaS required (console, Prometheus scrape, or a locally-run OTLP collector). Your first move is **extraction, not plumbing**: run `ccusage` over the JSONL and stand up a `SessionEnd`/`Stop` hook that appends one telemetry record per session to a committed JSONL log.
- **Fair model comparison is a measurement-design problem, not a dashboard problem.** LLM agents are nondeterministic even at temperature 0, self-reported speed is unreliable (the METR RCT found experienced devs were 19% *slower* with AI while believing they were 20% faster), and SWE-bench-style scores are contaminated. Use paired within-task designs, ≥5–10 repeats per model, report distributions with bootstrap confidence intervals, and gate new model lanes on a **private, versioned seeded-defect corpus** (mutation operators + hand-authored realistic defects) scored on detection rate, fix correctness, false-positive rate, and cost/time per defect.
- **The honest cross-provider denominator is narrow.** Only wall-clock, tokens in/out, tool-call counts, and outcome/verdict map cleanly across Claude Code, Codex CLI, Gemini CLI, Copilot CLI, and Grok CLI. Dollar cost and especially GitHub's "premium requests"/AI-credits do **not** normalize onto tokens; record raw provider units plus a separately computed token-based cost estimate, and never mix subscription-plan and API-billed cost as one ledger.

## Key Findings

1. **Claude Code exposes more than any competitor**, on two independent data paths: the on-disk JSONL transcript (always on, local) and native OpenTelemetry (opt-in, local or remote). Both are documented by Anthropic.
2. **The transcript format is explicitly "internal" and version-unstable.** Anthropic warns not to build parsers on undocumented record relationships — so prefer `ccusage`/OTel where possible and treat direct-JSONL joins as version-pinned.
3. **OTel is the standards-aligned path** and can run fully local (console exporter, Prometheus scrape, or a local OTLP collector into SQLite/DuckDB/ClickHouse) — no enterprise plan needed. Anthropic *also* offers admin Usage/Cost and Claude Code Analytics APIs, but those require an Admin API key and only cover API-billed and Pro/Team usage.
4. **Other agents converge on OTel and local JSONL, unevenly.** Codex CLI (`~/.codex/sessions/*.jsonl` + `[otel]` in `config.toml`) and Gemini CLI (OTel with GenAI semconv, `.gemini/telemetry.log`) are close to Claude Code. Copilot CLI meters in **premium requests / AI credits**, not tokens. Grok CLI (community, superagent-ai) logs tokens to `~/.grok/logs/unified.jsonl` but is less actively maintained.
5. **The dangerous metrics are LOC, commit counts, and self-reported speed.** DORA and SPACE both warn against single-dimension and individual productivity metrics; every proxy becomes gameable once it's a target (Goodhart). Defensible metrics are cost-per-*solved*-task, wall-clock and active-time per completed task, retry/error-loop counts, edit-revert rates, and tasks/rows closed per window — always paired with an outcome verdict.
6. **A private seeded-defect corpus is the right admission gate** for new model lanes, and the tooling exists: mutmut, cosmic-ray, mutatest for mutation-based defects; Defects4J/BugsInPy as templates for structure. Stratify by realistic defect classes, keep it out of agent context, version it in git, and score detection + fix-correctness + false-positive + cost.
7. **A standards-aligned telemetry record already has a vocabulary**: OpenTelemetry GenAI semantic conventions (span/attribute names like `gen_ai.usage.input_tokens`, agent spans, MCP tool spans). Align your committed per-session record to these keys so it's portable rather than invented.

## Details

### Q1 — What Claude Code actually exposes

**(a) Session transcript (local, always on, no server).**
Claude Code stores every session as JSONL, one JSON object per line, at `~/.claude/projects/<encoded-project-path>/<session-id>.jsonl` (on Windows, `%USERPROFILE%\.claude\projects\`). The `<project>` segment is your working-directory path with non-alphanumeric characters replaced by `-`. Anthropic's own docs describe it and give the field hooks/status lines receive (`transcript_path`), and note you can produce structured output non-interactively with `claude -p --output-format json` / `stream-json`. Each line is a typed record — user turn, assistant response, tool_use, tool_result, system event, or summary — chained by `parentUuid`. Assistant entries carry the **model id**, a **usage block** (input, output, cache-read, cache-creation tokens), a `requestId`, and timestamps; tool calls carry their full input; **subagent spawns link to child session records via sidechain entries** carrying `agent_id`/`agent_type`. This is what community parsers (ccusage, claude-devtools, simonw/claude-code-transcripts, lm-assist) read.

**Critical caveat, from Anthropic's docs:** the transcript "entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release." Treat direct JSONL joins as version-pinned mechanisms. Also, transcripts contain full source, file paths, and anything a tool printed (including secrets read from `.env` or error logs) — they are **not** safe to share and must be redacted before leaving the machine.

**(b) Native OpenTelemetry (opt-in; local OR remote).**
Enabled with `CLAUDE_CODE_ENABLE_TELEMETRY=1` plus exporter selectors (`OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER` = `otlp`|`prometheus`|`console`|`none`). **This can run with no server**: `console` prints to your terminal, `prometheus` opens a local scrape endpoint (`http://localhost:9464/metrics`), and `otlp` can point at a locally-run collector. OpenTelemetry support is in beta and marked subject to change.

Metrics emitted (each with rich attributes plus standard attributes like `session.id`, `model`, `user.id`):
- `claude_code.session.count` (with `start_type`: fresh/resume/continue/agents_view)
- `claude_code.lines_of_code.count` (`type` added/removed, `model`)
- `claude_code.pull_request.count`, `claude_code.commit.count`
- `claude_code.cost.usage` (USD; attributes include `model`, `query_source` = main/subagent/auxiliary, `effort` low/medium/high/xhigh/max, `agent.name`, `skill.name`)
- `claude_code.token.usage` (`type` = input/output/cacheRead/cacheCreation, `model`, `query_source`)
- `claude_code.code_edit_tool.decision` (`decision` accept/reject, `tool_name`, `language`)
- `claude_code.active_time.total` (seconds, `type` user/cli) — this is your **engaged-time** signal.

Events (via the logs/events exporter): `user_prompt`, `assistant_response`, `api_request` (carries `cost_usd`, `duration_ms`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `request_id`), `api_error` (with `attempt` count and `status_code`), `api_refusal`, `tool_result` (with `success`, `duration_ms`, `error_type`, sizes), `tool_decision`, `permission_mode_changed`, `mcp_server_connection`, `compaction` (with `pre_tokens`/`post_tokens`), plus hook lifecycle events (`hook_execution_start`/`complete` with per-hook durations and blocking counts) and `api_retries_exhausted` (with `total_attempts`, `total_retry_duration_ms`). Content (prompts, responses, tool inputs) is **redacted by default** — you must opt in via `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT`, `OTEL_LOG_RAW_API_BODIES`.

There is also a **traces (beta)** path (`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, `OTEL_TRACES_EXPORTER`) producing a span hierarchy: `claude_code.interaction` → `claude_code.llm_request` / `claude_code.tool` (with `tool.blocked_on_user`, `tool.execution`) — and subagent spans nest under the parent tool span. Spans carry OTel GenAI convention attributes (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.response.id`, `gen_ai.tool.call.id`) and per-phase timing (`interaction.duration_ms`, `ttft_ms`, tool execution vs. permission-wait split) natively.

**Enterprise/admin analytics surface.** Anthropic ships a **Usage & Cost Admin API** (`GET /v1/organizations/usage_report/messages` for token usage by model/workspace/API key with `1m`/`1h`/`1d` buckets and uncached/cached/cache-creation/output token breakdown; `GET /v1/organizations/cost_report` for USD cost, daily buckets only) and a dedicated **Claude Code Analytics API** (`GET /v1/organizations/usage_report/claude_code`) that returns per-user sessions, lines added/removed, commits, PRs, tool accept/reject rates (Edit/MultiEdit/Write/NotebookEdit), per-model tokens (incl. cache), and estimated cost. **All require an Admin API key (`sk-ant-admin01-…`), and the Admin API is unavailable for individual accounts.** The Claude Code Analytics API distinguishes `customer_type` = `api` vs `subscription` (Pro/Team), so subscription usage is covered — but it "only tracks Claude Code usage on the Claude API," excluding Bedrock/Vertex/Foundry/AWS deployments, is daily-aggregated with ~1h delay, and its costs are **estimates**. Anthropic positions the API as "more detail than the basic Analytics dashboard without the complexity of the OpenTelemetry integration." A separate **Enterprise Analytics API** (claude.ai Enterprise) uses a different Analytics API key. The Console also has web Usage/Cost pages (view by model, API key, date, drillable to hour/minute).

**(c) Hooks as instrumentation points (local, no server).**
Claude Code fires hooks at lifecycle events; command hooks receive JSON on stdin (HTTP hooks as POST body). Events relevant to instrumentation: `SessionStart`/`SessionEnd` (`SessionEnd` can archive the transcript), `UserPromptSubmit`, `PreToolUse`/`PostToolUse` (per tool call; `PostToolUse` sees `tool_response.exit_code`), `Stop`/`SubagentStop`, `PreCompact`, and in newer builds `SubagentStart`, `TaskCreated`/`TaskCompleted`, `PostToolUseFailure`. Hooks fire **inside subagents too**, and the input carries `agent_id`/`agent_type`. Timing: a hook captures wall-clock by recording timestamps at `SessionStart` vs `SessionEnd`, or per-tool latency at `PreToolUse` vs `PostToolUse`. `${CLAUDE_SESSION_ID}` (v2.1.9+) and `transcript_path` are available to hooks, so a `SessionEnd`/`Stop` hook is the natural place to run `ccusage`/a parser over the just-finished transcript and append one committed telemetry record. This is your "mechanisms not prose" enforcement point, fully local.

**(d) What requires a server / plan.** Fully local, no server: JSONL transcripts; OTel `console` and `prometheus` exporters; hooks; `ccusage`. Requires a locally-run process (justifiable, not SaaS): an OTLP collector writing to SQLite/DuckDB/ClickHouse; Grafana/Prometheus dashboards. Requires an enterprise/admin plan or external endpoint: the Usage/Cost and Claude Code Analytics Admin APIs (Admin API key, org account); any hosted backend (Honeycomb, Datadog, SigNoz Cloud, Grafana Cloud, CloudWatch).

### Q2 — Equivalents for the other agents

| Agent | Local session log | Token/cost in log | Native OTel | Usage-unit gotcha | Maintenance signal |
|---|---|---|---|---|---|
| **Codex CLI** (OpenAI) | `~/.codex/sessions/*.jsonl` (+ `archived_sessions/`) | Yes, since the `token_count` event landed 2025-09-06; earlier logs lack tokens | Yes — `[otel]` in `~/.codex/config.toml`; `service.name=codex_exec`/`codex_tui`, events share `conversation.id` | Token-based rate card + reasoning-weighted 5-hour limits rolled out April 2026; `/status` and `/statusline` show session tokens | Actively developed; log format still evolving (ccusage marks Codex support "experimental") |
| **Gemini CLI** (Google) | `.gemini/telemetry.log` (OTel log file) | Yes — GenAI semconv `gen_ai.client.token.usage`; also `user_added_lines`/`user_removed_lines`, tool execution breakdown | Yes — OTel-native; config in `.gemini/settings.json`; `--telemetry`/`--telemetry-target local\|gcp` | Free-tier quota is request/day-based, not token-based | Actively developed (Google-maintained OSS) |
| **Copilot CLI** (GitHub) | No documented local token log | No token log; usage is server-side | No documented OTel for the CLI | **Premium requests / AI Credits** — GitHub replaced Premium Request Units with token-based **AI Credits on 2026-06-01**; CLI *does* consume premium requests (Free 50/mo; Pro 300; Pro+ 1,500; Business 300/user; Enterprise 1,000/user; overage $0.04/request) | GitHub-maintained; billing model changed twice in 2025–26 |
| **Grok CLI** (community, superagent-ai) | `~/.grok/logs/unified.jsonl` (token counts) + per-session bundles; `~/.grok/sessions/.../summary.json` (final model) | Yes — tokens in unified log; cache-creation split missing; session-bundle counts cumulative-only | No native OTel found | xAI has **no official CLI**; billing via credits/API; mid-session model switches need the timeline, not just `summary.json` | superagent-ai/grok-cli ~2.4k stars, **last update Nov 2025** (stale); lalomorales22/grok-4-cli is a separate small project |

**Common denominator for fair cross-provider comparison:** wall-clock duration, tokens in / out (raw counts, not cost), tool-call counts, and a task outcome/verdict. These four exist (or can be derived) everywhere. **Cost does not normalize**: Claude Code and Codex report USD or tokens; Copilot meters premium requests / AI credits that map to tokens only through opaque, changing multipliers; Grok uses credits. **Honest normalization rule:** store the raw provider unit (tokens, premium requests, credits) *and* a separately computed token-based cost estimate using a single pricing table (e.g. LiteLLM's dataset, which ccusage already uses), clearly labeled as an estimate, and never sum subscription-plan usage with API-billed dollars.

### Q3 — Existing open-source tooling (so you don't hand-roll)

- **ccusage** (`ryoppippi`/now `ccusage/ccusage` org, MIT) — the de-facto Claude Code usage analyzer, actively developed in 2026 with 100+ releases (a recent Rust rewrite; version snapshots vary between v18.x and v20.x across cached pages — verify the current tag live). Reads `~/.claude/projects` JSONL; commands `daily`/`weekly`/`monthly`/`session`/`blocks` (5-hour billing windows); **`--json` for machine-readable output**; **`--offline`** uses pre-cached LiteLLM pricing (Claude models only); `--breakdown` for per-model cost; tracks cache-creation/cache-read tokens separately; costs are estimates from LiteLLM pricing. **Now also reads Codex logs** (companion `@ccusage/codex`; unified binary detects claude/codex/gemini/copilot/qwen/… sources). This is your fastest extraction win — offline + machine-readable — and feeds a committed telemetry log directly.
- **claude-usage-analyzer (ccwhy)** — complements ccusage: attributes *why* tokens were spent (tool attribution, "controllable token sinks"), JSON output.
- **aarora79/claude-code-usage-analyzer** — wraps ccusage + LiteLLM; JSON + Markdown; P95/median/mean stats; uv-based (fits your stack).
- **Session viewers/exporters (read-only, local):** simonw/claude-code-transcripts (JSONL→HTML; note its `web` command is currently broken per issue #77), claude-devtools, lm-assist, PixelPaw-Labs/codex-trace (Codex JSONL viewer with token counts, live SSE tail), ceshine's gemini-cli-usage-analyzer (converts `.gemini/telemetry.log` to JSONL with archiving/dedup).
- **Cross-tool local dashboards:** Token Telemetry (tokentelemetry.com) and SuperBased both read local logs for 13–28+ agents (Claude Code, Codex, Gemini, Copilot, Grok, etc.), 100% local, localhost dashboard — useful as a zero-plumbing viewer but not a committed-artifact source.
- **Local OTel → embedded DB:** `smithclay/duckdb-otlp` (DuckDB extension ingesting OTLP over HTTP/gRPC, storing to DuckDB/Parquet — a genuinely server-light "collector"); InfluxData Telegraf OTel→DuckDB; ClickStack/OpenInsight for ClickHouse if you outgrow SQLite. These satisfy "library-first, local, no SaaS" for OTel storage.
- **Anthropic's own reference:** `anthropics/claude-code-monitoring-guide` (Docker Compose for OTel + Prometheus + Grafana + report templates) — a starting point, but a running-server stack; adopt selectively.

### Q4 — Which metrics actually mean something

**Traps.**
- **Lines of code** — the classic anti-metric; high-quality refactors *reduce* LOC, and it's trivially inflated by AI. Claude Code even emits `lines_of_code.count`, so it's tempting; DORA/SPACE guidance is explicit that LOC, commit counts, and PR counts must never be used as productivity proxies or for individual ranking.
- **Self-reported speed** — the METR July 2025 RCT ("Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"; Becker, Rush, Barnes, Rein) recruited 16 experienced OSS developers to complete 246 real tasks in mature repositories (averaging 22,000+ GitHub stars and 1M+ lines of code) that they'd worked on for ~5 years, primarily using Cursor Pro with Claude 3.5/3.7 Sonnet. Developers **took 19% longer** with AI, had forecast AI would make them **24% faster**, and afterward still estimated they'd been **20% faster** — a ~39-percentage-point perception gap. This is the single strongest argument for measuring wall-clock objectively rather than trusting "it felt faster." METR itself now labels the result as historical, saying it "no longer necessarily reflects current AI tools or current developer workflows," and published a late-2025 follow-up in February 2026 — so cite it as an evolving snapshot, not a permanent verdict.
- **Token/cost as a quality proxy** — more tokens ≠ better outcome; contested and not predictive on its own.

**Defensible metrics (always paired with an outcome verdict):**
- **Cost-per-solved-task** — the metric agent benchmarks converge on. Compute cost only over *passing* attempts, or report cost alongside pass@1/pass^k. (Artificial Analysis's Coding Agent Index reports per-task cost, token usage, and wall-clock this way; τ-bench introduced pass^k — the chance *all* k trials pass — the right frame for a governance fleet where consistency matters more than best-of-k.)
- **Wall-clock per completed task** and **active/engaged time** (Claude Code's `active_time.total` separates engaged from idle wall-clock — important, since your shape-S task's "~3 hours" includes gate-mesh waiting, not just model work).
- **Retries and error loops** (`api_error.attempt`, `api_retries_exhausted`, tool `success=false` rates).
- **Edit-acceptance/revert rate** (`code_edit_tool.decision`).
- **Tasks/rows closed per window**, **test runs & failures**, **gate pass/fail** — your audit.py 41-check mesh and pytest results are already outcome-grade signals.

**DORA/SPACE for a one-operator agent fleet.** DORA's four keys (deployment frequency, lead time for changes, change failure rate, time to restore) are *team/system-delivery* metrics — deployment frequency and lead time still measure whether the *system* ships faster, and change-failure-rate maps naturally onto your gate/audit failures. SPACE's operative lesson: **measure at least three dimensions and never a single number** — pair throughput (tasks closed) with quality (gate/test pass, revert rate) and cost (tokens/$), and treat Activity counts as diagnostic, never as the target. Do **not** build individual-ranking dashboards; the principle protects you when models are the "individuals" being compared — rank on outcome quality, not activity volume. The 2025 research consensus ("The Fast and Spurious: Developer Productivity with GenAI," plus Anthropic-cited findings that AI assistance can impair debugging/code-reading without average efficiency gains) is that GenAI productivity claims are contested and self-report is unreliable — so your telemetry should privilege *measured outcomes over felt speed*.

### Q5 — Fair model-comparison methodology

**Nondeterminism is the central threat.** Temperature 0 does **not** give reproducibility: batched inference, MoE routing, and non-associative floating-point accumulation cause run-to-run variation. Measured determinism rates vary wildly by model and prompt length — one benchmark found Claude 4.5 at 100% byte-identical on a short prompt but 20% on a long open-ended one, with GPT-class models at 0% on the long prompt. Agentic evals compound this (prompt sensitivity, tool-order variation). **Implication:** a single run per model is uninformative; if within-model variance exceeds the between-model difference, the comparison is noise. (Deterministic-inference modes are emerging — e.g. SGLang's batch-invariant kernels — but assume nondeterminism by default.)

**Design rules for an internal bake-off:**
1. **Paired within-task design** — run every model on the *same* seeded tasks; compare per-task, not pooled, to control task-difficulty heterogeneity.
2. **Repeat runs** — uncertainty-quantification literature recommends increasing repeats until the prediction-interval width falls below a threshold (~0.01); practically, **5–10 rollouts per model per task** is the common floor (agent benchmarks use k=5–8). Report **distributions**, not single scores.
3. **Statistics for small samples** — **task-level bootstrap 95% CIs** (resample tasks with replacement, e.g. 10,000 resamples, as APEX-Agents does) and **paired tests** across the matched task set; consider sequential testing to stop early when a difference is clear.
4. **Control context/cache state** — fix repo state, standardize prompt-cache between runs (cache-read tokens are logged, so you can *verify* cache state rather than assume it), pin uv/tooling, and record `effort`/reasoning setting per run (Claude Code logs `effort`; treat your "opus-by-default keyed on context load" rule as a controlled variable).
5. **Control confounds** — randomize task order, interleave models (not model-A-all-morning), log time-of-day/API-latency, and **freeze model versions** for the window (a mid-eval model update invalidates the comparison; record `app.version` and model id).

**SWE-bench critiques — why an internal benchmark must differ.** Aleithan et al., "SWE-Bench+" (arXiv:2410.06992), found **32.67% of "successful" patches involved solution leakage** ("solutions were directly provided in the issue report or the comments") and **31.08% passed on weak test cases**; filtering both **dropped SWE-Agent+GPT-4 from 12.47% to 3.97%**. The "SWE-Bench Illusion" paper (arXiv:2506.12286) showed models recall buggy file paths up to 76% from issue text alone (vs ~53% off-benchmark) — memorization/contamination, not reasoning. OpenAI audited o3 failures, found the majority were test-harness flaws rather than model limitations, and on **February 23, 2026 stopped reporting SWE-bench Verified** citing contamination across GPT-5.2, Claude Opus 4.5, and Gemini 3. Even SWE-bench Pro containers leaked future git history recoverable via `git log`/`git show`. **Your internal corpus must therefore:** be private and never published (no training-data contamination), use *your* repos and gate mesh (ecological validity), have *robust* tests (not vacuous ones), sanitize git history so the fix isn't reachable, and be regenerated/rotated over time.

### Q6 — Building a seeded-defect corpus for an internal bake-off

**Generation strategies (use a blend):**
- **Mutation testing tools as defect generators (Python):** **mutmut** (v3+, `libcst`-based, actively maintained; requires fork support, so on Windows run under WSL — matches your git-bash/WSL reality; `mutmut apply` writes a mutant to disk, `mutmut browse` to inspect), **cosmic-ray** (v8.x, actively developed, distributed runs), **mutatest**, MutPy, Poodle. Comparative studies (Brazilian Symposium on Software Quality; IEEE) show they differ in operators and mutant difficulty — use more than one operator set. Mutation operators cheaply produce large, stratifiable defect volumes but many are trivial or equivalent.
- **Hand-authored realistic defects** — necessary for classes mutation can't express: **vacuous test** (assert-nothing), **fail-open exception handler** (bare `except: pass`), **stale locator/selector**, **corrupted fence/format** (broken JSONL/markdown), silent type coercions. These match your fleet's real failure modes and resist memorization.
- **Mining real historical bug-fix commits** — highest ecological validity but the **SZZ algorithm is known-inaccurate** (refactoring and cosmetic edits corrupt bug-inducing-commit attribution; see "SZZ revisited"/"Issues with SZZ"). Use **Defects4J** (initially 357 real Java bugs from 5 projects) and **BugsInPy** (493 real bugs from 17 real-world Python programs, each project with 10,000+ stars, ~831 man-hours to build; github.com/soarsmu/BugsInPy) as *structural templates* — but note Defects4J bugs are old (≤2020) and likely in LLM training data, so don't reuse them verbatim; prefer GitBug-style recent, reproducible packaging.

**How many defects?** For a usable signal with paired design and bootstrap CIs, aim for **40–80 seeded defects minimum**, stratified across classes (agent benchmarks operate at 40–113 tasks; Claw-SWE-Bench's "Lite-80" argues 80 preserves the ranking/cost structure of a 350-set). Start at ~40 to get moving, grow to ~80+ as variance demands.

**Classification & stratification:** tag each defect with `defect_class` (vacuous-test, fail-open, stale-locator, corrupted-fence, off-by-one, wrong-boundary, dropped-error-path, …), `difficulty`, `repo`, `subsystem`, and `detectable-by` (which gate/test *should* catch it). Stratify so no class dominates and you can report per-class detection.

**Prevent context leakage:** store the corpus in a **separate private repo or an encrypted/`.gitignore`d path** the agent's tools cannot read; inject defects into a throwaway worktree at eval time; sanitize git history (prune the fix commit) so `git log`/`git show` can't recover the answer; never put defect descriptions in CLAUDE.md, prompts, or committed artifacts the agent sees.

**Scoring (four axes):** **detection rate** (did the agent find it), **fix correctness** (does the *robust* hidden test pass — not a weak one), **false-positive rate** (did it "fix" non-defects or introduce regressions), and **cost & time per defect** (tokens, USD estimate, wall-clock). Report per-class and as distributions with CIs. **Admission rule:** a new model lane is admitted only if its paired detection + fix-correctness on the seeded corpus is statistically ≥ the incumbent baseline (bootstrapped) at acceptable cost.

**Reproducibility & versioning:** pin the corpus with a version tag and a manifest (seed, tool versions, mutation operators, defect hashes); store as committed JSON/YAML defect specs + a deterministic applier script; record the uv-pinned environment; regenerate on a cadence to stay ahead of contamination.

### Q7 — The telemetry record itself

**Standards alignment first.** Anchor field names to the **OpenTelemetry GenAI semantic conventions** (open-telemetry/semantic-conventions-genai): model calls, tool executions, **agent spans** (`gen_ai.operation.name` = `invoke_agent`/`create_agent`, `gen_ai.agent.name`), token-usage attributes, and MCP tool spans. The GenAI SIG (formed April 2024) now covers agent orchestration and tool calling; conventions are at ~v1.37–1.41 and still evolving (they physically moved repos in 2026 — pin the commit you align to). Claude Code already emits several of these keys (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.response.id`, `gen_ai.tool.call.id`), and OpenInference/MLflow/Datadog all consume the same vocabulary — so aligning makes your log portable, not invented.

**Proposed per-session / per-arc record (one committed JSONL line per session):**
```
schema_version, session_id, parent_session_id, repo, worktree/lane,
task_ids[], row_ids[], model, provider, effort/reasoning_setting,
start_ts, end_ts, wall_clock_s, active_time_s,
phase_timings{plan, implement, test, gate},
tokens{input, output, cache_read, cache_creation},
cost_usd_estimate, cost_source(litellm|otel|analytics_api),
provider_native_unit{premium_requests|credits|null},
tool_calls{total, by_tool{...}}, subagent_count,
retries, api_errors, refusals,
tests_run, tests_failed, xdist_workers,
gate_results{audit_checks_passed/failed, ruff, pre_commit_stages},
outcome_verdict(pass|fail|partial), human_touches, interruptions,
cc_app_version, corpus_version(if bake-off)
```

**Storage & versioning (library-first, local):**
1. **Committed JSONL, appended per session** (matches your existing JSONL-artifact discipline): a `SessionEnd`/`Stop` hook runs ccusage + gate parsers and appends one line to `telemetry/sessions.jsonl`, committed. Human-diffable, git-versioned, zero server. **Best default.**
2. **Local DuckDB/SQLite** for query/aggregation once the JSONL grows: load the committed JSONL into DuckDB on demand (DuckDB reads JSONL natively) or run `smithclay/duckdb-otlp` if you go the OTel route. Keep the JSONL as source of truth; treat the DB as a derived, rebuildable cache (don't commit the binary DB).

**PII/secret leakage avoidance:** transcripts and raw API bodies can contain secrets and source. **Never** commit raw transcripts or set `OTEL_LOG_RAW_API_BODIES`/`OTEL_LOG_TOOL_CONTENT` into a committed log. Emit only **structured metrics + hashes/ids** to the committed record; keep content redacted (Claude Code's defaults already redact prompts/responses/tool-content). Add a `PreToolUse` hook blocking `.env` reads (exit code 2) and run a secret-scanner in pre-commit over the telemetry file. If using OAuth, note `user.email` appears in OTel attributes — redact at the collector or omit for a one-operator fleet.

**Retention/rotation:** rotate `sessions.jsonl` monthly (e.g. `telemetry/2026-08.jsonl`); keep aggregates indefinitely, but **prune or archive raw transcripts** on a short window (e.g. 30 days) since they carry secret-leak risk. A `SessionEnd` hook can archive+compress the transcript to a gitignored local store, not the repo.

### Q8 — Minimal starter path

The **single highest-leverage step is #2** (the SessionEnd/Stop hook that runs ccusage and appends a committed telemetry line): it turns already-recorded data into a versioned, queryable artifact and immediately answers "how many tokens/tests/tasks, at what cost, how long" per session — the operator's core question — with S effort and no server.

**Numbered plan:**
1. **(S) Extract now with ccusage.** Run `ccusage session --json` / `daily --json --offline` over `~/.claude/projects`. Mechanism: parser. Collects: tokens, cache split, per-model cost estimate, per-session/day. Answers: "what did each session/day cost in tokens and $, per model." No server. *Do this today.*
2. **(S→M) SessionEnd/Stop hook → committed `telemetry/sessions.jsonl`.** Mechanism: hook + parser. Collects: the Q7 record (ids, model, wall-clock, tokens, tool counts, tests run/failed, gate results, outcome verdict). Answers: "did development get faster/cheaper over time; tasks closed per window." **Highest answers-per-effort.**
3. **(S) Turn on OTel `console`/`prometheus` locally to validate signals**, then (M) point `otlp` at a local `duckdb-otlp` or Prometheus. Mechanism: exporter. Collects: active-time, per-request cost/latency, retries, code-edit decisions, subagent attribution, phase timings (traces beta). Answers: "engaged vs wall time; where retries/errors cluster; per-phase timing."
4. **(M) Extend the hook to the other agents.** Codex (`~/.codex/sessions` + ccusage codex), Gemini (`.gemini/telemetry.log`), Grok (`~/.grok/logs/unified.jsonl`); record provider-native units for Copilot. Mechanism: parser/wrapper. Answers: "cross-provider tokens/wall-clock/tool-calls on the same task."
5. **(L) Build the seeded-defect corpus + paired bake-off harness.** Mechanism: gate + corpus + runner. Collects: detection/fix-correctness/false-positive/cost per defect, ≥5–10 repeats, bootstrap CIs. Answers: "is model X measurably better than the incumbent — admit the lane or not."

**Metric → source → mechanism → cost table:**

| Metric | Source | Collected automatically vs. added | Mechanism | Cost |
|---|---|---|---|---|
| Tokens in/out + cache split | JSONL usage block / OTel `token.usage` | Automatic | ccusage / OTel | S |
| Cost (USD, estimate) | ccusage (LiteLLM) / OTel `cost.usage` | Automatic (estimate) | ccusage / OTel | S |
| Model id, effort, subagent attribution | JSONL / OTel `query_source`,`effort`,`agent.name` | Automatic | ccusage / OTel | S |
| Wall-clock per session | JSONL timestamps / hook ts | Added (hook) | SessionStart/End hook | S |
| Active/engaged time | OTel `active_time.total` | Automatic | OTel exporter | S |
| Per-phase timing (plan/impl/test/gate) | OTel traces (beta) or hook timestamps | Added | traces beta / hook | M |
| Tool-call counts, tool success/error | OTel `tool_result` / JSONL tool entries | Automatic | OTel / parser | S |
| Retries / error loops | OTel `api_error.attempt`,`api_retries_exhausted` | Automatic | OTel | S |
| Edit accept/revert | OTel `code_edit_tool.decision` | Automatic | OTel | S |
| Tests run/failed | pytest output | Added | hook parses pytest/xdist | M |
| Gate results (audit.py, ruff, pre-commit) | your gate mesh | Added | hook/gate | M |
| Outcome verdict (pass/fail/partial) | your gate + human | Added (manual/gate) | gate + annotation | M |
| Tasks/rows closed per window | your backlog | Added | hook + backlog join | M |
| Cross-provider tokens/wall-clock | each agent's local log | Added | per-agent parser | M |
| Detection/fix/false-positive/cost per defect | bake-off runner | Added | corpus + runner | L |

**Minimum observation window before any conclusion is meaningful.** Because of nondeterminism, a *single* task or day proves nothing. For "did development get faster," you need enough *completed tasks* per condition that the paired difference exceeds within-model variance — practically **≥20–40 completed tasks per model/condition, and ≥2–4 weeks** of routine work to average out task-difficulty and time-of-day effects. For the bake-off, **≥40 seeded defects × ≥5 repeats per model**, reported as distributions with bootstrap 95% CIs; admit a lane only when the paired CI excludes zero. One shape-S task taking 3 hours is an anecdote that sets a hypothesis, not a conclusion.

## Recommendations

**Stage 1 — This week (S, no server, library-first):**
1. Run `ccusage` (offline, `--json`) over your Claude Code JSONL to get an immediate baseline of tokens/cost per session and model.
2. Write a `Stop`/`SessionEnd` hook that runs ccusage + parses your audit.py/pytest output and appends one OTel-GenAI-aligned record to a committed `telemetry/sessions.jsonl`. This alone answers most of the operator's questions and is your enforcement mechanism.
3. Add a `PreToolUse` `.env`-block hook and a pre-commit secret-scan over the telemetry file so nothing sensitive lands in git.

**Stage 2 — This month (S→M):** Enable OTel `console` to confirm signals, then run a local `duckdb-otlp` (or Prometheus) collector for active-time, retries, and per-phase timing. Load the committed JSONL into DuckDB for aggregation; keep JSONL as source of truth. Extend parsing to Codex and Gemini logs; record Copilot premium-requests separately.

**Stage 3 — Next quarter (L, the admission gate):** Build the private, versioned seeded-defect corpus (40→80 defects, stratified by class, blend of mutmut/cosmic-ray + hand-authored realistic defects, git-history sanitized, kept out of agent context). Stand up a paired bake-off runner: same defects, ≥5–10 repeats per model, interleaved order, frozen model versions, bootstrap 95% CIs, report distributions. Admit a new model lane only when its paired detection+fix-correctness CI beats the incumbent at acceptable cost/time.

**Benchmarks/thresholds that change the plan:**
- If within-model run variance ≥ between-model difference → increase repeats or declare "no difference"; do not ship a routing change on it.
- If a model update lands mid-window → discard the window and restart (record `app.version`/model id to detect this).
- If cost-per-solved-task rises without a quality gain → the new lane fails admission regardless of raw speed.
- Cross to an OTel collector / server only when local JSONL+DuckDB can no longer answer a question you actually have — justify it against the "no always-running servers" rule each time.

## Caveats
- **Transcript format is unstable and undocumented in detail** — Anthropic explicitly says parsers can break on any release. Pin versions; prefer ccusage/OTel over hand-rolled JSONL parsing; treat cross-file joins as version-specific.
- **All cost figures here are estimates.** ccusage (LiteLLM pricing), and Claude Code's OTel/Analytics costs, are approximations; only your provider's billing console is authoritative. Subscription-plan and API-billed costs are different ledgers — never sum them.
- **Cross-provider cost is not truly comparable.** Tokens/wall-clock/tool-calls are; premium-requests/credits are not. Report raw units + a single-pricing-table estimate, labeled as such.
- **The productivity evidence is genuinely contested.** The METR RCT (19% slower) is one study of early-2025 tools that METR itself now calls a historical snapshot, with a Feb-2026 follow-up; vendor/CEO claims of large speedups coexist with controlled studies finding slowdowns and skill effects. Do not treat either pole as settled — which is exactly why you measure your own outcomes.
- **Benchmark scores (SWE-bench et al.) are contaminated and partly memorized** — do not use public leaderboard scores to pick your model; your private seeded corpus is the decision instrument.
- **Nondeterminism at temperature 0 is real** and can exceed the signal you're testing — single runs are never conclusive.
- **Grok CLI is community-maintained and stale** (superagent-ai, last update Nov 2025); treat any Grok lane as lower-assurance and verify its logging live before relying on it.
- **OTel GenAI conventions and Claude Code's telemetry are both explicitly beta/evolving** (conventions moved repos in 2026; Claude Code OTel and traces are beta) — pin the versions you align to and expect field churn.