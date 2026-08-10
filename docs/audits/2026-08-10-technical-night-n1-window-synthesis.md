# Night N1 — window synthesis 2026-08-10/11, and a DRAFT execution-challenge pre-fill

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** night-n1-window-synthesis
- **Seat:** cloud lane (Opus 5), branch `claude/night-n1-synthesis-467s4h`. **READ-ONLY.**
  This report rules nothing, proposes no births, and closes nothing.
- **Base:** `origin/main` @ **`5455c2a2a008e0ce8cc1d8ac77d2835cfd767376`** (`5455c2a`,
  *"Merge branch 'docs/arc9-lane-census'"*), fetched at session start. Every fact below
  reads that one tree.
- **Filename pre-verified** against `validate_hermetization.classify()` (returns `None` =
  no violation) — the same pre-check the Fable lane recorded.

## Declared conditions — read before trusting any cell

**1 — The clone is SHALLOW and GRAFTED.** `git rev-list --count origin/main` = **293**;
the graft boundary is `4aba3854`. Consequence, stated as the contract requires: **this
report asserts no freshness or staleness verdict of the `canonical_freshness` class.** A
shallow graft makes whole files read as fresh creations — the exact false-positive mode
`[#501]`'s row already names (*"shallow grafts read as whole-file creations — 5 false
`canonical_freshness` FAILs"*, `tasks/501-*.md`). Every cell that would need such a verdict
is marked **UNVERIFIABLE-FROM-CLOUD**, not guessed.

**2 — No gate set exists in this checkout.** `.git/hooks/` contains no installed hooks and
`pre-commit` is not on `PATH`. This commit therefore lands **without** the pre-commit,
commit-msg or pre-push organs. **This is not a bypass this lane chose** — no `SKIP=` and no
`--no-verify` were used, because there was nothing to skip. Declared here rather than left
implicit, per the standing "an undeclared bypass is the thing this repo's doctrine refuses"
practice (`docs/audits/2026-08-09-technical-challenge-retrieval.md:17`).

**3 — Lane rule honoured: no JOURNAL entry.** A lane never journals; the integrator does
(census packet, `docs/audits/2026-08-10-technical-backlog-testability-census.md:890`;
batch4-prep packet, `…-batch-4-prep-evidence.md:997`). The session-end backpressure hook is
**declined for that recorded reason**. It is advisory in full since the ADR-85 amendment
2026-08-03 §A5 (`CLAUDE.md` §9), so declining it blocks nothing and hides nothing.

**4 — Writes.** This report, plus the regenerated `docs/audits/README.md` index line. That
second write is deliberate: a lane that adds an audit and does not regenerate leaves the
index stale, which is the failure witnessed twice this window (JOURNAL `2026-08-10 (h)` and
`(i)`). **Reproduced a third time here, mechanically:** `gen_audit_index.py --check` exited
**0** on the base tree, **1** once this report was added, and **0** again after `--write` —
so the trailing regen is mandatory whether or not anything conflicts, and in this checkout
no gate would have caught its absence (condition 2). Zero births, zero row / intake / ADR
edits, zero deletions, zero merges.

---

## 0 · PARTIAL protocol — what was expected, what is actually on main

The contract named six things expected on `main` and instructed PARTIAL handling for any
absentee. **Four present, one present-as-a-fix-not-a-report, two ABSENT.**

| Expected | State | Locator |
|---|---|---|
| `STANDING_RULINGS` §I | **PRESENT** | `protocols/STANDING_RULINGS.md:707` — *"I. ARC-9 — the 2026-08-10 ruling window (seat-27 checklist)"*; landed `57284aa`, extended by I-D2 at `e59c5c5` |
| ADR-111 **Accepted** | **PRESENT** | `docs/decisions/ADR-111-finding-triage-pipeline.md:3` — status line reads Accepted, with a `Decided-by` line under the ADR-94 status-line-only exception; set at `57284aa` |
| ARC-8 merge | **PRESENT** | `12ef9c9` (lane merge `ef71ed0`, report `b8f4004`) |
| ARC-9 merges | **PRESENT ×4** | `710dabf` (rulings) · `fcfc553` (lane 1) · `7d1d332` (lane 2) · `5455c2a` (lane 3) |
| Lane report — **arch-claims-fix, 16 claims** | **PRESENT, but it is a FIX, not a report** | `cf03975` edits `ARCHITECTURE.md` (+106/−48); there is no `docs/audits/*arch-claims*` file. The narrative record is JOURNAL `2026-08-10 (g)` and the register line I-D2 (`protocols/STANDING_RULINGS.md:846`) |
| Lane report — **batch4-prep evidence** | **PRESENT** | `docs/audits/2026-08-10-technical-batch-4-prep-evidence.md` (997 lines), `8e63eab` |
| Lane report — **backlog-testability-census** | **PRESENT** | `docs/audits/2026-08-10-technical-backlog-testability-census.md` (891 lines), `08c880f` |
| Lane report — **digest-content census** | **ABSENT** | see §0.1 — and it is cited twice in the JOURNAL as if present |
| Lane report — **research-corpus distillate + reconcile** | **ABSENT** | no file; the queue puts it last (`JOURNAL.md:153`) |

**Sections that inherit PARTIAL status: §2 rows 4–5, and challenge axes X-2 and X-8's
second leg.** Everything else stands on landed artifacts.

### 0.1 · The "digest census" is cited twice for an artifact reachable from no ref

This is the sharpest thing this lane found, so it is stated before the synthesis rather
than buried in it.

JOURNAL `2026-08-10 (i)` says *"That is the digest census's §7.2(3) point, confirmed from
both sides"* (`JOURNAL.md:33`), and JOURNAL `2026-08-10 (h)` says *"That is the digest
census's §7.2(3) prediction landing live"* (`JOURNAL.md:98`). Both entries are on `main`'s
first-parent spine (`4cb1092`, `f3bb49b`).

**Reproduced negatively, three ways:**

1. No `docs/audits/*digest*` file matches — the 19 hits are `conformance-nightly-digest`
   dailies plus `2026-08-03-technical-night-batch-digest.md` and
   `2026-08-10-verification-ruled-dispositions-and-digest-gap.md`, none of which carries a
   §7.2.
2. `git log --all --diff-filter=A -- 'docs/audits/*digest*'` across **every ref in this
   clone** adds no such census.
3. The only `## 7.2`-shaped heading in the whole corpus is
   `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md:420` — *"The
   hash-guard is load-bearing"* — a different subject entirely.

**Honest limit:** the clone is shallow (condition 1), so the strongest claim available is
*not reachable from any ref in this clone*. The artifact may live off-repo in the
operator's prompts directory, or may never have been written.

**Why it matters, and why it is not a nit.** The cited §7.2(3) point is load-bearing: it is
the *explanation* both integrator entries give for the gate asymmetry they witnessed, and
it was reused as a prediction. This is the `[#503]` mechanism arriving from the citation
side — the reference is stale not from a bad edit but because its referent never became a
repo artifact — and it is the same class as `[#505]` clause 1. **Reported, not ruled**; no
row is proposed, per this lane's read-only scope.

---

## 1 · What landed — the window 2026-08-10/11, one SHA per claim

Six integration arcs on the first-parent spine, all dated 2026-08-10. **No commit on `main`
carries a 2026-08-11 date at base** — the window's second half is still ahead.

| # | Claim | SHA | Where it is checkable |
|---|---|---|---|
| 1 | ARC-4 — the 20th `undeclared_edges` disposition; four kill candidates ruled, **zero closed, zero born**; the ARC-4 bundle cut | `e67fb8d` (merge) · `201191f` · `01410f9` · `9a7ffcb` · `bbc008c` | `ecosystem/disposition-register.yaml`; JOURNAL `2026-08-10 (a)` |
| 2 | ARC-5 — the night cloud batch archived; manifest authored *before* integrating; four ruled dispositions verified 4/4; the conformance-digest gap named as a **BROKEN step** | `1a76cf6` (merge) · `737dd47` · `19aca46` · `189fcb3` · `fd46496` · `8607806` | `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`; RESIDUAL §4(i) |
| 3 | ARC-6 — two evidence findings attached to `[#419]`/`[#310]`; one unowned defect **named rather than birthed** | `f91a433` (merge) · `a8c6295` | JOURNAL `2026-08-10 (c)` |
| 4 | ARC-7 — the boot instruction cites the live active-bundle predicate instead of *"most recent"* | `a967d27` (merge) · `0f3bce6` | `CLAUDE.md` §1 item 3 + §12 v2.55; carrier `templates/claude-regions/first-read.md` |
| 5 | ARC-8 — Fable adversarial review of plan v2 integrated: **0 Critical / 3 High / 6 Medium / 6 Low** | `12ef9c9` (merge) · `ef71ed0` · `b8f4004` | `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:271` |
| 6 | ARC-9 — the seat-27 ruling checklist recorded as `STANDING_RULINGS` **§I**; the corrected 25-row N-B table emitted; the seed corpus measured | `710dabf` (merge) · `57284aa` | `protocols/STANDING_RULINGS.md:707-875` |
| 7 | **ADR-111 Proposed → Accepted, as written**, §4 departure intact (Fork 1 = Option A) | `57284aa` | `docs/decisions/ADR-111-finding-triage-pipeline.md:3`; register I-F1 at `:797` |
| 8 | `[#511]` re-scoped to the **non-mechanized** cut load; intake #28 §B **decided and banked, not executed** | `57284aa` | register I-F2 at `:810` |
| 9 | Digest strategy ruled reading (b): **absorb ×7 AUTHORIZED as one batch**; retention self-resolves; the absorb step becomes an organ by amending `[#419]`/`[#426]` | `710dabf` (the authorization locator *is* this merge SHA) | register I-F3 at `:826` |
| 10 | `automation/*` joins `claude/conformance-*` on the branch-deletion protection list | `57284aa` | `.claude/rules/git-discipline.md`; register I-D 3c-3 |
| 11 | ARC-9 lane 1 — **16** checkably-false `ARCHITECTURE.md` claims corrected (Fable's 14 superseded as a *floor*) | `fcfc553` (merge) · `316d4ca` · `cf03975` · `e59c5c5` (I-D2 rider) | `protocols/STANDING_RULINGS.md:846`; JOURNAL `2026-08-10 (g)`, anchor `8773f63` |
| 12 | ARC-9 lane 2 — batch-4 prep: 6 evidence sheets, a 6×6 disjointness matrix, 6 contract skeletons, 4 paste-blocks | `7d1d332` (merge) · `9dcdc2a` · `8e63eab` · `4cab864` (index regen) | `docs/audits/2026-08-10-technical-batch-4-prep-evidence.md`; JOURNAL `(h)`, anchor `f3bb49b` |
| 13 | ARC-9 lane 3 — **all 170 open Done-when clauses graded**, 42 conversions drafted | `5455c2a` (merge) · `fbac3f0` · `08c880f` | `docs/audits/2026-08-10-technical-backlog-testability-census.md`; JOURNAL `(i)`, anchor `4cb1092` |

### 1.1 · The two numbers this window actually changed

**The testability claim was cut by 42%.** The carried figure *"78% of the open set cannot be
mechanically tested"* survives **as a measurement** (N-A's path-citation proxy reproduces:
130 today against 132 then, a 2-row parse-boundary delta) but fails **as a testability
claim** — because **55 of those 130 are MECHANICAL anyway**. Honest replacements: **95
(55.9%)** not-testable-as-written, **23 (13.5%)** neither testable nor convertible. Grading
of all 170: MECHANICAL 75 (44.1%) · PROSE-CONVERTIBLE 72 (42.4%) · PROSE-JUDGMENT 15 (8.8%)
· DEFECTIVE 8 (4.7%). Locator: census §1, `08c880f`.

**The ARCHITECTURE defect count was superseded upward, 14 → 16.** Not a correction of
Fable's work but a correction of its *type*: a count taken under an enumeration cap is a
floor, not a total (I-D2, `protocols/STANDING_RULINGS.md:846`). The durable half is the
anti-rot method — a volatile cardinality is **re-pointed at the surface that computes it**
rather than restated, which is how ≥3 of those claims went false *under their own review
stamp* at `8f09c12d`.

### 1.2 · Live re-derivations (this lane, on base `5455c2a`)

Counted directly from `tasks/*.md` frontmatter, never from the generated `BACKLOG.md`:

- **open 170 · deferred 26 · closed 55 · superseded 1 · retired 1 — 254 task files.**
  170 + 26 = **196 rendered**, matching `STANDING_RULINGS` H2's named-filter rule and
  Fable's *"BACKLOG reconciliation exact (196=196=196)"* calibration line.
- **`kill-candidates:` = 117 of 170 open. `footprint:` = 5 of 170 open.** Both reproduce
  the census's figures exactly. The census's own reading of that gap stands: one field has
  a commit-msg hook behind it and the other has nothing, so **the gap is a mechanism gap,
  not a discipline gap** (census §8 q7).
- **Seven `claude/conformance-*` branches exist and exactly seven** —
  `2026-08-{03,04,05,07,08,09,10}` — matching I-F3's enumeration character-for-character.
  Each is a single-file add against `main` (the 08-10 tip `40ae0e7` adds 205 lines). See
  §2.2: this exactness is the pending item's live risk, not its reassurance.

### 1.3 · The gate asymmetry, now witnessed from both sides in one session

Worth carrying above the arcs because it is a property of the machine, not of a lane. A
**conflict-free** merge runs only `commit-msg` hooks, so `pre-commit` never fires and a
generated file rots silently; a **conflicting** merge runs the full set. Same file, same
kind of change, opposite gate coverage — decided purely by whether git had to ask.
Lane 2 hit the first case (`docs/audits/README.md` auto-merged clean, `--check` still exited
1, trailing regen `4cab864` mandatory); lane 3 hit the second (conflict → full set → resolved
**by regeneration, never a hand-merge**). Locators: JOURNAL `(h)` `JOURNAL.md:96-99`,
JOURNAL `(i)` `JOURNAL.md:29-33`. The explanatory citation both entries give is the missing
artifact of §0.1.

### 1.4 · Suite state across the window — flat, and the RED is owned

**1 failed / 2715 passed / 4 skipped / 1 xfailed** on all three ARC-9 lane merges (20m48s ·
14m24s · 15m51s). The single RED is
`test_routine_consumers_live_backlog_governs_exactly_one_row` — the standing `[#426]` row,
**proven pre-existing** by re-running it on bare `main` `12ef9c9` where it fails identically.
Not dispositioned, not this window's. Noted in JOURNAL `(g)`: only one of the two expected
standing REDs appeared — `[#348]` did not fire. **Not re-run by this lane** (read-only, and
a cloud clone is not the measurement surface for a 15-minute suite).

---

## 2 · What is pending — each with the gate that holds it

### 2.1 · The queue, in the order the integrator recorded it

`JOURNAL.md:153` states the remaining order verbatim: **digest-absorb-prep → the authorized
absorb ×7 (route A) → ingest-research-corpus last.**

| Pending | Gate | State at base |
|---|---|---|
| **digest-absorb-prep** lane — owes the `[#419]`/`[#426]` absorb-organ amendment DRAFT | No mechanical gate; it is next in queue. Its input is already recorded: a **scheduler-run check** belongs inside the amendment's scope | **Not on disk.** I-I2 said so at recording time (`protocols/STANDING_RULINGS.md:863`) and this lane confirms it still is — no `docs/audits/*absorb*` exists |
| **absorb ×7** — merge the seven conformance digests serially, each branch deleting at its own merge | **Authorized**, locator = merge `710dabf` (I-F3 item 1). Not a fresh operator act | 7 branches live, unmerged. **See 2.2 — the authorization has an arithmetic expiry** |
| **ingest-research-corpus** — last in queue; carries the ingest distillate table | The GO / queue order | Absent. Fable: the **seeded-defect corpus spec** *"exists nowhere in-repo"* and is *"the single highest-value un-landed artifact"* — it gates `[#491]`, `[#492]` and the Copilot channel (`…fable-adversarial-plan-review.md:210`, feedback item 4) |

### 2.2 · The absorb-×7 authorization expires by arithmetic, and probably tonight

I-F3 item 1 is explicit: *"An eighth digest appearing before execution falls outside the
authorization, which covers seven"* (`protocols/STANDING_RULINGS.md:833`).

At base there are **exactly seven** conformance branches. The producer is healthy and
nightly — Fable's calibration line records *"conformance digest producer healthy, ×7
current"*, and the 08-10 digest landed on its own branch at `40ae0e7`. **The window this
report covers is 2026-08-10/11.** If the Routine fires for 2026-08-11 before the absorb
runs, an eighth branch exists and the authorization no longer covers the set.

**Two consequences worth stating plainly, neither of them a ruling:**

1. The cheapest disposition is to **execute the absorb before the next nightly fire**, which
   makes the arithmetic moot.
2. If it fires first, the seat needs one sentence — not a re-litigation — either extending
   the authorization to the new count or scoping the batch to the enumerated seven and
   leaving the eighth to the next window. **Which of those is the operator's call.** This
   lane reports the countdown; it does not pick.

Related and already established: the digest gap is a **recurrence at identical width** of
open `[#419]` (first instance `claude/conformance-2026-07-21`…`-26`, also six), and the
protection those branches carry is against **deletion**, not merging
(`docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`; RESIDUAL §4(i)).

### 2.3 · Adjudication debt — 13 of 15 discharged, 2 still open by design

The decision sheet's fifteen §7 items (`docs/audits/2026-08-09-technical-decision-sheet.md:13`)
map onto §I one-for-one. **Thirteen are ruled and recorded. Two are deliberately not:**

| Sheet item | Outcome | Locator |
|---|---|---|
| 1 `[#492]` Grok 4.6 · 2 the four kills · 3 OneDrive · 6 intakes #30/#31 · 7 N2 R6 · 8 the `2h43m`/`~9min` figures · 9 pre-commit rewriters · 10 the closure store · 11 the two engine amendments · 12 `ARCHITECTURE.md` · 13 `[#322]` | **RULED** — the DEFAULT BLOCK, one line each | `STANDING_RULINGS` I-D, `:737-795` |
| 4 ADR-111 ratification | **RULED** — Option A, as written | I-F1, `:797` |
| 5 `[#511]` | **RULED** — re-scoped to the non-mechanized load | I-F2, `:810` |
| **14 → §4A** (`[#502]`'s Done-when / where the Shape-B residual is owned) | **DEFERRED into FORK 4's pool, which §I does not open** | I-D, `:783` |
| **15 intake #28 §B** | **DECIDED and banked, NOT executed** — the `status:`/`decided-by` flip lands only as one atomic act at the batch-4 GO | I-F2, `:816-820` |

**FORK 4 — the births package — is unopened and named as such** in §I's own scope note
(`protocols/STANDING_RULINGS.md:717`), alongside two other deliberate gaps: the `[#241]` and
`[#390]` row texts (owed to batch4-prep's paste-blocks) and every intake `status:` field.

### 2.4 · Owed to the batch-4 GO — the operator's input queue, assembled

Nothing below is blocked on machinery. All of it is blocked on one act.

- **The ratification batch, as one atomic flip:** intake #28 §A **and** §B, #29, #30, #31,
  #32, plus the triage distillate (`JOURNAL.md:843`; `STANDING_RULINGS:820`).
  **Fable High M4-1: #32 and #28 §A are silently off the ratification surface** as plan v2
  is written, so criterion (2) would close with two silent drops — *"the exact thing it
  forbids"* (`…fable-adversarial-plan-review.md`, feedback item 1).
- **Batch4-prep's five batched questions** (`…batch-4-prep-evidence.md:979-993`): has the
  `mutation-pilot` job run since `27c37ae3`? · does any batch-4 lane own `ARCHITECTURE.md`?
  · which batch discharges `[#514]` leg 3? · does 3b-3 earn a birth? · `[#310]` is
  `deferred` and needs an un-defer first.
- **The census's seven batched questions** (`…backlog-testability-census.md:854-882`). Two
  carry unusual leverage: *"where does a 'recorded with a reason' record live?"* —
  **one decision converts 30 rows** — and whether a hollow existence check is acceptable for
  the §B amendment, which the census names as *"the amendment's central question and this
  census cannot answer it"*.
- **Fable's six deltas**, three of them High, including *"route BOTH halves"* of commission 5
  (the session-continuity half of memo `wf-fafd931b` has no destination and zero in-repo
  trace) and *"consume N-A"* — the satisfied-row census exists to let the seat adjudicate
  closes from evidence, and **no phase references it**.

### 2.5 · Two findings from lane 3 that touch already-recorded rulings

Surfaced by the census, **not reversed by it** — both are the operator's to revisit.

1. **`[#360]`'s "intent unrecoverable" is REFUTED.** The census located the referent: the
   `## Scope-freeze` section of `DEFINITION_OF_DONE.md`, a 4-week ADR-85 freeze that expired
   ~2026-07-14 and still stands verbatim — which is exactly *"expired in place"*, and fits
   the row's Done-when and nothing else in the file. **Operator input I-1
   (`STANDING_RULINGS:840`) and the dated review recorded at `710dabf` rest on a premise
   this lane disproves.**
2. **`[#505]` clause 2 is UNMEETABLE, and that half is uncovered.** *"batch-1 executes under
   it"* is past tense and batch-1 ran 2026-08-06, so no future act satisfies it. Ruling 3a-5
   covers clause 1 only.

Also reproduced live by that lane: `[#470]` is not hypothetical — `audit.py checks` crashed
in-lane with `UnicodeEncodeError` on `→`, the exact defect the row describes.

### 2.6 · Structural limit on tonight's execution surface

Batch4-prep's packet states it directly: consumer-repo work is a real **17+-row cohort** and
the census's **highest-yield untested cohort** — *"and it cannot be run from a cloud lane"*
(`…batch-4-prep-evidence.md:977`). The highest-value remaining cohort is unreachable from
where the work is currently happening. Reported as a scheduling input, not a complaint.

---

# 3 · DRAFT for the browser seat; colors are proposals, the seat rules

**This section is a pre-fill, not an answer.** Every color below is a *proposal* from a
read-only cloud lane on one pinned tree. The seat rules; nothing here binds.

### How to read it

- **The instrument is off-repo.** `CHALLENGE-ANSWER-2026-08-09.md` lives with the browser
  seat, not in this repo. The X-1..X-8 *axes* below are reconstructed from the one in-repo
  artifact that serves it — `docs/audits/2026-08-09-technical-challenge-retrieval.md`, whose
  `Serves:` line (`:6-7`) enumerates the deferred cells and whose §1–§6 map onto X-1..X-6 in
  order. **Where reconstruction fails, the axis is marked OWED rather than invented.**
- **Legend:** 🟢 healthy / verified this window · 🟡 sound with a named, bounded defect ·
  🟠 unresolved, deferred, or unverifiable from here · 🔴 failing, with evidence.
- **Every cell carries a locator or the word OWED.** No cell is filled from recall.

### The table

| Axis | Subject (reconstructed) | Proposed | Evidence this window — locator | What the seat must supply |
|---|---|---|---|---|
| **X-1** | Organ inventory & bypass — are the commands / hooks / skills actually used, or replaced by hand-written instruction? | 🟡 | Zero `SKIP=`, zero `--no-verify` across all three ARC-9 lanes (JOURNAL `(g)`/`(h)`/`(i)`). **But** the merge-path gate asymmetry is now witnessed from both sides in one session — a conflict-free merge skips `pre-commit` entirely (`JOURNAL.md:96-99` and `:25-33`). And this cloud lane has **no hooks armed at all** (§ conditions 2) | Whether the asymmetry earns a mechanism or a recorded acceptance. Retrieval's §1.4 *"one hand-written instruction that replaced a command that existed"* has **no measured successor this window** — OWED |
| **X-2** | The `[#408]` / distiller family, and pointer staleness (PLAYBOOK "dynamic-workflow shape" as §16) | 🟠 | **No delta located this window.** Standing state only: `[#408]` is doc-coupling-on-closure, *not* a distiller — the outgoing seat's own correction, `RESIDUAL.md:215`. Retrieval §2.3 (`:281`) recorded the pointer stale with content elsewhere | **PARTIAL** — the digest-content census that would have re-measured this is ABSENT (§0.1). Current staleness of the §16 pointer: **OWED** |
| **X-3** | The measurement ledger + intake #27 §A rows — are the numbers sourced and scheduled? | 🟡 | Three ledger repairs landed: the `2h43m`/`~9min` figures **STRICKEN as unsourced** (I-D 8, `:754`); sheet items 3 and 5 **re-graded VERIFIED** on located evidence (I-P1, `:727`); `[#511]` re-scoped to shape, not seconds (I-F2) | The **20m48s vs 15m03s** arithmetic is still unreconciled and I-F2 deliberately rules around it rather than through it (`RESIDUAL.md:120-122`). Whether that residue is accepted or closed: **OWED** |
| **X-4** | Registered specs (`_SPEC_REGISTRY`) + the intake-#25 W-9a hazard text | 🟡 | The registry gained its **second** spec — `templates/prompt-template.md` at `fc0b1f0` — closing retrieval §4.3's single-entry finding (`:569`). Cost: intake #30 §E mints a prose edge no rephrasing clears, dispositioned on the merits under `#241` (`RESIDUAL.md:32-37`) | The disposition class is now the smell: *"17 WARNs of one class is itself the smell"* (`RESIDUAL.md:214`), with the 20th landed at `201191f`. Whether the class earns a rule: **OWED** — RESIDUAL §4 already flags *"the rule that is missing"* |
| **X-5** | Root / folder governance — does a tool mandate each root file's location? | 🟢 | `validate_hermetization` Rule A/B live and prospective-only (`CLAUDE.md` §9); this lane's own filename pre-verified through `classify()`. One naming-convention **claim** corrected in the 16: `logs/parity-events.jsonl` written lowercase against the `[#395]` UPPERCASE convention (JOURNAL `(g)`) | Retrieval §5.3 (`:687`) recorded what the Folder Governance clause **does not** cover, and §5.4 the single-file folders. **No coverage extension this window — OWED.** Note the green is on the *gate*, not on completeness |
| **X-6** | Consumer-repo / win-tooling conformance — pre-commit config, armed hooks, stages | 🟠 | Retrieval measured **ABSENT config, NONE armed, no stages** (`:768`, `:779`, `:797`). Batch4-prep sizes the cohort at **17+ open rows**, the census's highest-yield untested cohort, and states it **cannot be run from a cloud lane** (`…batch-4-prep-evidence.md:977`) | Nothing moved it this window and the current execution surface structurally cannot. Whether batch 4 takes a local lane for it: **OWED** |
| **X-7** | **OWED — axis subject not recoverable in-repo** | 🟠 | The retrieval report's `Serves:` line enumerates deferred cells at X-1, X-2, X-3, X-4, X-5 and X-6, and X-8 appears at `:57`. **X-7 appears nowhere in the corpus.** Searched: all `X-[1-9]` occurrences repo-wide (2 files, both listed above) | The seat holds the instrument. Supply X-7's subject; this lane will not invent one |
| **X-8** | Contract & execution discipline — does a contract become a **committed repo artifact** before it is executed? | 🔴 | **Falsified a fourth time this window, by the census lane's own contract** — it arrived as a file in `~/Downloads`, not a committed artifact (`JOURNAL.md:53-58`). Prior instances: retrieval `:57` (X-8.2, `[#505]` leg 1) and the two 3a-5 cites. Ruling **3a-5** already answered it — *"the mechanism is being dodged, not wrong; batch-4 lanes dispatch from COMMITTED contract files"* (`STANDING_RULINGS:781`) | Two aggravators to weigh: **(a)** this lane's own contract also arrived as a prompt, not a committed file — arguably n=5; **(b)** §0.1's dangling `digest census §7.2(3)` citation is the same failure one layer up, in the JOURNAL. Whether 3a-5 needs teeth rather than a restatement: **OWED** |

### BOTTOM LINE

```
DRAFT — colors are proposals; the browser seat rules.
Base: origin/main 5455c2a2a008e0ce8cc1d8ac77d2835cfd767376 (shallow clone; no gates armed).

1. The landed half is real and clean. Six arcs, three lanes, zero SKIP=, zero
   --no-verify, zero births, zero closes. Suite flat at 1F/2715P/4S/1xf with the
   one RED proven pre-existing on bare main 12ef9c9. Governance landed as
   specified: STANDING_RULINGS section I, ADR-111 Accepted as written.

2. Adjudication is 13 of 15 discharged. The two that are not — sheet item 14 and
   intake #28 SS-B — are open BY DESIGN, both parked on FORK 4 / the batch-4 GO.
   That is one operator act, not a queue.

3. Two of the five expected lane reports are ABSENT: digest-content census and
   research-corpus distillate. The second is the more expensive: it carries the
   seeded-defect corpus spec, which Fable calls the single highest-value
   un-landed artifact, and which gates #491, #492 and the Copilot channel.

4. ONE PENDING ITEM HAS A CLOCK, AND IT IS TONIGHT. The absorb-x7 authorization
   (I-F3, locator = merge 710dabf) covers exactly seven digests. Exactly seven
   exist. The nightly producer is healthy. An eighth on 2026-08-11 falls outside
   the authorization by its own words. Cheapest disposition: absorb before the
   next fire. Otherwise the seat owes one sentence — extend, or scope to the
   enumerated seven. Not this lane's call.

5. THE ONE RED IS X-8, and it is not new — it is n=4 recorded, arguably n=5
   tonight. Contracts still are not repo artifacts. Ruling 3a-5 already named
   it correctly and the behaviour did not change, which makes the open question
   teeth-versus-restatement. New evidence this lane found: the JOURNAL cites
   "the digest census's section 7.2(3)" twice, at :33 and :98, for an artifact
   reachable from NO ref in this clone. Same failure, one layer up, inside the
   spine record itself. Reported, not ruled, no row proposed.

6. Two recorded rulings now rest on premises a later lane disproved: #360's
   "intent unrecoverable" (census located the referent) and #505 clause 2
   (unmeetable, past tense, uncovered by 3a-5). Surfaced for the operator to
   revisit; neither reversed here.

7. UNVERIFIABLE-FROM-CLOUD, stated not guessed: every canonical_freshness-class
   verdict (shallow graft = known false-positive source), the live suite, and
   any gate outcome — this checkout has no hooks armed and no pre-commit binary.
```

---

## Contract compliance

Read-only honoured. **Zero births · zero row / intake / ADR edits · zero status changes ·
zero deletions · zero merges · no `SKIP=` · no `--no-verify` · no force-push.** No JOURNAL
entry — lane rule; the Stop hook is declined for that recorded reason (§ conditions 3).
Writes: this report and the regenerated `docs/audits/README.md` index line. No verdict of the
`canonical_freshness` class is asserted anywhere above; every cell that would need one is
marked UNVERIFIABLE-FROM-CLOUD.

---

## Amendment — 2026-08-10 (the Stop hook did not decline; it could not execute)

**Everything above is left BYTE-UNCHANGED.** Appended under the CLAUDE.md §5 item 3 in-file
amendment marker, which is the sanctioned mechanism for an immutable audit; the precedent is
`docs/audits/2026-08-03-technical-night-ld-472-option-b.md:153`. Recorded here rather than
left in session chat, because *"an observation that never became a repo artifact is lost"* is
this report's own §0.1 headline and it would be incoherent to exempt itself from it.

**What happened.** At this lane's session boundary the Stop hook fired and **failed to run**:

```
[uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"]:
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

**It is a REPRODUCTION, not a discovery — stated first so it is not inherited as new.** JOURNAL
`2026-08-09 (c)` already records the identical mechanism, measured one night earlier across all
five night lanes: *"Every lane ran in a container where **no hook could execute** — `uv` 0.8.17
against the ADR-106 `==0.11.19` pin makes every `uv run --locked` entry refuse before doing any
work, and `.git/hooks/` held only samples"* (`JOURNAL.md:1114-1117`). What is new is only the
**layer**: that entry measured it at the pre-commit layer; this is the same pin refusing at the
`Stop`-hook layer.

**It refines condition 2 above, which is incomplete rather than wrong.** Condition 2 gave two
reasons no gate ran here — no installed hooks, no `pre-commit` on `PATH`. The pin is a **third
and strictly stronger** reason: it would still bite if both were fixed. Measured on this tree:
`pyproject.toml:25` pins `required-version = "==0.11.19"`, the live binary is `uv 0.8.17`, and
**16 of 16** `entry:` lines in `.pre-commit-config.yaml` invoke `uv run --locked` — so the
refusal is total, not partial. Condition 2's operative claim (this commit landed ungated) is
unchanged.

**It also makes condition 3's wording exact.** That condition says the Stop hook *"is declined
for that recorded reason"*. Both things are true — the lane rule declines it **and** it could
not have executed — but "declined" alone implies it was available to decline. It was not. The
JOURNAL-anchor obligation it would have asserted is discharged the same way regardless: a lane
never journals; the integrator does.

**One line of doctrine, witnessed rather than asserted.** ADR-85's 2026-08-03 amendment §A5
made this hook's outer error **loud rather than a silent `return 0`** (`CLAUDE.md` §9). The
failure surfaced loudly, at the boundary, with its cause named. That is the amendment behaving
exactly as designed — the first in-the-wild instance this report can attest to.

**Input for the integrator, not a ruling and not a row.** The established remedy is the one the
2026-08-09 (c) arc already used: **re-run the gates locally on the merged tree**, because a
cloud lane cannot be the gate for its own artifact. That applies to this report as much as to
the five it was written about. Nothing here is proposed as a birth; `[#419]`/`[#426]` and the
`[#501]` recorder row are the existing territory for anyone who later decides it needs one.
