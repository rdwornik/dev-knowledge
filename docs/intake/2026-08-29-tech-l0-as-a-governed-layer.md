---
intake-id: 62
status: DRAFT
origin: operator direction, stated mid-flight during the 2026-08-29 reconcile-and-file pass (item C9 of that pass's brief); filed by the `pn-filings` batch lane under ADR-111's only path from a CANDIDATE
consumed-by:
---

# L0 is a governed layer, not a place the hub cannot see

<!-- class: tech (governance-boundary question) · status: DRAFT — NOT ratified; DRAFT BINDS
NOTHING. Non-citable as doctrine until ratified; the repo wins on any conflict. -->
<!-- origin: operator direction, 2026-08-29 -->

> **DRAFT BINDS NOTHING.** This file records operator direction and the ruling-level question it
> raises. It authorises no edit to any `~/.claude` path, no change to core-invariant #6, and no
> supersession of any prior ruling. Nothing below is doctrine until this intake is ratified.

## Problem / motivation

The global `~/.claude` layer (skills, commands, settings, hooks) and each repo's `.claude/` layer
are where a large share of the fleet's live behaviour actually is — and the hub treats them as
*outside*. Core-invariant #6 makes global-infra a class the hub may neither hold nor edit;
`[#370]` ruled in 2026-07-28 that a **third ownership state exists, `owner=user`**, and left its
own follow-up open: *what `owner=user` GOVERNS vs merely CONTAINS*. The consequence is a boundary
that is stated but not modelled — the hub authors doctrine that L0 is expected to obey, and has
no surface that says what L0 should contain, no way to detect when it drifts from that, and no
carrier that would ship a per-repo skill the way every other organ ships.

The operator's direction of 2026-08-29 states the target shape: **both layers are governed
surfaces of the graph** — hub-authored, **derived** to L0 and never hand-owned there,
drift-guarded by agreement checks shaped like `[#613]`/`[#592]`, with per-repo skills shipping via
deploy carriers like any other organ.

If this stays unaddressed, the boundary keeps producing the same two symptoms it already has:
rows whose target is L0 and which therefore cannot state a done-when the hub can verify
(`[#130]`'s `MEMORY.md` cap arm is the live instance, amended 2026-08-29 with a measured
truncation), and rulings that terminate at the boundary rather than crossing it (`[#613]` had to
place the AUTHORITATIVE routing table in-repo precisely because *a table the hub cannot read is a
table the hub cannot gate*).

## Scenarios (+1 view)

- As the architect, I ask what the global `~/.claude` layer is *supposed* to contain, and read a
  hub-side declaration rather than reconstructing it from whatever is on one operator's disk.
- As a gate, I compare the derived L0 copy against its hub-side authority and FAIL on divergence —
  the shape `[#592]` built and `[#613]` reuses, applied to skills, commands, settings and hooks
  rather than only to a routing table.
- As a consumer repo being onboarded, I receive my `.claude/` skills through a deploy carrier,
  versioned and prunable, instead of by hand-copy.
- As the operator, I keep a hand-owned exception where I actually want one, and it is **declared**
  as an exception rather than being indistinguishable from drift.

## Functional requirements

- **Must:** state what the hub authors for L0 and what L0 owns for itself — the `owner=hub` /
  `owner=repo` / `owner=user` split applied to the `.claude` layers specifically, which is
  `[#370]`'s explicitly-open follow-up.
- **Must:** name the agreement-check shape (`[#592]`/`[#613]`) as the drift organ rather than
  inventing a rival, and say what it reads on each side.
- **Should:** route per-repo `.claude/skills/` through the deploy carrier mechanism that already
  ships every other organ class.
- **Could:** carry L0 as a first-class **layer** in the typed multi-layer graph of intake **#40**,
  with cross-layer edges to the repos that consume it. That is #40's scope, cross-referenced here
  rather than duplicated.

## Acceptance criteria (ex-ante)

1. A ruling records whether the hub may **author** (not merely describe) content that is derived
   into `~/.claude`, and if so under what act — because core-invariant #6 currently forbids it and
   this intake does not assume the answer.
2. For each of skills / commands / settings / hooks, the ruling names one of: hub-authored and
   derived · hub-described and L0-owned · out of scope — with no class left unassigned.
3. If any class is hub-authored, an agreement check exists for it and FAILs on divergence, and a
   fire-test proves it REDs on a planted divergence.
4. `[#370]`'s open follow-up (`owner=user` governs vs contains) resolves to a recorded answer or
   is explicitly re-pegged with its reason.

## Non-goals

- **No edit to any `~/.claude` path is proposed or authorised here.** Filing a question about a
  boundary is not crossing it.
- Not a re-litigation of `[#613]`'s in-repo routing table, which is already ruled (Z-G3 / A2) and
  blocked only on the operator's path selection.
- Not the graph build itself — that is intake #40.

## Impact sketch (4+1 lite)

- **Logical:** adds L0 to the ownership model as a governed layer rather than an excluded one.
- **Process:** every L0-targeting backlog row currently has to state an unverifiable done-when;
  this is the decision that would change that.
- **Development:** unknown until the ruling lands — a declaration surface plus N agreement checks,
  each the shape `[#592]` already built.
- **Physical:** possibly one new hub-side declaration file; no new dependency.

## Open questions

1. **Does the ruling that `~/.claude/memory/learned-rules.md` is outside hub scope need
   superseding?** The operator's direction says it **may**. This intake **does not self-declare
   the supersession** — it is a ruling-level question and is recorded as one.

   **The cited ruling is UNLOCATABLE as quoted, and that is stated rather than papered over.** The
   brief carrying this item cited a TO-NEXT note declaring `learned-rules.md` *"outside hub
   scope"*. Searched: `grep -r "outside hub scope"` over the tree returns **zero hits**;
   `git log -S "outside hub scope" --all` returns **zero commits**; `TO-NEXT` resolves only to
   `TO-NEXT-ARCHITECT-2026-08-28`, which `docs/audits/2026-08-29-technical-nb2-intake61-ratification.md`
   already records as resolving **nowhere in the tree** and as operator-side.

   **What DOES exist, quoted exactly, is a near neighbour and not the same thing.**
   `docs/audits/2026-08-28-technical-closure-harvest-k4.md` §5 records as ADR-111 CANDIDATE 1:
   *"The global `~/.claude/memory/` protocol gap. The global CLAUDE.md Self-Evolution Protocol step
   1 directs a read of `~/.claude/memory/learned-rules.md`, which **does not exist** … **L0,
   outside this repo's write scope** — the hub cannot discharge it (Layer-2 invariant)."* That is a
   **scope statement about a write**, recorded as a CANDIDATE, not a ruling that the subject is
   outside hub *governance*. Whether it is the thing the operator means, and whether it needs
   superseding, is the operator's to say.

2. **The 4b commands+skills census whose finding is cited as this item's evidence is
   UNLOCATABLE.** The claimed finding — *"Anthropic-shipped organs sit outside every census"* — was
   searched for as an exact phrase and by subject: `grep -ri "Anthropic-shipped"` over the whole
   tree returns **zero hits**, `git log -S "Anthropic-shipped" --all` returns **zero commits**, and
   every `### 4b` section in `docs/` is about a different subject (audit-file templates,
   question-shaped rows, Arm-1 deltas, window batches, an ambiguity budget). The **nearest live
   evidence**, offered as a substitute rather than as the citation: `[#132]`'s organ-index
   generator walks `.claude/{agents,commands,skills,workflows,rules}` plus the hook config and
   `ecosystem/organ-registry.yaml` — a repo-scoped inventory with no L0 arm — and
   `docs/audits/2026-08-25-technical-harvest-v-consolidation.md` U-8 records the routing table as
   sitting *"outside the repo"* with the boundary itself an **open operator decision** (R-2). The
   census claim is recorded as **unlocatable**, never as **unruled**.
3. **Does admitting L0 as a governed layer require amending core-invariant #6, or is "hub authors,
   L0 derives" already compatible with it?** The invariant forbids the hub *editing* global infra;
   a derived copy written by a deploy act on the operator's own machine may or may not be the same
   act. Not answered here.
4. **What is the hub-side authority's home** — `ecosystem/` beside the machine-read registries, or
   `protocols/` beside the doctrine? This is the same fork `[#613]` is blocked on, and the two
   should be decided together rather than twice.

## Status

DRAFT — filed 2026-08-29 from operator direction, by the `pn-filings` filing lane. **Its carrier
row is deliberately unborn**, on intake #40's precedent in this same tree: the path from a
CANDIDATE runs through intake and ratification, and question 1 is a ruling the operator owns.
Awaiting operator ruling on question 1 and technical-architect triage on the rest.
