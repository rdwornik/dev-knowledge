# Article research brief — "The Harness Needs a Substrate" (landed research artifact)

- **Class:** technical · **Date:** 2026-09-01 · **Genre:** landed research artifact
- **Provenance:** **operator-commissioned article brief.** The article itself lives **outside the hub**.
- **Source:** `demo-prep@9066345` — `docs/audits/2026-09-01_brief_article-harness-substrate.md`,
  branch `docs/article-research`, **unpushed** (no upstream configured)
- **Body author:** Claude Code, research + synthesis pass (demo-prep seat) · **§0 author:** CC (hub landing seat)
- **Landed on:** `worktree-land-article-substrate-brief`, from `16f91f69`

> **§0 IS THE ONLY HUB-AUTHORED CONTENT IN THIS FILE.** It records why the brief is here, what
> consumes it, what it still owes, and where the landing instruction's own premises did not survive
> being resolved. Everything below the rule that closes §0.7 is the landed brief, **unmodified —
> including the parts §0 corrects.** An artifact is corrected by a record beside it, never by a hand
> inside it.
>
> **The sole transformation is CRLF→LF**, forced by this repo's `.gitattributes` (`* text=auto eol=lf`);
> the source was authored 100% CRLF. Content is otherwise identical, and both hashes are recorded so
> the equivalence is checkable rather than asserted:
>
> ```
> source, as authored (CRLF)   50,369 B   sha256 780653fe90cdad580254a834b3526811504e56f86fb1c9aea4abd80b3954cfa3
> body, as landed (LF)         49,627 B   sha256 e707b3ff5ec3cd386002f20a2b6c8a0a4cea35c6acf5a0907e0ec07b81bd6eec
> ```
>
> **Formatting in §0 is flat by design** — no pipe tables — so it copies into browser chat without the
> TUI painting border glyphs (`CLAUDE.md` §4, output-formatting; same posture as the batch-F derivation).
> The body below keeps its own tables, because it is landed unmodified.

---

## 0 · LANDING RECORD

### 0.1 Why it is here, and what it is not

The brief is the **research substrate for one article** — argument, evidence, counter-argument, an
explicit cost model, chart specifications. It is not the article and it does not choose a venue.

It is landed in the hub because **three hub surfaces consume it** (§0.2). Its own §9 records the
constraints it was written under, including **`FREEZE · no push`**, which this landing honours (§0.7).

**A note on the home, so it is not re-litigated.** The standing precedent is that an *external research
memo* goes to `docs/archive/` (ADR-60's pending-classification zone; ADR-101 §1 Tier-2; the 2026-08-09
class precedent), because ADR-101 Rule B's class enum is scoped to `docs/audits/*.md` and **no enum
class describes a research memo**. This artifact lands in `docs/audits/` on **operator instruction**,
and the instruction is defensible on its own terms: this is not a third-party memo but an
**operator-commissioned internal work product** that three in-repo surfaces consume, which is the
`audits/`-class shape the archive precedent itself carves out ("a *distillate about* the memo is the
`audits/`-class artifact"). The class token is `technical` because `research` is not in
`AUDIT_CLASS_ENUM`. Recorded so a future session finds the reasoning rather than the discrepancy.

### 0.2 Consumed by — recorded at landing (Z-G1: no births unless a gap)

Four locators, each resolved before being written. **Three of the landing instruction's premises did
not survive that resolution**; the corrections are stated inline and consolidated at §0.6.

**(a) The orchestration rejection — `§3.6` absorbable/institutional table**

```
record (immutable)  docs/audits/2026-08-31-technical-langgraph-class-rejection-record.md
frozen contract     docs/audits/2026-08-31-technical-batche-launch-contracts/
                      LANE-batch-e-a6-langgraph-class-rejection-record.md
arc context         docs/audits/2026-08-29-technical-autonomy-synthesis.md (class routing, L465-474)
                    docs/audits/2026-08-30-technical-autonomy-decision-tree.md
```

**CORRECTION — "A6" is not an AUTONOMY-arc item.** It is a **lane id in batch E's "A" (cloud,
read-only) dispatch group** (`docs/audits/2026-08-31-technical-batche-launch-contracts/PLAN.md`, whose
roster line reads `A6  batch-e-a6-langgraph-class-rejection-record`, and which adds that *"A5, A6 and A7
record CLOUD as a parallelism choice, not a sizing verdict."*). The autonomy arc supplies the class
routing; the rejection itself is a batch-E artifact. Both are cited above so the pointer resolves either
way.

**CORRECTION — §3.6 does not *support* the recorded rejection. It reaches the same verdict by a route
the record does not use, which is a stronger thing and must not be reported as the weaker one.** The
record's stated reasons are five, and **none of them is transience**:

```
R1  wrong layer / wrong substrate (primary) -- "A lane's state IS its branch."
R2  the Layer-2 invariant is constitutional, not a preference (CLAUDE.md 5.4 / ADR-28 / ADR-36):
    "An orchestration framework is by definition an executor."
R3  dependency-closure cost (35 packages for langgraph, 103 for pydantic-ai)
R4  release churn against a pinned environment
R5  two sources of truth for lane state
```

The record further fences what its reason is **not** — *"NOT installability … NOT library health …
NOT the '40-50% cost reduction' figure … NOT AutoGen's maintenance stall."*

What §3.6 adds is an **independent sixth reason**: its absorbable/institutional table sorts
`Orchestration / workflow scaffolding` as **"Absorbable by a better model? Yes — largely → Concede
outright,"** on the Bitter-Lesson route (§3.5). Two unrelated arguments arriving at one verdict is
convergent corroboration, and it matters **because the record carries a `5. REOPENING TRIGGERS`
section**: a reason the record does not hold cannot be assumed to survive a trigger that weakens R1/R2.
§3.6 would survive it. **Recorded here, not folded in** — the record is immutable (CLAUDE.md §5 rule 3).

**(b) `§3.7` semantic-vs-context — it names what FUNNEL HEALTH and the north-star already are**

Sassoon's distinction, from the brief: a **semantic layer** answers *"what does this data mean?"* —
consistent, retrospective definitions; a **context layer** answers *"what does this agent need to know
to act well, here, now?"* Resolved against the live surfaces, the hub already built both halves without
the vocabulary:

```
SEMANTIC LAYER   protocols/FUNNEL_LIFECYCLE.md
                 "the governed-object state machine, written once" -- what a state MEANS,
                 defined once and consistently, independent of any one window

CONTEXT LAYER    FUNNEL HEALTH -- declared scripts/gen_handoff.py (FM-4 block),
                 derived by scripts/funnel_lifecycle.py::measure, rendered per bundle
                 (e.g. docs/handoffs/2026-08-31-dev-knowledge-architect/FUNNEL_HEALTH.md)
                 "so the seat that boots a window can see the funnel's state without asking"
                 -- assembled at cut time, for a decision, now
```

That is Sassoon's pair exactly: FUNNEL_LIFECYCLE defines the meaning; FUNNEL HEALTH assembles the
present. FM-4's own rule — *"Numbers ONLY: no verdict… 'funnel healthy' is a claim the reader cannot
check; 'leg a1 intakes terminal-unarchived: 7' is one they can"* — is the same discipline the brief
demands of the article's own figures.

**CORRECTION — the north-star does not map cleanly, and "the north-star" is not one object.**
`ecosystem/north-star.md` (generated by `scripts/gen_north_star.py`) is a **hybrid**: its *order* is
architect-declared and forward-looking, its *counts* are derived present-tense. Its retrospective twin
is a different surface — the HY-4 burn-down panel in `scripts/gen_trend_dashboard.py`, whose stated
purpose is *"a table shows VALUES, and a value cannot tell you whether the repo is getting better…
WHICH WAY IS IT GOING."* And `docs/audits/2026-08-21-technical-north-star-position.md` **rules** that
*"There is no single North Star statement. There are two, at two scopes, and one is nearer."* So the
mapping above holds for the **arc-sequence view only**, and that caveat travels with it.

**The line that earns this section's place in the hub**, from §3.7:

> *"No amount of consistent definition conjures data that was never recorded."*

It lands squarely on the three **ABSENT** series the observability surfaces already declare (§0.2(d)) —
and on the candidate at §0.5.

**(c) `[#617]` file distillation — `§4.5`, the cost driver is re-read context, `ρ × (1 − 0.9h)`**

```
row      tasks/617-file-distillation-the-output-half-and-the-only-w.md   status: open, P2/M
panel    "paste / boot bytes  WORSENING  +11232 bytes" -- the dashboard's ONLY worsening panel
series   scripts/gen_trend_dashboard.py, Series(key="paste_bytes", better="down")
store    protocols/HANDOFF_BOOT.md blob size per revision (32 revisions)
```

§4.5 supplies the external result that the dominant term in agent cost is **`ρ × (1 − 0.9h)`** — how
much context is re-read, and how well it caches — and that under pessimistic assumptions **input is 77%
of total cost**. Moving central→pessimistic multiplies output tokens 4.5× but effective **input** tokens
**26.5×**. That is independent evidence that **context supply, not generation, is the cost**, which is
the family `[#617]` chose to measure.

**CORRECTION — the fit is by family, not by quantity.** `[#617]`'s panel measures **boot bytes**: bytes
a seat reads *once*, before it can work. `ρ` prices **re-reads across a session**. Same family, different
quantity. So §4.5 corroborates the *choice* of metric family and gives `[#617]` an external warrant it
did not have; it supplies **no** evidence for the boot-bytes number itself, and the panel measures no `ρ`
and no `h`. **That gap is precisely what §0.5 exists for**, and it is why the candidate is not redundant
with this row.

**(d) The OBSERVABLE-HARNESS intake — log `h` and `ρ` per lane as telemetry**

**UNRESOLVED LOCATOR — declared, not silently written.** At this commit (`16f91f69`) **no
observable-harness intake exists in the tree**: `git grep` over tracked files returns zero hits and
`docs/intake/README.md` carries no entry. It exists only as an **untracked working-tree file inside the
live, `locked` worktree** `.claude/worktrees/observable-harness-filing`:

```
intended path   docs/intake/2026-09-01-tech-observable-harness.md
intake-id       66
status          DRAFT          consumed-by:   (empty)
title           "The OBSERVABLE HARNESS -- four layers, one home each, and the layer that
                 has no home at all"
banner          "DRAFT BINDS NOTHING."
```

So this leg is recorded as a **forward pointer, not a citation**: when intake #66 lands, its
`consumed-by:` should name this file, and the telemetry item at §0.5 is what it should carry.

**Measured, so the slot is known to be empty:** intake #66 names three **ABSENT** series —
`commit-gate ms` (store declared at `logs/TELEMETRY.db`, no rows), `suite wall-time` (no store),
`per-model quality` (no store). It names **no** cache-hit ratio, **no** token ratio, **no** re-read
volume. Nothing in it is displaced by §0.5.

### 0.3 MEASUREMENT-OWED — the brief's own verification debt, carried verbatim

The brief declares one unpaid debt against the **single strongest source that cuts against its own
thesis**. Reproduced verbatim from §3.5 and §6, and **it travels with the artifact**: it is not
discharged by landing, and this file must not be cited as if it were.

From **§3.5**, on Dennis, Diamond, Patil, Shabahang & Guo, *In-Context Prompting Obsoletes Agent
Orchestration for Procedural Tasks* (arXiv:2604.27891, 2026):

> **⚠ Verification debt:** I retrieved the arXiv paper's title, authors, claim and scope, but the fetch
> did not yield its measured results or sample sizes. **Read the PDF before citing it in print.** A
> saved copy is in the session tool-results directory. Citing a paper that cuts against you and getting
> its numbers wrong is the worst available outcome.

From **§6**, "Non-blocking but should be closed", item 4:

> **Read arXiv:2604.27891 properly** (§3.5). Its measured results and sample sizes are unretrieved, and
> it is the single strongest counter-source.

**Hub note on custody.** The "saved copy … in the session tool-results directory" is **not in this
repo and not in `demo-prep`** — it lived in the authoring session's scratch and must be assumed gone.
The debt is therefore **re-fetch, then read**, not "open the saved file." The brief's §9 lists the PDF
under `Disk-only`, which is consistent: it was never a tracked artifact.

**Two further owed verifications** ride the same status and are recorded so they are not lost (§4.3,
§6 items 5–6): the OpenAI/Google price comparison is **aggregator-sourced, not vendor-page-sourced**,
and the June 2025 Karpathy context-engineering definition is **second-hand through summaries** with no
primary link.

### 0.4 The REJECTED-figures ledger — landed as evidence-tier precedent

§3.8 grades every source A/B/C/D and then carries an explicit **REJECTED** row. That row is the reason
this artifact is worth landing as *precedent* and not only as *content*: it is a worked example of a
research pass **naming the numbers it refused to use, and why**, which is the same discipline
`validate_doc_rot`, FM-4's numbers-only rule, and the "never restate a count in prose" convention
enforce mechanically elsewhere in this repo.

Verbatim, the **REJECTED** row:

> **REJECTED** — "65% of enterprise AI failures trace to harness defects" — surfaced in search, **no
> primary source traced**. Also **MIT/NANDA "95% of pilots fail"** — not peer-reviewed, dataset
> unpublished, methodology publicly contested, and the real claim ("no P&L impact within ~6 months") is
> much narrower than the headline · **Do not use.** The 95% figure in particular is a credibility trap:
> it is exactly the statistic a sceptical reader will already know is contested

And §6's closing line, which is the precedent stated as a rule:

> **Deliberately not chased:** the MIT/NANDA 95% figure and the unsourced "65% harness defects" claim (§3.8).

**The tier ladder itself is the reusable half** — A institutional / B named practitioner / C interested
party, conflict disclosed / D trade press, directional only / REJECTED — together with §4.7's rule for
the D tier, **"A missing chart beats a fabricated one,"** and §5's standing constraint that **"None of
these may be drawn from invented data."** Cite this section when an artifact needs an evidence-grading
precedent; it is the first one in the corpus stated end-to-end with a refusal list attached.

### 0.5 CANDIDATE — "context-cost instrumentation"

**CANDIDATE only. No row is born, no intake is edited, no gate is touched.** Per ADR-111 / Z-G1 a raw
finding is not past triage, and the only route is CANDIDATE → intake (ADR-98) → ratification.

```
THE ITEM   Emit, per lane, the two parameters the brief's sensitivity analysis identifies as
           dominant: rho (input:output token ratio -- how much context is re-read) and h (cache
           hit fraction). The brief models them at rho=10 (range 5-30) and h=0.80 (0.50-0.95)
           and states rho is "the least defensible parameter and, per 4.5, the one that matters
           most." We do not emit either. They are measurable from local session data.

WHY NOW    Section 6 item 7 rates this the "highest-value optional work in the whole brief" and
           says the result would be, as far as its research found, NOVEL PUBLISHED DATA -- so
           the instrumentation pays twice: it retires the article's weakest parameter AND gives
           the hub a substrate metric it currently lacks.
```

**Three candidate homes were checked. None holds it.**

```
intake #50  docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md   status: READY
            EXCLUDED BY AN EXPLICIT NON-GOAL: "Per-request tracing or a cost-attribution model
            finer than per-project-per-week." Per-lane rho/h is finer than per-project-per-week.
            Its 2026-08-29 amendment is nonetheless adjacent and corroborating: it records that
            logs/TELEMETRY.db "does not exist and is gitignored" -- "a collection gap, and it is
            this intake's own subject."

[#617]      tasks/617-...md   status: open
            MEASURES A DIFFERENT QUANTITY -- boot bytes read once, not re-reads across a session
            (see 0.2(c)). Its Done-when is bound to the paste/boot panel specifically.

intake #66  OBSERVABLE HARNESS   status: DRAFT, untracked, in a locked worktree
            DOES NOT HOLD IT -- measured: no cache-hit, no token-ratio, no re-read metric among
            its three ABSENT series. It also "BINDS NOTHING" by its own banner, so it could not
            hold it even if it named it.
```

**A second, independent reason not to birth a row.** `BACKLOG.md` is already **over** the `[#589]`
byte bar — the batch-F derivation measures 70,276 B against a 70,000 B contract, **276 B over with a
live suite RED** — so filing any row widens an existing breach. Z-G1 and `[#589]` point the same way
here, which is a good sign the CANDIDATE disposition is right rather than merely convenient.

**Routing.** The natural destination is **intake #66 when it lands** (§0.2(d)) — its empty
cache-hit/token-ratio slot is exactly this shape — with **intake #50 as the fallback** if #66 is
abandoned, which would require #50 to widen its per-project-per-week non-goal by a recorded ruling
rather than in passing. **That routing is a recommendation to the operator, not a decision taken here.**

### 0.6 The three corrections, consolidated

Stated once more together, because a correction buried in a subsection is a correction nobody finds:

```
1.  "A6" is a BATCH-E CLOUD LANE ID, not an AUTONOMY-arc item. The rejection record is
    docs/audits/2026-08-31-technical-langgraph-class-rejection-record.md; the autonomy arc
    supplies class routing only.

2.  3.6 does not SUPPORT the recorded rejection -- it reaches the same verdict by a route
    (Bitter-Lesson transience) that the record does not use. The record's five reasons contain
    no transience argument. It is convergent corroboration and an independent SIXTH reason,
    which matters against the record's own REOPENING TRIGGERS.

3.  The north-star does not map cleanly onto Sassoon's semantic/context pair, and it is not
    one object -- 2026-08-21-technical-north-star-position.md rules there are TWO statements at
    two scopes. FUNNEL_LIFECYCLE.md / FUNNEL HEALTH map cleanly; ecosystem/north-star.md is a
    declared-order + derived-count hybrid whose retrospective twin is the HY-4 burn-down panel.
```

A fourth item is a state fact rather than a correction: **the OBSERVABLE-HARNESS intake does not exist
in this tree** (§0.2(d)), so its consumed-by is a declared forward pointer.

### 0.7 What this landing deliberately does NOT do

```
NO PUSH            The brief's own 9 ends "FREEZE . no push", the source branch
                   demo-prep/docs/article-research has no upstream, and this hub checkout was
                   found on docs/batch-f-freeze. Three independent freeze signals; the artifact
                   is committed to a branch and left for the operator to merge.

NO INDEX REGEN     docs/audits/README.md is left STALE ON PURPOSE. [#590] narrowed
                   audit-index-freshness to (README.md | gen_audit_index.py) on 2026-08-26
                   precisely so lanes stop colliding on it -- that one file was in 6 of the last
                   7 conflicted merges. The integrator regenerates ONCE on the merged result
                   (git add first: the index reads tracked files only). OWED, and named here so
                   it is not invisible.

NO ROW BORN        0.5 is a CANDIDATE under Z-G1 / ADR-111, reinforced by [#589]'s negative
                   byte headroom.

NO EDIT TO #66     Intake #66 is untracked in another lane's LOCKED worktree. Writing into it
                   would cross a live lane boundary.

NO EDIT TO THE     The langgraph-class rejection record and this brief body are immutable
IMMUTABLES         (CLAUDE.md 5 rule 3). Every correction above is recorded BESIDE them.

NO BODY EDIT       The brief is landed unmodified -- including its 3.5 verification debt, its
                   REJECTED ledger, and the premises 0.6 corrects. Hashes at the top make that
                   checkable.
```

### 0.8 AMENDMENT (same session, post-landing) — §0.2(d)'s unresolved locator RESOLVED

> **Appended, not edited.** §0.2(d) stands exactly as written: it was accurate at `16f91f69`, the
> commit this artifact was authored against, and an artifact is corrected beside itself rather
> than inside itself — the rule §0.2(a) applies to the rejection record applies here too.

**What changed, and when.** Between this artifact's commit (`95e36f61`) and its journal anchor,
a concurrent session landed **`9addeba8` — "Merge branch 'worktree-observable-harness-filing' —
intake #66 DRAFT (the OBSERVABLE HARNESS) plus five carrier amendments that reconcile rather than
restate"**. The locator §0.2(d) declares unresolvable is now tracked:

```
was (at 16f91f69)   untracked working-tree file in a locked worktree; zero tracked hits;
                    no entry in docs/intake/README.md
now (at 9addeba8)   docs/intake/2026-09-01-tech-observable-harness.md  -- TRACKED
                    intake-id 66 - status DRAFT - consumed-by: (still EMPTY)
                    indexed in docs/intake/README.md and docs/intake/manifest.json
```

**WHAT DID NOT CHANGE — and it is the half the candidate rests on.** Re-measured against the
landed file, not assumed from the draft:

- **`consumed-by:` is still empty.** The forward pointer §0.2(d) records is still owed: intake #66
  should name this artifact there.
- **It still names no cache-hit ratio, no token ratio, and no re-read volume.** The slot §0.5
  identified is **still empty**, so the CANDIDATE is not displaced and not redundant.
- **It is still `DRAFT`**, and its own banner still reads *"DRAFT BINDS NOTHING… Non-citable as
  doctrine until ratified; the repo wins on any conflict."* So it could not carry the candidate as
  doctrine even now.

**Net effect on §0.5's routing.** The recommended destination is unchanged but is no longer
conditional on a file landing: intake #66 **exists**, and the act owed is an amendment to it
carrying `ρ` and `h`, plus filling its `consumed-by:`. That remains **a recommendation to the
operator, not a decision taken here** — this session wrote nothing into intake #66, which was
another lane's live work throughout.

**Why this is recorded rather than quietly folded in.** §0.2(d) is the worked example of naming an
unresolvable locator *as* unresolvable instead of asserting it. Silently rewriting it once the
locator resolved would destroy the only evidence that the discipline was applied — and would make
this artifact's own integrity claims (§0.1, and the hashes at the top) less checkable, not more.

---

---

# Research brief — "The Harness Needs a Substrate"

**Type:** article research brief (flagship piece) · **Date:** 2026-09-01 · **Branch:** `docs/article-research`
**Status:** research complete, ready for conversational iteration. **Not a deck.** The deck derives from this.
**Author seat:** Claude Code, research + synthesis pass · **Owner:** Rob

> **Filename note:** the task named `2026-08-XX_…`; today is 2026-09-01, so the file takes today's date per the
> `YYYY-MM-DD_<type>_<kebab>` convention in `docs/audits/`. First `brief` type in the folder.

---

## 0. What this brief is, and what it is not

It is the research substrate for one article: the argument, the evidence, the counter-argument, an explicit
cost model, and chart specifications. It is **not** the article, and it does not choose the venue.

**Three inputs were used.** Rob's master's thesis (his own work, reused freely and marked where reused);
a Polish-language podcast on architecture in the AI era (**ideas only, credited — nothing reproduced,
no measurements reused**); and live web research, which is the bulk of the new work here and is cited
throughout with URLs.

**One thing changed during the research.** The cost model was commissioned to answer "what would it cost
to vibe-code an enterprise platform?" It does answer that — and the answer inverts the question. See §4.6.
That inversion is now the strongest movement in the article and it should probably be the lede.

---

## 1. The article spine

### 1.1 Thesis

The market has renamed its central skill twice in three years — **prompt engineering → context engineering →
harness engineering** — and each rename moved the work one layer *down*, closer to the system. Nobody has
named the next layer honestly. It is the **substrate**: the infrastructure, the single source of information,
and the engineering discipline a harness stands on — necessary conditions, evaluations, functional
requirements, architectural decisions, and quality attributes.

None of these are new inventions. They are the software-architecture canon of the last thirty years, being
re-derived under new names by people who have not read it. The article's job is to name that, show the
evidence that the substrate — not the tool — is what separates the organisations getting value from the ones
that aren't, and follow the economics to their genuinely surprising conclusion.

### 1.2 The argument in seven movements

| # | Movement | The claim | What carries it |
|---|---|---|---|
| **1** | **The renaming tells you where the work went** | Two renames in three years, each pushing the work one layer down. The trajectory is the story, not any one term. | Karpathy/Lütke on context engineering (Jun 2025); Gartner's "context engineering is in" (Jul 2025); harness-engineering literature through 2026 (Osmani, Schmid, a GitHub "awesome" list, several arXiv papers). §3.1 |
| **2** | **A harness stands on something** | Name the layer: necessary conditions, evaluations, functional requirements, architectural decisions, quality attributes. Not new — Bass/Clements/Kazman, Kruchten, ATAM, ADD. | Rob's thesis and its citation base (§2); the harness-component lists that read like an un-cited architecture syllabus |
| **3** | **The evidence says substrate, not tool** | The measured differentiator across organisations is the surrounding system, not the model. | **DORA 2025** — AI as amplifier; "platform engineering is the foundation"; healthy data ecosystems; AI-accessible internal data. Throughput up, **stability down**. §3.2 |
| **4** | **What gets worse when you skip it** | Volume rises; the maintainability signals move the other way. | **GitClear 2026** — duplication up 81%, refactoring moves 21%→3.8%, churn up 15%, across 623M changes. §3.3 |
| **5** | **The economics — and the inversion** | Token cost for a large rebuild is three-to-four orders of magnitude *below* the human cost. So cost is not the constraint. What stops you is the substrate. | The cost model, §4. **This is the engine of the piece.** |
| **6** | **The strongest objection, and what survives it** | The Bitter Lesson: scaffolding keeps getting absorbed. Conceded — for *technique*. Not for institutional fact. | §3.5, §3.6 — steel-manned, with a partial concession that must stay in |
| **7** | **What a leader does on Monday** | The necessary-conditions list as a decision instrument, not a maturity model. | Rob's five-step method, reframed (§2.3) |

### 1.3 Movements 5 and 6 are the article's whole claim to originality

Movements 1–4 are well-covered ground assembled unusually well. **Movement 5 has not been done** — nobody
has run the vibe-code-the-platform cost model to its inverting conclusion in public. **Movement 6 is what
makes it survive scrutiny.** If either is cut, this becomes a competent summary of other people's work.

---

## 2. The thesis-to-article map

**Source:** `C:\Users\1028120\Downloads\Praca_Dyplomowa_Magisterska` — LaTeX, Polish, Warsaw University of
Technology (EiTI template). ~90 files. Chapters 1–8 plus quality-attribute appendices B–F and an interview
transcript. Domain: a novel architecture-design method, applied to large grid-connected photovoltaic
installations, taking the computational model from a separate MSc thesis (Stankiewicz, PW, 2020) as its
business problem. **Stays disk-only.**

### 2.1 The single best bridge in the whole brief

Rob's own method chapter lists three **disadvantages** of his approach (`tex/5-5-autorska-metoda.tex`):

1. **Time-consuming** — many stages: scenarios, tactics, questionnaires, tradeoff analysis
2. **Requires specialist expertise** — in architecture, patterns, and performance evaluation
3. **Limited to the information gathered** — if the questionnaires miss something, the recommendation degrades

**Those three constraints are precisely what agentic tooling relaxes.** Cheap iteration removes (1). An
encoded procedure removes much of (2). Broad, fast document ingestion attacks (3).

Meanwhile the **advantages** he listed — structured method, systematic evaluation, stakeholder involvement,
tradeoff analysis — are exactly what a harness needs written down in order to work at all.

So the thesis is not a nostalgic artefact. **It is a specification for the substrate, written before the tools
existed, whose stated weaknesses have since been fixed by the tools.** That is a genuinely rare thing to be
able to say, and it is Rob's alone. It should open movement 2.

### 2.2 The second bridge — which half got automated

From the conclusions (`tex/8-wnioski-wynikające-z-pracy.tex`), Rob reports an asymmetry he found empirically:

- **Functional requirements were the most time-consuming stage.** Preparing to interview, asking the right
  questions, understanding what is actually to be achieved. He notes this is **under-served in the technical
  literature** and that the **transition from functional to non-functional requirements is essentially not
  covered at all**. Students rush past it to implementation.
- **The quality-attribute stage was simpler and more orderly.** Once you know what you want, translating human
  language into machine language "is a matter of nomenclature," and building the architecture is a matter of
  following documented patterns.

**Agents automate the second half. They do not automate the first.** That is the article's sharpest single
sentence and it is sourced to Rob's own experience, not to a vendor.

### 2.3 Reusable frameworks

**The five-step method** (`tex/5-5-autorska-metoda.tex`) — reframe each step as a substrate artefact:

| Thesis step | Reframed as substrate |
|---|---|
| 1. Define general scenarios for non-functional requirements | The **necessary conditions**, written down |
| 2. Develop tactics per quality attribute | The **option space** an agent may choose within |
| 3. Questionnaires with developers and stakeholders (closed questions) | The **elicitation instrument** — an agent can run it, a human still answers |
| 4. Analyse benefits and tradeoffs of candidate patterns | The **evaluation** |
| 5. Make the architectural decision | The **decision record** — and the human who owns it |

**The applied structure** — chapter 6 works seven-plus functional requirements through **Kruchten's 4+1 views**
(scenarios, logical, process, development, physical), then works quality attributes (availability,
deployability, integrability, performance, security; appendices add energy, modifiability, safety,
testability, usability) through scenario → tactics → questionnaire → pattern tradeoff → decision.

That is a **worked, complete, documented example of the exact artefact set agents now need to be handed.**
It is also, incidentally, a demonstration of the point: a document set of that shape is what a harness reads.

### 2.4 Lines worth reusing verbatim (Rob's own words, his to reuse)

- *Intro:* "If software does not flow from a solid system architecture, organisations risk incurring
  unsustainable costs." — **the substrate thesis, written years early.** Strong epigraph.
- *Conclusions (draft variant, currently commented out in the source):* "One can only imagine how many lines of
  code would have been wasted if we had started implementation too early." — **now inverted, and that inversion
  is the article.** Lines of code became cheap to produce and expensive to own. Use this to open movement 5.
- *Conclusions, via Bass:* after 30+ years the definition of a functional requirement remains unclear; the
  word to reach for is not *function* but **responsibility** — "what responsibilities does this problem
  involve?" Directly applicable: **agents should be given responsibilities, not functions.**
- *Conclusions:* the interview with the energy specialist was "the turning point." Confronting your thinking
  with someone who approaches the problem differently is what sets direction. Reusable as the human-in-the-loop
  argument that isn't sentimental.

### 2.5 The citation base — what still holds up

`bibliografia.bib` mixes real citations with unmodified EiTI template boilerplate. **The durable core:**

| Key | Reference | Verdict |
|---|---|---|
| `4edycja` | Bass, Clements, Kazman — *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021 | **Anchor.** Carries quality attributes, tactics, the FR/QA distinction, and the "responsibility" reframe |
| `4plus1-pros-n-cons-article` | Kruchten — "Architectural Blueprints: The 4+1 View Model of Software Architecture," *IEEE Software* 12(6), Nov 1995, 42–50 | **Use.** Genuine classic; the view set maps cleanly onto what an agent needs handed to it |
| `ATAM-zalety` | SEI — Architecture Tradeoff Analysis Method collection | **Use.** Institutional, citable, and the direct ancestor of "evaluations" |
| `ADD-zalety` | SEI — Attribute-Driven Design method collection | **Use** |
| `ADD-wady` | Ali & Solis — "Exploring How the Attribute Driven Design Method is Perceived," 2015 | **Use sparingly** — good for the honest "these methods were found heavy" note |
| `ATAM-wady` | Julia & Rodrigues — "Novel Creative Innovative Patterns for Architecture Analysis (CIPA)," *Indian J. Sci. Tech.* 9(30), 2016, DOI 10.17485/ijst/2016/v9i30/96653 | **Optional.** Weak venue; only if a named ATAM critique is needed |
| `old-definition` | Bachmann, Bass, Carriere, Clements, Garlan, Ivers, Nord, Little — *Software Architecture Documentation in Practice*, CMU/SEI-2000-SR-004, 2000 | **Use.** Excellent for "documentation as normative *and* descriptive" — which is what an `AGENTS.md` actually is |
| `agile` | Hoda, Salleh, Grundy — "The Rise and Evolution of Agile Software Development," *IEEE Software* 35(5), 58–63 | **Use, but fix the year.** The `.bib` says 2015; *IEEE Software* 35(5) is **2018** |
| `wzorce-architektoniczne` | Richards — *Software Architecture Patterns*, O'Reilly, 2015 | **Use, but fix the entry** — author and title fields are swapped in the `.bib` |
| `stankiewicz` | Stankiewicz — MSc, Politechnika Warszawska, 2020 | Context only; the source of the business problem |

**Drop for an external article:** the Medium/LinkedIn tier (`EDA-wzorzec`, `pattern-for-Deployment1..3`,
`pattern-for-availability1..3`, `analiza-integralnosc`, `four-plus-one-views`, `Functional-Requirements`,
`eda`, `atrybuty-jakości`). Fine in a 2023 thesis; not load-bearing in a 2026 published piece. Replace with
the 2025–26 sources in §3 and §8.

**Ignore entirely:** the unmodified template entries (`article`, `book`, `szczypiorski2015`, `goossens93`,
`wang97`, `goedel95`, `benzmuller2014`, `duqu2011`, `shs2015`, `wozniak2018`, `koons2005`, `dcp19`) — EiTI
template examples, never cited in the text.

---

## 3. Industry confrontation

### 3.1 Where the discourse actually is (movement 1's evidence)

**The renaming is real and datable.** *Prompt engineering* → *context engineering*, settled in **June 2025**
when Andrej Karpathy and Tobi Lütke publicly endorsed the term, with Karpathy defining it as filling the
context window with the right information for the next step; Gartner declared in **July 2025** that "context
engineering is in, prompt engineering is out." Through **2026** the centre of gravity moved again, to the
**harness**.

**Harness engineering is emerging but not yet settled.** It has a working definition, a literature, and
practitioner consensus, but no canonical citation:

- **Addy Osmani** (19 Apr 2026): a harness is "every piece of code, configuration, and execution logic that
  isn't the model itself"; **Agent = Model + Harness**; "a decent model with a great harness beats a great
  model with a bad harness." Component list: system prompts and skill files, tools/MCP, sandboxed execution,
  orchestration, hooks, observability, filesystem and version control, memory, context management, planning
  and verification.
- **Philipp Schmid** (5 Jan 2026): the harness is "the infrastructure that wraps around an AI model to manage
  long-running tasks" — the OS layer between model and application. Durability over many steps is what now
  separates systems; benchmarks don't catch a model drifting off-track at step fifty.
- A community "awesome-harness-engineering" list and several 2026 arXiv papers on harness design, harness
  security, and harness-vs-post-training interplay.

**The article's opening is therefore accurate and defensible:** two renames, each moving the work one layer
down, and the industry has not yet named the third layer.

**Note the shape of Osmani's component list.** Sandboxing, observability, version control, verification,
planning — it is an infrastructure-and-discipline checklist that a 2005 architecture reviewer would recognise
line for line, presented without a single citation to that tradition. That observation *is* movement 2, and
it costs nothing to make politely.

### 3.2 Where the market agrees with Rob — and it agrees hard

**DORA's 2025 State of AI-assisted Software Development** (Google Cloud; 5,000+ respondents, 100+ hours of
interviews) is the strongest external corroboration available, and it is not from a platform vendor with a
product to sell in this space:

- **90%** of respondents use AI at work; **80%+** believe it has increased their productivity; **~30%** report
  little or no trust in AI-generated code.
- A **positive** relationship between AI adoption and both delivery throughput and product performance —
  a reversal of the prior year.
- A **continuing negative relationship with delivery stability.**
- The framing: *"AI doesn't fix a team; it amplifies what's already there."* And: *"The greatest returns on AI
  investment come not from the tools themselves, but from a strategic focus on the underlying organizational
  system."*
- On the mechanism: *"Without robust control systems — like strong automated testing, mature version control
  practices, and fast feedback loops — an increase in change volume leads to instability."*

**The DORA AI Capabilities Model** names seven capabilities that amplify AI's impact. At least four are
literally Rob's substrate list:

| DORA capability | Maps to |
|---|---|
| **Quality internal platforms** | *the substrate*, named outright — "platform engineering is the foundation" |
| **Healthy data ecosystems** | the single source of information |
| **AI-accessible internal data** | the same, made reachable |
| **Strong version control practices** | necessary conditions / control systems |
| Working in small batches | — |
| Clear and communicated AI stance | — |
| User-centric focus | — |

**This is the single most useful research finding in the brief.** Rob's thesis is not a contrarian position;
it is Google's measured finding, stated in Google's own words, and almost nobody in the harness-engineering
conversation is citing it. The article can lead with external authority and then go further than DORA does.

### 3.3 The quality evidence (movement 4)

**GitClear, *The Maintainability Gap*, January 2026** — 623 million analysed code changes, 2023–2026:

- Code block duplication **up 81%** — a record 73.0 duplicated lines per thousand changed lines, up from 40.3
- Refactoring ("moved") lines collapsed from **21% (2022) to 3.8% (2026 YTD)**, while copy/paste rose from
  **9.4% to 15.7%** — roughly a **5× swing** toward duplication over reuse
- Cross-file function calls **down 35%**; method calls per thousand changed lines fell **343 → 223**
- Error-masking constructs **up 47%**; two-week churn **up 15%**; legacy-file updates fell **1.7% → 0.46%**

**Handle with care.** GitClear sells code-quality analytics, and the page does not disclose repository
selection criteria, geography, or industry mix. Report it as a strong directional signal from an interested
party, corroborated in direction by DORA's independent stability finding. **Do not present it as neutral.**

Their own **January 2026** follow-up is a useful honesty check and should be included: heavy AI users
out-produce non-users by 4–10×, **but most of that gap pre-dated AI** — measured against their own past
selves, heavy AI users gained a more modest **~25%** in velocity. Selection effect, not treatment effect.
Including this inoculates the article against the charge of cherry-picking.

### 3.4 The productivity evidence — and why the famous number must not be used naively

**METR's July 2025 RCT** is the most-cited result in this space: 16 experienced open-source developers, 246
issues on repositories they had worked on for ~5 years, using Cursor Pro with Claude 3.5/3.7 Sonnet.
Developers were **19% slower** with AI, while believing they had been **20% faster** and having predicted
**24% faster**.

**It is out of date, and METR says so.** Their **February 2026** methodology update reports:

- For returning developers from the original cohort: **−18%** speedup (CI −38% to +9%)
- For newly recruited developers: **−4%** (CI −15% to +9%)
- A **selection effect** they discovered in the original design: **30–50%** of invited developers declined to
  participate without AI access, biasing the sample toward those who benefit least
- Their own conclusion: **"AI likely provides productivity benefits in early 2026."**

**Rule for the article: never cite the 19% without the update.** An article that leans on it will be
discredited by anyone who has read METR's own follow-up — and it would be arguing the wrong thing anyway.
The interesting finding is not "AI is slow." It is the **perception gap**, which survives the update intact
and is a much better fit for a leadership audience: teams cannot self-report their way to knowing whether
this is working. **That is an argument for evaluations** — one of Rob's necessary conditions — and it lands
far better than a stale slowdown figure.

### 3.5 The strongest counter-argument to Rob's thesis, stated fairly

**The Bitter Lesson objection.** Sutton's argument is that general methods leveraging computation beat
hand-coded human knowledge, every time. Applied here: every layer of scaffolding built so far has been
absorbed by the next model generation. Retrieval scaffolding was absorbed by long context. Chain-of-thought
prompting was absorbed by reasoning models. Elaborate orchestration frameworks are being absorbed by natively
agentic training.

**The evidence for it is specific, current, and comes from people who build harnesses for a living:**

- Schmid (Jan 2026) argues harnesses should get **simpler**, not richer, as models improve — "build to delete"
- **Manus** refactored its harness **five times in six months** to strip out rigid assumptions
- **LangChain** re-architected its Open Deep Research agent **three times in one year**
- **Vercel** removed **~80%** of its agent's tools
- "Capabilities that required complex, hand-coded pipelines in 2024 are handled by a single context-window
  prompt in 2026"
- Dennis, Diamond, Patil, Shabahang & Guo, *In-Context Prompting Obsoletes Agent Orchestration for Procedural
  Tasks* (arXiv:2604.27891, 2026) — argues directly that in-context prompting replaces orchestration for a
  named task class, benchmarked against MultiWOZ/SimpleTOD, explicitly scoped to *procedural* tasks

**Stated at full strength:** *if the scaffolding keeps dissolving, then telling enterprises to invest heavily
in substrate is telling them to build the thing that is about to be obsoleted — and that bet has lost
repeatedly for three years running.*

**⚠ Verification debt:** I retrieved the arXiv paper's title, authors, claim and scope, but the fetch did not
yield its measured results or sample sizes. **Read the PDF before citing it in print.** A saved copy is in the
session tool-results directory. Citing a paper that cuts against you and getting its numbers wrong is the
worst available outcome.

### 3.6 What survives the counter-argument — and what must be conceded

**The rebuttal, and it is a good one:** the Bitter Lesson applies to **technique**, not to **institutional
fact**. A model can absorb a reasoning procedure. It cannot absorb your master data, your entitlements, which
of two conflicting definitions of "on-time delivery" your company actually uses, or who is allowed to approve
a release. Those are not capabilities awaiting a better model; they are facts about an organisation that must
be recorded by that organisation or not exist at all.

Sort Rob's substrate list by which side of that line it falls on:

| Substrate element | Absorbable by a better model? | Verdict |
|---|---|---|
| Single source of information / good infrastructure | **No** — it is institutional fact | **Holds** |
| Functional requirements (what the business wants) | **No** — nobody else knows | **Holds** |
| Architectural decisions (and who owns them) | **No** — accountability isn't a capability | **Holds** |
| Quality attributes (what "good" means here) | **Partly** — a model can propose, not decide | **Mostly holds** |
| Evaluations | **Partly** — models may need less hand-holding, but you still need to know if it worked | **Concede: the form will get thinner** |
| Orchestration / workflow scaffolding | **Yes — largely** | **Concede outright** |

**Two concessions the article must make, in its own voice, before a reader makes them for it:**

1. **The orchestration layer is transient.** Some of what is called "harness" today will be gone in
   eighteen months. Rob's argument survives because his list is deliberately one layer *below* orchestration
   — but he must say so explicitly, or he will be read as defending scaffolding.
2. **We may have the wrong half of the substrate.** See §3.7.

**The third objection, which is about the author rather than the argument:** "a harness needs a platform" is
exactly what a platform vendor says. There is no clever way around this. The only defence is method — lead
with DORA rather than with our own product, run the cost model honestly and publish the result even though it
undercuts the dramatic version of the question, and concede §3.7. An article that does those three things
survives the charge. One that doesn't, won't.

### 3.7 The sharpest challenge to the platform arm

**Yali Sassoon, "A semantic layer is not a context layer" (Data Creation, 6 July 2026)** is the most
uncomfortable and most useful source found in this pass. The argument:

- A **semantic layer** answers *"what does this data mean?"* — consistent, retrospective definitions
- A **context layer** answers *"what does this agent need to know to act well, here, now?"*
- *"A semantic layer describes the past consistently; a context layer assembles the present for a decision."*
- Agents need a five-step pipeline — comprehend the situation, frame the problem, determine what information
  is needed, acquire it across all sources, compose it for use. **A semantic layer serves step four, partly.**
- The killer line: *"No amount of consistent definition conjures data that was never recorded."*

A related piece (Metadata Weekly, "Semantic Layers Failed. Context Graphs Are Next") adds that neither
semantic nor context layers *create* the governed metadata they consume.

**Why this matters here.** A curated planning data model — dimensions, nodes, measures, hierarchies without
physical joins, one ingest at the leaf serving every level above it (`knowledge/sections/SEMANTIC_NETWORK.md`)
— is a semantic layer of unusually high quality. On Sassoon's account, that is necessary and **not
sufficient**. The honest position is therefore **not** "we already have the substrate." It is:

> *We have the durable half — the meaning — which is the half that takes a decade and cannot be prompted into
> existence. The present-tense half is real work still to do, and it is work nobody has finished.*

That is a **better** article than the triumphalist version. It is more credible, it is more useful to a
reader, and it survives contact with someone who has thought about this. It also converts the piece from
advocacy into analysis, which is the difference between thought leadership and marketing.

### 3.8 Source-quality ledger

Not all of the above is equally load-bearing. Grade it before publishing.

| Tier | Sources | Use |
|---|---|---|
| **A — institutional, methodologically stated** | DORA 2025 + AI Capabilities Model; METR (both passes); Kruchten 1995; Bass/Clements/Kazman; SEI ATAM/ADD; CMU/SEI-2000-SR-004; Anthropic official pricing docs; Wheeler's COCOMO essay; COCOMO II manual | Load-bearing. Cite freely |
| **B — credible practitioner, named author, current** | Osmani; Schmid; Sassoon; arXiv 2604.27891 *(pending PDF read)* | Cite with attribution; these are positions, not findings |
| **C — interested party, real data** | GitClear (both reports) | Cite **with the conflict disclosed** |
| **D — trade press, unstated method** | Build-vs-buy cost and time-to-production figures (§4.7); vibe-coding failure round-ups | Directional only. Never a headline number |
| **REJECTED** | "65% of enterprise AI failures trace to harness defects" — surfaced in search, **no primary source traced**. Also **MIT/NANDA "95% of pilots fail"** — not peer-reviewed, dataset unpublished, methodology publicly contested, and the real claim ("no P&L impact within ~6 months") is much narrower than the headline | **Do not use.** The 95% figure in particular is a credibility trap: it is exactly the statistic a sceptical reader will already know is contested |

---

## 4. The cost model

### 4.1 The scoping decision, stated plainly

**"What would it cost to vibe-code an enterprise supply chain platform?" is not a coherent question,** and the
article should say so rather than pretend to answer it. A two-decade platform is not a fixed body of code; it
is an accumulation of domain decisions, integrations, regulatory accommodations, customer-specific behaviour
and operational scar tissue. There is no defensible size estimate for it, and any headline number would be
invented.

**So the model does something more useful:** it prices a **size-parameterised slice**, three scenarios wide,
and lets the structure of the answer carry the argument. The three scenarios are deliberately not tied to any
Blue Yonder component — they are generic engineering sizes.

| Scenario | Size | Shape |
|---|---|---|
| **A** | 50 KSLOC | One substantial service |
| **B** | 250 KSLOC | A subsystem — several services with a shared data model |
| **C** | 1,000 KSLOC | A platform slice — a coherent functional area |

### 4.2 Human baseline — method and sources

**Method:** Intermediate COCOMO, semidetached mode, following **David A. Wheeler's** published methodology for
the Linux kernel — the canonical worked example of a "cost to rebuild X" analysis and the answer to the
brief's question about whether anyone has done this defensibly.

```
Effort_nominal (person-months) = 3.0 × (KSLOC)^1.12
Effort_adjusted                = Effort_nominal × EAF
Cost                           = (Effort_adjusted / 12) × fully_loaded_annual_cost
```

**Wheeler's precedent:** 4,287,449 physical SLOC → 3 × 4287.449^1.12 = 35,090 person-months → × EAF 1.549 =
54,344 person-months (4,528.6 person-years) → × $56,286/yr × 2.40 overhead = **$611,757,037**. Later Linux
Foundation work using the same family of methods put a full distribution at multi-billion scale; SLOCCount is
the tooling.

**Our assumptions, stated:**

- **EAF = 1.0** central (Wheeler used 1.549 for the kernel; EAF realistically spans ~0.5–2.5)
- **Fully loaded cost = $150,000/person-year** central, **$100,000–$200,000** band — salary plus overhead,
  blended across seniorities and geographies. *This is an assumption, not a citation.*

**Result — human rebuild:**

| Scenario | Effort (person-months) | Person-years | Cost @ $100k | **Cost @ $150k** | Cost @ $200k |
|---|---|---|---|---|---|
| **A** — 50 KSLOC | 240 | 20.0 | $2.0M | **$3.0M** | $4.0M |
| **B** — 250 KSLOC | 1,455 | 121.2 | $12.1M | **$18.2M** | $24.3M |
| **C** — 1,000 KSLOC | 6,873 | 572.7 | $57.3M | **$85.9M** | $114.5M |

*(At Wheeler's EAF of 1.549, scenario B becomes 187.8 person-years, ~$28.2M at $150k.)*

**COCOMO's own caveat, which the article must carry:** it was calibrated on 161 large institutional projects
and Wheeler himself notes it models a single snapshot's redevelopment cost, not value, and not the exploration
and discarded alternatives that produced the design. It is an order-of-magnitude instrument. That is all it
needs to be here.

### 4.3 Token side — method and assumptions

Every parameter below is an **assumption**, not a measurement. None is invented to flatter the conclusion;
the sensitivity analysis in §4.5 shows the conclusion survives all of them being wrong.

| Parameter | Symbol | Central | Range | Basis |
|---|---|---|---|---|
| Tokens per delivered line of source | `t` | 12 | 8–18 | ~40 chars/line at ~3.5 chars/token. **Anthropic's own docs note the Claude 4.7+ tokenizer produces ~30% more tokens for identical text** — so any figure calibrated on an older tokenizer is low |
| Rework multiplier (total output ÷ delivered) | `R` | 5 | 2–15 | Drafts, tests, revisions, abandoned attempts. Modelled |
| Input : output token ratio | `ρ` | 10 | 5–30 | Agents re-read context continually. Modelled — **the least defensible parameter and, per §4.5, the one that matters most** |
| Cache hit fraction | `h` | 0.80 | 0.50–0.95 | Modelled |

```
Output tokens     = LOC × t × R
Input tokens      = Output × ρ
Effective input   = Input × [ (1 − h) + 0.1h ]        # cache read = 0.1 × base input
Cost              = Output × price_out + Effective_input × price_in
```

**Prices — Anthropic official documentation, checked 2026-09-01. Prices move; re-check on the day of
publication.**

| Model | Input /MTok | Output /MTok |
|---|---|---|
| Claude Opus 5 | $5 | $25 |
| Claude Sonnet 5 | $2 | $10 |
| Claude Haiku 4.5 | $1 | $5 |
| Claude Fable 5 | $10 | $50 |

Cache read = 0.1× base input; 5-min cache write = 1.25×; 1-hour = 2×. Batch API = 50% off both directions.
For comparison, OpenAI's current frontier tier sits in the same band (~$5/$30 per MTok for its top model),
**but that figure comes from a pricing aggregator, not OpenAI's own page — verify before print.**

### 4.4 Result — and it is not close

**Scenario B (250 KSLOC), central assumptions:** output 15.0M tokens; input 150M raw → 42.0M effective.

| Model | Token cost |
|---|---|
| Opus 5 | **$585** |
| Sonnet 5 | $234 |
| Haiku 4.5 | $117 |

**Full range for scenario B on Opus 5:** **$115 (optimistic) — $7,256 (pessimistic)**.

**Against a human rebuild of $12.1M–$24.3M.**

| Scenario | Token cost (Opus 5, central) | Human cost (central) | Ratio |
|---|---|---|---|
| **A** — 50 KSLOC | $117 | $3.0M | **~25,600×** |
| **B** — 250 KSLOC | $585 | $18.2M | **~31,100×** |
| **C** — 1,000 KSLOC | $2,340 | $85.9M | **~36,700×** |

**And the gap widens with scale.** Token cost scales ~linearly with size; COCOMO effort scales as
`KSLOC^1.12`. The ratio therefore grows as `KSLOC^0.12` — about **43% wider** from scenario A to C. Small,
but it runs in the direction nobody expects.

### 4.5 Sensitivity — which assumption dominates

**Token side.** Moving from central to pessimistic multiplies output tokens 4.5× but effective input tokens
**26.5×**. In the pessimistic case input is **77%** of total cost. **The dominant parameter is `ρ × (1−0.9h)`
— how much context the agent re-reads, and how well that context is cached.**

That is worth stating in the article because of where it lands: **the cost driver is context, not
generation.** The sensitivity analysis arrives independently at the article's own thesis. Generating code is
close to free; supplying and re-supplying the *right context* is what you actually pay for — and the quality
of that context is exactly the substrate.

**Human side.** EAF dominates (~5× span) over the loaded rate (~2× span).

**The robustness claim, which is the important one:** take the **most** expensive token assumptions and the
**cheapest** human assumptions simultaneously — $7,256 against $12.1M — and the gap is still **~1,700×**.
There is no combination of defensible assumptions in which token cost approaches human cost. **The finding is
not sensitive to the assumptions.** It is the one number in this brief that can be stated with confidence.

### 4.6 The inversion — read this before writing anything

The model was built to answer "what would it cost to vibe-code an enterprise platform?" **The answer is: not
very much, and that is not the interesting part.**

If the marginal cost of generating a platform's worth of code is three-to-four orders of magnitude below the
cost of writing it by hand, and **no one has done it**, then cost was never the binding constraint. Something
else is stopping people. **That something else is the article.**

The honest framing is therefore not *"vibe-coding a platform would cost $X million"* — it would not, and any
piece claiming so is arithmetic dressed as insight. It is:

> **Generating the code is nearly free. Everything that makes the code into a system is not. The question was
> never affordability — it was whether you have the substrate to make generated code mean anything.**

**What the token model explicitly excludes** — and this list *is* the substrate, which is why the exclusion
list is the argument:

- Requirements elicitation and stakeholder alignment *(the stage Rob measured as most time-consuming)*
- Architectural decisions, and the accountability for owning them
- Evaluation design — deciding what "correct" means before you can check it
- Security review and threat modelling
- Data modelling and the semantic layer
- Integration with systems that already exist and cannot be regenerated
- Human review of generated output at volume
- Operating the result: observability, incident response, upgrade paths
- Migration of live customers, and the regulatory and contractual surface

**Under no assumption does the model claim a platform can be rebuilt for $2,340.** It claims the opposite: the
$2,340 is real, and it buys you nothing without the list above.

### 4.7 Building on a platform — the counter-side

**What is not rebuilt** when you build on an existing platform: the data model and its curated meaning;
ingestion, validation and distribution; governed access (roles, masking and row-level policies that hold
regardless of how a query arrives); traceability and audit; the promotion path and its review bodies;
monitoring and operations. **What you tokenise is the layer above** — the agent, its tools, its evaluations
and its domain logic.

That layer is a scenario-A-sized problem at most, and often much smaller. Which is the practical form of the
argument: **the substrate is the expensive part, and it is the part you can inherit.**

**Time to production and onboarding — trade-press figures, tier D, use only as illustration:** buy/configure
in complex environments ≈ 3–6 months; build ≈ 6–12 months; a basic agent ≈ 2–6 weeks; a production-ready
multi-agent system with monitoring, fallback, memory and security controls ≈ 3–6 months. Custom enterprise AI
platforms are quoted at $300k–$1.5M+ upfront with 20–30% annual maintenance. One source claims vendor-led
efforts succeed ~67% against ~33% for pure builds — **methodology unstated; do not print that pair.**

**Team learning and onboarding is unmodelled and should stay that way** unless Rob supplies experience. The
one defensible external anchor is DORA's finding that a quality internal platform amplifies AI's
organisational impact — which is an argument about onboarding without pretending to a number. **A missing
chart beats a fabricated one.**

---

## 5. Chart specifications

**None of these may be drawn from invented data.** Each names its source or its model output.

---

**Chart 1 — The cost gap (the article's centrepiece)**
- **Shows:** token cost vs human redevelopment cost, three size scenarios, **log scale**, with sensitivity
  bands on both bars
- **Data:** §4.4 table + §4.2 band + §4.3 range. Model output, assumptions published alongside
- **Type:** horizontal paired bars, log x-axis, banded
- **Must make the reader think:** *"Generating the code is not the expensive part — so the expensive part is
  everything else."*
- **Caveat on the chart itself:** "excludes requirements, architecture, evaluation, security, integration,
  review and operations — see exclusion list"

---

**Chart 2 — Where the cost actually sits inside the token model**
- **Shows:** for scenario B, the split between output-token cost and effective input-token cost, across
  central → pessimistic assumptions
- **Data:** §4.5 sensitivity. Model output
- **Type:** stacked bar, two or three assumption columns
- **Must make the reader think:** *"Even in the cheap part, you pay for context, not for generation."*

---

**Chart 3 — The reuse/risk scissors**
- **Shows:** refactoring ("moved") lines 21% → 3.8% against copy/paste 9.4% → 15.7%, 2022 → 2026 YTD; optional
  second panel for duplication 40.3 → 73.0 per thousand changed lines
- **Data:** GitClear *The Maintainability Gap*, Jan 2026 (623M changes). **Label the source on the chart** —
  interested party
- **Type:** two diverging lines, crossing
- **Must make the reader think:** *"Output went up and the maintainability signals went the other way."*

---

**Chart 4 — The phase transition**
- **Shows:** prompt engineering → context engineering (Jun 2025, Karpathy/Lütke; Gartner Jul 2025) → harness
  engineering (2026) → **substrate (unnamed)**, with the last position deliberately empty
- **Data:** §3.1, all datable and cited
- **Type:** horizontal timeline, four stations, last one blank
- **Must make the reader think:** *"Each rename moved the work one layer down. Here is the next one."*
- **This is the article's title slide** and probably its opening image

---

**Chart 5 (optional) — What you don't rebuild**
- **Shows:** the full platform stack with the inherited layers shaded and the tokenised layer highlighted
- **Data:** §4.7. Structural, not quantitative — **do not put numbers on it**
- **Type:** layered block diagram
- **Must make the reader think:** *"You only pay to generate the top layer."*
- **Risk:** this is the chart most likely to read as a product diagram. If the piece is external, either draw
  it generically or cut it. **Cut before adding.**

---

## 6. What's still missing to write it

**Blocking — only Rob can supply:**

1. **Any measured internal evidence.** The article currently has zero first-party data. It does not strictly
   need any — DORA and GitClear carry the empirical load — but one honest internal observation, even
   qualitative, is what separates this from a literature review. *What actually changed when he built his own
   harness?*
2. **The venue decision.** Internal, industry publication, or conference talk. It changes length, how much
   platform material is admissible, and whether chart 5 survives.
3. **How much platform specificity is permitted externally.** Capability-level description of a semantic
   modelling layer and a governed promotion path is almost certainly fine. Anything with numeric gate
   thresholds, named review bodies, dates or maturity states is out under the standing exclusions.

**Non-blocking but should be closed:**

4. **Read arXiv:2604.27891 properly** (§3.5). Its measured results and sample sizes are unretrieved, and it is
   the single strongest counter-source.
5. **Verify OpenAI and Google pricing against vendor pages** — currently aggregator-sourced (§4.3).
6. **Find a primary Karpathy link** for the June 2025 context-engineering definition. It is currently
   second-hand through several summaries.
7. **Decide whether `ρ` can be replaced with a measurement.** Rob could instrument one real agent session and
   report actual input:output ratio and cache hit rate. That would convert the model's weakest parameter into
   a measured one and would be, as far as this research found, **novel published data**. Highest-value
   optional work in the whole brief.

**Deliberately not chased:** the MIT/NANDA 95% figure and the unsourced "65% harness defects" claim (§3.8).

---

## 7. Positioning

**Length and shape.** 1,800–2,500 words. Seven movements is one too many for that length — **merge 3 and 4**
(the evidence movements) and lead with the inversion from movement 5. A leadership reader will not survive
four consecutive evidence sections before reaching the idea.

**Recommended structure:** open on the renaming (short), state the thesis, go straight to the cost inversion
while the reader is still interested, then bring the evidence, then concede, then close on the Monday list.

**Where it could land.** *Suggestions, not commitments.* Internally as a strategy note it works as-is. For an
industry publication, the harness-engineering conversation is currently hosted on personal blogs and Substack
rather than in journals — which is an opportunity, since the bar for rigour there is low and this piece clears
it easily. A conference talk version would lean on charts 4 and 1.

**The closest existing pieces, and how this differs:**

| Existing | What it does | What it doesn't |
|---|---|---|
| Osmani, *Agent Harness Engineering* (Apr 2026) | Best current definition and component list | Never asks what the harness stands on; no citation to the architecture tradition |
| Schmid, *The importance of Agent Harness in 2026* (Jan 2026) | Best statement of the simplify-over-time trajectory | Argues the layer above ours; is in fact our counter-argument |
| DORA 2025 | The empirical foundation; names internal platforms outright | Measures; doesn't argue. And almost nobody in the harness conversation cites it |
| Sassoon, *A semantic layer is not a context layer* (Jul 2026) | The sharpest thinking on what agents need underneath | Data-team framing; no software-architecture lineage, no economics |
| GitClear, *The Maintainability Gap* (Jan 2026) | The quality evidence | Interested party; describes symptoms, not causes |

**The gap this fills — and it is a real one.** Nobody is joining the harness-engineering conversation to the
software-architecture canon it is unknowingly re-deriving, *and* running the economics to a conclusion that
undercuts the dramatic version of its own question, *and* writing from a seat inside a platform vendor while
conceding that vendor holds only half the substrate.

**The unfair advantage:** a master's thesis from before the AI era whose stated weaknesses have since been
fixed by agents, and whose stated strengths turn out to be the specification for what a harness needs. Almost
nobody writing in this space has receipts that old. **Lead with it — it is the credential that makes the rest
of the argument land as observation rather than opinion.**

---

## 8. Sources

**Institutional and primary (tier A)**
- DORA, *State of AI-assisted Software Development 2025* — https://dora.dev/dora-report-2025/
- Google Cloud, announcement + figures — https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- DORA AI Capabilities Model (PDF) — https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf
- DORA 2025 full report (PDF) — https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf
- Introducing the AI Capabilities Model — https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model
- METR, original RCT (Jul 2025) — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- METR, **experiment-design update (Feb 2026)** — https://metr.org/blog/2026-02-24-uplift-update/
- METR, self-reported impact survey (May 2026) — https://metr.org/blog/2026-05-11-ai-usage-survey/
- Anthropic, official API pricing — https://platform.claude.com/docs/en/about-claude/pricing
- Wheeler, *The Linux Kernel: It's Worth More!* (COCOMO methodology) — https://dwheeler.com/essays/linux-kernel-cost.html
- Wheeler, *Counting Source Lines of Code* — https://dwheeler.com/sloc/
- COCOMO II Model Definition Manual — https://athena.ecs.csus.edu/~buckley/CSc231_files/Cocomo_II_Manual.pdf
- Linux Foundation, value-of-Linux estimate — https://www.linuxfoundation.org/press/press-release/linux-foundation-publishes-study-estimating-the-value-of-linux

**Practitioner positions (tier B)**
- Osmani, *Agent Harness Engineering* (19 Apr 2026) — https://addyosmani.com/blog/agent-harness-engineering/
- Schmid, *The importance of Agent Harness in 2026* (5 Jan 2026) — https://www.philschmid.de/agent-harness-2026
- Sassoon, *A semantic layer is not a context layer* (6 Jul 2026) — https://datacreation.substack.com/p/a-semantic-layer-is-not-a-context
- *Semantic Layers Failed. Context Graphs Are Next* — https://metadataweekly.substack.com/p/semantic-layers-failed-context-graphs
- Dennis, Diamond, Patil, Shabahang, Guo — *In-Context Prompting Obsoletes Agent Orchestration for Procedural Tasks*, arXiv:2604.27891 — https://arxiv.org/pdf/2604.27891 · **⚠ results unread**
- awesome-harness-engineering — https://github.com/ai-boost/awesome-harness-engineering
- Masood, *Agent Harness Engineering: The Rise of the AI Control Plane* — https://medium.com/@adnanmasood/agent-harness-engineering-the-rise-of-the-ai-control-plane-938ead884b1d
- Greyling, *Auto Agentic Harness Engineering* (May 2026) — https://cobusgreyling.medium.com/auto-agentic-harness-engineering-b27a962fad9a
- Sourcegraph, *Context Engineering: A Practical Guide* (term history) — https://sourcegraph.com/blog/context-engineering

**Interested-party data (tier C — disclose)**
- GitClear, *The Maintainability Gap* (Jan 2026) — https://www.gitclear.com/the_ai_code_quality_maintainability_gap
- GitClear, *AI Copilot Code Quality 2025* — https://www.gitclear.com/ai_assistant_code_quality_2025_research
- GitClear, developer AI productivity research index (2026) — https://www.gitclear.com/developer_ai_productivity_analysis_tools_research_2026

**Rob's own work (disk-only, not tracked)**
- `Praca_Dyplomowa_Magisterska` — LaTeX source, Warsaw University of Technology. Cited throughout §2

**Ideas credit (nothing reproduced)**
- devstyle / *Architekt Jutra* live, "Architektura w erze AI" (Aug 2026), hosts Jakub Pilimon, Kuba Kubryński,
  Łukasz Szydło — https://www.youtube.com/watch?v=_yG_32R2OCc
  *Prompted the line of thinking; supplied no text, no data and no measurements to this brief or the article.
  One credit line in the published piece discharges the debt.*

**Repo grounding**
- `knowledge/sections/SEMANTIC_NETWORK.md` · `knowledge/sections/PLATFORM.md` ·
  `output/2026-08-18_agent_paths_deck_v2/_work/SESSION-REPORT-agent-deployment-cortex.md`

---

## 9. Standing constraints observed

- **No customer-identifying content, nothing restricted, no dates/maturity/pricing claims about our own
  product.** Platform material appears at capability level only, as evidence.
- **Podcast:** ideas only, credited; no reproduction, no extended paraphrase, no reuse of its measurements.
- **Rob's thesis:** his own; reuse marked throughout §2.
- **Disk-only:** transcript, thesis copy, scraped material, the saved arXiv PDF. This brief is the only
  tracked artefact.
- **FREEZE · no push.**
