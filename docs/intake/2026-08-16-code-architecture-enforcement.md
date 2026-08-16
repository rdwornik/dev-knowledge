---
intake-id: 34
status: DRAFT
origin: operator-held compass research artifact ("Enforcing a Universal Code-Style Doctrine Across an LLM-Written Python Fleet"), routed into intake by architect ruling of 2026-08-16 (phase-2 Stage-7 wrap addition iv); the source artifact itself is NOT yet in-repo and lands with the ratification
consumed-by:
---

# Fleet code-architecture enforcement doctrine

<!-- class: tech (fleet enforcement doctrine) · status: DRAFT — NOT ratified; DRAFT BINDS
NOTHING. Non-citable as doctrine until ratified; the repo wins on any conflict. -->
<!-- origin: operator-held compass artifact, routed by architect ruling 2026-08-16 -->

> **DRAFT BINDS NOTHING.** This file records a routed research input and scopes it as a
> NEXT-WINDOW arc candidate. It authorises no adoption, no dependency, no config change and
> no gate. Nothing below is doctrine until this intake is ratified.

## Provenance, stated exactly

The source is an **operator-held** research artifact titled *"Enforcing a Universal Code-Style
Doctrine Across an LLM-Written Python Fleet"*. It is **not in the repo today**, by ruling: it
**lands with the intake ratification**, not with this DRAFT. Section A below quotes its TL;DR
verbatim so this file carries the claim rather than a paraphrase of it — the off-repo-claim
convention (LESSONS 2026-08-03 (5): an off-repo claim carries a locator or is marked as
paraphrase). Everything outside Section A is this file's own framing and is marked as such.

## Section A — the source artifact's TL;DR, quoted VERBATIM

> ## TL;DR
> - **Mechanize almost everything, write down almost nothing.** For a 5–6 repo Python fleet written mostly by LLM agents, the enforceable core is a shared, versioned config package (ruff + a type checker) + count-based ratchets + import-linter contracts + a PostToolUse lint hook + a pre-dispatch prompt checker. The "philosophy" (OO vs functional) is mostly taste; the only enforceable slice is function/module size, complexity ceilings, naming rules, and import boundaries.
> - **Pick one paradigm doctrine and enforce only its measurable shell.** "Functional core, imperative shell" (from Cosmic Python) is the right written doctrine for your fleet; "Functional Programming in Scala" is a mismatch — the Python-native equivalents are *Effective Python*, *Fluent Python*, and Cosmic Python. Ousterhout's *A Philosophy of Software Design* is a better source-of-truth than *Clean Code* (whose short-function/comment rules are widely contested).
> - **Your existing "silent_rule_ratchet" is already best practice — extend it, don't refactor blindly.** Before any big refactor, run a churn-vs-complexity hotspot analysis; the evidence says big-bang rewrites usually fail and incremental "strangler fig" + opportunistic refactoring on hotspots is the safer, better-supported path. Only refactor where high churn meets high complexity.

## Section B — the enforcement families the ruling names (this file's framing)

Recorded as the candidate scope, not as a plan:

- **ruff complexity families** — `C901` (mccabe), `PLR0911/0912/0913/0915/0904/1702`. Attacks
  over-long, over-branched modules with rules already available in a linter the fleet pins.
- **xenon** — the hard ceiling. radon measures and reports; xenon exits non-zero on a threshold
  breach, which is the difference between a metric and a gate.
- **import-linter module boundaries** — named by the ruling as **the natural `[#533]` follow-on**.
  That link is the reason this DRAFT exists now rather than later: `[#533]` decomposes
  `scripts/audit.py` into `scripts/audit_checks/`, and a decomposed tree is the first tree in
  which import contracts are expressible at all. Boundaries cannot be enforced on a monolith.
- **Count-based ratchets** — the fleet already runs one (`silent_rule_ratchet`), and the source
  artifact names it as already-best-practice and says extend rather than rebuild.
- **PostToolUse lint hook** — the mechanism half of the repo's own standing doctrine that
  *instructions are requests, MECHANISMS are guarantees*.
- **Shared config package** — cross-repo consistency via a published, versioned config rather
  than copy-paste, which is the failure mode the fleet's carrier/parity machinery already fights.

## Section C — scoping

**NEXT-WINDOW arc candidate**, explicitly alongside:

- the closing campaign, and
- `[#412]`.

It is **not** scoped to batch 6 and **not** to batch 7 by this file. No row is birthed here and
none is proposed; the ratification decides whether any of Section B becomes work.

## What ratification would have to settle

Listed so the DRAFT is actionable rather than merely filed:

1. Land the source artifact in-repo (it is the evidence base and is currently operator-held).
2. Decide sequencing against `[#533]` — import-linter contracts are cheap after the
   decomposition and near-impossible before it.
3. Decide whether ruff family enablement is a ratchet (count-based, never-worse-than-today) or a
   flag day, given the fleet's existing ratchet precedent.
4. Decide the ownership boundary: which of these are hub-enforced versus per-consumer, given
   that enforcement organs are **not** homogeneous across the fleet by construction.
5. Price the adoption per ADR-112's two-tier bar (Tier L evaluates; Tier S tries and keeps or
   deletes).
