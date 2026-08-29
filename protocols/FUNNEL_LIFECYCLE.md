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

State is a property of the tree, not of anyone's memory. Each class below has exactly one token,
at one location, with one declared domain.

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

**One token per object.** A class carrying two competing tokens has no state. Partial ratification
of an intake is the case that tempts a second token, and §3.3 records why it does not get one.

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
| `SEED` | `DRAFT` | the functional architect (`--mode functional`) | the doc filled to the template's eight sections |
| `DRAFT` | `READY` | **the operator** | the approval — the ADR-98 §4 confirm-gate |
| `READY` | `ACCEPTED` | the technical architect, or the operator | `decided-by:` **and** `disposition:`; `disposition: deferred` additionally requires `trigger:` or `review-date:` |
| `READY` · `ACCEPTED` | `CONSUMED` | the seat that lands the last consumer | `consumed-by:` naming the ADR(s), row(s) or consolidating doc |
| any live | `SUPERSEDED` | the author of the successor | `superseded-by:` |
| any live | `REJECTED` | the technical architect | `reason:` — one line, and the doc is kept, because "rejections are knowledge, not garbage" |

**`ACCEPTED` is live, not terminal.** A doc accepted as a standing authority stays visible in
`docs/intake/`; that is deliberate and it is unchanged here.

**The `ACCEPTED` → `CONSUMED` trigger, ruled explicitly because it was the missing join.** The
transition fires when **every row born of the doc has reached a terminal state and no unexecuted
clause of the doc remains**. Until then the doc is a live authority; from then on it is a record
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
| `Accepted` | `PARKED` | the ruling actor | the ruling, plus what un-parks it |
| `Accepted` | `Partially superseded` · `Explored, not adopted` | the ruling actor | the ruling, and what remains live |
| `Accepted` · `Proposed` | `Superseded` | the author of the successor | the successor ADR id |
| `Accepted` | `Deprecated` | the ruling actor | the ruling, and the note that it defines no live machinery |

The status line is the **one** in-place edit an immutable ADR admits — metadata, not decision
content. Every other change to a ratified ADR lands as an in-file amendment marker.

**Terminal:** `Superseded` and `Deprecated`. `PARKED`, `Partially superseded` and
`Explored, not adopted` are **live**: each was retained on the record as convention or as
historical authority, and each is still cited.

### 3.5 Backlog row

| From | To | Actor | Evidence required |
|---|---|---|---|
| *(birth)* | `open` | the seat filing it | a `source:` that resolves — a **ratified intake**, or a landed adjudication packet, in which case the row also cites the packet row id it executes |
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
| ADR | `Superseded` `Deprecated` | **byte-identical relocation, gated** (see the two-part bar below) | `docs/decisions/archive/` | commit `216ce3a8`, 2026-07-22 — "Byte-identical moves." |
| Backlog row | `closed` `retired` `superseded` | **the row file stays**; only its dated annotation history relocates | `tasks/archive/<id>.md` | the row-body archival mechanism, `[#612]` |

**The ADR bar has two halves and both are load-bearing.** A terminal status makes an ADR
*eligible*; **zero live inbound references** makes it *archivable*. An ADR that is `Superseded`
and still cited by live prose stays where it is, and that is conformance rather than debt — the
landed precedent says so in its own commit body, which archived two ADRs and left three
non-`Accepted` ones in place for exactly this reason. Archiving a cited ADR breaks locators that
immutable files cannot re-point.

**The audit class is the exception, and it is a ruled one.** Audit files are the evidence spine:
roughly four in five citation lines to them sit in immutable or append-only documents that cannot
be re-pointed, so a physical move breaks references permanently. Any future physical move of an
audit file requires **both** a referential-currency scan **and** an explicit architect ruling.

**When: the archival act rides the same commit as the transition that made the object terminal.**
This is the rule with the most leverage in this file and it is the one no source states. An object
that became terminal in commit A and is relocated in commit B leaves a window in which the tree
contradicts itself — and every window of that kind observed so far stayed open, because the second
commit had no owner and no trigger. **The transition is incomplete until its archival act lands.**
Where the two are performed by different actors, the actor who moves the token owns the relocation
too, or hands it over by name.

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
2. **Owed archival** — objects at a terminal state whose §4 archival act has not landed. For ADRs,
   the two-part bar applies, so an eligible-but-cited ADR is **not** counted here.
3. **Orphans, both directions** — an artifact with no consumer and no rejection record; and an open
   row whose `source:` does not resolve.
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
| The archival act rides the transition commit | — | **new** — §4. No source states it; the window it closes is observed |
| The ADR archival bar is terminal status **and** zero live inbound | practice of commit `216ce3a8` | **extended** — §4 writes the landed practice as a rule for the first time |
| `ACCEPTED` → `CONSUMED` fires when every born row is terminal | — | **new** — §3.3, the join no source drew |
| State + dated transitions generalize beyond the funnel | operator appendix A1 | **restated as scope** — §1 |

---

## 8. Two forks, named rather than resolved quietly

**Fork 1 — the ADR archival predicate.** The FM-2 contract's FAIL class (b) reads *"ADR
superseded/rejected, not archived → FAIL"*. Two frictions with landed state: `Rejected` is outside
the ADR status enum entirely, and three live ADRs carry non-`Accepted` statuses and stay in place
by an explicit recorded reason. Read literally, that FAIL class fires on conformant files. **This
file is written to the two-part bar of §4** — terminal **and** zero inbound — which is the reading
the landed precedent supports. Reported as a candidate filing; a ruling that prefers the literal
form amends §4 here first.

**Fork 2 — apparent, and resolved without weakening either side.** `docs/intake/README.md` §5 puts
`ACCEPTED` deliberately outside the terminal set, so an accepted doc is not archived; FM-2's FAIL
class (a) fires on an accepted intake whose rows are all terminal and which is not archived. Both
hold at once under §3.3: `ACCEPTED` is not an archival state, and the condition FM-2 names is the
**trigger for the `ACCEPTED` → `CONSUMED` transition**. It is the unfired transition that is the
defect; the archival act then follows `CONSUMED` under §4. No amendment to either source is
needed, and none is made.

---

## 9. Honest limits

- **Nothing here is gated today.** This file is doctrine a reviewer cites. The check that gives it
  teeth is a separate deliverable and is owed; until it lands, conformance rests on seats reading
  this page.
- **Finding-level state has no per-object token in the tree.** A finding is a line, and its outcome
  lives in the wave-close table rather than beside it. So finding coherence is checkable
  **per wave**, not per object — the weakest row in §2, and it is weak by construction rather than
  by oversight.
- **The zero-inbound half of §4's ADR bar is a reference scan**, and that scan has a recorded
  floor: the citation census behind ADR-100 covered the doc corpus only, leaving audit-to-audit and
  `ecosystem/*.yaml` references unscanned. A count derived from it is a lower bound.
- **§5's clock reads git dates.** A status set in a rewritten or squashed commit reads the rewrite
  date, which understates the wait. The alternative — a transition-date field in frontmatter — was
  declined here as a schema change with its own generator cost.
- **§4's same-commit rule has no enforcement and is stated as a rule anyway**, because the class of
  defect it addresses is precisely the one that survives when the rule is left implicit.
