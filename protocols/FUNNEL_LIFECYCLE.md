# FUNNEL_LIFECYCLE — the governed-object state machine, written once

<!-- scope: meta -->

> **What this is.** One state machine for every object the governance funnel moves — audit
> artifact, finding, intake doc, ADR, backlog row. It states the **states** (with the token in
> the tree that carries each), the **allowed transitions** (with the actor who performs each and
> the evidence it requires), the **terminal conditions**, and **who archives what and when**.
>
> **What it is not.** It supersedes nothing. ADR-98, ADR-111, ADR-100 and ADR-70 remain the
> deciding authorities; §7 states clause by clause where this file restates one of them and where
> it goes further. Where this file and a source disagree, the source wins and this file is the
> defect.
>
> **Why it exists.** Each of the four sources governs one edge. ADR-98 governs how a requirement
> is captured, ADR-111 how a finding is triaged, ADR-100 how audits are retained, ADR-70 how a row
> is closed. No source draws the whole machine, so each seat re-derived the joins, and the joins
> are where objects were lost: an intake consumed by rows that all closed, still sitting live; an
> ADR superseded by its successor, still filed beside it.
>
> **The bar this text is written to.** Two seats running one funnel pass from this text alone
> produce identical transitions. A judgement call left open here is a defect in this file, not a
> decision delegated to the reader.

---

## 1. A1 — this machine is the template for all governed objects

The shape below — **an explicit state token carried in the tree, a closed set of allowed
transitions, an actor and a resolving evidence locator per transition, and an archival act bound
to the terminal transition** — is stated here for the funnel because the funnel is where it was
first needed. It is **not specific to the funnel.** Any governed object this corpus later
introduces (a routine, a carrier, a lane contract, a deployed component) is expected to declare
the same four things, and a class that declares fewer is under-specified in exactly the way the
funnel was before this file.

The generalization is the claim, so it is stated rather than implied: **every governed object
carries explicit state plus dated transitions.** §2's table is one instantiation of that rule with
five rows in it.

---

## 2. The five classes, and the token that carries state

State is a property of the tree, not of anyone's memory. Each class below has **one token, at one
declared location, with one declared domain** — and for the audit class the **absence** of that
token is itself a declared value (`untriaged`), which is why the domain column names it.

| Class | Home | State token | Declared domain |
|---|---|---|---|
| **Audit artifact** | `docs/audits/*.md` | a row naming it in a **disposition ledger** — a markdown table carrying a file column, a `disposition` column and an `evidence locator` column | `ACTIONED` · `FILED` · `REJECTED` · `SUPERSEDED` · `PENDING`; **no row = untriaged** |
| **Finding** | a line inside an audit artifact | its **triage outcome**, recorded in the wave-close funnel table | `OWNED` · `DISCHARGED` · `CANDIDATE` · `REJECTED` |
| **Intake doc** | `docs/intake/*.md` | frontmatter `status:` | `SEED` · `DRAFT` · `READY` · `ACCEPTED` · `CONSUMED` · `SUPERSEDED` · `REJECTED` |
| **ADR** | `docs/decisions/ADR-*.md` | the header `Status:` field | `Proposed` · `Accepted` · `PARKED` · `Explored, not adopted` · `Partially superseded` · `Superseded` · `Deprecated` |
| **Backlog row** | `tasks/<id>-<slug>.md` | frontmatter `status:` | `open` · `deferred` · `closed` · `retired` · `superseded` |

**Where each domain is declared, so a reader checks rather than trusts:** the disposition set is
the architect ruling of 2026-08-17, carried in code at `scripts/funnel_coverage.py`
(`DISPOSITION_TERMS` + `PENDING_TERM`); the four outcomes are ADR-111 §1; the intake enum is
`docs/intake/README.md` §5, ruled 2026-07-19 and deployed by `[#398]`; the ADR enum is
`scripts/validate_adr_status.py` (`STATUS_ENUM`), which mirrors `docs/decisions/README.md`; the
row domain is `scripts/gen_task_tree.py` (`_TERMINAL_STATUSES`) plus the live `open` / `deferred`
values.

**A second token is what breaks a class.** An object carrying two competing tokens has no state.
Partial ratification of an intake is the case that tempts a second one, and §3.3 records why it
does not get one.

**Where the finding class differs, stated plainly rather than left to §9.** A finding does have
exactly one token — one row in the wave-close table — but that token is stored **in the wave's
table rather than beside the finding**, because a finding is a line inside an immutable artifact
and giving it an in-place token would mean editing that artifact. So finding state is resolved by
reading the wave's table, and the cost of that indirection is §9's first limit.

---

## 3. Transitions — actor and evidence, one row each

A transition is complete when **both** its token change **and** its evidence locator are in the
tree. A token moved without its locator is an assertion; a locator recorded without the token move
leaves the tree stating the old state.

### 3.1 Audit artifact

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | untriaged | the author | the artifact itself |
| untriaged | `PENDING` | any reader | the open question, recorded in the ledger row |
| untriaged · `PENDING` | `ACTIONED` | whoever verifies the conclusion is already live | the commit that made it live |
| untriaged · `PENDING` | `FILED` | the integrator at a wave close | the row id, open at the moment of writing |
| untriaged · `PENDING` | `REJECTED` | the ruling actor | the ruling that declined it |
| untriaged · `PENDING` | `SUPERSEDED` | the author of the successor | the later artifact |

**Terminal:** the four ruled terms. **`PENDING` is live, not terminal** — it records that the
artifact was looked at and its open question is written down, which is a different fact from
absence, and collapsing the two discards the only signal that says whether work happened.

**An artifact may disposition itself** at authoring time, which is what gives a new audit a
discharge path that requires editing no immutable file.

### 3.2 Finding

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | untriaged | the lane that recorded it | the artifact line |
| untriaged | `OWNED` | the integrator (wave close, step D4) | an id resolving to a row **open at classification time** |
| untriaged | `DISCHARGED` | the integrator | a locator that **resolves** — a claim of prior practice with no locator is not a discharge |
| untriaged | `CANDIDATE` | the integrator | the intake-id it becomes or joins; **or** a `Proposed` ADR with the Decision left blank, where ADR-98 §3's fork test is met |
| untriaged | `REJECTED` | the ruling actor | the reason, recorded where the finding lives |

**Exactly one outcome per finding**, and all four are terminal — a finding does not re-enter the
machine. A later, different finding about the same subject is a new object with its own row.

The wave close's five classifications map onto these four with no fifth vocabulary: `COVERED` is
`OWNED`, `MECHANICAL` is `DISCHARGED`, `ADR` and `INTAKE` are both `CANDIDATE`, `REJECT` is
`REJECTED`.

**Archival: none.** A finding lives inside its artifact, and §4 keeps the artifact where it is.

### 3.3 Intake doc

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | `SEED` | a feed (`/changelog-review`), or a seat dropping a candidate | the doc |
| *(birth)* | `DRAFT` | a functional-architect conversation that cleared **the ADR-98 §4 confirm-gate** for landing | the approval that let the doc enter the folder |
| `SEED` | `DRAFT` | the functional architect (`--mode functional`) | the doc filled to the template's eight sections |
| `DRAFT` | `READY` | **the operator** | the approval of the **content**, which is the meaning `READY` carries; a doc may be born straight at `READY` when one operator act covers both landing and content |
| `READY` | `ACCEPTED` | the technical architect, or the operator | `decided-by:` **and** `disposition:`; `disposition: deferred` additionally requires `trigger:` or `review-date:` |
| `READY` · `ACCEPTED` | `CONSUMED` | the seat that lands the last consumer | `consumed-by:` naming the ADR(s), row(s) or consolidating doc |
| any live | `SUPERSEDED` | the author of the successor | `superseded-by:` |
| any live | `REJECTED` | the technical architect | `reason:` — one line, and the doc is kept, because "rejections are knowledge, not garbage" |

**`ACCEPTED` is live, not terminal.** A doc accepted as a standing authority stays visible in
`docs/intake/`; that is deliberate and it is unchanged here.

**The `ACCEPTED` → `CONSUMED` trigger, ruled explicitly because it was the missing join.** The
transition fires when **every row whose `source:` clause names this `intake-id` carries a terminal
`status:`**.

Membership is the **`source:` clause specifically, not any mention of the id.** The two are
genuinely different sets and the difference is measurable on live rows: `tasks/608-*.md` mentions
intake #49 in its body while its `source:` clause names intake #59, so a body-wide search would
attribute it to the wrong doc. A mention is context; the `source:` clause is provenance, and only
provenance decides membership. A reader resolves the set with one search over that clause.

A doc with **zero** rows naming it in a `source:` clause does not reach `CONSUMED` by this route at
all — it leaves `ACCEPTED` by ruling, as `SUPERSEDED` or `REJECTED`. Until the condition holds the
doc is a live authority; from then on it is a record
of one, and `consumed-by:` names what it produced. An accepted intake whose rows are all terminal
and whose status still reads `ACCEPTED` is an **unfired transition**, which is a defect in the
tree — and it is *that* defect, rather than any rule about archiving `ACCEPTED`, that a check on
this class detects.

**Partial ratification is not a transition** and adds no token. Where an ADR ratifies part of a
doc, the doc keeps its pre-ratification status and gains a pointer to the ADR; the ratified part
is relied on **at the ADR**, which is the artifact with its own status, date and `decided-by`.

**Terminal:** `CONSUMED`, `SUPERSEDED`, `REJECTED`.

### 3.4 ADR

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | `Proposed` | any seat, where ADR-98 §3's fork test is met | the draft, Decision blank until ruled |
| `Proposed` | `Accepted` | the ruling actor per ADR-108 §A | the ruling, named in the header |
| `Proposed` · `Accepted` | `PARKED` | the ruling actor | the ruling, plus what un-parks it. The live instance parked **from `Proposed`** |
| `Proposed` | `Explored, not adopted` | the ruling actor | the ruling, and what stays canonical instead. The status records an option priced and left untaken |
| `Accepted` | `Partially superseded` | the author of the partial successor | the successor, and which part of this ADR stays live |
| `PARKED` | `Proposed` · `Accepted` | the ruling actor | the ruling that un-parks it, naming which. `PARKED` returns to `Proposed` where the un-parking only re-opens the question, and goes straight to `Accepted` where the un-parking ruling also decides it |
| `Accepted` · `Proposed` | `Superseded` | the author of the successor | the successor ADR id |
| `Accepted` | `Deprecated` | the ruling actor | the ruling, and the note that it defines no live machinery |

The status line is the **one** in-place edit an immutable ADR admits — metadata, not decision
content. Every other change to a ratified ADR lands as an in-file amendment marker.

**A correction is not a transition, and conflating the two makes the graph unreadable.** ADR-45 is
the live case: it was accepted, then carried a supersession claim that was **withdrawn**, then had
its status *clarified* to `Explored, not adopted` under an audit finding. That last step repaired a
token that had been wrong; it did not move the ADR through the machine. A correction rewrites the
token to what it should have read, cites the finding that caught it, and leaves the transition
history alone — so a reader reconstructing the graph from git skips corrections rather than
inventing edges for them.

**Terminal:** `Superseded` and `Deprecated`. `PARKED`, `Partially superseded` and
`Explored, not adopted` are **live**: each was retained on the record as convention or as
historical authority, and each is still cited.

### 3.5 Backlog row

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | `open` | the seat filing it | a **row-body `source:` clause** that resolves — a **ratified intake**, or a landed adjudication packet, in which case the row also cites the packet row id it executes. The clause sits in the row body beside `refs`, not in frontmatter |
| `open` | `deferred` | the ruling actor | the reason, in the row body |
| `open` · `deferred` | `closed` | the seat that finishes it | the commit carrying `closes [#id]` |
| `open` · `deferred` | `retired` | the ruling actor | the ruling that withdrew it |
| `open` · `deferred` | `superseded` | the seat filing the successor | the successor row id |

**Birth is the guarded edge.** The only routes to `open` are (i) a ratified intake, and (ii) a
landed adjudication packet under its two guards — the row names the packet row id one-to-one, and
the packet is in-repo, immutable and pointed at by the ruling register. An unlanded or still-
editable packet confers no birth rights at all. Outside those two routes, "a finding may not
become a backlog row without triage".

**`closed` requires `closes`, not `advances`.** The detector that proposes closures keys on
`closes [#id]`, so an arc finished entirely with `advances` leaves a done row `open` and
undetected. The commit that **finishes** an item carries `closes`.

**Terminal:** `closed`, `retired`, `superseded`.

---

## 4. Terminal conditions and archival — who archives what, and when

| Class | Terminal states | Archival act | Destination | Basis |
|---|---|---|---|---|
| Audit artifact | `ACTIONED` `FILED` `REJECTED` `SUPERSEDED` | **no file movement** — the grouping in the generated index moves, count-tiered at ~20 most recent | `docs/audits/README.md`, "a section of the index, not the filesystem" | ADR-100 §1–§3 |
| Finding | all four outcomes | none — it lives inside its artifact | — | §3.2 |
| Intake doc | `CONSUMED` `SUPERSEDED` `REJECTED` | **byte-identical relocation** | `docs/intake/archive/` | operator ruling 2026-07-22, archive-inside-each-folder |
| ADR | `Superseded` `Deprecated` | **byte-identical relocation, ruled** (see the two-part bar below) | `docs/decisions/archive/` | commit `216ce3a8`, 2026-07-22 — "Byte-identical moves." |
| Backlog row | `closed` `retired` `superseded` | **none — the row file stays where it is**, carrying its terminal `status:` | — | the row leaves the generated view, not the tree |

**`tasks/archive/` is not this machine's archive, and reading it as one inverts it.** That
directory holds row *narration* relocated verbatim out of rows that are **still open and still in
the queue**, as doc-rot relief; its own mechanism **refuses a retired row**, on the ground that a
retired row is an allocation record and rewriting it would be ledger tampering. So it fires on
**live** rows and declines terminal ones — the exact opposite of a terminal-state archival — and it
is named here only so the next reader does not wire it in.

**The ADR bar has two halves. A terminal status makes an ADR *eligible*; a recorded ruling naming
it makes it *archived*.** The second half is a ruling rather than a computed predicate, and that is
a measured conclusion rather than a preference — the alternative was tried against the landed
record and does not survive it:

- **ADR-52** (`Superseded`) was archived by commit `216ce3a8` while carrying **13 inbound files**
  — `JOURNAL.md`, five audits, two handoff bundles, `ADR-53`, both READMEs. Zero of them were
  living docs.
- **ADR-40** (`Deprecated`) was archived in the **same commit** while carrying inbound references
  in `VISION.md` **and** `protocols/PLAYBOOK.md` — both living docs.
- **ADR-45** stayed, and the commit body gives the reason: three prose references in
  `protocols/PLAYBOOK.md`.

No inbound count reproduces that set: a tracked-file count archives neither, and a living-doc count
archives ADR-52 but refuses ADR-40. The commit body's own phrase, "the zero-refs bar", therefore
describes **neither** archived case. What both archived ADRs share is one thing — an **operator
ruling of 2026-07-22** that named them. So the honest rule is the one that reproduces the record:
**terminal ⇒ eligible, and a recorded ruling archives.** Two readers looking at any ADR agree on
its eligibility mechanically, and agree that an eligible-but-unruled ADR stays put.

**Archiving a cited ADR breaks locators that immutable files cannot re-point**, which is why the
ruling — not a counter — is where the judgement sits. A ruling that archives an ADR is expected to
say what it did about the citations it leaves behind; §8's Fork 1 carries the open half.

**The audit class is the exception, and it is a ruled one.** Audit files are the evidence spine:
roughly four in five citation lines to them sit in immutable or append-only documents that cannot
be re-pointed, so a physical move breaks references permanently. Any future physical move of an
audit file requires **both** a referential-currency scan **and** an explicit architect ruling.

**When: the archival act rides the same commit as the transition that made the object terminal** —
for every class whose archival condition **is** the transition — which, once the row class is
excluded above, is the **intake doc**. This is the rule with the most leverage in this file and the one no
source states. An object that became terminal in commit A and is relocated in commit B leaves a
window in which the tree contradicts itself — and every window of that kind observed so far stayed
open, because the second commit had no owner and no trigger. **For the intake class the transition is
incomplete until its archival act lands.** Where the two fall to different actors, the actor who
moves the token owns the relocation too, or hands it over by name.

**The ADR class sits outside that rule, structurally rather than by exemption.** Its second
archival half is a **ruling**, which is an act by someone else at a time this transition does not
control. So an ADR's archival becomes **owed at the moment a ruling names it**, which is normally
later than the status edit, and §6's job-1 item 2 counts eligible-and-ruled ADRs from that moment
forward — not merely eligible ones. ADR-52 is the worked case: status moved 2026-05-19, archived
2026-07-22, and that two-month gap is conformance rather than debt.

**What "byte-identical" governs: the move, not the whole commit.** The relocation itself introduces
no content change, so the file arrives at its archive path carrying exactly the bytes it had once
the transition was recorded. Writing the terminal token and moving the file in one commit therefore
yields a rename plus that one edit, and a reader diffing the two paths sees the transition and
nothing besides it.

**Deletion is outside this machine.** Every archival act here is a relocation with the bytes
unchanged; content edits and deletions are a different question with a different authority.

---

## 5. The `READY` threshold — ruled here, as a number

**N = 30 days.**

**Justification, one line:** ADR-98 §6 already fixes *~1 month* as the interval at which
unconsumed intake becomes a signal, so 30 days is that ruled interval read as a fixed number of
days rather than a second clock introduced against the same object.

**The clock starts** at the commit date of the most recent commit that set the doc's `status:` to
`READY`. Intake frontmatter carries no transition-date field, and this file adds none — the git
date is the dated transition.

**Crossing 30 days is a WARN, not a FAIL.** An intake waiting on its consumer is a statement about
capacity, not a defect in the document; the WARN exists so the wait is visible rather than silent.

**Discharge** is a recorded ruling naming the `intake-id` — a `protocols/STANDING_RULINGS.md`
entry, or a landed adjudication packet. It is deliberately **not** a new frontmatter key: the
intake schema is closed, an off-schema key breaks the generated index, and a ruling is the
artifact that already carries a reason and an author.

**FM-2 binds to this number.** The check's `READY`-age leg reads 30, and if this number changes it
changes here first.

---

## 6. The session's two standing jobs

Every session carries both. They are not a wave-close ceremony — a wave close is where they are
*reported*, and a session is where they are *owed*.

**Job 1 — funnel coherence: everything consumed, numbered, archived at terminal state.** Four
derivations, each a count with a list behind it:

1. **Unfired transitions** — objects whose transition condition is met and whose token has not
   moved. Chiefly §3.3's `ACCEPTED` intakes whose rows are all terminal.
2. **Owed archival** — objects at a terminal state whose §4 archival act has not landed. For ADRs
   the two-part bar applies, so an **eligible-but-unruled** ADR is reported as *eligible*, not as
   owed; only an ADR a ruling has named and nobody moved is owed.
3. **Orphans, both directions** — an artifact with no consumer and no rejection record; and an open
   row whose row-body `source:` clause is absent or does not resolve.
4. **Untriaged** — audit artifacts carrying no disposition row at all, which is distinct from
   `PENDING` and counted separately.

**Job 2 — value audit: what shipped, what it bought, measured.** Per row closed in the window, the
"what it bought" line sourced from its close packet. A closed row with no such line is reported as
an unmeasured close rather than counted as value.

**A1 — where the numbers go.** Both jobs emit **time-series records into the existing telemetry
store**, `logs/TELEMETRY.db` (`scripts/telemetry_emit.py`; one append-only `events` table with a
`run_id` correlation column, gitignored, derived views read from it). **No second store is
created.** The event-type domain is closed at three — `check_run`, `hook_run`, `blocker_fired` —
so these records ride as `check_run` with the counts in `context_json`; widening that domain is a
change to the emitter module, not something a caller does on its own.

---

## 7. Sources — what is restated, and what goes further

Restating a ratified clause is safe; extending one silently is the failure this section exists to
prevent. Every row below is one or the other, explicitly.

| Clause | Source | Here |
|---|---|---|
| "Audit = evidence *about* state. Intake (ADR-98) = a request to *change* state." Separate genres, separate lifecycles | ADR-100 §4 | **restated** — §2, §4 |
| Keep-all-accepted; the archive for audits is a section of the index, count-tiered; a physical move is gated on a scan plus an architect ruling | ADR-100 §1–§3 | **restated** — §4 |
| The four triage outcomes, exactly one per finding | ADR-111 §1 | **restated** — §3.2 |
| "A finding may not become a backlog row without triage"; the packet route and its two guards | ADR-111 §2 + amendment 2026-08-25 | **restated** — §3.5 |
| Ratification is the birth authority, recorded in `decided-by` | ADR-111 §3 | **restated** — §3.5 |
| Genre demarcation: intake 0..1 per initiative, ADR 0..n, epic 1..n per accepted intake; acceptance criteria copied verbatim | ADR-98 §3 | **restated** — §2, §3.3 |
| The intake doc is confirm-gated; the operator approves before it lands | ADR-98 §4 | **restated** — §3.3 |
| Unconsumed intake is a signal at ~1 month | ADR-98 §6 | **extended** — §5 turns the interval into a number, for one object class, and states the clock |
| Git is the ledger; the commit that finishes carries `closes [#id]` | ADR-70 Tier 1 + addendum item 2 | **restated** — §3.5 |
| The archival act rides the transition commit, for the intake class | — | **new** — §4. No source states it; the window it closes is observed |
| The ADR archival bar is terminal status **plus a recorded ruling** | practice of commit `216ce3a8`, re-measured | **new** — §4. The commit body's own "zero-refs bar" phrase describes neither archived case, so the rule is derived from what both share |
| `ACCEPTED` → `CONSUMED` fires when every row whose `source:` names the doc is terminal | — | **new** — §3.3, the join no source drew |
| A row's provenance is a `source:` clause in the row body | live convention in `tasks/`, ungoverned by any ADR | **new** — §3.5 makes the clause the evidence for birth. ADR-111's amendment requires a **packet row id** for a packet-born row and defines no `source:` grammar; this is an additional requirement and is named as one |
| State + dated transitions generalize beyond the funnel | operator appendix A1 | **restated as scope** — §1 |

---

## 8. Two forks, named rather than resolved quietly

**Fork 1 — the ADR archival predicate, and it is wider than it first looked.** The FM-2 contract's
FAIL class (b) reads *"ADR superseded/rejected, not archived → FAIL"*. Three frictions with landed
state: `Rejected` is outside the ADR status enum entirely; three live ADRs carry non-`Accepted`
statuses and stay in place by an explicit recorded reason; and, measured in §4, **no inbound-count
predicate reproduces the two archivals that actually happened** — the only property both share is
an operator ruling. Read literally, that FAIL class fires on conformant files. **This file is
written to §4's terminal-plus-ruling bar.** The open half is what a ruling owes about the citations
an archived ADR leaves behind — ADR-40 was archived while cited by two living docs, and nothing
records what became of those locators. Reported as a candidate filing.

**Fork 2 — apparent, and resolved without weakening either side.** `docs/intake/README.md` §5 puts
`ACCEPTED` deliberately outside the terminal set, so an accepted doc is not archived; FM-2's FAIL
class (a) fires on an accepted intake whose rows are all terminal and which is not archived. Both
hold at once under §3.3: `ACCEPTED` is not an archival state, and the condition FM-2 names is the
**trigger for the `ACCEPTED` → `CONSUMED` transition**. It is the unfired transition that is the
defect; the archival act then follows `CONSUMED` under §4. No amendment to either source is
needed, and none is made.

**Fork 3 — `DRAFT` versus `READY`, a fork inside one source.** `docs/intake/README.md` §5 defines
`DRAFT` as *not yet operator-approved* and `READY` as *operator-approved*, while §6 of the same
file has an approved doc land *"at DRAFT or READY"*. Under §5's semantics a landed-at-`DRAFT` doc
is by definition unapproved, so the two readings disagree about what the confirm-gate attaches to.
§3.3 is written to the reading that keeps both true: **the confirm-gate approves the doc's
landing**, and **`READY` records approval of its content** — one operator act often covers both,
which is why a birth straight at `READY` is lawful. Reported as a candidate filing against the
intake README, since the ambiguity is that file's rather than this one's.

---

## 9. Honest limits

- **Nothing here is gated today.** This file is doctrine a reviewer cites. The check that gives it
  teeth is a separate deliverable and is owed; until it lands, conformance rests on seats reading
  this page.
- **Finding-level state has no per-object token in the tree.** A finding is a line, and its outcome
  lives in the wave-close table rather than beside it. So finding coherence is checkable
  **per wave**, not per object — the weakest row in §2, and it is weak by construction rather than
  by oversight.
- **§4's ADR bar leaves the judgement in a ruling, and that is a limit as much as a design.** Its
  mechanical half decides only *eligibility*; the question of which eligible ADR is safe to move is
  answered by an operator, one ADR at a time, and nothing here bounds how long an eligible ADR
  waits. What §4 buys is that two readers agree on the eligible set and agree that an unruled one
  stays put.
- **§3.3's membership rule finds nothing for a pre-convention doc.** The `source:` clause is a live
  convention, not a schema field, and older rows predate it: `tasks/271-*.md` mentions an intake in
  its body and carries no `source:` clause at all. Such a doc's row set reads as empty, which is
  why §3.3 sends the zero-row case out through a ruling rather than letting an empty set satisfy
  the condition — the guard is deliberate, and this is the population it was written for.
- **§5's clock reads git dates.** A status set in a rewritten or squashed commit reads the rewrite
  date, which understates the wait. The alternative — a transition-date field in frontmatter — was
  declined here as a schema change with its own generator cost.
- **§4's same-commit rule has no enforcement and is stated as a rule anyway**, because the class of
  defect it addresses is precisely the one that survives when the rule is left implicit.
