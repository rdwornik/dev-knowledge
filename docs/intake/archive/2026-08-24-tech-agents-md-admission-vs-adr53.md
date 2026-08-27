---
intake-id: 48
status: CONSUMED
consumed-by: ADR-115
origin: integrator, 2026-08-24 batch close (nine-branch batch); surfaced by cloud lane C2's ruling-provenance audit
---

# Root `AGENTS.md`: a live register ruling and a ratified ADR say opposite things

## Problem / motivation

Two normative surfaces of this repo currently contradict each other on whether a root
`AGENTS.md` may exist, and **both are live**:

- **`protocols/STANDING_RULINGS.md` R-1** — *"`AGENTS.md` is ADMITTED, on the substance reading
  of ADR-53"* — reasons that *"ADR-53 Decision 2 forbids **two files that both carry content**,
  not the filename `AGENTS.md`."*
- **`docs/decisions/ADR-53` Decision 2** — *"**`AGENTS.md` as a separate per-repo file is
  retired.** Existing `AGENTS.md` files ... are to be removed and their content merged into each
  repo's `CLAUDE.md`."* ADR-53 is **`Status: Accepted`** and **un-superseded**.

Three things were measured at the batch close, and each makes this harder to leave alone:

1. **The phrase R-1 quotes is not in ADR-53.** `grep -ci "two files that both carry content"`
   over `ADR-53` returns **0**. The nearest sentence is in its Context and argues the other way:
   *"Two instruction files create ongoing divergence with no compensating benefit."*
2. **ADR-53 Decision 2 names the filename**, not a content-duplication condition, so the
   "substance reading" is a reinterpretation rather than a reading of the text.
3. **The admitted shape is materially the alternative ADR-53 declared moot.** ADR-53's Context
   records that *"ADR-52 Decision 5 explicitly reserved a Codex-only `AGENTS.md` model for a
   future ADR; that reservation is now moot."* R-1 admits a portable root `AGENTS.md` whose
   named consumer is Codex.

This is not a drafting nit. `scripts/validate_hermetization.py` **refuses** the add today
(*"unsanctioned new top-level file … a genuinely new class is an ADR-101 amendment, not a
drive-by add"*, verified live 2026-08-24), so `[#577]` cannot execute without either an ADR-101
amendment or a bypass — and the repo forbids the bypass.

## Scenarios (+1 view)

- An executor picks up `[#577]`, reads R-1, writes root `AGENTS.md`, and the pre-commit gate
  refuses the file. They must now decide whether to `--no-verify` past a ratified tree-seal or
  stop. Both are bad, and the contract that sent them offered no third option.
- A future reader greps `AGENTS.md`, finds ADR-53 Decision 2 (`Accepted`), and removes a root
  `AGENTS.md` that R-1 admitted — correctly, by the ADR.
- A consumer repo inherits the methodology floor and asks which file is canonical. There is no
  answer that cites one surface without contradicting the other.

## Functional requirements

- **Must:** exactly one live normative answer to "may a root `AGENTS.md` exist in this repo".
- **Must:** whichever way it resolves, the losing surface is explicitly retired or superseded —
  not left standing and silently outranked.
- **Should:** `[#577]`'s Done-when is re-written (see Open questions) before it is executed.
- **Could:** state whether the answer binds consumer repos or only the hub.

## Acceptance criteria (ex-ante)

1. A new ADR exists that **either** supersedes ADR-53 Decision 2 (and 3, which retires the
   template and the PLAYBOOK/ESSENTIALS references) **or** retires register ruling R-1.
2. `grep -n "AGENTS" protocols/STANDING_RULINGS.md docs/decisions/ADR-53*.md` yields no pair of
   live statements asserting opposite permissions.
3. If admission wins: `validate_hermetization.classify('AGENTS.md')` returns no refusal, via a
   recorded ADR-101 §1 amendment — never via `--no-verify`.
4. If retirement wins: `[#577]` is closed REFUSED with the reason recorded, and R-1 carries a
   terminal marker.

## Non-goals

- Deciding whether a portable instruction layer is a **good idea**. R-1's byte measurement
  (15,439 B = 47.1% of the Codex 32 KiB cap) already answers the feasibility question; this is
  purely about which of two live normative surfaces governs.
- Re-opening `.gemini/settings.json`, which R-1 explicitly does not admit.

## Impact sketch (4+1 lite)

- **Logical:** the ADR corpus and the ruling register are peers today with no precedence rule;
  this is the first measured case where they disagree outright.
- **Process:** an executor cannot resolve a ratified-ADR-vs-ruling conflict from their seat.
- **Development:** `[#577]` is blocked on the outcome; so is any `CLAUDE.md` §10 correction.
- **Physical:** one top-level file, plus an ADR-101 §1 amendment if admission wins.

## Open questions

- **`[#577]`'s Done-when is unexecutable as written — an architect item.** It requires
  *"`CLAUDE.md` §10's retired-AGENTS.md anti-pattern is corrected in the [same commit]"*, but
  §10 is a HUB-single-sourced Form-A region whose body must stay byte-identical to
  `templates/claude-regions/antipatterns-universal.md`. Correcting §10 alone breaks fleet
  parity; correcting the template is outside the row's stated scope. The row names neither the
  template nor the parity constraint, so it cannot be discharged as written.
- Does a recorded ruling ever outrank a ratified `Accepted` ADR, or is the register strictly
  subordinate? This case is the forcing example either way, and the answer generalizes well
  beyond `AGENTS.md`.
- If ADR-53 is superseded only in part, what is the status token for a partly-superseded ADR?
  `CONTRIBUTING.md` records `Partially superseded` as a legacy off-enum carve-out, not
  precedent.

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.

## Evidence note — 2026-08-25: the required provider-consumption matrix has landed

The measurement the C01 decision criterion was made conditional on is no longer owed. The
R-L report landed byte-identical this session at
`docs/audits/2026-08-25-technical-research-agents-md-standard.md` ("AGENTS.md and Native
Instruction-File Support Across AI Coding Agents: An ADR Input Report", compiled 2026-08-25),
and it carries the per-tool support matrix the criterion requires — one row per tool giving the
instruction file(s) read, a native-AGENTS.md yes/no, the discovery/precedence rule, and a dated
source.

**The criterion is MET per that report.** C01 set it as *"≥2 admitted providers natively
consume `AGENTS.md` and not `CLAUDE.md`"*. Read strictly against this fleet's six admitted
providers, the matrix gives: **OpenAI Codex** — AGENTS.md natively, CLAUDE.md not at all; and
**Cursor** — AGENTS.md natively (alongside `.cursor/rules/*.mdc`), CLAUDE.md not at all. That is
the two, with no configuration step. **Gemini CLI** is a third on a one-line
`context.fileName` setting (its default is `GEMINI.md`, never `CLAUDE.md`). The report's own
TL;DR reaches the same verdict on a wider roster. Recorded for completeness, because it cuts the
other way and the count should not be inflated: **Grok Build** reads the AGENTS.md family *and*
auto-reads `CLAUDE.md`/`.claude/rules/`, so it does not satisfy the "and not CLAUDE.md" leg —
nor do Copilot, Zed, opencode or Amp, each of which reads both. **Claude Code** is the lone
major holdout in the other direction: `CLAUDE.md` at runtime, no AGENTS.md (its `/init` can
*read* AGENTS.md to *generate* CLAUDE.md, which is not runtime consumption).

**Corroborating prior art:** `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`
("Multi-Provider Portability for AI Coding Agents on One Repository", 2026-08-09) carries an
independent, 16-days-earlier matrix — `| Tool | Reads AGENTS.md natively? | File(s) it reads /
precedence | Nested/subdir? |` — covering Codex, Gemini CLI, Copilot, Cursor, Claude Code, Aider
and Windsurf. It reaches the same structural finding from a separate research run: AGENTS.md
ports natively across the fleet and Claude Code is the exception. Two independent measurements,
16 days apart, agreeing.

**One honest gap, flagged not papered over.** The landed report's **DeepSeek** row records *"no
official first-party coding CLI/instruction convention"*. The operator correction of 2026-08-25
(verified at deepseek.com/harness, carried in the register ruling packet) supersedes that:
DeepSeek now ships DSH, a first-party developer-preview harness. DeepSeek's AGENTS.md
consumption is therefore **unmeasured**, exactly as the packet anticipated ("R-L did not cover
DSH"). This does not disturb the criterion — Codex and Cursor already satisfy it without
DeepSeek — but the DSH probe remains owed.

**What this note does NOT do.** It lands evidence only. The ADR act the criterion points toward
— supersede ADR-53 Decision 2 with C01's thin-file spec, and amend the ADR-101 hermetization
class in the same act so a root `AGENTS.md` is admissible — is **next window's ruling, not this
session's**. Status stays `READY`; no row is banked here, and the ADR-53-vs-R-1 precedence
question this intake exists to force is untouched and still open.
