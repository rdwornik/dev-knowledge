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
