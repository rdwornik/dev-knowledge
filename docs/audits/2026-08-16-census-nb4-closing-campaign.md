---
title: "NB4-E — live census delta, closure-readiness classes, and the closing-campaign plan draft"
date: 2026-08-16
class: census
---

# NB4-E — closing-campaign preparation

> **DRAFT · PREPARES THE CAMPAIGN, DOES NOT OPEN IT · ZERO CLOSES EXECUTED.**
> L-3 places the dedicated closing campaign in **windows 3–8** and forbids re-scoping §B
> clause 3's number without **two or more windows of net-closure data**. This lane supplies
> the instrument and the plan; it opens nothing and re-scopes nothing. **No `tasks/` file, no
> `tasks/manifest.json` node, no `BACKLOG.md` row and no register entry was touched.** The
> only file it adds is this one.

**Lane:** `claude/nb4-closing-campaign-prep-gb68l0` (read-only) · **Base / HEAD:** `d137cc6a`
(2026-08-16, the phase-2 Position-0 merge) · **Census base of record:** `7bbb0674` (2026-08-14)

---

## 0. Method, and the two traps this lane hit before it could measure anything

**Inheritance, stated so the depth of this sheet is not overread.** The ratified NB2-F census
(`docs/audits/2026-08-14-census-night2-census.md`) read all 196 rows end-to-end two days ago and
verdicted each one. This lane does **not** repeat that read. It takes the census verdicts as the
base, applies the measured delta, and **re-verdicts only where evidence changed since** — the
seven phase-1 lane merges, the seven Position-0 acts, the night-3 rulings, and its own live
checks. Where a class below rests on the census rather than on a fresh read, the row says so.

**Trap 1 — the shallow-clone trap fired again. Third recorded container instance.**

```
git rev-parse --is-shallow-repository   ->  true
git rev-list --count --first-parent origin/main   ->  46      (oldest 2026-08-10)
```

Every "since its birth" and every velocity column would have been silently wrong. Un-shallowed
before any measurement: **1,454 first-parent commits, 5,114 total.** This is **[#453] leg (1)**
recurring for the **third** time — night-2's census recorded the second, and its own §8 note
says the row's *"a session preflight performs the unshallow and asserts the `uv` pin"* is still
unbuilt. **Recorded here as a third instance against that row; no reopening, no new filing.**

**Trap 2 — local `main` was two days stale and pointed at the census base itself.** `main` and
`origin/main` both read `7bbb0674` on arrival, i.e. the exact commit the census was cut from. A
delta measured against that would have reported **zero change of any kind**. `git fetch`
advanced `origin/main` to `d137cc6a`. Every number below is against `d137cc6a`.

**Traps 3 and 4 surfaced later, at this report's own commit, and are recorded with the first
two because they are one class.** All four are **[#453]**'s subject — *"the container gaps that
silently degrade an unattended run"* — and all four fired in a single session:

```
1  shallow clone            46 -> 1454 first-parent commits after unshallow   (3rd instance)
2  local main stale         at 7bbb0674, the census base itself
3  uv version pin           config pins uv==0.11.19; container ships 0.8.17
                            -> EVERY hook that shells through uv exits 2
4  audit-health preflight   FAILS in ANY fresh clone, by construction
```

**Trap 4 is the one worth stating as a general finding, not an incident.** `audit.py health`'s
operational preflight asserts *">=1 repo registered"*, and registration lives in
`ecosystem/<name>/state.yaml` — which is **gitignored** (`.gitignore:69`). So `discover_repos()`
returns `[]` in any fresh clone, the preflight FAILs, and the `audit-health` **pre-commit gate
cannot pass** — for any commit, by any seat, in any container. **Verified pre-existing on a
pristine HEAD tree with zero changes staged** (`health: DEGRADED`, exit 1, sole finding
`[!!] repos registered (none)`), so it is not an artefact of this lane's file.

**Trap 3's own repair is worth stating, because the obvious one is not enough.** A per-command
`PATH` override in front of `git commit` is sufficient to land a commit and **insufficient for
everything else** — the `Stop` hook (`uv run --locked python scripts/session_end_backpressure.py`)
inherits the session's PATH, not a caller's, and so it **errored out instead of evaluating**:
`error: Required uv version ==0.11.19 does not match the running version 0.8.17`. Witnessed live
at this session's end. That is the failure mode `[#453]` is actually about — not a gate that
says no, but **an organ that never gets to speak**, on the one surface that fires unattended.
Repaired durably by pointing the shadowing `/root/.local/bin/uv` at the pinned 0.11.19 binary
(the shadowed 0.8.17 moved aside, not deleted); `uv self update 0.11.19` does **not** work here
— it reports *"version 0.11.19 was not found for the app uv in workspace uv"*, so the error
message's own suggested remedy is a dead end in this container. The hook then ran clean.

Repaired locally rather than bypassed: the hub's own registration was restored through
`audit.save_state`, which is the writer the tool's own bootstrap path uses. `.dev-knowledge` is
the **first declared member of `adr104-fleet-members`** and already carries a tracked
`ecosystem/.dev-knowledge/history/`, so this restores intended state rather than inventing
membership. One gitignored file written; no tracked change; `health: OK` after. **The full gate
stack then ran green on this report's commit with no `--no-verify` and no `SKIP=`.**

Recorded as evidence against `[#453]` — whose own Done-when asks for *"a session preflight
[that] performs the unshallow and asserts the `uv` pin"*, i.e. traps 1 and 3 but **not** traps 2
and 4. **The row is not reopened, re-scoped or amended by this lane**; the two uncovered gaps
are named here so the next seat reading it has them.

**Honest limit of this sheet.** It verdicts *closure-readiness*, not correctness of a finish
line. Where a row's Done-when is itself the defect, that stays [#456]'s cohort and [#505]'s
clause-strike precedent. Three rows below are exceptions the evidence forced, and each is
flagged in place.

---

## 1. The denominator, stated before any number is used

**Live count at `d137cc6a` — 196.**

```
python scripts/validate_backlog.py
  -> OK (9 themes, 26 stories, 196 tasks, 1 warning)

196 live = 172 status:open + 24 status:deferred
```

The filter is **H2's live count** (open **plus** deferred), which **L-3** rules is also §B
clause 3's filter — *"one denominator everywhere"*. Every figure in this report is against 196.

### The trap the brief names, and it is real: 196 then, 196 now, **different set**

The census reported **196**. The live count today is **196**. Reporting that number bare would
read as *nothing moved*, and the truth is that **8 rows changed identity underneath it**:

```
census 196  -  4 closed  +  4 born  =  196 live today

closed: #352  #364  #524  #527
born:   #529  #530  #531  #532
```

**Denominator discipline for the campaign, stated as a rule:** a closing-campaign report cites
the live count **measured at the commit it reports against**, names that commit, and reports
**closed and born separately** — never a bare net, and never the census's 196 as a standing
figure. A net of zero is the *outcome* of 4 and 4; it is not the observation.

---

## 2. The live census delta since NB2-F

### 2a. The eight rows that moved

```
CLOSED (4)
  #352  versioned .vscode region decoration        8f9896e  2026-08-15  already-shipped (ADR-65)
  #524  four ruled check extensions                8f9896e  2026-08-15  already-shipped (ADR-65)
  #364  BACKLOG#353 accretion, prevention->repair  e9482bf  2026-08-15  obsoleted, premise discharged
  #527  commit-time direct-to-main gate            e123947  2026-08-16  Done-when met, 3 of 3 legs

BORN (4)
  #529  telemetry v1 EMIT                          e40308a  2026-08-15
  #530  single-flight dispatch guard               bf3c1b4  2026-08-15
  #531  lane-grammar enforcement at provisioning   e6ee9a1  2026-08-16
  #532  doc_rot arms split                         e6ee9a1  2026-08-16
```

**Both of the census's proposed-dead rows were executed** (#352, #524 at `8f9896e`). The
census's dead cohort is drained to zero. #364 was retired on a different reason — its premise
was overtaken by the 1320-char threshold, which is the fork the wave-2 drafts flagged at §5.1.
#527 is the only *built-then-closed* row in the window.

### 2b. Net closure — the data L-3 says a re-scope requires

Measured live over 19 days of `origin/main` first-parent history, one reading per day, live
count taken from `tasks/manifest.json` at each day's newest commit:

```
date        live   net   closed / born
2026-07-28   176         (baseline)
2026-07-29   178    +2   -1  +3
2026-07-30   181    +3   -2  +5
2026-07-31   190    +9   -5  +14
2026-08-01   186    -4   -6  +2
2026-08-02   186    +0   -0  +0
2026-08-03   188    +2   -3  +5
2026-08-04   187    -1   -3  +2
2026-08-05   199   +12   -1  +13
2026-08-06   202    +3   -3  +6
2026-08-07   202    +0   -6  +6
2026-08-08   194    -8   -8  +0
2026-08-09   196    +2   -3  +5
2026-08-10   196    +0   -0  +0
2026-08-11   195    -1   -2  +1
2026-08-12   194    -1   -2  +1
2026-08-13   194    +0   -2  +2
2026-08-14   196    +2   -1  +3     <- NB2-F census cut here
2026-08-15   195    -1   -3  +2
2026-08-16   196    +1   -1  +2

19 days:  closed 52 (2.74/day) · born 72 (3.79/day) · NET +20
best single window (2026-08-06 -> 2026-08-08):  net -8
```

**The finding this campaign has to be built around: the set is growing, not shrinking.** Over
19 days the repo closed 52 rows and birthed 72. The closure rate is real and healthy — 2.74
rows/day is not a stalled backlog — and it is **out-run by the birth rate**. The census's
reading (*"the rows are open because the work is not done"*) is confirmed and sharpened: the
rows are open because work arrives faster than it finishes.

**Since the census specifically: closed 4, born 4, net 0.** That is **window 1** of the two-or-
more L-3 requires before §B clause 3's number may be re-scoped. **This lane does not re-scope
it, and the plan in §4 does not assume it will be.**

---

## 3. Closure-readiness, per open row

### 3a. Class definitions, stated so each is checkable

| class | predicate |
|---|---|
| **NOW-CLOSABLE** | the Done-when **as currently written** is met on `main` @ `d137cc6a`, with cited evidence. The remaining act is ratification (`/review-closures`), not engineering |
| **CLOSABLE-AFTER-WAVE-2** | the current clause is unverdictable; the batch-6 wave-2 conversion makes it checkable **and** the converted clause reads MET, so conversion-and-close is one act |
| **NEEDS-ACT** | a bounded non-build act — a re-peg, an un-defer, a register entry, a recorded decision — is the whole remaining distance |
| **NEEDS-RULING** | no executor may lawfully start: the row's own text bars a build until a decision lands, **and** its Done-when's leading clause is that decision (NB2-F §4's predicate, inherited unchanged) |
| **LIVE** | real unbuilt engineering |

### 3b. The count

| class | n | share of 196 |
|---|---|---|
| **NOW-CLOSABLE** | **2** | 1.0% |
| **CLOSABLE-AFTER-WAVE-2** | **0** | 0.0% |
| **NEEDS-ACT** | **4** | 2.0% |
| **NEEDS-RULING** | **25** | 12.8% |
| **LIVE** | **165** | 84.2% |
| **total** | **196** | 100% |

**The shape, not the number.** Two closable rows out of 196 is not a failure to look — it is
what an aggressively-groomed set looks like two days after its dead cohort was drained. The
campaign's leverage is **not** in the NOW-CLOSABLE column. It is in §4's two levers: the 25-row
ruling batch, and birth suppression.

### 3c. NOW-CLOSABLE — 2 rows, with evidence

**`[#417]` P3/S — `check_dirty_tree` runs with no pathspec.** Its clause reads *"the dirty-tree
leg ignores tool-owned writer-isolated paths with a test, or the exclusion is recorded rejected
with a reason."* The first disjunct is **met on `main` today**, verified live by this lane:

```
scripts/session_end_backpressure.py:402   _is_lane_owned_daily()  — untracked ?? entries only,
                                          _LANE_DAILY_RE = ^ecosystem/[^/]+/history/[^/]+$
scripts/session_end_backpressure.py:412   check_dirty_tree()
scripts/session_end_backpressure.py:418   changes = [ln for ln in changes
                                                     if not _is_lane_owned_daily(ln)]

tests/test_session_end_backpressure.py:758  lane-owned daily on the lane -> does NOT flag
                          :766  stray untracked file under history/  -> STILL flags
                          :776  daily not yet on the lane             -> STILL flags
                          :785  daily on lane with DIFFERENT content  -> STILL flags
                          :799  exclusion applies to untracked only
                          :807  a daily does not mask other dirt
```

The test leg exists **in both directions**, which is what the clause's *"with a test"* has to
mean for an exclusion. Landed at `4bef950`.

> **How the census missed it, and it is a locator-rot finding rather than a reading failure.**
> The census's reason line reads *"`session_end_backpressure.py:340-349` still calls a bare
> `git status --porcelain`"* — inherited verbatim from the row's own `refs` pin. That pin has
> rotted: **`:340-349` is now `check_backlog_marker`**, a different function entirely. The
> wave-2 drafting lane re-derived the locator a day later and found the clause met (drafts
> §5.3). Re-verified independently here. **This is the third recorded instance of a row's stale
> line pin propagating into a downstream verdict** — the class `[#503]`/`[#497]` own, and the
> reason every wave-2 draft names a symbol or a section instead of a line.

> **COLLISION, FLAGGED LOUDLY: `[#417]` is dispatched RIGHT NOW as batch-6 lane `f`'s
> conversion target.** Lane f (`worktree-lane-f-130-conversions`, rows `#130 #274 #350 #417`)
> is converting a clause that is already discharged. The drafts file anticipated exactly this
> and named the fork (§5.3 (a) *"the Done-when is discharged and the correct act is a closure
> proposal, not a conversion"*). **This needs the operator's word before lane f integrates**,
> or a converted-and-immediately-closable row lands with a conversion that was never needed.

**`[#506]` P2/M — Whole-set P10 grooming arc.** Its clause has four legs; all four hold:

| leg | state |
|---|---|
| *"a `docs/audits/` sheet carries one row per `status: open` task with its last-touch date and closing-merge cross-check"* | **MET** — NB2-F §9, 196 rows, `task-file touch` + `spine refs since birth · newest` columns |
| *"(count matching the live open count at generation time)"* | **MET** — 196 at `7bbb0674`, derived live from `validate_backlog.py`, on H2's filter per L-3 |
| *"each id carries a live / dead / awaiting-ruling verdict"* | **MET** — 169 / 2 / 25 |
| *"every id verdicted dead is closed per ADR-65 or named as deferred"* | **MET** — `#352` and `#524` both closed at `8f9896e` (2026-08-15) |

> **The fork, stated rather than resolved, because it is the operator's.** The census's own
> header disclaims discharge: *"This artifact **prepares** the booted architect's P10 duty
> ([#506]); it does not discharge it."* The row's Done-when asks for the sheet, the verdicts and
> the dead closes — all delivered. So the **clause** is met while the **artifact** declines to
> claim it. That is a genuine conflict between a row's finish line and its producer's
> self-description, and a closing campaign that resolves it silently either way is closing on
> its own authority. **Proposed NOW-CLOSABLE with the conflict named**, not asserted closed.

### 3d. CLOSABLE-AFTER-WAVE-2 — **0**, and this is the campaign's most load-bearing finding

The 29 wave-2 rows are dispatched **right now** as batch-6 lanes `a`–`g`. Set reconciled live:

```
the 29 needs-draft rows  -  #364 (closed 2026-08-15)  +  #419 (the P2 re-check)  =  29 dispatched
all 29 verified status: open at d137cc6a
```

**Every one of the 29 was tested against its own drafted clause. Not one reads MET.** The
drafted clauses were checked mechanically against the live tree by this lane:

```
Form E — "STANDING_RULINGS.md carries a section naming [#NNN]"  (12 rows)
   #146 #210 #239 #263 #350 #351 #391 #412 #417 #443 #484 #491
   -> a genuine ruling section exists for ZERO of the 12

Form R — an ADR-105 `· routine:` block that routine_consumers passes  (6 rows)
   audit.py check_routine_consumers -> "2 declared routine row(s)" = #348, #426 only
   -> ZERO of the 6 carry one

Named-artifact clauses (the remaining 11) — spot-verified live:
   #263  ecosystem/doc-code-edge.yaml still carries mermaid_theme_directive     UNMET
   #274  .claude/commands/changelog-review.md contains no "dogfood" token       UNMET
   #285  protocols/PLAYBOOK.md has no last_reviewed; absent from
         _HUB_ONLY_FRESHNESS_FILES (audit.py:294 holds 3 files, not PLAYBOOK)   UNMET
   #361  block_immutable_edits.py:83 zone is still transcripts-only             UNMET
   #391  fleet_analytics appears in the wall's PATH SCOPE, never as a schedule  UNMET
   #417  MET -> but on its CURRENT clause; see 3c. Not an after-wave close
```

The remaining artifact-gated drafts (`#82 #130 #145 #324 #350 #351 #385 #393 #412 #438 #443 #484
#491 #502`) each require a `docs/audits/<date>-technical-*` artifact for a subject — a hygiene
digest, a codification pass, a fleet Python upgrade path, an audit-corpus verb list, a corp-sca
rot review — that the drafting lane verified absent on 2026-08-14. The only merges since are the
seven enumerated phase-1 lanes and the seven Position-0 acts, none of which produced any of them.

> **So: wave 2 buys VERDICTABILITY, not closure.** It converts 29 unverdictable clauses into
> checkable ones and closes **zero rows**. That is not a criticism of wave 2 — the conversion
> programme's own commit of record says exactly this, and says it as a negative rather than
> letting it be discovered: *"the convertible mass does NOT change the under-100 arithmetic.
> Conversion yields zero closes; it makes rows adjudicable"* (`08c880f61` body, the
> backlog-testability census). What is new here is the **measurement** of that claim against
> the 29 rows actually dispatched, two days later, on a live tree. A campaign plan that budgets
> net closure against wave 2 will miss by 29.

#### The predicate defect wave 2 would otherwise ship — **fix this before lanes a–g integrate**

Form E's drafted predicate is *"a `###` section in `protocols/STANDING_RULINGS.md` whose body
contains the literal `[#NNN]`"*. Measured against the live register:

```
[#409] [#410] [#411]  appear inside  ### L-8  and  ### M-7
[#415] [#425]         appear inside  ### L-8  and  ### M-7
[#502]                appears inside ### H4
```

Those mentions are **fold-set and removal-sheet rulings** — L-8 rules the trio *stays distinct*;
it does not rule the night batches *out*. Under the drafted predicate the escape branch reads as
**already satisfied for #409/#410/#411**, which would make three rows spuriously closable the
moment lane `a` converts them, on a ruling that says the opposite. **Recommended repair, minimal
and checkable:** the predicate must require the section to be *about* the row — a `###` heading
whose title names the id, or a body line of the form `[#NNN]` **followed by a disposition
token** — not a bare literal anywhere in a section body. This is a conversion-instrument defect,
not a row defect, and it is cheapest to fix in the contract rather than after 29 clauses ship.

### 3e. NEEDS-ACT — 4 rows, no engineering in any of them

| id | P/S | the act |
|---|---|---|
| **`[#102]`** | P2/M · deferred | **Re-peg.** Its DEFER peg is *"a repo whose codemap is generator-MANAGED"* and the row itself adds *"so no fleet codemap migration is coming to peg on"* — **a peg that states it cannot fire.** The Done-when is buildable. Un-defer or re-peg; the row cannot advance on its own trigger |
| **`[#325]`** | P3/S · deferred | **Re-peg.** In-row: *"DEFER — peg #221 DEAD, unreplaced 2026-08-09 … Stays open, **stranded**"*. `[#294]` was checked and cannot absorb it, `[#236]` is closed |
| **`[#181]`** | P2/S · deferred | **Re-peg onto an evaluable surface.** Its peg names `logs/coherence-nudge.log`; the canonical name has been `logs/COHERENCE-NUDGE.log` since the 2026-07-22 UPPERCASE-KEBAB ruling **and it is gitignored** (`.gitignore:81`). The peg *"the nudge log has enough entries to adjudicate"* is un-evaluable from any fresh clone and per-working-tree besides |
| **`[#492]`** | P3/S · deferred | **Dated trigger falls due 2026-08-17 — tomorrow.** Register `I-D` item 1, the Grok 4.6 re-check. Un-defer on the date; the comparison itself is then ordinary work |

`[#102]`/`[#325]` are NB2-F §7b verbatim; `[#181]` is its §8 note 1; `[#492]` its §7c. **All four
are [#505]'s clause-2 class — a finish line whose measurement can no longer be taken.** None is a
new filing; each already carries its diagnosis in-row. What they lack is a re-peg.

Deliberately **not** in this class: `[#348]`/`[#426]` (`review_date:` 2026-08-26), `[#322]`
(2026-09-09), `[#413]` (Done-when does not open before 2026-10-22) — future dates, not overdue
acts. And `[#428]`, whose leg 2 *is* dischargeable today by a non-build act (close the 15
`nightly-triage` Issues, record `15` in the commit — night-3 D5), but whose leg 1 needs a test
seeding a dead producer. A row with a build leg is LIVE however cheap its other leg is.

### 3f. NEEDS-RULING — 25 rows, unchanged and re-verified

The census's 25 (§4a 5 · §4b 11 · §4c 9), **all still open, none ruled since**. Verified: exactly
one register/decisions commit landed in the window (`a102e0db`, the journal-spine advisory
disposition + I-D7 retirement) and it names **none** of the 25.

```
4a operator-owned by authority (5)   #122 #189 #300 #346 #420
4b question-shaped by declaration (11) #323 #331 #347 #397 #406 #407 #409 #410 #411 #449 #450
4c decision-first, build-after (9)   #43 #126 #308 #371 #408 #414 #491 #494 #495
```

**The census's own sharpest observation stands and is now schedulable:** `[#409]`/`[#410]`/
`[#411]` are *"one architect decision releasing three rows"*, and `[#494]`'s peg has been met
since batch 4 closed 2026-08-14. **A quarter-day of rulings unblocks 25 rows — a larger change
to the workable set than any close batch available.** That is the campaign's first lever.

> **Second collision, flagged: four of the 25 are inside batch-6's wave-2 set** — `#409`,
> `#410`, `#411` (lane `a`) and `#491` (lane `g`). Lanes are converting the finish lines of rows
> no executor may lawfully start. That is legitimate work — a conversion is not a build — but it
> means the ruling batch and the conversion batch **must not both claim those four**, and the
> Form-E predicate defect in §3d lands on exactly three of them.

### 3g. LIVE — 165 rows, shaped for the campaign

```
by priority   P1  7    P2  82   P3  76
by size       S  95    M  65    L   5
status        open 148 · deferred 17

by serialize-group (contention unit — at most one lane per group per batch)
  (ungrouped)          24 S   22 M   3 L    49
  audit-py             27 S   14 M   1 L    42
  architecture         10 S    4 M   1 L    15
  handoff               7 S    6 M   0 L    13
  settings-json         7 S    5 M   0 L    12
  environment           3 S    5 M   0 L     8
  playbook              3 S    3 M   0 L     6
  gates                 4 S    1 M   0 L     5
  claude-md             3 S    1 M   0 L     4
  pre-commit-config     2 S    2 M   0 L     4
  codex-review          4 S    0 M   0 L     4
  coherence             1 S    1 M   0 L     2
  code-edge             0 S    1 M   0 L     1
```

**The structural constraint the campaign inherits: `audit-py` holds 42 of the 165 LIVE rows and
admits exactly one lane per batch.** At 2–4 rows per lane that group alone needs 11–21 batches
to drain. Any plan that treats width as the throughput lever is wrong; **the serialize-group
distribution is the throughput lever**, and it is the reason §4's batches are shaped by group
rather than by priority.

Of the 165, **24 are in the wave-2 set** — converted-but-unbuilt after batch 6 lands. They stay
LIVE; what changes is that they become verdictable.

---

## 4. The campaign plan — draft

### 4a. What the finish line actually requires, arithmetically

§B clause 3 is *"open backlog < 100"*, scored on the H2 live denominator (L-3).

```
196 live  ->  <100  requires net -97
observed net rate      +1.05/day     ->  never reached
observed close rate     2.74/day     ->  35 days IF births were zero
observed birth rate     3.79/day
L-3's window            windows 3-8  =  6 windows
required per window     -16.2 net
best window ever observed   -8       (2026-08-06 -> 2026-08-08)
```

**The conclusion the plan is built on: closure alone cannot reach the number, and the binding
constraint is the birth rate, not the closure rate.** 2.74 closes/day sustained over six windows
is roughly the observed rate — it is the 3.79 births/day that makes the target unreachable.
**A closing campaign that does not carry a birth budget is not a closing campaign.**

This is data, not a re-scope proposal. **L-3 requires two or more windows before the number may
move; this is window 1.** The campaign's own reporting (§4d) produces window 2 and beyond.

### 4b. Six batches — one per window, windows 3–8

Each batch names its shape, its row source, its **birth cap**, and its expected net. Expected
net is derived from the measured day-series in §2b rather than from intent or from per-batch
attribution the record does not cleanly support:

```
the six transitions spanning batch 4's close, batch 5 (phase 1), and Position 0
each row is the move INTO that date, from the 2026-08-10 baseline of 196 live

  -> 2026-08-11   -2 closed  +1 born   196 -> 195
  -> 2026-08-12   -2         +1        195 -> 194
  -> 2026-08-13   -2         +2        194 -> 194
  -> 2026-08-14   -1         +3        194 -> 196
  -> 2026-08-15   -3         +2        196 -> 195
  -> 2026-08-16   -1         +2        195 -> 196
  ------------------------------------------------
  totals         -11        +11        196 -> 196   NET 0
```

**Three batch arcs in a row netted zero**, at a real and sustained closure rate of ~1.8/day.
Every figure below is stated against that baseline rather than against hope. Batch 6 is
mid-flight and has closed nothing yet.

```
C1 · THE RULING BATCH                                   window 3
  shape        NOT a lane batch — one architect sitting over the 25 NEEDS-RULING rows
  rows         the 25, in the census's own three groups; #409/#410/#411 are ONE decision;
               #494's peg is already met
  prerequisite the Form-E predicate repair (§3d) lands FIRST — otherwise the trio's
               escape branch is spuriously satisfied the moment lane a integrates
  birth cap    0
  expected     net closure 0 · unblocks 25 rows into buildable state
  why first    it is the only act in the whole campaign that moves 25 rows, and it costs
               a quarter-day; every batch after it draws from a larger lawful pool

C2 · THE RATIFICATION + RE-PEG BATCH                    window 3 (rides C1)
  shape        one seat, no lanes
  rows         NOW-CLOSABLE #417 #506  ·  NEEDS-ACT #102 #181 #325 #492
  gate         #417's lane-f collision and #506's clause-vs-artifact fork are OPERATOR
               decisions; the batch executes them, it does not resolve them
  birth cap    0
  expected     net -2 (closes) · 4 rows re-pegged onto evaluable triggers

C3 · AUDIT-PY DRAIN I                                   window 4
  shape        width 8-10; ONE lane on audit-py (its 27 S-class rows), the rest drawn
               from ungrouped-S (24), gates (4 S), codex-review (4 S), claude-md (3 S)
  rows         S-class only — 3 rows/lane
  birth cap    2 per batch, enforced by the existing kill-candidates backpressure
  expected     closes 8-12 · births <=2 · net -6 to -10

C4 · AUDIT-PY DRAIN II + THE WAVE-2 RESIDUE             window 5
  shape        same as C3, plus the 24 wave-2 rows that batch 6 will have made verdictable
  rows         S-class; the wave-2 residue is now checkable, so a lane can finish rather
               than re-read
  birth cap    2
  expected     closes 8-12 · net -6 to -10

C5 · THE STRANDED + DEFERRED SWEEP                      window 6
  shape        width 6-8; the 17 deferred LIVE rows read against their pegs
  rows         every deferred row's peg re-evaluated: fired -> un-defer and finish;
               dead -> re-peg; unmeetable -> [#505] clause-strike route
  birth cap    2
  expected     closes 5-8 · a further ~6 rows re-pegged · net -3 to -6

C6 · THE M-CLASS BATCH                                  window 7
  shape        width 8; M-class rows, 1-2 per lane, drawn across groups
  rows         65 M-class LIVE rows; architecture (4 M) and handoff (6 M) first
  birth cap    2
  expected     closes 6-10 · net -4 to -8

C7 · MEASURE AND REPORT                                 window 8
  shape        no lanes — the campaign's own packet
  deliverable  the six-window series in §2b's format, the ratio instrument's readings
               (§5), and the L-3 evidence set: TWO OR MORE windows of net-closure data
  expected     net 0 · this is the artifact that makes a clause-3 re-scope lawful, or
               proves it unnecessary
```

**k = 6 execution batches (C1–C6) plus C7, the measurement batch.** C1 and C2 share window 3
because C2 is a ratification act, not a build.

**Cumulative expected net at the optimistic end of every range: −29.** Against a required −97.
**Stated plainly rather than smoothed: this plan does not reach under 100 in windows 3–8.** What
it does reach is (a) 25 rows released from ruling-block, (b) the birth rate under an explicit
cap for the first time, and (c) two-plus windows of net-closure data — which is exactly the
evidence L-3 names as the precondition for re-scoping the number. **The plan's honest output is
the evidence for that decision, not the number itself.**

### 4c. Batch shapes — the three rules the row data forces

1. **Shape by serialize-group, not by priority.** `audit-py` holds 42 of 165 LIVE rows and takes
   one lane per batch. Width above ~10 buys nothing once the groups are saturated: 13 groups,
   of which `(ungrouped)` is the only freely-parallel pool.
2. **S-class first, and only S-class in C3/C4.** 95 of 165 LIVE rows are S. A batch of S-rows
   closes rows; a batch of M-rows advances them. Both are needed — hence C6 — but a *closing*
   campaign that opens with M-class work reports advancement and closes nothing.
3. **Every batch carries a birth cap and reports against it.** The `backlog-filing-backpressure`
   commit-msg gate already forces a `kill-candidates:` line on every new id; the campaign's
   addition is a *numeric cap per batch*, reported in the packet next to the closes. This is the
   lever §4a identifies as binding and it is the only one not currently instrumented.

### 4d. Denominator discipline — the reporting contract

Every campaign artifact — manifest, packet, digest — reports:

```
live-count: <N>  at <sha>          # H2 filter: status:open + status:deferred, per L-3
opened: <n>  closed: <n>  net: <+/-n>
births against cap: <n>/<cap>
```

**Never the bare net. Never a count without its commit. Never the census's 196.** The 196 in
this report is measured at `d137cc6a` and is a different set from the census's 196 — §1 shows
the eight rows that make it so. **`[#505]`'s "operator-touch count recorded in the batch
manifest" and H2's velocity line already require most of this shape; the campaign's addition is
the birth-cap line.**

---

## 5. The ratio instrument — `[#277]`'s STRONG:WEAK becomes the campaign's live metric

### 5a. The live readings, taken this lane

**Run 1 — the organ as it actually fires** (`python scripts/propose_closures.py`, session-start
shape, whole history because no prior baseline exists in this container):

```
propose_closures: 3 strong, 0 weak over 5114 commit(s) -> PROPOSALS-2026-08-16.md
                  (weak suppressed: cold start)
```

**Run 2 — the 30-day window `[#277]`'s Done-when actually names**, computed by calling the
module's own `find_strong` / `find_weak` against `21e37683..origin/main`:

```
window        2026-07-17 .. 2026-08-16   (1651 commits on origin/main)
open ids      196
STRONG        3     #430  #505  #530
WEAK        145     74.0% of the whole open backlog
                    90.1% of the 161 open rows that cite any repo path at all
```

### 5b. Adjudicating the 3 STRONG — **0 valid**

| id | evidence commit | reading |
|---|---|---|
| `#430` | `3cf3a5b0b` — body: *"**Closes [#430] half (a)** and clears the standing RED"* | **INVALID — partial-closure mis-read.** The row is one defect in two halves; half (b) (`fleet_parity` reading live sibling-repo state) is untouched. The detector cannot see the word `half`. **A fourth distinct defect class in this organ**, after the quoting defect ([#437], fixed), the negation defect ([#454], open) and the two recorded `[#370]` false positives |
| `#505` | `25ff8ec37` — subject: *"3 rows filed, **0 closed** [#505] [#430]"* | **INVALID — negation false positive.** `CLOSES_RE` matches the bare `closed [#505]` adjacency while the subject declares zero closures. Reproduced this lane; already annotated twice in the record (`e351b685f`, `cd38fb8a8`) and re-rejected by night-3's D1 |
| `#530` | `73da833ca` — body: *"…does **not close [#530]**"* | **INVALID as evidence — [#454]'s defect verbatim.** And the trap [#454]'s own row names: the row's four Done-when clauses **are** met (night-3 §8: *"MET (4 of 4)"*), so the proposal is **accidentally right on the outcome and wrong on every fact it cites**. Ruling **R2** of 2026-08-15 then ruled `[#530]` **stays OPEN** with two P1 legs filed on it, so it is not closable either |

**Reading: STRONG-actioned = 0 of 3.** One of the three names a genuinely-complete row, by
accident, and that row is ruled open regardless.

### 5c. The ratio, against `[#277]`'s own bar

`[#277]`'s Done-when asks for *"a single run over the last 30 days of `main` [yielding] a
STRONG:WEAK-actioned ratio better than 49:0"*.

```
2026-07-07  (the row's own baseline)    49 proposals    0 valid
2026-08-16  (measured this lane)       148 proposals    0 valid       3 STRONG + 145 WEAK

the ratio has got WORSE by 3x, not better
```

WEAK's composition explains it without needing a per-row read — the top evidence paths are the
files that change **by construction** every arc:

```
protocols/STANDING_RULINGS.md    29 rows cite it    <- churn
scripts/audit.py                 22                <- churn
protocols/HANDOFF_PROCESS.md     11                <- churn
protocols/PLAYBOOK.md            11                <- churn
```

A detector that flags 74% of the open set ranks nothing. Night-3's D2 reached the same verdict
independently on a 159-row measurement and dismissed the class without a per-row reading.

### 5d. Two structural defects in `[#277]`'s own finish line — report, do not reopen

1. **The 30-day run its Done-when names has no supported invocation.** `propose_closures.py`
   derives its window from prior `logs/PROPOSALS-*.md` frontmatter (`resolve_window`, `:329`);
   there is **no CLI flag and no date argument**. Run 1 above is what the organ actually
   produces — a whole-history cold start with WEAK suppressed. Run 2 required calling
   `find_strong`/`find_weak` directly. **The clause names a run shape the organ cannot emit.**
2. **Leg (a) has become unverifiable.** It requires *"the two STRONG false positives no longer
   surface (pinned by a test seeding each)"* — `#5` and `#77`. Neither surfaces today, but
   **not because either was suppressed**: no suppression list exists in the script, and both ids
   are simply no longer open, so the still-open guard filters them. A test seeding each would
   pass **vacuously**. This is `[#505]`'s clause-2 class again — a measurement that can no
   longer be taken — landing on the very row that owns the detector.

**Filed as evidence against `[#277]`, and against `[#456]`'s finish-line cohort. Neither row is
reopened, re-scoped or closed by this lane.** `[#277]` is dispatched **right now** as batch-6
lane `i` (`worktree-lane-i-277-issues-evidence`), which is the correct place for both findings
to land.

### 5e. How the ratio becomes the campaign's live metric

The instrument is already deterministic, read-only and ADR-70-sanctioned. What it lacks is a
**consumer** — 149 proposals are parked and nothing reads them ([#487]). The campaign is that
consumer. Proposed shape, for the operator's word:

```
PER BATCH, in the packet, next to the velocity line:

  ratio: STRONG <s> / WEAK <w> / ACTIONED <a>   window <sha>..<sha>  (<d> days)

  s  STRONG proposals in the batch's own window
  w  WEAK proposals in the same window
  a  proposals that became an actual close in that batch     <- the number that matters

  campaign health = a/(s+w) trending UP across C1..C6
  today's reading = 0/148 = 0.0%
```

**Why this and not a count of closes.** A closes-count says how much the campaign shipped. The
ratio says whether the repo's own closure detector can *see* what shipped — and the campaign's
whole premise is that the open set is bigger than anyone's read of it. Two properties make it
the right metric:

- **It is falsifiable in the wrong direction.** Closing rows the detector never proposed drives
  `a/(s+w)` down, not up. The metric therefore cannot be gamed by closing easy rows; it improves
  only when detection and closure converge.
- **It is already measured, by an organ that runs at every session Stop.** No new machinery, no
  new surface. The campaign supplies the window boundaries (batch base → batch tip) that
  `resolve_window` cannot currently express — which is defect (1) in §5d, and fixing it is a
  prerequisite the campaign should carry rather than a nice-to-have.

**Baseline for C1, recorded here so the trend has an origin:** `STRONG 3 / WEAK 145 / ACTIONED
0` over `21e37683..d137cc6a`.

---

## 6. What this lane did NOT do

- **Opened nothing.** L-3 places the campaign in windows 3–8; this is preparation. No batch was
  dispatched, no manifest written, no lane provisioned.
- **Re-scoped nothing.** §B clause 3's number is untouched. §2b is **window 1** of the two-or-
  more L-3 requires.
- **Closed nothing, killed nothing, re-pegged nothing.** `[#417]` and `[#506]` are *proposed*
  NOW-CLOSABLE; the four NEEDS-ACT rows are *proposed* re-pegs. No `tasks/` file, no manifest
  node, no `BACKLOG.md` row moved.
- **Did not re-read all 196 rows at census depth.** §0 states the inheritance. The delta and the
  re-verdicted rows were read live; the rest carry NB2-F's verdict of 2026-08-14.
- **Did not resolve the two collisions with batch 6 in flight** (`[#417]` vs lane `f`; the four
  NEEDS-RULING rows vs lanes `a`/`g`). Both are named for the operator; a prep lane that resolved
  a live batch's scope would be overturning a dispatch.
- **Did not fix the Form-E predicate defect.** It is named with a proposed repair (§3d) because
  it lands inside a batch that is already running.
- **Wrote one tracked file — this one** (plus the mechanically-regenerated
  `docs/audits/README.md` index its own gate requires). Two gitignored files were produced as a
  side effect and are ephemeral by design: `logs/PROPOSALS-2026-08-16.md` (the detector's own
  output, `.gitignore:26`) and `ecosystem/.dev-knowledge/state.yaml` (the registration repair in
  §0, `.gitignore:69`).

---

**NOW-CLOSABLE 2 / AFTER-WAVE 0 / campaign batches 6**
