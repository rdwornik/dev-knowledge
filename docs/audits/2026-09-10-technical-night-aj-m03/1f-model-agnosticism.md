# 1f — model-agnosticism audit of our process

**Reader:** Claude Sonnet subagent — **ORDERED** by the mission ("one Claude Sonnet subagent").
Read-only; it reported findings as text and this file was written by the session, not by the agent.
**Model:** `claude-sonnet-5` (the `sonnet` alias).
**Exact invocation:** `Agent(subagent_type="general-purpose", model="sonnet", prompt="<eight-surface model-agnosticism audit, read-only>")`.
**Wall time:** 749.9 s. **Tool calls:** 55. **Tokens:** 154,674.
**Scope read:** the worktree, plus `C:\Users\1028120\.claude\ROUTING.md` and `C:\Users\1028120\.codex\` (both exist; the `.codex` session store was opened to settle a structural claim).

**R2 status: UNVERIFIED at row level.** The rows below are the reader's own opened-and-quoted
citations; they were not independently re-checked. A Claude subagent verifying a Claude subagent
is weak evidence and the budget went to leg 1c instead. Carried and labelled per R2, not promoted.

**One row IS verified — by execution rather than by reading, and it is not in the reader's
table.** See MA-1 below.

---

## MA-1 — the finding the audit did not make, and the night measured

**`.claude/settings.json:21` — `PreToolUse`, matcher `"*"`:**

```
"command": "python \"$CLAUDE_PROJECT_DIR/scripts/fleet_health.py\" --prompts-guard"
```

`cursor-agent` reads and honours this hook. It does **not** define `$CLAUDE_PROJECT_DIR`. The
variable expands empty, the command becomes `python C:\scripts\fleet_health.py`, the interpreter
exits non-zero, and matcher `"*"` turns that into **a refusal of every tool call, with no
in-session escape**. Two full `cursor-agent` runs were consumed proving it (NIGHT-LOG, leg 1e).

| BREAKS-ON-CODEX | BREAKS-ON-GEMINI | BREAKS-ON-GROK | SEVERITY |
|---|---|---|---|
| Any reader that honours Claude-Code-shaped hooks without setting Claude-Code's env vars is wedged identically. `codex` was not wedged tonight because it does not read `.claude/settings.json` — which is luck, not design. | same class | same class | **blocking** |

**Why it outranks every row in the table below:** the table describes places a swap would *lose*
capability. This describes a place where a swap makes our own configuration **actively hostile**
to the new reader, and where the symptom (`can't open file 'C:\scripts\fleet_health.py'`) points
at the reader rather than at us. It was found by running a non-Claude CLI against the repo, which
is the one thing none of our checks do.

---

## The reader's table

LOCATOR | SURFACE | ASSUMPTION | BREAKS-ON-CODEX | BREAKS-ON-GEMINI | BREAKS-ON-GROK | SEVERITY
---|---|---|---|---|---|---
`scripts/gen_lane_contract.py:129` `MODEL_ENUM = ("opus","sonnet","haiku")` | 5 dispatch verbs | the lane-contract Model cell is a closed enum of Anthropic tier names, enforced via `click.Choice(MODEL_ENUM)` at `:949` | breaks — `--model gpt-5.6-terra` refused at the CLI | breaks — no `gemini-*` token accepted | breaks — no `grok-*` token accepted | blocking
`scripts/gen_lane_contract.py:332-335` | 5 dispatch verbs | `parse_contract` REFUSES any model token outside the enum when re-parsing an emitted contract | breaks — a hand-edited contract naming a non-Anthropic model fails validation | breaks | breaks | blocking
`scripts/gen_lane_contract.py:833-835` | 5 dispatch verbs | the same enum enforced a second time on the routing-row extraction path | breaks | breaks | breaks | blocking
`templates/prompt-template.md:66-74` | 5 dispatch verbs | every M/L lane prompt must declare Model as one of the three Anthropic tier names; the text records the prior failure (four contracts wrote a non-conforming cell and fell back to manual launch) | breaks — a Codex-routed lane cannot express its model without failing `dispatch`'s parse | breaks | breaks | blocking
`scripts/gen_lane_contract.py:172`, `:525` (`parts.append("claude")`) | 5 dispatch verbs | the interactive dispatch shape is hardcoded to the `claude` binary, not an abstracted "start a session" verb | breaks — `codex` has no `--worktree`; no emitted form exists | breaks | breaks | blocking
`protocols/PLAYBOOK.md:2922-2977` | 4 Ch8 / 5 dispatch verbs | dispatch routes by *which verb the operator types*; no verb takes a provider argument, and a contract's `Substrate:` field is "documentation only" | breaks — no verb exists to launch a Codex-driven local lane | breaks | breaks | blocking
`protocols/PLAYBOOK.md:4565-4570` | 4 Ch8 | the model-choice heuristic is stated entirely in Anthropic tier vocabulary, with no capability-based fallback | degrades — becomes inapplicable prose | degrades | degrades | degrading
`protocols/PLAYBOOK.md:3566-3576` | 4 Ch8 | the canonical routing matrix every dispatched lane cites is keyed on the three Anthropic tier names | degrades — no row a non-Anthropic dispatch can select | degrades | degrades | degrading
`protocols/PLAYBOOK.md:4628` | 4 Ch8 / 7 registry (S17) | the M tier's canonical binding is the literal id `claude-sonnet-5`, asserted by `check_provider_registry.py::check_s17_playbook` | breaks — S17 has no branch for a non-Anthropic M-tier id | breaks | breaks | blocking
`protocols/PLAYBOOK.md:4629` | 6 browser contract / 4 Ch8 | the XL tier reserved for the architect layer is a named Anthropic product (Claude Fable 5) whose only fallback is another Anthropic model (Opus) | breaks — no XL rung is non-Anthropic | breaks | breaks | blocking
`.claude/agents/artifact-reader.md:8` `model: claude-sonnet-5` | 8 agent frontmatter | the one committed subagent definition pins a literal Anthropic id in a field the harness actually reads | breaks — no equivalent frontmatter contract outside Claude Code | breaks | breaks | blocking
`.claude/agents/artifact-reader.md:30` | 8 agent frontmatter | the prose escalation path names a second literal Anthropic id as the only upgrade target | degrades | degrades | degrades | degrading
`.claude/workflows/conformance-hub.js:150-152` `model: 'claude-sonnet-5'` ×3 | 8 workflows | per-stage model pinned as a literal string in a JS object parsed by the Workflow runtime | breaks — the Workflow tool is itself Claude-Code-specific | breaks | breaks | blocking
`scripts/check_provider_registry.py:13-16` | 7 registry | the registry's stated purpose is DETECTION of drift across hardcoded copies, not ELIMINATION of hardcoding — "A swap still edits N files; what changes is that it can no longer edit N-1 of them and ship" | no break — but it PROVES the swap is still N files, not 1 | same | same | degrading
`ecosystem/provider-registry.yaml:143-153` | 7 registry | the registry itself records that the M-tier model is pinned in three independently-edited places (S9, S10, S17) | no break — this is the registry's honest accounting, and the evidence base for the change set | same | same | cosmetic
`ecosystem/routing-table.yaml:23-24` | 7 registry / 3 ROUTING | the authoritative role→CLI table names `claude-code` as THE producer, Codex only as a "bounded alternate" | degrades — Codex-as-producer is an exception path, not a swap | breaks (no row) | breaks (no row) | degrading
`~/.claude/ROUTING.md:22` `## SONNET (default Claude Code session)` | 3 ROUTING | the routing rule names "Claude Code session" as the default execution channel for the tier | breaks — the heading itself asserts the vendor | breaks | breaks | blocking
`~/.claude/ROUTING.md:31` `## OPUS (via opusplan, planning mode)` | 3 ROUTING | routes architecture work through `opusplan`, a Claude-Code launch mode, not a generic planning mode | breaks — no Codex equivalent | breaks | breaks | blocking
`~/.claude/ROUTING.md:174` (generated block) `\| producer \| claude-code \|` | 3 ROUTING | the L0 rendered copy repeats the hardcoded producer row | breaks | breaks | breaks | blocking
`protocols/HANDOFF_PROCESS.md:447-448` | 6 browser contract | the browser's documented role names `opusplan` as the routine path it need not intervene on | breaks — vacuous for a Codex-driven routine | breaks | breaks | degrading
`protocols/OPERATOR-INTERFACE.md:229-238` | 6 browser contract | the whole architect-seat delivery mechanism is built on the claude.ai **Project** feature — a proprietary product surface with a knowledge/instructions split no other vendor's web UI reproduces | breaks — no analogue | breaks | breaks | blocking
`protocols/HANDOFF_BOOT.md:116` | 1 handoff / 6 browser | HANDOFF_BOOT — the ONE file resident in the claude.ai Project — itself names `opusplan` | breaks | breaks | breaks | degrading
`protocols/HANDOFF_BOOT.md:178` | 1 handoff | the canonical worktree instruction names the literal `claude --worktree <name>` and says NOT to use raw `git worktree add` | breaks — a Codex session literally cannot execute the instruction, and the fallback is the thing forbidden | breaks | breaks | blocking
`templates/handoff/v5/HANDOFF_BOOT.md.tmpl:100` | 1 handoff (template) | the same literal command baked into the template every generated bundle inherits | breaks | breaks | breaks | blocking
`protocols/HANDOFF_PROCESS.md:906` | 1 handoff | lane-visibility doctrine ("VISIBLE = DISPATCHED") is defined by the `claude agents` subcommand | degrades — no such view for a non-Claude lane | degrades | degrades | degrading
`protocols/HANDOFF_PROCESS.md:1039` | 1 handoff | the TOKEN-LOG cadence is sourced from `ccusage`, which reads Claude Code's own local usage data | breaks — no equivalent wired in; a Codex seat produces no usage snapshot | breaks | breaks | degrading
`scripts/gen_handoff.py:794-806` `_session_slug` | 1 handoff | live-session and worktree-ownership detection globs `~/.claude/projects/<slug>/*.jsonl` | **breaks, confirmed by inspection** — `C:\Users\1028120\.codex\` stores sessions under `.codex/sessions/` + `thread_history_1.sqlite`; the glob returns zero matches, so **every Codex worktree reads as "unowned"** by the direct-evidence leg | breaks | breaks | blocking
`scripts/gen_handoff.py:1206` | 1 handoff | the row-9 preflight locator string itself names the Claude-Code session store as half its evidence | breaks — the preflight row is structurally blind to a non-Claude architect | breaks | breaks | blocking
`.claude/commands/lane-boot.md:105` | 5 dispatch / 2 boot | `/lane-boot`'s dispatch-line composition bottoms out at the `claude`-rooted dispatch table | breaks | breaks | breaks | blocking
`.claude/commands/handoff-verify.md:104,113` | 1 handoff / 5 dispatch | the probe gate checks liveness of the Claude-rooted dispatch verbs only; no parallel verb set is ever probed | no mechanical break, but it verifies only that path's existence | same | same | cosmetic
`ARCHITECTURE.md:312` `- **L3 — Claude Code**: executor` | structural | the canonical three-layer model names Layer 3 itself "Claude Code" rather than an abstracted executor role | degrades — every downstream "CC" cites this layer name | degrades | degrades | degrading
`scripts/cost_usage_telemetry.py:50-52` | 8 pinned ids | `system="anthropic"`, `request_model="claude-opus-5"` hardcoded | degrades — a swapped seat's telemetry misreports `system`; flagged as an S2-class code seam the registry declares OUT of scope | same | same | degrading
`scripts/offload_admission.py:649-650` | 8 pinned ids | fixture data hardcodes an Anthropic id as the illustrative served model | no break — reads as example data | no break | no break | cosmetic

## MINIMUM-CHANGE-SET

The reader's ordered list, kept as given. Item 0 is added by the session from MA-1.

0. **`.claude/settings.json:21`** — make the `PreToolUse` guard resolve its own path without
   `$CLAUDE_PROJECT_DIR`, or narrow the `"*"` matcher, or fail **open** when its interpreter is
   missing. Until then a non-Claude reader is not merely degraded, it is refused. *(MA-1;
   measured, not read.)*
1. `scripts/gen_lane_contract.py:129-130` — replace the literal `MODEL_ENUM` / `DEFAULT_MODEL`
   with a value read from one config source, and repoint the four call sites (`:332`, `:833`,
   `:949`, `:1119`) at that source.
2. `templates/prompt-template.md:66-74` — change the Model-cell rule to cite the enum the
   generator declares, rather than restating the three literal tokens, so the two cannot drift.
3. `protocols/PLAYBOOK.md:3566-3576` and `:4565-4570` — re-key the routing matrix on capability
   tiers (S/M/L/XL), with vendor names as one instantiation rather than the vocabulary itself.
4. `scripts/gen_lane_contract.py:172,180,401-407,525,996,1126` and the `PLAYBOOK.md:2909-3116`
   dispatch table — parameterise the `claude` / `claude --worktree` literals behind the same
   config source.
5. `.claude/agents/artifact-reader.md:8` and `.claude/workflows/conformance-hub.js:150-152` —
   repoint both at the registry's `subagent-default` role lookup, and extend S9/S10 to fail on a
   *swapped* registry value, not only on a drifted `claude-sonnet-5`.
6. `~/.claude/ROUTING.md:22,31` and `ecosystem/routing-table.yaml:23-24` — rename the tier
   headers to capability names and make `producer.cli` a variable set once.
7. `protocols/OPERATOR-INTERFACE.md:229-238` — **not a find-and-replace.** The claude.ai Project
   has no drop-in equivalent. This needs an explicit decision: keep claude.ai as host regardless
   of which model answers inside it, or redesign the delivery mechanism. Name it as a decision
   point.
8. `scripts/gen_handoff.py:794-806,1173-1206` — add a second direct-evidence leg reading the
   swapped architect's own session store; `~/.claude/projects/<slug>/*.jsonl` and
   `~/.codex/sessions/` + sqlite are structurally different and cannot share one glob.
9. `protocols/HANDOFF_BOOT.md:116,178` and `templates/handoff/v5/HANDOFF_BOOT.md.tmpl:100` —
   replace the literal `claude --worktree` / `opusplan` references with a pointer to whatever (4)
   resolves to. HANDOFF_BOOT is the first file every boot reads and the one file resident in the
   Project of item 7.

## WHAT IS ALREADY AGNOSTIC

Recorded so the report does not overstate the problem.

- **`ecosystem/provider-registry.yaml`** genuinely models seven vendors as peer entries with
  identity, CLI, version probe and role-admission fields. Real multi-vendor infrastructure — just
  not wired to the *architect* role.
- **`scripts/check_provider_registry.py`** is an honest, narrowly-scoped drift detector that says
  in its own docstring that it does not solve one-line swapping.
- **`~/.claude/ROUTING.md:48-79`** — the REVIEWER LANE fallback chain (terra → grok → Kimi/GLM/
  DeepSeek → Codex pay-as-you-go) is genuinely vendor-agnostic and cost-ascending, with explicit
  degraded-artifact tagging and served-model-id recording (the `[#492]` scar). **The reviewer role
  is the one place this repo already treats vendor identity as a substitutable variable** — which
  makes it the working model for what the architect role needs.
- **`ecosystem/routing-table.yaml:31-38`** — `fan_out` is already declared as a *list* of CLIs
  (`[luna, haiku, gemini]`) and held in agreement with L0 by `scripts/routing_agreement.py`.
- **`protocols/AI_COUNCIL_PROCESS.md`** is fully multi-vendor by design and records a real
  ratified vendor swap (synthesizer gemini→openai, 2026-07-18) — precedent that such swaps are
  do-able in this ecosystem.

---

## Rows this file is evidence for

- **[#582]** - *substrate router: one gated enum, a capability-keyed table, and the generator that reads it.* The MINIMUM-CHANGE-SET above is a measured inventory of exactly what that router would have to displace, with locators.
- **[#676]** - *provider CLI invocation shape.* MA-1 is an invocation-shape failure caused by our own hook config rather than by any provider.

