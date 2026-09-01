---
intake-id: 66
status: DRAFT
origin: operator direction, stated 2026-09-01 under the binding rule "reconcile-before-birth — amend #62/#617/HY-2/HY-4/A2 where they carry it, birth only the gap"; filed after a reconcile pass that moved five of the seven legs onto existing carriers
consumed-by:
---

# The OBSERVABLE HARNESS — four layers, one home each, and the layer that has no home at all

<!-- class: tech (structural/ownership question) · status: DRAFT — NOT ratified; DRAFT BINDS
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

## Status

DRAFT — filed 2026-09-01 from operator direction, under the reconcile-before-birth rule. **Its
carrier row is deliberately unborn**, on the precedent intake #62 states in its own Status section
and #40 before it: the path from a CANDIDATE runs through intake and ratification (ADR-98,
ADR-111), and question 1 is a ruling the operator owns. **Seeds batch G.** Awaiting the operator's
ruling on question 1 and technical-architect triage on 2–5.
