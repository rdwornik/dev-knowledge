---
intake-id: 33
status: DRAFT
origin: operator strategy dump at the close of the 2026-08-10/11 window, consolidated by the outgoing seat as docs/audits/2026-08-11-technical-batch-4-brief-next-architect.md §2; filed 2026-08-12 at the adjudication hour under BLOCK-4's packaging ruling
consumers: "the next window's batch — Section A produces the definition a backlog row then cites; Sections B and C produce their own ADR-or-carrier decisions"
---

> **Intake note:** Filed by ARC2 from night-2's E5c draft, **amended to BLOCK-4's packaging
> ruling**: night-2's one-document envelope with night-1's ownership map inside it, so nothing
> double-births. The base draft is `docs/audits/2026-08-12-technical-night-2-lessons-governance-strategy.md`
> §E5(c); the amendments are recorded in-section below rather than left as a diff to reconstruct.
> Ruling register: `protocols/STANDING_RULINGS.md` M-5 (`N2-D1-06/07/08/09`) and L-7.

# Consolidation — the repo's self-description: architecture freshness, docs taxonomy, and per-provider config

- **Class:** functional · **Date:** 2026-08-12
- **Provenance:** BRIEF §2 GAP-1 / GAP-2 / GAP-3, which states these are the only three themes in
  the operator's dump with no existing owner. Every other theme is mapped to an owner at BRIEF §1
  and is deliberately absent here (BRIEF §4 anti-goal: no re-derivation of anything §1 maps).

## Filing legality — the ceiling arithmetic, stated because it gated this document

The night-2 draft was **gated on `A1`** and said so: it stated both I-D6 readings, noted they
differ by 11, and declined to pick. `A1` was ruled at the 2026-08-12 adjudication hour —
**the working-set count reads DRAFT + READY; SEED sits outside it** (`STANDING_RULINGS` L-1).

Live at filing, after intake #10's REJECT relocated it to `archive/`: **DRAFT 2 · READY 1 = 3 of
6.** Filing this document takes the working set to **4 of 6** — within the ceiling, with room for
two more. The draft's own Q1 is therefore **answered rather than carried**, and is struck from the
open-questions list below.

## Problem / motivation

The repo describes itself in three places — `ARCHITECTURE.md` (what the system is), the `docs/`
folder layout (where knowledge lives), and the per-provider instruction files (how an agent is told
what to do here). All three descriptions drift from what they describe, and **none of the three has
a mechanism that notices.** They are filed as ONE intake because they are one theme: the repo's
self-description. The operator's own priority sentence — consolidate the methodology before
deploying it elsewhere — is what makes this the next intake rather than a later one.

## Scenarios (+1 view)

**S1.** As the operator I land a change that alters an organ's behaviour, `ARCHITECTURE.md` keeps
describing the old behaviour, and nothing tells me — the way **16 checkably-false claims**
accumulated under a current review stamp before an adversarial review found them.

**S2.** As the operator I look for where a piece of knowledge lives and read four folders to find
it, because the intake → ADR → backlog → audit chain is a convention rather than a navigable path,
and `docs/archive/`'s role is stated in two ADRs and understood by nobody.

**S3.** As the operator I add a second provider and hand-copy the instruction content, because the
`CLAUDE.md`-class files across providers share content with no carrier between them.

## Section A — GAP-1: an architecture-freshness mechanism

**WHAT:** a check that flags a commit touching an architecture-described surface when
`ARCHITECTURE.md` carries no matching delta and no explicit no-impact note.

**WHY NOW:** the 16-claim fix (`cf039756`) repaired the stock and built nothing that keeps it
repaired. I-D2 records the anti-rot METHOD — re-point a volatile cardinality at the surface that
computes it — and names its own expiry: *"retires when a mechanism computes these claims at stamp
time"*.

**LIBRARY-FIRST BAR:** extend `validate_doc_claims` / the doc-counts machinery, which already
reconciles prose claims against live state. A new organ family is out of scope by construction.

**THE HARD PART, stated ex-ante:** *"architecture-described surface"* has **no definition today**.
Inventing one inside a backlog row is how `[#356]` ended up citing a register that does not exist.
**This section's OUTPUT is the definition; the row comes after.**

**NON-GOAL:** gating. Advisory-before-hard is the standing pattern (`STANDING_RULINGS` B4).

### Amendment on filing — three orphaned obligations are routed here

BLOCK-4 routed into this section, rather than into new rows, three items that were left without an
owner. All three are definitional work whose natural home is the definition this section produces.

1. **`N1-D11` + `N1-S15d` — the commissioned ARCHITECTURE re-read arc and the G-7
   soft-observations scope.** The commissioned lane was W6 (`worktree-lane-f-arch-soft-obs`),
   **DROPPED at manifest amendment A-1 with no row id**. The 16-claim FIX landed separately at
   `cf039756`, but the commissioned **re-read arc** and the **G-7 scope** have had no lane, no row
   and no owner since. G-7 itself is defined — *the `cf039756` STEP-3 list plus I-D2, and nothing
   wider* — so what is missing is a consumer, not a definition. Routed here because **GAP-1's
   output IS the "architecture-described surface" definition the re-read arc needs**; a new row now
   would fight the under-100 target and the capacity law while still waiting on this section.
2. **`N2-E1-1` — the W-wave referent.** §B clause 1 ("W-wave landed") is **UNMEASURED and
   unmeasurable**: the birth set is not enumerable from the tree by any predicate a lane could
   find, and `grep -oE 'W-[0-9]+' BACKLOG.md` returns only `W-2`/`W-3` inside `[#294]`/`[#308]` as
   an unlocatable DEFER peg. An unmeasurable clause earns a **definition**, not a score. This
   section owns the ontology work already, so the referent is defined here.
3. **`N2-R2-07` — the `[#294]` / `[#308]` re-peg decision.** Both rows carry
   `DEFER — peg: the intake #25 W-wave carrier decision (W-2/W-3)`, and **that decision has no
   in-repo referent**. The rows stay deferred; the **re-peg decision is owed at this filing** and
   is therefore a Section A deliverable. It is the same question as item 2 from the other side, so
   answering the referent answers the peg. (Register `STANDING_RULINGS` L-7.)

## Section B — GAP-2: docs taxonomy, NARROWED to repairing a belief

**Narrowed on filing, and this is the substantive amendment to the night-2 draft.** Night-1
verified the three GAP claims negatively and reached a different result here: *"Of the three gaps,
one is a true gap (GAP-1), and two are partially or wholly falsified by existing owners."* Night-2
independently concluded that `docs/archive/` is already ruled. The two drafts agree on the fact and
differed only on packaging; BLOCK-4 took night-2's envelope with night-1's ownership map, so this
section's scope is **repairing the belief, not taking a decision**.

**`docs/archive/` IS ruled — stated up front so it is not re-litigated.** ADR-60 defines it as a
deliberate holding zone / triage queue; ADR-101 §1 Tier-2 lists it as sanctioned (confirmed in
code — `SANCTIONED_GENRES` contains it); and four external-research memos already live there under
exactly that convention. **The gap is that three landed sites assert no such clause exists.** It is
unclear in prose, not unruled in governance.

**`[#420]` IS THE OWNER, and it carries a live prohibition this section obeys.** Quoted verbatim
from `tasks/420-*.md`, which is `status: open` at filing:

> **Do NOT touch `docs/archive/` while this is open** — no move, no promotion, no deletion.

So Section B **proposes no move, promotion or deletion of `docs/archive/`**. Its deliverable on the
archive question is the belief repair: correct the three sites that assert no clause exists, and
cross-reference `[#420]` as owner. Anything beyond that is `[#420]`'s to rule, not this intake's.

**What remains genuinely open here** (the part night-1 did not falsify): backlog-as-folder
placement, and making the intake → ADR → backlog → audit chain navigable. ADR-101's tree seal means
a folder decision is costly to reverse, so that part is a real fork and is where an ADR would land.

**CONSTRAINTS the section carries:** `validate_hermetization`'s `SANCTIONED_TIER1_DIRS` and
`SANCTIONED_GENRES` are the checkable surface; every locator in every immutable audit is a cost of
any move; redirects are part of the deliverable, not an afterthought.

## Section C — GAP-3: per-provider config unification, as the un-park of W-9(a)

**Framed on filing as an UN-PARK, not a new theme.** BLOCK-4 routed GAP-3 as the un-park of
**W-9(a)** — the multi-provider portability scope note that already landed — with the **`AGENTS.md`
collision as the decision**. This does not fork W-9(a); it resumes it.

**WHAT:** one folder convention for `CLAUDE.md`-class files across providers (Claude / Codex /
Grok / Gemini), with byte-identical carriers where content is shared.

**THE DECISION IS THE `AGENTS.md` COLLISION.** `AGENTS.md` is retired here (ADR-53 — `CLAUDE.md` is
the single instruction file, and "narrating or managing AGENTS.md" is a named anti-pattern), while
it is the convention other providers read. That collision is what this section decides; everything
else in it follows from the answer.

**MEASURED, so the section does not start from a false premise:** `SANCTIONED_TIER1_DIRS`
**already contains `codex`**. A top-level `codex/` is therefore **not a new folder** and does not
touch the ADR-101 seal. If the outcome is carriers plus a manifest component, **no ADR is owed at
all**.

**NON-GOAL:** a monorepo migration (BRIEF §4 anti-goal, parked by the operator's own
consolidation-first sentence).

## The anti-goal clarification (`N2-E3-03`), stated in-text as ruled

The window's anti-goal reads *"no folder created outside the GAP-2 intake's ruling"*, and GAP-2 is
scheduled at BRIEF §3 item 2 — while **three things want a folder before then**: this intake
itself, GAP-3 work, and the archive-role question.

**Stated here so the anti-goal does not block work it was not aimed at:** the anti-goal targets
*unruled folder proliferation*, and it is satisfied by a folder this intake's own ruling authorizes.
It is not a freeze on all directory work until GAP-2 concludes. Two consequences follow directly:
`SANCTIONED_TIER1_DIRS` already containing `codex` means **Section C may need no new folder at
all**, and this document **creates none** (see A4 below).

## Functional requirements

<!-- Added by the prep pass, 2026-08-21 (batch-1 lane D). DERIVED from Sections A/B/C and the
     A1-A4 acceptance criteria already in this document — not new asks. Nothing below states a
     requirement the sections above do not already carry. -->

- **Must:**
  - **(A)** Produce a written definition of *"architecture-described surface"* that a grep can
    evaluate, and the architecture-freshness check Section A specifies — flagging a commit that
    touches such a surface when `ARCHITECTURE.md` carries no matching delta and no explicit
    no-impact note. Zero new organ families (A1).
  - **(B)** Repair the belief at the three sites that wrongly assert no `docs/archive/` clause
    exists, cross-referencing `[#420]` as owner and proposing **no** move, promotion or
    deletion while `[#420]` is open (A2 i).
  - **(C)** State, **before any file is authored**, whether Section C resolves as a carrier
    decision or as an ADR — and answer the `AGENTS.md` collision either way (A3).
  - Add **zero** new top-level directories on this document's own authority (A4).
- **Should:**
  - **(B)** For the genuinely-open folder question only, author one ADR at the fork it
    surfaces, with every relocated path carrying a redirect and every breaking
    immutable-artifact locator enumerated **before** any move (A2 ii).
  - **(A)** Discharge the three routed obligations the definition inherits — the `N1-D11`/G-7
    consumer, the `N2-E1-1` W-wave referent, and the `N2-R2-07` re-peg decision (A1).
- **Could:**
  - **(A)** Run the Section A check advisory-only in v1 — deliberately left open as **Q3**
    rather than asserted here.

## Acceptance criteria (ex-ante)

- **A1.** Section A produces a written definition of *"architecture-described surface"* that a grep
  can evaluate, plus **ONE** backlog row citing it. Zero new organ families. The definition also
  discharges the three routed obligations: the `N1-D11`/G-7 consumer, the `N2-E1-1` W-wave
  referent, and the `N2-R2-07` re-peg decision.
- **A2.** Section B produces (i) the belief repair at the three sites that wrongly assert no
  `docs/archive/` clause exists, with `[#420]` cross-referenced as owner and **no move, promotion
  or deletion proposed**; and (ii) for the genuinely-open folder question only, one ADR at the fork
  it surfaces, with every relocated path carrying a redirect and every breaking immutable-artifact
  locator enumerated BEFORE any move.
- **A3.** Section C produces either (i) a carrier decision needing no ADR, or (ii) an ADR — and
  states which of the two **before any file is authored**. The `AGENTS.md` collision is answered
  either way.
- **A4.** The whole document adds **ZERO new top-level directories on its own authority**.

## Non-goals

Monorepo migration · provider retirement · new orchestration machinery · any folder created outside
this intake's own ruling · moving, promoting or deleting anything under `docs/archive/` while
`[#420]` is open · re-deriving anything BRIEF §1 maps to an owner.

## Impact sketch (4+1 lite)

**Logical:** the self-description surfaces. **Process:** one intake → 1..2 ADRs → one batch.
**Development:** `validate_doc_claims` (A), `validate_hermetization` + every locator (B), the
deploy manifest (C). **Physical:** none.

## Open questions

- **Q1 — STRUCK, answered before filing.** *"Which I-D6 reading governs the working-set count?"*
  Ruled DRAFT+READY at the 2026-08-12 adjudication hour (`STANDING_RULINGS` L-1); the arithmetic is
  at the top of this document. Retained as a struck line rather than deleted, so a reader of the
  night-2 draft can see it was answered rather than dropped.
- **Q2.** Does Section B's ADR precede or follow the doc-moves? (ADR-98 §3 says the ADR is authored
  at the fork; the moves are the consequence.)
- **Q3.** Is Section A's check advisory-only in v1, per B4?

## Births

**ZERO at filing** (capacity law). Section A's single row is born from the definition this intake
produces, not from this filing.

## Status

**DRAFT** — filed 2026-08-12 at the adjudication hour under BLOCK-4's packaging ruling; prepped
for ratification 2026-08-21 by batch-1 lane D. Zero rows born at filing (A4 / Births above).

## Template conformance (prep pass, 2026-08-21 — batch-1 lane D)

Completeness pass against `docs/intake/README.md` §2–§5 and `templates/intake-template.md`.
Two of the eight template sections were missing and are now present: **Functional
requirements** (added above the acceptance criteria, derived from Sections A/B/C and A1–A4 —
no new ask) and **Status** (added above). The other six were already present and conformant.
Frontmatter (§3) conformant — `consumers:` is an optional descriptive key ratified at the
[#398] deploy and is forward-looking, distinct from `consumed-by:`. Naming (§4) conformant:
`func` infix, origin date.
