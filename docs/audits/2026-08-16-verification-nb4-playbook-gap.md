---
title: "NB4-C — PLAYBOOK coverage matrix for the batch-4→6 mechanism set (DRAFT)"
date: 2026-08-16
class: verification
---

# NB4-C — PLAYBOOK coverage matrix for the batch-4→6 mechanism set

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** `nb4-playbook-gap`
- **Status:** **DRAFT — REPORT ONLY.** Nothing here is a ruling. No BACKLOG row, `tasks/` body,
  register entry, ADR, manifest or protocol file was touched to produce it. The §3 drafts are
  candidate text for the architect to rule on, not adopted text.
- **Lane:** `dk · nb4-C · playbook-gap`, read-only. **Branch `claude/nb4-playbook-gap-coverage-1ktsuc`**
  — the brief names `claude/nb4-playbook-gap`; the dispatched session was provisioned with the
  suffixed form and that is the branch this file lands on. Both are the sanctioned `claude/<slug>`
  machine-produced lane shape (CLAUDE.md §4), so the difference is the provisioning suffix and
  nothing else. Recorded rather than silently reconciled.
- **Base read:** `HEAD` = `d137cc6a` (2026-08-16 11:49 +0200) — the merge of `chore/phase2-position0`,
  i.e. after the seven Position-0 acts and the batch-6 manifest, before the twelve lanes are dispatched.
- **Instrument:** `protocols/PLAYBOOK.md` @ 4628 lines read directly; the batch 4/5/6 artifacts under
  `docs/audits/`; `scripts/{batch_manifest,validate_hermetization,silent_rule_detector,single_flight}.py`
  and `scripts/audit.py`; `JOURNAL.md` entries `2026-08-15 (c)/(d)` and `2026-08-16 (a)/(b)`. Every
  number below is measured on this tree unless marked INHERITED.

---

## §0 · The answer first

```
TALLY      covered 1 / partial 6 / absent 6   (of the 13 rows the brief enumerates)

COVERED    tiered suite

PARTIAL    batch manifest at dispatch . lane grammar + ADR-110 exemption . night-batch law
           consolidation briefings . board rules . codex tally artifacts

ABSENT     single-flight guard . land-then-delete teardown . decision-queue adjudication
           integrator-on-a-clock . honest-RED clause . Position-0 shape

SHAPE      The gap is not random. Every ABSENT row is a mechanism born in the last EIGHT DAYS
           (2026-08-08 .. 2026-08-16) and every PARTIAL row is an older section whose machine
           contract moved underneath it. The PLAYBOOK is current on DOCTRINE and behind on
           the MACHINE the doctrine now runs on.

WORST      Two rows are actively costing work rather than merely being silent:
           - lane grammar: 3 consecutive batches damaged (b4 dropped 2 lanes, b5 forfeited
             the exemption on 2 of 7, b6 had to verify 12 names by hand against the regex)
           - codex tally: the documented format FAILS the live parser on 2 of 4 legs, so an
             artifact written from PLAYBOOK lands in the check's `untallied` list

ARC        ONE amendment arc, 12 acts, 3 target chapters (Ch8 x7, Ch11 x3, section 5 x1,
           Ch10 x1). Measured ratchet cost of all 12 drafts: +0 tokens (headroom is 1).
```

---

## §1 · Method — what the three verdicts mean, and why the bar is what it is

The column verdicts are graded against the repo's **own** sufficiency standard, not against
"does a section exist". ADR-81 leg (a), quoted from Ch12 (`PLAYBOOK.md:2434`):

> a methodology home — its rule/doctrine written in PLAYBOOK **sufficiently for a fresh session to
> act on it from that section alone** (existence ≠ sufficiency).

So:

- **COVERED** — a fresh seat can run the mechanism from the cited section alone. No leg of the live
  mechanism has to be recovered from code, from a lane contract, or from an off-repo pack.
- **PARTIAL** — a section exists and is correct as far as it goes, and at least one named leg of the
  live mechanism is recoverable only outside it. Each PARTIAL row states its missing legs explicitly;
  a PARTIAL verdict with no named missing leg would be an opinion.
- **ABSENT** — no section carries the mechanism. Where a neighbouring section names the mechanism's
  *absence* (Ch11 does this for the morning ratification surface), the locator records that and the
  verdict stays ABSENT: naming an organ as missing is the opposite of documenting it.

**Why this bar and not a softer one.** The operator's doctrine for this pass is that the PLAYBOOK
carries the whole live methodology. Under a "a section exists" bar, rows 1, 2, 6, 10 and 11 all read
COVERED and the report says the corpus is fine — while the batch-6 manifest is on disk having had to
derive two mechanical facts against the parser because the doctrine did not state them, and four codex
artifacts landed this morning "authored against the parser regexes rather than against prose intent"
(`JOURNAL.md` 2026-08-16 (b), verbatim). Those two events are the evidence that the softer bar reports
green about a corpus that is costing lanes time.

**Scope limit, stated up front.** The row set is exactly the 13 shapes the brief enumerates, so the
final tally is checkable against the brief. Shapes witnessed in batches 4–6 that the brief did not name
are listed in §5 **without verdicts** and are outside the tally.

---

## §2 · The coverage matrix

### 2.1 · One-screen form

| # | Mechanism / routine / artifact shape | Verdict | PLAYBOOK locator |
|---|---|---|---|
| 1 | Batch manifest committed at dispatch | **PARTIAL** | Ch8 `:1871-1884` |
| 2 | Lane grammar + ADR-110 exemption | **PARTIAL** | Ch8 `:1838-1843`, `:1874-1880`, `:1981-1986` |
| 3 | Single-flight dispatch guard | **ABSENT** | — |
| 4 | Night-batch law | **PARTIAL** | Ch11 `:2400-2428` |
| 5 | Land-then-delete teardown shape | **ABSENT** | — |
| 6 | Consolidation briefings | **PARTIAL** | Ch11 `:2409` (cardinality only) |
| 7 | Decision-queue adjudication | **ABSENT** | Ch11 `:2415` names the organ as MISSING |
| 8 | Tiered suite | **COVERED** | Ch5 `:827-890`, cross-ref Ch8 `:1866-1868` |
| 9 | Integrator-on-a-clock | **ABSENT** | — |
| 10 | Board rules 1–8 | **PARTIAL** | Ch8 `:1988-2040` |
| 11 | Codex tally artifacts | **PARTIAL** | §5 `:3560-3640`, Ch7 `:1224`, §16 |
| 12 | Honest-RED clause | **ABSENT** | — |
| 13 | Position-0 shape | **ABSENT** | — |

### 2.2 · Row detail

---

**Row 1 — Batch manifest committed at dispatch. PARTIAL.**

*Locator:* Ch8, refuse-to-finish checklist bullet 4, `PLAYBOOK.md:1871-1884`.

*Carried, and carried well:* the two-halves shape (manifest at dispatch, packet at close); why a plan
living only in chat prompts leaves a batch reconstructable from outcome but not intent; that the
manifest is load-bearing **at the gate** since the ADR-110 amendment 2026-08-07; the two frontmatter
fields `status: open` and `closed_by:`; and the reason expiry is packet-landing rather than a mutable
flag (`docs/audits/` is immutable, so a mutable `status:` would be no expiry at all).

*Missing legs — the machine contract:*

1. **The filename glob.** `batch_manifest.MANIFEST_GLOB` is `docs/audits/*-batch-*-manifest.md`,
   matched with `PurePosixPath.match` against the basename. A manifest whose name misses it opens
   nothing, silently.
2. **`batch:` is a digit.** `tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed`
   asserts `b.batch.isdigit()` against every live open manifest. Batch 3's manifest shipped a
   date-shaped value and **was RED from the moment it landed** — a live defect this leg would have
   prevented at authoring time.
3. **Every input resolves through `HEAD`, not the working tree.** The module's own header records two
   rejected earlier attempts (a working-tree glob; then `git ls-files`, which a merely *staged*
   addition satisfies). An author who assumes disk truth writes a manifest that appears to open a
   batch and does not.

*Evidence the section is insufficient rather than merely terse:* the batch-6 manifest carries a
section titled **"Two mechanical facts derived live against the parser, before writing"** covering
exactly legs 1 and 2. The author had to read the parser because the doctrine does not state them.

---

**Row 2 — Lane grammar + ADR-110 exemption. PARTIAL. The most expensive row in the matrix.**

*Locator:* Ch8 per-lane requirement 5 (`:1838-1843`), the exemption note inside checklist bullet 4
(`:1874-1880`), and Honest limits (`:1981-1986`).

*Carried:* one lane = one contract = one worktree = one branch; a pointer to
`scripts/validate_branch_naming.py`; that the exemption exists and is load-bearing at the gate; and —
correctly and valuably — that the enum is **advisory and wired into no gate at all**.

*Missing legs:*

1. **The grammar itself appears nowhere in the file.** `grep -n "worktree-lane-" protocols/PLAYBOOK.md`
   → **0 hits**. The live constant is
   `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$` (`validate_branch_naming.LANE_BRANCH_RE`,
   imported by `batch_manifest.is_lane_merge` as the single definition of the grammar). A seat naming
   twelve lanes from Ch8 alone has a pointer to a script and no shape.
2. **The exemption's two-condition predicate is not stated.** It requires a `--no-ff` merge of a branch
   matching the ratified grammar **AND** a committed manifest declaring an open batch — neither alone.
   Ch8 states the manifest half and omits the grammar half, which is precisely the half that has failed.
3. **The failure mode is not stated.** An off-grammar lane name does not error; it silently receives
   **no** exemption, surfacing as a `journal_spine_anchor` gate FAIL at the integrator's first merge —
   far from the authoring act that caused it.

*Three consecutive batches damaged, measured:*

```
batch 4   two lanes hit the class; resolved by DROPPING them from the roster
batch 5   worktree-lane-s-w20-draft-landing   REFUSED (`w20` is not \d+)
          worktree-lane-r-gateclose-drain8    REFUSED (no id slot)
          -> exemption silently forfeited on 2 of 7; hand-anchoring workaround; queue nearly wedged
batch 6   12 of 12 PASS, refused 0 -- achieved by running every name through the regex BY HAND
          before writing the manifest (batch-6 manifest, section "THE OFF-GRAMMAR HAZARD ...")
```

Batch 6's zero is a **checked** roster, not a gated one. `[#531]` (born at Position 0, dispatched to
lane y) is the provisioning-time gate; this row is the doctrine half, and the two are independent.

---

**Row 3 — Single-flight dispatch guard. ABSENT.**

*Locator:* none. `grep -ni "single-flight" protocols/PLAYBOOK.md` → **0 hits**.

*What is live:* `scripts/single_flight.py` + `tests/test_single_flight.py`, merged `50daad05` (batch 5,
lane P, `[#530]`). A git ref as a distributed compare-and-swap: claim `refs/locks/<contract-id>` on
`origin` via `git push --force-with-lease=<ref>: origin HEAD:<ref>`, plus a local
`git update-ref --stdin create` fast leg for same-clone contention. Exits 0 claimed / 3 in-flight /
2 internal; fails CLOSED.

*Why the doctrine matters more than the tool here:* the class it closes was **witnessed** —
2026-08-14, three executions of one contract live at once, two independently allocating the same four
ids, sharing neither tree nor machine. And the trap it avoids is counter-intuitive enough to be
re-invented wrongly: a plain `git push` of a lock ref exits **0** with `Everything up-to-date` when
both racers sit at the same commit, which is the normal batch-dispatch state. The lease is the
mechanism; a seat that reasons "push the ref, check the exit code" builds a guard that greenlights the
exact race.

*Honest limit to carry into any draft:* `[#530]` is merged with Done-when met and **is not closed** —
two OPEN legs remain (an ABA race in `release`; `rev-parse` conflation in `--local-only`), both latent
because the guard is wired to no hook.

---

**Row 4 — Night-batch law. PARTIAL.**

*Locator:* Ch11 "Night-batch work — the morning-loop wave from the night side", `:2400-2428`.

*Carried, and this is the strongest of the six PARTIALs:* the hard rule (nothing merges unattended);
branch-only lanes; UNVERIFIED-UNTIL-LOCAL; the three organs a night batch needs; the orchestration
shape (Opus orchestrates, Sonnet runs bounded probes, Haiku runs read-only fan-out, every git mutation
serial in the orchestrating thread); producer ≠ reviewer; one dated report per workstream with
`consumer` + `consumption_path`; branch isolation in a sanctioned lane shape; and the honest-limits
requirement.

*Missing legs:*

1. **The evidence count is stale.** `:2423` reads *"the first witnessed batch (2026-07-30→31, **n=1** —
   this shape has **not** cleared the n=2 evidence gate above, so it is a recorded practice, not yet a
   graduated standard)"*. Four night batches have now run: 2026-07-30→31, night-1 (2026-08-12),
   night-2 (2026-08-14), night-3 (2026-08-15). The section describes its own subject as un-graduated
   while the tree holds three further instances.
2. **The third organ is described as missing and is now built.** `:2415` — *"a MORNING RATIFICATION
   SURFACE — the consumer whose absence is the root of `[#419]`"*. Rows 6 and 7 below are that surface,
   landed twice.

*Consequence, stated plainly:* a fresh seat reading Ch11 today learns that night batches are an
unproven practice missing their consumer. Both halves of that are now false.

---

**Row 5 — Land-then-delete teardown shape. ABSENT.**

*Locator:* none. `grep -niE "UNIQUE-HOLD|byte-faithful|sole copy" protocols/PLAYBOOK.md` → 0 relevant hits.

*Adjacent coverage that does not cover it:* Ch8 `:1362` (verify-then-teardown; a worktree branch needs
the worktree removed first) and `.claude/rules/git-discipline.md` ("WORKTREE TEARDOWN IS TWO BRANCHES,
NOT ONE"). Both are about **refs**. The missing shape is about **artifacts**.

*The live shape, witnessed twice:*

```
1. VERDICT each branch:  SUPERSEDED-DELETE (its artifacts are on main)
                         UNIQUE-HOLD       (it is the SOLE COPY of an artifact)
2. LAND the UNIQUE-HOLD artifacts on main byte-faithfully, extracted with
   `git checkout <source-ref> -- <path>` -- which writes the SOURCE blob straight into
   the index, so the staged blob cannot differ from the source BY CONSTRUCTION
3. RE-VERDICT: every branch now reads SUPERSEDED-DELETE
4. DELETE, per-branch, only on a byte-coverage proof; a branch not byte-covered is HELD
```

*Instances:* night-2 UNIQUE-HOLD landing `ed3abe9f` (JOURNAL 2026-08-15 (d)) — teardown table v2 read
3 SUPERSEDED-DELETE / 5 UNIQUE-HOLD, and the packet's warning was explicit: *"Rows 4–8 are sole copies.
Do not delete them without landing their artifacts first."* Night-3 landing `addca403` (JOURNAL
2026-08-16 (a)) — five of five branches present, zero MISSING, nothing synthesized; the sessionplan blob
taken from the branch **tip** `6d4818c9` rather than its first commit, because the tip carried a §5a
amendment the author had already superseded.

*Why it is doctrine rather than a one-off:* the phase-1 packet's own teardown table was **falsified by
the re-verdict** — it had read "SUPERSEDED-DELETE across the board" while five branches still carried
artifacts nothing had landed (JOURNAL `:235-236`). A teardown that reads refs and not artifacts deletes
the only copy and reports a clean tree.

---

**Row 6 — Consolidation briefings. PARTIAL.**

*Locator:* Ch11 `:2409` — *"the morning is the operator plus ONE report"*. That is the output
**cardinality** and it is correct. It is the whole of the coverage.

*Missing leg — the shape.* `docs/audits/2026-08-15-technical-night2-consolidated-briefing.md` (1850
lines) is the built artifact, and it is six-part:

```
section 0   STATE + CONTRADICTION LEDGER  -- executive state in three lines; an 18-entry
            contradiction ledger; a COLLISIONS block "recorded here so they are not lost"
section 1   DECISION QUEUE                -- D1..D6, one recommended verdict each (row 7)
section 2   NECESSARY CONDITIONS          -- session preconditions
section 3   FUNCTIONAL REQUIREMENTS       -- per-lane objective functions for the next wave
section 4   PARALLEL EXECUTION PLAN       -- proposed roster
section 5   PROVENANCE APPENDIX           -- per-source-lane (NB2-A..NB2-G) attribution
```

The contradiction ledger and the provenance appendix are the two parts that carry the consolidation's
value: N independent night lanes disagree, and a briefing that silently picks a winner destroys the
disagreement that is the fan-out's actual product.

---

**Row 7 — Decision-queue adjudication. ABSENT.**

*Locator:* Ch11 `:2415` names the organ **as missing** (*"the consumer whose absence is the root of
`[#419]`"*). No section describes the built shape. `grep -ni "decision queue" protocols/PLAYBOOK.md`
→ 0 hits.

*The live shape:* `docs/audits/2026-08-15-technical-night3-decision-queue.md` — *"the architect's
morning decision queue (DRAFT)"*, 546 lines, and its properties are the doctrine:

- Every item is **D-numbered** (D1..D14) and carries **evidence, then a proposed verdict**, phrased as
  a verdict the architect ratifies or overturns — a queue of proposals, not a queue of questions.
- It opens with **§0 measurement caveats — read before trusting any number here**, and closes with
  **§8 honest limits of this queue**.
- Items are **ordered preconditions-first**: the night-3 sessionplan §3 marks four items (A1–A4) as
  phase-2 preconditions to be taken first *"because everything after them is dispatchable"*.
- Class dismissals are permitted and are stated as such — D2 dismisses 159 WEAK proposals **as a class,
  with no per-row reading**, which is what makes a one-hour adjudication of a 161-item surface possible.
- The queue is **timeboxed** (the adjudication hour) and its output is a ruling record, not an edit.

*Why ABSENT and not PARTIAL:* Ch11's line is a gap statement. A seat that reads it learns the organ is
owed, not how to build or run one.

---

**Row 8 — Tiered suite. COVERED. The only COVERED row.**

*Locator:* Ch5 `#### Tiered suite — targeted in-lane, one full suite at integration`, `:827-890`;
cross-referenced from the Ch8 refuse-to-finish checklist at `:1866-1868`.

*Carried:* the A/B split and its reason (per-lane greens are evidence about each lane in isolation; the
merged tree is a state no lane exercised); the measured basis (host 918.9 s; 701.6 s serial vs 473.0 s
at `-n auto` on a 4-core container, 1.48×, outcome sets identical both ways); the five-file exclusion
set with a per-file reason; the oracle-tier rule (*tier A plus anything covering the touched module*)
and its `[#278]` successor; two honest limits (the `slow` marker does not express this split; deferring
the oracle tier defers real signal); and the five-rung xdist settings ladder including
`--max-worker-restart=0`, `--maxprocesses`, `-n 0` under a forking parent, and `--dist worksteal` as
the balanced-remainder default (`:882-883`).

*Cross-check against the live call site:* `/lane-integrate` now carries
`--dist worksteal --max-worker-restart=0` (landed `06b3dcda` at Position 0). Both flags are in the Ch5
ladder. The law and the runbook agree; no gap.

---

**Row 9 — Integrator-on-a-clock. ABSENT.**

*Locator:* none. Ch8 carries dispatch, lane protocol and the refuse-to-finish checklist, and contains
no scheduling clause for the integrator.

*The finding, measured twice at two widths:*

```
phase-1 wall clock by owner (commit timestamps, night-3 sessionplan section 2.2):
  lane work (7-way parallel)   1h15m   22%
  integrator serial tail       3h56m   70%   = idle 1h29 + queue 0h55 + close-out 1h32
  dispatch                     0h12m    4%
  the full test suite          0h24m    7%   (inside close-out)

the cheapest cut: the 1h29m IDLE PROLOGUE -- 27% of the window, costing nothing to remove.
lanes finished 17:52; the integrator's first act was 19:21.
```

*The rule it yields:* the integrator boots on a clock (dispatch + ~75 min) rather than on lane
completion. Corroborated across two batches, two widths and two lane mixes — `[NB2-B]` §4a named the
same term from the W4 wave (*"the dominant latency term was waiting for an integrator, not running
tests"*), and phase-1 is the second measurement that finding was missing.

*The counter-lever, worth carrying with it so it is not chased:* the suite is **7%** of the window.
`[#528]` legs 1+2 landed the xdist flags and the tiered-suite law; a further suite optimisation aims at
the seventh cheapest minute.

*One honest caveat the source states about itself:* if the packet's session-jsonl mtimes (`18:0x`) are
the true dispatch rather than the step-0 contract commits (`16:36`–`16:49`), the idle prologue shrinks
toward zero and the lever moves from *idle* to *queue + close-out* — leaving the conclusion
(**the integrator's serial tail owns the wall clock, not the suite**) unchanged. A draft that carries
the conclusion travels; one that carries only the 1h29m number does not.

---

**Row 10 — Board rules 1–8. PARTIAL.**

*Locator:* Ch8 "Dispatch visibility — Agent View shows DISPATCHED sessions only (STANDING_RULINGS B7)",
`:1988-2040`.

*Carried:* VISIBLE = DISPATCHED and why (a foreground session sits outside Agent View by construction,
verified live 2026-08-06); the `--bg` convention and that batch lanes take it without exception; the
board-label shape `[repo · #id-or-slug · verb-object]` and its two carriers (`.claude/commands/lane-boot.md`,
`templates/prompt-template.md`); flag composition against the installed CLI; **AM-5** (a nested session
carries no row, so dispatch is an operator act from a terminal); and the scoping of the agent-view
dispatch input to ad-hoc read-only default-model tasks.

*Missing legs:*

1. **The enumerated set 1–8 has no in-repo carrier.** The brief names "board rules 1-8" as a numbered
   set; the tree carries no such enumeration. `grep -niI "board" --include=*.md .` returns the
   board-*label* convention across PLAYBOOK / HANDOFF_PROCESS / STANDING_RULINGS / prompt-template, and
   nothing that enumerates eight rules. The set is off-repo (the operator's pack). **This report cannot
   verdict the individual rules 1–8 and does not pretend to** — see §6 limit 1.
2. **The teardown-ordering rule lives only in handoff bundles.** *"Teardown after merge: close the
   holding session on the Agents board FIRST (locks name live pids), then worktree remove + prune +
   branch -d"* appears at `docs/handoffs/2026-08-14-dev-knowledge-architect/PASTE_THIS.md:531` and
   `SUPPLEMENT.md:61`. Handoff bundles are immutable per-session artifacts; a rule whose only home is a
   dated bundle is invisible to the next seat, which boots on a *different* bundle.

---

**Row 11 — Codex tally artifacts. PARTIAL — and the documented format fails the live parser.**

*Locators:* §5 "Codex review archival protocol" `:3560-3640` (stamped `version: 1.0 — 2026-04-25`);
Ch7 `:1224` (the refuted-finding tally posture); §16 (the codex-utilization lane doctrine).

*Carried, and still correct:* the archival trigger/skip lists; the target path
`{repo}/docs/audits/YYYY-MM-DD-codex-{slug}.md`; the cross-linking discipline; and — the strongest
clause in the row — *"a refuted finding is kept, not deleted"*, with the tally excluding it and the body
retaining it plus the refuting commands.

*The divergence, measured against the live regexes in `scripts/audit.py:4108-4122`:*

```
check_review_artifact_coverage parses          PLAYBOOK section 5 "Format" prescribes
  ^# Codex Review\b                    OK        # Codex Review — {topic}
  ^\*\*Branch:\*\*                     OK        **Branch:** {branch-name}
  ^\*\*HEAD:\*\* <7-40 hex>            MISS      **Commit (HEAD at review):** {short SHA}
  ^\*\*Tally:\*\* N/N/N/N              MISS      ## Severity breakdown  (a markdown table)

run live against the documented format block:
  title True . branch True . head False . tally False
```

*What that costs.* An artifact authored from the PLAYBOOK is **recognized** (title + Branch), so it
enters the artifact list — and then reads `tally: False`, landing it in the check's `untallied` output.
It also carries no HEAD leg, so it links only by branch name in the merge subject and cannot cover a
review whose branch was later renamed.

*Live evidence this is not theoretical:* the four artifacts landed at Position 0 (`d6648d6`) took
`review_artifact_coverage` from 6 unlinked to 2, and the JOURNAL records how — *"authored against the
parser regexes rather than against prose intent"* (2026-08-16 (b)). The author reconciled to the code
because the doctrine would have produced an artifact the gate discounts.

*Also missing:* the tally's own **field order** (`Critical/High/Medium/Low`, carried as an HTML comment
on the line) and the **transcription posture** those four artifacts used — a review captured off-repo
and landed later states that it is a transcription, states the date the review ran versus the date the
file landed, and re-derives no verdict.

---

**Row 12 — Honest-RED clause. ABSENT.**

*Locator:* none. `grep -niE "honest-RED|honest RED" protocols/PLAYBOOK.md` → 0 hits.

*Adjacent clauses that are not it:* Ch8 `:1360` (a phantom RED from racing a suite against a commit in
one tree — a *sequencing* rule); Ch12 `:2471` (the vacuous-zero negative control — a *measurement* rule);
Ch2 `:763` (*"a rule that can't go red is decoration"* — a *design* rule). Three good clauses about RED,
none of which tells an integrator what to do with one.

*The live clause,* batch-6 manifest closure contract item 4:

> **honest-RED is in force**: the only tolerated RED is the one known pre-existing `routine_consumers`
> live pin, which lane l may FIX — in which case 0 RED is the expectation. Any other RED means `main`
> is NOT pushed and the packet attributes the failure.

*And its enabling half,* which is the part most at risk of being dropped — the manifest declares the
**baseline** at dispatch, so a later reading is attributable:

> Known carried WARNs at baseline, so they are not later mistaken for queue damage: `doc_rot` 9 loci
> … `review_artifact_coverage` 2 unlinked (both dispositioned) + 1 untallied; `undeclared_edges` 20;
> `preflight_backlog_ids` 1.

*Worked instance the same day:* JOURNAL 2026-08-16 (b) carries a paragraph headed **"Honest-RED,
recorded not suppressed"** — `doc_rot` went 7 → 9 loci, the two new WARNs being the two rows the arc
births, *"the defect `[#532]` exists to fix, demonstrating itself on arrival. Neither row was trimmed to
duck an undeclared threshold."*

---

**Row 13 — Position-0 shape. ABSENT.**

*Locator:* none. `grep -niE "Position 0|Position-0" protocols/PLAYBOOK.md` → 0 hits. Ch8 covers dispatch
and the batch protocol from the lanes onward; nothing covers the sequential head that precedes it.

*Proposed twice, executed once, and the executed form is the definition:*

- **Proposed** — night-3 sessionplan §3, *"Position 0 — before anything else (≈10 min, and it is not
  optional)"*: push `main`; tear down the previous batch's worktrees (two branches each); re-verdict and
  prune the night branches.
- **Executed** — `chore/phase2-position0`, seven acts, one commit per act, full gate stack on every
  commit, no `--no-verify` and no `SKIP=` anywhere, merged `--no-ff` to `main` **before a single lane
  session was dispatched** (JOURNAL 2026-08-16 (b); anchors `03a1c1ff` `cce0d644` `06b3dcda` `d6648d61`
  `e6ee9a15` `e123947c` `cd5cd32d`).

*The five properties that make it a shape rather than a to-do list:*

1. **`origin/main` carries the tip the lanes branch from.** Phase-1's `origin/main` was **59 commits
   behind**; a cloud-provisioned lane would have booted into a tree with no drafts artifact and no closed
   batch. The sessionplan's own words: *"the one item that silently produces seven wrong lanes rather
   than one loud failure."*
2. **Row births happen here, not mid-wave.** Every birth needs a `kill-candidates:` line
   (`backlog-filing-backpressure`) and mints churn in `BACKLOG.md` / `tasks/manifest.json` — the exact
   generated files every lane regenerates at merge.
3. **The previous batch's teardown completes here.** Mid-queue teardown while N lanes hold refs is how a
   merge loses its base; after close is fine, during is not.
4. **The manifest commits here**, which is what makes row 1's "at dispatch" true rather than aspirational.
5. **One commit per act**, so each act is independently anchored and revertible, and the arc reaches
   `main` as a single `--no-ff` merge.

*A property worth carrying explicitly:* the executed arc recorded a **defect its own re-read found and
deliberately did not sweep in** — `CLAUDE.md` §3 line 49 duplicates the §5 rule 4 claim the act was
scoped to fix, and was filed rather than widened. Position 0 is a sequence of *scoped* acts; the scope
discipline is the thing that keeps it ten minutes instead of a second session.

---

## §3 · The candidate PLAYBOOK amendment arc

**One arc. Twelve acts. Three target chapters plus one section.** Ordered so that same-chapter acts are
contiguous, which keeps the diff reviewable and lets the architect drop any act without disturbing the
rest. Every draft below is **paste-ready**: declarative phrasing, `<!-- scope: -->` tag where the
surrounding section carries one, and **zero** `must` / `shall` / `never` tokens (measured — §4).

**Suggested arc name:** `docs/playbook-batch46-mechanisms`.

---

### Act 1 — Ch8, row 1. Append after `:1884` (end of refuse-to-finish bullet 4).

```markdown
**The manifest's machine contract, so it is checkable while it is being written (batch-3 and
batch-6 evidence).** Three properties decide whether a committed manifest actually opens a batch,
and all three are read by `scripts/batch_manifest.py`:

- **Filename** — `MANIFEST_GLOB` is `docs/audits/*-batch-*-manifest.md`, matched with
  `PurePosixPath.match` against the basename. A manifest outside that glob opens nothing, silently.
- **`batch:` is a digit.** `tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed`
  asserts `b.batch.isdigit()` against every live open manifest. Batch 3 shipped a date-shaped value
  and was RED from the moment it landed.
- **Every input resolves through `HEAD`.** The manifest list, the manifest content, and the closing
  packet's absence are all read with git plumbing against the committed tree. Two earlier
  implementations read the working tree and `git ls-files` respectively; a staged-only addition
  satisfies the second, so a staged manifest declared a batch open. The rule says COMMITTED, and a
  HEAD-based read is what makes it mean that.

A manifest carrying no `closed_by:` opens nothing at all, because an exemption with no declared
expiry is a permanent hole. Checking these three at authoring time costs one `python -c` line;
discovering them costs the batch its exemption.
```

---

### Act 2 — Ch8, row 2. Replace per-lane requirement 5 at `:1838-1843`.

```markdown
5. **A worktree name paired 1:1 with its prompt file, on the ratified grammar.** One lane = one
   contract file = one worktree = one branch, so an open worktree resolves to the contract that
   created it and an orphan is attributable at a glance. The grammar is
   `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$` — `validate_branch_naming.LANE_BRANCH_RE`,
   which `batch_manifest.is_lane_merge` imports as the single definition in the repo. The `<id>` slot
   takes `\d+`, so a lane carrying no single row id is named from one of its own ids rather than from
   a topic word.

   **An off-grammar name does not error — it silently forfeits the ADR-110 exemption.** That
   exemption has two conditions and takes both: a `--no-ff` merge of a branch matching the grammar,
   AND a committed manifest declaring an open batch. Condition 1 alone would exempt any lane merge
   forever; condition 2 alone would amnesty every merge landed during a batch, the integrator's own
   included. A name that misses condition 1 surfaces as a `journal_spine_anchor` gate FAIL at the
   integrator's first merge — far from the authoring act that caused it, and the direction is
   deliberately the safe one (a missing exemption is loud; a spurious one is a hole).

   Three consecutive batches paid for this: batch 4 dropped two lanes from its roster, batch 5
   forfeited the exemption on two of seven and hand-anchored around it, and batch 6 reached
   twelve-of-twelve by running every name through the regex by hand before writing the manifest.
   A conforming roster is a checked roster, not a gated one — the grammar is enforced at no
   provisioning point, which is `[#531]`.
```

---

### Act 3 — Ch8, row 13. New subsection, insert before `### Dispatch visibility` at `:1988`.

```markdown
### Position 0 — the sequential head a batch dispatches from
<!-- scope: meta -->

A batch has a head that runs **before** any lane exists: one branch, one commit per act, merged
`--no-ff` to `main`, and only then are the lane sessions dispatched. It is ten minutes of sequential
work whose whole value is that it happens while the tree still has one writer.

**What lands here, and why each item resists being moved later:**

1. **`main` is pushed.** A cloud-provisioned lane branches from `origin/main`, so an unpushed tip
   produces N lanes booted into a tree missing the artifacts they were contracted against. Phase-1
   left `origin/main` 59 commits behind — the class that produces seven quietly wrong lanes rather
   than one loud failure.
2. **The previous batch's teardown completes.** Mid-queue teardown while N lanes hold refs is how a
   merge loses its base. Before dispatch is the good window; after close is acceptable; during the
   queue is the one timing that is actively bad.
3. **Row births happen here.** A birth needs a `kill-candidates:` line
   (`backlog-filing-backpressure`) and mints churn in `BACKLOG.md` and `tasks/manifest.json` —
   precisely the generated files every lane regenerates at merge.
4. **The batch manifest commits here**, which is what makes "committed at dispatch" a fact rather
   than an intention: at the moment it is written, none of the lane branches exists, so its roster
   declares INTENT and says so.
5. **The baseline is stated here** — gate readings, carried WARNs, `git worktree list`,
   `git stash list` — so a later reading is attributable to the queue rather than inherited.

**Each act is scoped, and a defect the act's own re-read finds outside its scope is filed rather
than swept in.** Position 0 stays ten minutes because its acts stay narrow; widening one silently is
how it becomes a second session. Worked instance: the phase-2 head re-scoped `CLAUDE.md` §5 rule 4 as
its own act with its own full-file re-read, found a duplicate of the same claim at §3, and recorded
it for the next window rather than editing beyond the ruled scope.
```

---

### Act 4 — Ch8, row 9. New subsection, insert after Act 3.

```markdown
### The integrator boots on a clock, not on lane completion
<!-- scope: meta -->

**The serial tail owns a batch's wall clock; the suite does not.** Measured on phase-1 from commit
timestamps at width 7:

| owner | span | share |
|---|---|---|
| lane work (7-way parallel) | 1h15m | 22% |
| **integrator serial tail** | **3h56m** | **70%** — idle 1h29 + queue 0h55 + close-out 1h32 |
| dispatch | 0h12m | 4% |
| the full test suite (inside close-out) | 0h24m | 7% |

The cheapest cut inside the tail is the **idle prologue**: 1h29m, 27% of the window, costing nothing
to remove and requiring no new machinery, no gate change and no ruling. Lanes finished at 17:52; the
integrator's first act was 19:21. So the integrator boots at **dispatch + ~75 min regardless of lane
state**, and picks up lanes as they hand back.

**Two readings, one conclusion — which is why the conclusion is what travels.** If the
session-transcript mtimes rather than the step-0 contract commits mark the true dispatch, the idle
prologue shrinks toward zero and the dominant term moves to queue + close-out. Either way the serial
tail owns the clock and the suite is 7% of it. This is a second measurement of a term `[NB2-B]` §4a
first named from the W4 wave, reproduced at a different width under a different lane mix.

**The lever the numbers decline to support, said plainly so it is not chased:** a further suite
optimisation aims at the seventh cheapest minute. The tiered-suite law and the xdist flags (Ch5)
already took that term.
```

---

### Act 5 — Ch8, row 12. New subsection, insert after Act 4.

```markdown
### Honest-RED — the batch declares its baseline, and a RED outside it stops the push
<!-- scope: meta -->

A batch names, **in the manifest at dispatch**, the gate readings it inherits: the known pre-existing
RED (if any), the carried WARN loci per check, `git worktree list`, `git stash list`. That declaration
is what makes a later reading attributable — a WARN appearing after the queue belongs to the queue,
because the baseline was recorded before it.

**The clause the closure contract then carries:** the only tolerated RED at close is the declared
pre-existing one. Any other RED leaves `main` unpushed and the end-of-batch packet attributes the
failure. A batch that fixes its declared RED reports 0 and says which lane did it.

**Recorded, rather than suppressed, in both directions.** A gate reading that moves the wrong way is
reported with its cause: the phase-2 head took `doc_rot` from 7 to 9 loci and recorded that the two
new WARNs are the two rows the arc births — the defect one of them exists to fix, demonstrating
itself on arrival — and that no row was trimmed to duck an undeclared threshold. The symmetric case
is a reading that hits a ceiling: `silent_rule_ratchet` touched its baseline on a single word, which
was reworded to identical meaning rather than left at zero headroom for the lanes that edit
`protocols/*.md`.

This is distinct from the three neighbouring RED clauses and does not restate them: the phantom-RED
rule (sequence the suite and the commit) is about a RED that is not real, the vacuous-zero control is
about a green that carries no information, and *a rule that can't go red is decoration* is about
gate design. This one is about what an integrator does with a RED that is real.
```

---

### Act 6 — Ch8, row 10. Append to "Dispatch visibility", after `:2040`.

```markdown
**Teardown is ordered against the board, not only against the refs.** A dispatched lane's session
holds live pids that keep its worktree name locked, so teardown runs in this order: close the holding
session on the Agents board **first**, then `git worktree remove`, then `git worktree prune`, then
delete both branches — the work branch and the `worktree-<name>` provisioning branch. Out of order,
`worktree remove` reports a name still in use and the leftover survives every subsequent check, all
of which are ref-shaped.

This rule lived only in dated handoff bundles until now. A bundle is an immutable per-session
artifact and the next seat boots on a different one, so a board-ordering rule housed there reaches
nobody — which is the reason it is here.
```

---

### Act 7 — Ch8, row 5. New subsection, insert after Act 6.

```markdown
### Land-then-delete — teardown reads artifacts, not only refs
<!-- scope: meta -->

The teardown items above read **branches and worktrees**. A branch that carries the only copy of an
artifact passes all of them, and deleting it destroys the artifact while every check reports a clean
tree. So an artifact-bearing branch is verdicted before it is deleted:

1. **Verdict each branch.** `SUPERSEDED-DELETE` — everything it carries is on `main`. `UNIQUE-HOLD` —
   it is the sole copy of at least one artifact.
2. **Land the UNIQUE-HOLD artifacts on `main` byte-faithfully**, extracted with
   `git checkout <source-ref> -- <path>`, which writes the source blob straight into the index: the
   staged blob differs from the source only if git itself disagrees, so byte-faithfulness is a
   property of the staging method rather than an assertion. Take the branch **tip**, not its first
   commit — a later commit may be an amendment its own author already treated as superseding.
3. **Re-verdict.** Every branch now reads `SUPERSEDED-DELETE`.
4. **Delete on a per-branch byte-coverage proof.** A branch that is not byte-covered is HELD, and a
   HOLD is a recorded disposition with a reason.

**Why the verdict is re-derived rather than inherited.** A phase-1 packet recorded
*"SUPERSEDED-DELETE across the board"*; the re-verdict measured 3 SUPERSEDED-DELETE and 5 UNIQUE-HOLD
— five branches held artifacts nothing had landed. The packet was written honestly and was wrong,
because the state it described moved. Re-deriving costs one pass; inheriting costs the artifacts.
```

---

### Act 8 — Ch11, row 4. Replace the `n=1` framing at `:2423`.

```markdown
**Beats learned across four witnessed batches** (2026-07-30→31, then night-1 2026-08-12, night-2
2026-08-14, night-3 2026-08-15 — past the n=2 evidence gate above, so these are graduated rather
than provisional):
```

*(The two existing bullets below that line — "Report what you did not check" and "A read-only mandate
needs a leftover sweep" — carry over unchanged. The organ list at `:2412-2415` also updates: item 3
"a MORNING RATIFICATION SURFACE" now points at the two subsections Acts 9 and 10 add, rather than at
`[#419]` as an absence.)*

---

### Act 9 — Ch11, row 6. New subsection, insert after the amended `:2423` block.

```markdown
### The consolidated briefing — N night reports become ONE morning artifact
<!-- scope: meta -->

The hard rule above sets the cardinality: the morning is the operator plus ONE report. This is that
report's shape, and it is six-part:

| part | carries |
|---|---|
| **State + contradiction ledger** | executive state in three lines; every point where two night lanes disagree, entered as its own row; a collisions block |
| **Decision queue** | the D-numbered items, one proposed verdict each (below) |
| **Necessary conditions** | preconditions the next session opens against |
| **Functional requirements** | per-lane objective functions for the next wave |
| **Execution plan** | the proposed roster |
| **Provenance appendix** | per-source-lane attribution — which night lane produced which claim |

**The contradiction ledger and the provenance appendix are the two parts that carry the fan-out's
value.** N independent lanes produce disagreement, and disagreement is the product: a briefing that
silently picks a winner has consumed the evidence and reports a consensus that no lane held. Entering
each contradiction as a row, and attributing every claim to the lane that made it, keeps the
architect able to overturn the consolidation rather than only the conclusion.

A consolidated briefing is a **report**, so the `[#443]` rent rule applies: it creates no standing
planning artifact, and it lands as one dated file with a named `consumer` and `consumption_path`.
```

---

### Act 10 — Ch11, row 7. New subsection, insert after Act 9.

```markdown
### The decision queue and the adjudication hour
<!-- scope: meta -->

The consumer the night side hands to. A queue is a list of **proposed verdicts with their evidence**,
not a list of questions — the architect ratifies or overturns, and a queue phrased as questions
converts an hour of adjudication into an hour of re-derivation.

**Shape:**

- **D-numbered items.** Each carries its evidence first, then a proposed verdict, then what the
  verdict unblocks. An item whose evidence is absent says so and proposes nothing.
- **Measurement caveats open the queue; honest limits close it.** The first section states what the
  numbers below can and cannot support; the last states what the queue did not reach.
- **Preconditions first.** Items that unblock dispatch are ordered ahead of everything else, because
  the rest of the queue is dispatchable and they are not.
- **Class dismissals are permitted, and are stated as classes.** A surface of 160 proposals is
  dismissed as a class with its rule, rather than read row by row — which is what makes a one-hour
  adjudication of a large surface tractable.
- **Timeboxed.** The hour is the unit. An item that outgrows it becomes a row, not a longer hour.
- **The output is a ruling record.** The queue proposes; the adjudication rules; the acts that
  execute the rulings are separate and land at Position 0.

**An item may rule that something is deliberately left un-ruled**, with the reason recorded. A bar
honoured by omission is indistinguishable from a bar forgotten.
```

---

### Act 11 — §5, row 11. Replace the `#### Format` block at `:3593-3620`; bump `<!-- version: -->` to `1.1`.

*(Outer fence is four backticks — this draft contains a fenced block of its own, which is the
template a reviewer copies.)*

````markdown
#### Format
<!-- scope: meta -->

The header is a machine contract: `audit.py check_review_artifact_coverage` links a code-impact merge
to its review by parsing these lines. `**Branch:**` and `**HEAD:**` are the two linkage legs (either
satisfies) and `**Tally:**` is what separates a tallied artifact from an untallied one, so a header
written to a different shape produces a file the check recognises and then discounts.

```markdown
# Codex Review — {topic}

**Date:** YYYY-MM-DD
**Branch:** `{branch-name}`
**HEAD:** `{short SHA}`
**Diff range:** `{base}..{branch}`
**Codex version:** {codex-cli x.y.z}
**Mode:** {diff-review | full | targeted}
**Tally:** C/H/M/L <!-- Critical/High/Medium/Low -->

**Model used:** `{exact model string}`
**Review profile:** {code | docs}
**Merge this review covers:** `{merge sha, when known}`

## Findings

### [SEVERITY] file:line — short description

**What:** One sentence.
**Why:** One sentence.
**Fix direction:** One sentence.
**Action:** [resolved in this session / queued / deferred / declined with reason]

(Repeat per finding. Group by severity. Omit empty sections.)

## Resolution summary

What was fixed in this session vs queued for later. Cross-link to JOURNAL entry and commits.
```

**Two legs, either satisfying.** `**Branch:**` covers a review that ran before a rebase rewrote its
SHA out of the range; `**HEAD:**` covers a review whose branch was later renamed. An artifact carrying
one of them links; an artifact carrying both is robust to either event.

**A review captured off-repo and landed later says so.** It states that it is a transcription, gives
the date the review ran in `**Date:**` while the file's own landing date differs, quotes the finding
text and the adjudication verbatim, and re-derives no verdict. Back-dating a landing, or restating a
verdict in the transcriber's words, produces a record that reads like a fresh review and is not one.
````

---

### Act 12 — Ch10, row 3. New subsection under "Two-tier automation doctrine".

```markdown
### Single-flight — one execution of one contract at a time
<!-- scope: dev -->

Dispatch concurrency is a distributed problem, so the guard is a distributed primitive: a **git ref
as a compare-and-swap**. A dispatcher claims `refs/locks/<contract-id>` on `origin` with
`git push --force-with-lease=<ref>: origin HEAD:<ref>` (an empty expect-value, i.e. the ref does not
exist), plus a local `git update-ref --stdin` `create` fast leg for same-clone contention. Release is
a ref delete. It fails CLOSED, on the `block_ff_push` posture, and adds no dependency.
`scripts/single_flight.py`, exits 0 claimed / 3 in-flight / 2 internal.

**The trap it exists to avoid, which is the reason this is doctrine and not only a tool.** A plain
`git push` of a lock ref exits **0** with `Everything up-to-date` when both racers sit at the same
commit — the normal state at batch dispatch. So a guard built on push exit codes greenlights exactly
the race it was written for, and the lease is what makes the claim atomic. Filesystem locks are
single-host by construction and do not address this at all: the witnessed failure was three
executions of one contract live at once, two of them independently allocating the same four ids,
sharing neither tree nor machine.

**Honest limit.** The guard is wired to no hook, so it is invoked rather than enforced, and two
latent defects stay open on its row: an ABA race in `release` (after a manual lock clear, one
dispatcher's cleanup deletes another's live lock, since racers share HEAD and the token is not
generation-unique) and a `rev-parse` conflation in the local-only path (a non-zero return maps to
"ref absent", so a corrupt repo reads FREE). Both are `[#530]` legs, and the row is open for them.
```

---

### 3.1 · Arc summary for the architect

| Act | Target | Row | Kind | Approx. lines |
|---|---|---|---|---|
| 1 | Ch8 `:1884` | 1 | append | 16 |
| 2 | Ch8 `:1838-1843` | 2 | replace | 25 |
| 3 | Ch8 before `:1988` | 13 | new subsection | 32 |
| 4 | Ch8 | 9 | new subsection | 25 |
| 5 | Ch8 | 12 | new subsection | 24 |
| 6 | Ch8 `:2040` | 10 | append | 12 |
| 7 | Ch8 | 5 | new subsection | 26 |
| 8 | Ch11 `:2423` (+ `:2415`) | 4 | replace | 5 |
| 9 | Ch11 | 6 | new subsection | 26 |
| 10 | Ch11 | 7 | new subsection | 26 |
| 11 | §5 `:3593-3620` | 11 | replace + version bump | 45 |
| 12 | Ch10 | 3 | new subsection | 22 |

**Net PLAYBOOK growth ≈ +250 lines on 4628** (~5%). PLAYBOOK carries no line budget — the ≤200-line
cap is `CLAUDE.md`'s (ADR-53) — and the TOC regenerates via the `toc-freshness-playbook` pre-commit
gate, which fires on every act here.

**Independence.** Each act stands alone; the architect can rule any subset. The only ordering
constraint inside the arc is that Act 8's organ-list edit at `:2415` points at Acts 9 and 10, so
dropping either of those leaves Act 8 pointing at a section that does not exist.

**Two acts touch existing text rather than adding to it** — Act 2 (replaces per-lane requirement 5)
and Act 11 (replaces the §5 format block and bumps its version stamp). Act 11's version bump makes it
the one act with a reconciliation consequence: `<!-- version: 1.0 → 1.1 -->` on a section that other
surfaces may declare an edge against. `reconciled_versions` reads declared `reconciled_with:` stamps,
so the bump is worth checking against `_COUPLED_VERSION_SETS` before it lands.

---

## §4 · Ratchet and gate accounting for the drafts

**Measured live on this tree, not inherited:**

```
detector          silent-rule-v4  (scripts/silent_rule_detector.py)
token             \b(?:must|shall|never)\b, case-insensitive, one count per OCCURRENCE
scope             protocols/*.md . templates/**/*.{md,tmpl} . ecosystem/*.yaml
live count        440   (58 files in scope)
committed baseline 441  (ecosystem/silent-rule-baseline.yaml)
HEADROOM          1
```

**Every one of the twelve drafts carries zero `must` / `shall` / `never` tokens**, so adopting all
twelve moves the count by **+0** and leaves the headroom at 1. That is deliberate rather than
incidental: at a headroom of one, a single normative token in one draft would take the arc to
441 = baseline and leave nothing for the lanes concurrently editing `protocols/*.md`. The phrasing
throughout is declarative — *"the integrator boots on a clock"*, *"an off-grammar name does not error
— it silently forfeits the exemption"*, *"a branch that is not byte-covered is HELD"* — which is also
how the surrounding PLAYBOOK prose reads, so the drafts do not announce themselves as imports.

**Other gates the arc would meet, and how each is discharged:**

- `toc-freshness-playbook` — fires on all twelve acts. Regenerate with the `scripts/toc/` tool.
- `canonical_freshness` (audit check #10) — **does not fire.** `PLAYBOOK.md` is in neither
  `canonical_freshness_gate.DEFAULT_FRESHNESS_FILES` nor `audit._HUB_ONLY_FRESHNESS_FILES`; the
  comment above the hub-only list records why, verbatim: *"PLAYBOOK is the largest ungated canonical
  doc but is DEFERRED (no `last_reviewed` frontmatter yet + a genuine end-to-end re-read is its own
  arc)"* (2026-07-08 fleet-census A-2 ruling). So this arc adds ~250 lines to the largest canonical
  doc with no stamp obligation and no edited-since-review signal — which is the deferral working as
  ruled, and also the reason the arc's own review quality is carried by the architect's ruling rather
  than by a gate.
- `audit-health` — the standing FAIL-blocks-commit gate; nothing in these drafts touches a checked
  surface.
- `doc_structure` / `doc_rot` — the arc adds subsections with headings inside existing chapters,
  which is the shape the TOC and `doc_structure` already expect.
- `validate-hermetization` — no new paths; every act edits an existing tracked file.

---

## §5 · Witnessed in batches 4–6, not rowed (outside the tally)

Listed without verdicts, because the tally is scoped to the brief's thirteen. Each is a shape a
successor could reasonably ask about; none has been graded here.

- **Lane contract files as committed artifacts** — the `docs/audits/<date>-technical-<slug>-lane-contract.md`
  class, carrying `## Common law (all phase-N contracts)` + `OWNED-FILES manifest` + `## What NOT to do`.
  Ch8 `:2050-2075` covers the *path* question (the contract of record lives in the tree) and states its
  own honest limit that nothing checks a manifest's lane rows resolve to committed contracts.
- **The lane packet** — `T_start` · manifest-as-executed · per-step commit SHAs · targeted-test
  evidence · self-reported deviations · a final `STOPPED` line.
- **The `T_start` line** — one line per lane converting the latency row from UNVERIFIABLE to derivable
  at essentially zero cost (`[NB2-B]` §4b).
- **`uv run --locked` on every in-lane test invocation** — carried at Ch8 per-lane requirement 3, and
  the phase-2 cloud finding sharpens it: the container image ships `uv 0.8.17` against a `==0.11.19`
  floor, so a cloud lane either approximates the gate or skips it until `uv` is replaced at
  provisioning (`[#484]`).
- **Regenerate-at-merge for the three generated files** — `BACKLOG.md`, `tasks/manifest.json`,
  `docs/audits/README.md`; stage the lane's `tasks/` edits first, because `gen_audit_index.py` reads
  tracked files only.
- **The HOLD disposition** — a lane branch held with a reason rather than merged, with its worktree and
  branch left untouched for the operator. Ch8 states "merged-or-explicitly-abandoned"; HOLD as a named
  third state, and the teardown asymmetry it implies, is not covered.
- **The ex-ante process-lane cap declaration** — Ch8 carries the cap and the dispatched-width
  denominator; that the bucket assignment is *declared before dispatch rather than reconstructed after*
  is the D10 requirement and reads as an implication rather than a clause.

---

## §6 · Honest limits of this report

1. **"Board rules 1–8" could not be enumerated.** No in-repo artifact carries a numbered set of eight
   board rules; a corpus-wide `grep` for `board` returns the board-*label* convention and nothing else.
   The set is off-repo (the operator's pack). Row 10 therefore verdicts **the in-repo board surface**,
   not rules 1–8 individually, and Act 6 drafts only the one board rule this report could locate a
   source for (teardown ordering, from two handoff bundles). If the eight are a distinct enumeration,
   this row is under-specified and the architect holds the source.
2. **Batch-4 and batch-5 evidence is read from artifacts, not from execution.** This lane observed
   neither batch run. Timings, lane counts and failure attributions are quoted from the phase-1 packet,
   the night-3 sessionplan and the JOURNAL, all of which state their own instruments; where they
   disagree (the dispatch-time discrepancy in row 9) both readings are carried rather than one being
   chosen.
3. **The tally is a judgment, and its bar is stated so it can be overturned.** §1 defines COVERED as
   ADR-81 leg (a) sufficiency. Under a "does a section exist" bar the tally would read covered 6 /
   partial 1 / absent 6. The rows most sensitive to the bar are 1, 2, 6 and 10; rows 3, 5, 9, 12 and 13
   read ABSENT under either bar, and row 8 reads COVERED under either.
4. **No test suite was run and no gate was executed against a modified PLAYBOOK.** The ratchet count in
   §4 is measured against the tree as it stands; the "+0 tokens" claim for the drafts is a token count
   of the draft text, not an observation of the check passing on an edited file. Adopting the arc and
   re-running the detector is what converts it from arithmetic to a measurement.
5. **The drafts are candidate text, not ruled text.** They are written to be paste-ready so the
   architect's cost is a ruling rather than an authoring pass — which also means they carry this lane's
   phrasing choices into canonical files if adopted verbatim. Act 2 and Act 11 replace existing text and
   deserve the closest reading for that reason.
6. **`silent_rule_ratchet` headroom is 1 and this lane is one of several editing concurrently.** The
   +0 accounting holds for this arc in isolation; if another lane in batch 6 adds a normative token
   before this arc lands, the arithmetic changes without any of these drafts changing.
7. **`audit.py health` reads DEGRADED here, and all four `[!!]` markers are shallow-clone artifacts —
   a 4-for-4 reproduction of the night-3 finding on an independent lane.** This container holds a
   shallow clone (29 grafts, 281 reachable commits, earliest reachable `fcfc553` @ 2026-08-10 22:18),
   and the markers are: `repos registered (none)` — no sibling repos on this disk;
   `canonical_freshness` 6 stale — every one of the six reports its last edit as **2026-08-10**, i.e.
   the graft floor, because an untouched file's history terminates there; `hooks_armed` — the
   container never ran `pre-commit install`; `journal_spine_anchor` — the ADR-85 disposition floor
   `24882f8cc` sits below the floor and is not a valid object here. **None is a regression and none is
   this lane's.** The gates that actually govern this commit were run against the staged files and
   **passed**: `block-commit-on-main`, `normalize-dated-headers`, `audit-index-freshness`,
   `validate-hermetization`. Running them at all required the `[#484]` workaround the night-3 lane
   documented — the image ships `uv 0.8.17` against a `==0.11.19` `requires-version` floor, so the
   pinned toolchain was installed alongside and placed ahead of it on `PATH`. **`health: OK` is not
   reproduced here and is not claimed.**

---

covered 1 / partial 6 / absent 6
