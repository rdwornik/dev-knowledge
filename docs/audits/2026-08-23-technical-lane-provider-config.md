# LANE L1 — Provider configuration (M1)

**Branch:** `worktree-provider-config` · **Merge base:** `aeec0fd1` · **Contract:**
`C:\Users\1028120\Downloads\LANE-L1-provider-config.md` (frozen, read in full before Step 1)
**Model:** Opus 5 · **Effort:** high · **Mode:** auto · **Reviewer:** terra, pre-merge, mandatory

> **Amendments applied.** `C:\Users\1028120\Downloads\RULINGS-and-AMENDMENTS-2026-08-23.md`
> Part 3 declares itself to *"apply to every lane in this batch"*. It has **not landed in-repo**
> at this lane's merge base — LANE-L6 lands it — so it is cited from the operator's disk, which
> is lawful for a LOCAL lane. The five that bind here are **A1** (`docs/adr/` reads
> `docs/decisions/`), **A2** (the suite baseline replaces *"pytest green"*), **A3** (no lane
> writes to `tasks/` at all), **A5** (a citation without a quote is not a citation), and **R2**
> (birth budget zero — a row specification is a *queued proposal*, not a filing). **A6** does
> **not** bind: nothing in this lane registers a check in `audit.py::ALL_CHECKS` — §4 states
> where the check leg lands instead and why that is the correct home rather than a dodge.

---

## 1. Ground truth — what exists today

Premise **E** of `docs/audits/2026-08-23-technical-phase0-preconditions.md` is this lane's
dispatch gate and its starting state. Everything below was **re-verified against the live tree**
at `aeec0fd1` rather than carried from the packet; where the packet and the tree agree, that is
stated as agreement, not repeated as a claim.

### 1.1 The registry exists — and it is the one to extend

`ecosystem/provider-registry.yaml`, **5,889 bytes**, added at **`ff01fd10`** (2026-08-22,
*"feat(ecosystem,scripts): land the provider/model + canonical-doc-name registries (CLOUD-4
v2)"*). This confirms the contract's **Risk** clause in the direction that matters:

> **Risk.** Creating a second registry beside an existing one. Phase 0 tells you whether one
> exists — if it does, **extend it**. Two registries is a worse outcome than none.

One registry exists. This lane extends it. No second registry is created.

### 1.2 The live schema, enumerated from the file rather than described

Two collections, `providers:` and `models:`. The header states the shape is deliberate:

> **SHAPE** — mirrors `ecosystem/tool-versions.yaml`, deliberately (library-first: the repo
> already has a two-key `<collection>: <id>: <fields>` ecosystem-state shape and this does not
> invent a second one).

**`providers.<id>` keys in live use** (7): `display_name`, `cli`, `version_command`,
`changelog_tool_key`, `changelog_source_url`, `marketplace_id`, `marketplace_source_path`.

**`models.<id>` keys in live use** (5): `provider`, `tier`, `roles`, `attribution_token`,
`pinned_at` — the last a list of `{path, seam, format}`.

**The schema is nowhere declared.** It is implied by `scripts/provider_registry.py`'s accessors
and by what `scripts/check_provider_registry.py::check_registry_shape` happens to assert, which
today is exactly one rule — *"every model names a registered provider"*. That is the gap §3
closes with pydantic, and it is why the contract's library-first clause names this file.

### 1.3 Current entries — 3 providers, 5 models

```
providers  anthropic (cli: claude) · openai (cli: codex) · xai (cli: null)
models     claude-sonnet-5 · claude-opus-4-8 · gpt-5.6-terra · gpt-5.6-sol · grok-l5
```

Agrees with premise E exactly.

### 1.4 Consuming seams — the three numbers, and they are not the same number

Premise E's warning that conflating these is how the registry gets misread is correct, and the
counts re-verify:

```
9  DECLARED in scope by the file's own header (R2 §3.2 table-edit seams)
     S7 S8 S9 S10 S11 S17 S26 S29 S30
7  ASSERTED by scripts/check_provider_registry.py
     check_s8_tool_versions · check_s9_artifact_reader · check_s10_conformance_hub
     check_s17_playbook · check_s26_settings · check_provenance_pins (S29+S30)
     (+ check_registry_shape, which validates the registry itself, not a seam)
5  PINNED sites listed in the registry's own pinned_at blocks
     .claude/agents/artifact-reader.md (S9) · .claude/workflows/conformance-hub.js (S10)
     protocols/PLAYBOOK.md (S17) · ecosystem/satellite-onboarding-rulings.yaml (S29)
     pyproject.toml (S30)
```

**Mechanical consumer set, whole** — the answer to *"is it read by anybody?"*:

| Consumer | Kind | How it reads |
|---|---|---|
| `scripts/provider_registry.py` | reader module | `load_registry()` + 8 accessors |
| `scripts/changelog_sentinel.py` | **runtime**, SessionStart | `_TOOLS = _preg.version_commands()` (S7) |
| `scripts/check_provider_registry.py` | pre-commit gate | 7 seam checks |
| `tests/test_provider_registry.py` | suite | 23 tests |
| `.pre-commit-config.yaml` | gate wiring | hook `provider-registry-agreement` |

So the registry is **already consumed** at its merge base. The contract's closure item 2 is
therefore not *"make something read it"* — it is *"make something read the rows this lane
adds"*, which is a strictly harder bar and the one §4 answers.

### 1.5 What `[#577]` actually carries — and why this lane does not touch it

`tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md`:

```yaml
id: "[#577]"
title: "Adopt `AGENTS.md` as the portable instruction layer — the bounded execution lane"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
```

Its body opens *"**RULED ADMITTED (architect, 2026-08-22); this row is the execution, not the
decision.**"* and its four bounds are all about `AGENTS.md`. **Nothing in the row concerns
`ecosystem/provider-registry.yaml`.** Premise E's operative finding stands:

> **So the operative answer to L1 is: `[#577]` IS the AGENTS.md carrier. L1 must NOT extend it,
> and must instead specify a new carrier row in its artifact without creating the task file.**

The contract's branch fires. §2 writes the specification; no task file is created.

### 1.6 The configuration gap, stated as a measurement rather than an intent

The mandate names four providers — Grok 4.6, Gemini, DeepSeek harness, Codex/OpenAI. Measured
against the registry at `aeec0fd1`:

| Mandate provider | Registry provider | Present? | Model row for it? |
|---|---|---|---|
| Grok 4.6 | `xai` | **yes** (`cli: null`) | **no** — only `grok-l5`, a *provenance* token |
| Gemini | `google` | **NO** | no |
| DeepSeek harness | `deepseek` | **NO** | no |
| Codex/OpenAI | `openai` | **yes** (`cli: codex`) | yes — `gpt-5.6-terra`, `gpt-5.6-sol` |

**There is an independent, checkable surface that says the same thing**, and it is what turns
this from a mandate assertion into a repo fact. `protocols/AI_COUNCIL_PROCESS.md:169` declares
the council's default provider panel as a closed five-token set:

```
| `models`         | `claude,gemini,openai,deepseek,grok`     | All 5 by default. `--lite` overrides to 3-model (claude, gemini, openai). |
```

Five aliases; the registry carries **three** of them. `gemini` and `deepseek` resolve to nothing.
That is the configuration gap, and because it is a *disagreement between two committed surfaces*
it is exactly the class the registry was cut to end — R2 §3.3's finding was a value living in
several formats *"with nothing asserting they agree"*. §4 makes this pair assert.

### 1.7 Two boundaries this lane inherits and does not cross

- **Routing is not here.** The registry header: *"**ROUTING IS NOT HERE.** ... This registry
  records model IDENTITY, not which model gets routed to which job."* Reinforced by standing
  ruling **R-2**: `~/.claude/ROUTING.md` is **L0, outside this repository**. Nothing in this
  lane routes anything.
- **`.gemini/settings.json` is refused, and that is not the same act as a `google` row.**
  Standing ruling **R-1** records: *"**Not admitted:** `.gemini/settings.json`. It would be a
  new top-level directory that `validate_hermetization.py` Rule A refuses absent an ADR-101 §1
  amendment."* A provider **row** in an existing tracked YAML file creates no top-level
  directory and triggers no Rule A. The refusal is of a *config-directory shape*, not of the
  provider's existence in the vocabulary — which is itself an instance of the distinction §6
  records.

### 1.8 Suite baseline at the merge base

Per **A2**, *"pytest green"* is retired in favour of an exact baseline:

> **1 failed (`test_anchor_gate_probe_distinguishes_installed_from_absent`), 3567 passed,
> 4 skipped, 1 xfailed.**

Measured at the Final step, unpiped, and reported in §8 with every delta attributed.

---

## 2. Carrier row — one attachment, one queued proposal, one collision reported

The contract instructs: *"If premise E confirms `[#577]` is the AGENTS.md carrier, **do not
extend it** — subjects do not share rows."* §1.5 confirms it does. But the batch amendment **R2**
overrides the assumption that a *new* row is the answer, and it is quoted rather than paraphrased:

> **Therefore, per the mandate's own option (b): every mandate item ends as a filed intake with
> its ADR fork named, or attaches to an existing open row. Existing rows first** — `[#242]`/
> `[#362]` for M5, `[#171]` for M8, `[#560]` for M3. Every row specification a lane produces is a
> **queued proposal awaiting an explicit architect grant**, not a filing.

So the honest act is to look for the existing owner **before** specifying a new row. There is one.

### 2.1 `[#568]` already owns provider configuration — and says so itself

`tasks/568-provider-config-as-code-dev-knowledge-as-source-of-.md`, `status: open`, `[P2][M]`,
theme `[E7] Tooling & evaluation`, story `[S18] Cut session friction with better tooling`. Its
own kill-candidates line makes the ownership claim explicit:

> `kill-candidates: none — no open row owns provider configuration`

and its Done-when carries the clause this lane partially executes:

> "one model registry file carries **every model id with its effort enum and admission status**"

**Verdict: attach, do not duplicate.** Two of that clause's three components are landed by this
lane (§3: every model id; admission status as data). One is not — the **effort enum** (the
canonical set `{low, medium, high, xhigh, max}` from the outgoing architect's ratified-in-chat
register), not landed here because no live surface in this repo binds a *model* to an effort
value, and inventing that binding is the fabrication class this lane exists to guard against.

**Attachment text, for the integrator to append to `[#568]`'s body — a queued proposal under R2,
not a filing:**

```text
PARTIAL EXECUTION, LANE L1 (2026-08-23, docs/audits/2026-08-23-technical-lane-provider-config.md):
the "one model registry" half of this row's Done-when is now two-thirds landed in
`ecosystem/provider-registry.yaml` — every provider on the live surface carries a row (5 of 5
council aliases resolve), and admission status rides as per-role DATA (`role_admission:`) rather
than as prose in an audit. STILL OPEN on this row: (a) the per-model EFFORT ENUM, unlanded
because no in-repo surface binds a model to an effort value; (b) the junction topology, untouched;
(c) Done-when clause 3, "the routing table derives from it rather than restating it", which
COLLIDES with standing ruling R-2 — see the lane artifact section 2.3.
```

### 2.2 The queued row proposal — provider discoverability, the one subject with no owner

The residual that neither `[#568]` (config-as-code / junctions / routing derivation) nor `[#577]`
(`AGENTS.md`) nor any other open row covers is the **discoverability surface** §5 proposes: a
generated, gated, human-facing provider index. It is specified here and **not filed** — R2 sets
the birth budget at zero and **A3** forbids a lane writing to `tasks/` at all:

> **A3 — No lane writes to `tasks/` at all.** Not the manifest, and **not even its own task
> file.** ... A lane needing a row writes a **row specification into its own `docs/audits/`
> artifact** (lane-private, no collision).

```text
- [#<integrator-assigned>] [P3][S] **Provider discoverability surface — one generated index, gated
  like the other seven** — `ecosystem/provider-registry.yaml` is machine-readable and machine-read,
  and that is the whole of its reach. Measured at `aeec0fd1` across the tracked `.md` corpus: the
  registry's PATH appears in exactly ONE canonical living doc — `CLAUDE.md:176`, inside a
  pre-commit-hook roster row, described as the thing a gate checks; `ARCHITECTURE.md:714` names the
  hook and not the file; `VISION.md`, `CONTRIBUTING.md`, `protocols/PLAYBOOK.md` and
  `protocols/ESSENTIALS.md` carry ZERO mentions; and repo-wide there is **not one markdown link**
  to it (`grep -rcE '\]\(\.?/?(ecosystem/)?provider-registry\.yaml' --include=*.md` returns
  nothing). A human asking "which providers does this repo know about?" has no surface to read.
  The operator asked for exactly this — "all major LLM providers visible at root with
  dynamic links" (outgoing-architect supplement, answer 6, 2026-08-23) — and the ROOT half of that
  ask is barred until ADR-114 is ruled, so this row builds the lawful half now: a generated
  `ecosystem/providers.md` in the shape `ecosystem/registry.md` already established (human surface
  beside machine surface), regenerated from the registry and drift-gated by regen-and-diff exactly
  as `audit-index-freshness` / `organ-index-freshness` / `intake-index-freshness` already are — the
  repo runs that organ shape seven times over and would not be inventing one. · Done when:
  `scripts/gen_provider_index.py --write` emits `ecosystem/providers.md` from the registry alone, a
  `provider-index-freshness` pre-commit hook runs `--check` and BLOCKS on drift, every link in the
  emitted file resolves (asserted by a test, not by eye), and one line in an existing canonical doc
  points at it · refs docs/audits/2026-08-23-technical-lane-provider-config.md section 5, ADR-114
  (PARKED — the root file stays barred), ADR-101 section 1, `ecosystem/registry.md` (the precedent
  shape), #568 · kill-candidates: none — `[#568]` owns config-as-code and the junction topology and
  explicitly scopes itself to "config and registry only"; this is the READ surface over that
  registry, which no open row owns
```

**Position is a stated preference, not an assumption** — the A6 discipline applied to a row rather
than to `CHECK_ORDER`: theme `[E7] Tooling & evaluation`, story `[S18] Cut session friction with
better tooling`, immediately after `[#568]` at `BACKLOG.md:268`. The integrator derives the real
position from the manifest node.

**Next-free id at this merge base is `[#579]`, and the obvious measurement is wrong.** A history
scan for the maximum bracketed id returns **777** — which is *synthetic*, appearing only inside
`[#574]`'s own body as the example of this exact trap (*"the next-free-id history scan is defeated
by synthetic `[#777]` — a surface that looks authoritative and is not"*). The live maximum from
`tasks/` is **578**. Reported rather than used: **the integrator assigns the id**, per A3.

### 2.3 Reported, not fixed — `[#568]`'s Done-when clause 3 collides with standing ruling R-2

`[#568]` requires *"the routing table derives from it rather than restating it; and a test FAILs
on a routed model absent from the registry."* Standing ruling **R-2** (2026-08-22, later than the
row) places that table outside the repo:

> `~/.claude/ROUTING.md`, `~/.claude/bin/codex-review.ps1` and `~/.codex/config.toml` sit at L0.
> Their absence from this repository is a placement, not a gap.

A hub-local test cannot assert over an L0 file without reversing that placement, so the clause is
**unexecutable as written** while R-2 stands. Surfaced, not resolved: rewording a live row's
Done-when is not a lane's act, and per **A3** this lane does not touch `tasks/` at all.

---

## 3. The four providers, configured — and the schema that was missing

### 3.1 Library-first, discharged with a measurement rather than a preference

The contract's clause is unconditional:

> Before writing any validation code: the registry is YAML with a schema. `pydantic` is already
> in the curated baseline. **Use it.** Hand-rolled YAML shape-checking in this repo needs a
> measured divergence to justify itself, and there is none here.

**There is none here, and the measurement is the gap it closes.** Before this lane, the whole
of the registry's shape enforcement was `check_registry_shape()` — eleven lines asserting one
rule, *"every model names a registered provider"*. Nothing asserted that a `cli:` and its
`version_command:` named the same binary, that `changelog_tool_key` had its
`changelog_source_url` partner, or that an unrecognised key was a typo rather than a feature.
`pydantic>=2.0,<3` is at `pyproject.toml:36`, named by the operator-ratified intake #22 §E, and
`ecosystem/schema/desired_state.py` (ADR-109 §8, F2 — an operator-approved directory) already
establishes this exact home for a pydantic contract. **No divergence was found, so none is
recorded, and no hand-rolled checker was written.**

Landed: **`ecosystem/schema/provider_registry.py`** — models only, no I/O, no execution
(Layer-2, ADR-28/36), with `extra="forbid"` and `frozen=True` mirroring the sibling module.

### 3.2 Where validation runs, and why that placement is the consumption answer

`scripts/provider_registry.py::load_registry` validates through the schema on **every load**,
then returns the raw mapping unchanged so all eight existing accessors keep working. That
placement is the point: it means the SessionStart sentinel, the pre-commit agreement gate and
the suite each validate the rows this lane added **without any of them opting in**. A
`ValidationError` is re-raised as `RegistryError`, so the pre-existing failure contract is
untouched — `main()` still exits 2, the fail-soft hook still goes quiet rather than bricking
session start.

### 3.3 The rows

**Providers — 3 → 5. All five council aliases now resolve.**

| id | display_name | council_alias | cli | version_command | changelog pair |
|---|---|---|---|---|---|
| `anthropic` | Anthropic | `claude` | `claude` | `["claude","--version"]` | yes |
| `openai` | OpenAI | `openai` | `codex` | `["codex","--version"]` | yes |
| `xai` | xAI | `grok` | `null` | `null` | no |
| **`google`** *(new)* | Google | `gemini` | `gemini` | `["gemini","--version"]` | **no — see below** |
| **`deepseek`** *(new)* | DeepSeek | `deepseek` | `null` | `null` | no |

**Models — 5 → 7.**

| id | provider | roles | role_admission |
|---|---|---|---|
| **`grok-4.6`** *(new)* | `xai` | `[]` | `fan-out: refused` · floors `G1, G2` |
| **`gemini-3.7-flash`** *(new)* | `google` | `[]` | `fan-out: refused` · floor `G1` |

**Every value above was verified, not assumed:**

- `gemini` resolves on PATH and `gemini --version` prints `0.56.0`. `grok` and `deepseek` do
  not resolve — hence `cli: null` for `xai` and `deepseek`, which is a fact about this surface
  rather than an omission (and the schema now asserts `cli` and `version_command` agree).
- The two model ids are the strings the providers **actually served**, re-recorded on every
  scored round: `docs/audits/2026-08-23-technical-lane-562-local-admission.md` **§1.2** records
  *"model AS SERVED: `grok-4.6`"* and *"modelVersion AS SERVED: `gemini-3.7-flash`"*, under the
  Q9 substitution probe that exists because a client quietly serving `grok-4.5` cost a window.
- The floors come from that artifact's own arithmetic — **§7.1**'s
  `G1 v2 = (a) AND (b) AND (c)   gemini FAIL   grok FAIL`, plus **§7.4**'s *"**G2 still fails on
  the `C1-R5` fabrication**, which is independent of `C1-N2`"* — and agree with `[#578]`'s row
  body (*"`gemini-3.7-flash` on the G1 floor, `grok-4.6` on G1 and G2"*).

### 3.4 Three fields added to the schema deliberately, each with its reason

The contract permits this and requires the reason be stated: *"If a provider genuinely needs a
field the schema lacks, add it to the schema deliberately and say why — do not smuggle it in as
a one-off."*

1. **`providers.<id>.council_alias`** — the token `protocols/AI_COUNCIL_PROCESS.md` names the
   provider by. It is a **different string from the registry key for two of five**
   (`anthropic`/`claude`, `xai`/`grok`), which is precisely why it must be data: without it the
   §4 checker would hardcode that mapping, re-creating in code the drift the registry exists to
   end. Nullable — a provider the council does not panel simply omits it.
2. **`models.<id>.role_admission`** — `{role: verdict record}`, carrying `verdict`,
   `decided_by`, `decided_on`, `floors`, `evidence`, `rerun_carrier`. Without it the only home
   for a refusal is prose in an audit, and — worse — the *absence* of any admission field is
   what currently makes "present in the registry" read as "admitted". Recording the verdict as
   data is what lets configuration be unconditional. **Optional, and that is load-bearing:** a
   model row is fully valid with no admission record at all, which is the structural statement
   of §6's rule.
3. **`verdict` as a closed three-member enum** — `admitted | refused | **unevaluated**`. The
   third member is deliberate: a provider nobody has run through the pipeline is in a *known*
   state, not a missing one, and naming it is what stops an absence being read as a refusal.

### 3.5 What is NOT configured, and why each absence is the honest state

- **No `changelog_tool_key` / `changelog_source_url` for `google`.** Those keys are the S8 half
  of `ecosystem/tool-versions.yaml`, whose rows carry `last_reviewed_version` and
  `reviewed_date` — an **ADR-80 DURABLE record of a review the operator performed**. Adding a
  row would either fabricate that act or seed one the sentinel is structurally silent on
  (`parse_version("") → None → is_newer False`). **Discharge, named rather than left open:**
  run `/changelog-review` against the gemini CLI once; the tool-versions row and these two keys
  land on the same commit and `check_s8_tool_versions` begins asserting immediately.
- **No model row for `deepseek`.** No model id for this provider is verified anywhere on this
  repo's live surface. DeepSeek reaches the fleet only as an `ai-council` panel member, whose
  model string lives in that child repo's config and is therefore not this repo's to declare —
  `CLAUDE.md` §5 rule 4: *"**Layer 2 never executes** — no orchestration scripts: no script
  drives state in a child repo (ADR-28, ADR-36)."* `deepseek-v4-pro` appears in `ADR-31` and
  `ADR-68` as a 2026-04/06 council-panel record, unverified since; registering a stale id is
  worse than registering none. The operator's 2026-08-23 ask — DeepSeek through the admission
  pipeline — is the act that produces a probe-verified served id, and the id lands with it.

### 3.8 One gate fired on this step, and the fix is a rewording rather than a bypass

The first attempt at this commit was **BLOCKED** by `audit-health`:

```
[!!] silent_rule_ratchet: silent-rule pool GREW: live 443 > baseline 441 (+2) under detector
     silent-rule-v4 across 59 file(s) — drain the additions or record an operator ruling; the
     baseline does not rise on a commit
```

`ecosystem/*.yaml` is inside the detector's scope (`SCOPE_GLOBS = ("protocols/*.md",
"templates/**/*.md", "templates/**/*.tmpl", "ecosystem/*.yaml")`), and the registry's new
header comments carried **exactly two** occurrences of the `must|shall|never` token set. Both
were **drained by rewording**, not bypassed and not baseline-raised — the baseline may be
lowered or held but not raised without an operator ruling, and this lane holds none:

1. *"its absence **never** makes a row less valid"* → *"a row carrying none is exactly as valid
   as one that does"* — same claim, no normative token.
2. The parenthetical quote of `CLAUDE.md` §5 rule 4 (*"Layer 2 **never** drives a child repo's
   state"*) moved **out of the YAML and into this artifact** (§3.5 above), where `docs/` is
   outside the ratchet corpus. The **A5** obligation to quote a cited clause is discharged at
   the site that can afford the tokens; the YAML keeps the locator.

`ecosystem/schema/provider_registry.py` and this artifact are both outside the scope globs, so
neither contributes to the pool — worth stating, because a lane that drained the wrong file
would have shipped a green gate and a lost sentence.

**One mechanism note, because it cost a measurement.** The detector reads **staged blobs**,
not the working tree: after the two rewordings the standalone run still printed `443`, and only
`git add` brought it to `441`. Re-measuring before staging reads the pre-edit file and says the
fix did not work.

---

## 4. Proving consumption — S31, and why the bar is the added rows

The contract's closure item 2 is deliberately strict:

> The registry is **actually consumed** by at least one existing seam — not merely present.
> Name the seam and show the consumption. Present-but-unread is the failure mode this repo
> already carries in four unwired modules; do not add a fifth.

§1.4 established that the registry *file* was already consumed at the merge base. That makes
the honest bar harder, not easier: the question is whether the rows **this lane added** are
read by anything, or whether five new providers and two new models are five-and-two pieces of
inert data. Two mechanisms answer it, and the second has teeth.

### 4.1 Mechanism 1 — schema validation, at every existing consumer

`load_registry()` validates through `ProviderRegistry` (§3.2). Since all three live consumers
reach the file through it, the added rows are parsed and validated by:

| Existing seam | When it runs | What it now does with the new rows |
|---|---|---|
| `scripts/changelog_sentinel.py` (S7) | every SessionStart | parses all 5 providers; a malformed one raises `RegistryError` |
| `provider-registry-agreement` hook | every commit touching a checked site | same, and an error **exits 2 / BLOCKS** |
| `tests/test_provider_registry*.py` | every suite run | 51 tests |

Honest about what this is: **validation, not use.** It stops a bad row, it does not read a good
one. On its own it would be a weak answer, which is why there is a second mechanism.

### 4.2 Mechanism 2 — S31, a new seam leg on the existing checker

**The seam, named:** `protocols/AI_COUNCIL_PROCESS.md`'s council provider roster, held in
agreement with the registry's `council_alias` vocabulary by
`scripts/check_provider_registry.py::check_s31_council_panel`, registered in `run()` and
therefore live in the **existing** `provider-registry-agreement` pre-commit hook. This is
wiring a leg onto a consumer that already exists — the contract's permitted act — rather than
building a new consumer from nothing, which it forbids.

**This is not a new seam class.** It is R2 §3.3's own finding applied to the one surface where
it was still true: a closed provider vocabulary living in committed prose, with nothing
asserting it agrees with the registry.

**Checked in both directions, each catching a different rot:**

- *roster → registry* — the council panels a provider the registry has never heard of. Same
  class as `check_provenance_pins` ("a provider quietly enters the corpus without entering the
  vocabulary"), and it is how the roster came to name five while the registry declared three.
- *registry → roster* — the registry claims an alias the roster no longer names, i.e. a stale
  assertion. `council_alias: null` is the unambiguous fix, and the schema permits it.

**The measurement that shows it is not vacuous** — `check_s31_council_panel` run against the
**merge-base** registry (`git show aeec0fd1:ecosystem/provider-registry.yaml`) versus now:

```
merge base aeec0fd1   council_alias vocabulary: {}                 roster tokens unresolved: 5/5
                      providers with no entry of any kind:         gemini, deepseek  (2/5)
after this lane       {claude: anthropic, gemini: google, openai: openai,
                       deepseek: deepseek, grok: xai}              roster tokens unresolved: 0/5
```

Both numbers are reported because they measure different things. **5/5** is unresolved under
the new field's semantics — `council_alias` did not exist, so nothing resolved. **2/5** is the
substantive gap: `gemini` and `deepseek` had no provider entry at all, by any name. The seam
would have failed at the merge base under either reading, which is the point of running it
there.

**Teeth, asserted rather than claimed** — three mutation tests over a tmp-tree copy: a roster
token with no registry entry is caught; a registry alias the roster dropped is caught; and a
**reworded roster row fails LOUD** (*"roster row not found"*) instead of passing quietly, the
same anchored-regex posture `_PROSE_TIER_RE` already uses for S17.

### 4.3 A second, smaller consumer — admission evidence resolves

`check_role_admission_evidence` requires every recorded verdict to cite an artifact that
**exists**. The schema refuses a decided verdict with no `evidence:` string, but a models-only
module cannot touch a filesystem; this is the other half. A verdict citing a renamed artifact
decays into an unfalsifiable claim, and the registry is exactly the surface a future lane reads
to find out *why* a role is not held — a dead locator there is worse than none. Mutation-tested
by deleting the cited artifacts from the tmp tree.

### 4.4 The hook's `files:` pattern was extended — flagged as a likely conflict site

`.pre-commit-config.yaml` gained `AI_COUNCIL_PROCESS` to its existing `protocols/PLAYBOOK\.md`
alternation, so an edit to the roster fires the gate. Without it the coupling would only fire
from the registry end — half-wired, which is the present-but-unread failure in a new costume.

**Stated for the integrator rather than left to be discovered:** this lane's contract does not
reserve `.pre-commit-config.yaml`, so the edit was made rather than shipped as a fenced diff
(the CLOUD-4 v2 precedent recorded at `CLAUDE.md` v2.64 applies to a lane whose contract *did*
reserve it). Seven lanes were live in this batch and this file is a classic collision surface.
The change is one regex alternation plus its comment — textual, surgical, and trivially
reconcilable if another lane also adds a hook.

### 4.5 What is honestly NOT proven

**No seam routes to these providers, and none can from this repo.** Standing ruling R-2 places
the routing table at L0. So "consumption" here means *the rows are read, validated and held in
agreement with a live committed surface* — it does not mean anything dispatches to Gemini or
DeepSeek on the strength of them. Claiming otherwise would be the overstatement this lane's own
§2.3 finding penalises `[#568]` for.

### 4.6 Suite delta from this step

Six new tests in `tests/test_provider_registry.py` (three S31 teeth, one live S31 assertion,
one live evidence assertion, one evidence teeth). The `tree` fixture gained
`protocols/AI_COUNCIL_PROCESS.md` and — **derived from the registry rather than typed** — every
artifact a live verdict cites, so a future verdict cannot silently leave the fixture behind.
Combined: **51 passed, 0 failed.**

---

## 5. Root visibility — the derivation says BARRED, so this proposes the nearest lawful home

The contract's instruction and its escape clause are both explicit:

> **5. Root visibility — PROPOSE, do not create.** Derive the taxonomy-correct home from
> primary sources, quote them, and write the proposal into your artifact: the exact path, the
> governance clause permitting it, and the generation mechanism for the links. **If the
> derivation says the root is barred, say so and propose the nearest lawful home.** Do not
> create a root file on the strength of the mandate's wording alone.

**The derivation says barred, on four independent grounds. None of them is a judgement call.**

### 5.1 Ground 1 — the tree seal refuses it mechanically

`scripts/validate_hermetization.py` Rule A gates every added top-level file against a closed
enum. Measured live, `SANCTIONED_TIER1_FILES` holds **20 members**:

```
.dev-knowledge.code-workspace  .gitattributes  .gitignore  .methodology.yaml
.pre-commit-config.yaml  .pre-commit-hooks.yaml  .python-version  .ruff.toml
.worktreeinclude  ARCHITECTURE.md  BACKLOG.md  CLAUDE.md  CONTRIBUTING.md  JOURNAL.md
LESSONS.md  VISION.md  package-lock.json  package.json  pyproject.toml  uv.lock
```

`PROVIDERS.md` → **not a member**. `providers.md` → **not a member**. A root provider file is a
pre-commit **BLOCK**, and the enum is closed by ADR-101 §1 — widening it is an ADR amendment,
which is an architect act.

### 5.2 Ground 2 — the identical question is already PARKED, and citing it is forbidden

ADR-114 is the live decision on whether a root file may be added, and its ruling closes with:

> **Until it is ruled, nothing in this repo may cite ADR-114 as authority**, and the
> `README.md` prohibition stands unchanged.

Its **option (B)** is precisely the shape a root `PROVIDERS.md` would need — *"Amend ADR-101 §1
to sanction a root `README.md` as an **additional** Tier-1 file"* — and that option is unruled.
So there is no authority to cite, and the ADR itself forbids citing it as one.

### 5.3 Ground 3 — the operator's own ask routes it to a decision, not to an execution

The outgoing architect's supplement (`docs/handoffs/2026-08-23-dev-knowledge-architect/
SUPPLEMENT.md`, answer 7) records the ask and its home in the same line:

> - **"provider-visibility ask"** · operator wants major providers visible at repo root with
>   dynamic links · home: **re-opened discussion under ADR-114 (PARKED status re-presented
>   with price), NOT a silent execution.**

A lane creating the root file would be performing exactly the *"silent execution"* the record
names and refuses. **This is the ground that would still bar it even if grounds 1 and 2 did
not**, and it is why the contract's *"on the strength of the mandate's wording alone"* clause
is pointed rather than decorative.

### 5.4 Ground 4 — the adjacent precedent, one day old

Standing ruling **R-1** refused `.gemini/settings.json` on this exact mechanism: *"It would be
a new top-level directory that `validate_hermetization.py` Rule A refuses absent an ADR-101 §1
amendment."* Same gate, same amendment requirement, same week.

### 5.5 The proposal — `ecosystem/providers.md`, generated and gated

| | |
|---|---|
| **Exact path** | `ecosystem/providers.md` |
| **Governance clause permitting it** | `ecosystem` is a `SANCTIONED_TIER1_DIRS` member **and** a Rule C allowlisted home — verified live: `validate_hermetization.is_allowed_home("ecosystem")` → `True`. Adding a file there triggers **no** ADR-101 amendment, no new top-level entry, no new `docs/<genre>/` folder. |
| **Precedent shape** | `ecosystem/registry.md`, whose header states the split this proposal copies: *"The registry is two surfaces, split by audience: **`ecosystem/registry.md` (this file) = the human registry** ... **`ecosystem/<repo>/` + `ecosystem/index.yaml` = the machine registry**"*. Human surface beside machine surface, same directory, already ratified once by the 2026-07-08 census ruling C-10. |
| **Generation mechanism** | `scripts/gen_provider_index.py --write` emits the file from `ecosystem/provider-registry.yaml` **alone**; `--check` is a regen-and-diff comparison. Wired as a `provider-index-freshness` pre-commit hook with `files:` covering the registry, the schema and the generator. |
| **Why regen-and-diff and not a hand-maintained page** | ADR-114's own consequence analysis for its option (B): *"a front door that goes stale is worse than none, so (B) should carry a generated-and-gated shape — the repo already runs regen-and-diff seven times over and would not be inventing an organ."* The seven: `codemap-freshness`, `toc-freshness-playbook`, `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`, `intake-index-freshness`. |
| **Links, and that they resolve** | Emitted links: the registry itself; each provider's `changelog_source_url` where present; each `role_admission.evidence` artifact; each `rerun_carrier` row. All are already validated data — `check_role_admission_evidence` (§4.3) proves the evidence paths exist today — so the generator emits from a source that is checked rather than from prose. The proposed row's Done-when requires a test asserting every emitted link resolves. |
| **Root-discoverability** | One line from an existing canonical doc. **`ARCHITECTURE.md` Ch3 "Automation axes"** is the taxonomy-correct anchor: `CLAUDE.md` §3 already routes model routing and the t-shirt tiers there, and Ch3 is where standing ruling R-2's L0 boundary is recorded. |

**The cost of that one line, stated rather than hidden.** `ARCHITECTURE.md` carries a
`last_reviewed` stamp, and `CLAUDE.md` §4's freshness cadence defines what editing it obliges:

> the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS` carry a `last_reviewed`
> frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* —
> **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last
> edit.

So the pointer line is not free: it obliges a genuine end-to-end re-read of `ARCHITECTURE.md`
in the same commit. That is a reason to spend it deliberately in the proposed row — not a
reason to skip it, since a generated index nothing points at is the discoverability problem
one directory deeper.

### 5.6 What this lane did NOT do, so the boundary is unambiguous

No root file was created. `ecosystem/providers.md` was **not** created either — it is the
*proposal*, and the row that would build it is the queued proposal at §2.2, unfiled under R2's
zero birth budget. `ARCHITECTURE.md` was not edited. The lane's whole answer to closure item 3
is this section: the exact path, the quoted clause admitting it, the generation mechanism, and
the four quoted grounds barring the root.
- **No effort enum on any model.** §2.1 records why: no live in-repo surface binds a *model* to
  an effort value, and the canonical enum's home is doctrine, not this file.
- **No routing.** The registry header and standing ruling **R-2** both place it at L0.

### 3.6 One existing test fixture changed — stated because a changed test is a claim

`tests/test_provider_registry.py::test_version_commands_omits_a_provider_with_no_cli` built its
tmp-path registry as `{"with": {"version_command": [...], "changelog_tool_key": "x"}, ...}` —
a provider with a **probe and no CLI**, and **half an S8 pair**. Both are now refused by the
schema. The fixture gained `display_name`, an explicit `cli:` and the missing
`changelog_source_url`; **the assertion is byte-identical**. This is the schema catching an
illegal shape that had been sitting in the suite, not a test relaxed to fit a change.

### 3.7 Suite delta from this step

`tests/test_provider_registry_schema.py` — **22 new tests**, every one a **mutation check**:
a legal registry is built, exactly one field is broken, and the schema is required to refuse
it. A schema test that only proves the live file passes would still pass with every validator
deleted. Combined with the 23 pre-existing: **45 passed, 0 failed.**
