# TIER (B) B-1 — the OTel GenAI event schema, and the one dependency finding it will not decide alone

> **PROVENANCE — harvested COPILOT-ENTERPRISE artifact, body VERBATIM below this header.**
> Payload `B-1` from
> `docs/audits/2026-08-31-technical-batche-launch-contracts/TIER-B-COPILOT-PAYLOADS.md`, run
> 2026-09-01 from the integrator seat. Provider `copilot-enterprise`, CLI `copilot` 1.0.81,
> identity **`Robert-Dwornik_ghub`** asserted with `gh api user` before the call. Nothing below
> this line was edited, reflowed or trimmed — including the CLI's own tool-trace lines and its
> credits footer, which are part of the receipt.
>
> **Consumed by:** DM-2 (`lane-f-6-observability-otel`), which was BLOCKED on this draft and is unblocked by it, and `[#614]` (batch E's frozen execution arc).
>
> **THE PACK'S ROUTING CLAIM WAS REFUTED BY WITNESS, and this run is the witness.**
> `TIER-B-COPILOT-PAYLOADS.md` states *"Enterprise Copilot is not driveable from this seat"*, and
> the 2026-09-01 night window took that at face value and did NOT dispatch DM-1/DM-2 as a result.
> **The operator refuted it**, citing the SDA-1 adversarial incumbent baseline
> (`docs/audits/2026-08-29-technical-sda1-adversarial-incumbent-baseline.md`, 21.15 credits,
> identity recorded) as an existing enterprise run from this machine. The mechanism is a
> **per-invocation `GH_TOKEN`** — `gh auth token --user Robert-Dwornik_ghub` scoped to the call,
> never `gh auth switch`, which this repo has recorded as unreliable. Provenance stays exactly
> where the pack assigned it: this is a copilot-enterprise artifact, not a re-route.

---

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "Phoenix|Langfuse|OpenTelemetry|OTel|GenAI"[39m
  [38;2;145;152;161m└ 21 files found[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252mLANE-f-6-observability-otel.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-31-technical-batche-launch-contracts\LANE-f-6-observability-otel.md[39m
  [38;2;145;152;161m└ 64 lines read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-30-technical-autonomy-decision-tree.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-30-technical-autonomy-decision-tree.md[39m
  [38;2;145;152;161m└ 135 lines read[39m

[38;2;231;72;86m✗[39m [1mRead [22m[38;2;240;246;252m2026-08-26-technical-cost-usage-telemetry.md[39m
  [38;2;231;72;86m│ docs\audits\2026-08-26-technical-cost-usage-telemetry.md[39m
  [38;2;231;72;86m└ Path does not exist[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(glob)[39m
  [38;2;145;152;161m│ "**/cost_usage_telemetry.py"[39m
  [38;2;145;152;161m└ No matches found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(glob)[39m
  [38;2;145;152;161m│ "docs\audits\2026-08-26*"[39m
  [38;2;145;152;161m└ 17 files found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(glob)[39m
  [38;2;145;152;161m│ "scripts\*telemetry*"[39m
  [38;2;145;152;161m└ 1 file found[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252m2026-08-26-technical-research-cost-usage-telemetry.md[39m
  [38;2;145;152;161m│ docs\audits\2026-08-26-technical-research-cost-usage-telemetry.md[39m
  [38;2;145;152;161m└ 1 line read[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252mtelemetry_emit.py[39m
  [38;2;145;152;161m│ scripts\telemetry_emit.py[39m
  [38;2;145;152;161m└ 1 line read[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "Phoenix|Langfuse|LangSmith|attribute|schema|span|event""[39m
  [38;2;145;152;161m└ 9 lines found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "^def |^class |emit|attribute|event_type|model|tokens|cost|duration|status|def main""[39m
  [38;2;145;152;161m└ 85 lines found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "EVENT_TYPES|OUTCOMES|context_json|def emit_event|CREATE TABLE""[39m
  [38;2;145;152;161m└ 47 lines found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "model|token|cost|call_site|per-tool|ccusage"[39m
  [38;2;145;152;161m└ 28 lines found[39m

[38;2;145;152;161m/[39m [1mSearch [22m[38;2;145;152;161m(grep)[39m
  [38;2;145;152;161m│ "otel|opentelemetry|structlog|langfuse|phoenix|dependencies|\[project\]"[39m
  [38;2;145;152;161m└ 1 line found[39m

[38;2;63;185;80m●[39m [1mRead [22m[38;2;240;246;252mpyproject.toml[39m
  [38;2;145;152;161m└ L1:60 (60 lines read)[39m

## Assumptions (stated, since I can't see your internals directly)

1. **"Our current emission"** = the two things I can find on disk: (a) `scripts/telemetry_emit.py`, a Stage‑1 library writing gate/hook telemetry (`check_run`, `hook_run`, `blocker_fired`) into a single SQLite `events` table — this is **not** model-usage telemetry, it's audit-gate telemetry; and (b) the Lane f‑6 write-scope names a not-yet-created `scripts/cost_usage_telemetry.py`, and the research audit (`2026-08-26-technical-research-cost-usage-telemetry.md`) recommends a **batch pull-and-join** design (ccusage JSONL + provider admin billing APIs → DuckDB → weekly Markdown), not per-call live span emission. I'm treating the batch design as the "current emission" this schema migrates, and treating gate telemetry as **out of scope** (different axis, different table, not a GenAI concept).
2. Model calls happen inside CLI-agent sessions (Claude Code, Codex, etc.) that themselves can emit OTel — I'm assuming *this* schema is for **our own wrapper/aggregation layer**, not a re-implementation of each vendor's exporter.
3. "Cache read/write tokens," "subscription utilization %," and "imputed API-equivalent cost" are real concepts in your research doc with no OTel GenAI counterpart — I assume you still want them captured, just not by bending a standard attribute.
4. I assume `gen_ai.*` staying "Development" status (per your own audit) means attribute names are a moving target — the mapping layer already recommended for that reason is presupposed here.

---

## 1. Event schema

**Spans** (one per model invocation — the unit Phoenix/Langfuse both key traces on):

| Our concept | Span/attribute | Maps to OTel GenAI convention | Notes |
|---|---|---|---|
| A model call | span, `gen_ai.operation.name` = `"chat"` | `gen_ai.operation.name` | root span per invocation |
| Provider | `gen_ai.system` | `gen_ai.system` (e.g. `anthropic`, `openai`) | pin the enum values you use; they drift |
| Model requested | `gen_ai.request.model` | `gen_ai.request.model` | as-configured, before any fallback |
| Model that answered | `gen_ai.response.model` | `gen_ai.response.model` | may differ (routing/fallback) |
| Input tokens | `gen_ai.usage.input_tokens` | `gen_ai.usage.input_tokens` | direct |
| Output tokens | `gen_ai.usage.output_tokens` | `gen_ai.usage.output_tokens` | direct |
| Cache-read tokens | **no convention attribute** | — | propose `devknowledge.gen_ai.usage.cache_read_tokens` — Anthropic-specific, no standard slot; do not overload `gen_ai.usage.input_tokens` |
| Cache-write tokens | **no convention attribute** | — | propose `devknowledge.gen_ai.usage.cache_write_tokens`, same reasoning |
| Latency | span duration / `gen_ai.client.operation.duration` (metric) | `gen_ai.client.operation.duration` | metric, not span attribute, per spec |
| Cost estimate (client-side) | **no convention attribute** | — | propose `devknowledge.cost.estimated_usd` — cost is explicitly out of the GenAI semconv (it's provider-billing-derived, and your own audit already flags it as an approximation, never ground truth) |
| Imputed API-equivalent value (Max subscription) | **no convention attribute** | — | propose `devknowledge.cost.imputed_usd` — this is a derived valuation, not a metered spend, and conflating it with `devknowledge.cost.estimated_usd` would erase that distinction |
| Conversation/thread | `gen_ai.conversation.id` | `gen_ai.conversation.id` | direct |
| Finish reason | `gen_ai.response.finish_reasons` | `gen_ai.response.finish_reasons` | direct |
| Which lane/worktree/batch fired this call | **no convention attribute** | — | propose `devknowledge.lane_id`, `devknowledge.batch_id`, `devknowledge.run_id` (reuse the existing `run_id` correlation concept from `telemetry_emit.py` rather than minting a second one) |
| Which executor/substrate ran it | **no convention attribute** | — | propose `devknowledge.substrate` (e.g. `local`, `codespace`) — this repo already tracks this concept (batch-E's admission probe); it is not a GenAI property |

**Events** (log-based, attached to the span — content capture):

| Our concept | Event name | Maps to | Notes |
|---|---|---|---|
| System/instruction content | `gen_ai.system.message` | convention | opt-in; content capture is separately gated by your own privacy posture, not this schema |
| User turn | `gen_ai.user.message` | convention | same caveat |
| Assistant reply | `gen_ai.choice` | convention | carries `finish_reason`, message body |
| Tool invocation | span (child), `gen_ai.tool.name`, `gen_ai.tool.call.id` | convention | if/when tool calls need tracing |
| Error | span status + `error.type` | general (non-GenAI-specific) semconv attribute | already generic OTel, not a GenAI extension |

**Deliberately NOT modeled here:** the verdict layer (trends → rulings). Per the brief it is unchanged — it consumes telemetry, it is not itself an event in this schema. If a span needs to reference a ruling later, that's a link (`devknowledge.verdict.ruling_ref`), never an attribute that reshapes the span.

---

## 2. The collector seam

The smallest interface that keeps both interchangeable is **the standard OTLP exporter contract**: endpoint URL + protocol (gRPC or HTTP/protobuf) + headers, resolved from environment/config at process start, never branched on in code. If the emitting code only ever calls the OTel SDK's exporter interface (`SpanExporter`/`LogRecordExporter`), swapping collectors is a config change, not a code change.

Where they diverge — what each needs that the other doesn't:

- **Langfuse-specific:** expects Basic Auth in the OTLP headers (`Authorization: Basic base64(public_key:secret_key)`), and groups traces in its UI using its own session/user attributes (`langfuse.session.id`, `langfuse.user.id`) layered *on top of* standard OTel — Phoenix has no equivalent requirement for a viewable trace.
- **Phoenix-specific:** typically wants a project identifier carried as a resource attribute or header (e.g. `openinference-project-name`/similar) to route traces into its per-project views; self-hosted deployments may also gate ingestion behind an API-key header Langfuse doesn't need in the same shape.
- **Shared, no branching needed:** both accept OTLP directly (Phoenix as an all-in-one collector+UI; Langfuse's self-hosted stack exposes an OTLP ingest endpoint) — so the *span/event schema itself* need not know which backend receives it. The only vendor-specific matter is the header/attribute set attached at export time, which belongs in a thin per-target adapter behind the exporter interface, not in the emission code.

**FINDING — do not treat as decided:** no `opentelemetry-sdk`/`opentelemetry-exporter-otlp*` package is declared in `pyproject.toml`/`uv.lock` today. Emitting real OTLP wire traffic (the mechanism this seam assumes) requires adding that dependency, which is a separately gated ADR-106 act, not a side effect of this schema. Until that gate runs, the schema above can be **drafted and even written into the existing SQLite `context_json` shape** as conforming JSON — a paper/at-rest format Phoenix/Langfuse cannot directly ingest — but it cannot be *live-exported* without the new package. Stop here and report rather than adding it silently.

---

## 3. What this schema cannot express

- **The verdict layer's actual judgment.** A span records that a call happened, with what cost/tokens — it does not, and by design must not, carry *why a trend became a ruling*. That reasoning stays wherever your rulings already live; folding it into a span attribute would be exactly the "bending a standard" this task forbids in reverse.
- **Ground-truth cost.** Every cost figure here is client-side estimate (your own audit already says this about `claude_code.cost.usage` and ccusage). The schema can carry `devknowledge.cost.estimated_usd`; it cannot make that number authoritative. Reconciliation against provider billing APIs is a separate, out-of-band process this schema doesn't touch.
- **Flat-fee subscription spend.** A Claude Max session isn't metered per call the way an API key is. The schema can attach a derived `devknowledge.cost.imputed_usd` to a span, but there is no span-level truth for "percent of the 5-hour window consumed" — that's a *stateful, cross-call* aggregate, not a property of any one event.
- **Decision-budget / escalation semantics.** Which V-2 escalation class a lane triggered, or why, is not a GenAI property and has no attribute here; if it needs telemetry, it's a different event class entirely (closer to `telemetry_emit.py`'s gate events than to this schema).
- **Causality across calls.** `gen_ai.conversation.id` groups calls; it does not encode "call B happened because call A's ruling failed." Any causal graph stays external to the span data.
- **Cross-vendor attribute stability.** Because `gen_ai.*` is pre-stable ("Development" status, per your own research), a schema frozen today is a schema that will need a mapping-layer patch tomorrow — this document is a snapshot, not a contract.
- **Content-capture completeness.** Message-body events (`gen_ai.user.message` etc.) are opt-in and redaction-sensitive; a schema that lists them as available says nothing about whether your privacy posture permits populating them.

A schema presented as covering all of this would be wrong; it covers call-shaped, cost-shaped, and routing-shaped facts only.

---

## 4. Migration note

**What changes:**
- Today's planned design (per the research audit) is a **weekly batch pull-and-join**: ccusage JSONL + provider admin billing endpoints, joined offline, rendered to Markdown. This schema assumes **per-call, live span emission** at the moment a model call happens — a different timing and cardinality model entirely (one row per call vs. one aggregate report per week).
- `telemetry_emit.py`'s existing `events` table (gate/hook telemetry) is untouched — it has a fixed `EVENT_TYPES` enum (`check_run`, `hook_run`, `blocker_fired`) that doesn't include a model-call type, and mixing GenAI spans into that table would be scope creep. This is a **new emitter**, not an extension of Stage-1.
- Adding the live-span path requires instrumenting each model-call site directly (wrapping the call, not reading it back out of provider JSONL after the fact) — nothing in the repo does that today.

**What breaks / is lost if you move fully to live emission:**
- The batch design's reconciliation step (join against authoritative provider billing) has no natural place in a live per-call schema — it would need to become a separate, asynchronous "cost correction" event layered on top, or the reconciliation stays batch-side and the live spans stay estimates forever.
- Subscription (Max) utilization tracking, which the batch design computes as a *derived weekly aggregate*, has no single-call representation — see item 3 above. Moving to live emission doesn't gain you that number; it has to be computed separately regardless.
- Anything currently captured only in ccusage's local JSONL format (its own schema) needs an explicit translation step into this schema; that translation, not ccusage itself, is the new code surface.

**What this migration does NOT change (guardrails restated):** it does not re-decide OTel GenAI, Phoenix, or Langfuse — those stay DISCHARGED; it does not hard-wire a collector; it does not touch the verdict layer; and it adds no dependency without a separate, explicit gated act (flagged above as the one open finding).



Changes    +0 -0
AI Credits 36.73 (2m 20s)
Tokens     ↑ 556.8k (488.0k cached, 68.7k written) • ↓ 9.8k (3.7k reasoning)
Resume     copilot --resume=f7661a86-218b-4303-8516-da9bd53a91ff
