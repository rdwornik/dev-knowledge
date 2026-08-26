# Chinese-Origin Coding Models in 2026: A Provider-Agnostic Access Guide for a Windows 11 Solo Developer

## TL;DR
- **Yes, there are far more than DeepSeek, GLM, and "K3."** The 2026 Chinese coding-model field includes at least ten serious families — DeepSeek (V4), Zhipu/Z.ai GLM (5.x), Moonshot Kimi (K2.7 Code / K3), Alibaba Qwen (3.x), MiniMax (M3), ByteDance Doubao Seed 2.x Code, plus Baidu ERNIE, Tencent Hunyuan, StepFun, and Kuaishou's KAT-Coder — and the top open-weight ones (DeepSeek V4, GLM-5.2, Kimi K3) now sit within a few points of Claude Opus/Sonnet and GPT-5-class models on SWE-bench Verified.
- **The single most powerful lever for this user is the Anthropic-compatible endpoint.** DeepSeek, Moonshot/Kimi, Z.ai/GLM, MiniMax, and Alibaba Qwen all publish an official `/anthropic` Messages-API endpoint, so Claude Code itself can drive them by setting `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_MODEL`. The trap the user already hit — being silently switched off his Max subscription — is caused by a globally exported `ANTHROPIC_BASE_URL`; the fix is to scope those variables per-invocation (wrapper functions / per-project `.claude/settings.json`), never globally.
- **Recommended minimal setup:** keep Claude Code on Max as the default (no global env vars); add ONE Chinese endpoint via a scoped PowerShell wrapper for headless "lane" work (GLM Coding Plan or DeepSeek direct are the best value); and install Cline or Kilo Code in VS Code with saved provider profiles for fast mid-task model switching. This gives swappable extra capacity without ever touching the Max login.

## Key Findings

1. **The Anthropic-compatibility wave is the defining 2026 development.** What began with Moonshot/Kimi in mid-2025 is now standard: every major Chinese lab ships an Anthropic Messages-API-compatible endpoint specifically so Claude Code, Cline, Roo Code and similar tools work unchanged. This is the fastest route to swappable capacity for a Claude Code user.
2. **Open weights are genuinely competitive on coding.** DeepSeek V4-Pro (~80.6% SWE-bench Verified, vendor), GLM-5.2, and Kimi K3 now trade blows with frontier closed models on coding, at roughly one-tenth the token price. Per Morph, Kimi K3 (Moonshot AI) launched July 16, 2026 and took #1 on the Arena.ai Frontend Code Arena at roughly 1,679 points, ahead of Claude Fable 5 and GPT-5.6 Sol; on Vals AI's independent SWE-bench Verified harness it scores 93.4%, third behind GPT-5.6 Sol (96.2%) and Fable 5 (95.0%) — and Vals.ai's board also lists DeepSeek V4 Pro 0813 second at 96.40%.
3. **Subscription "coding plans" are the value story.** Z.ai's GLM Coding Plan (from $18/mo Lite) and Moonshot's Kimi Code plan (from ~$19/mo) meter *prompts per window* rather than tokens, and both run through Anthropic-compatible endpoints — a direct structural parallel to the Claude Max plan the user already has.
4. **First-party CLIs now exist for most vendors.** Qwen Code (Alibaba), Kimi Code CLI (Moonshot), iFlow CLI, and — new in August 2026 — DeepSeek's own "DeepSeek Harness" (`@deepseek-ai/dsh`). All have headless/non-interactive modes suitable for the user's "lane" dispatch workflow.
5. **Data-handling risk is real and asymmetric.** DeepSeek's consumer terms permit training on user data and store data in China; enterprise/employment implications matter for someone at a Western software company. The safest postures are the open weights run locally, or providers with documented zero-retention (e.g. Fireworks-hosted).

## Details

### 1. The Model Landscape (dated table)

| Family (vendor) | Flagship coding model (2026) | Open/Closed | Context | API price (per 1M in/out, USD) | Key benchmark (dated) |
|---|---|---|---|---|---|
| **DeepSeek** | DeepSeek-V4-Pro (1.6T total/49B active); V4-Flash (284B/13B) | Open weights (MIT) | 1M (384K max output) | Pro ~$0.435/$0.87; Flash ~$0.14/$0.28 (off-peak/peak tiers effective Aug 16 2026) | V4-Pro ~80.6% SWE-bench Verified (vendor, 2026); Vals.ai lists V4 Pro 0813 at 96.40% on its SWE-bench Verified board (2026) |
| **Zhipu / Z.ai (GLM)** | GLM-5.2 / GLM-5.3 (Aug 14 2026); GLM-4.7 lighter tier | Open weights (MIT for GLM-5.1, 754B/40B active) | ~200K (GLM-4.6); ~1M (GLM-5.2 class) | Standalone API $1.40/$4.40 (from Jun 16 2026); cached input ~1/5 | GLM-4.6 on par with Claude Sonnet 4/4.5 across 8 benchmarks (vendor, 2025); per HyScaler GLM-5.2 scored 81.0 on Terminal-Bench 2.1 and 62.1% on SWE-bench Pro, trailing Claude Opus 4.8 (85.0 Terminal-Bench) but outperforming GPT-5.5 (58.6% SWE-bench Pro) |
| **Moonshot (Kimi)** | Kimi K2.7 Code / K3 (2.8T MoE, announced Jul 16 2026) | Open weights | 256K (K2.6); up to 1M (K3 `[1m]`) | K2.7 Code $0.95/$4.00, cache $0.19; K3 ~$3/$15 | K3 93.4% SWE-bench Verified (Vals AI); #1 Arena.ai Frontend Code Arena (~1,679 pts), Terminal-Bench 2.1 88.3 (Jul 2026) |
| **Alibaba (Qwen)** | Qwen3.8-Max (2.4T/95B active, Aug 2026); Qwen3-Coder / Qwen3.x-Plus | Mixed (Max open-weight promised; coder tiers Apache 2.0) | 1M | Qwen3.6 Plus ~$0.325/$1.95 (promo, OpenRouter) | Qwen3.5-397B: 83.6 LiveCodeBench v6, 86.7 Tau2-Bench (2026) |
| **MiniMax** | MiniMax-M3 (Jun 1 2026); M2.7 legacy | Open weights (community license) | 1M (MSA sparse attention) | M3 ~$0.30/$1.20 (RMB-based; OpenRouter lists ~$0.23/$0.96) | M3 SWE-Bench Pro 59.0%, Terminal-Bench 2.1 66.0% (vendor); M3 ~80.5% SWE-bench Verified |
| **ByteDance** | Doubao-Seed-2.0 Code (Feb 14 2026) | Closed (API via Volcano Engine) | — | Ultra-cheap Chinese-market tiers | Powers TRAE IDE; agentic planning focus |
| **Baidu** | ERNIE 5.x (2.4T omnimodal) | Mostly closed | — | — | Leader on formal Chinese writing (2026) |
| **Tencent** | Hunyuan Turbo | Mixed | — | — | Multimodal/video strength |
| **Kuaishou** | KAT-Coder-Pro V2 (Mar 27 2026) | Closed | 256K | $0.30/$1.20 | Chinese-language coding |
| **StepFun / 01.AI / iFlytek / InternLM / Skywork** | Step-2 (math), Yi-Coder, Spark 5.0, etc. | Mixed | varies | varies | Niche/vertical strengths |

Caveat: many benchmark numbers above are **vendor-reported** or from third-party aggregator pages that are frequently AI-generated; where independent (Vals AI, Artificial Analysis) I've said so. Treat single-board scores skeptically and re-verify before relying on them.

### 2. Anthropic-Compatible Endpoints — HIGHEST PRIORITY

All five below are documented in official provider docs. The pattern is identical: set `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` (NOT `ANTHROPIC_API_KEY`), and model-mapping vars.

**DeepSeek** (official — `api-docs.deepseek.com`):
- Base URL: `https://api.deepseek.com/anthropic`
- Model IDs: `deepseek-v4-pro[1m]`, `deepseek-v4-flash`; Claude names auto-map (opus→v4-pro, sonnet/haiku→v4-flash)
- PowerShell: `$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"`, `$env:ANTHROPIC_AUTH_TOKEN="<key>"`, `$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"`
- Works: tool use, web search (billed as extra tokens), 1M context. Breaks: images/documents and some advanced tool-result structures not fully supported; returns 404 on `/v1/models` preflight (Claude Code proceeds anyway); rejects non-alphanumeric `metadata.user_id` on some CC versions.

**Moonshot / Kimi** (official — `platform.kimi.ai`):
- Base URL: `https://api.moonshot.ai/anthropic` (global) or `https://api.moonshot.cn/anthropic` (China)
- Model IDs: `kimi-k3[1m]`, `kimi-k2.7-code` (pay-per-token) or `kimi-for-coding` (subscription)
- Note: `kimi-k2.7-code` requires thinking mode ON (press Tab) or WebSearch returns 400; `kimi-k3` thinks by default. WebFetch not yet supported. Claude Code's `/model` menu shows only Claude aliases — verify via `/status`, not the menu.

**Z.ai / GLM** (official — `docs.z.ai`):
- Base URL: `https://api.z.ai/api/anthropic`
- Model IDs: `glm-4.7`, `glm-5.2`, etc. (map via `ANTHROPIC_DEFAULT_SONNET_MODEL`/`OPUS_MODEL`)
- Helper: `npx @z_ai/coding-helper` auto-configures. Note: the auto-install shell script is **macOS/Linux only** — Windows users edit `settings.json` manually.
- Works with Cline, Roo Code, Claude Code, and 20+ tools; used heavily in agentic loops.

**MiniMax** (official — `platform.minimax.io`):
- Base URL: `https://api.minimax.io/anthropic` (intl) or `https://api.minimaxi.com/anthropic` (China)
- Model IDs: `MiniMax-M3` / `MiniMax-M2.7-highspeed`
- **MiniMax docs explicitly warn:** "Environment variables `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` take priority over settings.json" and instruct you to `unset` any pre-existing Anthropic env vars first — directly relevant to the user's billing-switch problem.

**Alibaba Qwen** (official — Model Studio / DashScope):
- Base URL: `https://dashscope.aliyuncs.com/apps/anthropic` (Beijing) or `https://dashscope-intl.aliyuncs.com/apps/anthropic` (Singapore); Coding Plan uses `coding.dashscope.aliyuncs.com/apps/anthropic`
- Model IDs: `qwen3.7-plus`, `qwen3.8-max`, etc.
- Gotcha: endpoint provides ONLY `/v1/messages`, no `/v1/models`, so model discovery 404s; do NOT append `/v1/` to the base URL (causes `/v1/v1/models` 404). Add models manually.

**Aggregator route:** OpenRouter and Requesty also expose Anthropic-compatible surfaces (`https://openrouter.ai/api/v1`... or Requesty's `router.requesty.ai`), giving one key across all Chinese models. Claude Code will use `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` against these too.

#### ENV-VAR PRECEDENCE AND PER-INVOCATION SCOPING (the billing-switch fix)

**How Claude Code resolves auth/routing (highest→lowest):**
1. **Managed/enterprise policy** (`managed-settings.json`: Windows `C:\ProgramData\ClaudeCode\managed-settings.json`) — cannot be overridden.
2. **CLI flags** (e.g. `--model`).
3. **Local project** `.claude/settings.local.json` (gitignored).
4. **Shared project** `.claude/settings.json`.
5. **User global** `~/.claude/settings.json`.
6. **Shell environment variables** (`$env:` exports).

Critical nuance: **when a custom `ANTHROPIC_BASE_URL` is present (env OR settings), Claude Code silently routes there instead of your Max/Pro OAuth subscription — with no warning.** GitHub issue #23022 (anthropics/claude-code) documents it precisely: "When users have both OAuth credentials (Max/Pro subscription) AND custom environment variables like ANTHROPIC_BASE_URL in their settings.json, Claude Code silently uses the custom URL instead of Anthropic's API… The .credentials.json correctly shows subscriptionType: 'max', but API calls fail because they're being routed to a non-Anthropic endpoint." Related reports (#44669, #36350, #33330, and #62338 — a user "silently billed $447 to API instead of Max subscription") confirm this is a recurring, costly failure mode. A stray `ANTHROPIC_API_KEY` triggers a conflict too; Anthropic's help center says keep it **unset** to use the subscription, and `/status` shows which auth is active.

**Per-invocation scoping on Windows/PowerShell (do this, not global exports):**
- **Wrapper function** — define a PowerShell function that sets the vars only inside a child scope, e.g.:
  ```powershell
  function glm { $env:ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"; $env:ANTHROPIC_AUTH_TOKEN=$env:ZAI_KEY; $env:ANTHROPIC_MODEL="glm-5.2"; claude @args; Remove-Item Env:\ANTHROPIC_BASE_URL,Env:\ANTHROPIC_AUTH_TOKEN,Env:\ANTHROPIC_MODEL }
  ```
  This routes to GLM for that call and unsets afterward, so a bare `claude` stays on Max.
- **Per-project settings** — put the Chinese-endpoint `env` block in a specific repo's `.claude/settings.json`; other repos and the global default keep Max.
- **`--setting-sources`** — `claude --setting-sources user` loads only your global settings and ignores project overrides (managed policy + CLI flags always still apply).
- **`apiKeyHelper`** — a `settings.json` key pointing at a script whose stdout is used as the token; good for pulling keys from a secret manager in unattended runs.
- **Golden rule for THIS user:** never `setx` or add `ANTHROPIC_BASE_URL` to your PowerShell `$PROFILE`. Keep the user-global `~/.claude/settings.json` free of any `ANTHROPIC_BASE_URL`, and gate every Chinese-model session behind a named wrapper. Run `/status` if a session ever appears to be on the wrong provider.

### 3. Official & Community CLI Agents

| CLI | Vendor | Windows install | Headless mode | Permission bypass | Config location | Reads AGENTS.md / CLAUDE.md |
|---|---|---|---|---|---|---|
| **Qwen Code** | Alibaba (official) | `npm i -g @qwen-code/qwen-code` | `qwen -p "…"`, stdin, `--output-format stream-json`, `--continue`/`--resume` | `--yolo` / `--approval-mode=yolo` (no sandbox unless `--sandbox`) | `.qwen/`, settings.json | AGENTS.md yes |
| **iFlow CLI** | iFlow (official) | npm | `-p` (headless; `-c`+`-p` resume); ACP mode | yes | iflow config json | via OpenAI-compatible |
| **Kimi Code CLI** | Moonshot (official) | `npm i -g @moonshot-ai/kimi-code` (binary `kimi`) | `kimi -p "…"`, `-c`, `--session`, JSONL stream | `--auto`, `--yolo` | kimi-cli config | yes |
| **DeepSeek Harness** (`dsh`) | DeepSeek (official, Aug 13 2026, MIT, dev preview) | `npx @deepseek-ai/dsh web` | headless + ACP automation documented | — | Cordis plugin config; `DEEPSEEK_API_KEY` | — (preview) |
| **@vegamo/deepcode-cli** (`deepcode`, v0.3.1) | Community (user's current) | npm | check `-p`/stdin support | — | — | — |
| **MiniMax** | via Claude Code / Cline; no standalone flagship CLI | — | — | — | — | — |
| **opencode / Crush / Aider / Cline CLI** | Community multi-provider | npm/binary | all support non-interactive/`-p`/`run` | varies | per-tool | AGENTS.md widely |

Notes: Roo Code's original repo was **archived May 15, 2026** (it "reached 24,200 GitHub stars and 1.56 million VS Code installs before archival," now a community handoff) — treat as in-transition. Gemini CLI was slated for retirement June 18 2026. Kilo Code (fork lineage from Cline→Roo) is actively maintained with a CLI + VS Code extension. DeepSeek's `awesome-deepseek-agent` repo is an official *list* of third-party integrations (endorsement, not support); `@vegamo/deepcode-cli` and `reasonix` are community, while `@deepseek-ai/dsh` is the only agent under the official deepseek-ai npm scope.

### 4. VS Code Access and Model Swapping

- **Agentic extensions accepting any OpenAI/Anthropic-compatible provider — best for fast switching:**
  - **Cline** (Apache 2.0; per Fastio citing the GitHub API, cline/cline shows about 64,700 stars and ~6,900 forks as of 16 July 2026; actively maintained): model-agnostic, plan-then-execute, MCP, saved provider configs. Point at Moonshot/DeepSeek/GLM via OpenAI-compatible or the `/anthropic` endpoints.
  - **Kilo Code** (Kilo-Org/kilocode; ~20k stars per Morph's June 2026 count, with theaiagentindex.com reporting 26.5k stars, "3M+ users" and "$8 million in seed funding"; fastest-growing, Cline/Roo lineage): **API Configuration Profiles** you switch per task; auto-detects models from `/v1/models`; VS Code + JetBrains + CLI; BYOK zero-markup. Best "many profiles, switch mid-task" option.
  - **Roo Code**: same OpenAI-compatible pattern but **archived May 2026** — verify maintenance before adopting.
  - **Continue.dev / Void**: also OpenAI-compatible; Void's upstream repo is now deprecated/archived.
- **GitHub Copilot BYOK** (public preview, added to the Copilot app June 23 2026; VS Code 1.120+ Model Provider dropdown): supports Anthropic, OpenAI, Azure/Foundry, xAI, and **OpenAI-compatible/local endpoints (Ollama, LM Studio)**. Chinese models work **only through their OpenAI-compatible endpoints or a gateway** — there is no first-class "DeepSeek/GLM" provider button, and models must support tool calling + streaming. Enterprise admins can also push org-wide custom-model keys.
- **Official vendor extensions / IDEs:**
  - **Alibaba Tongyi Lingma → rebranded Qoder CN (May 20 2026)**: VS Code + JetBrains plugin and standalone IDE; can switch between GLM, DeepSeek, Kimi, MiniMax. 20M+ downloads.
  - **ByteDance Trae**: standalone VS Code-fork IDE with SOLO autonomous mode, Pro+ at ~$30/mo, custom-model + MCP support; runs Doubao Seed 2.0 Code and can switch models. A separate IDE, not an extension.
  - CodeGeeX (free/open) also available.
- **Windows caveats:** Z.ai's auto-install script is macOS/Linux only; Trae/Qoder are full IDE installs; all npm-based CLIs need Node.js 18+ and Git for Windows.

### 5. Aggregators and Subscription Coding Plans

**Aggregators (all OpenAI-compatible; all preserve function/tool calling):**
- **OpenRouter**: one key, huge menu; lists `deepseek/deepseek-v4-pro` (~$0.435/$0.87), Kimi, GLM-5.2 (~$1.40/$4.40), MiniMax M3, Qwen. Routing layer, not a host.
- **SiliconFlow**: 37 models, **all support function calling**, 30/37 JSON mode; DeepSeek V4-Flash blended ~$0.07/1M; GLM-5.1 (FP8) ~$1.03/1M; Kimi K2.6 FP8 lowest TTFT ~1.3s.
- **Together / Fireworks / Novita / DeepInfra / Parasail**: carry DeepSeek/GLM/Kimi/Qwen/MiniMax. Together lists Kimi K2.6 $1.20/$4.50, GLM-5.2 $1.40/$4.40, MiniMax M2.7 $0.30/$1.20. **Fireworks advertises US-hosted, zero-data-retention** K3 — relevant for compliance.
- **Quality note:** most serverless hosts quantize activations to FP8/FP4, which degrades output vs reference weights; Morph and some others serve bf16. For agentic coding, verify the host's precision.
- **Single key/base URL covering all:** OpenRouter or Requesty give one key + one Anthropic-compatible base URL across everything; cost is a small routing margin vs direct provider keys. Direct provider keys are cheaper and (for GLM/Kimi) unlock the subscription plans.

**Subscription coding plans vs pay-per-token:**
- **GLM Coding Plan (Z.ai):** Per aipricing.guru, Lite lists at **$18/mo** ($12.60/mo on annual, $151.20/yr; "up to about 80 prompts per 5 hours and about 400 prompts per week, plus 100 MCP… calls per month"), **Pro $72/mo** ($50.40 annual; ~400/5h, ~2,000/week), **Max $160/mo** ($112 annual; ~1,600/5h, ~8,000/week). One "prompt" = one user turn but "may invoke the model 15-20 times." Per aipricing.guru citing Z.ai DevPack docs, "GLM-5.2 and GLM-5-Turbo consume 3x quota during peak hours and 2x off-peak, with a limited-time 1x off-peak benefit through September" (peak = 14:00–18:00 UTC+8). Runs through the Anthropic-compatible endpoint.
- **Kimi Code (Moonshot):** entry paid tier from ~$19/mo; weekly quota + rolling 5-hour window; model ID `kimi-for-coding`; plan structure was mid-restructure in mid-2026 (verify live prices).
- **MiniMax Coding Plan:** prompt-quota tiers (launch: Starter $10 / Pro $20 / Max $50, e.g. Starter 40 prompts/5h); as of the last dated docs still ran **MiniMax-M2.1** as the designated model (verify whether upgraded to M3).
- **Qwen:** Alibaba Model Studio Coding Plan with dedicated API key and the `coding.dashscope.aliyuncs.com/apps/anthropic` endpoint.
- These plans are the closest structural analog to the user's Claude Max: flat monthly, prompt-metered, and they slot under Claude Code via the same env vars.

### 6. Practical Risks

- **Data/training terms:** DeepSeek's consumer app/policy permits using inputs for training and stores data in China; there is no reliable in-product training opt-out on the hosted consumer app, though the policy references a "right to opt out" for some regions and paid API accounts are described as excluded from training by default (this is contested across sources — verify against your account's live terms). Multiple third-party analyses state DeepSeek's API ToS are the weakest among major providers on data privacy and lack SOC 2 / HIPAA. GLM, Qwen, Kimi, MiniMax each have their own terms; read them per-account.
- **Enterprise/employment implications:** for someone employed by a Western enterprise software company, sending proprietary/employer code to any Chinese-hosted API likely triggers vendor-risk/legal review and may violate employment or customer confidentiality terms. Regulators (Berlin DPA, Korea PIPC, others) have acted against DeepSeek over cross-border data transfer. **Do not send employer code to these APIs without written approval.** Prefer local open weights or a zero-retention Western host for anything sensitive.
- **Europe/payment:** DeepSeek/GLM/Kimi/MiniMax platforms accept international cards; aggregators (OpenRouter, Together, Fireworks) are US/EU-billed and simpler for European developers. Requesty offers EU data-residency routing.
- **API stability/rate limits:** DeepSeek has had multiple outages; free/low tiers are heavily throttled. Subscription plans meter by prompt-window and can throttle under load. Build failover (aggregator or second provider) into any "lane" pipeline.
- **Local open-weights on a normal workstation:**
  - **Realistic today:** Qwen3-Coder 30B-A3B (~19 GB Q4_K_M) runs on a single 24 GB GPU (RTX 4090) at usable speed because only ~3B params activate/token; Qwen3 8B runs in ~5.5 GB. GLM-4.7-Flash / smaller GLM tiers and Qwen3-Coder-Next (80B/3B active, MoE, splits GPU+CPU) are viable with quantization. Q4_K_M loses <1% on benchmarks vs FP16.
  - **NOT realistic on a workstation:** DeepSeek V4 (1.6T, ~150–250 GB memory), Qwen3-235B (~142 GB), Kimi K3 (MXFP4 files >1.4 TB, ~8× GB300 GPUs). These are datacenter-only.
  - **Tooling:** Ollama (`ollama pull qwen3-coder:30b`, OpenAI-compatible at `localhost:11434`), llama.cpp (`llama-server`), or vLLM. Wire into Qwen Code / Cline / Copilot BYOK via the local OpenAI-compatible endpoint. Raise `OLLAMA_CONTEXT_LENGTH` to ≥64K for agentic coding.

## Recommendations

**Stage 0 — protect the Max subscription first (do this before anything else).**
- Remove any `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` from your PowerShell `$PROFILE`, from `setx`/system env, and from `~/.claude/settings.json`. Run `claude` then `/status` and confirm it shows your Max login, not "Claude API."
- Change-my-mind signal: if `/status` ever shows API billing, you have a stray global var.

**Stage 1 — add ONE Chinese endpoint, scoped, for headless lanes.**
- Best value/quality for a Claude Code user: **GLM Coding Plan (Lite $18 → Pro $72)** — prompt-metered like Max, Anthropic-native, strong coding. Alternative: **DeepSeek direct** (`api.deepseek.com/anthropic`, V4-Pro) for cheapest pay-per-token and 1M context.
- Implement as a named PowerShell wrapper (`glm`, `dsk`) that sets the env vars in-process and unsets them after — never globally. Your existing non-interactive "lane" dispatch calls the wrapper instead of bare `claude`.
- Keep your current `@vegamo/deepcode-cli` if it already works headless; but the new **DeepSeek Harness (`@deepseek-ai/dsh`)** is now the official option worth testing for automation/ACP.

**Stage 2 — fast switching in VS Code.**
- Install **Kilo Code** (or Cline). Create saved **provider profiles**: Claude (Max via Copilot BYOK or Anthropic key), DeepSeek, GLM, Kimi, Qwen. Switch per task from the model picker — this is your "fast model switching in VS Code" answer, and it keeps Chinese keys out of Claude Code's env entirely.
- If you prefer Copilot: use **Copilot BYOK** with the vendors' OpenAI-compatible endpoints (tool-calling + streaming required).

**Stage 3 — add local open weights for sensitive/offline work.**
- If you have a 24 GB GPU, run **Qwen3-Coder 30B via Ollama** and point Kilo Code / Qwen Code at `localhost:11434`. Use this for anything employer-confidential.

**Thresholds that change the recommendation:**
- If you exceed GLM Lite's ~400 prompts/week → step to Pro $72 or add DeepSeek pay-per-token for overflow.
- If independent (non-vendor) benchmarks show Kimi K3 or GLM-5.2 beating Sonnet on YOUR tasks → promote it from "extra capacity" to a primary lane.
- If your employer's policy prohibits Chinese APIs → collapse to local open weights + Fireworks zero-retention only.

## Caveats
- **This space changes weekly.** Model versions (V4→?, GLM-5.2→5.3, Kimi K2.7→K3, MiniMax M2.x→M3) and prices moved repeatedly through 2026; re-verify every price/model ID on the official page before committing.
- **Many cited pages are AI-generated aggregators**, and some benchmark numbers are vendor-reported. I flagged independent sources (Vals AI, Artificial Analysis, official docs) where possible; treat single-board superlatives skeptically.
- **Anthropic-compatibility ≠ identity.** Tool use, thinking blocks, prompt caching, subagents, MCP, and `/model` behave differently per provider; images/documents and WebFetch are commonly unsupported. Test your real payloads.
- **The billing-switch risk is a documented Claude Code behavior, not user error** — but the mitigation (never set `ANTHROPIC_BASE_URL` globally) is entirely in your control.
- **Legal/employment risk is the dominant caveat** for a Western-enterprise employee: get written approval before routing any employer or customer code through a Chinese-hosted endpoint.
- Kimi Code exact USD tiers, whether MiniMax's Coding Plan now runs M3, and DeepSeek V4-Flash exact token rates could not be fully confirmed from primary sources at time of writing — verify live.