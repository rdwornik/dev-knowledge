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

## AMENDMENT — 2026-08-31: THE `.CLAUDE` GOVERNANCE MODEL — the umbrella this intake was one leg of

> **Source:** operator direction, stated mid-flight during the batch-E derivation pass of
> 2026-08-31, filed under this batch's binding rule — *reconcile-before-birth: amend existing
> leaf/row/intake, birth only proven gaps*. **Zero new folders**, zero new intakes, zero new rows.
> This amendment records direction and a shape; **it still binds nothing**, because this intake is
> `status: DRAFT` and DRAFT BINDS NOTHING. Question 1 remains the operator's ruling to make.

### What changed: this intake is a LEG, not the whole subject

Four objects have been filed and worked separately, and the operator's direction names them as one
umbrella — **the `.CLAUDE` GOVERNANCE MODEL**:

- **this intake (#62)** — L0 as a governed layer;
- **the commands + skills census (4b)** — see the amendment to open question 2 below;
- **the prompt distiller** — 4a / `[#617]` (FILE DISTILLATION, the output half) / batch-E item DM-5;
- **the floor carrier** — `templates/child-methodology-floor.md.tmpl`, its `.sha256` sidecar,
  `.claude/CLAUDE-FLOOR.md` and the `check_floor_hash.py` SessionStart guard.

Filing them as one umbrella is the substantive act: each was individually unresolvable because
each answered a different third of the same ownership question.

### The three layers, as directed

1. **L0 (`~/.claude`) — DERIVED FROM HUB, plus an agreement check.** Not hand-owned. The drift
   organ is the shape `[#592]` built and `[#613]` reuses, not a rival invention. This is exactly
   the target shape this intake's Problem section already records; the amendment adds that L0 is
   **derived**, which sharpens Acceptance criterion 2's "hub-authored and derived" class from one
   option among three into the directed answer for this layer — *subject to question 1*, which
   core-invariant #6 still gates and which this amendment does not self-rule.
2. **Hub `.claude` — CANONICAL**, carrying a **usage-ranked, deduplicated census** of commands and
   skills, and that census must include **Anthropic-shipped organs**, which sit outside every
   census the repo currently runs.
3. **Consumer `.claude` — the DEPLOYED FLOOR plus local skills, each with PROVENANCE.** A consumer
   skill is either floor-carried or locally-authored, and which one it is must be readable from
   the artifact rather than inferred.

### The admission gate — new, and the sharpest clause

**Any skill or command is admitted only through an evaluation loop** (Harbor / SkillsBench-class).
**LLM-authored skills without an eval are REFUSED BY RULE**, on the SkillsBench finding that they
contribute approximately **zero percentage points**. This couples the umbrella to batch E's
**DM-1 (EVAL)** and to the north-star arc **THE METRIC**, which is RANK 1 precisely because
"every absent property is downstream of a measurement that does not yet exist". The admission gate
is a *consumer* of that metric, so it inherits the metric's ordering: **an admission gate built
before the harness that scores it would be a gate with nothing to read.** Stated here so the
sequence is on the record rather than rediscovered.

### The bidirectional distiller hangs off this umbrella

Two directions, one object: **intent -> tool-plan** and **files -> cheap representations**. This
is the `[#617]` / DM-5 leg, and its filing amendment (eval-loop as a PRECONDITION) is the same
clause as the admission gate above, reached from the other side.

### Deployment sequence — the HERMETIZATION arc order

**batch E -> engine ratification -> win-tooling full cycle -> monorepo -> ai-council.**

Recorded in `ecosystem/north-star.md` via the DEPLOYMENT WAVE arc declaration in
`scripts/gen_north_star.py` — north-star is generated, and the arcs are declared there.

**A CONFLICT IS NAMED RATHER THAN RESOLVED HERE.** The batch-E brief's DC-1 records a ruled
deployment order of **hub -> monorepo -> ai-council -> win-tooling** for the VISION -> README
migration carrier. This amendment's order puts **win-tooling FIRST**, not last. The two orders
carry different payloads and may both be correct, but running two fleet orders inside one batch is
a coordination hazard. **Both are recorded, labelled by payload; neither is overridden.** The
choice is the architect's cut, not the filer's.

> **RULED 2026-08-31 — batch E CUT-1. The paragraph above is SUPERSEDED, and the conflict it
> names is DISSOLVED rather than adjudicated.** The two sequences were never rivals: they address
> **instantiation order** and **migration order**, which are different things.
>
> - **MIGRATION order (ruled):** `hub -> monorepo -> ai-council -> win-tooling` — the order the
>   consolidated-doctrine corpus ships in.
> - **INSTANTIATION order (unchanged, and AFFIRMED):** win-tooling is the **FIRST instantiated
>   consumer**. The floor stays. DC-5 instantiates ai-council **from win-tooling's template**,
>   which is why that lane exists at all.
>
> So win-tooling is **first instantiated and last migrated** — most mature, therefore best able to
> wait, and the member where a mid-re-genre ship would cost the most. The original paragraph is
> left standing above rather than rewritten, because what it recorded (two sequences on the
> record, unresolved at filing time) was true when written. Full ruling:
> `docs/audits/2026-08-31-technical-batche-launch-contracts/CUT.md` CUT-1.

### Amendment to OPEN QUESTION 2 — the 4b census is now DECLARED, not merely unlocatable

Open question 2 records that the 4b commands+skills census, and its claimed finding
*"Anthropic-shipped organs sit outside every census"*, were **UNLOCATABLE** — zero grep hits, zero
`git log -S` commits. **That finding stands: nothing has been located.** What has changed is its
standing. The operator has now **stated the census as a required component of the umbrella**, so
the item is no longer a citation that cannot be resolved — it is a **requirement that has not yet
been built**. The distinction is the whole point of the funnel: an unlocatable citation is a
defect in the record; a declared requirement is work. Recorded as the latter, from 2026-08-31.

**No backlog row is born here**, on this intake's own stated precedent — its carrier row is
deliberately unborn, and the path from a CANDIDATE runs through intake and ratification (ADR-98,
ADR-111). Birthing the census row ahead of ratification would be the exact move both ADRs forbid.

### What this amendment does NOT do

- **No edit to any `~/.claude` path**, and no authorisation of one. Core-invariant #6 stands.
- **No supersession** of any ruling, and no answer to open questions 1, 3 or 4.
- **No new folder, no new intake, no new row.**
- **No status change** — this intake stays `DRAFT`, and DRAFT BINDS NOTHING.

## AMENDMENT — 2026-09-01: the OBSERVABLE HARNESS, and the distiller trace as the EVAL CORPUS

> **Source:** operator direction, 2026-09-01, filed under the same binding rule the 2026-08-31
> amendment ran under — *reconcile-before-birth: amend existing leaf/row/intake, birth only proven
> gaps*. **Zero new folders, zero new rows.** One new intake (**#66**) was born, for the one leg
> nothing carried. This amendment **still binds nothing**: this intake is `status: DRAFT`, and
> DRAFT BINDS NOTHING. Question 1 remains the operator's ruling to make.

### The coupling this amendment exists to record

The 2026-08-31 amendment established the **admission gate**: any skill or command is admitted only
through an evaluation loop, and **LLM-authored skills without an eval are REFUSED BY RULE**. It
also established the ordering — the gate **consumes** the metric, so a gate built before its
scoring harness has nothing to read.

**What was never said is where the eval's corpus comes from.** The 2026-09-01 direction closes
that: the **prompt-distiller trace doubles as the eval corpus for the skills gate.** One artifact,
two consumers — the distiller records `intent -> final prompt` plus the chosen
skills/commands/model/substrate **and the reason**, and that record is exactly the labelled input
an eval loop needs in order to score whether a skill earned its invocation.

This is **not** a new requirement on this intake. It is the missing edge between two clauses it
already carries — the admission gate above, and the bidirectional distiller (the `[#617]` / DM-5
leg, recorded here as *"the same clause as the admission gate, reached from the other side"*). The
two sides now meet at a named artifact instead of at a description.

**Consequence for the ordering, stated so it is not rediscovered.** The 2026-08-31 amendment ruled
the admission gate downstream of THE METRIC. The corpus is downstream of the **trace**, and the
trace does not exist yet — it has no home until intake #66's TRACE layer is ruled. The sequence is
therefore **trace -> corpus -> eval loop -> admission gate**, which puts the gate **two** organs
away from buildable rather than one. Recorded as an ordering fact, not as a new blocker.

### The harness is this umbrella's OBSERVABILITY half — and it is a SIBLING, not a leg

The 2026-09-01 direction names four layers with one home each (MECHANISM `scripts/` · DOCTRINE
`protocols/` · TRACE `logs/` · VIEW `dashboard/`). The reconcile pass moved five of its seven legs
onto existing carriers and birthed **intake #66** for the remainder — the layering rule itself, and
the **DOCTRINE layer**, which nothing in the repo carries.

**#66 is filed as a sibling of this intake rather than as another leg of it.** The reason is worth
one line: this umbrella is about **ownership** — who authors what across L0 / hub / consumer. The
harness is about **placement** — which of four layers an observing organ belongs to. They meet at
exactly one point, the corpus coupling above, and folding either into the other would have made
both harder to rule.

**One fork is shared and both files say so.** #66's open question 4 and this intake's open
question 4 are the same question — *where does a hub-side authority live, `protocols/` or
`ecosystem/`* — and `[#613]` is parked on it too. Three sites, one decision; it should be made
**once**.

### What this amendment does NOT do

- **No edit to any `~/.claude` path**, and no authorisation of one. Core-invariant #6 stands.
- **No supersession** of any ruling, and no answer to open questions 1, 3 or 4.
- **No new folder, no new row.** One new intake (#66), for a proven gap, per ADR-98/ADR-111.
- **No status change** — this intake stays `DRAFT`, and DRAFT BINDS NOTHING.
