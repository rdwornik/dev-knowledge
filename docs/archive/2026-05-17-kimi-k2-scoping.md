# Kimi K2 Incorporation Scoping Note

<!-- scope: llm -->

**Date:** 2026-05-17
**Author:** Claude Code (Sonnet 4.6) in `.dev-knowledge`
**Purpose:** Scoping-level evaluation of incorporating Kimi K2 as an
additional provider in the AI Council workflow. No implementation, no
config changes. A future session executes based on this note.
**Status:** Scoping only — no decisions made.

---

## 1. What Kimi K2 is

Kimi K2 is a mixture-of-experts (MoE) large language model from Moonshot
AI, released June 2025. Key characteristics:

| Property | Value |
|---|---|
| Architecture | MoE, ~1T total parameters, ~32B active per forward pass |
| Context window | 128K tokens |
| Strengths | Coding, tool use, agentic tasks, mathematical reasoning |
| Open weights | Yes — base and instruct variants on Hugging Face |
| API access | Moonshot AI API (api.moonshot.cn / compatible endpoint) |
| OpenAI-compatible | Yes — Drop-in for the OpenAI SDK client |
| Tool use | Native function calling (OpenAI-format tools) |
| Pricing (est.) | Competitive with GPT-4o class; exact rate needs verification at time of integration |

Kimi K2 scored highly on agentic and coding benchmarks in the June 2025
period. Its MoE design means strong per-token throughput relative to cost.

---

## 2. Where it would plug in

### 2.1 AI Council debate panel

The current ai-council panel uses named providers (Claude, GPT, Gemini,
DeepSeek, Grok). Kimi K2 would enter as an additional `moonshot` or
`kimi` provider slot.

Integration surface:
- `ai-council/providers/` — add a Moonshot provider wrapper
- Panel config YAML — add `kimi-k2` as an optional provider slug
- `ai-council/council_runner.py` (or equivalent) — add Moonshot API
  client call (OpenAI-compatible, so minimal new code)
- Environment variable: `MOONSHOT_API_KEY` (store via `keys set`)

### 2.2 Model routing (`~/.claude/ROUTING.md`)

Current routing covers Claude tiers (Sonnet / Opus). Kimi K2 is a
non-Claude provider; routing guidance would need a note for cases where
the ai-council is the execution target, not Claude Code. ROUTING.md
governs Claude Code model selection, not Council panel composition —
Kimi K2 lives in the Council layer only.

### 2.3 `.dev-knowledge` governance

No changes needed to `.dev-knowledge` governance structure. If Kimi K2
becomes a permanent panel member, it should appear in:
- `protocols/PLAYBOOK.md` § AI Council section (provider inventory)
- `protocols/ENVIRONMENT.md` (active providers + key reference)

---

## 3. What would need to be tested

1. **API connectivity** — obtain key, verify `api.moonshot.cn` is
   reachable from the dev machine; confirm OpenAI-SDK compatibility.
2. **Tool use fidelity** — run a Council debate with tool calls and
   verify K2 parses and returns JSON-format tool results correctly.
3. **Panel balance** — K2 is a Chinese-origin model; verify response
   style, length, and epistemic framing are compatible with the
   synthesizer's cross-model comparison task.
4. **Cost** — measure token cost per debate round; ensure K2 doesn't
   dominate total session cost.
5. **Rate limits** — Moonshot AI free tier is limited; confirm limits
   before enabling for automated Council runs.
6. **Latency** — MoE models can have variable latency under load;
   measure p50/p95 for a typical debate round.
7. **Output language** — default output is in English when prompted in
   English, but verify this holds with the Council's system prompts.

---

## 4. Open questions

| Question | Who decides | Notes |
|---|---|---|
| Is K2 performance differentiated enough from GPT-4o to add panel diversity? | Council debate | If it overlaps with GPT-4o without adding new viewpoints, the panel seat isn't worth the cost |
| Which Council debate types benefit most from K2? | Empirical testing | Coding-heavy debates or architecture questions are the likely sweet spot |
| How to handle Chinese-origin model in enterprise governance contexts? | Rob | corp-monorepo audits may touch confidential data; data-residency considerations apply |
| OpenAI-compatible endpoint: is streaming supported? | Moonshot API docs | Council runner may require streaming for long debates |
| Is the open-weights version worth self-hosting on a GPU? | Cost/complexity tradeoff | Only relevant if API rate limits or cost become blockers |
| Key storage: `MOONSHOT_API_KEY` → `keys set`? | Rob | Confirm via `keys list` before integration session |

---

## 5. Recommended next step (when ready to implement)

1. Obtain Moonshot API key via moonshot.cn.
2. Add `MOONSHOT_API_KEY` to `~/.secrets/.env` via `keys set`.
3. Open an ai-council session with this note as context.
4. Add a minimal `moonshot` provider wrapper (copying the DeepSeek
   provider pattern as closest analogue — both use OpenAI-compatible
   endpoints).
5. Run a single-question Council debate with K2 on panel; compare output
   to existing panel members.
6. Decide whether to make K2 a permanent optional panel member.

**Estimate:** ~1–2 hours of implementation time if the OpenAI-compat
endpoint works as documented. Risk: low (additive, no existing paths
change).
