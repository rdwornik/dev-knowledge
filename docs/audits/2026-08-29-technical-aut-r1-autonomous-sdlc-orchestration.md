> **PROVENANCE — harvested cloud artifact, body VERBATIM below this header.**
> Lane `AUT-R1 autonomous-sdlc-orchestration` | receipt id `cse_01SnDbjafAyf8S14zaA4zdCF` | dispatched 2026-08-29, harvested 2026-08-29 by `Save-CloudSessionReport` (the `Harvest-Cloud` alias).
> Selection rule: the LONGEST assistant text, not the last — text #2 of 10 across 6 pages.
> Bytes written unchanged: **52,705**. Harvester reported no deviation.
> Nothing below this line was edited, reflowed or trimmed.

---

# AUT-R1 — Autonomous SDLC orchestration: industry pattern catalog with sources + fit-assessment

**Lane:** AUT-R1 (arc AUTONOMY) · **Substrate:** cloud, read-only · **Date:** 2026-08-29
**Repo state at survey:** `main` @ `7709613`, clean tree · **Rows birthed:** zero · **Commits:** zero · **Pushes:** zero
**Format note:** flat markdown, no pipe tables (CLAUDE.md §4 output-formatting — a painted table copies out as border glyphs). Not fenced as a whole, so the artifact opens at byte 0 with its own heading per the PLAYBOOK Ch8 harvest rule.

---

## 0. Method, and what to distrust in it

**What I ran.** Repo reads (Read/Grep/`sed`); `python3` invoked directly exactly once, to confirm the interpreter exists (`python3 -c "print('python3 ok')"` → `python3 ok`). **No gate was run and none is reported.** `uv run --locked` was not attempted, per contract.

**Source provenance is marked on every citation**, because egress here is heavily filtered and it changes what I can honestly claim:

- `[FETCHED]` — I pulled the page in this session and am quoting it.
- `[SNIPPET]` — the search tool returned the result and quoted content from it; I could not open the page. Treat figures as second-hand.
- `[BLOCKED]` — the domain is refused by this container's egress proxy (`anthropic.com`, `cognition.com`, `arxiv.org`, `docs.github.com`, `github.blog`, `githubnext.com`, `kiro.dev` all returned `EGRESS_BLOCKED`). Anything from those is `[SNIPPET]` at best.

**I invented no source.** Where I could not find a practitioner doing something, the pattern is labelled **HYPOTHESIS — no source found** and is not ranked.

**Repo locators: all resolved.** Every `file:line` and heading below was opened. Two resolution results worth stating up front because they change conclusions:

- `PLAYBOOK §2 "Creating a Claude Code Prompt"` **is not in Ch2 or Ch4** — it lives in **Part II, `protocols/PLAYBOOK.md:3886`**, with `How to choose Model` at `:3924` and `How to choose Mode` at `:3965`. The brief was right to ask.
- **`[#185]` (the GAP-2 backstop) is live and still not built** — `BACKLOG.md:52`, `tasks/185-gap-2-deterministic-gotcha-injection-guard.md`. **`[#184]` does not resolve to an open row** in `BACKLOG.md` or `tasks/`, consistent with ADR-87's "closes on empirical demonstration".

---

## 1. Ranking — patterns by fit × value

Ordered for the operator's build decision. Verdict enum is the ruled three.

1. **Contract-compiles-to-a-checked-plan, including substrate and model** (axis 1 + 2) — **partial**. Highest value: it is the repo's own named unbuilt organ.
2. **Telemetry-ranked catalog curation** (axis 5) — **absent**. Cheapest real win; the catalog is already past the size where selection accuracy is documented to degrade.
3. **Cross-artifact consistency check over the spec chain** (axis 1) — **partial**. The intake→ADR→row→contract chain exists; nothing checks it *across* artifacts.
4. **Deferred / on-demand catalog loading** (axis 5) — **partial**. Mostly free: the platform already does it for skills; the hub's own instruction layer does not.
5. **One machine-readable per-step routing source** (axis 2) — **partial**. Half-built and internally contradicted in prose.
6. **Propose-only unattended runs with safe outputs and a human adjudication gate** (axis 3) — **already-have-it** as doctrine, **partial** as enforcement.
7. **Consultation-with-weights** (axis 4) — **absent**, and I recommend **not building it**. The evidence base is contested-to-negative.
8. **Learned/dynamic model routing** (axis 2) — **absent**, and I recommend **not building it here**. Wrong population.

---

## 2. AXIS 1 — Prompt distillation / prompt-to-toolchain compilation

### Pattern 1A — The spec chain as durable, versioned repository artifacts

**What it is.** Loose intent is compiled, in named stages, into files that live in the repo and outlive the run. Not a distilled prompt — a *persisted* one.

**Who does it — primary.** **GitHub `spec-kit`** `[FETCHED github.com/github/spec-kit]`. Commands and their artifacts, as the repo states them: `/speckit.constitution` → `.specify/` (project principles, one-time); `/speckit.specify` → `specs/` ("what" and "why"); `/speckit.plan` → `specs/` (tech-stack choices); `/speckit.tasks` → `specs/` (work items); `/speckit.implement` → codebase; `/speckit.clarify` (resolve underspecified areas, recommended *before* planning); `/speckit.analyze` (cross-artifact consistency check, run after task generation); `/speckit.converge` (assess completion, appends remaining work); `/speckit.taskstoissues` (tasks → GitHub issues). Its own framing: "**specifications become executable**, directly generating working implementations"; the loop terminates on "Repeat steps 4 and 5 until `/speckit-converge` reports Converged." Roughly 2025, still active.

**Second instance, weaker sourcing.** **AWS Kiro** ships the same three-file shape (requirements / design / tasks). `kiro.dev` is **`[BLOCKED]`** here and I did not fetch it, so I record the pattern's second instance as *reported, unverified in-session* rather than quoting figures.

**Problem solved.** The plan stops being chat scrollback. A later reader can ask "what was this lane told to do" against a file rather than against memory.

**Cost.** Ceremony per feature; four artifacts to keep true; the spec becomes another thing that rots.

**Where it breaks.** spec-kit's own README, as fetched, carries **no explicit mandatory human approval gate** inside the workflow — convergence is agent-assessed. A chain of agent-written artifacts checked by an agent is a closed loop, and that is precisely where a bad compilation survives to burn a run.

### Pattern 1B — Compile-and-lock: the plan is machine-compiled before it may run

**What it is.** The authored intent is not executed directly. A compiler turns it into a locked, validated execution artifact, and *that* is what runs.

**Who does it — primary.** **GitHub Agentic Workflows (`gh-aw`)** `[FETCHED github.com/githubnext/gh-aw]`: workflows are "Markdown with YAML frontmatter"; **`gh aw compile` validates the source and generates a `.lock.yml`** workflow file that GitHub Actions actually executes. Frontmatter carries triggers, permissions, tools and **engine (model) selection**; the markdown body carries the task. Technical preview; reported as Feb 2026 `[SNIPPET InfoQ]`.

**Problem solved.** A bad compilation is refused at compile time, not discovered at minute forty of a run. The lock file is also the audit record of what actually ran.

**Cost.** Two representations to keep in step (source + lock), and a compiler to maintain.

**Where it breaks.** A compiler checks *shape*. Nothing in the fetched material claims it checks whether the workflow's stated intent is true.

### Fit-assessment — axis 1

**Verdict: `partial`.** The repo has more of this than the industry average, and is missing the two checks that make it safe.

**What exists (organ + locator).**
- **The ADR-98 intake pipeline** — `protocols/PLAYBOOK.md:3891` "The intake pipeline — intent → intake doc → decomposition → epic lanes (ADR-98)": functional architect → intake doc with **ex-ante acceptance criteria**, technical architect → triage + decomposition, developer → epic lane where "UAT at EPIC RETURN = the intake doc's acceptance criteria **verbatim**". This is spec-kit's chain, authored a year of this repo's history earlier, and with the approval gate spec-kit lacks: "**Confirm-gated:** the operator approves the draft before it lands in `docs/intake/`" (`:3896`). Live corpus: `docs/intake/README.md` reports 55 intake documents grouped by status (generated block — cite the generator, `scripts/gen_intake_index.py`, not the number).
- **The contract compiler** — `scripts/gen_lane_contract.py`. Its docstring is the strongest statement of Pattern 1B I found anywhere, in or out of this repo: "A generator removes the class rather than warning about it: the mechanical regions of a contract are BAKED IN here, so a contract cannot be emitted missing its decision budget, missing its worktree-file pairing line, or naming an effort tier the dispatch surface refuses." Provoked by a measured failure — batch 6 passed the branch name where the flag takes the bare worktree name, "uniformly across all twelve lanes, and nothing surfaced it until the integrator's merge queue matched 0 of 12".
- **The compile-time gate** — `lane-contract-check` (CLAUDE.md §9), `scripts/gen_lane_contract.py check`: mandatory sections present, dispatch line and routing row agreeing on tier, worktree⇄file pairing self-consistent.
- **`/preflight`** (`.claude/commands/preflight.md`) — locator verification before acting, "wired into no gate".

**What is missing, precisely.**
1. **No cross-artifact consistency check.** `/speckit.analyze` has no counterpart here. `check-against-spec` enumerates reconciliation sites when a *spec version* advances; it does not ask whether an intake doc's acceptance criteria, the ADR that ruled it, the `tasks/` row and the lane contract still say the same thing. The repo has already paid for this absence: intake #46 (`docs/intake/2026-08-24-tech-contract-integrity-gate.md`) is titled "A contract states facts it has not verified — **and twelve of them were wrong in one window**".
2. **The compiler checks shape, not truth** — stated by the gate's own honest limit in CLAUDE.md §9: "it checks SHAPE, never whether a contract's footprint claims are true."

**Does the industry confirm, refine, or contradict ADR-87's by-class finding?** — **It refines it, and pressures one half.**

- **Confirms the mechanism half.** ADR-87 Decision 6 files GAP-2 to a deterministic backstop because "prose in this contract does **not** close it" — it had already recurred n=2/n=3 *with* the standing prose line. The industry's measured version of that argument is **IFScale** (Jaroslawicz et al., Distyl AI, arXiv 2507.11538, ~Jul 2025) `[SNIPPET — arxiv.org blocked]`: 500 keyword-inclusion instructions, 20 models across seven providers, and "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions", with a documented **bias toward earlier instructions**. That is external support for "an enforceable invariant belongs in a mechanism, not in prose" — and it indicts a 200-line always-on instruction file on the same grounds. Note this repo already holds this finding second-hand at `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md`; I am citing the primary because a quoted quote is not evidence.
- **Refines the by-class half.** ADR-87's structure is *conditional*: intent-only is reliable for code-impact, and the architect must supply a thin governance pointer for read-only / governance / gotcha-sensitive work. **The industry does not condition on class at all.** spec-kit and gh-aw compile an explicit artifact for *every* task, including trivial ones, and accept the ceremony to get the audit trail and the compile-time refusal. Their implicit claim is that the cheap-path exemption is not worth the classification surface — which is exactly the cost ADR-87 books as its accepted negative: "the architect must classify the task … misclassifying a governance task as code-impact silently re-opens GAP-3."
- **One honest pressure point, and it is a repo-side observation, not an industry one.** ADR-87 says "STEP 1 of this arc verified the answer **by class**", but **no dated measurement artifact for that verification resolves in-repo**. I grepped `docs/`, `protocols/` and `LESSONS.md`: the by-class finding appears only as restatement inside handoff bundles (`docs/handoffs/2026-06-18-dev-knowledge-architect/RESIDUAL.md:132`, and the same sentence carried forward in ten later `PASTE_THIS.md` files). The only sample size the ADR itself records is GAP-2's n=2/n=3. So the finding the whole equilibrium rests on is **restated eleven times and measured nowhere the tree can show**. That is not a contradiction of ADR-87 — it is the thing to re-measure before the industry pattern is judged against it.

**Cheapest experiment.** Take one already-closed lane (e.g. the batch-1 L1 arc `[#577]`/`[#584]` recorded at CLAUDE.md §12 v2.68) and run its intake doc, ruling ADR, `tasks/` row and frozen contract through a hand-written 30-line consistency reader that reports only disagreements in acceptance criteria, footprint and ids. If it finds ≥1 real disagreement on an arc everyone believes closed cleanly, Pattern 1A's analyzer is worth building; if it finds none on three arcs, it is not. **Tier S under ADR-112** — try it and keep or delete.

---

## 3. AXIS 2 — Per-step model routing

### Pattern 2A — Static, declared-per-step routing (the shipped shape)

**Who does it — primary.** **Claude Code subagents** `[FETCHED code.claude.com/docs/en/sub-agents]`. Routing is a declared field, and the precedence order is documented rather than emergent:

- `model` accepts "a model alias: `sonnet`, `opus`, `haiku`, or `fable`", a full model ID, or `inherit`; omitted defaults to `inherit`.
- Resolution order: **(1)** `CLAUDE_CODE_SUBAGENT_MODEL` env var → **(2)** per-invocation `model` parameter → **(3)** the subagent's frontmatter → **(4)** the main conversation's model.
- Routing pairs with capability restriction: `tools` (allowlist) and `disallowedTools` (denylist), "`disallowedTools` is applied first, then `tools` is resolved against the remaining pool".
- Discovery is a five-level precedence ladder (managed settings → `--agents` flag → `.claude/agents/` → `~/.claude/agents/` → plugin), with "the definition closest to the working directory wins".

**What drives the decision, in the shipped design:** *task class, declared by a human, once, in a file.* Not measured accuracy, not a budget.

**Evidence tiered routing beats single-model.** The most-cited figure is Anthropic's multi-agent research system — Opus lead + Sonnet subagents "outperformed a single-agent setup by more than 90 percent" on internal evals `[SNIPPET — anthropic.com/engineering/multi-agent-research-system is BLOCKED here]`. **I could not fetch it. Treat the 90.2% as second-hand.**

### Pattern 2B — Learned / dynamic routing

**Who does it — primary-ish.** **RouteLLM** (LMSYS) `[FETCHED github.com/lm-sys/RouteLLM]`: routers trained on Chatbot Arena preference data augmented with GPT-4-as-judge; router families `mf` (matrix factorization), `sw_ranking` (weighted Elo), BERT classifier, LLM classifier; a **calibrated cost threshold** turns "I want 50% strong-model calls" into a concrete cutoff, compared against a win-rate estimate per query. Headline: "reduce costs by up to 85% while maintaining 95% GPT-4 performance" on MT Bench, ">40% cheaper" than commercial routers, GPT-4-1106-preview / Mixtral-8x7B pair. Paper arXiv 2406.18665 (Jun 2024) `[SNIPPET]`, which adds 45% on MMLU, 35% on GSM8K, and "only 14% of queries needed the expensive model" for 95% of GPT-4 quality on MT-Bench, with transfer to a Claude 3 Opus / Llama 3 pair.

**Cascade variant.** FrugalGPT (Stanford, 2023) — chain cheapest-to-most-expensive, stop when confidence suffices — appears repeatedly in search results as the canonical confidence-gated cascade `[SNIPPET]`. **I did not fetch the paper; verify the identifier before citing it anywhere binding.**

### The negative direction — reported honestly, because it is strong

1. **Routing in production is a trust surface, not just a cost lever.** OpenAI's GPT-5 launch (7 Aug 2025) shipped a real-time router choosing between fast and thinking variants; the rollout became "a product and trust crisis", Altman conceded "the autoswitcher broke" for much of a day, and the durable fix was **giving control back** — explicit Auto / Fast / Thinking toggles, and later reporting that automatic switching was scrapped for free users `[SNIPPET — the-decoder, AIC, Storyboard18]`. **An opaque router is worse than a mediocre static one when a single operator has to trust it.**
2. **Tiered/multi-agent shapes cost 15× tokens.** "Multi-agent systems consume approximately fifteen times more tokens than standard chat interactions"; "token usage explains 80% of performance variance" `[SNIPPET, Anthropic — BLOCKED]`.
3. **Under matched compute, the tiered/parallel advantage often vanishes.** See §5 — the debate literature's normalization result applies to any fan-out shape, not only to debate.
4. **The single-writer objection.** Cognition's "Don't Build Multi-Agents" argues parallel subagents "make independent decisions… and those decisions conflict"; the recommended shape is a single-threaded linear agent with context compression, with extra agents contributing *intelligence, not actions* `[SNIPPET — cognition.com BLOCKED]`. This repo already independently reached the same conclusion by a different route — ADR-110's file-disjoint lanes plus one serial integrator, and N4 as "the batch's EXCLUSIVE `tasks/` writer" (`docs/audits/2026-08-28-technical-night-batch2-frozen-bundle.md`).

### Fit-assessment — axis 2

**Verdict: `partial`.**

**What exists.**
- **`ecosystem/routing-table.yaml`** — live, in-repo, machine-readable, with an agreement gate. Roles: `producer: claude-code` (Codex a *bounded* alternate), `reviewer: codex / gpt-5.6-terra`, `adversarial: sol`, `fan_out: [luna, haiku, gemini]` mode `retrieval-only`. It carries a scar worth quoting in full because it is the best in-repo evidence on this axis: "A fan-out head asked to COUNT returned a fabricated count — a number with no computation behind it, indistinguishable in shape from a measured one… a fabricated count is worse than a refusal because it reads as evidence."
- **`provider-registry-agreement`** pre-commit hook over `ecosystem/provider-registry.yaml` (CLAUDE.md §9), which since 2026-08-22 asserts the **pin count**, not only the values, because "a *deleted* pin passed clean until 2026-08-22".
- **The routing matrix** — `protocols/PLAYBOOK.md:2946` "Model + effort are stated at dispatch": opus default for anything touching `.dev-knowledge`; sonnet only "small **and** self-contained"; haiku retrieval only; `max` held out of dispatch routing.
- **ADR-87 amendment 2026-08-08** — the population boundary: architect states the session boot tier, CC routes sub-steps inside it.

**What is missing, precisely.**
1. **The routing matrix is prose and nothing reads it.** `routing-table.yaml`'s own scope note says so: "It does not rule on model tiers — routing doctrine's canonical table is L0, outside this repository." So the *role* axis is machine-readable and gated; the *tier* axis is a markdown table at `PLAYBOOK.md:2946` plus a file on the operator's disk.
2. **Two live surfaces disagree in the tree right now.** `PLAYBOOK.md:3922` and `:3927`: "**Model is CC's pick**… The architect does not choose Model", default "Opus 4.8". `PLAYBOOK.md:2949`: "The browser-architect states model **and** effort on every dispatch it emits." The collision is declared and scoped at `:3003–3012` and the residual is explicitly left open — "the equilibrium table and its §2 restatement still read as architect-excluded on the dispatch act itself." A machine-readable tier source would end this by construction; prose has now failed to for three weeks.
3. **The effort enum forks.** `gen_lane_contract.py` implements five (`low|medium|high|xhigh|max`) and logs a warning; `PLAYBOOK` Ch8 records four. The generator's docstring says correctly: "Choosing between the two enums is a ruling, and a generator is not the place one gets made." **Still unruled.**

**On the dispatch table's own stated limit — "what would the industry put there?"** The limit is real and I resolved it: `PLAYBOOK.md:2532` rules `dispatch <contract.md>` "**local-only**: it does not read a contract's `Substrate` field and cannot route, so today the substrate is chosen by **which verb the operator types**… and a contract's `Substrate:` line is **documentation only** until the Layer-3 router lands." Intake **#45** (`docs/intake/2026-08-24-tech-substrate-router.md`, `status: READY`) already specifies the fix and already names the failure it prevents: "**No cloud lane's commits passed a gate in this batch, because no hook was armed in any container**", with the compensating control living "in **prose in a hand-written batch contract**."

**The industry answer to that unbuilt router is Pattern 1B, not Pattern 2B.** gh-aw is the exact shape: frontmatter declares triggers, permissions, tools **and engine**; `gh aw compile` refuses an invalid combination and emits a lock file. Transposed here, the Layer-3 router is *not* a learned router — it is:

- one machine-readable substrate+tier source (intake #45's acceptance criterion 1: "A single machine-readable source names the three substrates and their capability facts; no second copy exists in prose"),
- read by `gen_lane_contract.py` (criterion 2: a cloud contract emits the mesh-re-run obligation without the author typing it),
- with an enum refusal (criterion 3, modelled on `validate_branch_naming.py`),
- and the dispatch verb selected *from the contract* rather than typed by the operator.

That is deterministic compilation. It needs no preference data, no win-rate model, and no trust in an opaque switcher — and the GPT-5 episode is the argument for keeping it that way.

**Where the industry assumption does not hold.** RouteLLM-class routing is trained on query distributions at platform scale. This repo is **one operator, a few dispatches a night, and a context load the routing matrix already calls high by construction**. There is no distribution to learn from, and the repo has already measured the failure of the cheap-tier heuristic in-house: a **shape-S arc on sonnet ran ~3h** against the gate mesh (`PLAYBOOK.md:2962–2973`), which is why the tier now keys on **context load, not task shape**. That measurement is worth more than any external routing benchmark for this corpus, and it points away from dynamic routing, not toward it.

**Cheapest experiment (for the router that is worth building).** Add a `substrate:` + `tier:` block to `ecosystem/substrate-registry.yaml` (the file already exists), have `gen_lane_contract.py` read it for exactly one field — the dispatch command — and dry-run it over the eleven grandfathered batch-1 contracts at `docs/audits/2026-08-21-*-lane-contract.md`. If the generator picks the same verb the operator actually typed in ≥10 of 11, the router is a compile step, not a research problem. **Tier S.**

---

## 4. AXIS 3 — Self-planning repositories

### Pattern 3A — Propose-only background agents with "safe outputs"

**Who does it — primary.** **`gh-aw`** `[FETCHED]`. The bounding mechanism is the interesting half, and it is architectural rather than exhortative: "Agents operate in **read-only, sandboxed mode by default**." For writes, "**Safe outputs buffer configured writes, validate them, and apply them in separate jobs with scoped permissions**." Named use cases include issue triage, PR review, CI-failure investigation, docs maintenance, dependency analysis, repository reporting. GitHub Next's umbrella framing is **Continuous AI** — "background agents that operate in your repository the way CI jobs do, but only for tasks that require reasoning instead of rules" `[SNIPPET — githubnext.com and github.blog both BLOCKED]`.

**How approval is represented:** as a *separate CI job with different permissions*. The agent cannot write; a downstream job with scoped credentials applies a validated buffer. Approval is a permission boundary, not a prompt instruction.

**Who does it — second instance.** **GitHub Copilot coding agent** — assigned an issue, works on a branch, returns a PR; GA reported Sept 2025, and it is the successor to the Copilot Workspace research preview `[SNIPPET — docs.github.com BLOCKED]`.

**Cost.** CI minutes, model spend, and a review queue that is now the bottleneck.

**Where it breaks — the sourced negative result.** **GitHub sunset Copilot Workspace on 30 May 2025** `[SNIPPET]`. Workspace's pitch was exactly "issue → editable plan → implementation, with the plan as a first-class artifact." The capability did not die — it was decomposed into the coding agent, agentic review, and MCP — but **the standalone plan-editing surface did not survive**. The lesson for axis 3: the durable unit is *a proposal that lands in the tracker the humans already read* (issue, PR), not a bespoke plan UI. Related casualties in the same window: Copilot Knowledge Bases retired 1 Nov 2025 (→ Spaces), GitHub-App Copilot Extensions deprecated 10 Nov 2025 (→ MCP) `[SNIPPET]`.

### Fit-assessment — axis 3

**Verdict: `already-have-it` (doctrine) / `partial` (enforcement).** This axis is the one where the repo is *ahead of* what I could source, and saying otherwise would be the failure the verdict enum exists to prevent.

**What exists (organ + locator).**
- **The night-batch protocol, five named phases** — `protocols/PLAYBOOK.md` Ch8, phases with inputs, outputs and **refusal conditions** each. Phase 3's refusal: "A night lane that merges, pushes, edits canon, closes a row or issues a ruling has left the propose-only envelope." Phase 4: "**Adjudication stays a human act in the morning.** The night produces proposals and evidence; **nothing merges unattended.**"
- **The frozen bundle** — `docs/audits/2026-08-28-technical-night-batch2-frozen-bundle.md`. This is the SEED mechanism the brief asked me to find, and it is *stronger* than the industry's declarative frontmatter: it is an immutable, committed artifact that folds the night's owed decisions (D1–D4, P5) into decided rulings **before any lane boots**, names the per-lane write-scope, names the exclusive `tasks/` writer, and carries the ratchet authorization. The manifest is committed **at dispatch**, not at close (`PLAYBOOK.md:1929`), so the batch is reconstructable from its *intent* and not only its outcome.
- **The harvest rules** — byte-identical landing, "the artifact wins and the Verification section records the deviation", and the **Stop-hook-noise trap**: "select the longest assistant text", because on the reference night the last text in all four sessions was backpressure noise from a container where `uv run --locked` could not start.
- **Phase 5, the ledger — a REQUIRED output.** Reference instances: `docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md` and `docs/audits/2026-08-29-technical-night-harvest-consumption-ledger.md` (both resolve). Its purpose line is the whole case for the phase: "if this chat or seat is lost, the next seat executes THIS file and nothing from the night is dropped." **Rejected items are listed with their reason** — I found no industry equivalent of that, and it is the half that stops relitigation.
- **The four standing constraints** — `PLAYBOOK.md:2348`: ~5 proposals/night cap; 7-day auto-expire on untriaged items; no autonomous semantic refactoring at night; proposals land in `docs/intake/` as `status: SEED`, "deliberately not a parallel `proposals/` folder".
- **Bounded review load** — ADR-110's 4–6 lane batch ceiling, "bounded by integration capacity, which is serial".

**What is missing, precisely — and the repo already says so.** `PLAYBOOK.md:2364`: "*Honest limit, and it is why the list reads as prose rather than as enforcement.* Each of the four is prose… **these four bind the seat and not the tree.**" The industry's answer to exactly this is gh-aw's safe-outputs: **the constraint is a permission boundary in a separate job, not a sentence in a contract.** The transposition is direct — a night lane's output validated and applied by a *different* step than the one that produced it — and it is the same argument ADR-85's amendment already won on the Stop hook ("an organ that can be exhausted cannot carry teeth").

Also missing and already owned: **`[#271]`'s survival review** — a dated `docs/audits/` artifact with a measured accept-rate against the `<20%` kill threshold. It is the row's *only* surviving Done-when after the 2026-08-28 re-cut, and it has not been run. Under ADR-111 this is **OWNED**, not a new finding.

**Where the industry assumption does not hold.** Every axis-3 instance I found assumes a CI cluster and a team of reviewers: gh-aw compiles to GitHub Actions, Copilot's agent returns PRs to a review queue. Here there is **one reviewer**, and the ceiling is his morning. That is why the ~5/night cap is the load-bearing constraint and the CI substrate is not — and it is why "scale up the fan-out" is the wrong lesson to import.

**Cheapest experiment.** Turn one of the four prose constraints into a check: a pre-commit or `audit.py` leg that fails when `docs/intake/*.md` gains more than five `status: SEED` files bearing the same night's date, or when a `SEED` older than seven days still has no triage verdict. One check, one test, one night of data. If the check never fires because the seat already holds the constraint, that is a measured answer too — record it and don't build the other three. **Tier S.**

---

## 5. AXIS 4 — Consultation-with-weights escalation

### The honest finding: genuine weighting is rare, and the evidence for the family is contested

**What exists as real weighting.**
- **Mixture-of-Agents** (Together AI, arXiv 2406.04692, Jun 2024; ICLR 2025) `[SNIPPET]` — layered proposers whose outputs feed an aggregator; 65.1% on AlpacaEval 2.0 with open-source models vs GPT-4 Omni's 57.5%. **This is aggregation by a learned aggregator, not weights** — the aggregator model decides what to keep. Calling it "weighted consultation" would be an overclaim.
- **Confidence-weighted aggregation** — the genuinely weighted form. Search-surfaced work states the case formally: "confidence-weighted aggregation is the Best Linear Unbiased Estimator (BLUE)… yielding strictly lower variance than uniform averaging" under an inverse-confidence noise model, and "confidence-weighted majority sums the confidences assigned to each answer" with votes weighted "by self-reported confidence (a 0–100 value the model is prompted to emit)" `[SNIPPET — arxiv.org BLOCKED; I could not fetch these papers and do not have verified identifiers for the two quoted above. Treat as a pointer to a literature, not as a citation.]`
- **Panels of judges** with track-record weighting: reported as "replacing a single judge with a panel of diverse models, showing improved agreement with human annotations", with the caveat "the reliability of LLM judges varies considerably across prompting strategies and aggregation methods" `[SNIPPET]`.

**Escalation without weighting** — which is what most systems actually ship: FrugalGPT-style cheapest-first cascades with a confidence stop `[SNIPPET]`; RouteLLM's calibrated threshold (§3). These are **plain escalation**, and the brief was right to ask me to separate them: a threshold on a scalar is a gate, not a weight.

### The negative results — and they are the most useful thing on this axis

- "**When and Why Does Multi-Agent Debate Fail and Does It Really Underperform?**" (arXiv 2510.20963, Oct 2025) `[SNIPPET — abs page BLOCKED]`: MAD "often fails to outperform simple single-agent baselines such as Chain-of-Thought and Self-Consistency, even when consuming significantly more inference-time computation"; both competitive and consensus protocols "exhibit debate hacking, and under matched token budgets, both underperform single-agent methods".
- "**Stop Overvaluing Multi-Agent Debate — We Must Rethink Evaluation and Embrace Model Heterogeneity**" (arXiv 2502.08788, Feb 2025) `[SNIPPET]`.
- "**Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets**" (listed as arXiv 2604.02460, 2026) `[SNIPPET]`: "across two datasets, three model families, and five different multi-agent architectures… single-agent systems match or outperform multi-agent systems when computation is normalized."
- Synthesis from the same result set: "Many reported multi-agent gains are better explained by **compute and context effects** than by inherent architectural superiority."

**Read that against Anthropic's +90.2%** `[SNIPPET, BLOCKED]`: the two are not necessarily in conflict — Anthropic's task was breadth-first web research, where parallel subagents buy *independent context windows*, which is a compute-and-context effect the debate papers would predict. It is weak evidence for debate-style weighted consultation on a *judgment* question, which is what this repo would use it for.

### Fit-assessment — axis 4

**Verdict: `absent` as weighting; `already-have-it` as bounded escalation.**

**What exists (organ + locator).**
- **The V-2 decision budget** — `protocols/STANDING_RULINGS.md:26–33`, quoted verbatim from intake #25 AMENDMENT-b: "agents may ask only about (a) curated-baseline touches, (b) genuine rule-vs-ruling conflicts, (c) fork classes with no standing ruling; everything else is decided per contract defaults and REPORTED in the end packet, not asked… Target metric: ≤2 operator interactions per lane-batch." Restated as per-lane requirement 2 at `PLAYBOOK.md:1880`. The application rule at `:35`: "a fork covered by an entry below is decided, applied, and reported — not escalated."
- **The two-seam interaction budget** — `PLAYBOOK.md:2008`: operator↔integration target exactly 2; operator↔lane target ≤1 escalation per batch, "reported in the packet rather than budgeted away". Both numbers reported, "neither substitutes for the other".
- **ADR-108 §A** — routing by *kind*: operator rules functional, architect rules technical, AI Council distils contested technical.
- **The retrieval-only scar** — `ecosystem/routing-table.yaml`, quoted in §3 above. This repo has already measured what happens when a cheap consulted head is asked a question with no checkable answer.

**Does consultation-with-weights extend the V-2 budget or compete with it?** — **It competes, and it loses.**

V-2 routes by **class of question**; weighting routes by **confidence in an answer**. They are different primitives, and the repo's is the one the evidence supports:

1. **V-2's scarce resource is operator attention, not accuracy.** ≤2 interactions per batch. A weighting scheme does not reduce interactions — it produces a *number* attached to a recommendation, which the single operator must then still adjudicate. It adds a surface without removing a round-trip.
2. **A confidence weight is exactly the artifact this repo already ruled against accepting.** The fan-out scar: a fabricated count "is worse than a refusal because it reads as evidence." A self-reported 0–100 confidence from a consulted model is the same object — an uncomputed number in the shape of a measurement — and this repo has a standing ruling about that class.
3. **The evidence base is contested-to-negative** at matched compute (above), and the reported gains are attributed to context effects the repo already gets from file-disjoint lanes with their own context windows.
4. **Contested outcomes already have a resolution rule.** ADR-108 §A resolves by *whose question it is*, which is deterministic and revertable. Weight-based resolution replaces a rule with an estimate.

**Recommendation: REJECT for build; keep as a recorded rejection with its reason**, per ADR-111's REJECTED outcome ("reason recorded, not relitigated"). The one genuinely additive piece is cheap and does not need weights: **have the AI Council's distillation carry, per contributing head, whether that head's prior distillations were later overturned** — a track record is a *measured* datum, unlike a self-reported confidence. That is a ledger, not a weighting scheme.

**Cheapest experiment (for the ledger, not the weights).** For the next three contested technical questions that reach AI Council, record in the consumption ledger which head's position the architect adopted. Three data points will not weight anything, but they will say whether the heads disagree often enough for the question to matter. If they agree 3/3, the consultation is ceremony and the finding is worth more than the organ. **Tier S — and it is nearly free, since the ledger phase already exists.**

---

## 6. AXIS 5 — Command / skill library curation with usage ranking

### Pattern 5A — Deferred loading: the catalog stops being resident

**Who does it — primary, with numbers.** **Anthropic's tool search tool** `[FETCHED platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool]`, tool versions dated `20251119` (so ~Nov 2025). Verbatim:

- "A typical multiserver setup (GitHub, Slack, Sentry, Grafana, and Splunk) can consume **~55k tokens in definitions before Claude does any work**. Tool search typically reduces this by **over 85 percent**, loading only the 3–5 tools Claude needs."
- "**Claude's ability to pick the right tool degrades once you exceed 30–50 available tools.**"
- Mechanism: `defer_loading: true` per tool; at least one tool must stay non-deferred; two search variants, `regex` (Python `re.search`, ≤200 chars) and `bm25` (natural language, ≤500 chars); both "search tool names, descriptions, argument names, and argument descriptions"; up to **10,000** deferred tools; results default to 5 per search.
- Prompt-cache safety: "the API excludes deferred tools from the system-prompt prefix… The prefix is untouched, so prompt caching is preserved."
- Its own "when to use" bar: **10 or more tools**, or definitions over 10k tokens, or "tool selection accuracy drops as your toolset grows."
- Curation advice that is really catalog hygiene: consistent namespacing (`github_`, `slack_`) "so one search matches the whole group"; "**Monitor which tools Claude discovers to refine your descriptions.**"

**The same principle, applied to skills** `[FETCHED code.claude.com/docs/en/skills]`: "In a regular session, **skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked**." And the recurring-cost warning: "Once a skill loads, its content stays in context across turns, so **every line is a recurring token cost**." Compaction detail worth knowing: re-attached skills keep "the first 5,000 tokens of each" under a "combined budget of 25,000 tokens", filled most-recent-first, "so older skills can be dropped entirely after compaction."

**Companion measure.** Programmatic tool calling — "roughly 38%" fewer billed input tokens on a 75-tool benchmark "with no change in task accuracy" `[SNIPPET — platform docs page not fetched for this figure]`.

### Pattern 5B — Measured curation: rank and retire by evidence, not by taste

**Who does it — primary.** Two mechanisms, both fetched:

1. **Usage telemetry.** `[FETCHED code.claude.com/docs/en/monitoring-usage]` — the OTel event **`claude_code.tool_result`** carries `tool_name`, `tool_use_id`, `success`, `duration_ms`, and "optionally `tool_parameters` with **`skill_name`** and `mcp_server_name` attributes". **`claude_code.tool_decision`** carries `tool_name`, `decision` (accept/reject), and with `OTEL_LOG_TOOL_DETAILS=1`, "**JSON string with tool-specific parameters including skill names, MCP server names, subagent types**". Metrics include `claude_code.cost.usage`, `claude_code.token.usage`, `claude_code.active_time.total`, `claude_code.commit.count`.
2. **Per-entry value measurement.** `[FETCHED code.claude.com/docs/en/skills]` — the `skill-creator` plugin's eval loop: test cases in `evals/evals.json`; "**Isolated runs**: spawns a subagent per test case so each run starts with a clean context, and **records token count and duration**"; "**Benchmark**: aggregates pass rate, time, and tokens for **with-skill versus without-skill** into `benchmark.json` so you can compare the **pass-rate improvement against the token and time overhead**"; "**Version comparison**: runs a **blind A/B** between two versions"; "**Description tuning**: generates should-trigger and should-not-trigger prompts, **measures the hit rate**, and proposes description edits when the skill activates on the wrong requests."

That last bullet is the closest thing I found anywhere to an answer for "how are overlapping entries deduped": you measure **mis-triggering**, and an entry that fires on another entry's prompts is the overlap, empirically identified.

**Cost.** A telemetry pipeline; an eval corpus per entry; the eval loop itself burns tokens.

**Where it breaks.** Telemetry measures *invocation*, not *value* — a skill invoked constantly may be load-bearing or may merely be first in the list. Only the with/without benchmark separates those, and it is the expensive half. And **no source I found addresses retirement policy**: every mechanism measures; none of them decides when to delete.

### Fit-assessment — axis 5

**Verdict: `partial` for deferred loading; `absent` for usage ranking.**

**What exists (organ + locator).**
- **`ecosystem/organ-index.md`** — generated inventory, gated by the `organ-index-freshness` pre-commit hook, covering `.claude/{agents,commands,skills,workflows,rules}`, `settings.json`, the pre-commit config and the plugin manifest, with distribution (`L0`/hub/plugin/pre-commit) and status (`ARMED`/`RETIRED`/`DECLARED`). At HEAD its generated header reports **55 organs across 8 classes** (cite `scripts/generate_organ_index.py`, not that number — it is stale at the next commit). Its own stated non-coverage: it does not carry failure posture.
- **`.claude/generated/commands-repo.md`**, `.claude/methodology-roster.md`, `docs/intake/README.md`, `docs/audits/README.md` — all generated, all drift-gated. The repo's index discipline is genuinely better than anything I surveyed.
- **The retirement ranking R1–R4 + the auto-retirement prohibition** — `protocols/STANDING_RULINGS.md:92`, homed by declaration to the `[#488]` row body. Status: `docs/audits/2026-08-08-technical-successor-prep.md:76` records it **DORMANT** since the `[#487]` engine refutation. So a ranking exists as vocabulary and is inert.
- **`[#488]`'s ruled successor** — `tasks/566-constraint-contention-tiebreak-implement-the-accept.md`: rank by **constraint-contention over `serialize-group`**, under the hand-set `[P1..P3]`, with `P-enum + age` as the floor; WSJF/RICE explicitly foreclosed ("WSJF alone = 732 new estimates"). **This is backlog ranking, not catalog ranking** — the two are different problems and the repo should not let one stand in for the other.

**What is missing, precisely.**
1. **Nothing measures organ usage.** The index answers "what exists and what fires it". No surface answers "what has actually fired, how often, and did it help". Every mechanism in Pattern 5B is unbuilt here, and one of them (`claude_code.tool_result` with `skill_name`) is a config change rather than a build.
2. **Nothing measures per-entry value.** No `evals/` directory exists under `.claude/skills/`; the `verify` and `check-against-spec` skills have no with/without benchmark. So an entry's worth is asserted at authoring and never re-tested — which is also why the R1–R4 ranking could go dormant without anyone noticing a cost.
3. **The always-on instruction layer is at its ceiling and is not deferred.** CLAUDE.md §12 v2.68 records the file closing at **196/200 lines, headroom 4**, with 6 lines *bought* by condensing history into git. AGENTS.md measures 5,270 B; combined global+root payload 9,161 B = 28.0% of Codex's 32 KiB cap. This is the exact condition Pattern 5A addresses — and the skills doc states the fix in one sentence: "a skill's body loads only when it's used, so **long reference material costs almost nothing until you need it**", and "**a section of CLAUDE.md has grown into a procedure rather than a fact**" is its named trigger for extraction. CLAUDE.md §9's hook roster — with its multi-sentence honest limits per hook — is a procedure catalogue sitting in an always-on file whose budget is measured in single-digit lines.
4. **The catalog is past the documented degradation threshold.** Anthropic documents selection accuracy degrading "once you exceed 30–50 available tools". The generated organ index is above that band. The repo has never tested whether its own agents pick the right organ.

**Where the industry assumption does not hold.** Anthropic's 55k-token figure is about *MCP tool definitions in an API context window*, not about markdown governance organs, and no MCP server aggregation problem exists here. Do not import the token arithmetic. What imports cleanly is the **30–50 selection-accuracy band** and the **measure-before-retire loop** — both are about catalogs, not about protocols.

**Cheapest experiment — and this is my top recommendation on the whole survey.** Two weeks, no build:

- Set `OTEL_LOG_TOOL_DETAILS=1` and export Claude Code OTel events to a local file exporter for the operator's own sessions. Collect `claude_code.tool_result` and `claude_code.tool_decision` — `tool_name`, `skill_name`, `subagent_type`, `success`, `duration_ms`.
- After two weeks, join the counts against `ecosystem/organ-index.md` and publish one `docs/audits/<date>-technical-*` artifact: every organ, its invocation count, its success rate, and the zero-count list.
- Rule on the zero-count list under the **existing** R1–R4 ranking and the **auto-retirement prohibition** — nothing deletes itself; the operator rules each row, and the funnel is ADR-111's four outcomes.

If the zero-count list is short, the catalog is healthy and the finding is worth the two weeks. If it is long — and with 55 organs and a documented 30–50 accuracy band I expect it is — this single artifact revives a ruling that has been dormant since `[#487]` and gives it the evidence it lacked. **Tier S under ADR-112** (try it and keep or delete), and it births zero rows to run.

---

## 7. Patterns I looked for and did not find

Recorded so the next seat does not re-spend the search.

- **HYPOTHESIS — no source found: an agent system that retires its own catalog entries on measured disuse.** Everything I found measures (telemetry, evals, description hit-rate); nothing decides. This repo's `auto-retirement prohibition` (STANDING_RULINGS A4) may therefore be **ahead of the field rather than behind it** — it is a policy the industry has not yet needed to write down.
- **HYPOTHESIS — no source found: a durable, human-editable plan artifact that survives the run *and* is machine-validated against the run's outcome.** spec-kit persists and self-assesses (`/speckit.converge`); gh-aw validates at compile; neither closes the loop back from outcome to spec. This repo's `docs/audits/` frozen bundle + close packet + consumption ledger triad is closer to that loop than anything I could source.
- **Not found: any published operator-scale (n=1) autonomous SDLC practice.** Every source assumes a team. Treat all cost, concurrency and review-queue advice accordingly.

---

## 8. Recency, and what I would want re-verified

My knowledge cutoff is May 2026 and this area moves monthly. Specifically:

- **Everything from a `[BLOCKED]` domain.** The Anthropic multi-agent figures (+90.2%, 15×, 80% variance) and the Cognition single-writer argument are **search-snippet only**. Re-fetch `anthropic.com/engineering/multi-agent-research-system` and `cognition.com/blog/dont-build-multi-agents` from a session with open egress before either is quoted in a ruling.
- **The two confidence-weighting quotes in §5** have no verified identifier. Do not cite them; treat that paragraph as a pointer to a literature.
- **FrugalGPT's identifier** — named in snippets, not fetched. Verify before citing.
- **The 38% programmatic-tool-calling figure** — snippet only.
- **gh-aw's status.** Technical preview as reported; preview APIs move. Re-check `gh aw compile` and the safe-outputs contract before designing against it.
- **Tool search's model list and the `20251119` tool versions** are fetched and current as of today, but the "30–50 tools" accuracy claim is a vendor statement without a published benchmark attached — treat as a design heuristic, not a measurement.
- **What I would most want re-run in-repo, not re-verified externally:** ADR-87's STEP 1 by-class self-load finding. It is eleven times restated and, as far as the tree shows, once measured with no recorded n.

---

## 9. Sources

Fetched in this session:

- [Claude Code — Subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code — Skills](https://code.claude.com/docs/en/skills)
- [Claude Code — Monitoring usage (OpenTelemetry)](https://code.claude.com/docs/en/monitoring-usage)
- [Claude Platform — Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- [github/spec-kit](https://github.com/github/spec-kit)
- [githubnext/gh-aw — GitHub Agentic Workflows](https://github.com/githubnext/gh-aw)
- [lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)

Search results only (page not fetched — blocked or not opened):

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) `[BLOCKED]`
- [Cognition — Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) `[BLOCKED]`
- [RouteLLM: Learning to Route LLMs with Preference Data (arXiv 2406.18665)](https://arxiv.org/abs/2406.18665) `[BLOCKED]` · [LMSYS blog](https://www.lmsys.org/blog/2024-07-01-routellm/)
- [When and Why Does Multi-Agent Debate Fail and Does It Really Underperform? (arXiv 2510.20963)](https://arxiv.org/abs/2510.20963) `[BLOCKED]`
- [Stop Overvaluing Multi-Agent Debate (arXiv 2502.08788)](https://arxiv.org/abs/2502.08788) `[BLOCKED]`
- [Single-Agent LLMs Outperform Multi-Agent Systems Under Equal Thinking Token Budgets (arXiv 2604.02460)](https://arxiv.org/pdf/2604.02460) `[BLOCKED]`
- [Mixture-of-Agents Enhances LLM Capabilities (arXiv 2406.04692)](https://arxiv.org/abs/2406.04692) `[BLOCKED]` · [togethercomputer/MoA](https://github.com/togethercomputer/moa)
- [How Many Instructions Can LLMs Follow at Once? — IFScale (arXiv 2507.11538)](https://arxiv.org/pdf/2507.11538) `[BLOCKED]`
- [GitHub Next — Continuous AI](https://githubnext.com/projects/continuous-ai/) `[BLOCKED]` · [Automate repository tasks with GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) `[BLOCKED]`
- [Sunset notice: Copilot knowledge bases](https://github.blog/changelog/2025-08-20-sunset-notice-copilot-knowledge-bases/) `[BLOCKED]` · [Copilot Extensions deprecation](https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/) `[BLOCKED]`
- [GPT-5 (Wikipedia)](https://en.wikipedia.org/wiki/GPT-5) · [ChatGPT Auto/Fast/Thinking toggles — the-decoder](https://the-decoder.com/chatgpt-users-can-now-toggle-auto-fast-and-thinking-modes-for-more-control-over-gpt-5/) · [Why GPT-5's model router was controversial — AIC](https://aicommission.org/2025/08/why-gpt-5s-most-controversial-feature-the-model-router-might-also-be-the-future-of-ai/)

Repo locators cited (all opened):

`protocols/PLAYBOOK.md` — dispatch table `:2520`, Q1–Q4 `:2544`, the local-only ruling `:2532`, night-batch phases 3–5 `:2284`–`:2346`, four standing constraints `:2348`, batch protocol `:1846`, V-2 budget `:1880`, two-seam budget `:2008`, routing matrix `:2946`, context-load amendment `:2962`, ADR-87 collision `:3003`, §2 prompt conventions `:3886`, How to choose Model `:3924` · `protocols/STANDING_RULINGS.md` — decision budget `:26`, A4 retirement ranking `:92` · `docs/decisions/ADR-87-equilibrium-contract.md` (whole, incl. amendment `:112`) · `docs/intake/2026-08-24-tech-substrate-router.md` (#45) · `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md` (#35) · `docs/audits/2026-08-28-technical-night-batch2-frozen-bundle.md` · `docs/audits/2026-08-27-…-consumption-ledger.md` and `…2026-08-29-…` · `docs/audits/2026-08-08-technical-successor-prep.md:76` · `ecosystem/routing-table.yaml` · `ecosystem/organ-index.md` · `scripts/gen_lane_contract.py` (module docstring) · `tasks/271-nightly-proposal-loop.md` · `tasks/488-…md`, `tasks/566-…md` · `BACKLOG.md:52` (`[#185]` open) · `CLAUDE.md` §4, §9, §12 v2.68.

**END OF ARTIFACT — AUT-R1. Zero rows birthed. Nothing committed, nothing pushed. No gate was run and none is reported.**