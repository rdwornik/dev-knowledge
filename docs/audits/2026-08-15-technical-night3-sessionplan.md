# Night-3 session plan — PROPOSAL for the architect (phase 2)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** `night3-sessionplan`
- **Status:** **DRAFT — PROPOSAL ONLY.** Nothing here is a ruling. No BACKLOG row, `tasks/` body,
  register entry, ADR or manifest was touched to produce it. The booted morning seat rules.
- **Lane:** `dk · night3-E · sessionplan`, read-only, branch `claude/night3-session-plan-proposal-ma3t2c`.
- **Base read:** `HEAD` = `65dc318` (post-phase-1: boot-acts `d62796ad` → 7 lane merges →
  integration wrap `6a80f98` → night-2 UNIQUE-HOLD landing `65dc318`).
- **Instrument:** commit timestamps on this branch, `tasks/manifest.json`, the landed census +
  drafts artifacts, and one `audit.py health` run. Every number below is measured here unless
  marked INHERITED or UNVERIFIABLE.

---

## §0 · The answer first

```
GO-READY:  NO as of this reading -- 6 of 8 phase-2 premises GO, 2 NO-GO.
           Both NO-GOs are clearable inside the adjudication hour; neither needs new work.

BLOCKING   P7  origin/main is 59 commits BEHIND this branch. Phase-1 is NOT on origin/main.
           P6  Forks D6.5 and D6.6 have no in-repo resolution -- 4 of 29 ids, 3 of 7 lanes.

ESTIMATE   ~5h15m  adjudication(1h00) + dispatch(0h15) + lanes(1h00) + queue(1h30) + close(1h30)
           ~6h45m  if phase-1's 1h29m idle prologue repeats

LEVER      The integrator's serial tail was 70% of phase-1's wall clock (3h56m of 5h36m).
           The suite was 7%. Boot the integrator on a clock, not on lane completion.

WAVE       29 ids (not 30) -- #364 retired. Lanes 4+3+4+5+4+4+5. All 29 PROSE-CONVERTIBLE.
```

---

## §1 · Premise validation against the live tree

### 1.1 · The 29 ids — **CONFIRMED, and the count is 29, not 30**

The plan of record (`…-night2-consolidated-briefing.md` §3.1/§4) specifies **7 lanes, 30 ids**.
Re-derived here against `tasks/manifest.json` and each `tasks/<id>-*.md` frontmatter:

| lane | ids | n | all `status: open`? |
|---|---|---|---|
| W2-a | `#409 #410 #411 #419` | 4 | yes |
| **W2-b** | `#210 #285 #361` ~~`#364`~~ | **3** | yes |
| W2-c | `#146 #266 #438 #443` | 4 | yes |
| W2-d | `#351 #385 #393 #484 #502` | 5 | yes |
| W2-e | `#82 #145 #239 #263` | 4 | yes |
| W2-f | `#130 #274 #350 #417` | 4 | yes |
| W2-g | `#271 #324 #391 #412 #491` | 5 | yes |
| | | **29** | **29/29 open, 0 deferred** |

**`#364` is `status: retired`** and is absent from `tasks/manifest.json` (195 live nodes; the other
29 all resolve). It was obsoleted at `e9482bf` by the morning adjudication D4.9(a)/D6.2 — the
`_BACKLOG_GROSS_CHARS` 1200 → 1320 recalibration discharged its premise. Its own body already
records the consequence: *"`[#364]` is REMOVED from conversion lane W2-b, which becomes 3 ids."*
**Consistent, and the plan's `4+4+4+5+4+4+5 = 30` line is the stale one.**

**Class premise (`[NB2-E]` A7) — CONFIRMED.** All 29 are graded `PROSE-CONVERTIBLE` in
`docs/audits/2026-08-10-technical-backlog-testability-census.md`; none is `PROSE-JUDGMENT` or
`DEFECTIVE`, so none falls into the judgment carve-out. Two carry qualifiers that survive into the
lane: `#393` is `PROSE-CONVERTIBLE (off-repo)` (verdicts land in corp-sca), and `#502` is the only
one of the 29 with `footprint: Y`.

**Drafts are landed and consumable.** `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md`
is on this branch (lane S, `6c4743cd` byte-faithful + `6516f6e2` the four ruled fork edits). The
wave no longer depends on an unmerged branch — which was the whole point of running W2-0 first.

### 1.2 · File-disjointness re-derived post-phase-1 — **PARTITION HOLDS; COLLISION PROFILE WORSENS**

Phase-1 moved 22 `tasks/` files. Intersection with the wave's 29:

```
phase-1 tasks/ churn (main 7bbb067 .. HEAD):
  R's drain-8        344 415 423 428 430 487
  integration wrap   293 528 529 530
  boot-acts          278 322 352 364 387 426 494 505 510 511 522 524
  -----------------------------------------------------------------
  intersection with the 29-id wave:  {} -- EMPTY
  intersection with the original 30: {364}, and #364 is now retired
```

**The seven-way `tasks/` partition survives phase-1 intact.** Every id's file is still touched by
exactly one lane, and no lane's file was moved, renamed or re-slugged.

**But the merge-queue cost premise does not survive.** Phase-1 measured *"every merge conflicted on
`docs/audits/README.md` and only there"*. Re-derived per lane (`merge-base..lane-tip`, so lane-own
footprint, not inherited delta):

| lane | `BACKLOG.md` | `tasks/*` | `docs/audits/README.md` | files |
|---|---|---|---|---|
| S · w20-draft-landing | — | 0 | ✔ | 3 |
| Q · 293-satellite | — | 0 | ✔ | 3 |
| **R · gateclose-drain8** | **✔** | **7** | ✔ | 10 |
| N · 528-legs12 | — | 0 | ✔ | 7 |
| M · 529-telemetry | — | 0 | ✔ | 5 |
| P · 530-single-flight | — | 0 | ✔ | 5 |
| O · 527-block-main | — | 0 | ✔ | 7 |

**1 of 7 phase-1 lanes touched the BACKLOG generated set. In phase 2 it is 7 of 7** — every
conversion lane rewrites a `tasks/<id>-*.md` body, and every such edit regenerates **`BACKLOG.md`**
and **`tasks/manifest.json`** alongside the audit index. So the queue goes from **one** generated
conflict surface per merge to **three**, and two of the three are an order of magnitude larger and
structurally denser than the audit index.

This does not threaten correctness — the resolution is already ruled (*"regenerate BACKLOG/manifest/
audit-index at merge, never hand-merge"*) and `task_tree_coherence` is the check that catches a bad
one. It is a **cost** finding, and it is the single largest input to the phase-2 queue estimate in §2.

### 1.3 · The `#371`-before-`#387` bar — **STANDS, and it binds the adjudication hour, not the dispatch**

Both rows are live and `status: open` in `tasks/manifest.json`:

- `#371` — *Consumer editor-config write-through* (P2/S, `[E8]`) — *"Vehicle decided by the
  buy-vs-build fleet-template ADR … do NOT implement bespoke."*
- `#387` — *Rewrite the buy-vs-build intake BEFORE anything ingests it* (P2/S, `[E7]`) — exists
  because that very intake *"argued FOR the template engine that was subsequently rejected."*

The census's finding is therefore intact: **ruling `#371` before `#387` lands would ratify against a
document the fleet has already refuted.** Neither id is in the wave, so this constrains **what the
adjudication hour may rule**, not what may be dispatched. Proposed disposition: leave `#371`
un-ruled tomorrow and say so explicitly, so the bar is honoured by record rather than by omission.

### 1.4 · W5 cap arithmetic at width 7 — **WITHIN CAP, with one slot free and one trap**

PLAYBOOK Ch8 caps hub-process lanes at **≤1/4 of dispatched width**, floor arithmetic, evaluated
under the I-D10 three-way split (*feature/satellite · finish-line · hub-introspection*).

```
width 7  ->  floor(7/4) = 1 hub-introspection lane permitted
```

**All seven conversion lanes bucket as `finish-line`** — each finishes existing rows by replacing a
Done-when clause; none lands methodology doctrine and none arms a gate. So the wave as specified
occupies **0 of 1**, and the cap is not near binding.

**The trap:** that free slot is exactly one lane wide, and three plausible morning additions all
compete for it — `[#528]` leg 3 (telemetry `test_run` duration, PLAYBOOK-adjacent), the owed
provisioning-time lane-grammar row (packet W3), and any doctrine write-up from the adjudication.
**At most one may ride.** Note also that phase-1's own overage (W5: N *and* O both in the hub
bucket at width 7) is **reported and undischarged** — it should be dispositioned before a second
batch inherits the precedent, and that is a one-line ruling, not work.

### 1.5 · The two premises that do **not** validate

| # | Premise | Verdict | Evidence |
|---|---|---|---|
| **P7** | The base the lanes will branch from carries phase 1 | **NO-GO** | `origin/main` = `7bbb067` (2026-08-14). `HEAD` is **59 commits ahead**; `main` is an ancestor of `HEAD`, so nothing is divergent — but the manifest, all seven lane merges, the integration wrap, the drafts artifact and the five night-2 landings exist **only** above `origin/main`. A lane provisioned from `origin/main` boots into a tree with **no drafts artifact and no closed batch**. |
| **P6** | Forks D6.5 and D6.6 are resolved | **NO-GO** | The W2-0 contract cross-checked D6.1–D6.6 against the off-repo `~/Downloads/MORNING-ADJUDICATION-2026-08-15.md` §A and records verbatim matches for **D6.3 (`#391`) and D6.4 (`#417`) only**. D6.2 (`#364`) is discharged by the retirement. **D6.5 (`#502`, "the stated blocker is discharged") and D6.6 (the three home-substitutions `#82` / `#324` / `#412`) have no in-repo resolution.** |

**P6's blast radius, stated per lane rather than in aggregate:** `#502` → W2-d · `#82` → W2-e ·
`#324`, `#412` → W2-g. **4 of 29 ids across 3 of 7 lanes.** The drafts artifact's own §2 says the
three home-substitutions are *"a textual substitution if the operator names another"* — so D6.6 is
**three words from the architect, not a work item**. D6.5 is a one-line verdict on whether `#502`'s
blocker is discharged. Both are adjudication-hour business.

**Neither NO-GO is a reason to shrink the wave.** They are reasons to sequence: push first, rule
D6.5/D6.6 in the adjudication hour, then dispatch all seven at full width.

### 1.6 · Premises that validate cleanly, recorded so they are not re-checked

- **Batch state is clean.** The phase-1 packet is committed, so batch 5 is closed and the ADR-110
  exemption is expired. A phase-2 manifest opens a fresh batch with nothing inherited.
- **`doc_rot` is exactly the packet's 7 loci** — `#514 #530 #528 #529 #523 #492 #419`, matching the
  packet's attribution line for line. WARN-tier; gates nothing.
- **`undeclared_edges` is 20**, unchanged in kind. **`silent_rule_ratchet` live 440 ≤ baseline 441.**
- **`task_tree_coherence` OK** — `BACKLOG.md` reassembles from `tasks/` exactly, which is the check
  that will police all seven phase-2 regenerations.
- **The suite's one RED is pre-existing and re-confirmed independently here.**
  `routine_consumers` prints *"2 declared routine row(s)"* while
  `test_routine_consumers_live_backlog_governs_exactly_one_row` asserts `'1 declared routine row'`.
  Not the batch's, and not phase-2's to fix.

### 1.7 · One defect found in passing, in an append-only file

`JOURNAL.md:80` (entry `2026-08-15 (c)`) reads:

> **Result:** 7 of 7 lanes merged, **0 abandoned**, close-width delta **0**. Full suite:
> `SUITE_ONELINE_TOKEN` Rows: …

**The literal placeholder `SUITE_ONELINE_TOKEN` was committed unsubstituted**, so the batch-5
JOURNAL entry states no suite result at all. The real figure (`1 failed, 2955 passed, 3 skipped,
1 xfailed in 1431.73s`) is in the packet §2, so nothing is lost — but `JOURNAL.md` is append-only
and cannot be edited in place, which makes this a **correction-by-append** item, not a fix.
Proposed: one line in tomorrow's own JOURNAL entry naming the token and carrying the number.
Reported here rather than acted on — this lane is read-only.

---

## §2 · Phase-1 measured anatomy → the phase-2 estimate

### 2.1 · What phase 1 actually cost (commit timestamps, this branch)

| segment | span | note |
|---|---|---|
| **Dispatch** — first → last step-0 contract commit (`16:36:11` → `16:48:36`) | **0h12m** | all 7 lanes booted and contracted |
| **Lane work** — dispatch → last lane work commit (`→ 17:52:01`) | **1h15m** | 7-way parallel; lanes finished `17:22`–`17:52` |
| **IDLE** — last lane commit → first integrator act (`→ 19:21:50`) | **1h29m** | dead time; nothing was running |
| **Merge queue** — manifest merge → last lane merge (`19:44:05` → `20:39:48`) | **0h55m** | 7 merges, intervals `10.8 · 6.5 · 6.9 · 11.5 · 6.6 · 7.8` min, **mean 8.3** |
| **Close-out** — last lane merge → batch close (`→ 22:12:16`) | **1h32m** | suite 23.9 min = **26%** of it; the rest is row updates + packet + JOURNAL |
| **TOTAL dispatch → batch close** | **5h36m** | |
| *(+ night-2 UNIQUE-HOLD landing → `23:00:53`)* | *6h24m* | post-batch, not part of the estimate |

**The prompt's figures reconcile as follows, stated rather than silently adjusted.** *Suite 1431s*
— exact, packet §2. *Integration 3h09m* — measures ~`19:03` → `22:12`, i.e. the integrator session
from boot; the first integrator **commit** is `19:21:50`, giving 2h50m, and manifest-commit → close
gives 2h40m. All three describe the same window and differ only in where the clock starts; I use the
commit-derived spans because they are re-derivable from the tree. *Dispatch 18:0x* — does **not**
match the commit record, where all seven step-0 contracts land `16:36`–`16:49`; `18:0x` is
consistent with the packet §4a session-jsonl mtimes (`17:58`–`18:43`), which are **idle-session**
timestamps, not dispatch. **The commit record is the instrument I trust here; the mtimes measure
when a seat stopped typing, not when it started.**

### 2.2 · The single biggest wall-clock lever

```
Phase-1 wall clock, by owner:
  lane work (7-way parallel)   1h15m   22%
  integrator serial tail       3h56m   70%   <- idle 1h29 + queue 0h55 + close-out 1h32
  dispatch                     0h12m    4%
  the full test suite          0h24m    7%   (inside close-out)
```

**The lever is the integrator's serial tail, and the cheapest cut inside it is the 1h29m idle
prologue.** It is 27% of the window, it costs nothing to remove, it needs no new machinery, no gate
change and no ruling — only that **the integrator boots on a clock (dispatch + ~75 min) rather than
on lane completion.** Phase-1's lanes were done at `17:52`; the integrator's first act was `19:21`.

This is the same term `[NB2-B]` §4a already named from the W4 wave — *"the dominant latency term was
waiting for an integrator, not running tests"* — reproduced at a second width, on a second batch,
under a different lane mix. **Phase-1 is the corroborating measurement that finding was missing.**

**The lever the numbers do *not* support, said plainly so it is not chased:** the suite is 7% of the
window. `[#528]` legs 1+2 already landed the xdist flags and the tiered-suite law; there is nothing
further to win there tomorrow, and a second suite optimisation would be work aimed at the seventh
cheapest minute.

**Second-order, and worth ten minutes of the adjudication hour:** §1.2's 3× conflict-surface
increase lands entirely inside the queue segment. Pre-agreeing the mechanical resolution — stage the
lane's `tasks/` edits, then run the three generators, never a hand-merge, in that order because
`gen_audit_index.py` reads **tracked files only** — converts a per-merge decision into a per-merge
keystroke. Phase-1 learned that ordering the hard way on the audit index alone; phase 2 hits it on
three files, seven times.

### 2.3 · The phase-2 estimate

| segment | estimate | basis |
|---|---|---|
| Adjudication hour (NB3-B queue) | **1h00** | operator-set; queue size not visible to this lane (§5) |
| Dispatch, 7 lanes | **0h15** | measured 0h12 at the same width |
| Lane work | **1h00** | conversion is lighter than build — 3–5 Done-when rewrites + regen + packet, vs. new modules with tests. Phase-1's 1h15m is the ceiling, not the mean |
| Merge queue | **1h30** | 8.3 min/merge measured at **1** conflict surface; phase 2 has **3** on 7 of 7 lanes. +50–60%/merge → ~13 min × 7 |
| Close-out | **1h30** | measured 1h32m; suite unchanged (~24 min), packet comparable |
| **Subtotal — integrator booted on a clock** | **≈ 5h15m** | |
| Subtotal — if the 1h29m idle prologue repeats | ≈ 6h45m | |

**Sensitivity, since one number carries the estimate.** If the 3× conflict surface costs *nothing*
(regeneration is scripted and clean), the queue holds at ~1h00 and the total is **4h45m**. If it
costs double rather than +55%, the queue is ~2h00 and the total is **5h45m**. The estimate is
therefore **4h45m – 5h45m** with the idle prologue removed, and that band is dominated by one
unmeasured quantity: how long a three-file regenerate-and-verify takes at merge. **Phase-2's own
first merge measures it** — worth recording explicitly in the manifest so phase 3 does not estimate
it again.

---

## §3 · Proposed morning sequence

### Position 0 — before anything else (≈ 10 min, and it is not optional)

1. **Push `main`.** `origin/main` is 59 commits behind. Until it is pushed, a cloud-provisioned lane
   boots without the drafts artifact and without a closed batch. This is premise **P7** and it is
   the one item that silently produces seven wrong lanes rather than one loud failure.
2. **Confirm the seven phase-1 worktrees are teardown-eligible** and remove them
   (`lane-{m,n,o,p,q,r,s}-*`). All seven are merged; the packet withheld teardown pending the
   operator's word. Teardown is **two branches, not one** — the work branch *and* the
   `worktree-<name>` provisioning branch. Doing this **before** dispatch keeps `stale_worktrees`
   clean and frees the lane letters; doing it mid-queue is the one timing that is actively bad.
3. **Re-verdict and prune the eight `claude/night2-*` branches.** JOURNAL `(d)` landed all five
   UNIQUE-HOLD artifacts, so the teardown trap is dissolved — but its own **Next** line sets the
   bar: *"deletion proceeds only on a per-branch byte-coverage proof — any branch not byte-covered
   is HELD, not deleted."* Not a wave dependency; do it here or after close, never during.

### Hour 1 — adjudication (≈ 1h00)

Work the NB3-B queue. **Four items are phase-2 preconditions and should be taken first, in this
order**, because everything after them is dispatchable:

| # | Item | Why first | Cost |
|---|---|---|---|
| A1 | **D6.6** — name the home for `#82`, `#324`, `#412` | Unblocks W2-e and W2-g. The drafts call it a *textual substitution* — three names, not a design | ~5 min |
| A2 | **D6.5** — is `#502`'s stated blocker discharged? | Unblocks W2-d | ~5 min |
| A3 | **Confirm the wave is 29, W2-b is 3** | Ratifies §1.1 so no lane re-derives it | ~2 min |
| A4 | **Disposition phase-1's W5 cap overage** | An undischarged overage becomes precedent at the next dispatch | ~3 min |

Then the rest of the NB3-B queue, plus the packet's carried wrap items — **W1** (`CLAUDE.md` §5
rule 4's descriptive falsity: amend, or re-scope to §10's accurate *"no scripts that drive state in
child repos"*), **W2** (re-point `PLAYBOOK.md` L844/L866 at the landed audit paths), **W3** (a row
for the provisioning-time lane-grammar gap — third occurrence, needs `kill-candidates:`), **W4**
(`[#527]`'s closure proposal via `/review-closures`), **W9** (`review_artifact_coverage` cannot see
an off-repo terra artifact).

**Explicitly do not rule `#371`** (§1.3). Say so in the record.

### Hour 2 — dispatch (≈ 0h15)

Seven lanes, full width, all `finish-line` class declared **ex-ante** in the manifest roster.

- **Open the batch manifest AT DISPATCH, not at integration.** `[#505]` leg 1 has now been missed
  **four consecutive batches**, phase-1 being the worst of the four (its manifest landed at
  integration). Tomorrow is the cheapest possible window to fix it: the manifest is one file and the
  batch has no prior state to reconcile.
- **Name the lane branches on-grammar** — `worktree-lane-<letter>-<id>-<slug>`, `<id>` matching
  `\d+`. Phase-1 lost the ADR-110 exemption on two of seven (`w20` is not `\d+`; `gateclose-drain8`
  has no id slot) and nearly wedged the queue at merge #1. Conversion lanes carry no single row id,
  so **this is the batch where that bites again** unless each lane is named from one of its own ids.
  The grammar is still enforced nowhere at provisioning (packet W3).
- **Order:** W2-a first (it carries the `#419` re-check, whose skip reason is the one the wave most
  risks repeating); W2-d last (off-repo verdicts escalate most readily); the rest order-free.
- **Stop-condition, restated in every contract:** *if a lane finds its conversion requires touching
  the grouped surface, it stops and reports rather than proceeds.*

### Hour 3 — lane work (≈ 1h00, parallel)

Lanes run. **The integrator boots at dispatch + 75 min regardless of lane state** — that is the
§2.2 lever, and it is the single scheduling decision that most changes tomorrow's finish time.

### Hours 4–5 — merge queue (≈ 1h30)

Serial, `--no-ff`, from the primary checkout. Per merge: stage the lane's `tasks/` edits **first**,
then regenerate `BACKLOG.md`, `tasks/manifest.json` and `docs/audits/README.md`, never hand-merge.
**Record the first merge's wall time in the manifest** — it is the measurement §2.3 is missing.

### Hours 6–7 — close-out (≈ 1h30)

Full suite **once**, on the merged tree, in a default shell. Expect the same one pre-existing RED
(§1.6) — if a second appears, it is the wave's. Then the packet, then JOURNAL (carrying the §1.7
`SUITE_ONELINE_TOKEN` correction), then:

- **Promotions** — D3.1 `N2-D1-02` (trigger now met, W3 landed), D3.2 the consolidation intake
  (`status: DRAFT`, Sections A/B/C — **one** artifact, not four items), D3.3, D3.4, D3.5 (`I-D7`,
  whose expiry is met and whose locator no longer resolves).
- **Re-measure the untestable count properly.** The `58` baseline is now stale on at least three
  counts: `#364`'s retirement, the `#529`/`#530` births, and the 29 conversions themselves. It is
  arithmetic over 2026-08-10 grades, never a fresh re-grade (`O-3`'s own honest limit), and the live
  set is **195 rows (171 open + 24 deferred)**, not the 196 the plan carries. **A wave that converts
  29 rows and reports against a stale denominator proves nothing** — this is the one close-out item
  where the measurement matters more than the work.
- **`[#492]`'s 08-17 checkpoint is Monday, tomorrow is Sunday 08-16.** Do the browser re-check if
  convenient and record the result; **do not move the date** and do not treat a Sunday check as
  discharging a Monday commitment. The peg is an external fact (Grok 4.6 release), the corpus that
  gates it is reconciled (`…-verification-492-corpus-reconciliation.md`), and the dated commitment
  is watched by **no organ** — which is L1's whole point and the reason it needs a human on Monday.

---

## §4 · What should NOT be attempted tomorrow

| # | Do not | Reason |
|---|---|---|
| 1 | **Rule `#371`** | `#387` has not landed. Ruling `#371` first ratifies against a document the fleet has already refuted — `#387`'s own stated reason for existing (§1.3). |
| 2 | **Start the `[#412]` measurement leg** | The roadmap scopes it *"after batch-4 closes"* and it is a **research** leg — measure CC-native custom agents and auto-triggering skills **before** building. It cannot share a window with a 7-wide wave without one starving the other, and `[#412]` is a named anti-goal for re-derivation (roadmap §6). It is a next-window headliner, not a rider. |
| 3 | **Open the closing campaign** | `L-3` places it in the **windows-3–8** sequence and forbids re-scoping the under-100 number on anything less than *"two or more windows of net closure data."* Phase 2 **produces** that data. Starting the campaign tomorrow spends the evidence before it exists. |
| 4 | **Treat `[#492]` as dischargeable on 08-16** | The commitment is dated **08-17**. A Sunday check is evidence, not discharge; moving the date to fit the session is precisely the drift `RE-CHECK` was written to prevent. |
| 5 | **Add an eighth lane** | Width 7 is measured — dispatch 12 min, queue mean 8.3 min/merge. Width 8 is the first roster admitting **two** hub lanes (`⌊8/4⌋ = 2`) and would invite exactly the W5 overage phase-1 has not yet dispositioned. The queue is already the binding constraint (§2.2); widening lengthens it. |
| 6 | **Edit `CLAUDE.md` §5 rule 4** | Ruled **R3** as carry-not-edit. It is a governance edit to a canonical file, and `CLAUDE.md` sits ~195 of its 200-line budget and is the fleet's most reliable collision file. If the architect wants it, it is a standalone act with its own re-read and `last_reviewed` stamp — never a rider on a wave. |
| 7 | **Birth rows mid-wave** | Every new id needs a `kill-candidates:` line (`backlog-filing-backpressure`), and a birth during a 7-way queue mints `BACKLOG.md`/`manifest.json` churn in the exact files all seven lanes are regenerating. The owed W3 row belongs in the adjudication hour, before dispatch. |
| 8 | **`[#528]` leg 3 (telemetry `test_run` duration)** | It needs the emit module to have produced data, which it has not; and it competes for the single free hub-process slot (§1.4). Cheap and correct alternative, already proposed by `[NB2-B]` §4b: **one `T_start` line per lane**, which converts the whole latency row from UNVERIFIABLE to derivable at essentially zero cost — and would have made §2.1's reconciliation unnecessary. |
| 9 | **Hand-merge any of the three generated files** | Already ruled; restated because phase 2 triples the exposure. `task_tree_coherence` catches a bad `BACKLOG.md`, but `gen_audit_index.py` reads **tracked files only** and will silently omit an unstaged addition. |
| 10 | **Delete branches or worktrees during the queue** | Do it at position 0 or after close. Mid-queue teardown while seven lanes hold refs is how a merge loses its base. The five night-2 UNIQUE-HOLD artifacts are now on `main`, so deletion is finally *safe* — which is a reason to schedule it, not to improvise it. |

---

## §5 · Honest limits of this report

1. **This is a shallow clone** — 28 grafts, history begins `2026-08-10`, 283 commits reachable.
   Every git-history-dependent check is unreliable here. The `audit.py health` run returned
   `health: DEGRADED` with three FAILs, and **all three are clone artifacts, not regressions**:
   `journal_spine_anchor` (the ADR-85 disposition floor `24882f8cc` is not a valid object in this
   clone), `hooks_armed` (hooks were never installed here), and `canonical_freshness` (computed from
   truncated `git log` dates). **I did not reproduce the packet's `health: OK`, and I do not claim
   it — I claim only the tree-content checks, which are unaffected by depth.** `no_ff_merges` reads
   1 here vs. the packet's 3, and `review_artifact_coverage` 1 vs. 2, both for the same reason.
2. **I did not run the test suite.** The pinned toolchain does not resolve here
   (`uv 0.8.17` vs. the required `0.11.19`); `audit.py` ran only after installing `click`,
   `pyyaml` and `markdown-it-py` into the container. This is `[#484]`'s system-vs-locked Python
   divergence showing up in a third place, and it is worth noting that a **cloud lane cannot
   currently run this repo's own gate as specified.**
3. **`NB3-B`'s output is not visible to this lane.** No `docs/audits/*night3*` artifact exists in
   the tree and no night-3 branch exists on `origin` beyond this one. The adjudication hour is
   costed at 1h00 as a **placeholder**; if NB3-B's queue is long, §2.3's total moves with it
   one-for-one.
4. **The "outgoing review §7/§8" is not in-repo.** The phase-1 review packet
   (`PHASE1-REVIEW-PACKET.md`) and `MORNING-ADJUDICATION-2026-08-15.md` are both operator-side
   Downloads files, and the phase-1 packet's own §7/§8 are *Ruling discharge* and the
   *`/lane-integrate` checklist* — not next-window headliners. The headliners in §3's close-out are
   therefore **reconstructed from the in-repo record** — `…-roadmap-north-star-frozen.md` §1/§2/§4,
   `STANDING_RULINGS` `L-3`, the packet §5 wrap items and JOURNAL `(c)`/`(d)` **Next** lines — and
   should be reconciled against the actual review before they are acted on.
5. **The dispatch-time discrepancy (§2.1) is reported, not resolved.** If `18:0x` is the true
   dispatch, the idle prologue shrinks to ~0h00 and lane work stretches to ~2h50m — which would
   move §2.2's lever from *idle* to *queue + close-out* while leaving the conclusion
   (**the integrator's serial tail owns the wall clock, not the suite**) unchanged. The lever
   survives either reading; only its cheapest cut moves.

---

## §5a · AMENDMENT — 2026-08-15, same session, after the locked toolchain was made to run

Appended per CLAUDE.md §5 rule 3 (an audit is superseded by a new file **or an in-file amendment
marker**; never edited in place). §5's text above is left exactly as written. Two corrections and
one strengthening, in order of consequence.

**1. CORRECTION — §5 limit 1 says "three FAILs"; there are four `[!!]` markers.** The three it
names are the `self-audit` check FAILs and are correctly named. The fourth,
`[!!] repos registered  (none)`, sits in the **`operational:`** preamble rather than the check
list, and my first run read it through a `tail` that cut the head off. It is a container artifact
of the same class — no sibling repos exist on this disk, corroborated independently by
`fleet_parity` (*"/home/user/ai-council is not a git repo"*, likewise `corp-monorepo`).
**The conclusion is unaffected; the count was incomplete and is now stated correctly.**

**2. STRENGTHENING — §5 limit 1's attribution is now proved, not asserted.** I got the pinned
toolchain running (`uv 0.11.19`, installed via `pip` and placed ahead of the container's `0.8.17`
on `PATH`) and re-ran `uv run --locked python scripts/audit.py health`. **The result is identical**
— same `health: DEGRADED`, same three check FAILs, same text. So the verdict is independent of
the toolchain, which removes the obvious alternative explanation. The `canonical_freshness` leg is
now demonstrated rather than inferred:

```
git log -1 -- VISION.md                        -> 12ef9c9  2026-08-10T17:47:01+02:00
git log -1 -- CONTRIBUTING.md                  -> 12ef9c9  2026-08-10T17:47:01+02:00
git log -1 -- protocols/SESSION_SETUP.md       -> 12ef9c9  2026-08-10T17:47:01+02:00
git log -1 -- protocols/DEFINITION_OF_DONE.md  -> 12ef9c9  2026-08-10T17:47:01+02:00
earliest reachable commit (the graft floor)    -> 12ef9c9  2026-08-10T17:47:01+02:00
```

All six stale files report their "last edit" as **the graft floor itself**. In a shallow clone every
untouched file's history terminates there, so `canonical_freshness` reads the truncation as an edit.
`journal_spine_anchor` fails on the same truncation (`24882f8cc` is below the floor and therefore not
a valid object here), and `hooks_armed` fails because the container never ran `pre-commit install`.
**All four are clone artifacts. None is a regression. The packet's `health: OK` is still not
reproduced here, and is still not claimed.**

**3. CORRECTION — §5 limit 2 overstates the blocker.** It reads *"a cloud lane cannot currently run
this repo's own gate as specified."* **It can** — after replacing the container image's `uv`. The
repo's pin is not the defect; the **container image ships `uv 0.8.17` against a `==0.11.19`
requires-version floor**, and `uv self update 0.11.19` is refused by the managed install
(*"version 0.11.19 was not found for the app uv in workspace uv"*), so the working route is
`pip install uv==0.11.19` ahead of it on `PATH`. Once that is done the locked environment resolves
cleanly (CPython 3.12.10, 27 packages) and both the gate and the `Stop` hook run as configured,
exit 0. **This sharpens rather than withdraws the finding for `[#484]`:** the divergence is in the
cloud image, it is one line to fix at provisioning, and until it is fixed every cloud lane either
approximates the gate or silently skips it — which is the failure mode worth the architect's
attention, not the pin itself.

---

```
GO-READY: NO -- 6 of 8 phase-2 premises GO; 2 NO-GO, both clearable in the adjudication hour.
          GO on: 29 open ids all PROSE-CONVERTIBLE (W2-b is 3, not 4) | tasks/ partition still
          7-way disjoint post-phase-1 | #371-before-#387 bar stands and binds adjudication only |
          cap arithmetic floor(7/4)=1 with 0 hub lanes in the wave | drafts landed | batch closed.
          NO-GO on: P7 origin/main is 59 commits behind (push before dispatch) and P6 forks
          D6.5 + D6.6 unresolved in-repo (4 ids, 3 lanes) -- ~10 min of ruling, not work.
ESTIMATE: ~5h15m to batch close with the integrator booted on a clock (band 4h45m-5h45m);
          ~6h45m if phase-1's 1h29m idle prologue repeats. Add the adjudication hour as measured.
```
