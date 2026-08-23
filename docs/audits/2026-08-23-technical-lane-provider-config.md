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
