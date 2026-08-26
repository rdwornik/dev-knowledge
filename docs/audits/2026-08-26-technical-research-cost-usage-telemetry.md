# Unified Cost-and-Usage Telemetry for a Multi-Agent, Multi-Substrate Solo Dev Fleet

## TL;DR
- **Build a thin "pull-and-join" pipeline, not a platform:** run **ccusage** (local JSONL) for per-tool token/cost, pull each provider's **admin billing API** (Anthropic Usage & Cost, OpenAI Costs, GitHub enhanced-billing `/usage`, Cursor Admin API) into one **DuckDB/SQLite** file on a **GitHub Actions weekly cron**, join to **git/GitHub delivery data**, and render a **Markdown report committed to a repo**. ~90% is existing components; the only custom code is the ~150–250-line join-and-render script.
- **Your subscription spend (Claude Max) will never appear in any billing API** — it is a flat fee. Track it as a *utilization* metric (percent of the 5-hour and weekly windows consumed) plus an *imputed API-equivalent value* computed by pricing the local JSONL token counts against LiteLLM's price catalog. This is how practitioners prove Max is worth it: AgentPlix documented one normal month on a $159/mo Max 5x plan modeling to **$6,600 in API-equivalent cost during a burst month**, and Build This Now pegs break-even at **~$3.33/day of API-equivalent usage for Max 5x and ~$6.67/day for Max 20x**.
- **Two hard gaps to accept up front:** (1) Claude Code *cloud/web sessions* expose almost no programmatic usage data and are the hardest substrate to account for; (2) client-side cost estimates (Claude Code's `/cost`, ccusage, OTel `claude_code.cost.usage`) are explicitly *approximations* that diverge from invoices — the official docs say "Cost metrics are approximations. For official billing data, refer to your API provider." Reconcile monthly against the Anthropic Cost API, which lags ~5 minutes but is authoritative.

## Key Findings

1. **Claude Code has the richest native telemetry of any agent.** Its OpenTelemetry export (opt-in via `CLAUDE_CODE_ENABLE_TELEMETRY=1`) emits exactly 8 metrics — `claude_code.token.usage` (broken down by `input`/`output`/`cacheRead`/`cacheCreation`), `claude_code.cost.usage` (USD), `claude_code.lines_of_code.count`, `claude_code.commit.count`, `claude_code.pull_request.count`, `claude_code.session.count`, `claude_code.code_edit_tool.decision`, and `claude_code.active_time.total` — plus 25+ structured events (`user_prompt`, `tool_result`, `api_request`, `tool_decision`, `subagent_completed`, etc.). It also writes local session JSONL to `~/.claude/projects/**` regardless of plan, which is what ccusage reads.
2. **The price-catalog problem is already solved.** LiteLLM's `model_prices_and_context_window.json` is the de-facto community price catalog that ccusage, tokencost, and many dashboards resolve against; it prices new models automatically as they're added, so subscription token volumes can be valued without hand-maintaining prices.
3. **Every major first-party provider now has a programmatic cost/usage endpoint** — Anthropic (`/v1/organizations/cost_report` + `/usage_report/messages`, Admin key), OpenAI (`/v1/organization/costs` + `/usage/*`, admin key, group by `project_id`), GitHub (enhanced-billing `/usage` + CSV report API), Cursor (Admin API). The Chinese providers (DeepSeek, Moonshot/Kimi, Z.ai/GLM) and xAI are weakest on programmatic billing endpoints; for them, route through a gateway or read local JSONL.
4. **OTel GenAI semantic conventions are NOT stable.** Per OpenTelemetry semantic-conventions v1.42.0 (released June 12, 2026), all `gen_ai.*` attributes/spans/metrics/events were deprecated in the main repo and moved to the dedicated `open-telemetry/semantic-conventions-genai` repository; as of July 17, 2026 none is marked Stable — they remain "Development" status. Don't hard-code attribute strings; isolate them behind a mapping layer.
5. **A self-hosted gateway (LiteLLM Proxy) is the single highest-leverage component** for the API-key traffic (Codex, Grok, Gemini, Chinese models via Anthropic-/OpenAI-compatible endpoints), because it converts N provider billing problems into one spend table with zero per-request markup — but it cannot capture subscription (Max) or compute (Codespaces) spend.

## Details

### (a) Per-tool telemetry-source table

| Tool | What it emits natively | How to capture | Subscription or API | Gaps |
|---|---|---|---|---|
| **Claude Code (local)** | OTel: 8 metrics (`token.usage` split input/output/cacheRead/cacheCreation, `cost.usage` USD, `lines_of_code.count`, `commit.count`, `pull_request.count`, `session.count`, `code_edit_tool.decision`, `active_time.total`); 25+ events (`user_prompt`, `tool_result`, `api_request` w/ `cost_usd`+`cost_usd_micros`, `tool_decision`, `subagent_completed`, etc.). Local JSONL in `~/.claude/projects/**`. Slash cmds `/usage` (aliases `/cost`,`/stats`), `/context`. | Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `OTEL_*` exporters → OTLP collector; OR read JSONL with **ccusage** (no infra). | Both — JSONL written on Pro/Max/API alike | Cost is a **client-side estimate** ("Cost metrics are approximations. For official billing data, refer to your API provider"). Pre-v2.1.214 multi-frame streams inflated cost/token metrics. OTel config read only at startup; when `prometheus` is the sole exporter, USD/tokens/s units are omitted to keep the scrape valid. |
| **Claude Code (Anthropic cloud/web sessions)** | Runs at claude.ai/code on Anthropic infra; monitorable in UI/mobile app only. | No documented programmatic usage export; `--teleport` a session to local to get JSONL. | Subscription | **Hardest substrate** — no session summaries/export API; near-invisible to automation. |
| **OpenAI Codex CLI** | Local session JSONL `~/.codex/sessions/YYYY/MM/DD/*.jsonl` (token counts); OTel via `[otel]` in `~/.codex/config.toml` (logs/traces/metrics; `service.name=codex_exec`/`codex_tui`, shared `conversation.id`); anonymous health metrics to OpenAI by default. | ccusage `codex` source; or OTel exporter; or the cost-log hook pattern. | API (or ChatGPT plan auth) | OTel behind feature flag in source builds (on in prebuilt binaries); tool results can leak file contents. |
| **Gemini CLI** | OTel-native: `gen_ai.client.token.usage`, `gen_ai.client.operation.duration`, `gemini_cli.file.operation.count` (incl. `user_added_lines`/`user_removed_lines`), plus session/tool/prompt logs. Pre-built GCP Monitoring dashboard (tokens, LoC added/removed, API/tool calls, active users). | `.gemini/settings.json` telemetry block → local file, OTLP collector, or GCP; ccusage `gemini` source. | API / Code Assist | Local logs to `.gemini/telemetry.log`; GCP path needs a project. |
| **Grok CLI (xAI)** | ccusage has a `grok` source (local usage). xAI API is OpenAI-compatible (`/v1/chat/completions`), returns token usage in responses. | ccusage `grok`; or gateway; or parse response usage. | API | No first-party programmatic spend/usage admin API found; rely on console + gateway. |
| **Cursor** | Admin/Analytics API: per-member spend, tokens, LoC, acceptance rate, `chargedCents`/`cursorTokenFee` per event, `conversationId` join key to AI Code Tracking API. | Cursor Admin API (Bearer team key, read-only + `set_spend_limit`); community `cursor-admin-api-exporter` (Prometheus) or `cursor-usage` MCP. | Subscription + usage-based | Teams/Enterprise plans only for full API; analytics history ~30 days; docs lag actual response fields. |
| **ccusage (aggregator)** | Unified daily/weekly/monthly/session/`blocks` (5-hr windows) across Claude, Codex, Gemini, Grok, Copilot, Kimi, Qwen, OpenCode, Droid, etc. Prices via LiteLLM catalog. | `npx ccusage@latest` (Node); library mode; `@ccusage/mcp`. Windows-friendly (npx). | Reads local JSONL (works for subscription usage) | Only sees what's on local disk (misses cloud/web sessions, other machines); cost = estimate. |

**Community parsers & maintenance status (Aug 2026):** **ccusage** is actively maintained (v20.x, published within days); **better-ccusage** is a fork adding Z.ai/GLM/Kimi/MiniMax/Qwen model support; **Claude-Code-Usage-Monitor** (Maciek-roboblog) gives real-time burn-rate/limit predictions; **claude-code-otel** (ColeMurray) is a Docker-Compose OTel→Prometheus/Loki/Grafana stack; **claude-code-usage-analyzer** (aarora79) shells out to ccusage + LiteLLM pricing and ships a `/tokenomics-dashboard` skill; **claude-usage** (phuryn) and **claude-code-usage-tracker** (codeinaire, SQLite + `SessionEnd` hook auto-sync) are local dashboards.

### Subscription accounting (Claude Max)

Max subscription usage is a **flat fee** ($100 Max 5x, $200 Max 20x per month) and appears in **no** billing API. The right metrics:
- **Utilization** — percent of the **5-hour rolling window** and the **weekly caps** consumed (there are two weekly caps: an overall cap plus a model-specific one). Anthropic doesn't publish exact token numbers, so treat any figure as an estimate; `/usage` shows progress bars for Pro/Max.
- **Imputed API-equivalent value** — price the local JSONL token counts (including the huge cache-read volume — often >90% of tokens in large-repo sessions) against the LiteLLM catalog. Published practitioner cases: AgentPlix's normal month on $159 Max 5x modeled to **~$6,600 API-equivalent in a burst month**; Botfarm measured Max 5x delivering **~$523/week of API compute for $25/week (~20x)**; Build This Now puts break-even at **~$3.33/day API-equivalent for Max 5x and ~$6.67/day for Max 20x**. Rule of thumb: 3+ days/week with Opus → Max wins; 1–2 days/week or mostly Sonnet → API wins.

### (b) Per-provider billing-API table

| Provider | Endpoint(s) | Granularity / grouping | Auth | Lag / gaps |
|---|---|---|---|---|
| **Anthropic (Console/Platform)** | `/v1/organizations/usage_report/messages` (tokens), `/v1/organizations/cost_report` (USD) | Usage: `1m`/`1h`/`1d` buckets; group/filter by `api_key`, `workspace`, `model`, `service_tier`, `context_window`, `inference_geo`, `speed`(beta). Cost: **`1d` only**, group by `workspace_id` or `description` (model/geo surface as parsed fields). | **Admin key** `sk-ant-admin01-…` (`x-api-key` + `anthropic-version`); unavailable for individual accounts; Enterprise uses Analytics key; not available on AWS. | "Usage and cost data typically appears within 5 minutes… delays may occasionally be longer." Poll ≤1/min. Default-workspace rows have `null` workspace_id; Workbench usage has `null` api_key_id. Priority-tier costs excluded from cost endpoint. CSV export from Console UI too. |
| **OpenAI** | `/v1/organization/costs`; `/v1/organization/usage/{completions,…}` | Costs: `1d` buckets, group by `project_id`, `line_item`, `api_key_id`; limit 1–180. Usage: minute/hour/day, filter by key/project/user/model. | Admin/org key (`OpenAI-Organization` header) | UTC; dashboard exports ≤60 days; some report 404s on costs endpoint (permissions/path). Tag spend via **projects**. |
| **Google/Gemini** | No dedicated LLM cost REST endpoint; costs land in Google Cloud Billing; Gemini CLI usage via OTel → Cloud Monitoring. | Cloud Billing granularity (project/SKU/day) | GCP IAM / service account | LLM-specific cost attribution requires GCP billing export + OTel; no simple per-key token-cost endpoint. |
| **xAI (Grok)** | OpenAI-compatible chat endpoint returns usage; no first-party admin cost API surfaced. | Console only | API key | Programmatic spend weak; use gateway. |
| **DeepSeek** | Balance endpoint + console; OpenAI- and Anthropic-format compatible. | Console | API key | No rich per-project cost API; use gateway/local JSONL. |
| **Z.ai / GLM** | Console; used via Claude-Code / Anthropic-compatible endpoint (better-ccusage tracks it). | Console | API key | No documented programmatic cost API; capture via ccusage/gateway. |
| **Moonshot / Kimi** | Console + balance; ccusage `kimi` source. | Console | API key | Same as above. |
| **OpenRouter** | Own accounting + activity/credits endpoints; per-request cost in response. | Per-request, per-model, per-key | API key | 5.5% credit-purchase fee (markup); its accounting is a genuine multi-provider pane. |
| **GitHub** | Enhanced-billing `/organizations/{org}/settings/billing/usage` and `/users/{user}/settings/billing/usage`; async CSV report API (`…/settings/billing/reports`); legacy Actions billing (`/orgs/{org}/settings/billing/actions`). | `/usage` returns per-day line items: `product` (Actions/Codespaces), `sku` (e.g., "Codespaces Compute 8-core"), `quantity`, `unitType` (minutes / core-hours / GB-hours), `pricePerUnit`, `netAmount`, repo name. Query by year/month/day. | Fine-grained PAT ("Administration"/"Plan" read) or classic `repo`/`admin:org`; CSV report needs `manage_billing:enterprise`. | `hour` granularity removed (2026); day = daily totals. Codespaces billed as **core-hours (compute) + GB-hours (storage)** separately; base dev-container storage is free. No per-"project" tag — segment by repo. |

### (c) Tooling landscape & library-first recommendation

| Category | Tool | Self-host vs SaaS | Price | Windows | Multi-provider pane? | Maintenance |
|---|---|---|---|---|---|---|
| **Gateway** | **LiteLLM Proxy** ⭐ | Self-host (Docker + Postgres) | OSS free; you pay providers directly, **zero markup** | Yes (Docker/WSL) | **Yes** — 140+ providers, 1,892 models, spend logs priced by built-in catalog | Very active (53K+★, 240M+ Docker pulls) |
| Gateway | Portkey | SaaS + OSS core | $49/mo + $9/100k logs | via SaaS | Yes | Active |
| Gateway | Helicone | SaaS + self-host | free tier; 10k req/mo | via SaaS | Yes (observability-led) | **Maintenance mode** since Mintlify acquisition (Mar 2026) |
| Gateway | Cloudflare AI Gateway | SaaS (edge) | Free at moderate vol | Yes | Yes; <10ms | Active |
| Gateway | OpenRouter | SaaS | 5.5% credit fee | Yes | Yes (its own accounting) | Active |
| Gateway | Bifrost | Self-host | OSS | Yes | Yes; high-RPS | Active |
| **Observability** | Langfuse | Self-host (MIT) or Cloud | Self-host free; Cloud Hobby free/Core $29/Pro $199 | via Docker | Yes (token+cost capture) | Active; acquired by ClickHouse Jan 2026 |
| Observability | Traceloop/OpenLLMetry, Arize Phoenix, Braintrust, LangSmith, W&B Weave | mixed | mixed | mixed | Yes | Active |
| Observability | SigNoz / Grafana+Prometheus+Loki | Self-host | OSS | Docker | Yes; ready-made Claude Code + Codex dashboards | Active |
| **Price catalog** | **LiteLLM `model_prices_and_context_window.json`** ⭐ | file/library | free | Yes | n/a (feeds everything) | Active, tracks newest models |
| Price catalog | tokencost | library | free | Yes | n/a | Active |
| **Metering** | OpenMeter, Lago | self-host/SaaS | OSS/paid | Docker | usage-metering grade | Active — overkill for solo |
| **Delivery** | Apache DevLake ⭐ | Self-host | OSS | Docker | DORA + Copilot/AI-cost & "AI Cost-Efficiency"/"Multi-AI Tool Comparison" dashboards | Active |
| Delivery | Sleuth, LinearB, Haystack, DX/getdx | SaaS | paid | n/a | DORA; AI-cost dimension emerging | Active |

**Library-first recommendation set:** **ccusage** (local per-tool) + **LiteLLM Proxy** (all API-key traffic, one spend table) + **LiteLLM price catalog** (valuation) + provider **Admin billing APIs** (reconciliation) + **DuckDB** (store/join) + **GitHub Actions** (schedule) + Markdown/**Grafana** (render). Optional: **Langfuse** or **SigNoz** if you want a hosted dashboard/traces instead of Markdown.

### (d) OTel GenAI semantic conventions status (2026)
As of mid-2026 every `gen_ai.*` span/metric/attribute is **Development** (formerly "experimental") status — none Stable — and the conventions moved to a dedicated repo (`semantic-conventions-genai`) in v1.42.0 (June 12, 2026). Standard metrics in use: `gen_ai.client.token.usage` (histogram), `gen_ai.client.operation.duration`. **Datadog** was among the first commercial platforms to natively support v1.37+ GenAI conventions; adoption is real but fragmented. Claude Code, Codex, Gemini CLI, and VS Code Copilot already emit GenAI traces. **Implication:** pin the version and isolate attribute strings behind a thin mapping layer; don't treat names as a frozen contract.

### (e) Joining spend to delivered output
- **Native:** Claude Code emits `commit.count`, `pull_request.count`, `lines_of_code.count`, and `code_edit_tool.decision` (accept/reject) directly; Anthropic's Claude Code usage analytics correlates session activity with GitHub commits/PRs (monthly, resets each month). Cursor exposes an AI Code Tracking API joined via `conversationId`.
- **Git-trailer attribution:** Claude Code appends `Co-Authored-By: Claude <noreply@anthropic.com>` + a "Generated with Claude Code" PR footer **by default** (configurable via the `attribution` object in settings.json; set to `""` to disable; `CLAUDE_CODE_SUPPRESS_SESSION_ATTRIBUTION` handles cloud). Aider adds `(aider)`; Codex/Copilot/Cursor add none. A proposed convention (RAI footers) distinguishes `Assisted-by` / `Co-authored-by` / `Generated-by` + `Signed-off-by`. You can `git log --grep` these trailers to count AI-touched commits.
- **DORA tooling:** **Apache DevLake** (OSS, self-host) is the standout — it ingests GitHub/GitLab/Jira, computes DORA with Elite/High/Medium/Low benchmarking, and already ships AI dashboards ("AI Cost-Efficiency," "Multi-AI Tool Comparison," Copilot impact via `gh-devlake`). Google's Four Keys is a lighter OSS option. SaaS: Sleuth, LinearB, Haystack, DX.
- **"Cost per merged PR / shipped change":** compute as (period AI spend incl. imputed subscription value) ÷ (merged PRs or deploys) from GitHub data.
- **Pitfalls (with hard data):** LoC is a poor proxy — AI inflates PR size and volume. Faros AI's 2025 study of 10,000+ developers across 1,255 teams ("The AI Productivity Paradox") found that high-AI-adoption teams "complete 21% more tasks and merge 98% more pull requests, but PR review time increases 91%," with average PR size up 154% and bugs up 9%; its larger 2026 "Acceleration Whiplash" report (22,000 developers, 4,000+ teams) found median PR review time up 441.5%, incidents per PR up 242.7%, and code churn up 861%. So rework/churn and unmerged/abandoned work badly distort cost-per-PR; commit-level attribution is coarse and self-reported; and `Co-Authored-By` pollutes git blame and contribution graphs.

### RECOMMENDED MINIMAL ARCHITECTURE (for exactly this user)

**One private "telemetry" GitHub repo** containing a scheduled workflow + a Python script + a committed report.

**Data sources → collector (weekly GitHub Actions cron):**
1. **Local machine (Windows/PowerShell):** ccusage runs on the workstation (a Scheduled Task or a `SessionEnd` hook) writing `ccusage weekly --json` for Claude Code, Codex, Gemini, Grok into the repo (or to object storage). This captures **subscription + local API** token/cost estimates and per-project breakdown (ccusage groups by project).
2. **API-key traffic:** point Codex, Grok, Gemini, Cursor, and the Chinese models (DeepSeek/GLM/Kimi via their Anthropic-/OpenAI-compatible endpoints) at a **self-hosted LiteLLM Proxy** (one small VM + Postgres, or local Docker). One spend table, priced with zero markup, tagged per virtual key = per project.
3. **Provider reconciliation (in the Action):** call **Anthropic Cost API** (`cost_report`, Admin key), **OpenAI** `/v1/organization/costs` (group by `project_id`), **GitHub** enhanced-billing `/usage` (Codespaces core-hours + Actions minutes, per repo), **Cursor** Admin API. Store secrets in GitHub Actions encrypted secrets.
4. **Delivery data:** GitHub REST (merged PRs, commits, deploys) + `git log --grep 'Co-Authored-By: Claude'` counts.

**Store:** a single **DuckDB** file (or SQLite) committed/artifacted in the repo — no server. **Join** spend (per provider × substrate × project) to delivery (PRs/commits) and compute cost-per-merged-PR and imputed-Max-value.

**Render:** a **Markdown report committed to the repo** each Monday (diffable, zero-hosting), optionally also pushed to a Grafana Cloud free dashboard.

**What must be custom, and why:** only the **~150–250-line join-and-render script**. No existing tool joins *subscription-imputed value + API billing + Codespaces/Actions compute + git delivery* into one per-project view for a one-person fleet — each ingredient exists, but the join key (project) is not something any provider tags natively, so you must map (ccusage project path ↔ LiteLLM virtual key ↔ GitHub repo) yourself. Everything else is off-the-shelf.

**Minimum viable version (if you do nothing else):** `npx ccusage@latest weekly` in a Windows Scheduled Task + the GitHub enhanced-billing `/usage` call + a one-file Python script that prints Markdown. That alone answers "what did I spend, per tool, per week" and "Codespaces/Actions compute" without any server.

### (f) Phased adoption plan
- **Week 1 (zero infra):** Enable ccusage on the workstation (`npx ccusage@latest`); confirm `~/.claude/projects/**` is populating; create GitHub **budgets** for Codespaces + Actions; create the Anthropic Admin key (`sk-ant-admin…`) and OpenAI admin key; write the one-file Python script that pulls GitHub `/usage` + Anthropic `cost_report` + ccusage JSON and prints Markdown. Run it manually once.
- **Week 2–3:** Move it into a **GitHub Actions weekly cron**; add DuckDB storage + the delivery join (`git log` + PR counts); commit the Markdown report. Add the imputed-Max-value calc (ccusage tokens × LiteLLM prices).
- **Month 2:** Stand up **LiteLLM Proxy** and route Codex/Grok/Gemini/Chinese-model API traffic through it (per-project virtual keys). Add Cursor Admin API. Reconcile estimates vs invoices monthly.
- **Later / optional:** Add **DevLake** for DORA + AI-cost dashboards, or **Langfuse/SigNoz** for hosted dashboards and traces; enable Claude Code **OTel** export to that backend if you want live metrics beyond weekly.
- **Thresholds that change the plan:** if monthly API-key spend exceeds ~$200 or you add more machines, promote LiteLLM to always-on and add Postgres HA; if you collaborate/hire, move from ccusage-per-machine to gateway-first; if cloud/web Claude sessions become material, the only recourse is `--teleport`-ing them local or manual logging.

### Anti-patterns checklist
- ❌ Treating Claude Code `/cost`, ccusage, or `claude_code.cost.usage` as ground-truth billing — they are **approximations** ("For official billing data, refer to your API provider"); reconcile against the Anthropic **Cost API** monthly.
- ❌ Expecting Max/subscription usage in any billing API — it's flat-fee; track utilization + imputed value instead.
- ❌ Ignoring **cache-read/cache-write** token pricing — cache reads dominate large-repo sessions (>90% of tokens) and are priced far below input; use the LiteLLM catalog which models all four token types.
- ❌ Paying gateway/aggregator **markups** (OpenRouter 5.5%, per-log fees) when self-hosted LiteLLM has zero markup — unless you value the zero-ops.
- ❌ Assuming any provider tags spend by **project** — none do natively; you must map project ↔ virtual key ↔ repo yourself.
- ❌ Conflating Codespaces **compute (core-hours)** with **storage (GB-hours)** — they bill separately; base dev-container storage is free.
- ❌ Hard-coding OTel `gen_ai.*` attribute names — they're pre-stable (Development status, June 2026 repo split); isolate behind a mapping layer.
- ❌ Using **lines-of-code** as a productivity/ROI proxy — inflated by AI (Faros: PR size +154%, review time +91%); prefer cost-per-merged-PR with churn caveats.
- ❌ Multi-account/multi-key attribution drift — default-workspace rows return `null` IDs in Anthropic; Workbench usage has `null` api_key_id; name and segregate keys per project.
- ❌ Building a telemetry system that costs more than the spend it tracks — for a solo dev, avoid self-hosted Langfuse/Datadog ($200–800+/mo infra + eng time); the Markdown-in-repo + DuckDB + Actions approach is near-free.

## Recommendations
1. **Start this week with ccusage + GitHub `/usage` + a one-file script → Markdown.** This is the MVP and answers most of the question with zero servers.
2. **Automate it in GitHub Actions on a weekly cron** with secrets for the four admin keys; store to DuckDB; commit the report. Cron on Actions is reliable enough for weekly (schedules can lag a few minutes — acceptable weekly).
3. **Add LiteLLM Proxy in month 2** to collapse all API-key providers (Codex, Grok, Gemini, DeepSeek, GLM, Kimi) into one zero-markup spend table tagged per project. This is the single biggest simplification.
4. **Value your Max subscription monthly** (ccusage tokens × LiteLLM prices) and compare to the flat fee to prove ROI; watch your 5-hour/weekly utilization to decide Max 5x vs 20x vs API (break-even ~$3.33/day and ~$6.67/day API-equivalent respectively).
5. **Reconcile estimates against invoices monthly** via the Anthropic Cost API and OpenAI Costs API; treat client-side numbers as directional.
6. **For delivery joins, keep the Co-Authored-By trailers on** and count AI commits/PRs via `git log`/GitHub API; adopt DevLake only if you want formal DORA.
7. **Accept the two gaps** (cloud/web Claude sessions; per-project tagging) explicitly in the report rather than over-engineering around them.

## Caveats
- This space changes fast; every figure here is dated to **August 2026** and should be re-verified. Anthropic doesn't publish exact Max token caps — utilization figures are estimates.
- Claude Code cloud/web session accounting remains an unsolved gap with no documented export API.
- OTel GenAI conventions are pre-stable; attribute names may shift.
- Some third-party valuation figures (e.g., the $6,600 API-equivalent) come from individual practitioner blog posts (AgentPlix, Botfarm, Build This Now), not audited data — treat as illustrative but directionally consistent across independent sources.
- Cursor and GitHub full billing APIs assume Teams/Enterprise or enhanced-billing access; a purely personal account may see reduced granularity (though the enhanced-billing platform is now rolled out to all accounts, and user-level `/usage` endpoints exist).