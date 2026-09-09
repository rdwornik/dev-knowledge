# MATRIX — AJ M01–M03 + Maister + repo B, against our harness

**Phase 2 of the 2026-09-09 night mission.** Built by the session (Opus 5) from the Phase 1
reader tables, the R2 verification, and two support extractions of our own prior conclusions.

**Cell rule, enforced:** a cell is filled only from a **verified locator**. Where the only
available locator is UNVERIFIED, the cell says so. Where the source document does not exist in
this repository, the cell says **NO IN-REPO SOURCE** rather than restating the claim as though it
were checkable.

**What this matrix could not be built from — stated first, because three of its ordered inputs
are missing and a reader who does not know that will over-read every table below:**

| ORDERED INPUT | STATUS | CONSEQUENCE FOR THIS MATRIX |
|---|---|---|
| leg 1d — grok's independent census | **UNFULFILLED (R1, quota)** | The census-diff rows are built from an **in-repo** re-measurement instead. That is our own artifact, not a substitute reader, and is labelled as such everywhere it appears. |
| leg 1e — cursor-agent's "test that cannot fail" scan | **UNFULFILLED (R1, quota + our own hook)** | The DELETE LIST carries **no cannot-fail-test rows**. It says so instead of guessing. |
| DECLARE-HARNESS-IS-PROCESS §5, DECLARE-CONDUCTOR-DECISION (E + AMEND-001), the five DEAD PLAYBOOK sections, the 16-stage delivery-loop map | **NO IN-REPO SOURCE** | Four of R4's five attack targets **cannot be read from this repository at all.** See §0. |

---

## §0 — The finding that reorganises the mission

R4 named five of our prior conclusions as targets. **Four of them have no source document in this
git repository.** They are cited, never landed.

| R4 TARGET | IN-REPO STATUS | EVIDENCE |
|---|---|---|
| "Maister offers nothing beyond a spine" (DECLARE-HARNESS-IS-PROCESS §5) | **source absent.** `Glob **/DECLARE-HARNESS-IS-PROCESS*` → zero matches. Three files cite it by its transport path `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`, always as external and unlanded | `docs/audits/2026-09-08-technical-process-trigger-census.md:4` ("Commissioned by: `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md` §4"); `…lane-v-642-assembly-debt-rows.md:151`; `…lane-v-643-enforcement-debt.md:95` |
| the conductor decision E + AMEND-001 | **source absent.** No file names options A–D, states why E was chosen, or reproduces AMEND-001. The only description of E anywhere in the tree is the mission prompt's own clause | `MISSION-PROMPT.md:79` — "what E (Actions as runner, Free plan, no required checks) cannot do" |
| the five DEAD PLAYBOOK sections | **source absent, and the five are unnamed.** No document names which five. `protocols/PLAYBOOK.md` marks no section dead; the one "dead" hit at `:1835` is the unrelated phrase "a fresh committing worktree is dead on arrival" | grep over the tree |
| the 16-stage delivery-loop map | **source absent as an enumeration.** `docs/audits/2026-09-09-technical-lane-v-664-delivery-spine.md` is **not** the loop map — it contains no numbered 16-stage list and never says "stage 10/12/15". The fullest in-repo description is one ratio | `docs/intake/2026-09-09-tech-recovery-plan.md:24` — "8 of 16 loop stages mechanical". Stage 10 is named only at `tasks/670-step-g-floor-v1-5-0-reaches-corp-monorepo-and-th.md:13` |
| the census's 32 orphans | **source present** — and **already contradicted in-repo by our own later lane** | see §0.1 |

**Why this is the mission's most important output rather than a procedural complaint.**

The mission asked what our *spine* lacks. This is the answer, and it arrived before any reader
opened Maister: **our decisions do not have a state carrier.** A conclusion that governs work —
"Maister offers nothing beyond a spine", "the conductor decision is E" — lives in a Google-Drive
transport directory, is cited by committed audits as authority, and **cannot be read by anyone
working in the repository.** The census at `:4` cites `to-cc/…§4` as its commission. A reader of
that census cannot check what commissioned it.

Maister's answer to exactly this is `orchestrator-state.yml`. Ours is a filename in a citation.

**This is not the same defect as "we lack a runner."** It is upstream of it. A conductor that
executes phases still needs to know what was decided, and four of five decisions this mission was
told to attack are unreadable from the tree the conductor would run in.

### §0.1 — the census's 32 is already wrong, by our own hand

`docs/audits/2026-09-08-technical-process-trigger-census.md:11-16` records:

```
population                216 rows
  TRIGGERED               160
  ON-DEMAND-BY-OPERATOR    24
  ORPHAN                   32
```

**One day later, lane v-664 re-measured the same class and got 39** —
`docs/audits/2026-09-09-technical-lane-v-664-delivery-spine.md:230-243`, which records a
prediction of 26 against a measured 39.

So the "32 orphans" figure is **superseded in-repo before this mission began**, and nothing
reconciled the two. Leg 1d was ordered precisely to arbitrate this and could not run. The honest
state is: **two of our own measurements of the same population disagree (32 vs 39), the
disagreement is one day old, and no third measurement exists.** The DELETE LIST below therefore
refuses to delete anything on the strength of the 32.

The census also documents its own false-orphan risk, which matters for any deletion built on it:
- it admits two earlier passes were wrong — a docstring-regex pass produced 133/139 false
  "triggered", and a bare-filename AST pass collided 7 module names (`:55-62`);
- "Reachability is static… proves wiring, not execution" (`:438-445`);
- **function granularity is out of scope** — a module can be TRIGGERED while a function inside it
  is orphaned, and that is not counted.

---

## §1 — THE MATRIX

Legend: **MECH** = implemented mechanically (organ + trigger named) · **PROSE** = implemented in
prose only (doc line named) · **MISSING** · **REJECTED** (ruling cited).
`†` = the supporting locator is UNVERIFIED (reader-reported, not re-checked). `‡` = verified by
this session first-hand.

### 1a — M01 / M02 practices (from intake #20, our own prior extraction)

| PRACTICE | SOURCE | VERDICT | EVIDENCE |
|---|---|---|---|
| Judge a dependency partly on AI-friendliness (does it ship skills/an MCP server an agent can consume) | M01 | **MISSING** | our own verdict: "No. ADR-106 declares dependencies and ADR-112 sets a two-tier adoption bar, but neither asks whether a dependency is legible to an agent" — `docs/audits/2026-09-05-technical-research-aj-second-pass.md:59` |
| Measure the token/cost effect of an optimisation on your own usage, not a published benchmark | M01 | **PROSE / partial** | "ADR-112's Tier S is exactly 'try it and keep or delete it', and `logs/TOKEN-LOG.md` is a weekly aggregate — but we have no per-tool before/after" — `…aj-second-pass.md:60` |
| Weigh popularity, complexity and cross-release stability together when picking a framework | M01 | **MISSING** | "No. No such criterion is recorded anywhere in `docs/decisions/`" — `…aj-second-pass.md:61` |
| Seed a greenfield project's standards from a mature sibling | M01 | **MECH** | `deploy/carrier_floor.py` + `deploy/manifest-v*.yaml`; `.claude/CLAUDE-FLOOR.md` is the hash-guarded replica — `…aj-second-pass.md:62` |
| Run the agent from a directory already holding sibling implementations | M02 | **MISSING** | "Our lane worktrees are provisioned per-lane at `.claude/worktrees/<name>`; nothing positions a lane beside comparable prior work deliberately" — `…aj-second-pass.md:64` |
| Split the fast in-loop check from the slower CI pass deliberately | M01 | **MECH** | targeted tests per lane, full suite once at integration — `CLAUDE.md:65`; pre-commit carries the fast gates — `…aj-second-pass.md:65` |
| Keep the human accountable for architecture even when it is reached through dialogue | M01 | **MECH** | ADR-108 §A splits it: operator rules functional questions, architect technical ones — `docs/decisions/ADR-108-*.md:40` |
| Commit orchestration and decision artifacts so a later reader can reconstruct why and by whom | M01 | **MECH — but see §0** | `docs/handoffs/*/`, `docs/audits/`, append-only `JOURNAL.md` — `…aj-second-pass.md:67`. **The practice is implemented for lane work and violated for architect decisions:** four of five R4 targets are exactly the artifacts this row claims we commit. |
| Per-loop model-call trace inspection | M01L02 | **REJECTED** | "REJECT (as framed) — the model-call half is real but is not what either side ships; Maister does not have it either" — `…aj-second-pass.md:26`. **This rejection is now questionable: repo B ships it** (§1c). |
| "Harnessability" as a named quality attribute | M01L01 | **REJECTED** | "REJECT as vocabulary, ADOPT as question" — `…aj-second-pass.md:32` |
| SlopCodeBench-class modifiability benchmark | M01L05 | **REJECTED** | "REJECT for now — neither side has run a modifiability benchmark. Ours is a design; theirs is a citation" — `…aj-second-pass.md:39` |
| ADE / multiplayer; plugin-microkernel architecture; generated ADRs | M01L06 | **REJECTED** | "single-operator system by design… we are not a product… their cheapness is the opposite of what ADR-94 protects" — `…gap-analysis.md:276-278` |

**Correction that must travel with any citation of the M01/M02 comparison.** The
2026-09-06 erratum voids a specific claim of the second-pass audit: the audit reported
`FR2-legM-01-init.json` as absent ("its wrapper was OOM-killed, so no JSON was written… No dollar
figure is estimated"); the file **exists** and carries `total_cost_usd: 21.8585621` —
`docs/audits/2026-09-06-technical-erratum-aj-second-pass.md:45-48`. The init figure was low by
**3.76×**. The headline ratio is "correct as scoped… incomplete" (`:55-57`), and its honest status
is "verified by a seat with disk access — and **unreproducible from the repository**" (`:160-162`).

### 1b — M03 practices (leg 1a, agy; all locators UNVERIFIED †)

| PRACTICE | M03 LOCATOR † | VERDICT | EVIDENCE |
|---|---|---|---|
| **Logical model aliases** — apps name `prod-model`, a config maps it to a physical model, so provider swaps need no code change | L02.md:37 | **MISSING** | This is the direct answer to the mission's MODEL-AGNOSTIC question. We have the opposite: `MODEL_ENUM = ("opus","sonnet","haiku")` enforced at three call sites — `scripts/gen_lane_contract.py:129`, `:332-335`, `:833-835` † |
| Unified API contract at the boundary so app code is provider-independent | L02.md:37 | **MISSING** | our dispatch layer emits the literal binary `claude` — `scripts/gen_lane_contract.py:525` † |
| **Model switching by YAML edit, zero code refactoring** (BAML + gateway) | L03.md:67 | **MISSING** | see MODEL-AGNOSTIC §4 |
| Insulate the system from bi-weekly model/API churn behind an abstraction layer | L04.md:43 | **MISSING** | nothing sits between our process and a vendor CLI |
| Automated provider fallback on outage | L02.md:13 | **PROSE, and only for one role** | `~/.claude/ROUTING.md:48-79` — the REVIEWER fallback chain (terra → grok → … → Codex) is real and cost-ascending. **It is the only role that has one.** Tonight two readers hit quota and no chain existed for them. |
| Route by prompt complexity / cost / latency | L02.md:23, L06.md:29 | **PROSE** | model+effort stated by a human at dispatch — `protocols/PLAYBOOK.md:3566-3576` † |
| **Hard assertions that fail the run (`@@assert`) vs soft ones that report without blocking (`@@check`)** | L03.md:55 | **MECH — we already have this** | our `[!!]` FAIL-blocks vs `[~~]` WARN-informs split in `audit.py`, witnessed live tonight when the anchor check blocked this bundle's own first commit ‡ |
| Single schema file as source of truth, regenerating all downstream clients | L03.md:59 | **MECH** | our generator/derived-copy discipline — `derived-copies-rebind` pre-commit hook, `gen_claude_rosters.py --write`, the `@`-imported `.claude/generated/` fragments ‡ |
| Prompts as typed functions with named inputs and typed outputs | L03.md:25 | **MISSING** | our prompts are markdown |
| Prompt unit tests colocated with the prompt | L03.md:23, :55 | **MISSING** | no prompt has a test |
| Pre-deployment **evals** as unit tests for prompts (Ragas/DeepEval/Promptfoo) | L02.md:41 | **MISSING** | `[#661]` — "SDA-1 is a complete benchmark design that has never been run" ‡ |
| Runtime **guardrails** as synchronous middleware on the live path | L02.md:45 | **MECH, by accident and mis-aimed** | our `PreToolUse` guard IS runtime middleware — and it is the thing that wedged cursor-agent (MA-1) ‡ |
| Post-production **observability** feeding defect traces back into the eval suite | L02.md:47 | **MISSING — this is the self-improvement loop** | see §3 |
| **Three-pillar governance: evals → guardrails → observability** | L02.md:39-47 | **1 of 3** | we have guardrails; no evals, no observability consumed by anything |
| Measure LLM load in tokens-per-minute, not requests-per-minute | L02.md:19, L04.md:35 | **MISSING** | `logs/TOKEN-LOG.md` is a weekly aggregate — `…aj-second-pass.md:60` |
| Attribute token spend per team/model | L02.md:25 | **MISSING** | `scripts/cost_usage_telemetry.py` is "Library only; no call sites" — `…gap-analysis.md:28` |
| Hard budget caps over rolling windows | L02.md:63 | **MISSING** | tonight's two quota refusals were discovered by hitting them |
| **Monitor reviewer approval-rate and review-duration to detect rubber-stamping** | L05.md:31 | **MISSING — and it is the sharpest row in this table** | see §3.2 |
| **Inject synthetic flawed items into the review queue to test reviewer diligence** | L05.md:31 | **MISSING** | we have no mechanism that tests whether a gate or a reviewer actually bites |
| Confidence-tiered routing: autonomous / review / expert | L05.md:29, :55 | **PROSE** | ADR-108 §A splits question *kinds*, not confidence |
| Sync vs async approval chosen by irreversibility and blast radius | L05.md:37-39 | **PROSE** | our destructive-act rule is a flat "ask", not a tiering |
| Deterministic Policy-as-Code risk classification at intake | L05.md:17 | **PARTIAL MECH** | ADR-98 intake + `validate_backlog` are schema gates, not risk classifiers |
| Logging by design across the whole lifecycle | L05.md:19 | **PARTIAL** | governance telemetry exists (`duration_ms` per check); model-call telemetry does not — `…aj-second-pass.md:26-27` |
| Dual-track logging (long-term anonymised audit vs short-lived personal data) | L05.md:21-23 | **N/A** | no personal data in scope |
| Anti-automation-bias mechanisms in human review | L05.md:27 | **MISSING** | |

### 1c — Maister (leg 1c, codex; **R2-VERIFIED**) and repo B (leg 1b + this session ‡)

| MECHANISM | LOCATOR | THEIRS | OURS |
|---|---|---|---|
| 14-phase development workflow | `plugins/maister/skills/development/SKILL.md`, phases at :128 → :538 — **all 14 CONFIRMED** | prose in one SKILL.md | 8-phase spine, `protocols/PLAYBOOK.md:6064-6071` — **all 8 CONFIRMED** |
| Per-task state carrier | `.maister/tasks/development/<task>/orchestrator-state.yml` | **described in prose; never mechanically written.** 33 mentions, all `.md`, plus one 21-line shell hook that only emits a reminder string. **Zero `.py`/`.js`/`.ts` in the tree** | our `tasks/*.md` frontmatter: `id, title, status, priority, size, theme, story, serialize-group, depends-on, generates` — **no execution position, no phase results** |
| …but **in practice** (repo B) | `.maister/tasks/development/*/orchestrator-state.yml` — **10 committed instances, verified first-hand ‡** | `completed_phases: [phase-1, phase-2, phase-5, phase-6, phase-7, phase-8, phase-10, phase-11, phase-12, phase-14]`, `failed_phases: []`, `auto_fix_attempts: {}`, `options.{spec_audit_enabled, skip_test_suite, e2e_enabled, …}`, `task_context.{risk_level, architecture_decision}` ‡ | **nothing equivalent exists** |
| Conditional phase routing from task characteristics | SKILL.md:193 (`has_reproducible_defect`), :212 (`ui_heavy`), :496 (`e2e_enabled`), :516 (`user_docs_enabled`) — CONFIRMED | a task's shape selects which phases run | our lanes are hand-composed per batch |
| Explicit verification-option selection as a phase | SKILL.md:395 — CONFIRMED | the operator picks the verification suite and the choice is recorded in state | our gate set is fixed |
| A GO/NO-GO artifact | `.maister/tasks/…/verification/reality-check.md:5-9` † — "**Status**: NOT READY -- Critical gap in Success Criterion #1 / **Deployment Decision: NO-GO**" | a written, committed verdict | our operator GO is spoken and leaves no artifact — `PLAYBOOK.md:6068` is a spine row with no carrier |
| Append-only per-task work log | `.maister/tasks/…/implementation/work-log.md:3-6` † | per-task, step-level | ours is repo-level (`JOURNAL.md`) |
| CI | none — "No CI workflows present" † | **absent** | ours is the pre-commit/commit-msg/pre-push gate set ‡ |
| Repo-level agent hooks | none in `.claude/hooks` † | **absent** | ours: 22 pre-commit + session hooks ‡ |
| LLM gateway with guardrails + observability | `litellm/config.yaml:12-24` † — Presidio PII guardrails (`CREDIT_CARD: BLOCK`), Langfuse callbacks | **the M03 lessons, running** | **absent** |

---

## §2 — SPINE

**What Maister's state carrier does that our `tasks/` + FPG-1 + the planned conductor do not.**

1. **It records execution position.** `started_phase`, `completed_phases`, `failed_phases`. Our
   `tasks/*.md` frontmatter carries `status: open|closed` and nothing between. A lane that died at
   its fourth of seven clauses is, in our carrier, indistinguishable from one that never started —
   which is the recorded gotcha *"a gate-blocked lane looks identical to a finished one."* Maister
   would have written `failed_phases`.
2. **It records what was deliberately skipped, and why it was skippable.**
   `options.skip_test_suite: true` sits beside `completed_phases` that omit phase-3 and phase-9
   (TDD red/green) ‡. Ours has no way to say "this gate was consciously not run for this task" —
   so we either run everything or leave no trace of the decision.
3. **It records attempts, not just outcomes.** `auto_fix_attempts: {}`. We record a closure; we do
   not record that it took three tries. Every retry this mission made — three `agy` re-runs, two
   `codex`, three `cursor-agent` — would be invisible in our carrier.
4. **It carries per-task risk and architecture decisions inline.** `task_context.risk_level: low`,
   `architecture_decision: "Spring DI-based microkernel (ADR-003)"` ‡. Ours are in ADRs, one
   directory away, linked by prose.
5. **It is one file per task, machine-readable, resumable.** The `post-compact-reminder.sh` hook
   exists precisely so a context-compacted agent can recover position by reading it. Our
   equivalent recovery instruction is "read the last 5 JOURNAL entries and the active handoff
   bundle" — a *human-ordered* recovery over prose.

**And what ours does that theirs does not, which is not a small thing.**

Maister's spine is **unenforced by construction**: no executable code, no CI, no hooks. Every
phase gate is an instruction to a model. A model that skips a phase and writes
`completed_phases: [...]` anyway produces a state file indistinguishable from an honest one.

Ours is **executable refusal**. This bundle's own first commit was blocked tonight by
`journal_spine_anchor` and could not land until the tree was synced ‡. That is a guarantee a
prose phase list cannot make.

> **The R4 verdict, stated plainly:** *"Maister offers nothing beyond a spine"* is **false about
> content and true about enforcement.** It carries conditional phase routing, verification-option
> selection, UI-mockup machinery with a reviewable gallery, and per-phase risk decisions — and it
> enforces none of them. We carry far less shape and mechanically enforce what we carry.
>
> The synthesis is not "adopt Maister". It is: **our enforcement is good and our state shape is
> impoverished, and those are independent axes.** A richer `tasks/` frontmatter — `phase`,
> `attempts`, `skipped_gates`, `risk` — would cost us nothing in enforcement and is the single
> highest-value change this mission found in the spine.

**What conductor decision E cannot do.** E is described in-repo only as "Actions as runner, Free
plan, no required checks" (`MISSION-PROMPT.md:79`) — **no ratified source exists** (§0). On that
fragment alone, and stated as conditional because the source cannot be read:

- **No required checks means no refusal.** A runner that cannot block a merge is a reporter. Our
  entire enforcement advantage over Maister is that our gates refuse; moving the loop to a runner
  that cannot refuse trades the one thing we are ahead on.
- **Free-plan compute is exactly what failed tonight.** Two of five ordered readers died on
  free-tier quota, mid-mission, with no fallback. A nightly loop on free-tier Actions inherits
  that failure mode, and inherits it unattended.
- **A runner does not fix §0.** Actions can execute phases; it cannot make an unlanded decision
  readable.

---

## §3 — SELF-IMPROVEMENT LOOP

### 3.1 Telemetry consumed by which process: **none**

Confirmed against our own prior measurements, not asserted:

- `scripts/cost_usage_telemetry.py` — "**Library only; no call sites**"
  (`docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md:28`). It is also one
  of the census's 32 orphans, whose only call site is *a lane contract*
  (`…process-trigger-census.md:86-105`).
- Governance telemetry **does** run: `DEV_KNOWLEDGE_TELEMETRY=1 audit.py health` wrote 42
  `check_run` events with per-check `duration_ms` (`…aj-second-pass.md:26`). **Nothing reads
  them.**
- Our own trend surface says so in its own words: "gate time per runner invocation ABSENT",
  "suite wall-time ABSENT", "**per-model change quality ABSENT**" (`…aj-second-pass.md:27`).

So: we emit governance telemetry, emit no model telemetry, and **consume neither**. The loop is
open at both ends.

### 3.2 Which M01–M03 practice closes stage 12 (eval) and stage 15 (nightly)

**Caveat that governs this whole subsection:** the 16-stage map has **no in-repo enumeration**
(§0). "Stage 12 = eval" and "stage 15 = nightly" are taken from the mission prompt's own gloss.
The practices below are matched to those *descriptions*, and must be re-matched against the real
map when it lands.

**Stage 12 (eval) is closed by the M03 three-pillar stack — specifically its third pillar.**

> "Production observability functions as a post-production review mechanism, surfacing real costs,
> hallucination rates, and model errors **to feed back into development and eval suites**" —
> L02.md:47 †

The mechanism M03 teaches is not "write evals". It is **the return path**: a production trace that
fails becomes an eval case. We have neither end — no eval suite (`[#661]`: SDA-1 designed, never
run) and no trace to feed it. **The cheapest first move is the return path with a trivial suite,
not a large suite with no return path** — because the return path is what makes the suite grow
without anyone deciding to grow it.

L03's `@@assert` / `@@check` split (L03.md:55 †) is the shape our own `[!!]`/`[~~]` audit split
already has ‡. So the eval *grammar* is not new to us; only its subject is. We assert over
governance state and never over a model's output.

**Stage 15 (nightly) is closed by L05's reviewer-diligence practices — and this is the finding
that most directly indicts our current loop.**

> "Avoid the 'rubber-stamping' anti-pattern where reviewers unthinkingly approve AI outputs in
> split seconds **by monitoring approval rates and review durations**" — L05.md:31 †
> "**Inject synthetic, flawed blind tests** into human reviewer queues to catch reviewers who
> exhibit abnormally fast review times or excessive approval rates" — L05.md:31 †

Our loop's terminal gate is a human GO (`PLAYBOOK.md:6068`, CONFIRMED). We have **no measurement of
that gate at all** — not how long a review took, not how often GO is given, not whether any GO was
ever withheld. A nightly process that measured approval rate and review duration would be
consuming telemetry we could start emitting immediately, and it is the one telemetry consumer that
improves the *process* rather than the code.

The synthetic-flawed-item practice is stronger still, and it is the direct answer to the leg-1e
question this mission could not run: **a gate that has never refused anything is
indistinguishable from a gate that cannot refuse.** Injecting a known-bad item is how you find
out. That applies to our reviewer *and* to our 22 pre-commit hooks — several of which, on
tonight's evidence, have never been observed to fire.

---

## §4 — MODEL-AGNOSTIC

**The minimum change set for "swap the architect model" to be one config line** is in
`docs/audits/2026-09-10-technical-night-aj-m03/1f-model-agnosticism.md`, items 0–9, each with a
locator. It is not restated here. Three things belong in the matrix instead.

**First: M03 names the mechanism we lack, and it is one mechanism, not nine fixes.**

> "Logical model aliases (e.g. `prod-model`) decouple application code from physical models,
> allowing provider swaps and model upgrades via gateway configuration changes without code
> refactoring" — L02.md:37 †
> "Pairing BAML with LiteLLM enables model switching via YAML configuration without application
> refactoring" — L03.md:67 †

Our nine-item change set exists **because we have no alias layer.** Every item is a place a
physical model name or a vendor binary leaked into a surface that should have named a role. The
registry already knows this and says so in its own docstring: *"A swap still edits N files; what
changes is that it can no longer edit N-1 of them and ship"* — `scripts/check_provider_registry.py:13-16` †.
The registry is a **drift detector, not an indirection layer**, and it is honest about it.

**Second: we already have a working alias layer — for exactly one role.**

`~/.claude/ROUTING.md:48-79` † binds the REVIEWER role to a cost-ascending fallback chain with
degraded-artifact tagging and served-model-id recording. `ecosystem/routing-table.yaml:31-38` †
declares `fan_out` as a *list* of CLIs. **The reviewer role is the working prototype of what the
architect role needs**, which makes this a generalisation problem, not a design problem.

**Third — MA-1, the finding this mission measured rather than read.**

`.claude/settings.json:21` declares a `PreToolUse` hook with matcher `"*"` whose command is
`python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`. `cursor-agent` **honours
the hook and does not define the variable.** It expands empty, the path becomes
`C:\scripts\fleet_health.py`, the interpreter fails, and matcher `"*"` converts that into refusal
of every tool call with no in-session escape. Two full `cursor-agent` runs were spent proving it ‡.

Every row in the 1f table describes capability a swap would **lose**. MA-1 describes our own
configuration becoming **actively hostile** to the new reader — and presenting as the reader being
broken. `codex` escaped only because it does not read `.claude/settings.json`. That is luck.

**Model-agnosticism is not only about which model answers. It is about whether our harness lets a
different one work at all — and nothing in the repo tests that, because nothing in the repo has
ever run a non-Claude CLI against itself.**

---

## §5 — DELETE LIST

**One line each, evidence, verb ∈ {delete, wire}. No third verb.**

**Three of the five ordered inputs to this list are unavailable** (§0), so the list is short and
says why rather than padding itself:

- census 32 orphans → **available but superseded** (32 vs v-664's 39; §0.1)
- the 1d diff → **UNFULFILLED** (grok quota)
- the 1e cannot-fail tests → **UNFULFILLED** (cursor quota + our own hook)
- the five DEAD PLAYBOOK sections → **NO IN-REPO SOURCE**; the five are unnamed anywhere
- what M03/Maister makes redundant → available, below

### 5.1 — What the evidence supports acting on

| ITEM | VERB | EVIDENCE |
|---|---|---|
| `scripts/cost_usage_telemetry.py` | **wire** | census orphan #5; its only call site is a lane contract (`…census.md:86-105`); "Library only; no call sites" (`…gap-analysis.md:28`). It is the exact organ §3 needs to close the loop. Deleting it would delete the one thing that already exists for stage 12. |
| `scripts/gen_trend_dashboard.py` | **wire** | census orphan #12, call site is a lane contract. Our trend surface's own "ABSENT" rows (`…aj-second-pass.md:27`) are what it would fill. |
| `scripts/window_metrics.py` + `scripts/failed_set.py` | **wire** | orphans #20 and #9; `failed_set` is called only by the untriggered `window_metrics` (`scripts/window_metrics.py:359`). A two-module orphan pair that computes exactly the review-cadence numbers §3.2 wants. |
| `~/.claude/hooks/block-onedrive.SUPERSEDED*.ps1` ×3 | **delete** | census orphans #21–23, "SUPERSEDED copy — retired, still on disk", zero references (`…census.md:123-125`). **The only unambiguous deletions in the whole census** — retired copies of a live guard, and a stale copy of a safety hook is worse than none. |
| `/override` | **delete** | `.claude/commands/override.md:1` — its own frontmatter says "RETIRED (ADR-85 amendment 2026-08-03 §A2) — discharges no gate". A command that announces it does nothing. |
| `scripts/setup-fleet-scheduler.ps1` | **delete** | census orphan #17 — **NONE, zero references** (`…census.md:86-105`). The only census orphan with no caller of any kind, not even a lane contract or a test. |
| The `MODEL_ENUM` literal at `scripts/gen_lane_contract.py:129` and its three enforcement sites (`:332`, `:833`, `:949`) | **wire** | 1f items 1–2 † — repoint at one config source. This is the alias layer §4 says we lack, at its cheapest point. |
| `.claude/settings.json:21` `PreToolUse` matcher `"*"` | **wire** | MA-1 ‡ — make it resolve its own path, or fail **open** when its interpreter is missing. Currently it converts a missing file into total refusal, for any reader that is not Claude Code. |

### 5.2 — What this mission refuses to put on the list, and why

- **The other 26 census orphans.** The population is contested by our own later measurement (32 vs
  39, §0.1), the census documents two prior passes that were wrong (`:55-62`), and its method
  cannot see function-level orphaning (`:438-445`). Leg 1d existed to arbitrate and did not run.
  **Deleting on a contested census is how a real caller gets removed.**
- **Anything from the "five DEAD PLAYBOOK sections".** They are unnamed in every file in this tree.
  A delete list cannot carry a row it cannot locate.
- **Any cannot-fail test.** Leg 1e never produced one. The gap is real — §3.2 argues the
  synthetic-flawed-item practice is how to find them — but this mission has no evidence and will
  not manufacture it.
- **`/preflight`, `/save`, `/changelog-review`, `/codex-review`, and the three skills** (census
  orphans #24–32). They are operator-invoked by design; the census counts "not one of the seven
  sanctioned on-demand verbs" as ORPHAN, which is a **classification artifact, not a finding**.
  `/preflight`'s own frontmatter says "wired into no gate" — that is its design, and CLAUDE.md §4
  calls it "the most-recorded executor failure" prevention. Deleting it would be acting on a
  vocabulary choice.
- **`scripts/file_purpose_graph.py`** (orphan #10). Tagged in the census itself as ADR-118
  *Proposed, NOT ratified* (`…census.md:109`), and lane v-664 has since wired FPG-1 behind three
  commit-tier hooks — two of which refused this bundle's own commit tonight ‡. **It is not an
  orphan any more.** Live proof that the census's 32 has decayed.

---

## Rows this file is evidence for

- **[#582]** — *substrate router: one gated enum, a capability-keyed table, and the generator that reads it.* §4 is the measured case for that router, and names the one mechanism (logical model aliases) the router would be an instance of.
- **[#661]** — *SDA-1 is a complete benchmark design that has never been run.* §3 argues the return path matters more than the suite, which bears directly on how that row should be closed.
- **[#676]** — *no check verifies a provider CLI's non-interactive invocation shape.* Two of this mission's five ordered readers were lost to a failure mode that row's four-way split does not express.
