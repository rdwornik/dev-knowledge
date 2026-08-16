# Night-3 B — the architect's morning decision queue (DRAFT)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** night3-decision-queue
- **Status:** **DRAFT — proposals only.** This lane closed nothing, ratified nothing, edited no
  governed file and deleted no ref. Every verdict below is *proposed*; the architect's word is what
  makes any of it real.
- **Lane:** night-3 B, read-only · branch `claude/night3-decision-queue-791dkc`
- **Base:** `main` @ `65dc3183` — post phase-1 wrap (`6a80f98`) **and** post the night-2
  UNIQUE-HOLD landing (`ed3abe9f`), which is newer than the phase-1 packet and changes one of its
  tables (§7, D14).
- **Brief:** the 7 items of the night-3 B dispatch. Each decision carries **evidence · proposed
  verdict · one-line rationale · what it unblocks**.

---

## §0 · Measurement caveats — read before trusting any number here

This lane ran in a **cloud clone that is shallow** (283 commits; `.git/shallow` carries 28 graft
points, the oldest dated 2026-08-02). Three consequences, stated up front so no number below is
read as a finding when it is an artifact:

1. **`audit.py health` reports `DEGRADED` here and that verdict is an artifact, not repo state.**
   `journal_spine_anchor` aborts with `AnchorError: disposition floor 24882f8cc is not an ancestor
   of main` — the floor commit is below the graft boundary. The phase-1 packet's `health: OK` at
   `d62796ad` stands; this clone cannot reproduce it and does not contradict it.
2. **`canonical_freshness` FAILs here on 6 files, and that is also an artifact.** All six resolve
   to the *same* commit `12ef9c9` — a graft boundary, which appears to introduce every file it
   contains, so `git log -1 -- <file>` mis-attributes unedited files to it. Proof: `VISION.md`,
   `CONTRIBUTING.md`, `docs/handoffs/README.md`, `protocols/SESSION_SETUP.md`,
   `protocols/AI_COUNCIL_PROCESS.md` and `protocols/DEFINITION_OF_DONE.md` all report the identical
   "last edit 2026-08-10". **This is why §2 does *not* revive the triage backlog's VISION.md
   freshness finding** — on a full clone that check passed at `d62796ad`.
3. **`no_ff_merges` flags `12ef9c912`** — the same graft artifact. `git_backlog_drift` reports clean
   where the packet reports `#505` closed-but-present, for the same reason.

Everything in §1–§7 below was derived from sources the shallow clone *does* hold in full: the
working tree, `tasks/`, `BACKLOG.md`, the landed audits, and the 283 commits of the phase-1 window.
Where a claim depends on history below the boundary, it is marked.

**One non-read act was performed:** `python scripts/propose_closures.py` was run to materialise the
`/review-closures` surface, which is gitignored and therefore absent from a fresh clone. It writes
only `logs/PROPOSALS-2026-08-15.md` (ephemeral, gitignored, never governed state) and mutates no
BACKLOG row — the script's own read-only contract. Nothing else was executed.

---

## §1 · The closure-proposal surface — item 1

### 1.0 · The count reconciles to 161, not 153, and the delta is explainable

| Measure | Value |
|---|---|
| Brief's stated figure | **153** pending proposals |
| Measured live at `65dc3183`, full window | **161** (2 STRONG + 159 WEAK) |
| Open BACKLOG rows (denominator) | **195** |
| **Share of the open backlog proposed for closure** | **82.6 %** |

The 8-row delta is a **window artifact, not a discrepancy**: the operator's surface was measured
before the phase-1 wrap and the UNIQUE-HOLD landing; a sweep across baselines from `HEAD~260` to
`HEAD~280` plateaus at 161 in every case. Nothing turns on 153 vs 161 — the decisions below hold
identically at either figure, and the ratio is what matters.

### D1 — the two STRONG proposals: **REJECT BOTH**

**Evidence.** STRONG means a `closes [#N]` commit landed while `[#N]` is still open. Both fire, and
both are contradicted by a ruling made *after* the commit they cite:

| id | Evidence commit | Why it is a false positive |
|---|---|---|
| `#505` | `08c880f61` *"backlog testability census — all 170 open Done-when graded"* | Phase-1 packet **W6**: *"`[#505]` leg 1 stays unmet — this is the **fourth consecutive batch** to miss commit-at-dispatch."* The commit discharged a *leg*, not the row. `status: open` is deliberate. |
| `#530` | `73da833ca` *"lane P packet — Done-when met on the real origin"* | Ruling **R2** of 2026-08-15 explicitly rules **`[#530]` stays OPEN** with two P1 legs filed on the row. The commit subject asserts a completion the ruling then declined. |

**Proposed verdict — REJECT both.** *Rationale:* a closing-commit token is evidence of intent, not
of ruled completion, and in both cases the governing ruling post-dates the commit and says
otherwise. *Unblocks:* nothing is closed; it prevents two rulings being silently reversed by a
detector.

### D2 — the 159 WEAK proposals: **DISMISS AS A CLASS, no per-row reading**

**Evidence.** The WEAK heuristic fires when an open row *names a file* and *some commit touched
that file* with no `closes` token. Measured composition of today's 159:

```
evidence path                            rows citing it
protocols/STANDING_RULINGS.md                 29   <- churn
scripts/audit.py                              22   <- churn
protocols/HANDOFF_PROCESS.md                  11   <- churn
protocols/PLAYBOOK.md                         11   <- churn
scripts/session_end_backpressure.py            8
scripts/gen_handoff.py                         7
   (tail: 141 further paths, 1-6 rows each)

serialize-group spread:  audit-py 41 · architecture 16 · settings-json 15 ·
                         handoff 14 · none 44 · (9 further groups) 29
```

Four hub-churn files alone drive **73 of 159**. These are files that change *by construction* every
arc, which is precisely the defect `[#277]` leg (b) names verbatim: *"a task naming audit.py /
PLAYBOOK.md / HANDOFF_*.md / BACKLOG.md is flagged every arc because those files change by
construction (near-zero precision)."*

**Proposed verdict — DISMISS all 159 as a class.** *Rationale:* a detector that proposes closure for
82.6 % of the open backlog carries no information — the proposal set is not a signal about any row,
it is a restatement of the backlog. *Unblocks:* the `/review-closures` surface stops consuming
architect attention every session; and it removes the standing risk that a real STRONG hit gets
lost in a 159-row list.

### D3 — route today's measurement to `[#277]` as its **ratio evidence**

**Evidence.** `[#277]`'s own Done-when: *"a single run over the last 30 days of `main` yields a
STRONG:WEAK-actioned ratio better than 49:0 with the run's numbers recorded in the closing
commit."* Today's run, over 283 commits:

```
STRONG proposed  2   actioned 0   (both rejected — D1)
WEAK   proposed 159  actioned 0   (dismissed as a class — D2)
                ---
        total  161   actioned 0        vs the 2026-07-07 baseline of 49:0
```

**Proposed verdict — record 161:0 against `[#277]`; the row stays OPEN and its priority is a live
question.** *Rationale:* the ratio has degraded 3.3× since the row was written, which converts
`[#277]` from a quality complaint into a measured regression. *Unblocks:* `[#277]` gains the
denominator its Done-when demands, so a future repair has a real before-number to beat.

### Conflict + serialize-group flags (the brief's explicit ask)

- **Serialize-group collisions are structural, not incidental.** 41 of the 159 sit in
  `audit-py` and 16 in `architecture` — the two largest serialize-groups in the repo (60 and 30
  rows). Any batch-close of WEAK rows would therefore have serialised behind two groups at once.
  D2 dissolves this rather than sequencing it.
- **Four rows conflict directly with *open* phase-1 work** and must not be closed under any
  reading: `#527` `#528` `#529` `#530` all appear in the WEAK set because phase-1 touched files
  they name — and all four are ruled OPEN (R2/R7), three of them with explicitly enumerated
  unbuilt legs.
- **No conflict with lane R's drain.** R drained `#344 #423 #430 #415 #487 #428`; none of the six
  is among the ids this decision queue proposes to act on anywhere.

---

## §2 · The 15 nightly triage findings — item 2

**What they are.** 15 open GitHub Issues labelled `nightly-triage`, authored by `github-actions`
between **2026-06-09 and 2026-06-25**, carrying ~26 findings between them. They are the exact 15
`[#428]` names: *"15 Issues stay open and every SessionStart tells the operator they await action."*

### D4 — **BATCH-DISMISS all 15.** Every finding class is resolved, superseded, or out-of-scope by its own rule

Verified against the live tree, class by class:

| # | Finding class | Issues | Live state | Verdict |
|---|---|---|---|---|
| A | CLAUDE.md §8 *"no repo-level skills directory exists yet"* | 11 | Phrase **absent**; §8 documents `verify` + `check-against-spec` | **dismiss — fixed** |
| B | CONTRIBUTING.md *"squash-merged automatically"* vs ADR-84 Q9 | 2 | No `squash` token anywhere in CONTRIBUTING.md | **dismiss — fixed** |
| C | CONTRIBUTING.md hardcoded check count (13 vs 16/17) | 2 | The number is **gone**; text now reads *"the self-conformance checks"* — the durable fix the finding itself proposed. (Live registry: `len(ALL_CHECKS) == 43`) | **dismiss — fixed structurally** |
| D | ARCHITECTURE.md inline vs frontmatter timestamp | 3 | Both read `2026-08-14` | **dismiss — fixed** |
| E | ARCHITECTURE.md stale test count (`329 collected`) | 1 | Count moved to generated `ecosystem/doc-counts.md` | **dismiss — fixed structurally** |
| F | VISION.md `last_reviewed` drift | 3 | Passed on the operator's full clone at `d62796ad`; the FAIL in *this* clone is the §0(2) graft artifact | **dismiss — resolved** |
| G | CLAUDE.md §11 ADR window not rotated | 1 | §11 is now the generated `@.claude/generated/recent-adrs.md`, gated by `claude-rosters-freshness` | **dismiss — fixed structurally** |
| H | `[#152]` closed though PLAYBOOK §8 was not pointerized | 1 | `[#152]` closed; §8 is 194 lines — but Ch8 is now *deliberately* a chapter whose handoff-prep part is an index of pointers (cited by `HANDOFF_BOOT.md`) | **dismiss — superseded by design** |
| I | JOURNAL cites unresolvable SHAs `f578ac4`, `818a1c6` | 1 | Both pre-date the shallow boundary; the issue's own text records that *"the guard's explicit rule is that pre-boundary SHAs are not findings"* | **dismiss — out of scope by its own rule** |
| J | BACKLOG `#79` closed by inline RESOLVED notation | 1 | Self-corrected at `024282c` in the same window; issue says *"no current remediation needed"* | **dismiss — process note** |
| K | Merge commits carry `closes [#N]` without the BACKLOG removal | 1 | Now mechanized: the `backlog-id-on-close` commit-msg gate | **dismiss — mechanized since** |
| L | JOURNAL omission, 2026-06-08 floor re-pilot | 1 | Historical; superseded by the ADR-85 anchoring regime + `journal_spine_anchor` | **dismiss — superseded** |

**Net: 0 of ~26 findings survive as live work.** *Rationale:* every class was either repaired, or
repaired *structurally* (the hand-maintained value replaced by a generated one — which is why these
did not recur), or is excluded by the guard the finding itself cites. *Unblocks:* the Issue backlog
becomes closable in one act rather than 15 readings.

### D5 — close out the Issue backlog and record the count → discharges `[#428]`'s second leg

**Evidence.** `[#428]` Done-when, leg 2: *"the GitHub Issue backlog is either closed out or
`scripts/surface_triage.ps1` no longer reads it — **with the Issue count at closing time recorded in
the commit**."* The count at closing time is **15** (measured this lane, `state=OPEN`,
`label=nightly-triage`, `totalCount: 15`).

**Proposed verdict — close all 15 with a one-line disposition pointing at this section, and record
`15` in the closing commit.** *Rationale:* leg 2 is satisfiable *today* by an act that needs no
build, and D4 supplies the per-issue justification the closure would otherwise lack. *Unblocks:*
`[#428]` drops to a single remaining leg — the dead-producer *test* (leg 1) — and the SessionStart
surface stops asserting pending work that does not exist.

> **Leg 1 is NOT discharged by this.** `[#428]` also requires *"no session-start surface asserts
> pending work from a producer with no run in the last 30 days, **with a test seeding a dead
> producer**."* Closing the Issues empties the surface but builds no detector; the next dead
> producer would repeat the class. Closing the Issues without that test is a **partial** discharge
> and should be recorded as such, not as a close.

### D6 — `[#428]`'s row carries a **stale locator**; correct it at the `tasks/` source

**Evidence.** The row asserts *"the producer has been dead since 2026-07-09 (`.github/` deleted at
`82227f08`, on no branch)"*. Live: **`.github/` exists** and contains
`.github/workflows/report-only-wall.yml` (16,640 bytes) — the `[#501]` report-only wall. The
*premise* holds (no nightly-conformance producer runs), but the *evidence* as written is falsified
by the tree.

**Proposed verdict — correct the locator at `tasks/428-*.md` to name the deleted workflow rather
than the deleted directory; no closure, no birth.** *Rationale:* a row whose evidence clause is
checkably false invites exactly the "verify and find nothing" cycle that `/preflight` exists to
prevent. *Unblocks:* `[#428]` becomes verdictable by reading one path.

---

## §3 · W4 — the `[#527]` close proposal — item 3

**Evidence — the Done-when, leg by leg, re-measured live at `65dc3183`:**

| Leg (verbatim from the row) | Live evidence | Verdict |
|---|---|---|
| *"a seeded direct commit attempt on `main` is refused by a pre-commit hook"* | `scripts/block_commit_on_main.py` present; refuses a non-merge commit while `HEAD` is on `main`, with a `MERGE_HEAD` carve-out for a conflicted merge | **MET** |
| *"with a test"* | `tests/test_block_commit_on_main.py` — **13 passed** in this clone | **MET** |
| *"the hook is armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism"* | `block-commit-on-main` registered in `.pre-commit-config.yaml` under `default_install_hook_types: [pre-commit, commit-msg, pre-push]`; the `arm_hooks.py` SessionStart self-arm installs all three | **MET** |

Corroborating: the gate fired live during phase-1 integration, and `CLAUDE.md` §9 carries its roster
row (`a84f069d`) — the row the packet flagged as *owed to the integrator by design*.

### D7 — **CLOSE `[#527]`**

*Rationale:* all three Done-when legs are evidenced and the only reason it is open is that no ruling
in R1–R7 closed it — the packet says exactly this (*"Proposed, not self-declared"*), and W4 routes
it to the operator via `/review-closures`. *Unblocks:* `[#527]` leaves the open set; the `gates`
serialize-group frees up; and core-invariant #5 has both halves (`block-commit-on-main` at commit,
`block-ff-push` at push) recorded as *shipped* rather than *in flight*.

> **Close it with its honest limit attached, because the limit is the lane's own finding.**
> `current_branch()` returns `None` on **any** non-zero `git symbolic-ref`, so a genuine git failure
> silently **allows** the commit — while its sibling `merge_in_progress()` **raises** on git failure
> by explicit design. The module answers the same question two ways. `CLAUDE.md` §9's row already
> states this. It is a documented operator decision, not a defect discovered here — but a closure
> that omits it would overstate what shipped. **`block-ff-push` remains the real teeth.**

---

## §4 · W1 — `CLAUDE.md` §5 rule 4 is descriptively false — item 4

**Evidence.** `CLAUDE.md:89` currently reads:

```
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
```

It is false in the tree it governs: ~23 scripts under `scripts/` mutate state (`gen_*.py --write`,
`normalize_headers.py`, `propose_closures.py` writing `logs/`), and `scripts/audit.py:4707` pushes
to `origin`. Ruled **R3**: carry as a wrap item; do **not** let the integrator edit `CLAUDE.md`.
`CLAUDE.md` §12 v2.60 records the rule as *"knowingly LEFT STANDING"*.

**Three structural facts that constrain any fix — all verified, because they change the diff:**

1. **The line is REPO-LOCAL, not hub-coupled.** The `critical-rules-records` hub region ends at
   rule **3** — `templates/claude-regions/critical-rules-records.md` contains rules 1–3 only, and
   `parse_regions` confirms the region body terminates there. **Rules 4 and 5 have no template
   mirror**, so this is a *single-site* edit. (Contrast the v2.55/v2.56 fixes, which had to edit the
   carrier first.) `tests/test_boundary_headers.py` — 40 passed — stays green either way.
2. **Budget headroom is 4 counted lines.** `CLAUDE.md` measures **196 / 200**. Blank lines count;
   comment-only lines do not. A §12 entry costs **2** (bullet + separating blank), leaving 2 spare.
   **Both options below fit without a §12 condense.**
3. **Neither option adds a `must|shall|never` token beyond the one already there**, so
   `silent_rule_ratchet` (live 440 ≤ baseline 441) is unmoved. Option B removes none either.

### D8 — pick **Option A (amend)** or **Option B (re-scope)**. Both are paste-ready; the architect picks.

**Option A — AMEND: state the true invariant (blast radius, not absence of writes).**

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -89 +89 @@
-4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
+4. **Layer 2 never drives child-repo state** — no orchestration scripts: nothing in `scripts/` mutates, or executes against, a repo other than this one (ADR-28, ADR-36). Hub-local writes ARE in scope and permitted — generated rosters/indexes, `logs/` artifacts, and `audit.py`'s own `origin` push. The invariant is the **blast radius**, not the absence of writes; the read-only claim survives only where a check makes it true (`review_closures.py` is read-only *on governed state*, and says so).
```

- **What it buys:** the rule becomes true, and it keeps teeth — it still forbids the thing ADR-28
  and ADR-36 actually forbid.
- **What it costs:** it is a genuine governance amendment. It widens what §5 admits, so it wants a
  §12 entry saying so, and arguably an ADR-28/36 cross-check that neither ADR states the narrower
  claim as load-bearing.

**Option B — RE-SCOPE: make rule 4 say what §10 already says accurately.**

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -89 +89 @@
-4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
+4. **Layer 2 never executes** — no orchestration scripts: no script drives state in a child repo (ADR-28, ADR-36). Hub-local validators, generators and gates are in scope.
```

- **What it buys:** it is the *minimum* true edit, and it converges §5 rule 4 with §10's
  already-accurate *"validators only, no scripts that drive state in child repos"* — one claim at
  two sites instead of two that disagree. This is exactly the move v2.56 (I-D8) made for the
  boot-instruction phrase, and that precedent is on the books.
- **What it costs:** it drops the "read-only" language entirely rather than qualifying it, so a
  reader loses the (real, if narrower) fact that the *validators* are read-only on governed state.

**Recommendation, offered not taken: Option B.** It is the smaller edit, it has a live in-repo
precedent (I-D8: converge the second site onto the accurate one), and it leaves the wider question
— whether ADR-28/36 need amending — as its own act rather than smuggling it into a one-line fix.
*Unblocks either way:* W1 clears, the `doc_claims`/terra finding stops recurring against a canonical
file, and §12's *"knowingly left standing"* debt is discharged.

---

## §5 · W5 — the process-lane cap reading for lane O — item 5

**Evidence.**

- **The rule** (PLAYBOOK Ch8 / ADR-110 §amendment 2026-08-08 / `STANDING_RULINGS` **I-D10 G-8**):
  ≤1/4 of a batch's lanes may be `hub-introspection`, floor arithmetic, evaluated on **dispatched
  width**, under a three-way split — `feature/satellite · finish-line · hub-introspection` —
  declared **ex-ante** per lane.
- **Phase-1 as dispatched** (from its own manifest): width 7 → `⌊7/4⌋ = 1` permitted.

```
feature/satellite   Q(293) · M(529) · P(530)      3
finish-line         S(W2-0 drafts) · R(drain8)    2
hub-introspection   N(528 legs 1+2) · O(527)      2      <- permitted 1
```

- **N is hub by any reading** — it lands doctrine in `PLAYBOOK.md` and moves an `ESSENTIALS.md`
  stamp. Not in dispute.
- **O is the debatable one.** It ships `scripts/block_commit_on_main.py` + tests (a mechanism), and
  it edits `.pre-commit-config.yaml` (the hub's own commit path).
- **The precedent is thinner than it looks.** Batch 4 is the *only other* batch dispatched under
  G-8, and its packet records that it passed **"at the line"** — `1 of 4 = 25.0%` — **and that it
  passed only because W6 was dropped**: *"At the dispatched width of 6 the manifest itself recorded
  2 hub lanes against a permitted 1 — an overage cleared by roster change (A-3), not by
  conformance."* Batches 1–3 predate the vocabulary and are declared absent, not estimated. So
  **the cap has been evaluated exactly once, and has never been tested against a surviving
  overage.** Phase-1 is the first.

### D9 — proposed reading: **O is `hub-introspection`. The cap was exceeded by one, and the honest verdict is a recorded exceedance, not a re-bucketing.**

*Rationale:* the shipped-feature reading is available — O really does ship a mechanism with tests —
but it proves too much: **every** hub-process lane ships a mechanism (N shipped a `verify.py`
change; a doctrine lane that shipped nothing would be a no-op), so "it shipped code" cannot be what
distinguishes the buckets or the `hub-introspection` bucket is empty by construction and the cap can
never bind. The distinguishing question the split actually asks is **whose surface does the work
change** — and O changes `.pre-commit-config.yaml`, the hub's own gate mesh, on the hub's own commit
path. That is the same surface class as N. *Unblocks:* the cap gets its first real adjudication
rather than a second clearance-by-attrition, and the split gains a worked example of the boundary
that future dispatches can cite.

> **The counter-argument, stated fairly because the architect may prefer it:** `[#527]` is a
> *product* of the methodology (a gate other repos will install via the plugin), not an
> *introspection* of it, and the cap exists — per PLAYBOOK — *"because methodology work is the class
> that expands to fill whatever width is available."* `[#527]` did not expand; it was a bounded
> S-sized row with a three-leg Done-when, closed in one lane. If the cap's *purpose* is the test,
> O passes it. **This reading is coherent and would put the roster within cap.** What it costs is
> that the bucket boundary then runs on intent rather than surface, which is much harder to declare
> ex-ante — and ex-ante declaration is the mechanism G-8 chose.

### D10 — what D9 implies for the **phase-2 roster**

Under D9, phase-2's roster is constrained *before* it is drafted:

| Dispatched width | `hub-introspection` lanes permitted |
|---|---|
| 4–7 | **1** |
| 8–11 | **2** |

- **Known phase-2 hub-process candidates already exceed one:** the W1 `CLAUDE.md` §5 edit (§4),
  the W2 PLAYBOOK re-point (§7), `[#428]` leg 1's dead-producer detector (§2), and `[#277]`'s
  detector repair (§1) are all hub surfaces. At any width below 8, **at most one may be a lane** —
  the rest must ride as drive-bys inside non-hub lanes, or wait.
- **Two of them are one-line doc edits** (W1, W2) and are the natural drive-by candidates under the
  I-D8 precedent (*"a drive-by fix scheduled in W-n, birthing no row"*). That is the cheapest way
  to stay within cap without running narrower.
- **If phase-2 wants both `[#277]` and `[#428]` leg 1 as real lanes, it must dispatch at width ≥8**
  — and PLAYBOOK requires that a batch which cannot fill its non-process lanes **reports the
  shortfall and runs narrower** rather than backfilling with process lanes. So width 8 has to be
  justified by four real feature/finish-line lanes existing, not by wanting two hub slots.

---

## §6 · Wave-2 drift check — the 29 conversion drafts on `main` — item 6

**Method.** The drafts landed via lane S at `6516f6e2` (blob `4c3481a8`), which is the
**four-ruled-edits amendment** of the original `8df3be88`, not the original. Every verdict below is
against the *landed* text. For each target row: (a) is it still open, (b) did its `tasks/` file
change since the draft was authored (2026-08-14), (c) did phase-1 touch any file the draft cites.

**Result — the wave is clean.**

```
target rows still open              30 / 30   (29 drafts + the [#419] re-check)
target rows changed since drafting   1 / 30   ([#364] — and it was already withdrawn by lane S)
phase-1 tasks/ edits hitting a draft target      0
lane R's six drained rows hitting a draft target 0
```

- **R's drain does not collide.** R drained `#344 #423 #430 #415 #487 #428`; the 29 draft targets
  are `82 130 145 146 210 239 263 266 271 274 285 324 350 351 361 385 391 393 409 410 411 412 417
  438 443 484 491 502` + `[#419]`. **Intersection: empty.**
- **Phase-1's `tasks/` footprint** was `293 344 415 423 428 430 487 528 529 530` — also disjoint
  from the 29.
- **The four ambiguity forks were already resolved by the morning adjudication, upstream of
  phase-1** — three of lane S's four ruled edits *are* those resolutions:

| Fork | Resolution already landed in the draft on `main` | Live re-verification |
|---|---|---|
| 5.1 `[#364]` | **Withdrawn** — *"obsoleted 2026-08-15, premise discharged by the 1320 threshold (Y-2)"* | `status: retired`; `#353` is **not** a `doc_rot` locus (7 loci live, `#353` absent) — premise genuinely gone |
| 5.2 `[#391]` | Branch (b) **deleted**; draft now requires the nightly wiring outright | `[#384]` still closed (no task file) — the dead disjunct was correctly removed |
| 5.3 `[#417]` | **Remainder clause added** (D6.4(b)) — carries the unlanded `audit.py:2625-2633` extraction | `_is_lane_owned_daily` at `:402`, `check_dirty_tree` at `:412`, test at `:758` — the landed half still landed; `audit.py` untouched by phase-1, so the remainder still stands |
| 5.4 `[#502]` | Left as drafted (report-only framing kept) | `[#501]` closed, wall live at 16,640 bytes — premise holds |

- **Every other cited premise re-verified live and holds:** `[#285]` — PLAYBOOK still carries prose
  `Last updated` and **no** `last_reviewed` frontmatter, and is still absent from
  `_HUB_ONLY_FRESHNESS_FILES` (`audit.py:294`); `[#263]` — `mermaid_theme_directive` still at
  `doc-code-edge.yaml:115`, exactly as drafted; `[#412]` — `ROUTING.md` still absent, so the
  draft's redirect to PLAYBOOK is still the right call.

### D11 — **ratify all 29 as CURRENT.** Stale drafts: **0**

*Rationale:* the drafts were written to name **sections and keys rather than line numbers**
precisely to survive edits like N's — and that design held: N inserted 79 lines into PLAYBOOK at
L824 and not one draft clause moved. *Unblocks:* the wave can be applied as one act; no re-draft
round is owed.

> **One provenance-note correction, which is *not* a stale draft and should not be counted as one.**
> The `[#146]` entry's **Intent** note says *"the de-hardcode paragraph now sits at
> `PLAYBOOK:1032`"*. Post-phase-1 it sits at **`PLAYBOOK:1105`** — N's `+79/-0` hunk at L824 moved
> it by exactly the delta. **The draft clause itself is unaffected** (it names the
> `amendment_coherence` honest-limits *section*, deliberately), so the wave is not stale — but the
> note is now wrong, and it is wrong in a document whose whole thesis is *"a clause pinned to a line
> number re-rots on the next edit."* Correct the note when the wave is applied; it is the wave's own
> lesson demonstrating itself inside twenty-four hours.

---

## §7 · W2 and `[#528]` leg 3 — what closes now that `[#529]` emits — item 7

### D12 — W2 (the PLAYBOOK re-point) is **unblocked, independent of telemetry, and TIME-CRITICAL**

**Evidence.** Both citations are still stale, verbatim on `main`:

```
PLAYBOOK.md:844   ... commit `8387ff2a` §1–§3 — a draft on the unmerged branch
                      `claude/night2-latency-audit-6s1k6p` ...
PLAYBOOK.md:866   ... commit `757077f2` §2.2–§2.6 (a draft on the unmerged branch
                      `claude/night2-research-d30vhu`).
```

Both audits landed on `main` at merge `7d1f6ce0` (R5), so *"unmerged branch"* is false today.

**The part that makes this urgent rather than cosmetic — and it is not in the packet:**

```
git ls-remote --heads origin  ->  refs/heads/main
                                  refs/heads/automation/fleet-audit
git cat-file -t 8387ff2a      ->  fatal: Not a valid object name
git cat-file -t 757077f2      ->  fatal: Not a valid object name
```

**Origin carries neither night-2 branch.** Those SHAs exist only in the operator's local clone. The
moment the teardown in D14 runs, `PLAYBOOK.md` — a canonical doctrine surface — permanently cites
two commit hashes that no clone on earth can resolve. `757077f2` is worse than stale: the packet
records that the *landed* research content is `413bbd60` (`+24/−0` over the cited SHA), so the
citation names neither the branch state nor the landed state.

**Proposed verdict — re-point both lines to the landed `main` blobs BEFORE any branch deletion,
and treat the ordering as a hard dependency of D14.** *Rationale:* this is a two-line doc edit with
no build, no telemetry dependency and no ruling in its way — and its cost goes from *trivial* to
*unrecoverable* the moment teardown runs. *Unblocks:* `[#528]` leg 3's **doc half** closes; the
teardown in D14 becomes safe on the last surface still pointing into those branches.

### D13 — `[#528]` leg 3's **telemetry half stays BLOCKED.** The brief's premise "now that `[#529]` emits" is only half true

**Evidence.** `[#528]` leg 3: *"emit `test_run` duration via the telemetry leg … so the trend is
measured, not felt."* `[#529]`'s landed state, from its own row:

> **INTEGRATION 2026-08-15 (R7) — merged `4ad2025d`, LIBRARY ONLY (zero call sites), 30 tests
> green; STAYS OPEN on 4 legs:** (1) wire the call sites (phase 3); (2) `.gitignore`
> `logs/TELEMETRY.db` — else the first live emit dirties `git status` and trips session-end
> backpressure; (3) decide `structlog` — absent from `[dependency-groups]`/`uv.lock`, so it
> silently falls back to stdlib logging; (4) last two Done-when legs are phase-3.

`[#529]` **can** emit; nothing **calls** it. So no `test_run` event can land, and leg 3's telemetry
clause has no path to satisfaction until `[#529]` leg 1 (phase-3 wiring) is built.

**Proposed verdict — split leg 3 explicitly: the doc re-point (D12) closes now; the telemetry
clause is re-pegged behind `[#529]` phase-3 and named as such on the row.** *Rationale:* leg 3 today
bundles a two-line doc fix with a blocked build, so the row cannot report honest progress on either
— and `[#528]` is a P1. *Unblocks:* `[#528]` gets a truthful state (one leg closed, one blocked on a
named row) instead of one opaque blocked leg, and `[#529]`'s phase-3 gains a declared consumer.

> **Two phase-3 traps already recorded, worth carrying into whatever dispatches it:** `[#529]` leg 2
> — the first live emit writes `logs/TELEMETRY.db` into a dirty `git status` and **trips
> session-end backpressure**, so the `.gitignore` entry must land *before* the first call site, not
> with it. And the terra P1 — `default_db_path()` resolves `_REPO_ROOT` (`:110,275`), which **in a
> linked worktree resolves to the worktree**, so a batch running telemetry from lanes would scatter
> N databases. Fix per `fleet_analytics.py:1076`. Both are on the row; neither is built.

### D14 — teardown: **all 8 night-2 branches are now SUPERSEDED-DELETE.** The packet's table is superseded

**Evidence.** The phase-1 packet §4 measured **3 SUPERSEDED-DELETE / 5 UNIQUE-HOLD** and warned:
*"Rows 4–8 are sole copies. Do not delete them without landing their artifacts first."* That
condition has since been met — **after** the packet, at `ed3abe9f`:

> *"land the 5 night-2 UNIQUE-HOLD artifacts — dissolves the teardown trap … landing them flips all
> eight `claude/night2-*` branches to SUPERSEDED-DELETE and the teardown trap disappears."*

Byte-faithfulness was proven per file (staged blob vs source blob) before that commit.

**Proposed verdict — the 5 UNIQUE-HOLD branches are now safe to delete; teardown of all 8 is
ratifiable as one act — SUBJECT TO D12 LANDING FIRST.** *Rationale:* the only thing still reaching
into two of those branches is `PLAYBOOK.md` L844/L866, and origin does not carry them, so the doc
re-point is the last dependency. *Unblocks:* `/lane-integrate` checklist item 3 (currently *"open by
construction"*, 8 worktrees registered) can finally close, and the phase-1 batch stops carrying an
open teardown.

---

## §8 · Honest limits of this queue

- **Everything here is a proposal.** No BACKLOG row was edited, no Issue closed, no branch deleted,
  no `CLAUDE.md` line changed. The two diffs in §4 are drafts for the architect to paste, not
  applied work.
- **The `/review-closures` surface was regenerated, not observed as the operator left it.** The
  operator's own surface (153) is 8 rows narrower for window reasons (§1.0). If the exact 153-row
  set matters — it does not for D1–D3, which are class verdicts — it must be re-derived on the
  operator's clone.
- **§0's three artifacts mean this lane cannot confirm the repo is green.** It can only confirm that
  the phase-1 packet's `health: OK` is *not contradicted* by anything reproducible here.
- **D9 is a reading, not a derivation.** The G-8 split does not define its boundary in terms of
  surface-vs-intent; D9 argues the surface reading is the only one under which the bucket is
  non-empty, but the counter-argument is stated in full because it is genuinely available.
- **§2's dismissals are verified against the tree, not against the digests.** The nightly digests
  themselves live on the `automation/conformance-digest` branch, which this clone does not carry;
  each finding was re-derived from the Issue body against live files instead.
- **`[#419]`'s re-check is counted as a draft, not adjudicated.** It is one of the 30 and its row is
  unchanged, but its substance (routines with no consumer) overlaps `[#428]` and `[#426]`, and this
  lane did not attempt that untangling.

---

**Decisions queued 14, batch-ratifiable 5, stale drafts 0.**

<!--
  batch-ratifiable = a decision covering >=2 items that the architect can ratify with one word,
  with no per-item reading required: D1 (2 STRONG) · D2 (159 WEAK) · D4 (15 Issues) ·
  D11 (29 drafts) · D14 (8 branches).  The remaining 9 (D3, D5, D6, D7, D8, D9, D10, D12, D13)
  each need an individual word.
  stale drafts = 0 of 29; the [#146] line-number provenance note is a note-level correction
  carried inside D11, not a stale clause, and [#364] was withdrawn by lane S before landing.
-->
