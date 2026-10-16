# Archive copy of transport file DIGEST-VERIFY-providers-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-providers-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 7f011dae99ab6447. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-d-telemetry-providers (claude-sonnet-5-5), V10 providers

Nonce probes, one per CLI, stdin closed.

| element | class | witness | caller |
|---|---|---|---|
| claude -p --json-schema --model claude-sonnet-5-5 | WORKS | nonce NONCE-41950 back: `"structured_output":{"nonce":"NONCE-41950"}`; served `modelUsage` key `claude-sonnet-5-5`; `total_cost_usd":0.224222`. Stray `'m' is not recognized` cmd-shim line on stderr | provider_router, dispatch |
| codex exec -m gpt-6-astra | WORKS | nonce NONCE-60144 back; header `model: gpt-6-astra`, `provider: openai`; 19,268 tokens | reviewer role |
| copilot -p -s --model gpt-5.6-terra | WORKS | nonce NONCE-43970 back; served id not disclosed in its log (requested id only) -> UNATTESTED | plan-review fallback |
| copilot Enterprise model list | UNRUN | no CLI verb lists the catalog; asking the model returned only `gpt-5.6-terra` (a self-report, not a catalog) | n/a |
| grok -p --max-turns 1 | BROKEN | `Max turns reached` / `Error: max turns reached`, no nonce | contract invocation shape |
| grok -p --max-turns 2 | WORKS | `**NONCE-12946**`; `grok models` default `grok-4.20-0309-non-reasoning` (not echoed by the run, UNATTESTED) | substitute reviewer |
| agy -p (stdout) | WORKS | nonce NONCE-90904 back; log: `selected model override ... label="Gemini 3.8 Flash (High)"` | bulk reading |
| provider_bench census: gemini 0.56.0, cursor-agent 2026.09.08 | UNRUN | PRESENT in census, not in the contract's probe list | n/a |
| provider_bench census: ollama | BROKEN | `Warning: could not connect to a running Ollama instance` | none found |
| provider_bench census: aider, llm, amp | DEAD | `ABSENT`; caller search: `provider_bench census` lists them, nothing probes them | n/a |

PREMISE-FAILED: contract "grok `--max-turns 1`" -> one turn cannot return text; 2 turns can.
PREMISE-FAILED: contract "agy 1.2.2" in provider_bench report -> census shows agy 1.3.5.
DECIDED-BY-LANE: one retry used on grok only (turns 1 -> 2).
No DUPLICATE found.

CHECKER
vendor: OpenAI via codex exec; served model (header line): `model: gpt-5.6-terra`; stdin closed. Workspace-write sandbox.
rows re-run: 7. The checker's sandbox blocks writes to user dirs, so most of its DISAGREEs are its own `Access is denied`, not a disagreement about the CLI. Both readings stand; the first lane reading is the only one run unsandboxed.
- grok --max-turns 1 | AGREE | `FS_PERMISSION_DENIED: Couldn't create session` (it also could not answer; a different error than ours, same non-answer)
- grok --max-turns 2 | DISAGREE | `FS_PERMISSION_DENIED: Couldn't create session` (sandbox)
- copilot | DISAGREE | no response captured before its 30-second runner cutoff
- agy -p | DISAGREE | `Authentication required` after expired token/network refusal (sandbox network)
- claude -p | DISAGREE | `'m' is not recognized as an internal or external command` (the same cmd-shim noise the lane saw)
- census ollama | DISAGREE | `uv` failed initializing its cache: `Access is denied`
- census aider/llm/amp | DISAGREE | same `uv` cache error
OPERATOR-ACTION: re-run the provider checker unsandboxed or from a lane with a writable uv cache (the checker cannot reach the user dirs these CLIs write to).

USAGE
claude: 1 probe USD 0.224. agy calls: 1 probe. Copilot: 2 calls (probe, model list). codex: 1 call. grok: 2 calls.

