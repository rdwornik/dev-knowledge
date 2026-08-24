---
intake-id: 34
status: DRAFT
origin: operator-held compass research artifact ("Enforcing a Universal Code-Style Doctrine Across an LLM-Written Python Fleet"), routed into intake by architect ruling of 2026-08-16 (phase-2 Stage-7 wrap addition iv); the source artifact itself is NOT yet in-repo and lands with the ratification
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

## Template conformance (prep pass, 2026-08-21 — batch-1 lane D)

Completeness pass against the protocol that governs intakes — `docs/intake/README.md` §2
(doc format), §3 (frontmatter schema), §4 (naming), §5 (lifecycle) — plus the fill-in
skeleton `templates/intake-template.md`. Section A is a **verbatim** quotation of an
operator-held artifact and is untouched; nothing above this heading changed.

- **Problem / motivation** — **ABSENT as a section**; carried by the `DRAFT BINDS NOTHING`
  preamble plus `## Provenance, stated exactly` and Section A's TL;DR.
- **Scenarios (+1 view)** — **ABSENT.** No operator walkthrough exists; this doc records a
  routed research input, not an elicitation. Not back-filled — §2 calls scenarios
  load-bearing and inventing them would manufacture authority the doc explicitly disclaims.
- **Functional requirements** — carried by `## Section B — the enforcement families the ruling
  names`, which is explicitly "the candidate scope, not a plan" (no must/should/could split).
- **Acceptance criteria (ex-ante)** — **ABSENT.** `## What ratification would have to settle`
  is the nearest section and is a **precondition list**, not measurable ex-ante criteria.
  This is the one absence that is load-bearing rather than cosmetic — see the blocker below.
- **Non-goals** — carried by `## Section C — scoping` ("not scoped to batch 6 and not to
  batch 7 by this file"; "no row is birthed here and none is proposed").
- **Impact sketch (4+1 lite)** — **ABSENT** in all four views.
- **Open questions** — **ABSENT as a section**; items 2–5 of "What ratification would have to
  settle" are open questions in substance.
- **Status** — added below.

**Frontmatter fix landed by this pass:** the empty `consumed-by:` key was removed — README §3
makes it CONSUMED-only and says to leave companion fields absent at any other status. (Same
template↔README conflict reported for intake #24: `templates/intake-template.md` seeds
`consumed-by:` with "leave blank until status: CONSUMED".)

**Naming (§4) — RECORDED DEVIATION, not repaired.** `2026-08-16-code-architecture-enforcement.md`
carries **no `{func|tech}` genre infix**, and §4's convention binds docs created after its
2026-07-08 ratification. Its own HTML comment declares `class: tech`, so the intended infix is
`tech`. Not renamed by this lane: a rename moves a file the intake generators are contracted
never to move, invalidates the path any other artifact cites, and is a structural act outside a
prep pass. Reported for the architect.

**Ratification blocker — why this doc was NOT transitioned by batch-1 lane D.** Item 1 of
"What ratification would have to settle" is *"Land the source artifact in-repo (it is the
evidence base and is currently operator-held)"*, and the frontmatter `origin:` says the
artifact *"lands with the ratification"*. That artifact is operator-held and not in this
repo, so a lane cannot satisfy the precondition; ratifying anyway would produce an ACCEPTED
standing authority whose own stated evidence base is absent. Item 5 (price the adoption per
ADR-112's two-tier bar) is likewise unpriced. Under the lane contract's "ambiguity →
prep-only + report" budget this doc is **prepped and left at DRAFT**.

## Status

**DRAFT** — routed into intake 2026-08-16 by architect ruling; prepped 2026-08-21 by batch-1
lane D and **deliberately not transitioned** (see the ratification blocker above). DRAFT BINDS
NOTHING; zero rows born, none proposed.

## Provenance correction — APPENDED 2026-08-23 (architect ruling R6). Status unchanged.

> **Appended, not edited.** Nothing above this heading changed. The frontmatter `origin:` field
> and the `## Provenance, stated exactly` section both assert that the source artifact is **not
> in the repo** and *"lands with the ratification"*. **That is false, and it was false when this
> intake was written.** The original sentences are deliberately **left visible**: they are the
> evidence for the funnel finding recorded below, and a silent fix would destroy the finding.
> Source: `RULINGS-and-AMENDMENTS-2026-08-23.md` **R6**, landed verbatim in
> `docs/audits/2026-08-23-technical-phase0-preconditions.md`; the identity evidence is that
> packet's **§6.1**.

**The source artifact IS in-repo.** Location:

```
docs/archive/2026-08-09-research-code-style-doctrine-wf-8a83eb70.md
```

**Three independent identity checks, each established by the Phase 0 packet §6.1:**

1. **Title.** The archive file's H1 —
   *"Enforcing a Universal Code-Style Doctrine Across an LLM-Written Python Fleet"* — matches the
   title quoted in this intake's `origin:` field **character-for-character**.
2. **Content.** Section A above reproduces that file's `## TL;DR` **exactly** — all three
   bullets, down to the em-dashes.
3. **Chronology.** The file was git-added at **`f571ac3c`, 2026-08-10** (*"docs(archive): land the
   six 2026-08-09 research memos byte-identical + index them"*) — **six days before this intake
   was routed** on 2026-08-16.

### Effect on the ratification checklist

- **Item 1 — "Land the source artifact in-repo" — DISCHARGED.** It was already discharged when
  this file was authored. The **"Ratification blocker"** recorded by the 2026-08-21 prep pass is
  therefore **void**: no lane was ever blocked on an unsatisfiable precondition.
- **Item 3 — "ratchet or flag day for ruff family enablement" — RULED: RATCHET.** Ruled by the
  architect on 2026-08-23 on standing precedent (the same shape ruled twice that day — R1's
  freshness leg and L2's coverage gate — plus the repo's established zero-baseline ratchet
  pattern, which this intake's own Section B already names via `silent_rule_ratchet`).
- **Items 2, 4 and 5 remain OPEN and are the operator's** — sequencing against `[#533]`, the
  hub-versus-consumer ownership boundary, and ADR-112 two-tier pricing. Three items remain, not
  four.

### Status: unchanged, and deliberately so

**`status:` stays `DRAFT`. No `decided-by` is added.** Discharging item 1 changes this intake's
**characterization**, not its status: from *"blocked, precondition unsatisfiable by any lane"* to
**"unblocked, awaiting an operator ratification decision on items 2, 4 and 5."** *The blocker is
discharged* and *ratification is ready* are different claims, and only the first is made here.
No lane owns `#34` and none should take it.

### Funnel finding (recorded, not fixed here)

An intake was authored **declaring a blocker that was already false at authoring time** — a
claim-at-authoring defect, the same family as the recorded architect error **E2**, and **not** a
workflow delay. Routed to the funnel per ADR-111; this appended block records it, and files
nothing.
