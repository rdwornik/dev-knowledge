# lane-z-11 — the three comparison repos, and why each earns its slot

> **Step 1 of `lane-z-11-three-repo-comparison`.** Read-only. This file fixes the
> comparison set and the axis each repo is admitted on; the gap matrix is
> `2026-09-15-technical-lane-z-11-comparison-matrix.md` and the two dispositions lists are
> `2026-09-15-technical-lane-z-11-comparison-dispositions.md`.
>
> **Why a slot needs a reason.** Three repos is a sample, and a sample picked for fame
> measures fame. Each slot below is admitted on ONE axis this repo already claims to care
> about, so a gap found there lands on a surface that exists rather than on an aspiration.

---

## The witnesses

Every claim in this lane's three files resolves to one of these trees, at these commits.
They were cloned `--depth 1` into the session scratchpad and read; nothing was installed
and nothing was run from them.

```
github/spec-kit            fd490fac952cc6baeb421905b28031b4c5fe8a99   2026-09-14
bmad-code-org/BMAD-METHOD  94b6727b00c8316557828c8a8ff2a48ff60d60cc   2026-09-11
obra/superpowers           b36e0829c6d0140e93cfef2ca599b1b07d4a7797   2026-08-12 (v6.3.0)
```

**A limit of this session, stated first.** This lane ran in a cloud session whose checkout
is a **shallow clone** (`.git/shallow` present, 275 commits). Any predicate that reads this
repo's object store is therefore unreliable here, and one measurement below had to be
discarded because of it. See the matrix, row G-7.

---

## Slot 1 — `github/spec-kit`, on the spec-driven axis

**What it is.** A spec-driven development toolkit: an installable CLI (`src/specify_cli`),
a command set (`templates/commands/` — `specify`, `clarify`, `plan`, `tasks`, `analyze`,
`implement`, `checklist`, `converge`, `constitution`, `taskstoissues`), artifact templates
(`spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`), and
a versioned `constitution.md` under `.specify/memory/`.

**Why it earns the slot.** This repo *already claims* spec-driven development —
`CLAUDE.md` §4 names ADR-108 §B, the `check-against-spec` skill, the `coherence-nudge`
hook over `_SPEC_REGISTRY`, and the `reconciled_with:` stamp. spec-kit is the most-adopted
public implementation of the same doctrine, which makes it the one repo here that can be
compared **head-to-head on a claim we have already made** rather than on one we have not.
A gap found against spec-kit is a gap in a thing we are already committed to, not a new
appetite.

The sharpest point of contact is `analyze`: a cross-artifact consistency pass over
spec + plan + tasks, run *after* generation and *before* implementation. This repo's
nearest organ, `coherence-nudge`, is declared **non-blocking** in `CLAUDE.md` §9 and fires
on a version-bump signal, not on artifact content.

## Slot 2 — `bmad-code-org/BMAD-METHOD`, on the corpus-self-validation axis

**What it is.** An agentic-agile methodology distributed as skills (`skills/` — roles such
as `bmad-agent-analyst`, `-architect`, `-dev`, `-pm`, `-ux-designer`, plus process skills
`bmad-prd`, `bmad-create-epics-and-stories`, `bmad-correct-course`, `bmad-retrospective`),
with a tool layer under `tools/`: `validate_skills.py`, `validate_file_refs.py`,
`quality.py`, `bundle_web_bundles.py`, `stamp_release.py`.

**Why it earns the slot.** BMAD is the only repo of the three whose *corpus is the product*
in the same way this one's is — markdown instructions that other agents consume — and it is
the only one that ships validators **whose subject is that corpus**: `validate_skills.py`
checks ten deterministic rules over every skill directory, and `validate_file_refs.py`
resolves cross-file references across all source files and refuses absolute-path leaks.

That is the comparison this repo most needs. We are strong on validators whose subject is
*state* (`audit.py health`, the freshness gates, the orphan census) and we have the
predicates for locator resolution in `scripts/preflight_contract.py` — but that module's
input is **one contract handed to it**, not the committed corpus. BMAD runs the corpus-wide
version. The gap is scope of application, not capability, which is the most actionable
shape a gap can have.

BMAD also supplies the honest counter-example on posture: `validate_file_refs.py` defaults
to warning-only, exit 0, and says so in its own docstring — *"Default mode is warning-only
(exit 0) so adoption is non-disruptive."* That is the same adoption-first posture
`preflight_contract.py` declares. Two independent projects reaching the same posture for
the same organ is evidence the posture is right, and it is recorded here so this lane is
not read as arguing for a hard gate.

## Slot 3 — `obra/superpowers`, on the distribution-and-portability axis

**What it is.** Process-enforcing skills (`skills/` — `test-driven-development`,
`verification-before-completion`, `writing-plans`, `executing-plans`,
`dispatching-parallel-agents`, `using-git-worktrees`, `subagent-driven-development`,
`systematic-debugging`, `writing-skills`) shipped as a plugin to **eight** provider
surfaces, each with its own manifest directory: `.claude-plugin/` (with
`marketplace.json`), `.codex-plugin/`, `.cursor-plugin/`, `.devin-plugin/`,
`.hermes-plugin/`, `.kimi-plugin/`, `.opencode/`, `.pi/` — and a `tests/` tree with a
directory **per provider** (`claude-code`, `codex`, `devin`, `hermes`, `kimi`, `opencode`,
`pi`, `antigravity`).

**Why it earns the slot.** This repo's distribution problem is live and named: ADR-115 made
`AGENTS.md` the portable instruction layer, `ecosystem/provider-registry.yaml` holds nine
provider/model seams with `check_provider_registry.py` as the coupling, and
`ecosystem/parity-surfaces.yaml` exists. Superpowers solves the adjacent half of that
problem — not "do the strings agree" but "does the corpus *behave* under each provider's
harness" — and it solves it with per-provider test directories.

It also carries the closest public analogue to this repo's own working mode: skills for
worktrees, parallel-agent dispatch and verification-before-completion map onto PLAYBOOK
Ch8 lanes, `/lane-boot`, `/lane-integrate` and the `verify` skill. That overlap is what
makes it useful as a *rejection* source too — several of its ideas are ones we have
already solved differently and on purpose, and the dispositions file records them as
rejected-with-reason so they are not re-proposed as oversights.

---

## What this set deliberately does not cover

Stated so the sample's shape is legible rather than implied:

- **No LLM-application framework** (LangChain, DSPy and kin). They govern runtime
  behaviour of a program; this repo governs the development process of a fleet. A gap
  matrix across that boundary would compare surfaces that do not correspond.
- **No rules-only collection** (`awesome-cursorrules`, `agent-rules` and kin). They are
  prose corpora with no mechanism layer, so every row would read "they have no gate", which
  measures the sample rather than this repo.
- **No single-vendor product documentation.** Docs describe a tool; they do not commit to a
  methodology that can be compared to ours.

---

**Lane:** `lane-z-11-three-repo-comparison` · **Branch:** `claude/lane-z-11-three-repo-comparison`
**Substrate:** cloud (no gate run — PLAYBOOK Ch8 Layer-1 Q1) · **Date:** 2026-09-15
