# Archive copy of transport file DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 3bdccf8eadc49903. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
supersedes: DIGEST-OUTER-LOOP-RESEARCH-2026-10-14-v1-superseded.md
summary: v2, the final plan from Tech-Architect-44, decided by the operator's delegation on 2026-10-14 ("Pójdę za twoją rekomendacją"). v1 proposed building a new Python driver. That was wrong: the repo had already DECIDED the outer loop on 2026-09-09, as Conductor E. Rows carry their state in tasks/, a phase table lives in scripts/conductor.py, code fires the transitions, and required checks are the gates. It was filed as [#689] and [#669], both P1 and both OPEN. Only the read-only half exists: conductor.py's phase gate and a report-only phase-gate job; 0 task files carry `phase:`. The plan is to finish what was ruled, using the research below as the reason, starting on its own fallback B (local, every vendor CLI signed in on subscriptions), with vendor roles in the registry, Gemini through agy first for reading, Grok admitted as a reviewer, and one steel-thread row before anything else is built. Section 8 lists what changed between my four formulations today and why.
by: Tech-Architect-44 (outgoing, 2026-10-08-dev-knowledge-architect, SEQ 1; Claude Code session aafe072f-4da2-5256-b29a-5c61187468a0, remote cse_014RFuLQH4gyfcjTpnbLRwAD)
to: Tech-Architect-45; the operator

# DIGEST — the outer loop: research, decision, plan (v2, final)

## 1. Why the problems recur (witnesses on main `b46836c8`)

1. **The program is prose, and the executor may skip it.**
   - `protocols/` is 1,414,034 B; `CLAUDE.md` is 24,100 B; the transport registry has 112 kinds; `.claude/commands/lane-boot.md` is 11,975 B.
   - Slash commands are markdown prompts; only scripts and hooks are code.
   - Instruction compliance falls as the instruction count rises (Jaroslawicz et al. 2025; AgentIF; both cited second-hand in anthropics/claude-code #32163).
2. **Organs without a `main()`.** 73 organs (21 DEAD); 232 processes (103 UNOBSERVED; DIGEST-PHASE0 E0). Each organ was a lane whose Done-when was its own unit tests.
3. **An LLM decides what runs next.** R99 and R104 name an Opus orchestrator. Anthropic's workflows page puts the difference in one row: "Who decides what runs next: Claude, turn by turn | The script".
4. **Gates sit at the end.** `land`, P11, the pre-push anchor and the commit hooks block, but only after the work is paid for. Nothing blocks at entry (PHASE0 E4).
5. **The producer grades itself.** BW's main thread was orchestrator, integrator and reviewer at once. Self-preference bias is measured (Panickssery et al., NeurIPS 2024).
6. **Decisions are made and then scheduled nowhere.** Conductor E was ruled on 2026-09-09 (`to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md`, option E, weighted 58 against A 52, B 55, C 38, D 46).
   - [#689] says so in its own title: "decided and unbuilt".
   - Five weeks and two architect seats later it is still OPEN, and neither the boot nor my handoff named it.

## 2. What the field does (sources at the end)

- **Anthropic, "Building effective agents".** Workflows are "systems where LLMs and tools are orchestrated through predefined code paths". It recommends prompt chaining with programmatic checks between steps, and an evaluator separate from the generator.
- **12-factor agents.** "Own your control flow": the LLM proposes and the code carries out.
- **Claude Code hooks.**
  - PreToolUse denies (`permissionDecision: "deny"` or exit 2).
  - UserPromptSubmit blocks or adds `additionalContext`.
  - Stop blocks, which forces Claude to continue.
  - There are prompt and agent hook types; agent hooks are experimental.
  - Managed hooks cannot be removed by project settings.
- **Claude Code headless.** `claude -p --output-format json --json-schema` returns `structured_output` and `total_cost_usd` (an estimate). `--max-budget-usd` caps spend; `--permission-prompts none` runs unattended.
- **Claude Code dynamic workflows.** A script in `.claude/workflows/` holds the plan; `agent()` takes a schema. The script itself has no shell. The repo already has one: `conformance-hub.js`, used for audits only.
- **On GitHub Actions, per vendor:**
  - `anthropics/claude-code-action` accepts a subscription token (`claude_code_oauth_token`, from `claude setup-token`), runs a fixed `prompt` in automation mode, and spends Actions minutes;
  - the Copilot coding agent works from an assigned issue and opens a PR;
  - `openai/codex-action` documents only `openai-api-key`;
  - `google-github-actions/run-gemini-cli` uses a Gemini API key (AI Studio), Vertex or Workload Identity Federation.
- **The field's verdict:** "Rules in prompts are requests. Hooks in code are laws."
- **Spec Kit and Kiro:** their gates are human and prose. They do not enforce.

## 3. The decision (operator, 2026-10-14, by delegation)

**D1 — Finish Conductor E. Do not design a new loop.** The rows that own the work already exist:
- **[#689]:** the `phase:` field in `tasks/<row>.md` plus its validator; the runner; required checks as gates.
- **[#669]:** the state machine over rows. Its transitions: intake ACCEPTED → row filed; row + contract → dispatched; merged → docs rendered, telemetry written, closure proposed; ratified → row archived. The operator's decisions stay the only manual transitions.
- **The spine** (`doit -f scripts/dodo.py spine`, 12 stages in `ecosystem/harness.yaml`) is the "row → contract" step. Its stage 1 reads `protocols/BUILD-LIST.md` and must read `tasks/`.
- **The lane's phases** follow the pilot's chain, in conductor.py's phase table: spec → RED tests → implement → constraints and dependencies → QA → two adversarial reviewers → judge → land. Each phase is a separate process (`claude -p --json-schema`, `copilot -p`, `codex exec`, `agy`), with an exit-code gate and a receipt.
- **This replaces R104's LLM orchestrator.** Opus keeps the plan, judge and architect-review phases.

**D2 — The runner starts on E's own fallback B.** B is "same task files, same graph, same phase table, run locally".
- **Why B first:** every vendor CLI is signed in on the laptop with a subscription (R87, no API keys). Actions minutes are at 364 % of the included amount (10,921 of 3,000; `quota_watch`). Codex and Gemini document only API keys in Actions.
- **The move to Actions (E proper)** happens per vendor, once its credential is sanctioned. Claude goes first (an OAuth token is allowed). Copilot follows through its native coding agent.
- **Cost and the API-key exceptions** are the operator's decisions.

**D3 — Vendor roles live in code** (`ecosystem/provider-registry.yaml` + `provider_router`), not in orders:
- **read, summarize, bulk evidence:** Gemini through agy FIRST. `provider_router route read` already ranks antigravity first (DIGEST-TOOLS-IN-USE), so orders stop overriding it. Copilot Enterprise is second. (Phase 0 spent 738,542 Claude subagent tokens on reading.)
- **implement:** Copilot (Sonnet 5.5, or Opus 5.5 by tier); Codex for bounded code; Claude Sonnet as fallback.
- **review:** Codex, then Grok (xai admitted for review), then Gemini. Never the producer's vendor; at most 2 rounds.
- **RED tests:** Claude Sonnet 5.5. **Plan, judge, architect review:** Claude Opus 5.5.
- **Model ids** come from each CLI's own list at run time (a registry currency check). The `claude-sonnet-5` and `haiku-4-5` pins are replaced. New Gemini and Antigravity model names: UNVERIFIED until agy lists them.

**D4 — agy in a Codespace:** one device login at Codespace creation is the accepted design. The operator, earlier on 2026-10-14: "Logowanie do AGY jest w momencie tworzenia Codespacu". It does not block a Codespace lane.

**D5 — Turn on what is built, after main is green, before any build:**
- **(a)** `transport.py janitor --apply` + `index --write` (it moves superseded files and deletes nothing). Done when INDEX ≤ 40 KB and lists current files only.
- **(b)** Land D5 (boot v2) with its HIGH fixed, carrying THE FLOW, MAP-DISPATCH, the `--dispatch-map` generator (today only on the D5 branch), and [#689] and [#669] as the plan. The Project copy of HANDOFF_BOOT is re-written in the same act.
- **(c)** R101, R102, R104 and this entry go into STANDING_RULINGS.
- **(d)** commit-gate, ship-gate and phase-gate lose `continue-on-error`. TA-45 gives the operator the exact command to enforce the main ruleset.

**D6 — One steel thread, then a prose freeze.**
- One real backlog row goes through B end to end. Done when: the row closes on main; there is a receipt per phase; a planted failure halts at its phase.
- Until then: no new organ, transport kind, command or order beyond the two running sessions and D5.
- The browser rules only at INPUT_REQUIRED points and reads at most 20 KB per turn.

## 4. The order of work

| # | What | Done-when | State now |
|---|---|---|---|
| 1 | TA-45's two sessions finish: green-main pilot, codespace-finish | LANE-END-green-main, DIGEST-HOW-WORK-RUNS, LANE-END-codespace-finish | running; QUESTION dispositions written 17:02; codespace rebased `0d97edde` 18:39 |
| 2 | D5 (a)–(d) | as in D5 | after green |
| 3 | [#689] build, locally: the `phase:` field + validator; the phase table in conductor.py from the pilot's chain; phase-gate blocking | `validate_backlog` refuses a row with no phase; the phase gate fails a skipped phase | input = the GAP list from DIGEST-HOW-WORK-RUNS |
| 4 | [#669] transitions, fired by code; spine stage 1 reads `tasks/` | [#669]'s own Done-when (a trip-test per transition, and a test that it does not fire on the state before it) | after 3 |
| 5 | Steel thread (D6) | as in D6 | after 4 |
| 6 | Everything else as rows through the loop: D1 producer launch, D7 trailers, Codespace as a substrate, R103 trial cut, boot-drift gate, Actions per vendor (D2) | each closes through the loop | — |
| 7 | Remove the prose the loop replaced (ADR-125; [#689] §5 lists it: the dispatcher and integrator seats, most of PLAYBOOK Ch8, "paste this to the integrator") | the operator's act | — |

## 5. Expected GAPs in the two running sessions

- `gen_handoff.py --dispatch-map` does not exist on main. It is only on the D5 branch, `gen_handoff.py:3591` there. MAP-DISPATCH (to-browser, 2026-10-10) was generated by unlanded code.
- agy has no credential file to mirror (`codespace_parity.py`, "BLOCKED-AUTH"; Windows Credential Manager `gemini:antigravity`). Under D4 a device login at creation is accepted.

## 6. Compatibility with my earlier files

- **Register v5 §9.4 is compatible** and folded into D3 and D5:
  - the reading contract becomes the ≤ 20 KB rule;
  - the six boot gaps go into D5(b);
  - the distiller emitting a vendor becomes D3, read from the registry.
- **The ANSWER to the plan review (7 corrections)** still holds: L1 and L2 split, L4 independent, L9 boot drift. Those lanes now enter through step 6.

## 7. Answers to the operator's 24 questions

They are in `to-browser/DIGEST-HANDOVER-ANSWERS-2026-10-14.md`.

## 8. What changed between my formulations today, and why (consistency log)

| When | What I said | What changed | Why |
|---|---|---|---|
| v1 of this file (16:51) | build a new Python driver; an ADR; B-1 = P0–P3 | — | research only, without checking the repo |
| handover paste 2 | do not build a driver; arm the existing spine; let the two sessions finish; agy optional | driver → spine | I read `dodo.py` and `harness.yaml`: the spine is a halting doit runner |
| handover paste 3 | decisions by delegation; agy is a first-class read route; vendor roles in code | agy optional → agy first | the operator's stated will |
| v2 (this file) | finish Conductor E, [#689] + [#669], on fallback B first | "spine executes" → "finish the loop that was already ruled; the spine is its contract step" | I found [#689] and [#669]: the same answer, ruled on 2026-09-09 and never built |

The direction never changed: control flow in code, models called per step, gates on exit codes, one steel thread, use what exists. The specifics changed three times. Each change came from a witness I should have read before writing v1.

## Sources

- https://www.anthropic.com/research/building-effective-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/workflows
- https://code.claude.com/docs/en/github-actions
- https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
- https://paddo.dev/blog/12-factor-agents
- https://github.com/anthropics/claude-code/issues/32163
- https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639
- https://glukhov.org/ai-devtools/ai-coding-assistants/spec-kit-vs-kiro-vs-claude-code/
- https://arxiv.org/abs/2404.13076
- https://learn.chatgpt.com/docs/github-action
- https://github.com/google-github-actions/run-gemini-cli
- https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/
