---
intake-id: 66
status: READY
origin: operator direction, stated 2026-09-01 under the binding rule "reconcile-before-birth — amend #62/#617/HY-2/HY-4/A2 where they carry it, birth only the gap"; filed after a reconcile pass that moved five of the seven legs onto existing carriers
consumed-by:
---

# The OBSERVABLE HARNESS — four layers, one home each, and the layer that has no home at all

<!-- class: tech (structural/ownership question) · status: READY (operator-approved on the
dashboard-home ruling, 2026-09-01; see the AMENDMENT at the foot) — NOT ratified; BINDS
NOTHING. Non-citable as doctrine until ratified; the repo wins on any conflict. -->
<!-- origin: operator direction, 2026-09-01 -->

> **DRAFT BINDS NOTHING.** This file records operator direction and the ruling-level questions it
> raises. It authorises **no new folder**, no ADR-101 amendment, no edit to any gate, and no
> backlog row. Nothing below is doctrine until this intake is ratified.

## Problem / motivation

The repo observes itself in pieces that do not share a shape. `logs/` holds sixteen-odd flat
UPPERCASE artifacts in at least four different formats; `ecosystem/conformance.html` is a
committed trust surface; `ecosystem/trends.html` is a gitignored on-demand render; the closure
proposals are a dated flat series two callers glob by prefix. Each was built correctly for its own
purpose. **Together they have no declared layering**, so there is no answer to the question the
operator actually asks — *where does a new observation go?* — and every new observing organ makes
that question harder rather than easier.

The operator's direction of 2026-09-01 states the target shape as **four layers with exactly one
home each**:

1. **MECHANISM** — `scripts/`. The code that observes.
2. **DOCTRINE** — `protocols/`. The **event contract**: what is logged, and when.
3. **TRACE** — `logs/`, as **append-only structured streams** rather than flat prose files.
4. **VIEW** — a **`dashboard/`** at the repo root, generated **only** from layers 1–3, a single
   self-contained HTML file openable in VS Code.

**The reconcile is the substantive act, and it moved most of this off this intake.** Most of the
legs the direction names turned out to be carried by live objects, and have been **amended onto
them** rather than restated here — the ledger below is the enumeration, and it is the evidence for
this filing's scope. What is left, and what this intake exists for, is **layer 2 — the DOCTRINE
layer, which nothing in the repo carries at all** — plus the layering rule itself.

**What happens if this stays unaddressed:** the next observing organ is placed by precedent rather
than by rule, exactly as `logs/` was — and `logs/` is the surface the operator has already
complained never visibly thins (`[#626]`). A layering that exists only as the shape of what
happened to be built is not a contract, and cannot refuse a wrong placement.

## The reconcile ledger — what was AMENDED, and what is genuinely unowned

> This section is the filing's evidence, not its narrative. **AMENDED** means an amendment was
> landed on the named carrier in the same act that filed this intake. **NOT A GAP** means the
> carrier already says it and nothing was written — the honest outcome of a reconcile, and the one
> that keeps this file small.

| Leg of the direction | Carrier | Disposition |
|---|---|---|
| Distiller trace doubles as the **eval corpus** for the skills admission gate (SkillsBench) | intake **#62** amendment + `[#617]` | **CARRIED — amended.** #62 already rules the admission gate and the eval-loop precondition; #617 already owns the distiller. The *corpus* coupling was the only new clause. |
| `logs/prompts/` — the distiller trace stream itself | `[#617]` | **CARRIED — amended.** #617 owns the distiller; its trace had no declared home. |
| `logs/proposals/` under a retention rule | `[#626]` (HY-2 residual) | **NOT A GAP.** `[#626]`'s done-when *is* this relocation, including the two flat-globbing callers. Restating it here would have duplicated an open row. |
| `logs/telemetry/` — per model, per lane, gate time, rows closed per day | intake **#50** (READY) **+ a four-row telemetry arc** | **NOT A GAP — and this is the reconcile's sharpest result.** A telemetry store is already **specified, built and partly landed**: `[#529]` (emit stage-1 events from the gate mesh) and `[#565]` (`run_id` in emit) are **CLOSED**; `[#575]` (store performance, silent drops under concurrent writers) and `[#576]` (the read path) are **OPEN**. The store has a declared home — **`logs/TELEMETRY.db`**, a **gitignored sqlite** file — cited by name in `gen_trend_dashboard.py`'s input table. Filing `logs/telemetry/` as a new stream would have **duplicated a live arc**. |
| VIEW is generated **only** from layers 1–3 — no hand-entered numbers | `scripts/gen_trend_dashboard.py` (HY-4, landed) | **ALREADY IMPLEMENTED for one artifact.** Its docstring states the rule in as many words — *"INPUT IS THE STORE — and the store is git. Nothing here computes a metric from scratch, scrapes a doc, or accepts a hand-entered number"* — and `test_output_is_pure_ascii` plus the no-second-store clause hold it closed. The rule exists; what it lacks is **generality**, which is this intake's business. |
| `dashboard/` at ROOT + ADR-101 amendment + root-contract update | intake **#38** amendment | **CARRIED — amended,** on the 2026-08-29 wave-2 precedent that the root-contract maps to #38 rather than to a fresh intake. Two blocking findings recorded there (below). |
| VIEW is local self-contained HTML in VS Code, never cloud | intake **#9** (SEED) | **NOT A GAP.** #9 is this clause, verbatim, from 2026-07-08 — *"a file openable inside VS Code in-session, self-contained, zero external hosting"*. This intake cites it and adds nothing. |
| `conformance.html` MIGRATE-not-delete; its one honest question becomes an atlas panel; two live consumers re-pointed | intake **#42** amendment | **CARRIED — amended.** #42 is the artifact-currency home and already quotes the honest question in its own scenario. |
| **The four-layer rule itself, and the DOCTRINE layer (`protocols/` event contract)** | **nothing** | **THE GAP. This intake.** |

**HY-4 and A2 have no amendable open carrier, and that is stated rather than skipped.** HY-4
landed as **code** — `scripts/gen_trend_dashboard.py`, whose burn-down panel is live at
`build_arc_burndowns` / `render_burndown_panel` — with no open row to amend; its only open citation
is inside `[#617]`. A2 landed as `docs/audits/2026-08-31-census-templates-consumers.md`, an
**immutable audit**. Neither can take an amendment, so both legs are recorded here instead, which
is why this intake names them at all.

### The VIEW layer already names the TRACE layer that does not exist — and that sets the ordering

The strongest evidence for this intake is not an argument, it is an artifact that has been asking
for the missing layer by name since it was written. `gen_trend_dashboard.py`'s input table declares
**three ABSENT series**, each rendered as a first-class absence with its reason printed in the
legend rather than omitted:

- `commit-gate ms` — store **declared** (`logs/TELEMETRY.db` `events.duration_ms`), **no rows**;
- `suite wall-time` — *"no store exists"*;
- `per-model quality` — *"no store exists"*.

Those three are, near-exactly, what the direction asks `logs/telemetry/` to carry — **gate time,
per lane, per model**. The VIEW layer was built to make their absence visible, on the stated
principle that *"a chart of invented history is worse than no chart, and the two 'no store exists'
rows are findings this surface exists to make visible rather than gaps it should quietly paper
over."*

**Two consequences, both load-bearing.** First, the **ordering is settled by evidence rather than
preference: TRACE before any VIEW expansion** — building more panels before the stores exist adds
more absences, not more answers. Second, this hands the harness a **ready-made acceptance test**:
when the TRACE layer lands, three named panels flip from ABSENT to a rendered series, and nothing
else about the page changes. That is a mechanical pass/fail, not a judgment call, and it is why
acceptance criterion 6 below can be stated at all.

## Scenarios (+1 view)

- As the architect placing a new observing organ, I read one rule that tells me which of four
  layers it belongs to, and the rule refuses the placement that would put a renderer in `logs/` or
  a trace in `scripts/`.
- As the operator, I open **one** file — the dashboard — and every panel on it is derived from
  layers 1–3, so nothing on the page is a number somebody typed.
- As a gate, I read the **event contract** and can answer "should this have been logged?" — today
  that question has no authority to consult, so an absent log entry is indistinguishable from an
  event that correctly produced none.
- As a consumer repo, I receive the dashboard the way I receive every other organ — through a
  deploy carrier — rather than by hand-copy.
- As the operator six months from now, `logs/` has thinned, because every stream in it was born
  under a retention rule instead of acquiring one afterwards.

## Functional requirements

- **Must:** state the four layers and the **one home each**, as a rule a placement decision can be
  checked against — MECHANISM `scripts/` · DOCTRINE `protocols/` · TRACE `logs/` · VIEW `dashboard/`.
- **Must:** state the **event contract** — *what* is logged and *when* — as doctrine in
  `protocols/`. This is the layer with no current home and the reason this intake exists.
- **Must:** the VIEW layer is generated **only** from layers 1–3. A panel with a hand-entered
  number is a contract violation, not a shortcut.
- **Must:** every TRACE stream is **append-only and structured**, and is born **under the HY-2
  retention rule** rather than acquiring one later — which is the failure `[#626]` records.
- **Should:** `dashboard/` deploys to every consumer as an **organ**, via the existing carrier
  mechanism, not by copy.
- **Should:** the prompt-distiller trace (`logs/prompts/`) is **also the eval corpus** for the
  skills/commands admission gate — one artifact, two consumers. Recorded as a coupling so the
  corpus is not built twice; the gate itself is intake #62's.
- **Could:** consume the library-first survey the direction names as **ATLAS-R1** when it lands
  (see open question 3 — the identifier does not currently resolve).

## Acceptance criteria (ex-ante)

1. A ruling records whether **`dashboard/` may exist at the root**, given that the closed Tier-1
   set's only contraction to date was the **revocation of a root folder on this exact reasoning**
   (open question 1). No layering work proceeds on the VIEW layer before that answer.
2. The four-layer rule is stated once, in one home, and **names the surface that checks each
   layer's boundary** — or declares that boundary unasserted in the same breath, on the
   ROOT-CONTRACT C1 precedent.
3. The event contract exists in `protocols/` and, for each stream under `logs/`, says what event
   writes to it and when. A stream with no clause is a defect the contract can name.
4. `ecosystem/conformance.html` is **retired without loss**: its honest question renders as a
   dashboard panel, and **both** live consumers resolve — `generated_artifact_freshness.py`'s
   `conformance-dashboard` tuple (`outputs=("ecosystem/conformance.md", "ecosystem/conformance.html")`)
   and intake #42's scenario. A fire-test proves the freshness tuple REDs on a stale new target.
5. No TRACE stream is created without its retention clause landing in the same act.
6. **The three ABSENT panels flip.** When the TRACE layer lands, `gen_trend_dashboard.py` renders
   `commit-gate ms`, `suite wall-time` and `per-model quality` as **series rather than absences**,
   with no other change to the page and no hand-entered value anywhere in the input path. This is
   the harness's end-to-end test: a trace written by layer 3 reaching layer 4 through layer 1
   alone.

## Non-goals

- **No folder is created here, and none is authorised.** `dashboard/` is a *request* recorded on
  intake #38; creating it before ADR-101 admits it is the exact move `validate_hermetization.py`
  Rule A exists to block.
- **Not the telemetry content, and not a second telemetry store** — that is intake #50 plus the
  live arc (`[#529]`/`[#565]` closed, `[#575]`/`[#576]` open) writing to `logs/TELEMETRY.db`. This
  intake must not mint a rival stream beside it.
- **Not the retention mechanism** — HY-2 built it and `[#626]` owns its unfinished half.
- **Not the admission gate or the eval loop** — intake #62 and `[#617]`.
- **Not a deletion of `conformance.html`.** MIGRATE, then retire; the direction is explicit and
  the artifact is a committed trust surface with two live readers.
- Not the graph — intake #40.

## Impact sketch (4+1 lite)

- **Logical:** turns four accidentally-separate observation surfaces into a declared layering with
  a placement rule.
- **Process:** every future observing organ gets its home from a rule instead of from precedent;
  the operator's "where does this go?" stops being a per-artifact judgment.
- **Development:** the DOCTRINE layer is one new `protocols/` document. The VIEW layer is a
  relocation plus a panel migration, **gated on question 1**. The TRACE layer is mostly re-pointing
  existing producers, and is largely `[#626]`'s and #50's work rather than new code.
- **Physical:** one new root directory **if and only if** ADR-101 admits it; three stream
  directories under an already-sanctioned top-level. No new dependency.

## Open questions

1. **May a new folder exist at the ROOT, and does this one clear the bar that revoked the last
   one?** This is the ruling-level question and it is **not** rhetorical. On **2026-08-26** an
   operator ruling **revoked** the root `prompts/` directory admitted the previous day, on the
   stated reasoning *"root is sacred, and the docs disease is cured by the consumer gate ([#595]),
   not by a sibling folder at the root"* — and the closed set **shrank by one, the first and only
   contraction it has taken** (`scripts/validate_hermetization.py:86-93`, and quoted again in
   intake #38's ROOT-CONTRACT C2 as *the standing precedent*). The current direction asks the
   operator to sanction a root folder that is a sibling of `ecosystem/`, where both HTML artifacts
   live today. **This intake does not self-rule it.** The operator directed the sanction and may
   well rule the same way again — a *generated view surface* is arguably a different class from a
   *dispatch-input folder* — but the precedent is three days older than the direction and is
   recorded here so the ratification reads it rather than rediscovers it.

2. **What does a root `dashboard/` actually buy, given that its contents may be invisible to the
   fleet's only retrospective root check?** `ecosystem/trends.html` is **gitignored**
   (`.gitignore:84`) and `ecosystem/conformance.html` is **committed** — the two artifacts the
   direction folds into one folder are in **different zone classes**. ROOT-CONTRACT C1's second
   honest limit records that `fleet_parity.py::_eval_sweep` sees **TRACKED entries only**; a
   `dashboard/` holding only generated-and-ignored output would therefore be **undetectable by the
   fleet sweep by construction**, and a `root-dashboard` parity row would have nothing to observe.
   Either the dashboard is committed (and joins the committed-generated class whose currency rule
   intake #42 says does not exist yet), or it is ignored (and the root sanction buys less
   enforcement than it appears to). **Both halves cannot be true at once, and the direction does
   not say which.** Technical-architect question, recorded not answered.

3. **`ATLAS-R1` does not resolve, and is recorded as UNLOCATABLE rather than assumed.** The
   direction says this intake *"consumes ATLAS-R1's library-first survey when it lands"*. Searched
   over tracked files: `git grep -in "atlas"` returns **no lane, round, batch or artifact by that
   name** — the only hits are `Atlassian` (a company, in two audits) and `ATLAS-GATE-MCP` (an
   unrelated external repo cited once in archived research). `library-first` resolves richly, but
   to the **2026-08-09 archived research set** and ADR-112's Tier L/S bar, not to anything named
   ATLAS. The phrase *"when it lands"* implies future work, so this is most likely a **batch-G lane
   not yet dispatched** — but that is an inference, and the identifier is recorded as unresolved so
   a later reader does not hunt for a survey that was never filed under that name.

4. **Does the DOCTRINE layer belong in `protocols/` beside ESSENTIALS/PLAYBOOK, or in `ecosystem/`
   beside the machine-read registries?** The direction says `protocols/`. This is the **same fork**
   intake #62 open question 4 and `[#613]` are both parked on — *where does a hub-side authority
   live* — and the three should be decided **once**, together, rather than three times.

5. **What IS a "structured stream" — and does `logs/` need a fourth format to get one?** `logs/`
   already carries **four** shapes: dated Markdown (the bulk), `PARITY-EVENTS.jsonl`,
   `OPERATOR-LOAD.csv`, and a **gitignored sqlite store** `logs/TELEMETRY.db` that is *declared and
   does not exist on disk*. Two consequences the direction does not resolve. **(a)** HY-2's
   retention mechanism buckets **dated filenames**; a genuinely append-only single-file stream
   carries no date in its name and sits outside that mechanism entirely — so format and retention
   are **one decision, not two**. **(b)** A **gitignored** store is invisible to any git-derived
   view, which is the store class the telemetry arc already chose; if the harness wants its traces
   readable by a git-history reader, that is a **reversal** of a live decision and needs to be
   ruled as one rather than assumed. Technical-architect question; not answered here.

## Landed inputs (ATLAS-R1, 2026-09-01)

Two artifacts landed under `docs/audits/` on the day this intake was filed, each recorded here
as the consumer at landing. **Both are HTML views landed VERBATIM with a markdown sidecar**
(architect's format ruling): a generated view is not rewritten by hand, and the `.md` twin is
what this intake cites.

- **`docs/audits/2026-09-01-technical-atlas-r1-layer-graph.md`** — feeds the **`docs/dashboard/`
  view**. It is the worked example of what that view renders: 1,783 nodes and 11,515 edges
  collapsing into **12 aggregate cells**, which is the finding that makes a whole-graph render
  possible at all. It also settles the reconcile-before-birth question for the dashboard leg —
  four incumbents were measured and only `file_purpose_graph.py` overlaps, by owning a real
  `rustworkx` graph with **no view of the whole**.
- **`docs/audits/2026-09-01-census-atlas-r1-def-usage-ledger.md`** — feeds the **telemetry
  stream**, and it is the measured statement of what that stream would have to carry. Across 31
  lanes in three batches, **credits recorded: 0** — no receipt carries a cost,
  `logs/TOKEN-LOG.md` is a host-wide weekly aggregate that cannot attribute a lane and stops 25
  days before the window opens, and the codespace probe burned real compute and recorded none.
  **Until `[#615]` lands, per-lane attribution is underivable, not merely unrecorded.** That is
  question 5's premise, measured rather than asserted.

## OPERATOR ASKS — the fifth section, and the one the organ renders FIRST

**Added 2026-09-01 from operator direction, on lesson L-S7:** *an operator ask that is answered by
"filed in arc X" is NOT addressed from the operator's seat — a visible change, or a named
blocker with its date, is.* Filing is the repo's answer to itself. From the seat that asked, a row
id is indistinguishable from silence, and the ask comes back.

**The mechanism, and it is deliberately not prose.** The v7 boot bundle and the FUNNEL HEALTH
digest both carry an **OPERATOR ASKS** section. Each ask is a record, not a sentence:

```
asked            <date>            when it was first raised
visible-fix      <sha | path>      the change the operator can SEE, or empty
blocker          <text + date>     required when visible-fix is empty -- a NAMED blocker
                                   carrying its own date, never "filed as [#N]"
owner            <id>              the row, arc or seat that owns it
re-asked         <n>               incremented every time it is raised again
```

**The teeth: `re-asked >= 2` with no visible-fix renders RED** — at boot and in the close
packet, as a status, not a paragraph. An ask that has been raised twice and produced nothing
visible is a failure of the loop, and the loop is what this intake is about. A blocker discharges
the RED only if it is NAMED and DATED; "tracked in [#N]" is exactly the answer L-S7 rules
insufficient.

**The `/boot-session` organ renders this section FIRST**, above funnel health and the proposed
batch. A seat that opens the bundle sees what the operator is still waiting for before it sees
what the repo would like to do next.

### Seed entries, 2026-09-01

```
ESSENTIALS de-bless    asked 2026-09-01  re-asked 3  visible-fix: this merge (CLAUDE.md sends
                       nobody to it; ESSENTIALS status: superseded)          -> GREEN
VISION.md out of root  asked 2026-09-01  re-asked 2  blocker: ARCHITECTURE.md + README.md are
                       FRESHNESS_FILES; the A2 gate makes the edit require a genuine end-to-end
                       re-read. Owner: batch-F L5 / [#621]                    -> blocker named
logs thinning          asked 2026-09-01  re-asked 1  blocker: three flat globbers must resolve
                       bucketed paths BEFORE the exemption retires. Owner: batch-F L3 / [#626]
config/ fate           asked 2026-09-01  re-asked 1  blocker: ROOT-R1 unlanded             
dashboard home         asked 2026-09-01  re-asked 1  blocker: docs/ placement is batch G     
```

**Two of these seeds are already RED-adjacent and that is the point of writing them down.** The
de-bless was asked **three times** before a visible change existed; under this mechanism it would
have rendered RED after the second, in the bundle, where the operator would have seen it without
having to ask a third time.

## Status

DRAFT — filed 2026-09-01 from operator direction, under the reconcile-before-birth rule. **Its
carrier row is deliberately unborn**, on the precedent intake #62 states in its own Status section
and #40 before it: the path from a CANDIDATE runs through intake and ratification (ADR-98,
ADR-111), and question 1 is a ruling the operator owns. **Seeds batch G.** Awaiting the operator's
ruling on question 1 and technical-architect triage on 2–5.

---

## AMENDMENT — 2026-09-01: THE DASHBOARD HOME IS RULED — `docs/dashboard/`, and the build order is fixed by evidence

> **Source:** operator ruling, stated 2026-09-01, under the same *reconcile-before-birth* rule that
> filed this intake. **Appended, not edited** — the body above stands as filed, including its open
> question 1, which this amendment ANSWERS rather than deletes. **No folder is created here and
> none is authorised**; the ruling names a home, and the admission of that home is still a gated
> act with a cost, stated in §3 below rather than assumed away.

### 1 · The ruling

**The dashboard is a PER-REPO ORGAN, universal by construction. Its home is `docs/dashboard/`.**

- **Root stays sacred.** The 2026-08-26 ADR-101 amendment — *"root is sacred, and the docs disease
  is cured by the consumer gate (`[#595]`), not by a sibling folder at the root"* — is **untouched
  and upheld**. A root `dashboard/` is **WITHDRAWN**, not merely deferred.
- **`ecosystem/dashboard` is WITHDRAWN too**, and for a different reason: it is **hub-only and
  therefore non-scalable**. `ecosystem/` is the hub's fleet-facts tree, keyed by consumer repo
  name; no carrier ships it and a consumer repo has none. A dashboard placed there could never be
  the per-repo organ the direction asks for — it would be an instrument the hub can open and no
  consumer can.
- **`docs/dashboard/` is the home** because it rides the tree a consumer already receives, so
  universality is a property of the placement rather than a promise about future work.
- **Data sources, per repo:** `logs/`, `tasks/`, the FPG graph, funnel state. **The HUB instance
  additionally renders fleet panels from `ecosystem/`** — the same renderer, one extra input that
  is present in exactly one repo. The fleet half is an *addition at the hub*, never a requirement
  on a consumer, which is what keeps the organ universal.
- **`ecosystem/trends.html` relocates to `docs/dashboard/`.** It stays **generated and regenerable
  by one command**; VS Code discoverability comes from **a task, not from the path** — `.vscode/`
  is already an owner=hub carried surface, so the discoverability mechanism exists and needs no new
  convention.

### 2 · What the ruling CLOSES

**Open question 1 is ANSWERED, and the answer is the one the precedent predicted.** The question
asked whether a new folder may exist at the ROOT and whether this one clears the bar that revoked
`prompts/`. It does not, and the ruling does not ask it to: **the folder relocates into the genre
tree**, which is precisely the remedy the 2026-08-26 revocation itself applied when it moved the
`prompts/` convention to `docs/audits/<date>-technical-<batch>-launch-contracts/`. The ruling
therefore **follows** C2's standing precedent rather than overriding it, and the conflict intake
#38's amendment named as *"left open ON PURPOSE"* is discharged without a contradiction being
created. **Acceptance criterion 1's blocking clause is satisfied**: the ruling exists, so VIEW-layer
work is no longer barred by it — though see §5, which bars it again for a different and better
reason.

**Open question 2 is answered in part, and the unanswered half is now smaller.** The question was
what a root `dashboard/` buys given that `fleet_parity.py::_eval_sweep` sees TRACKED entries only.
Relocating to `docs/dashboard/` **dissolves the root-sanction half of it** — there is no
`root-dashboard` parity row to be empty, because there is no root entry. What **survives** is the
zone-class question, unchanged and still the technical architect's: `ecosystem/trends.html` is
gitignored (`.gitignore`, the `ecosystem/trends.html` entry and the reasoning block above it) and
`ecosystem/conformance.html` is committed, so the two artifacts this folder gathers are still in
**different zone classes**, and the ruling does not say which one `docs/dashboard/` takes. The
direction's own words — *"generated, regenerable by one command"* — read toward **ignored**, which
would make the folder's contents invisible to any git-derived view; the deploy-as-an-organ clause
reads toward **tracked**. **Both cannot hold, the ruling must hold for both artifacts, and it is
recorded here as still open rather than inferred from the phrasing.**

### 3 · What the ruling COSTS — measured, not assumed

The relocation is **cheaper than a root admission, and it is not free.** Three costs, each with the
surface that carries it:

1. **A Tier-2 genre admission is still owed.** `validate_hermetization.py`'s `SANCTIONED_GENRES`
   is a closed set and **`dashboard` is not a member**; Rule A refuses an added path under an
   unsanctioned `docs/<genre>/` with *"unsanctioned new docs genre folder"*. So `docs/dashboard/`
   needs an **ADR-101 amendment** exactly as a root folder would — what changes is the **tier**:
   a Tier-2 genre admission against a closed genre set, not a Tier-1 contraction-precedent fight.
   This amendment does **not** draft that ADR amendment, and the folder must not be created before
   it.
2. **The carrier premise is PARTLY FALSE and is corrected here rather than repeated.** The ruling
   says the dashboard *"deploys with the `docs/{intake,handoffs,decisions,audits,archive}` tree at
   instantiation"*. **That tree is not a carried payload.** The docs carrier's `doc_paths` in the
   live manifest declares exactly three pairs — `docs/intake/README.md`,
   `templates/intake-template.md` and the plugin `INSTALL.md` at the consumer root; the remaining
   genre directories are **consumer-created, not shipped**. What IS true, and is the useful half,
   is that **`deploy/carrier_docs.py` is fully manifest-driven** — its own module docstring:
   *"Unlike every other carrier this one is fully manifest-driven: it hardcodes no payload …
   shipping one more hub doc to consumers is a manifest edit, not a code change."* So the vector
   exists and is cheap; the "rides the existing tree" phrasing overstates what the tree does today.
3. **What deploys is the GENERATOR and the DOCTRINE, never the rendered page.** The same manifest
   block already records the constraint, for `README.md`: the carrier ships **verbatim,
   hash-guarded replicas**, which is correct for methodology-generic content and **wrong for
   repo-specific content** — declaring such a pair *"is not a migration, it is a mis-carry"*. A
   rendered dashboard is repo-specific output by construction; hash-guarding it would fail on every
   consumer at every regeneration. **The organ that deploys is layers 1–2 (`scripts/` + the event
   contract); layer 4's artifact is produced locally in each repo.** This is a sharpening of the
   direction's *"deploys as an organ"* clause, not a contradiction of it — and it is what makes the
   clause implementable at all.

### 4 · What this supersedes in the body above

- **Functional requirements, the four-layer statement:** VIEW's home reads `dashboard/`. It is now
  **`docs/dashboard/`**. MECHANISM `scripts/` · DOCTRINE `protocols/` · TRACE `logs/` · VIEW
  **`docs/dashboard/`**.
- **Non-goals, first bullet:** *"`dashboard/` is a request recorded on intake #38"* — the request
  is **resolved** (refused at root, relocated), and intake #38 carries the resolution as its own
  amendment of the same date. The bullet's operative clause is unchanged and still binds: **no
  folder is created before ADR-101 admits it.**
- **Impact sketch, Physical:** *"one new root directory if and only if ADR-101 admits it"* → **one
  new `docs/<genre>/` directory if and only if ADR-101 admits it.**
- **Open question 1** — answered, §2. **Open question 2** — half answered, half still open, §2.
  Questions **3, 4 and 5 are untouched and remain open**; in particular question 5(b), the
  gitignored-store reversal, is the same fork as question 2's surviving half and should be ruled
  with it.

### 5 · The build order, recorded by evidence: TRACE first, VIEW second

The body's *"the VIEW layer already names the TRACE layer that does not exist"* section established
the ordering from an artifact rather than from preference. The ruling **adopts it as the build
order**, and it is stated here as a sequence a lane can be dispatched against:

1. **TRACE first**, and specifically the two OPEN rows of the live telemetry arc — **`[#575]`**
   (store performance; silent drops under concurrent writers) and **`[#576]`** (the read path).
   `[#529]` and `[#565]` are already CLOSED. Nothing on the VIEW layer proceeds ahead of these two,
   because a panel built over a store that drops rows silently is worse than an absence: it renders.
2. **The acceptance test is the three ABSENT panels, and it is mechanical.** `commit-gate ms`,
   `suite wall-time` and `per-model quality` flip from **ABSENT to a rendered series**, with
   **nothing else on the page changing** and **no hand-entered value anywhere in the input path**.
   Pass/fail is a diff of the page plus a read of the input table; it is not a judgment call. This
   restates the body's acceptance criterion 6 as the *gate on step 1*, which is its operative use.
3. **VIEW expansion after** — new panels, the relocation of `trends.html`, the conformance
   migration of §6. Building panels before the stores exist adds absences, not answers.

**This ordering is now the binding half of criterion 1's replacement.** Criterion 1 barred VIEW work
pending a ruling on the root; the ruling has been made, and the bar is **re-established on the
evidence instead**: VIEW work waits on TRACE, not on an admission question.

### 6 · `conformance.html` — MIGRATE, and the migration is specified

The direction is **MIGRATE, not delete**, and this amendment fixes the three things the word
"migrate" left ambiguous:

- **The `.md` twin STAYS, and stays the data surface.** `ecosystem/conformance.md` is not part of
  the migration. It is the parseable, diffable, git-visible record; nothing about the VIEW layer
  replaces it, and a migration that took it out would trade a durable surface for a rendered one.
- **The `.html` RENDERER becomes a `docs/dashboard/` panel.** What moves is the rendering half of
  `scripts/gen_dashboard.py` — the artifact the operator opens — not the generator's data path.
  Its **one honest question** becomes a panel among the others, which is the whole point of a
  single VIEW: the operator opens one file, not two HTML siblings in a fleet-facts directory.
- **Consumers are re-pointed ONLY where they cite `.html`.** Enumerated, with the surface that
  carries each, so the migration is checkable rather than asserted — and the count is deliberately
  not restated as a number, per the standing rule that a count typed into a doc is stale at the
  next commit:
  - `scripts/generated_artifact_freshness.py` — the `conformance-dashboard` entry, whose `outputs`
    tuple names **both** files. **Only the HTML leg moves**; the `.md` leg is unchanged. A
    fire-test proving the tuple REDs on a stale new target is criterion 4's, and stands.
  - `scripts/gen_dashboard.py` — the `HTML_RELPATH` constant, and the module docstring that
    records the 2026-08-19 operator addendum admitting the HTML sibling.
  - `tests/test_generated_artifact_freshness.py` and `tests/test_gen_dashboard.py` — each pins the
    tuple or the `--commit-path` string literally, so each is a re-point rather than a rewrite.
  - `ARCHITECTURE.md` — the operator-addendum sentence naming the HTML sibling and its generator.
  - The two artifacts' **own commit-path prose**, in `ecosystem/conformance.md` and the rendered
    `ecosystem/conformance.html`, which name the pathspec pair verbatim.
  - Intake **#42**'s scenario, whose amendment of this date names `docs/dashboard/` as the
    destination.

  **This is the "four+ consumers" the direction names, and the enumeration is why the count is
  understated there**: it is at minimum six live surfaces plus two self-describing artifacts, and
  intake #42's amendment already recorded the direction's figure as UNDERSTATED before this ruling
  landed.

### 7 · Status: DRAFT → READY

**`status:` moves to READY** — *operator-approved, waiting on its consumer* — on the ruled enum
(intake README §5). The transition is warranted because **the one blocking question was the
operator's and it has now been ruled**: question 1 gated every other clause, and §2 answers it.

Two consequences, stated so neither is inferred:

- **READY is not ACCEPTED, and this file still binds nothing.** The blockquote at the head of this
  intake stands **verbatim and remains true**: nothing below it is doctrine until the intake is
  ratified, and the repo wins on any conflict. **Ratification is the operator's act**, and this
  amendment does not perform it.
- **Only the status TOKEN was edited in place** — the frontmatter `status:` key's value and the
  same token in the header comment, which is a second copy of the same machine fact and would
  otherwise drift. That is the ADR-94 class of edit (status is metadata, not decision content); no
  frontmatter KEY was added, removed or renamed, and no decision content above was altered.

### What this amendment does NOT do

- **No folder is created.** `docs/dashboard/` does not exist after this commit, and creating it
  before ADR-101 admits the genre is exactly what Rule A exists to block.
- **No ADR-101 amendment is drafted**, and `SANCTIONED_GENRES` is untouched.
- **No row is born**, on this intake's own reconcile-before-birth precedent.
- **No code, no test, no manifest edit.** The carrier finding of §3.2 is a **correction to the
  record**, not a declaration; the live deploy manifest is unchanged.
- **No ratification.** READY is a waiting state, and §7 says whose act ends the wait.
- **No answer** to open questions 3, 4 or 5, or to the surviving half of 2. Four questions remain
  the architect's and the operator's, and they are named rather than quietly closed.
