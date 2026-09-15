---
intake-id: 98
status: DRAFT
origin: lane `lane-z-11-three-repo-comparison`, 2026-09-15 — measured against obra/superpowers' per-provider test tree; see `docs/audits/2026-09-15-technical-lane-z-11-comparison-matrix.md` row G-4
consumed-by:
---

# Provider agreement is asserted over strings, never over behaviour

## Problem / motivation

`ecosystem/provider-registry.yaml` is the declared home for every provider, CLI and model
string the repo's live surface names, and `scripts/check_provider_registry.py` holds nine
table-edit seams in agreement with it. The registry is explicit about what that buys: it
exists because R2 §3.3 found `claude-sonnet-5` hardcoded in three file formats *"with
nothing asserting they agree"*, and a checker is *"the honest mechanism"* for sites that
cannot read YAML at runtime.

What it asserts is that **the strings agree**. What nothing asserts is that **the corpus
behaves** when a second provider actually reads it.

We have already paid for that distinction once, and the evidence is in our own config.
`.claude/settings.json` records that a bare `$CLAUDE_PROJECT_DIR` in a hook command *"turned
any other reader honouring this file (cursor-agent, measured over two paid runs) into total
refusal of every tool call, presenting as the reader being broken."* No string was
inconsistent. Every seam agreed. The corpus was still unusable under a different reader, and
it took two paid runs to find out.

ADR-115 made `AGENTS.md` the portable instruction layer and ADR-117 (Proposed) is actively
splitting carriers by divergence, so the portability surface is growing while the only
assertion over it stays lexical.

`obra/superpowers` treats this as a test problem. It ships its corpus to eight provider
surfaces — `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.devin-plugin/`,
`.hermes-plugin/`, `.kimi-plugin/`, `.opencode/`, `.pi/` — and carries a `tests/` directory
**per provider**: `claude-code`, `codex`, `devin`, `hermes`, `kimi`, `opencode`, `pi`,
`antigravity`. Portability is a thing it runs, not a thing it declares.

**This is the largest row in the comparison and it is filed with that flagged.** It is not a
checker; it is a test substrate, and its cost scales with the number of providers taken
seriously. The functional question below — how many is that, really — decides whether this
is worth anything at all, and it is the operator's to answer.

## Scenarios (+1 view)

- As the **operator** adding a second reader to a repo, I want to know the corpus works
  there before a paid run tells me it does not. Today the only assurance is that the strings
  agree, and the cursor-agent incident is the measured proof that this is not the same
  thing.
- As the **architect ruling on ADR-117 carrier splits**, I want evidence about which
  divergences are real. A per-provider check produces that evidence; a string checker
  cannot.
- As a **consumer repo** receiving the deployed corpus, I want the floor to work under the
  reader I actually run, not under the one the hub happened to author against.

## Functional requirements

- **Must:** at least one assertion exists whose subject is a provider's **behaviour** on
  this corpus, not the agreement of strings that name the provider.
- **Must:** the provider set under test is **declared and small** — the providers this fleet
  actually uses, not every provider that exists. A test tree for a reader nobody runs is
  cost with no signal.
- **Should:** the known failure class is covered first: an instruction or hook command that
  a second reader honours but cannot execute, which is what the cursor-agent incident was.
- **Should:** the result feeds `ecosystem/parity-surfaces.yaml` and the ADR-117 carrier
  split rather than standing alone.
- **Could:** a provider that cannot be exercised in CI is declared untested rather than
  silently assumed working — the same "cannot evaluate" discipline intake `#95` asks for.

## Acceptance criteria (ex-ante)

1. Re-introducing the bare-`$CLAUDE_PROJECT_DIR` defect is detected by something other than
   a paid run under a second reader.
2. The declared provider set under test is readable from one surface and matches what
   `ecosystem/provider-registry.yaml` says the fleet uses.
3. A provider in the registry with no behavioural coverage is *reported as uncovered*, not
   silently counted as passing.
4. Nothing in the existing nine-seam string agreement regresses.

## Non-goals

- Shipping to eight providers. Superpowers' breadth is a product decision for a public
  plugin; ours is a fleet with a named provider set, and copying the breadth would be
  copying the cost without the reason.
- Replacing `check_provider_registry.py`. String agreement stays; this is a second
  assertion over a different subject.
- Live API calls to model endpoints. The subject is whether a reader can consume the corpus,
  not whether a model answers well.
- Re-opening ADR-115 or pre-empting ADR-117.

## Impact sketch (4+1 lite)

- **Logical:** the portability claim gains a second assertion class — behavioural alongside
  lexical.
- **Process:** a carrier-split ruling gains evidence; a second reader stops being adopted on
  faith.
- **Development:** the largest item in this lane's candidate set — a test substrate, plus
  per-provider fixtures. Scope depends entirely on the provider count.
- **Physical:** CI time proportional to providers under test; possibly a provider that
  cannot run in CI at all.

## Open questions

- **How many providers does this fleet actually take seriously?** The functional question
  that decides whether this is worth anything. Operator's to answer (ADR-108 §A).
- Can a second reader be exercised without a paid run? If not, what is the cheapest honest
  substitute — a dry-run parse, a fixture, a declared-untested marker? Technical.
- Does this belong in this repo at all, or at the deploy boundary where the corpus reaches a
  consumer? Technical, and it may reshape the whole item.
- Is the cursor-agent class the only known one, or is there a second measured incident to
  cover? Unmeasured.

## Status

DRAFT — filed by lane `lane-z-11-three-repo-comparison`, 2026-09-15. Not triaged. Flagged as
the largest item in this lane's candidate set; the provider-count question gates it.
