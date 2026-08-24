# Model-switching architecture — routing table vs adapter layer vs bus

**Date:** 2026-08-23 · **Lane:** RESEARCH-M9, cloud, read-only · **Branch:** `claude/research-model-bus`
**Base:** `main` @ `aeec0fd` (merge of `chore/phase0-preconditions-2026-08-23`)
**Providers in scope:** Grok 4.6 (xAI) · Gemini (Google) · DeepSeek · Codex/OpenAI
**Mode:** evidence, not verdict. The decision is the operator's. This lane names a fork; it does not rule it.
**Banked:** 0 — no `tasks/` row filed, no `BACKLOG.md` edit. §7 names the fork; filing is the operator's act.

---

## 0. The honest starting position

**The routing table is the incumbent, and it is already the ratified posture.** Three facts fix that,
and each is a locator rather than an impression:

1. **Routing is doctrine and its canonical table is out of this repo.** `protocols/PLAYBOOK.md:4747`
   — *"The model-routing table is canonical in `~/.claude/ROUTING.md`"*, with the resident copy
   deliberately killed (#158 Decision B) because a cached table silently drifts.
   `protocols/STANDING_RULINGS.md:1949` (ruling **R-2**, 2026-08-22) makes the placement a ruling:
   `~/.claude/ROUTING.md`, `~/.claude/bin/codex-review.ps1` and `~/.codex/config.toml` are **L0
   surfaces**, and *"their absence from this repository is a placement, not a gap."*
2. **The enforcement mesh is already provider-agnostic.**
   `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md:537` — the seam census, and the
   line that follows it: *"The load-bearing observation: the enforcement mesh is already
   provider-agnostic."*
3. **A provider/model registry already exists** — `ecosystem/provider-registry.yaml`, landed by
   CLOUD-4 v2, with a commit-time agreement gate (`provider-registry-agreement`, `CLAUDE.md:176`).

So **Option 1 is not hypothetical — it is partially built, and its real cost is incremental.**
The burden of proof sits on the challengers.

**And the same honesty cuts the other way, which the brief did not anticipate.** Option 2 is not
hypothetical either. A five-provider adapter layer over exactly this provider set **already exists and
already runs** — in the `ai-council` child repo, at Layer 3. `protocols/AI_COUNCIL_PROCESS.md:239–240`:

> *"Build providers from `PROVIDER_CLASSES` (anthropic, openai, gemini, xai, deepseek). Missing API
> key → provider skipped, not fatal unless all skipped."*

`protocols/AI_COUNCIL_PROCESS.md:169` records the default panel as `claude,gemini,openai,deepseek,grok`
— **all four named providers plus Anthropic, behind one call shape, shipping since at least
2026-05.** It also already carries a blocking health check, per-provider skip-on-missing-key, a
synthesizer routing rule and graded exit codes (`:241–275`) — i.e. several of the things Option 3
is proposed to buy.

The comparison this lane was asked to make therefore has a different shape than the brief assumed:
**one option is partially built here, one is fully built next door, and one has no in-repo referent
at all.** ("Magistrala" appears once in this corpus — `protocols/PLAYBOOK.md:3354` — as a worked
example of a hard debugging task in an unrelated domain. There is no prior bus design to inherit.)

---

## 1. Framing — where the burden of proof sits

A challenger to the routing table must show something the table **cannot do**, not that it would be
tidier. Three specific bars, each derived from a live constraint rather than invented for this lane:

- **The doctrine bar.** `CLAUDE.md:91`, critical rule 4: *"**Layer 2 never executes** — no
  orchestration scripts: no script drives state in a child repo (ADR-28, ADR-36). Hub-local
  validators, generators and gates are in scope."* A bus is an orchestration mechanism. Building one
  **in this repo** is not a design choice available to a lane — it requires superseding ADR-28/ADR-36.
  Building one in a child repo is available, and is a different question than the one asked.
- **The caller bar.** An adapter interface needs callers. §2 measures how many exist here.
- **The placement bar.** The thing a table-driven swap would edit — the routing table — is at L0 and
  outside this repo by ruling R-2. No architecture built inside this repo changes that unless the
  ruling is reversed (option (a) of R-2, *"bringing a copy in-repo behind a drift gate"*, remains
  available and is explicitly still on the table).

---

## 2. Current state, measured

Every number below names the command that produced it. Interpreter and gate state: §7.

### 2.1 What model-invocation machinery exists in this repo

```
python files under scripts/ + deploy/        122     find scripts deploy -name "*.py" | wc -l
model-API SDK imports (anthropic/openai/
  google/litellm/httpx/requests) in those      0     grep -rn "^import |^from " --include=*.py scripts deploy
                                                      | grep -Ei "anthropic|openai|httpx|requests|urllib|google\.|litellm"
                                                      (sole hit: urllib.parse in scripts/reverse_dep_oracle.py:56 — URL parsing)
subprocess.run/Popen/check_output sites       86     grep -rn "subprocess.run(|subprocess.Popen(|check_output(" --include=*.py scripts deploy | wc -l
of those, sites that GENERATE model output     1     deploy/lived_sandbox/spawn.py:190
```

`deploy/lived_sandbox/spawn.py:190` is the whole of it:

```
[CLAUDE_BIN, "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose"]
```

`scripts/changelog_sentinel.py` also shells out per provider, but to `--version` probes (seam S7),
not to a model. `.claude/workflows/conformance-hub.js:150–152` pins a model three times, but those
are arguments to the **harness's** `agent()` call — the harness makes the request, not this repo.

**The decision-relevant number is 1.** This repository contains exactly one place where code chooses
a model and gets tokens back. An adapter layer is an abstraction over call sites; a bus is
infrastructure between callers. Here there is one caller, and it is a test-fixture spawner.

### 2.2 What the registry covers today

```
providers: 3   models: 5   pinned_at rows: 5
  python3 -c "import yaml; d=yaml.safe_load(open('ecosystem/provider-registry.yaml')); ..."
```

Providers: `anthropic` (cli `claude`), `openai` (cli `codex`), `xai` (**`cli: null`** — present only
because a provenance string names it). Models: `claude-sonnet-5`, `claude-opus-4-8`, `gpt-5.6-terra`,
`gpt-5.6-sol`, `grok-l5`.

**Of the four providers this lane was asked to price, the live surface count is one.**

| Provider | Registry entry | Executable surface in this repo | Standing verdict |
|---|---|---|---|
| Codex / OpenAI | yes, `cli: codex` | version probe (S7); reviewer pin is at **L0** (S19) | live |
| Grok 4.6 / xAI | yes, `cli: null` | none — provenance attribution only (S30) | admission work open, `[#562]`, `[#578]` |
| Gemini | **absent** | none | `.gemini/settings.json` **not admitted** — `protocols/STANDING_RULINGS.md:1941` |
| DeepSeek | **absent** | none | no row, no mention outside `ai-council` history |

The Gemini verdict is a recorded one and this lane does not re-run it:
*"**Not admitted:** `.gemini/settings.json`. It would be a new top-level directory that
`validate_hermetization.py` Rule A refuses absent an ADR-101 §1 amendment, and ADR-53 records the
active toolset as Claude Code + Codex. **A third provider is a cost with no present consumer.**"*
(`protocols/STANDING_RULINGS.md:1941–1943`.)

### 2.3 Seams that change under each option

Baseline census, `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md:537–542`:

```
doctrine-change ....... 12 sites   (S1, S12, S15, S16, S18, S19, S20, S21, S22, S23, S28, + S17 partial)
code-change ........... 10 sites   (S2, S3, S4, S5, S13, S14, S24, S25, S27, + S6 for a 3rd provider)
table-edit ............  9 sites   (S6 retarget, S7, S8, S9, S10, S11, S17, S26, S29, S30)
already agnostic ......  3 classes (S31, S32, S33)
```

Of the 9 table-edit seams, **7 are now asserted** against the registry by
`scripts/check_provider_registry.py` (S8, S9, S10, S17, S26, S29, S30); S7 *derives* from the
registry at runtime; S11 was repointed at `scripts/canonical_docs.py` as a canonical-doc seam.
Source: the module docstring at `scripts/check_provider_registry.py:17–28` and `CLAUDE.md:176`.

**Seams touched to add a fifth provider under each option:**

| | Files changed to admit one new provider | Doctrine seams requiring a ruling | New code paths |
|---|---|---|---|
| **Option 1** (finish the table) | **1** — `ecosystem/provider-registry.yaml` (+ any `pinned_at` row that names a new model) | 0 to add an *identity*; the routing decision stays at L0 by R-2 | 0 |
| **Option 2** (adapter layer here) | **3 seams / 2 files** — S2, S3, S4 in `deploy/lived_sandbox/spawn.py` + `cli.py` | 0 *if* scoped to the sandbox; the routing decision still stays at L0 | 1 interface, 1 impl per provider, for **1 caller** |
| **Option 3** (bus here) | the same 2 files, plus new infrastructure with no existing home | **≥1 ADR superseding ADR-28/ADR-36** (`CLAUDE.md:91`) before a line is written | queueing, policy, observability, fallback, budget — none of which has a consumer in §2.1 |

A caveat this lane owes: the "1 file" for Option 1 is the cost of adding an *identity*. It is not the
cost of making a new provider **usable** — that is a CLI, a config surface, an admission A/B, and
the `[#562]`/`[#578]` shape of work. Option 1 is cheap because it is doing less, and saying otherwise
would be the dishonest comparison the brief warns about.

---

## 3. Library survey

**Retrieval note, recorded because it bounds the survey:** `docs.litellm.ai` and `docs.mozilla.ai`
are **blocked by this container's egress proxy** (`EGRESS_BLOCKED`). Coverage was therefore verified
from **package metadata and library source** — PyPI JSON and `raw.githubusercontent.com` — not from
vendor documentation. `api.github.com` is scoped to `rdwornik/dev-knowledge` in this session, so
directory listings for third-party repos were unavailable; where a provider list could not be read
from source, the PyPI `provides_extra` field was used and is named as such.

### 3.1 Maintenance and dependency signal — read directly

PyPI JSON API, `https://pypi.org/pypi/<name>/json`, fetched 2026-08-23:

| Package | Latest | Uploaded | Total releases | Releases since 2026-05-25 | `requires_python` | Direct deps (uncond.) |
|---|---|---|---|---|---|---|
| `litellm` | 1.98.0 | 2026-08-22 | 1081 | **117** | `>=3.10,<3.15` | 14 (incl. `boto3`, `tiktoken`, `tokenizers`, `aiohttp`) |
| `any-llm-sdk` | 1.26.0 | 2026-08-17 | 80 | 12 | `>=3.11` | 7 |
| `llm` (simonw) | 0.33 | 2026-08-22 | 69 | 7 | `>=3.10` | 14 |
| `pydantic-ai` | 2.33.0 | 2026-08-21 | 319 | 54 | `>=3.10` | 1 |
| `aisuite` | 0.1.14 | **2025-11-25** | 15 | **0** | `>=3.10,<4.0` | 2 |
| `langchain` | 1.3.16 | 2026-08-20 | 510 | 15 | `>=3.10,<4.0` | 3 |
| `portkey-ai` | 2.3.4 | 2026-07-23 | 108 | — | — | — |
| `@musistudio/claude-code-router` (npm) | 3.0.21 | 2026-08-14 | 89 versions | — | — | — |

Transitive closure, resolved with `uv pip compile --python-version 3.12 --universal` (uv 0.8.17 —
see §7):

```
current repo lock                                    34    grep -c "^name = " uv.lock
litellm                                              56
any-llm-sdk[anthropic,openai,gemini,deepseek,xai]    61
aisuite[anthropic,openai,google,deepseek]            57
llm                                                  32
llm + llm-gemini + llm-anthropic + llm-grok + llm-deepseek   47
pydantic-ai                                         103
```

Current declared surface for comparison: `dev` group **10** entries, `analytics` group **1**,
`project.dependencies` **None** (`python3 -c "import tomllib; ..."` over `pyproject.toml`).

### 3.2 Four-provider coverage

| Candidate | Grok/xAI | Gemini | DeepSeek | OpenAI | How verified |
|---|---|---|---|---|---|
| `litellm` | ✅ `XAI` | ✅ `GEMINI`, `VERTEX_AI` | ✅ `DEEPSEEK` | ✅ `OPENAI` | `LlmProviders` enum in `litellm/types/utils.py` — **152 members**, read from source |
| `any-llm-sdk` | ✅ `xai` | ✅ `gemini` | ✅ `deepseek` | ✅ `openai` | PyPI `provides_extra` — **54 extras** |
| `pydantic-ai` | ✅ `Xai` | ✅ `Google` | ✅ `DeepSeek` | ✅ `OpenAI` | `pydantic_ai_slim/pydantic_ai/providers/__init__.py`, read from source |
| `llm` (simonw) | ⚠️ plugin `llm-grok` 1.4.2 (2026-03-20) | ✅ plugin `llm-gemini` 0.33 (2026-08-13) | ⚠️ plugin `llm-deepseek` 0.1.6 (**2025-02-14**) | ✅ core | PyPI per plugin |
| `aisuite` | ❌ no `xai` extra | ✅ `google` | ✅ `deepseek` | ✅ `openai` | PyPI `provides_extra` — 16 extras |
| OpenRouter (hosted) | ✅ | ✅ | ✅ | ✅ | hosted gateway; no package required |

### 3.3 Verdicts — recorded so they stick

The repo's own precedent for a recorded dependency rejection is `tasks/433-...md`: *"scrummd
**REJECTED** as a dep (bus factor 1, 0.2.x-dev) — pattern reference only."* Same vocabulary here.

- **`litellm` (SDK) — REJECT for adoption into this repo's dependency set; ADOPT-scoped as a
  reference and, separately, as a pricing dataset.**
  Reason, and it is a measured collision with this repo's own ratified discipline, not taste:
  **117 releases in the 90 days to 2026-08-23.** `pyproject.toml:21–25` pins `uv` *exactly*
  (`required-version = "==0.11.19"`) with the stated rationale that uv *"is pre-1.0 and ships ~every
  three days with behavioural drift in point releases."* LiteLLM ships **~1.3× per day** — roughly
  four times that cadence — and would sit in the same lockfile under the same discipline. It also
  more than doubles the lock (34 → 56) and pulls `boto3` unconditionally. Separately, the prior
  measured verdict on LiteLLM *in the proxy path* stands and is not re-run here (§3.4).
  **ADOPT-scoped, narrowly:** its public **pricing dataset** is already the de-facto source used by
  `ccusage` (`docs/archive/2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md:59,63`)
  and consuming that JSON is not the same act as depending on the library.
- **`any-llm-sdk` — DEFER, and it is the strongest adopt candidate if a caller ever appears.**
  Covers all four (54 extras), 7 direct deps, an explicit "no proxy, no extra config" posture, and a
  documented LiteLLM migration path (README). Two honest marks against adopting **now**: 61-package
  closure against a 34-package lock, and a project that first shipped 2025-07-15 — thirteen months
  old. DEFER rather than REJECT because the blocker is §2.1's caller count, not the library.
- **`pydantic-ai` — REJECT on cost-for-purpose.** Full four-provider coverage, but a **103-package**
  closure — 3× the current lock — for an agent framework whose agent-loop, tool and dependency-injection
  machinery this repo has no use for. `pydantic` is already a declared dep; the framework is not the
  same buy.
- **`llm` (simonw) — DEFER, with one specific hazard named.** Smallest closure of the covering
  candidates (32 alone, 47 with the four provider plugins), plugin-per-provider, CLI-and-library
  shape that matches how this repo already invokes tools (subprocess to a CLI). **Hazard:**
  `llm-deepseek` last released **2025-02-14** — an 18-month-old single-purpose plugin is the
  `scrummd` bus-factor shape, and DeepSeek coverage would rest on it.
- **`aisuite` — REJECT on maintenance signal.** Last release **2025-11-25**; **0 releases** in the
  90-day window. Also no `xai` extra, so Grok coverage would be an OpenAI-compatible workaround, not
  first-class. This is a clean, citable rejection: re-proposing it needs a new release, not a new
  argument.
- **`langchain` / LangGraph — REJECT, already measured.** `docs/archive/2026-04-24-multi-agent-debate-patterns.md:44,185`
  evaluated LangGraph for stateful debate orchestration and it did not become the mechanism;
  `ai-council` runs its own `PROVIDER_CLASSES`. No new grounds are offered here, so the prior
  outcome stands.
- **OpenRouter (hosted gateway) — REJECT for the credential path; ADOPT-scoped for cost probing.**
  It puts a third party in the request path for a private governance repo, and it collides head-on
  with the **VERIFIED ToS finding** already recorded at
  `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md:114`: *"Using OAuth
  tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service
  … is not permitted."* A gateway is only lawful here on **API keys**, never on a subscription.
- **LiteLLM Proxy / Portkey Gateway / `claude-code-router` — REJECT as standing infrastructure.**
  All three are **always-running local or hosted servers**. The prior memo flags exactly this at
  `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md:105` — *"These run a
  local server — flag against your 'no always-running servers unless justified' rule; justified only
  transiently for a swap test or if you need task-type cost routing."*
  **Honest caveat on that constraint:** I could not locate the no-always-running-servers rule in any
  canonical in-repo doc (`grep -rn "always-running|background server|daemon|127.0.0.1" protocols
  docs/decisions ARCHITECTURE.md VISION.md` returns nothing). It is attributed to the operator in
  that memo and is **not gate-backed**. If it is not in fact a live constraint, this verdict weakens
  and should be re-taken.

### 3.4 The rejection this lane does not re-run

`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` (2026-08-09) already
priced the proxy/adapter path for this fleet against primary sources. Cited, not re-litigated:

- **Prompt-cache loss is the biggest hidden tax** (`:110`). Anthropic's own docs describe silent,
  session-long cache loss behind a custom base URL; LiteLLM strips `cache_control` for
  non-Claude/Gemini models; GitLab hit `cache_creation: 0` in production on the LiteLLM path.
- **Tool-calling format breaks** (`:111`) — case-mangled tool names, dropped `input_json_delta`
  fragments, malformed edit hunks.
- **The steelman against flattening** (`:154`): *"do NOT sacrifice Claude-specific mechanisms to the
  lowest common denominator."*
- **The shape it recommended instead** (`:128`, `:146`) — enforcement in provider-agnostic gates, a
  generation-plus-checksum drift guard, never a hand-rolled framework. **This repo then built that**:
  `provider-registry-agreement` is exactly a generation/agreement gate over provider strings.

---

## 4. The three options, priced

### Option 1 — Routing table (incumbent, partially built)

| | |
|---|---|
| **Build cost** | Incremental. The registry, its reader (`scripts/provider_registry.py`), its checker (`scripts/check_provider_registry.py`, 268 lines) and its commit gate exist. Adding a provider identity = one YAML block. |
| **Adopt-instead cost** | n/a — nothing to adopt; the mechanism is 268 lines of local checker over a 2-key YAML that deliberately mirrors `ecosystem/tool-versions.yaml` rather than inventing a shape. |
| **Maintenance** | One YAML + one checker + one hook. The checker's own stated limit: it asserts **agreement, not correctness** (`CLAUDE.md:176`). |
| **Enables** | Every provider string having one home; a swap being a table edit; a hand-deletion of a pin failing the gate (the S10 count leg, added after a deleted pin passed clean on 2026-08-22). |
| **Forecloses** | Nothing structural. It is additive and reversible. |
| **Does not solve** | Per-provider quirks in callers, shared retry, token accounting, redaction — **and it does not need to, because §2.1 measures one caller.** It also cannot reach the routing decision itself, which is at L0 (R-2). |

### Option 2 — Adapter layer

| | |
|---|---|
| **Build cost** | One interface + one implementation per provider. Serving **1** call site (§2.1). |
| **Adopt-instead cost** | `any-llm-sdk` (+27 packages over the current lock) or `llm`+plugins (+13). Both cover all four. |
| **Maintenance** | A seam, versioned against 4–5 provider APIs. The prior memo's flattening cost (`:154`) applies in full. |
| **Enables** | A genuine common call shape — *if* there are callers. **Proof it works at this exact provider set exists:** `ai-council`'s `PROVIDER_CLASSES` (`protocols/AI_COUNCIL_PROCESS.md:239`) already does this over anthropic/openai/gemini/xai/deepseek, with health-check gating and skip-on-missing-key. |
| **Forecloses** | Per-provider distinctive capability, to the degree callers only see the common shape. |
| **The awkward fact** | The one thing this option would buy is **already bought, one layer down**. Building a second instance in this repo does not extend it; it duplicates it — with `CLAUDE.md:91` standing in the way of the executing half. |

### Option 3 — Full bus

| | |
|---|---|
| **Build cost** | The largest by far: queueing, routing policy, observability, fallback, budget control. |
| **Adopt-instead cost** | LiteLLM Proxy / Portkey / `claude-code-router` — all standing servers, all rejected at §3.3, all carrying the measured prompt-cache and tool-format taxes of §3.4. |
| **Maintenance** | A running service, its config, its failure modes, its upgrades — against a fleet whose gate mesh is deliberately client-side and stateless. |
| **Enables** | Cross-provider fallback, budget ceilings, unified telemetry. |
| **Forecloses** | Provider-native features that do not survive a normalized wire format — most expensively **prompt caching** (`:110`), which is where this fleet's token economics live. |
| **The doctrine bar** | `CLAUDE.md:91` — *"Layer 2 never executes."* In this repo, Option 3 is not a build decision; it is an ADR-28/ADR-36 supersession, and it must be ruled before it is designed. |
| **What already covers part of it** | `[#565]` (`run_id` in telemetry emit) and `[#529]` already own the observability half — **with zero call sites by design**, deliberately sequenced before any read path. A bus proposing to own telemetry would collide with an open, already-ruled row. |

---

## 5. What would have to be true

This section is worth more than a recommendation, because it survives changing circumstances.
**Each condition below is checkable, and none is checkable today by a fact this lane could not read.**

**Option 1 is right if:**
- The count at §2.1 stays at or near **1**. A repo that does not call models does not need an
  abstraction over calling models.
- Provider switching continues to mean *"which CLI does a role invoke"* rather than *"which HTTP
  endpoint does a library hit"*.
- Ruling **R-2** holds — routing stays at L0. (Note that under R-2 the table itself is out of scope
  here, so "Option 1" as a *repo* act means completing the **identity registry**, not owning routing.)
- The cost of a new provider stays dominated by admission work (`[#562]`, `[#578]`) rather than by
  invocation plumbing.

**Option 2 becomes right if:**
- The model-invoking call-site count in this repo rises materially above 1 — the cleanest trigger is
  a number, e.g. **≥3 distinct call sites in ≥2 modules**, which is when duplicated retry/parsing
  starts to cost more than a seam.
- **Or** the `ai-council` adapter is promoted to a shared library the hub consumes, at which point
  the question stops being "build an adapter" and becomes "depend on the one that exists" — a
  materially cheaper and differently-shaped decision.
- **Or** `[#568]` (*provider config as code — one model registry the routing table derives from*)
  lands and its registry needs a runtime consumer rather than a checker.

**Option 3 becomes right if — and all three, not any one:**
- There is measured, recurring **provider unavailability or budget overrun** that a human cannot
  absorb by re-running a lane. No such measurement exists in this repo today.
- Concurrent multi-provider execution becomes routine enough that queueing is a real constraint
  rather than an anticipated one.
- ADR-28/ADR-36 are superseded, **or** the bus is sited in a child repo where execution is lawful —
  in which case it is not this repo's build at all, and `ai-council` is the obvious host.

**A falsifier that would overturn this lane's framing entirely:** if the operator's intent behind
"switching between Grok 4.6, Gemini, DeepSeek and Codex/OpenAI" is **agent-harness switching** (run a
lane under a different CLI) rather than **API-call switching**, then every library in §3 is answering
the wrong question, and the live work is `[#577]` (AGENTS.md as the portable instruction layer) plus
`[#568]` (provider config as code) — neither of which is any of the three options. The four named
providers exactly match `ai-council`'s panel roster, which is weak evidence for the API reading; the
open backlog rows are stronger evidence for the harness reading. **This lane cannot resolve the
ambiguity and does not pretend to** — it is the first thing the fork should settle.

---

## 6. Adversarial pass — run in-lane, and what it changed

The brief names the symmetric failure modes: quietly confirming the incumbent, or talking oneself
into a bus. Both were checked.

**Strongest case for the option I was least inclined toward (Option 3, the bus):**

1. *"One caller" is an artifact of the constraint, not evidence about demand.* `CLAUDE.md:91` forbids
   execution at Layer 2 — so of course the repo has one call site. Measuring caller count in a repo
   that is doctrinally forbidden to call things and concluding "no demand" is circular. The honest
   read is that demand, if it exists, is **displaced** into `ai-council` and into the operator's
   manual dispatch, where this lane cannot see it.
2. *The fleet already runs five providers and already hit exactly the failure a bus prevents.*
   `tasks/568-...md` records it verbatim: *"three provider clients were exercised across two A/B runs
   and each carried its own undocumented config surface, with client behaviour — a silently
   substituted model id, an effort flag that ignores short forms — turning out to be the thing that
   decided a run."* **A silently substituted model id invalidating an A/B is precisely the class of
   defect a normalizing layer with observability catches and a hand-edited table does not.**
3. *Half of Option 3's observability leg is already scoped and ruled* (`[#529]`, `[#565]`), which
   lowers its marginal cost below the "largest by far" framing the brief hands it.

**What the pass changed — not "nothing":**

- **It changed §5.** The Option-3 trigger was originally written as a single condition (measured
  unavailability). Point 1 above is correct that caller-count is partly circular, so the trigger was
  rewritten as a **conjunction of three**, one of which explicitly permits siting the bus in a child
  repo — which is the reading under which point 1 has force.
- **It added the §5 falsifier.** Point 2 forced the question of whether the operator means
  harness-switching, and the honest answer is that this lane cannot tell. Suppressing that would have
  been the "quietly confirms the incumbent" failure.
- **It added the §2.3 caveat** that Option 1's "1 file" is cheap because it is doing less.
- **It did not change the verdict structure**, because there is no verdict — and it did not move
  Option 3 out of "needs an ADR first," because that is a doctrine fact (`CLAUDE.md:91`), not a
  preference.

**What it did not change:** the library verdicts. Points 1–3 argue about *whether to build*, not
*what to adopt*; `aisuite` is still 9 months stale and `litellm` still ships 117 releases a quarter
whichever way the fork is ruled.

---

## 7. Named ADR fork — for the operator to rule

**Proposed ADR question:** *When this fleet switches between Grok 4.6, Gemini, DeepSeek and
Codex/OpenAI, what is the mechanism of record — and where does it live?*

- **Fork A — Registry-and-table (incumbent, completed rather than replaced).** Finish
  `ecosystem/provider-registry.yaml` as the single identity home; leave routing at L0 per R-2; treat
  provider admission (`[#562]`, `[#578]`) and provider config-as-code (`[#568]`) as the live work.
  Cost: incremental. Forecloses nothing.
- **Fork B — Adapter, by dependency rather than by construction.** Rule that the call-shape
  abstraction is a Layer-3 concern, and that the hub consumes `ai-council`'s existing
  `PROVIDER_CLASSES` (or `any-llm-sdk`) **if and when** a caller appears. Cost: a sequencing ruling
  now, an adoption later. Requires naming the caller-count trigger.
- **Fork C — Bus, and the supersession it requires.** Rule that orchestration infrastructure is
  warranted, name its host repo, and either supersede ADR-28/ADR-36 or site it at Layer 3. Cost: the
  largest, and it must be paid before design starts, not after.

**The prior question the fork must settle first**, because it changes which fork is even responsive:
**does "model switching" here mean switching the API a library calls, or switching the agent harness
a lane runs under?** §5's falsifier sets out the evidence on both sides. If the answer is "harness,"
all three forks are the wrong menu and the live rows are `[#577]` and `[#568]`.

**This artifact ends as an intake with that fork named. `banked = 0`** — no `tasks/` row, no
`BACKLOG.md` edit, no `docs/adr/` (which does not exist). Filing is the operator's act.

---

## 8. Interpreter and gate declaration

**Every number in this artifact was produced under the following environment. The gate mesh is
INERT here and nothing above relies on it.**

- **Interpreter:** CPython **3.11.15** at `/usr/local/bin/python3` (`python3 --version`).
  `pyproject.toml:15` declares `requires-python = ">=3.12"` — **this container is below the
  repo's own floor.** No repo script's behaviour was depended upon for a headline number; the two
  scripts invoked were `python3 -c` one-liners over `yaml` and `tomllib`.
- **`uv`:** present at `/root/.local/bin/uv`, version **0.8.17**. `pyproject.toml:25` pins
  `required-version = "==0.11.19"`. `uv run --locked` **refuses**, verbatim:

  ```
  error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
  ```

  This is the **identical** condition recorded by the prior cloud lane at
  `docs/audits/2026-08-21-technical-library-first-research.md:18–21`. The `uv run --locked` gate
  mesh is therefore **inert in this container**, exactly as the brief predicted.
- **What `uv` *was* used for:** `uv pip compile --python-version 3.12 --universal` only — pure
  resolution against PyPI, writing to the scratchpad, installing nothing and touching no repo file.
  Those six closure counts are therefore **resolved under uv 0.8.17, not under the pinned 0.11.19**,
  and a different resolver version could return a different closure. They are directionally sound
  (a 34-package lock vs 56/61/103) and should not be quoted to the package.
- **Network:** outbound HTTPS via the agent proxy. `docs.litellm.ai` and `docs.mozilla.ai` returned
  `EGRESS_BLOCKED`; `pypi.org`, `raw.githubusercontent.com` and `registry.npmjs.org` succeeded.
  `api.github.com` is repo-scoped to `rdwornik/dev-knowledge` and returned an access error for
  third-party repos. Coverage claims in §3.2 name their source per row for this reason.
- **Gates at commit time — measured, not assumed.** The mesh is not merely inert here; it is
  **absent**. `python3 -m pre_commit --version` → `No module named pre_commit`, and neither
  `.git/hooks/pre-commit` nor `.git/hooks/commit-msg` exists, so **no hook fired on this commit**.
  `python3 scripts/audit.py health` cannot run at all — `ModuleNotFoundError: No module named
  'click'` (no synced venv, because `uv sync --locked` refuses on the version pin above). What
  *could* be run standalone, and was:

  ```
  ruff check                                 All checks passed!   (exit 0)
  python3 scripts/validate_hermetization.py  clean                (exit 0)
  python3 scripts/gen_audit_index.py --check clean after --write  (exit 0)
  ```

  The index was stale on adding this file and was regenerated with
  `python3 scripts/gen_audit_index.py --write` (2 insertions, 1 deletion) — the gate's own required
  output. `pytest` was not run: no test-bearing file changed, and the test deps are not installed
  either.
- **Repo mutation:** this file, the `JOURNAL.md` entry, and — if the `audit-index-freshness` gate
  requires it — the regenerated `docs/audits/README.md`, which is a machine-generated index and not
  an independent edit. Nothing else. No `tasks/`, no `BACKLOG.md`, no build, no prototype.

### Traceability index

Every number above resolves to one of these, each read directly this session: `pyproject.toml` ·
`uv.lock` · `ecosystem/provider-registry.yaml` · `protocols/AI_COUNCIL_PROCESS.md` ·
`protocols/STANDING_RULINGS.md` · `protocols/PLAYBOOK.md` · `CLAUDE.md` ·
`deploy/lived_sandbox/spawn.py` · `scripts/check_provider_registry.py` ·
`.claude/workflows/conformance-hub.js` · `tasks/433-*.md`, `tasks/568-*.md` ·
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` ·
`docs/audits/2026-08-21-technical-library-first-research.md` ·
`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` ·
`docs/archive/2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md` ·
`docs/archive/2026-04-24-multi-agent-debate-patterns.md` · PyPI JSON for 9 packages ·
`litellm/types/utils.py` and `pydantic_ai_slim/pydantic_ai/providers/__init__.py` from
`raw.githubusercontent.com` · `registry.npmjs.org` for `@musistudio/claude-code-router` ·
`uv pip compile` output for 6 specs.

**No count in this artifact was estimated, inferred from a summary, or carried over from the brief
without independent measurement** — including the brief's own "3 providers, 5 models, 9 declared /
7 asserted / 5 pinned", which was re-derived from the registry and the checker and **agrees**.
