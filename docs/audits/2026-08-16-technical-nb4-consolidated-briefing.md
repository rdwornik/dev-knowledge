---
title: "NB4 consolidated briefing — six night-batch-4 lanes aggregated into one morning artifact (DRAFT)"
date: 2026-08-16
class: technical
status: DRAFT
---

# NB4 consolidated briefing — the six night-batch-4 lanes, aggregated

> **DRAFT · BINDS NOTHING · AGGREGATE-NEVER-ADJUDICATE.**
> This file rules nothing, closes nothing, births nothing, re-scopes nothing and lands nothing on
> `main`. It carries no verdict of its own. Where a recommendation appears it is **the source lane's
> recommendation, attributed** — relaying a proposal is aggregation; forming one would be
> adjudication, and this artifact does not have that authority.
> **No branch was deleted and nothing was merged.** Landing happens on the primary machine after
> batch 6 closes.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** `nb4-consolidated-briefing`
- **Lane:** `dk · nb4-CONS · cloud-consolidation`, read-only against `origin`. **Branch
  `claude/nb4-consolidated-ychsah`** — the brief names `claude/nb4-consolidated`; the session was
  provisioned with the suffixed form and that is the branch this file lands on. Both are the
  sanctioned `claude/<slug>` machine-produced lane shape (CLAUDE.md §4). Recorded rather than
  silently reconciled — the fourth consecutive lane to record this (X7).
- **Base of record:** the six lanes were each cut from **`d137cc6a`**. **`origin/main` is now
  `43cd1ce`** — it moved *after* every lane cut its base (X8, and it invalidates a number in all six).
- **Sources:** six branch reports, read in full via `git show`. Nothing is summarized from a summary.

## Evidence grades, defined before use

| grade | meaning |
|---|---|
| **VERIFIED** | re-derived live this session against the tree, git, or an executed module — not taken from the source lane's word |
| **PROPOSED** | a source lane's proposal or recommendation, adopted by nothing and gating nothing. The label is about *status*, not quality |
| **UNVERIFIABLE** | rests on a source this session cannot reach — an off-repo pack, a blocked egress host, a working tree on another machine, or another container's state |

Every claim below carries a source tag `[NB4-A]`…`[NB4-F]` and a locator. Locators of the form
`A:127` mean *line 127 of that lane's report as committed*; repo locators are given as
`path:line`. Where this session re-derived a lane's claim, the row says **VERIFIED (live)** and
names the command or module.

---

## §0 · State and contradictions

### 0.1 · State in three lines

```
Six lanes ran read-only from ONE base (d137cc6a), landed six DRAFT reports on six branches,
and between them closed 0 rows, birthed 0 rows, changed 0 gates and wrote 6 tracked files.

main has since moved to 43cd1ce -- ruling D-1v2: [#533] born, batch-6 roster 12 -> 11,
lanes l and y deferred to batch 7 -- AFTER every lane cut its base. All six are stale on it.

The architect's queue is 6 items. TWO of them are time-critical because they land INSIDE
batch 6, which is mid-flight: [#417] vs lane f, and the Form-E predicate vs lane a.
```

### 0.2 · The six lanes, and what each is for

| tag | lane | branch | report | verdict line |
|---|---|---|---|---|
| **NB4-A** | llm-acceptance | `claude/nb4-llm-acceptance-benchmark-pnoo2q` | 545 ln, technical | `Tally: 2/3/3/2` |
| **NB4-B** | telemetry-read | `claude/nb4-telemetry-read-path-ivoka2` | 626 ln, technical | *(none — see X13)* |
| **NB4-C** | playbook-gap | `claude/nb4-playbook-gap-coverage-1ktsuc` | 1026 ln, verification | `covered 1 / partial 6 / absent 6` |
| **NB4-D** | equilibrium | `claude/nb4-equilibrium-audit-el1o0w` | 562 ln, verification | `JUDGMENT 13 · MECHANIZABLE 13 · BYPASSED 2` |
| **NB4-E** | closing-campaign | `claude/nb4-closing-campaign-prep-gb68l0` | 709 ln, census | `NOW-CLOSABLE 2 / AFTER-WAVE 0 / campaign batches 6` |
| **NB4-F** | fleet-parity | `claude/adr-104-fleet-parity-audit-f1lr7a` | 282 ln, technical | `in-parity 2/8 · seeding-ready 0/8` |

**3,750 report lines total.** Full provenance — SHAs, timestamps, per-lane honest limits — in §3.

### 0.3 · Contradiction ledger

Fourteen entries. A contradiction is entered as its own row and **is not resolved here**: N
independent lanes disagreeing is the fan-out's product, and a briefing that silently picks a winner
has consumed the evidence and reports a consensus no lane held.

---

**X1 — THE CONTAINER IS REPAIRABLE, OR IT IS NOT. [NB4-D] and [NB4-E] ran the same test and
reached opposite operational conclusions — and this session is a third data point that reconciles
them.** *Severity: the highest-value disagreement in the set.*

- **[NB4-D]** `D:523-558` (AMENDMENT 2) ran `uv self update 0.11.19` live → `error: The version
  0.11.19 was not found for the app uv in workspace uv`, and concluded: *"no invocation of
  `uv self update` will ever succeed on this image"*. It then **declined** to install by another
  route (`D:552-558`), leaving `audit.py health` and the pre-commit stack un-runnable and the full
  gate stack *"owed at integration on the operator's clone"* (`D:477-479`).
- **[NB4-E]** `E:68-85` hit the same class and **repaired it durably**: it pointed the shadowing
  `/root/.local/bin/uv` at the pinned 0.11.19 binary (the shadowed 0.8.17 *moved aside, not
  deleted*), and records *"The full gate stack then ran green on this report's commit with no
  `--no-verify` and no `SKIP=`."* It agrees `uv self update 0.11.19` does not work — *"the error
  message's own suggested remedy is a dead end in this container"* (`E:76-78`).
- **THIS SESSION, VERIFIED (live):** `which -a uv` → `/root/.local/bin/uv`; `uv --version` →
  **`uv 0.8.17`**. The broken state D described reproduces here exactly; E's repair is **absent**.

**Reconciliation, stated as fact rather than verdict:** the two lanes are not in factual conflict —
they are in conflict about *scope of remedy*. E demonstrated a working repair; D inferred from one
failed update path that none existed. But **E's repair is per-container and does not survive**:
this session got a fresh container and got 0.8.17 back. So D's *"un-runnable here"* is true of any
container that has not had E's manual repair applied, and E's *"gate stack ran green"* is true of
one that has.

**What that jointly implies, and no single lane states it:** the repair exists, is cheap, and is
performed by no organ — which is precisely `[#453]`'s own Done-when (*"a session preflight performs
the unshallow and asserts the `uv` pin"*). The route that preflight should take is **E's
un-shadow**, not `uv self update`, which both lanes independently measured as a dead end.

---

**X2 — `audit-health` fails in a fresh clone: container artifact, or structural defect?**

- **[NB4-C]** `C:1009-1022` reads all four `[!!]` markers as **shallow-clone artifacts**, a
  *"4-for-4 reproduction of the night-3 finding"*, attributing `repos registered (none)` to
  *"no sibling repos on this disk"*. Concludes *"None is a regression and none is this lane's."*
- **[NB4-E]** `E:60-66` (trap 4) reads the same marker as **structural**: `audit.py health`'s
  preflight asserts *">=1 repo registered"*, registration lives in `ecosystem/<name>/state.yaml`,
  and that path is **gitignored** (`.gitignore:69`). So `discover_repos()` returns `[]` in *any*
  fresh clone and the `audit-health` **pre-commit gate cannot pass — for any commit, by any seat,
  in any container.** E **verified this on a pristine HEAD tree with zero changes staged**.

**Not a factual conflict; a conflict of generality, and the generality is the finding.** C's
reading makes it a property of cloud containers. E's makes it a property of the gate, and E's is
the falsifiable one — it was tested against a clean tree, which removes the shallow-clone
confound. Under E's reading the hub's own commit gate is unarmable from a fresh clone and no row
owns that. E repaired it locally through `audit.save_state` (`E:80-85`) and **filed rather than
reopened** `[#453]`.

---

**X3 — `[#453]` is enumerated two different ways, and the two enumerations imply different
contracts.**

- **[NB4-D]** `D:492-501` reads the row as **three** gaps, reports 2 REPRODUCED / 1 UNTESTED, and
  calls this *"witnessed a third time"*.
- **[NB4-E]** `E:52-58` enumerates **four** traps in one session and states that `[#453]`'s
  Done-when covers traps 1 and 3 *"but **not** traps 2 and 4"* (`E:88-90`) — stale local `main`,
  and the audit-health preflight of X2.

**Consequence:** a preflight built from D's reading ships covering two gaps; from E's, four. E's is
a strict superset and the safer contract. Both lanes explicitly declined to reopen, re-scope or
amend the row (`D:507-510`, `E:88-90`) — the disagreement is in what a future implementer inherits.
The two also number the instances differently, and this session is a further reproduction of gap
(2) (X1), so **the count is unsettled and is left so.**

---

**X4 — `[#417]` is closable and is simultaneously being converted by a live lane. TIME-CRITICAL.**

**[NB4-E]** `E:229-266`. `[#417]`'s Done-when is **met on `main` @ `d137cc6a`**, with cited
evidence in both directions (`scripts/session_end_backpressure.py:402/412/418`;
`tests/test_session_end_backpressure.py:758-807`), landed `4bef950`. And:

> **COLLISION, FLAGGED LOUDLY: `[#417]` is dispatched RIGHT NOW as batch-6 lane `f`'s conversion
> target.** Lane f (`worktree-lane-f-130-conversions`, rows `#130 #274 #350 #417`) is converting a
> clause that is already discharged.

E adds the reason the census missed it — a **locator-rot** finding: the row's own `refs` pin cited
`session_end_backpressure.py:340-349`, which *"is now `check_backlog_marker`, a different function
entirely"*, and the stale pin propagated into a downstream verdict for the **third recorded time**
(`E:251-258`). **VERIFIED (live):** lane `f` survives ruling D-1v2 — the amended roster of 11 is
`a b c d e f g h i x m`. No other lane touches `[#417]`.

---

**X5 — the Form-E conversion predicate would ship three spuriously-closable rows. TIME-CRITICAL.**

**[NB4-E]** `E:330-348`. The wave-2 drafted predicate is *"a `###` section in
`protocols/STANDING_RULINGS.md` whose body contains the literal `[#NNN]`"*. Measured against the
live register, `[#409] [#410] [#411]` appear inside `### L-8` and `### M-7`, and `[#502]` inside
`### H4` — but those mentions are **fold-set and removal-sheet rulings that say the opposite**:
*"L-8 rules the trio stays distinct; it does not rule the night batches out."*

> Under the drafted predicate the escape branch reads as **already satisfied for #409/#410/#411**,
> which would make three rows spuriously closable the moment lane `a` converts them, on a ruling
> that says the opposite.

E's proposed repair (`E:344-348`, PROPOSED): require the section to be *about* the row — a `###`
heading naming the id, or a body line `[#NNN]` **followed by a disposition token** — not a bare
literal anywhere in a section body. E calls it *"a conversion-instrument defect, not a row defect,
and it is cheapest to fix in the contract rather than after 29 clauses ship."* Lane `a`
(`worktree-lane-a-409-conversions`) is on the amended roster. **These same three rows are also
inside the 25 NEEDS-RULING set (X6), so two campaign levers claim them.**

---

**X6 — four NEEDS-RULING rows are inside batch 6's conversion set.**
**[NB4-E]** `E:386-390`: `#409 #410 #411` (lane `a`) and `#491` (lane `g`) are among the 25 rows
*"no executor may lawfully start"*. E states this is legitimate — *"a conversion is not a build"* —
but *"the ruling batch and the conversion batch **must not both claim those four**, and the Form-E
predicate defect lands on exactly three of them."* Compounds X5.

---

**X7 — brief-vs-tree branch naming diverged for the fourth consecutive lane, and once beyond the
`nb4-` prefix entirely.**
`[NB4-C]` `C:13-17`, `[NB4-D]` `D:4-6` and `[NB4-F]` (implicitly, by branch) each recorded that the
operator brief named an unsuffixed branch and the harness provisioned a suffixed one. **VERIFIED
(live):** the consolidation brief calls all six *"claude/nb4-\* branches"*, but **NB4-F's branch is
`claude/adr-104-fleet-parity-audit-f1lr7a`** — not `nb4-`-prefixed at all; only five of six are.
This session's own branch is `claude/nb4-consolidated-ychsah`, not the brief's
`claude/nb4-consolidated`. **No grammar violation** — all are the sanctioned `claude/<slug>` shape
(CLAUDE.md §4), which is exempt from the `worktree-lane-…` lane grammar. Recorded, not reconciled.

---

**X8 — every report says batch 6 is width 12. It is 11. VERIFIED (live).**
`[NB4-A]` `A:10-11`, `[NB4-C]` `C:19`, `[NB4-D]` `D:134` (12 phase-2 contracts), `[NB4-E]` `E:286`,
and `[NB4-B]`'s D2 mock header literally renders `BATCH 6 (width 12, one wave)` (`B:368`). Ruling
**D-1v2** at `3c07314` (merged `43cd1ce`, 2026-08-16 13:53–14:05 +0200) removed lanes `l` and `y`
on a measured OWNED-FILES collision — *"COLLISION l <-> y : scripts/audit.py , tests/test_audit.py"*
— birthed `[#533]`, and added lane `m`. Amended roster: `a b c d e f g h i x m`, merge order with
`m` last. **All six lanes cut their base before this existed; not one is wrong-at-authoring.**

Two second-order effects the reports could not know:
- **[NB4-D] §2 act C9** proposed the 12×12 collision matrix as MECHANIZABLE with *"no organ
  exists"* (`D:139`). It was run by hand at Position 0b and **found exactly one collision in 66
  pairs** — so D's proposal is now backed by a live instance of the class it predicted.
- **[NB4-E]**'s denominator moved: 196 live at `d137cc6a`, **197 at `43cd1ce`** (`[#533]` born).
  **VERIFIED (live):** `tasks/manifest.json` carries 197 nodes with a `task` key. This is E's own
  §1 rule demonstrating itself within one day — *"a closing-campaign report cites the live count
  measured at the commit it reports against, names that commit … never the census's 196"*.

---

**X9 — the ADR-101 audit-name gate has a hole, and this session reproduced it. VERIFIED (live).**
**[NB4-B]** `B:526-527` and `B:565-568`: Rule B grammar-checks `docs/audits/*.md` **only**, so
`docs/audits/*.html` (or `.csv`, `.svg`) *"is name-checked by nothing. That is a gate hole, not a
licence."* Re-derived here by executing the live module:

```
docs/audits/GARBAGE_Name.md      ->  Rule B VIOLATION   (UPPERCASE + underscore refused)
docs/audits/GARBAGE_Name.html    ->  no violation on any rule
docs/diagrams/organ-cost.html    ->  Rule A + Rule C violation
```

B's §4.3 recommendation (PROPOSED) deliberately declines to walk through the hole and proposes
`logs/<NAME>-DASHBOARD.html` instead, *"because the gate already admits it"* — no ADR-101 amendment
needed.

---

**X10 — the fleet's own template points every consumer at a home the hub's gate refuses.**
**[NB4-B]** `B:561-564`: `templates/ARCHITECTURE-template.md:103` tells every consumer repo that
diagrams *"live under `docs/diagrams/`"*; that path is refused by Rule A **and** Rule C and the
directory does not exist in the hub (reproduced above, X9). **Every consumer repo carries this
template.** Filed by B as a drive-by, in this lane's own words *"not re-discovered"*.

**Cross-lane gap this exposes:** `[NB4-F]` swept all 8 non-hub members against the parity surfaces
and has **no column for "a hub template names a refused home"** — so a fleet-wide divergence
sourced in the hub's own carrier is invisible to the parity instrument. Neither lane contradicts
the other; the finding falls between them.

---

**X11 — the strongest cross-lane agreement in the set: two lanes reached the same organ from
opposite directions.**
**[NB4-C]** row 2 (`C:144-180`) grades lane grammar PARTIAL and *"the most expensive row in the
matrix"* — three consecutive batches damaged — with `[#531]` as the **provisioning-side** gate.
**[NB4-D]** §2-BYPASS-1 (`D:166-179`) independently classifies the same class as
ALREADY-MECHANIZED-BUT-BYPASSED, and its M1 `--check` leg arms *the same regex* at the
**contract/manifest side**, explicitly *"complementing `[#531]`'s provisioning-side gate rather than
duplicating it. Two sides, one regex, one definition"* (`D:275-278`). Convergent, not redundant.
Both cite `validate_branch_naming.LANE_BRANCH_RE` as the single definition.

---

**X12 — `[#293]` / lane k: the withheld word and the reason it should stay withheld.**
**[NB4-D]** E2 (`D:160-161`) records the operator **withheld** lane k's word, *"so it is absent
from this roster rather than silently carried"*. **[NB4-F]** F1 (`F:169-201`) supplies the reason
independently and grades it **HIGH**: `[#293]`'s Done-when requires creating `docs/handoffs/` in
child repos — *"the exact directory a standing ruling forbids"*
(`docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md:25-28`, architect-ratified). So
the measured **0 of 8 seeded is conformance, not a gap**, and *"executing `[#293]` as written would
push all 8 members out of conformance in one move."* `[#303]` is open, already names the hazard,
and lists `#293` as its own kill-candidate. **VERIFIED (live):** `[#303]` is open on `main` and
`[#293]` carries the phase-1 R6 denominator ruling (8, not 6) and the `OPERATOR-GATED, not executed`
correction. Convergent; nothing contradicts.

---

**X13 — one report in six carries a severity tally, and the lane that carries it is the lane that
names the tally as standing law. VERIFIED (live).**
**[NB4-A]** `A:14-17` states the standing law it works under: *"artifact-or-RED with the severity
tally in the artifact body from day one"* (`BACKLOG.md:267` `[#492]`, the `[#480]` durability
property), and carries `Tally: 2/3/3/2`. Grepping all six reports for a `Tally:` header:

```
NB4-A   Tally: 2/3/3/2   <- present
NB4-B   none        NB4-D   none        NB4-E   none        NB4-F   none
NB4-C   the only hit is a QUOTATION inside its own row-11 analysis of the codex format,
        not the report's own tally
```

Not a defect claim against any lane — the standing law A cites is scoped to the codex review-lane
artifact grammar, not to night-batch reports. It is recorded because **[NB4-C] row 11 grades that
very grammar PARTIAL and measures the documented format failing the live parser on 2 of 4 legs**
(`C:408-419`), so the question of which artifacts owe a tally is live in the same batch.

---

**X14 — the `silent_rule_ratchet` headroom is 1, and eleven lanes are editing concurrently.**
**[NB4-C]** `C:916-931` measured live: 440 against a committed baseline of **441**, headroom **1**,
and all twelve of its draft acts are **+0 tokens** by construction. C's own limit 6 (`C:1006-1008`)
states the exposure: *"if another lane in batch 6 adds a normative token before this arc lands, the
arithmetic changes without any of these drafts changing."* **VERIFIED (live):**
`ecosystem/silent-rule-baseline.yaml` on `main` reads `baseline: 441`, `detector_id: silent-rule-v4`,
`measured_at: 2026-07-30`. The file's own header records that the number *may be lowered or held,
never raised* except by operator ruling.

### 0.4 · COLLISIONS — recorded here so they are not lost

```
C-1  [#417]  NOW-CLOSABLE (NB4-E)          vs  batch-6 lane f converting it       LIVE NOW
C-2  #409 #410 #411  Form-E predicate      vs  batch-6 lane a converting them     LIVE NOW
C-3  #409 #410 #411 #491  NEEDS-RULING     vs  batch-6 lanes a / g (conversion)   LIVE NOW
C-4  [#492] peg lifted by NB4-A evidence   vs  NB4-E's NEEDS-ACT dated 2026-08-17 TOMORROW
C-5  [#293] lane k                         vs  [#303]'s open hazard + the 2026-07-08 ruling
C-6  NB4-C's 12-act arc (+0 ratchet)       vs  ratchet headroom 1, 11 lanes live  LIVE NOW
C-7  [#529] legs 1/2 (NB4-B F1/F2)         vs  NB4-B D1 and D2 having no data source
C-8  [#530] merged, Done-when MET          vs  ruled OPEN (R2) on two P1 legs     settled
```

---

## §1 · The architect decision queue

Six items, plus a precondition block ordered ahead of them. **Ordering is
preconditions-first** — that is `[NB4-E]`'s own rule for its campaign (`E:479-484`) and the shape
`[NB4-C]`'s Act 10 draft describes (`C:777-779`); it is carried, not invented.

**No item below carries a verdict from this briefing.** Each states the evidence, the source
lane's own recommendation *attributed to it*, the options as that lane framed them, and what the
decision unblocks.

### D0 · PRECONDITIONS — two decisions that land inside a running batch

These are ordered first because batch 6 is mid-flight and both expire when a lane integrates.

| | item | evidence | source lane's own words | grade |
|---|---|---|---|---|
| **D0.1** | Does lane `f` convert `[#417]`, or is `[#417]` proposed closed instead? | `E:229-266`; Done-when met on `main`, evidence in both directions, landed `4bef950` | *"This needs the operator's word before lane f integrates, or a converted-and-immediately-closable row lands with a conversion that was never needed."* | **PROPOSED** (E proposes NOW-CLOSABLE; E explicitly does **not** close it) |
| **D0.2** | Is the Form-E predicate repaired before lane `a` integrates? | `E:330-348`; measured spurious satisfaction for `#409/#410/#411` (and `#415/#425/#502`) inside `### L-8`, `### M-7`, `### H4` | *"a conversion-instrument defect, not a row defect, and it is cheapest to fix in the contract rather than after 29 clauses ship"* | **PROPOSED** (repair drafted, not applied) |

Neither lane resolved these deliberately: *"a prep lane that resolved a live batch's scope would be
overturning a dispatch"* (`E:696-698`).

### D1 · The routing-table amendment — `[NB4-A]` §4

**Evidence.** `[NB4-A]` `A:420-435` establishes the blocking fact first: **the canonical routing
table is not in this repo and is not reachable from this container.** `protocols/PLAYBOOK.md:4502`
places it in `~/.claude/ROUTING.md` and records that `#158` Decision B *killed the resident copy* —
*"a cached table silently drifts from ROUTING.md"*. `~/.claude/ROUTING.md` does not exist in the
cloud runtime. So the lane could not draft a byte-accurate edit and says so.

**What is on the table.** One added row, **roles-not-vendors** (`A:442-446`), so admitting a lane
later is a *cell edit* rather than a schema change. The `Admitted lanes` cell lists **the incumbent
only** — *"A candidate's model id is written into that cell by the ADMIT verdict, never in
advance"* (`A:449-453`). The existing t-shirt pins (S=Haiku · M=Sonnet · L=Opus) are **untouched**;
A states they route *size* while the new row routes *role*, and *"conflating them would be the
drift the row is meant to prevent"*.

**The options, as A framed them.**
1. Apply in `~/.claude/ROUTING.md` — **an operator act, not a session act**: core-invariant #6,
   per-machine global infra, and `[#338]` leg (c) is already open on exactly this class for
   `codex-review.ps1` (`A:431-434`).
2. Apply in-repo at `ARCHITECTURE.md` Ch3 *"Model routing (t-shirt)"* — A names this **with its
   known cost**: it *"re-creates the resident copy #158 Decision B killed — so it is named as an
   option with its known cost, not recommended"* (`A:457-460`).

**Attached, and independently time-critical.** A's §0 headline: **`[#492]`'s peg is MET.** Grok 4.6
released **2026-08-12**; both legs the row's `EVIDENCE 2026-08-10` line names as missing (a model
card, an API id) now exist. **Honest limit stated by A before the claim is used** (`A:40-48`): the
first-party card and `docs.x.ai` are **EGRESS_BLOCKED** from the container, so this is corroborated
across secondary sources — *"one grade weaker than the browser verification the row itself used"*.
A's recommendation: run the 2026-08-17 re-check in a browser anyway, *"but it should be run
expecting to lift the peg"*. `[NB4-E]` independently classes `[#492]` NEEDS-ACT with the same date
(`E:357`). **This is C-4 and it falls due tomorrow.**

**Unblocks:** the `[#492]` acceptance run; A's §3 promotion gate (HARD REFUSE on any fabricated
locator; ADMIT-full vs ADMIT-shadow vs REFUSE); and the ADR-74 Footnote B **n=2** rule that a first
ADMIT is provisional (`A:404-408`).

**Grade: PROPOSED** (the amendment), **UNVERIFIABLE** (the Grok 4.6 release, from this container —
egress-blocked, secondary-sourced by A's own declaration).

### D2 · The first dashboard to build — `[NB4-B]` §5

**Evidence.** `[NB4-B]`'s single most important measurement (`B:30-37`): **`logs/TELEMETRY.db` has
never been written.** `[#529]` merged the emit library with **zero call sites**, so Stage 2 is
being designed against an empty database. Two further findings decide build order:

- **F1** (`B:73-80`) — **VERIFIED by B against the tree:** `ALL_CHECKS` has **43** members and a
  grep for `perf_counter|monotonic|time()|elapsed|_ms` across all of `scripts/audit.py` returns
  **zero hits**. So `duration_ms` is a real column with no producer. *"a wiring pass that emits
  `duration_ms=None` for 43 checks satisfies the leg and still leaves D1 empty."*
- **F2** (`B:82-99`) — lane telemetry resolves to `<worktree>/logs/TELEMETRY.db`, `.worktreeinclude`
  does not carry it, and CLAUDE.md §5 rule 9 teardown deletes it. *"today a batch lane would emit
  into a private database and then delete it."*
- **F3** (`B:101-107`) — `logs/TELEMETRY.db` is still absent from `.gitignore`, and WAL adds `-wal`
  / `-shm` sidecars, so **the read path can dirty the tree even though it writes no data**. Any
  ignore line must be `logs/TELEMETRY.db*`, not the bare name.

**B's recommendation, attributed** (`B:574-592`): stack = stdlib `sqlite3` views as the data layer
+ **hand-rolled self-contained HTML/SVG** as the surface, written to `logs/<NAME>-DASHBOARD.html`
and gitignored; `uvx datasette` retained as an ad-hoc explorer, never imported, never the
dashboard; **no charting library adopted in Stage 2**. Build **D3 first — the WARN-ledger
burn-down** — *"not because it is the most valuable — D1 is — but because it is the only one of the
three whose data exists today"*: **17 committed `docs/audits/*-ecosystem-audit.md` files** already
carry a parseable per-check verdict series.

**The cost axis B says nobody costed** (`B:254-278`): ADR-112 tier. Plotly/Altair import from
`scripts/` → **Tier L**, spending a gap-week evaluation slot *before a single pixel is drawn*.
Hand-rolled HTML + stdlib `sqlite3` is **not an adoption at all** — no tier, no slot, no ledger
line. B also surfaces rather than designs around the fact that the memo of record picked a
**fourth** option (`rich`+`plotext`) as primary, and that intake #9 (SEED, so *direction not
ratified*) postdates it (`B:233-252`).

**Where they live** (`B:461-555`, gate **executed** not asserted): `logs/*.html` is admissible
today — no amendment, no ruling. `docs/<anything>.html` at the `docs/` root is refused by Rule C.
`docs/diagrams/` is refused by Rule A and C (X10). `docs/audits/*.html` passes everything, which is
the hole at X9.

**Unblocks:** Stage 2, and two prerequisites B assigns to `[#529]` rather than to Stage 2 — leg 1
must say *time the checks*, not merely *wire the call sites*; and `default_db_path()` must resolve
via `git rev-parse --git-common-dir`, the pattern `scripts/fleet_analytics.py:1075` already carries.

**Grade: PROPOSED** (stack, pick, home). **VERIFIED (live)** for the gate-hole leg (X9).

### D3 · The PLAYBOOK amendment arc — `[NB4-C]` §3

**Evidence.** Tally **covered 1 / partial 6 / absent 6** across the 13 mechanism shapes the brief
enumerated. C's shape finding (`C:40-43`): *"Every ABSENT row is a mechanism born in the last EIGHT
DAYS and every PARTIAL row is an older section whose machine contract moved underneath it. The
PLAYBOOK is current on DOCTRINE and behind on the MACHINE the doctrine now runs on."*

**Two rows C says are actively costing work rather than being merely silent:**
- **Row 2, lane grammar** — three consecutive batches damaged: batch 4 dropped 2 lanes, batch 5
  forfeited the exemption on 2 of 7 and hand-anchored, batch 6 reached 12/12 *by running every name
  through the regex by hand*. `grep -n "worktree-lane-" protocols/PLAYBOOK.md` → **0 hits**: the
  grammar appears nowhere in the file.
- **Row 11, codex tally** — the documented format **fails the live parser on 2 of 4 legs**
  (`C:408-419`): `**HEAD:**` MISS, `**Tally:**` MISS. An artifact authored from the PLAYBOOK is
  *recognized and then discounted*, landing in the check's `untallied` list. Live evidence: the
  four Position-0 artifacts were *"authored against the parser regexes rather than against prose
  intent"* (`JOURNAL.md` 2026-08-16 (b)).

**The arc.** 12 acts · 3 chapters + one section (Ch8 ×7, Ch11 ×3, §5 ×1, Ch10 ×1) · **≈ +250 lines
on 4628 (~5%)** · **+0 ratchet tokens, measured** (X14). All twelve drafts are **paste-ready**, so
*"the architect's cost is a ruling rather than an authoring pass"*. **Independence:** each act
stands alone and any subset may be ruled — *the one ordering constraint* is that Act 8's organ-list
edit points at Acts 9 and 10, so dropping either leaves Act 8 dangling (`C:900-902`).

**Two acts C flags for the closest reading** because they **replace** existing text rather than
adding: **Act 2** (per-lane requirement 5) and **Act 11** (the §5 Format block + a `version: 1.0 →
1.1` bump, *"the one act with a reconciliation consequence"* — worth checking against
`_COUPLED_VERSION_SETS` before it lands).

**The bar is stated so it can be overturned** (`C:994-997`): under a *"does a section exist"* bar
the tally reads **covered 6 / partial 1 / absent 6** instead. Rows 1, 2, 6, 10 are bar-sensitive;
rows 3, 5, 9, 12, 13 read ABSENT under either bar.

**One limit C states about its own instrument** (`C:983-988`): **"board rules 1–8" could not be
enumerated** — no in-repo artifact carries a numbered set of eight; the set is off-repo. Row 10
verdicts the *in-repo board surface*, not rules 1–8 individually, and Act 6 drafts only the single
board rule C could locate a source for.

**Grade: PROPOSED** (all 12 acts). **VERIFIED (live)** for the ratchet baseline of 441 (X14).
**UNVERIFIABLE** for board rules 1–8 (off-repo pack).

### D4 · The top mechanization — `[NB4-D]` §4 M1

**Evidence.** 33 browser-seat acts classified: **JUDGMENT 13 · MECHANIZABLE 13 ·
ALREADY-MECHANIZED-BUT-BYPASSED 2** (+5 already-mechanized and used). D's arithmetic is stated to
be checkable: families A=4, B=12, C=8, D=5, E=4 → 33, every act in exactly one disjoint class
(`D:207-212`).

**The measured number that carries the case** (`D:216-224`) — the hardest figure in the set:

```
common-law block      17 lines / 2,014 bytes
identical in          7 of 7 phase-1 contracts   (md5 ab56434a232166ff692819f4be1ff89e)
boilerplate share     48.3%   (14,098 of 29,208 bytes)
per-contract judgment 9-11 lines out of 26-28
phase-2 exposure      the same block x 12 lanes = ~24 KB
```

**M1 — `scripts/gen_lane_contract.py`: assembly, not generation.** D grounds the design in the
rejection it has to survive: **ADR-62 alternative 2** rejected *"fully automated mechanical
generation … as aspirational"*, and D concludes *"Nothing below proposes a template engine, and
nothing below generates judgment content"* — the surviving shape is **assembly with hand-authored
FILL-IN regions**, the model `scripts/gen_handoff.py` already ships and ADR-82 ratified.
Library-first with **no new dependency**: stdlib + `yaml.safe_load` (register **N-2**) +
`markdown_it` (**N-1**), both already adopted with recorded rulings.

**Why D ranks it first — the `--check` leg subsumes both BYPASS findings** (`D:270-280`): as a
pre-commit hook on an added `*-lane-contract.md` it regen-and-diffs the common-law block (the exact
shape of the four existing `*-freshness` gates), runs `validate_branch_naming.LANE_BRANCH_RE` at the
contract side (arming §2-BYPASS-1, complementing `[#531]` — X11), and runs `preflight_contract.py`
over the contract's locator claims (arming §2-BYPASS-2) *"with no change to `preflight_contract`
itself and no new authority"*.

**§2-BYPASS-2 is the load-bearing measurement:** `/preflight` *"was run against zero of this
window's 19 contracts"* (`D:181-193`) — and D then **ran it on its own report and it earned its
keep on the first pass** (`D:455-466`): 2 of 7 locator claims flagged, one a **real defect** fixed
before commit (a bare `ADR-56-…:85` with no `docs/decisions/` path), one a **tool false positive
left standing and reported** (an md5 digest extracted as a `sha` claim). D declined to widen the
extractor: *"widening a live extractor from an audit is exactly the out-of-scope edit this repo
files rather than sweeps in."*

**Tier L bars, stated per mechanization.** M1: ADOPT if an emitted contract is byte-equal to a
hand-authored one on its judgment regions **and** `--check` catches a seeded off-grammar name and a
seeded dead locator (RED-first). REJECT if the FILL-IN regions start absorbing derived content —
*"that is the ADR-62 failure recurring, and it is the one thing to watch."* M2
(`check_rulings_register.py`) and M3 (`pending_words.py`) each carry their own bar; D ranks M3 third
**on merit and says so**. Three candidates were **evaluated and deliberately not ranked** — merge-queue
ordering (*"genuinely borderline"*), the 12×12 matrix (*"deliberately sequenced behind M1"* — and see
X8, where it has now fired once), and the process-lane cap (*"too small to rank alone"*).

**Grade: PROPOSED** (M1/M2/M3). **VERIFIED by D against the tree** for the md5/byte/line
measurements; D's own limit 4 states *"every payoff figure for M2 and M3 is an argument"*.

### D5 · Closing-campaign readiness — `[NB4-E]` §4

**Evidence, and it reframes the campaign.** `[NB4-E]` measured 19 days of first-parent history
(`E:160-185`): **closed 52 (2.74/day) · born 72 (3.79/day) · NET +20.**

> **The finding this campaign has to be built around: the set is growing, not shrinking.** … The
> closure rate is real and healthy … and it is **out-run by the birth rate**.

**The arithmetic against the finish line** (`E:432-445`): §B clause 3 is *"open backlog < 100"*;
196 → <100 requires **net −97**; L-3's window is 6 windows → **−16.2 net per window**; the best
window ever observed is **−8**. E's conclusion: *"closure alone cannot reach the number, and the
binding constraint is the birth rate, not the closure rate. **A closing campaign that does not
carry a birth budget is not a closing campaign.**"*

**Readiness classes** (`E:212-220`): NOW-CLOSABLE **2** · CLOSABLE-AFTER-WAVE-2 **0** · NEEDS-ACT
**4** · NEEDS-RULING **25** · LIVE **165**. E's reading: *"Two closable rows out of 196 is not a
failure to look — it is what an aggressively-groomed set looks like two days after its dead cohort
was drained."*

**The most load-bearing finding** (`E:284-328`): **wave 2 buys verdictability, not closure.** All 29
dispatched wave-2 rows were tested against their own drafted clauses and **not one reads MET** —
Form E: a genuine ruling section exists for **zero of 12**; Form R: **zero of 6** carry a routine
block. *"A campaign plan that budgets net closure against wave 2 will miss by 29."*

**The throughput lever is not width** (`E:415-419`): `audit-py` holds **42 of 165** LIVE rows and
admits **one lane per batch** — 11–21 batches to drain that group alone. **This is the same
constraint ruling D-1v2 hit from the other side** (X8): the `l ↔ y` collision was two checks inside
`scripts/audit.py`, and `[#533]` decomposes the monolith. **E's structural finding and the batch-6
amendment are the same finding, reached independently.**

**The plan** — C1 ruling batch (25 rows, quarter-day, *"the only act in the whole campaign that
moves 25 rows"*) · C2 ratification+re-peg · C3/C4 audit-py drains · C5 stranded sweep · C6 M-class ·
C7 measure. **E states its own shortfall plainly** (`E:532-537`): *"Cumulative expected net at the
optimistic end of every range: −29. Against a required −97. **Stated plainly rather than smoothed:
this plan does not reach under 100 in windows 3–8.**"* What it does reach: 25 rows released, the
birth rate capped for the first time, and **two-plus windows of net-closure data — which is exactly
the evidence L-3 names as the precondition for re-scoping the number.**

**The ratio instrument** (`E:570-681`): `[#277]`'s STRONG:WEAK measured live — **3 STRONG / 145
WEAK / 0 valid**, against the row's own 2026-07-07 baseline of 49 proposals / 0 valid. *"the ratio
has got WORSE by 3x, not better."* All 3 STRONG adjudicated INVALID, each a distinct detector defect
class. Plus two structural defects in `[#277]`'s **own finish line**: the 30-day run its Done-when
names *"has no supported invocation"*, and leg (a) *"would pass vacuously"*. Both filed as evidence,
**neither row reopened** — and `[#277]` is dispatched right now as lane `i`, which E names as the
correct place for them to land.

**E opened nothing, re-scoped nothing, closed nothing** (`E:685-705`), and states this is **window 1**
of the two-or-more L-3 requires.

**Grade: PROPOSED** (the plan, the two NOW-CLOSABLE rows, the four re-pegs). **VERIFIED (live)** for
the denominator moving 196 → 197 at `43cd1ce` (X8).

### D6 · The k / fleet findings — `[NB4-F]`

**The limit that bounds every number, stated by F before any of them** (`F:31-42`): this is a
**remote-HEAD view, not the hub checker's view**. `ecosystem/registry.md` addresses members by local
Windows path and `scripts/fleet_parity.py` reads working trees **by design (AC-7)**. *"this report
cannot reproduce `fleet_parity.py`'s verdict and does not claim to."* F confirmed the limit with the
hub's own machinery rather than asserting it — `audit.py health` reported both consumers
`unavailable: … is not a git repo`, so **`fleet_parity` walked 0 of 9 in that container**.

**Reachability, measured not inferred** (`F:67-88`): **3 of 8 observable, 5 not.** F is careful that
*"'Not reachable' … does not prove the repo does not exist"* — `life-architect`'s registry row
records a confirmed private origin — so the honest reading is *"local-first fleet, partial
publication, not missing repos."*

**Three findings.**
- **F1 (HIGH)** — `[#293]`'s Done-when requires the directory a standing ruling forbids. See X12.
  F's proposal (`F:199-201`): *"`[#303]` is the prerequisite, not a sibling — lane k should be gated
  behind it, or `[#293]`'s Done-when re-scoped to `docs/intake`-only per the ruling's instruction."*
  **Seeding-ready 0 of 8 on two independent grounds, either alone sufficient**: 5 have no reachable
  remote; all 8 are blocked on content.
- **F2 (MEDIUM-HIGH)** — `corp-sca-time-automation` carries live methodology surfaces (floor
  byte-exact, sidecar, `check_floor_hash.py`, an active `floor-hash-verify` hook, `.claude/rules/`)
  that **no contract describes and no checker walks**: role `pre-deploy` → not walked;
  `deployed-versions.yaml` null on all three fields; **no `.methodology.yaml` at all**, so *"there is
  no file in which a divergence could be declared."* Last methodology touch **2026-06-08, 69 days**.
  *"It happens to be current today; that is luck, not a gate."*
- **F3 (MEDIUM)** — manifest **v1.4.0 has no release tag**, and the manifest states its own
  constraint: the tool's preflight requires the tag before `--execute`. So *"the hub's newest declared
  corpus is unreleasable"*, and `ai-council` is simultaneously **fully current** (against tags) and
  **one minor behind** (against manifests) depending on which surface you read. **Nothing checks
  manifest↔tag agreement.**

**Two structural readings** (`F:107-123`): the parity checker walks **at most 3 of 9** declared
members — *"every 'fleet parity' verdict is a statement about the hub and two consumers"* — and the
declared-absence `reason:` machinery *"makes the 6 skips honest, which is exactly why this is a scope
statement and not a defect."* And **where parity is measurable it is good**: all three observable
repos carry the floor byte-identical to the hub source hash.

Two secondary items with **dates that have arrived or are about to**: `ai-council`'s
`dep-pytest-xdist` declaration carries `review_date: 2026-08-16` — **expires today**; both consumers'
`.vscode` declarations carry `review_date: 2026-08-26` — **10 days out**.

**Grade: PROPOSED** (F1's routing, F2, F3). **VERIFIED (live)** that `[#303]` is open and `[#293]`
carries the R6 denominator ruling. **UNVERIFIABLE** for the 5 unreachable members — F states it:
*"5 of 8 rows are unmeasured, not measured-and-clean."*

---

## §2 · Proposed next-window arc map

Four arcs. **Proposed, not scheduled** — the ordering below is derived from the source lanes' own
stated preconditions and is offered for the architect to rule on.

### A1 · The closing campaign — `[NB4-E]`'s C1–C7

Carried as E specified it (`E:475-527`), with the two corrections this session's re-measurement
forces:

```
C1  RULING BATCH          window 3   25 NEEDS-RULING rows, one seat, ~quarter-day
                                     PREREQUISITE: the Form-E predicate repair (D0.2) lands FIRST
C2  RATIFY + RE-PEG       window 3   #417 #506 close; #102 #181 #325 #492 re-peg      (rides C1)
C3  AUDIT-PY DRAIN I      window 4   width 8-10, S-class only, birth cap 2
C4  AUDIT-PY DRAIN II     window 5   + the 24 wave-2 rows batch 6 makes verdictable
C5  STRANDED + DEFERRED   window 6   the 17 deferred LIVE rows read against their pegs
C6  M-CLASS BATCH         window 7   width 8, M-class, 1-2 per lane
C7  MEASURE AND REPORT    window 8   the L-3 evidence set: 2+ windows of net-closure data
```

**Correction 1 — the denominator moved under the plan already.** E's 196 was measured at
`d137cc6a`; **`43cd1ce` is 197** (X8). E's own §4d reporting contract already governs this: *"Never
the bare net. Never a count without its commit. Never the census's 196."*

**Correction 2 — C3/C4's premise is now partly held by batch 6.** E shapes C3/C4 around `audit-py`
admitting one lane per batch. `[#533]` (born at `f24a169`, lane `m`, merging **last**) decomposes
that monolith into `scripts/audit_checks/`. If it lands, the constraint E built C3/C4 around
changes — **in E's favour** — and the drain batches can widen. E could not know this; the ruling
postdates its base by ~90 minutes.

**Grade: PROPOSED.** The two corrections are **VERIFIED (live)**.

### A2 · An enforcement intake — proposed id **#34**

**VERIFIED (live):** `docs/intake/` holds **28 documents**, highest id **#33**
(`2026-08-12-func-repo-self-description-consolidation.md`). **#34 does not exist** — this arc is a
*birth*, not an edit. Frontmatter schema and lifecycle are `docs/intake/README.md`; the skeleton is
`templates/intake-template.md`; the status-grouped Contents block is generated and gated by
`intake-index-freshness`.

**The theme the six lanes converge on without any of them naming it: organs that exist and gate
nothing.** Nine findings across five lanes, each already carrying its own locator and severity:

| # | finding | source | grade |
|---|---|---|---|
| 1 | Rule B name-checks `docs/audits/*.md` only — `.html`/`.csv`/`.svg` enter unchecked | `[NB4-B]` `B:565-568` | **VERIFIED (live)**, X9 |
| 2 | `templates/ARCHITECTURE-template.md:103` names `docs/diagrams/`, a home the hub's own gate refuses | `[NB4-B]` `B:561-564` | **VERIFIED (live)**, X10 |
| 3 | `audit-health` preflight cannot pass in any fresh clone (registration state is gitignored) | `[NB4-E]` `E:60-66` | **PROPOSED** (E verified on a pristine tree), X2 |
| 4 | lane grammar is *"advisory and wired into no gate at all"*; 3 batches damaged | `[NB4-C]` row 2 | **PROPOSED** |
| 5 | single-flight is *"wired to no hook, so it is invoked rather than enforced"*; 2 latent legs open | `[NB4-C]` `C:201-204` | **PROPOSED** |
| 6 | the documented codex tally format fails the live parser on 2 of 4 legs | `[NB4-C]` `C:408-419` | **PROPOSED** |
| 7 | `preflight_contract` is adoption-first, wired into no gate; run against **0 of 19** contracts | `[NB4-D]` `D:181-193` | **PROPOSED** |
| 8 | nothing asserts manifest↔tag agreement, so a manifest sits declared-but-unreleased and every version check stays green | `[NB4-F]` F3 | **PROPOSED** |
| 9 | `propose_closures` flags 74% of the open set; **0 of 148** valid; its own finish line is unmeasurable | `[NB4-E]` §5 | **PROPOSED** |

**Two things this intake would need to state about itself**, both drawn from the source lanes:
PLAYBOOK is **outside** `canonical_freshness` by a 2026-07-08 ruling (`C:936-943`), so a doctrine
fix carries no stamp obligation and no edited-since-review signal; and `[#487]` already owns the
closure-proposal consumption arc, so item 9 is evidence against an existing row rather than a birth.

**Filing cost, stated because the gate will ask for it:** a new BACKLOG id requires a
`kill-candidates:` line (`backlog-filing-backpressure`), and an L-sized new-feature epic draws the
advisory ADR-98 intake-id WARN. **Grade: PROPOSED** — nothing here is filed.

### A3 · The `[#412]` measurement design — `[NB4-D]` §5

**Gate status, which D states precisely** (`D:370-379`): the frozen roadmap scopes this *"after
batch-4 closes"* and **batch 4 has closed**, so the roadmap gate is **discharged** — but the night-3
sessionplan independently ruled the leg *"a next-window headliner, not a rider"*, and in batch 6
`#412` rides lane `g` as a Done-when **conversion**, which is not this leg. **Nothing is started.**

**The design's whole point** (`D:390-397`): *the instrument already exists.* `telemetry_emit.py` is
landed and wires nothing, so *"the measurement needs no new store, no new dependency, and no new
organ family — it needs call sites."*

**Four parts.** Unit = a **dispatch**, keyed by branch name, with the denominator known ex-ante from
the manifest — *"the property that stops the measurement being reconstructed from survivors"*.
**Three fields, each with a source that exists today**: `t_start` (already collected in the
common-law block, unaggregated), `t_end` (git), `prompt_bytes` (git). A **pre-registered
hypothesis**: *does reducing a contract's authored byte-count change lane outcome?* — prediction
**no effect on outcome, a reduction in authoring cost** — *"if the prediction fails, M1 is the thing
that is wrong."*

**The limit D states before anyone runs it** (`D:425-431`): n is tiny (7 + 12 lanes) and byte-count
is confounded with task difficulty. *"This design yields a descriptive series, not a controlled
comparison, and must be reported as one."*

**A convergence worth recording:** D's three fields deliberately avoid the `events` store, and
`[NB4-B]`'s F1/F2 show exactly why that matters — D1 has no data until timers exist, and D2's
telemetry is destroyed at worktree teardown. **D's design is unblocked precisely because it does not
depend on the legs B found open.** Neither lane cites the other.

**Grade: PROPOSED · DESIGN ONLY, NOT STARTED** (D's own label).

### A4 · The batch-7 roster — `l` · `y` · `533-leg2` · `harvest`

**Standing facts, VERIFIED (live)** from ruling D-1v2 (`3c07314`, merged `43cd1ce`):

- Lanes **`l` and `y` are deferred, not cancelled**. Both contract files stay in
  `$env:CLAUDE_PROMPTS_DIR` **untouched**, and the ruling states they *"open **batch 7** tomorrow,
  running against the decomposed structure this batch lands."*
- The removal cause is on record: `COLLISION l <-> y : scripts/audit.py , tests/test_audit.py` —
  one collision in 66 pairs, derived rather than assumed (neither contract names the file literally).
- Lane **`m` merges LAST** *"so nothing in this batch is merged against a moving foundation, and
  **batch 7 boots on the decomposed tree**."* **Batch 7's premise is therefore conditional on lane
  `m` landing.**

**Proposed roster — 4 lanes.**

| lane | rows | bucket | precondition | source |
|---|---|---|---|---|
| `l` | the `audit.py` detector legs deferred from batch 6 | finish-line | lane `m` merged | D-1v2 |
| `y` | `check_hooks_armed` (`scripts/audit.py:1625`) | finish-line | lane `m` merged | D-1v2 |
| `533-leg2` | `[#533]` residual after lane `m`'s first pass | hub-introspection | lane `m` merged | D-1v2 |
| `harvest` | land the NB4 findings — the arcs in §1/§2 the architect rules IN | hub-introspection | §1 adjudicated | this briefing |

**Its own cap arithmetic**, computed on the batch-6 amendment's stated method
(`width -> floor(width/4)` hub-process lanes):

```
width 4  ->  cap = floor(4/4) = 1 hub-process lane
roster   ->  l, y            = finish-line          (2)
            533-leg2, harvest = hub-introspection    (2)
verdict  ->  2 hub-process lanes declared against a cap of 1  ==  OVER CAP by one
```

**Stated as arithmetic, not as a verdict.** Three ways out exist on the record and the choice is the
architect's: widen the roster (a width of 8 lifts the cap to 2), fold `533-leg2` into `harvest`, or
run one of them in a later batch. This is surfaced now because the batch-6 amendment makes the point
that *"the roster is at cap both before and after; that is arithmetic, not slack"* — a roster
authored without running its own arithmetic is how the cap stops being checkable.

**On the brief's phrase "with its own W5 arithmetic" — reading stated, not assumed.**
**VERIFIED (live):** `W5` is a **batch-4 lane name** (`[#132]`, the organ index; `JOURNAL.md:1765`,
merge `e624a172`). Two readings of the phrase are consistent with the record and this briefing does
not choose between them:
1. **The cap arithmetic** — the roster states its own `floor(width/4)` computation ex-ante, as the
   batch-6 manifest and its amendment both do. That is the reading computed above.
2. **The W5 integrator-debt precedent** — CLAUDE.md §12 v2.57: a lane's `CLAUDE.md` §9 roster row is
   *"OWED TO THE INTEGRATOR, not forgotten"*, keeping a lane's footprint out of the freshness-gated
   collision file and paying the debt at the merge. `JOURNAL.md:1336` warns the precedent does not
   transfer universally — *"W5 deferred a **description** of a landed gate"*.

Under reading 2, `harvest` is exactly the shape W5 describes: a lane that lands descriptions of
gates other lanes built. **Both readings are actionable and neither is contradicted; the operator
holds the intent.** **Grade: PROPOSED** (roster), **VERIFIED (live)** (the D-1v2 facts and the cap
arithmetic), **UNVERIFIABLE** (which reading of "W5 arithmetic" the brief intends).

---

## §3 · Provenance and final metric lines

### 3.1 · Per-lane provenance

All six branches were cut from **`d137cc6a`** and each landed **one tracked report** plus the
mechanically-regenerated `docs/audits/README.md` index. **No branch was merged, rebased, deleted or
modified by this session.**

```
[NB4-A]  llm-acceptance
  branch   claude/nb4-llm-acceptance-benchmark-pnoo2q
  commit   a3a44bc   2026-08-16 12:06 +0000   base d137cc6a
  file     docs/audits/2026-08-16-technical-nb4-llm-acceptance.md   545 lines, class technical
  model    (not stated in report)          status  DRAFT · Tally 2/3/3/2
  limits   nothing was run; no CLI invoked, no model called, no defect seeded, no worktree cut.
           3 primary sources EGRESS_BLOCKED (docs.x.ai, media.x.ai, geminicli.com +
           google-gemini.github.io). Grok 4.6 pricing + Gemini quotas are SECONDARY-SOURCED.
           The corpus is designed, not built. R2/R3/R8 unruled. "This document is itself
           contamination" -- it names the answer key in a tree its own scrub list covers.

[NB4-B]  telemetry-read
  branch   claude/nb4-telemetry-read-path-ivoka2
  commit   5b8aaa5   2026-08-16 12:05 +0000   base d137cc6a
  file     docs/audits/2026-08-16-technical-nb4-telemetry-read.md   626 lines, class technical
  status   DRAFT -- proposals only; no row born, no dependency added, no .gitignore line written
  limits   logs/TELEMETRY.db has NEVER been written -- every claim about what a dashboard would
           SHOW is a claim about a schema, not observed data. Shallow clone, python3 11.15
           against a >=3.12 requires-python, pandas + structlog absent. Mocks are described
           layouts; nothing was built. Intake #9 is SEED -- direction, not a ratified decision.

[NB4-C]  playbook-gap
  branch   claude/nb4-playbook-gap-coverage-1ktsuc
  commit   39f8d5d   2026-08-16 12:10 +0000   base d137cc6a
  file     docs/audits/2026-08-16-verification-nb4-playbook-gap.md  1026 lines, class verification
  status   DRAFT -- REPORT ONLY; no BACKLOG row, tasks/ body, register entry, ADR, manifest or
           protocol file touched
  limits   "board rules 1-8" could not be enumerated -- the set is off-repo; row 10 verdicts the
           in-repo surface only. Batch-4/5 evidence read from artifacts, not execution. The tally
           is bar-dependent (6/1/6 under a weaker bar). No suite run, no gate executed against a
           modified PLAYBOOK -- the +0 ratchet claim is a token count, not an observation.
           audit.py health DEGRADED; all four [!!] are shallow-clone artifacts (contested, X2).

[NB4-D]  equilibrium
  branch   claude/nb4-equilibrium-audit-el1o0w
  commits  0d530a6  2026-08-16 12:08 +0000   the audit
           02861f2  2026-08-16 12:13 +0000   AMENDMENT 1 -- container gaps are [#453]
           ca87d03  2026-08-16 12:14 +0000   AMENDMENT 2 -- uv self update re-tested live
  file     docs/audits/2026-08-16-verification-nb4-equilibrium.md   562 lines, class verification
  model    (pinned in its own report header) status  DRAFT -- PROPOSAL-ONLY
  limits   5 off-repo packs classified from the record, NOT read -- "the weakest evidence in this
           report". The act grain is a choice; the RATIO is more robust than the absolutes.
           "Bypassed" is a claim about absence. Only M1 has measured payoff; M2/M3 are arguments.
           The gate stack did not run -- container fact, no --no-verify used or needed. Two
           in-file amendment markers per CLAUDE.md section 5 rule 3; nothing edited in place.

[NB4-E]  closing-campaign
  branch   claude/nb4-closing-campaign-prep-gb68l0
  commits  021e718  2026-08-16 12:27 +0000   the census delta + campaign plan
           a3e9cb0  2026-08-16 12:29 +0000   the two container gaps [#453] does not cover
           6b96869  2026-08-16 12:31 +0000   trap 3's repair, and the organ that never got to speak
  file     docs/audits/2026-08-16-census-nb4-closing-campaign.md    709 lines, class census
  status   DRAFT -- PREPARES THE CAMPAIGN, DOES NOT OPEN IT · ZERO CLOSES EXECUTED
  limits   Verdicts closure-READINESS, not correctness of a finish line. Did NOT re-read all 196
           rows at census depth -- inherits NB2-F's 2026-08-14 verdicts and re-verdicts only where
           evidence changed. Did not resolve either batch-6 collision. Did not fix the Form-E
           predicate defect. Wrote one tracked file; two gitignored side effects, both declared.

[NB4-F]  fleet-parity
  branch   claude/adr-104-fleet-parity-audit-f1lr7a          <- NOT nb4-prefixed (X7)
  commit   9d1487a   2026-08-16 12:06 +0000   base d137cc6a
  file     docs/audits/2026-08-16-technical-nb4-fleet-parity.md     282 lines, class technical
  model    (pinned in its own report header) status  DRAFT -- ZERO writes to any consumer repo
  limits   THE limit: a remote-HEAD view, not the hub checker's view -- cannot reproduce
           fleet_parity.py's verdict and does not claim to. 5 of 8 members unreachable from this
           session; those rows are UNMEASURED, not measured-and-clean. fleet_parity.py was NOT
           run (it would have produced a false result, not a partial one). No hub row advanced.
```

### 3.2 · What this session verified live, independent of the six lanes

| # | verification | command / module | result |
|---|---|---|---|
| 1 | `main` moved past the shared base | `git log d137cc6a..origin/main` | 4 commits; D-1v2, `[#533]`, roster 12→11 |
| 2 | the live denominator | `tasks/manifest.json` @ `43cd1ce` | **197** task nodes (E measured 196 @ `d137cc6a`) |
| 3 | Rule B's `.md`-only hole | `validate_hermetization.rule_b_violation` | `.md` refused, `.html` admitted — X9 |
| 4 | `docs/diagrams/` refused | `rule_a_violation` + `rule_c_violation` | both fire — X10 |
| 5 | the ratchet headroom | `ecosystem/silent-rule-baseline.yaml` | `baseline: 441`, `silent-rule-v4` — X14 |
| 6 | this container's `uv` | `which -a uv; uv --version` | `/root/.local/bin/uv` → **0.8.17** — X1 |
| 7 | severity tallies across the six | grep `Tally:` | **1 of 6** carries one — X13 |
| 8 | intake `#34` is free | `docs/intake/README.md` + tree | 28 docs, highest **#33** |
| 9 | this file's own ADR-101 admission | `validate_hermetization` A/B/C | no violation on any rule |

**This session's own honest limits.** It ran in an Anthropic cloud container on a **shallow clone**
(277 reachable commits) — so no claim here depends on history below the graft. `uv` is **0.8.17**
against the `==0.11.19` pin, so `audit.py health` and the pre-commit stack were **not** run; the
repairs `[NB4-E]` demonstrated were **not** applied, deliberately, because this lane is read-only and
mutating the environment would have destroyed the X1 data point. **No `--no-verify` and no `SKIP=`
was used or needed — nothing was armed to bypass.** The five off-repo packs remain UNVERIFIABLE here
for the same reason they were for `[NB4-D]`. **The full gate stack is owed at integration on the
operator's clone.**

### 3.3 · The six final metric lines, verbatim

Quoted exactly as each report closes. **Four of six close on a metric line; `[NB4-A]` carries a
header tally instead and `[NB4-B]` carries none** (X13).

```
[NB4-A]  (header, A:14 -- no closing metric line)
- **Tally:** 2/3/3/2 <!-- Critical/High/Medium/Low -->

[NB4-B]  (none -- the report closes on a Sources block)

[NB4-C]  (C:1026)
covered 1 / partial 6 / absent 6

[NB4-D]  (D:562)
**JUDGMENT 13 · MECHANIZABLE 13 · ALREADY-MECHANIZED-BUT-BYPASSED 2 (+5 already-mechanized and used, of 33 acts); the single highest-leverage mechanization is M1 — `gen_lane_contract.py` as assembly-not-generation with a `--check` pre-commit leg — because it moves the measured 48.3% mechanical half of contract emission repo-side while leaving every judgment region hand-authored, and its check leg arms both bypassed organs (`validate_branch_naming`, `preflight_contract`) instead of creating a third.**

[NB4-E]  (E:709)
**NOW-CLOSABLE 2 / AFTER-WAVE 0 / campaign batches 6**

[NB4-F]  (F:273)
**in-parity 2/8 · seeding-ready 0/8**
```

---

## §4 · What this briefing did NOT do

- **Adjudicated nothing.** No decision item carries a verdict of this lane's. Every recommendation
  in §1 is attributed to the lane that made it.
- **Landed nothing on `main`.** No merge, no push to `main`, no branch deleted, no worktree touched.
  Landing happens on the primary machine after batch 6 closes.
- **Resolved no contradiction.** The fourteen ledger entries are recorded, sourced and left open —
  a briefing that silently picks a winner has consumed the evidence.
- **Touched no row, register entry, ADR, contract, gate, manifest or protocol file.** The only
  tracked files it writes are this one and the mechanically-regenerated `docs/audits/README.md`.
- **Did not re-run any lane's work.** The nine live checks in §3.2 verify *specific contested
  claims*; they do not reproduce any lane's analysis, and where a lane's number could not be
  re-derived here it is carried with its source's grade.
- **Did not apply `[NB4-E]`'s container repairs**, deliberately — see §3.2.

---

**aggregated 6 / contradictions 14 / decisions queued 6 (+2 preconditions) / arcs proposed 4 · BINDS NOTHING**

---

## AMENDMENT 1 — 2026-08-16, post-commit: X1's remedy is corrected, and the Stop hook witnessed the class live

*(In-file amendment marker per CLAUDE.md §5 rule 3 — `docs/audits/` is immutable, so this is marked
rather than woven into §0. Nothing above this line is edited, including the metric line, which the
amendment does not move.)*

**The trigger: the class fired on this session, at the surface it is actually about.** After the
commit above was pushed, the `Stop` hook ran and returned:

```
[uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"]:
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

That is `[NB4-E]`'s trap-3 finding reproducing verbatim (`E:70-74`) — *"not a gate that says no, but
**an organ that never gets to speak**, on the one surface that fires unattended"* — and it is at
least the fifth live witness of `[#453]` gap (2) in this window. §0 X1 predicted the state; this is
the state occurring.

**What the hunt then established, and it CORRECTS this briefing's own conclusion.** §0 X1 closed
with: *"the route that preflight should take is **E's un-shadow**, not `uv self update`."*
**That is too strong, and this amendment withdraws it.** Measured on this image:

```
find / -xdev -type f -name uv -perm -u+x   ->  EXACTLY ONE hit: /root/.local/bin/uv  (0.8.17)
no 0.11.19 binary exists anywhere on the filesystem, shadowed or otherwise
uv self update 0.11.19  ->  "The version 0.11.19 was not found for the app uv in workspace uv"
```

`[NB4-E]`'s repair was *"pointing the shadowing `/root/.local/bin/uv` at the pinned 0.11.19 binary"*
(`E:76-78`) — which presupposes a pinned binary present-but-shadowed. **This image has none, so E's
route is not available here, and E's report does not record where its 0.11.19 came from.** That is
the gap: E's repair is real and was demonstrated, but it is **container-local, not a general
route**, and X1 credited it as general.

**So the three-way resolution, which no single lane holds:**

| | claim | status after this test |
|---|---|---|
| `[NB4-D]` | `uv self update` cannot reach the pin on this image | **REPRODUCED, twice more** — verbatim error, both before and after the hunt |
| `[NB4-E]` | the container is repairable by un-shadowing the pinned binary | **TRUE where a pinned binary exists; NOT REPRODUCIBLE here** — none exists |
| this briefing, X1 | the preflight should take E's un-shadow route | **WITHDRAWN** — it only works on an image that already carries the pin |

**The remedy shape that survives both containers is `[NB4-D]`'s, stated at `D:544-546`:** the
preflight `[#453]` owes must *"either assert the pin and **fail fast with a named reason**, or obtain
`uv` from a source other than its own updater."* An un-shadow step is a valid *first* leg, but it
cannot be the only one, because it is a no-op on an image with nothing to un-shadow. **X3 stands
unchanged and is reinforced:** `[NB4-E]`'s four-trap enumeration remains the safer contract; what
changes is only which repair the preflight attempts.

**The organ did get to speak, once run without its wrapper.** `python3 scripts/session_end_backpressure.py`
executed directly under the container's system interpreter **exits 0, clean, with no findings** —
tree clean, branch pushed, and no JOURNAL anchor owed because this session pushed to a
`claude/<slug>` lane branch and not to `main`'s first-parent spine (the ADR-85 hard leg
`block-unanchored-push` is scoped to pushes targeting `main`). **The backpressure verdict is
therefore recorded, not merely unavailable** — the wrapper was the only broken part.

**Three deliberate non-actions, each on a rule this repo already carries.** The pin is **not
bumped** — `pyproject.toml` states a uv upgrade *"is its OWN gated change … never incidentally
mid-arc"*, and this is a read-only lane. **No row is born** — `[#453]` owns this class and its
`kill-candidates:` line already reads *"none — no open task owns cloud-container preflight"*, so a
birth here is the duplicate `backlog-filing-backpressure` exists to refuse. **§0 X1 is not edited** —
it is corrected here, which is this repo's standing move for a claim that has since been overtaken,
and the same move `[NB4-D]`'s own Amendment 2 made on `[NB4-D]`'s Amendment 1.
