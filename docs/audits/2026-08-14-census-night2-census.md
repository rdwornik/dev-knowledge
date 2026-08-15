---
title: "Night-2 census — the whole open set, one row per open [#id], proposed verdicts only"
date: 2026-08-14
class: census
---

# Night-2 census — the whole open set

> **DRAFT · PROPOSED VERDICTS ONLY · ZERO CLOSES EXECUTED.**
> This artifact **prepares** the booted architect's P10 duty ([#506]); it does not discharge it.
> The whole-open-set grooming *judgment* stays his. This lane assembled the evidence, read all
> 196 open rows end to end, and proposes a verdict per id so ratification can happen in batches
> rather than per-id. **No `tasks/` file, no `manifest.json` node, and no `BACKLOG.md` row was
> touched by this lane.** The only file it adds is this one.

**Lane:** `claude/night2-census-audit-btqr42` (read-only census) · **Base:** `main` @ `7bbb067`

---

## 0. Method, and what it cannot tell you

**Open-set derivation (live, not transcribed).** `python scripts/validate_backlog.py` →
`OK (9 themes, 26 stories, 196 tasks, 1 warning)`. The 196 are the `"task"` nodes in
`tasks/manifest.json` — the ADR-107 source of truth — not a parse of the generated `BACKLOG.md`.
Cross-check: 262 `tasks/*.md` files on disk, 196 referenced by the manifest, 66 orphaned
(closed rows keeping their file as the id-allocation record, per ADR-107 §6.3). Zero manifest
nodes point at a missing file.

**History.** The container arrived a **shallow clone** (`git rev-parse --is-shallow-repository`
→ `true`; 318 commits, 59 on main's first-parent, oldest 2026-08-02). Every "since its birth"
column would have been silently wrong. Un-shallowed before any measurement — **5,043 commits,
1,441 on the first-parent spine, back to 2026-03-30**. This is [#453] leg (1) recurring, in a
second container, on a different night: *a freshness/history organ that lies on a shallow
checkout is the trap, not the FAIL.* Recorded here as fresh evidence against that row.

**Birth** per id = the earliest of 685 `BACKLOG.md` revisions in which the `[#id]` token appears
(full-history walk via `git cat-file --batch`). All 196 resolve; none is unborn.

**First-parent reference** = a commit on `git log --first-parent main` whose **subject or body**
contains the `[#id]` token, dated at or after that birth. It is a *mention* count, not a
closure signal — the repo's own closure detector is on record as unreliable in exactly this
way ([#277] 49 proposals / 0 valid; [#454] a negated mention parsed as a closure). Read the
column as "has the spine ever named this row", nothing stronger.

### Three honest limits, stated rather than left to be discovered

1. **The "last git touch of its task file" column is nearly uninformative, by construction.**
   `tasks/` post-dates the rows it holds (ADR-107 strangler step 3). 84 of 196 files share one
   date, **2026-07-28** — the migration commit. A further 44 share **2026-08-13** — the W4a–d
   *Done-when conversion* lanes, which rewrote wording and built nothing. The column is
   reported because it was asked for; **the first-parent-reference column is the one that
   carries signal**, and neither is a work-happened signal on its own.
2. **A brand-new row shows zero first-parent references and that is correct, not stale.**
   [#526] / [#527] / [#528] were born 2026-08-14 and no merge has yet named them. Do not read
   the 56 zero-reference rows as 56 abandoned rows — see §7 for the ones that genuinely are.
3. **This census verdicts rows against their own stated Done-when.** It does not re-litigate
   whether a Done-when is the *right* finish line. Where a row's finish line is itself the
   defect, that is [#456]'s cohort and [#505]'s clause-strike precedent, not this sheet's call.

---

## 1. The count

| verdict | n | share |
|---|---|---|
| proposed **live** | 169 | 86.2% |
| proposed **dead** | 2 | 1.0% |
| proposed **awaiting-ruling** | 25 | 12.8% |
| **total** | **196** | 100% |

**The headline is the shape, not the number.** Two dead out of 196 is not a census that failed
to look — it is what an aggressively-groomed set looks like. ARC-2, ARC2b and batch 4 closed
the dead rows in the last six days ([#270] · [#132] · [#521] · [#513]), and the W4a–d lanes
had already re-cut 39 Done-when clauses against live state. What is left is **169 rows of real
unbuilt engineering and 25 rows that no executor may lawfully start**. The grooming lever here
is not deletion; it is §4 — a quarter-day of rulings unblocks 25 rows, which is a larger
change to the workable set than any close batch available.

---

## 2. Proposed-dead, grouped by close-reason

Two rows, one reason class. Both are **already-shipped** under ADR-65 — the artifact the row
asks for exists on `main` today and the row was simply never closed. Neither is superseded and
neither is obsoleted; **there are no proposed members in those two classes**, which is itself a
result worth recording.

### Group D1 — already-shipped (2 rows)

**[#524] · P2/S · four ruled check extensions — the N2 set, Codex-produced**

| leg | Done-when clause | landed at |
|---|---|---|
| (a) | `audit.py health` REDs on a duplicate JOURNAL day-letter (3 tests) | `scripts/audit.py:3955` marker, `:3970` `check_journal_day_letters`; tests `tests/test_audit.py:2057`, `:2068`, `:2079` |
| (b) | `validate_backlog` WARNs on a past body-date, silent on future (2 tests) | `scripts/validate_backlog.py:84` marker, `:355` scan; tests `tests/test_validate_backlog.py:383` |
| (c) | `journal_anchor` WARNs "anchored by mention, not by record" | `scripts/journal_anchor.py:199` marker, `:238` the verbatim WARN string; test `tests/test_batch_manifest.py:706` |
| (d) | `check_hooks_armed` asserts the **pre-push** hook type (1 test) | `scripts/audit.py:1628`/`:1660`; test `tests/test_audit.py:2015` |

Merged to `main` at **`62f42dad`** (2026-08-14, `worktree-lane-l-524-check-extensions`) — the
row's only first-parent reference after birth, and it is a landing. Reviewed:
`docs/audits/2026-08-14-codex-524-check-extensions.md`, tally **0 Critical / 1 High / 0 / 0**,
the single HIGH dispositioned a false positive in-artifact with the verifying commands shown.
`docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §2 states the row's state in one
word: **"Complete."** Leg (d) required no code — `check_hooks_armed` already discharged it.

**[#352] · P3/S · versioned `.vscode` region decoration (RULING-S human-facing half)**

Done-when has two clauses; both hold against the live tree.

- *"covers the owner=hub/repo regions of ≥1 governed file"* — `.vscode/settings.json`'s
  `//boundary` block carries two `highlight.regexes` entries keyed on the #312 marker
  vocabulary: `owner=hub` → grey `rgba(140,140,140,0.16)`, `owner=repo` → navy
  `rgba(38,79,140,0.30)`, dark-theme tuned, `filterFileRegex` scoped to `CLAUDE.md` and
  `.claude/**.md`. `CLAUDE.md` carries **8 `owner=hub` + 8 `owner=repo`** marker regions
  (`grep -c "methodology:start" CLAUDE.md` → 15 starts + the pairs). The file is tracked
  (`git ls-files .vscode/`) and landed at **`897577b7`** (2026-07-20), whose subject reads
  *"flip colours to the [#352] spec"* — the config was built against this row.
- *"carries no hand-maintained ownership state"* — satisfied and already adjudicated. The row's
  own **AMENDED** clause records it: the config holds two regexes and **no per-region state**,
  so region add/remove/reclassify needs no config change; *"generating a static two-regex file
  is ceremony."*

**Third, independent signal:** the row declares **"P4a, shelf-life 2026-08-13 (revisit/kill if
not advanced)."** That date passed yesterday. The row's own instruction on expiry is *revisit
or kill*; the tree says the work is done, so the reading is *close*, not *kill-unbuilt*.

> **Both dead proposals sit inside serialize-groups. See §6 — flagged there, loudly.**

### Groups D2 (superseded) and D3 (obsoleted) — EMPTY

No open row was found superseded by a named successor, and none was found obsoleted by a
subject that no longer exists. Both were checked, not assumed:

- **Supersession sweep:** 9 rows contain a supersession token. Each was read; every one
  describes a supersession *the row itself survives* — the sharpest is **[#43]**, whose body
  says *"superseded-by that intake ... this task persists as the decomposition target."* It is
  proposed **awaiting-ruling**, not dead, because only a ruling can decide whether the
  decomposition-target role outlives the supersession.
- **Obsolescence sweep:** the 16 rows citing a repo-relative path that does not exist were
  enumerated (§8). Every one names an artifact **to be built** ([#43] `templates/new-repo-skeleton/`,
  [#112] `scripts/hooks/adr_amend.py`, [#171] `ecosystem/conformance.md`), a **gitignored log**
  ([#181], [#322], [#418], [#277]), or a **cross-repo path** ([#303], [#344], [#393], [#427],
  [#509]). None indicates a dead subject.

---

## 3. Where the closing-verb scan landed (and why it produced nothing extra)

A full-history scan of main's first-parent spine for a closing verb adjacent to an open
`[#id]` returned **24 open rows**. Every one was read; **all 24 are co-mentions** — the verb
governs a *different* id in the same merge subject (e.g. `[#293]` surfaced from
*"Merge feat/164-handoff-finish -- [#164] v5 /handoff generator FINISHED"*, which closes #164
and merely names #293).

This is not a null result. It is [#454]'s recorded defect reproduced at full-corpus scale
(`closure_ids` reads a mention next to a verb as a closure) and [#277]'s 49:0 ratio in a second
independent run. **The two genuine already-shipped rows in §2 were found by reading, not by the
detector** — which is the evidence [#487] leg (iii) and [#454] both want, and it is recorded
here rather than filed as a new row.

---
## 4. Proposed awaiting-ruling — 25 rows no executor may lawfully start

**Predicate, stated so it is checkable and not a feel.** A row is proposed *awaiting-ruling*
only when **both** hold:

1. the row's own text bars a build until a decision lands — one of *"filing only, zero build"*,
   *"QUESTION-SHAPED, no ruling taken"*, *"Decide (do not build)"*, *"ROW ONLY this session"*,
   *"Options, NONE chosen (a ruling)"*, *"needs an explicit operator ruling / ask / GO"*,
   *"a DECISION ticket, not the execution"*; **and**
2. its Done-when's **leading** clause is a ruling or decision, not an artifact.

A row whose Done-when merely *offers* a `protocols/STANDING_RULINGS.md` escape beside a
buildable primary clause is **live**, not awaiting-ruling — that escape is an exit, not a
precondition. That single distinction is what keeps this set at 25 instead of ~60.

### 4a. Operator-owned by authority — an executor cannot act even with a design (5)

These are not "unruled work"; they are work the ruling *authority* forecloses.

| id | why the executor is barred |
|---|---|
| [#122] | deletion authority — *"removal needs an explicit operator ask per the no-delete invariant"* |
| [#189] | executes in `~/.claude` (queue-only here, #100 execute-elsewhere precedent) |
| [#300] | *"bundle sweep AWAITING explicit operator deletion GO (no drive-by deletion)"* |
| [#346] | the `~/.claude` edit is global infra — core-invariant #6 exception-with-ruling |
| [#420] | carries a live **do-not-touch order** on `docs/archive/` while the row is open |

[#456] independently reaches four of these five (*"[#122] and [#189]/[#346] by deletion
authority and core-invariant #6"*), which is a cross-check on this grouping rather than a
coincidence.

### 4b. Question-shaped by declaration — the row was filed to be ruled (11)

[#323] · [#331] · [#347] · [#397] · [#406] · [#407] · [#409] · [#410] · [#411] · [#449] · [#450]

Six of these are a **single ruling apart from being buildable**, and three of them
([#409] / [#410] / [#411]) are *the same ruling* — the standing night-batch trio, each
identically worded *"defined as a routine (trigger, scope, consumption path) and ruled in or
out"*, each gated on ADR-105 activation. **That is one architect decision releasing three rows.**

### 4c. Decision-first, build-after — the ruling is the leading clause (9)

[#43] · [#126] · [#308] · [#371] · [#408] · [#414] · [#491] · [#494] · [#495]

Two sequencing notes the architect will want:

- **[#371]'s vehicle is [#387]'s subject.** [#371] says *"Vehicle decided by the buy-vs-build
  fleet-template ADR ... do NOT implement bespoke"*, and [#387] exists because that very intake
  *"argued FOR the template engine that was subsequently rejected."* [#387] is **live** and
  buildable. Ruling [#371] before [#387] lands would ratify against a document the fleet has
  already refuted — [#387]'s own stated reason for existing.
- **[#414] and [#408] each name their organ choice as the first gate on any build** — for
  [#408] the per-section granularity is *"an OPERATOR DECISION deliberately not settled"* in
  its own design draft; for [#414], *"Organs, NONE chosen (a ruling)."*

---

## 5. Still-Proposed promotions — the live register state

**Scope note.** Two surfaces carry promotion state, and they disagree in *kind*, so both are
read: `protocols/STANDING_RULINGS.md` **M-5** (the Night-2 Part D1 promotion-candidate table,
9 items) and **M-6** (Part D2 ADR-set hygiene, 5 items), plus the pre-ratification intake
corpus that M-5's own dispositions land into.

**ADR corpus: zero ADRs sit in `Proposed`.** Every `docs/decisions/ADR-*.md` status line was
read. The only non-`Accepted` values are three terminal/other states — ADR-45 *"Explored, not
adopted"*, ADR-46 and ADR-47 *"Partially superseded"*. **There is no Proposed ADR to ratify.**

### 5a. M-5 promotion candidates — 4 of 9 still un-landed

| item | disposition (register) | live state | locator |
|---|---|---|---|
| `N2-D1-01` | PROMOTE — new ADR | **LANDED** | `docs/decisions/ADR-112-*.md` — *Accepted (operator ratification 2026-08-12)* |
| `N2-D1-02` | **DO-NOT-PROMOTE YET** — *"reassess after W3 lands"* | **STILL PROPOSED · trigger now MET** | W3 landed 2026-08-13; `[#513]` DISCHARGED at `387b794a` per the true-close packet §1 |
| `N2-D1-03` | PROMOTE AS CONSOLIDATION | **LANDED** | `docs/decisions/ADR-110-*.md:310` — *"Amendment — 2026-08-12: a pointer block ... (navigational only)"* |
| `N2-D1-04` | DO-NOT-PROMOTE — it is done | terminal | `CLAUDE.md` §4 + register B5 |
| `N2-D1-05` | DO-NOT-PROMOTE | terminal | answered at register **L-1**; ceiling self-retires |
| `N2-D1-06` | CONSOLIDATION-INTAKE **Section A** | **STILL PROPOSED** | `docs/intake/2026-08-12-func-repo-self-description-consolidation.md:54` — file is **`status: DRAFT`** |
| `N2-D1-07` | CONSOLIDATION-INTAKE **Section B** | **STILL PROPOSED** | same file `:97` — `status: DRAFT` |
| `N2-D1-08` | CONSOLIDATION-INTAKE **Section C** | **STILL PROPOSED** | same file `:129` — `status: DRAFT` |
| `N2-D1-09` | ONE intake, three sections | **structure LANDED, ratification not** | the three sections exist in one doc, as ruled; the doc is unratified |

**Read this as three items, not four.** `N2-D1-06/07/08/09` are one artifact: the consolidation
intake was **born as ruled** (one doc, Sections A/B/C, §201 `Births`) and is sitting at
`status: DRAFT` awaiting ratification. `N2-D1-02` is the genuinely separate one, and it is the
one whose **trigger has since fired** — its reassess condition was *"after W3 lands"*, and W3
landed the day before yesterday.

### 5b. M-6 ADR-set hygiene — 2 of 5 still standing

| item | disposition | live state |
|---|---|---|
| `N2-D2-i` | RULE — declare the enum | **LANDED** — `docs/decisions/README.md:10` *Status enum*, the five + `Superseded` + `Deprecated` |
| `N2-D2-ii` | TAK — forward pointers, no status edits | **LANDED** — `ADR-32:140` and `ADR-42:450`, both *"appended 2026-08-12 (not a status edit)"* |
| `N2-D2-iii` | **REVIEW-EACH, no action now** | **STILL OPEN** — the six sunset/review candidates stand with their named blockers |
| `N2-D2-iv` | ROUTED → `A1` | closed into register **L-1** |
| `N2-D2-gaps` | **FLAGGED, NOT ACTED ON** | standing — numbering gaps 40, 44, 52; ids are not reused |

### 5c. Pre-ratification intake corpus — the denominator behind the I-D6 ceiling

Live frontmatter today: **SEED 9 · DRAFT 3 · READY 1 · ACCEPTED 15** (28 docs under
`docs/intake/`). Under **L-1**'s ruled reading — the ceiling of six counts **DRAFT + READY**,
SEED sits outside it as the parking lot — the working set is **4 of 6**, unchanged from the
figure L-1 recorded at the ruling. **The ceiling is not breached**, and the three DRAFT docs
are: `2026-08-05-tech-currency-wave-1` (#24), `2026-08-06-tech-adoption-consolidation-intake`
(#27), `2026-08-12-func-repo-self-description-consolidation` (#33 — the M-5 consolidation
intake above). The READY doc is `2026-07-16-satellite-onboarding-prompts` (#15).

### 5d. One register entry whose own expiry has been met

**`I-D7` · Intake #10 — survival review OPENED, disposition owed.** The entry's expiry reads
*"retires when the disposition is recorded"*, owner **operator**, due *"next window"*. **The
disposition has been recorded:** intake #10 was **REJECTED and relocated to the archive** at
`f095a81f` (2026-08-12, *"docs(intake): ARC2 step 6 — intake #10 REJECTED and relocated to the
archive path"*), and the file now lives at `docs/intake/archive/2026-07-11-tech-c4-visualization-memo.md`.
The register entry still stands, and its locator — `docs/intake/2026-07-11-tech-c4-visualization-memo.md` —
**no longer resolves**. Reported, not edited: the register is the architect's surface and B6's
append-not-amend discipline governs it. This is the `[#503]` doc-currency class landing inside
the register itself.

---

## 6. Serialize-group cross-check — **BOTH PROPOSED-DEAD ROWS ARE SERIALIZED** 🚩

`python scripts/validate_backlog.py` emits **12 serialize-groups covering 132 of the 196 open
ids**. Cross-checked mechanically against this census: every group member is in the open set
(0 strays), and every open row carrying a `serialize-group:` frontmatter field appears in that
exact group (0 mismatches). The grouping surface is clean.

**The flag: neither proposed-dead row is a free-standing leaf. Both sit inside a group, and
both are mid-chain.**

| dead id | group | group size | position in the emitted order | co-members proposed awaiting-ruling |
|---|---|---|---|---|
| **[#524]** | `audit-py` | **48** — the largest group in the repo | **17th of 48** | [#323] · [#397] · [#406] · [#408] |
| **[#352]** | `settings-json` | **18** | **11th of 18** | [#308] · [#371] · [#414] |

**Why this matters and what it does *not* mean.** A serialize-group is a *contention* declaration
— these rows touch the same file and must not be worked concurrently — not a dependency chain.
So closing a mid-chain member **cannot orphan a successor**; it removes a member from the
contention set, which strictly *widens* what can be worked in parallel. There is no ordering
breakage to repair here.

**But the flag is still owed, for two reasons the architect should weigh before ratifying:**

1. **`audit-py` at 48 members is a third of the open set serialized behind one file.** [#524]
   is the *only* member this census proposes closing. Ratifying it shrinks the largest
   contention set in the repo by exactly one — worth knowing when it is also the group most
   likely to be a batch-planning bottleneck.
2. **Neither group's ordering is machine-enforced.** [#424] records that `depends-on` gates are
   inert for the bare-id form (`validate_backlog.py:78` `_DEPID_RE` requires the `#`), and
   [#510] records that the lane-exemption keyed on branch *shape* rather than a declared
   roster. So the serialize-group order is prose the operator honours, not a checked
   constraint — which is precisely why a mid-chain close deserves a loud line rather than a
   silent one.

**Neither close is executed here.** Both stay open until ratified.

---

## 7. Grooming signals the architect can act on without a per-id read

Distinct from the verdicts: these are rows whose **peg** — not whose work — has gone wrong.
Every one is proposed **live**; the defect is the trigger, and the ARC-2 precedent for all of
them is *un-defer or re-peg, do not close*.

### 7a. Peg MET — un-defer candidates (2)

| id | peg | evidence it fired |
|---|---|---|
| [#494] | *"the batch-4 ratification batch"* | batch 4 closed 2026-08-14 — `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §1 |
| [#352] | shelf-life **2026-08-13**, *"revisit/kill if not advanced"* | date passed; and the work is done — hence its **dead** proposal in §2 |

### 7b. Peg DEAD or unmeetable — the row is stranded (2)

| id | the row's own words |
|---|---|
| [#102] | peg is *"a repo whose codemap is generator-MANAGED"* — and the row adds *"so no fleet codemap migration is coming to peg on"*. **A peg that states it cannot fire.** The Done-when itself is buildable. |
| [#325] | *"DEFER — peg #221 DEAD, unreplaced 2026-08-09 ... Stays open, **stranded**"* — [#294] was checked and cannot absorb it, [#236] is closed. |

This is [#505]'s clause-2 class exactly — *"a finish line in the past tense ... the measurement
was not merely missing, it could no longer be taken"* — recurring on two further rows. Neither
is a new filing; both already carry the diagnosis in-row. What they lack is a re-peg.

### 7c. Dated triggers now on the near horizon (4)

| date | id | what falls due |
|---|---|---|
| **2026-08-17** (3 days) | [#492] | dated re-check of Grok 4.6's release — *not a new peg*, register `I-D` item 1 |
| 2026-08-26 | [#348] · [#426] | `review_date:` on both routine declarations |
| 2026-09-09 | [#322] | dated review, converted 2026-08-10 from the retired C4-viz peg |
| 2026-10-22 | [#413] | Done-when does not open before this date |

### 7d. The 56 zero-first-parent-reference rows, honestly split

Zero spine references since birth is **not** an abandonment signal on its own. Split:

- **3 are newborn** — [#526] / [#527] / [#528], born 2026-08-14. Correct, not stale.
- **13 are proposed awaiting-ruling** — [#43] [#122] [#126] [#189] [#323] [#331] [#397] [#409]
  [#410] [#411] [#450] [#494] [#495]. A row nobody may lawfully start is a row the spine will
  never name. Their silence is the *symptom of §4*, not an independent finding.
- **40 are live, unbuilt, and un-narrated.** Of those, **17 were born 2026-06-01 … 06-19 and
  have never once been named by a merge on `main`** — ten weeks, zero spine mentions:

  | | | |
  |---|---|---|
  | [#4] P2/M · 06-01 | [#19] P3/M · 06-01 | [#23] P3/S · 06-01 |
  | [#71] P3/S · 06-01 | [#99] P3/S · 06-06 | [#116] P3/S · 06-06 |
  | [#127] P3/S · 06-07 | [#139] P2/L · 06-09 | [#144] P3/M · 06-10 |
  | [#153] P2/M · 06-11 | [#166] P3/M · 06-14 | [#169] P3/M · 06-16 |
  | [#171] P3/M · 06-16 | [#181] P2/S · 06-17 | [#185] P2/M · 06-18 |
  | [#188] P3/M · 06-18 | [#190] P3/M · 06-19 | |

  **This is the sharpest single grooming datum in the census.** They are not dead — every
  Done-when was read and each is unmet and buildable — but nothing has pulled on them in ten
  weeks. That is the *condition* [#488]'s ranking axis exists to make legible and [#506]'s
  whole-set contract exists to catch, and it is the set the architect should look at first if
  the P10 pass wants a kill batch rather than a ruling batch. **This census does not propose
  killing any of them**, because "old and quiet" is not one of ADR-65's three classes.

---

## 8. Census hygiene notes (reported, not fixed — zero edits beyond this file)

1. **[#181]'s peg names a path that cannot exist under that name.** The row and its DEFER peg
   both read `logs/coherence-nudge.log`; the canonical name has been **`logs/COHERENCE-NUDGE.log`**
   since the 2026-07-22 UPPERCASE-KEBAB ruling (`CLAUDE.md` §9), and it is **gitignored**
   (`.gitignore:81`). So the peg — *"the nudge log has enough entries to adjudicate"* — is
   un-evaluable from any fresh clone, and per-working-tree besides: the same shape [#418]
   records for `logs/FLEET-HEALTH.md`. `[#503]`/`[#497]` stale-locator class.
2. **ADR-112 carries an internal disagreement about its own ratification.** Its status line
   reads *"Accepted (operator ratification 2026-08-12)"* while the **Decision tier** line two
   rows below still reads *"ratification is a separate operator act and **has not happened**"*.
   This is a *predicted* consequence, not a slip: ADR-94's exception permits the **status line
   only** to be edited in place, so a pre-ratification parenthetical elsewhere in the header
   survives by design. Noting it because [#242]'s go-forward header↔index coherence check is
   the organ that would surface exactly this, and it remains unbuilt.
3. **`validate_backlog` carries one standing WARN**, unchanged and expected:
   *user story with no tasks — story "[S24] Declare desired state once, as data" line 443*.
   [S24] is an [E9] North-Star story whose rows have all closed or moved; not a census defect.
4. **The shallow-clone trap fired again** (§0). [#453] leg (1) is the owner. This is its second
   recorded container instance; the row's Done-when — *"a session preflight performs the
   unshallow and asserts the `uv` pin"* — is still unbuilt, and this lane paid the cost
   manually.

---

## 9. Appendix — the full 196-row census

One row per `status: open` task, ordered by id. Columns are the four asked for plus the
verdict.

- **task-file touch** — last commit touching `tasks/<id>-*.md`. Read §0 limit 1 first: 84 rows
  share 2026-07-28 (the ADR-107 migration) and 44 share 2026-08-13 (the W4a–d Done-when
  conversions). Low signal, reported as specified.
- **spine refs** — count of first-parent commits on `main` naming `[#id]` at or after its
  birth, then the **most recent** such commit. `**none**` = never named.
- **verdict** — proposed only. Nothing here is executed.

| id | title | P/S | task-file touch | spine refs since birth · newest | proposed verdict | one-line reason |
|---|---|---|---|---|---|---|
| [#4] | Build lessons-index.json + SessionStart retrieval… | P2/M | 2026-07-28 | 0 · **none** | live | lessons-index.json absent; DEFER peg (retrieval-miss after #185) unfired |
| [#19] | Complete the ADR-39 register | P3/M | 2026-07-28 | 0 · **none** | live | clause (a) BACKLOG.md ADR-39 register entry is buildable and unbuilt |
| [#23] | Validate ADR frontmatter relation-fields | P3/S | 2026-07-28 | 0 · **none** | live | no audit check flags an unresolvable ADR relation-field; #112 depends on it |
| [#43] | Decide + | P3/L | 2026-07-28 | 0 · **none** | awaiting-ruling | "Decide + (if yes) author"; Done-when leads with *decision recorded*; body also carries a `superseded-by` intake marker |
| [#71] | Reconcile ENVIRONMENT.md's `~/.claude/` directory… | P3/S | 2026-07-28 | 0 · **none** | live | ENVIRONMENT.md `~/.claude` tree + Codex/Rejected lines still unreconciled |
| [#82] | Define per-repository agentic-review profiles | P3/M | 2026-08-09 | 1 · a4fc652d (2026-08-13) | live | no per-repo agentic-review profile recorded; UN-DEFERRED 2026-08-09, work untouched |
| [#99] | FLEET-HEALTH digest names the failing check per r… | P3/S | 2026-07-28 | 0 · **none** | live | fleet-health digest still prints `!! N fail` with no check name |
| [#102] | Machine-readable repo index for agent consumption | P2/M | 2026-08-09 | 1 · 7e024317 (2026-08-09) | live | pilot index unbuilt; **DEFER peg is DEAD by its own text** — see §7 |
| [#112] | adr_amend helper + ADR immutable-zone extension | P2/M | 2026-08-13 | 1 · a4fc652d (2026-08-13) | live | `scripts/hooks/adr_amend.py` absent; ADR zone still ungated |
| [#116] | Hooks hygiene | P3/S | 2026-07-28 | 0 · **none** | live | PS hooks not migrated to exec-form `args:[]`; no `if:` scope filter present |
| [#117] | Evaluate prompt/agent-based hooks | P3/S | 2026-08-11 | 1 · 7f752a89 (2026-08-11) | live | UN-DEFERRED 2026-08-11 on a met peg (`#270` closed `679d8eca`); VF-1 go/no-go unrecorded |
| [#122] | Retire the PATH shim | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "removal needs an explicit operator ask per the no-delete invariant"; Done-when = operator approves, or close as keep-for-defence-in-depth |
| [#123] | Routine observability convention + value review | P2/S | 2026-08-13 | 1 · a4fc652d (2026-08-13) | live | no `Routine:` marker convention in PLAYBOOK; no per-routine value review artifact |
| [#126] | Backpressure-loop pattern evaluation | P2/M | 2026-07-28 | 0 · **none** | awaiting-ruling | Done-when = "a go/no-go is recorded ... (or an explicit operator drop)"; the pilot executes in corp (ADR-41 queue-only here) |
| [#127] | verify skill failure-output contract | P3/S | 2026-07-28 | 0 · **none** | live | verify skill still emits the compact form on failure; no file/expected/received/directive block |
| [#130] | Memory-hygiene review | P3/S | 2026-07-28 | 1 · a4fc652d (2026-08-13) | live | no hygiene pass has run; no capture-time scrub in the gotcha write path |
| [#139] | merged-arc→record verifier | P2/L | 2026-07-28 | 0 · **none** | live | merged-arc→record verifier unbuilt; DEFER peg #170 still open |
| [#144] | Feature DoD = end-to-end / user-flow test | P3/M | 2026-07-28 | 0 · **none** | live | ADR-81 (d) carries no E2E clause; "in the cloud" target unresolved |
| [#145] | Codification-completeness pass | P3/M | 2026-08-09 | 2 · a4fc652d (2026-08-13) | live | the broader fresh-session enumeration pass has not run; UN-DEFERRED (ARC-2) |
| [#146] | De-hardcode-first doctrine + sweep | P3/S | 2026-08-06 | 2 · a4fc652d (2026-08-13) | live | clause (a) landed at `PLAYBOOK:1016-1024`; clause (b), the sweep, has not run |
| [#153] | Enforcement-completeness pass | P2/M | 2026-07-28 | 0 · **none** | live | mixed: prevention teeth + mechanize-or-accept legs buildable; two ruling legs noted in §7 |
| [#162] | Vocab decision | P2/M | 2026-08-13 | 1 · a4fc652d (2026-08-13) | live | no ADR / STANDING_RULINGS section lands the architect actor-vs-mode disambiguation |
| [#166] | doctrine_enforcement_coherence check | P3/M | 2026-07-28 | 0 · **none** | live | no `doctrine_enforcement_coherence` check in ALL_CHECKS; DEFER peg n=2 unfired |
| [#169] | Ungated-doc staleness detection | P3/M | 2026-07-28 | 0 · **none** | live | no staleness signal in the digest; depends-on #171 which is itself open |
| [#170] | Design + land the traceability-spine ADR | P3/M | 2026-08-12 | 1 · 315a0345 (2026-08-06) | live | no traceability-spine ADR; the absorbed #168 hard-gate half unratified |
| [#171] | Build the conformance dashboard at `ecosystem/con… | P3/M | 2026-08-09 | 0 · **none** | live | `ecosystem/conformance.md` **does not exist** (verified); UN-DEFERRED 2026-08-09 |
| [#181] | Coherence v2 nudge-response | P2/S | 2026-07-28 | 0 · **none** | live | nudge-response undecided; peg log gitignored + mis-cased in-row — see §8 |
| [#185] | GAP-2 deterministic gotcha-injection guard | P2/M | 2026-07-28 | 0 · **none** | live | no PreToolUse gotcha-injection guard exists |
| [#188] | Deny-rule + hook completeness audit | P3/M | 2026-07-28 | 0 · **none** | live | no coverage matrix emitted; DEFER peg (#112 arc) not landed |
| [#189] | Execute in ~/.claude | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | execute-in-`~/.claude` (queue-only here); [#456] names it operator-owned by core-invariant #6 |
| [#190] | General intra-file duplication detector | P3/M | 2026-07-28 | 0 · **none** | live | no intra-file duplication check in ALL_CHECKS; DEFER peg n=2 unfired |
| [#210] | Convert journal-wrap no-ff WARNs from per-instanc… | P3/S | 2026-07-28 | 3 · a4fc652d (2026-08-13) | live | journal-wrap no-ff class still per-instance in `disposition-register.yaml`; shape undecided+unbuilt |
| [#218] | Safe-removal gate M2+M3 boundary | P1/M | 2026-08-05 | 2 · 0bfa64b0 (2026-08-05) | live | M2+M3 legs unbuilt; DEFER peg rides [#487]'s first close batch, [#487] open |
| [#220] | MODIFY / semantic-drift axis | P2/M | 2026-08-13 | 2 · a4fc652d (2026-08-13) | live | MODIFY-axis spike unrun; no `docs/audits/` record names which organs fired |
| [#227] | Relocate AGENT_FRAMEWORK.md out of protocols/ | P3/S | 2026-07-28 | 1 · fbf4a2d0 (2026-07-01) | live | `protocols/AGENT_FRAMEWORK.md` still under `protocols/` |
| [#231] | Consumer → hub feedback report | P3/M | 2026-07-28 | 1 · 7cc4b6a6 (2026-07-01) | live | no structured consumer→hub report schema/destination; DEFER peg unfired |
| [#234] | Cross-repo probe validator | P3/S | 2026-07-28 | 2 · 5b2ccadb (2026-07-21) | live | `_FALLBACK_EXCLUDE_DIRS` still degrades a cross-repo `.claude/` probe to WARN |
| [#239] | Follow-up | P3/M | 2026-08-09 | 1 · a4fc652d (2026-08-13) | live | Informant Tier-2 still limited to the 4 deploy-manifest carriers |
| [#240] | Follow-up | P3/S | 2026-07-28 | 0 · **none** | live | Stage-3 regression WARN unbuilt; DEFER peg (mesh baseline n=2) unmet |
| [#241] | Undeclared-edge groom | P2/S | 2026-08-11 | 1 · bbacd6c0 (2026-08-11) | live | the `undeclared_edges` surfaced set is not yet all declared-or-permanently-deferred |
| [#242] | ADR status-flip coherence check | P2/M | 2026-08-04 | 0 · **none** | live | no audit leg reconciles an ADR header status against the README index |
| [#244] | Essence-spec lifecycle epic | P2/L | 2026-07-28 | 5 · 25b104ed (2026-07-04) | live | P5 hub self-prune + P6 fleet both UNOWNED (#221 closed, no successor) |
| [#245] | Add-path status-awareness | P2/M | 2026-07-28 | 0 · **none** | live | deploy add-path still blind to `status: removed` |
| [#263] | Protocols/edge-map reconciliation residuals | P3/S | 2026-07-28 | 1 · a4fc652d (2026-08-13) | live | stale `doc-code-edge.yaml` exempt entry + the two ESSENTIALS refs unreconciled |
| [#266] | Codify the test-scoped-grant language lesson | P3/S | 2026-07-28 | 1 · a4fc652d (2026-08-13) | live | grant-language guidance does not name the count/pinning-assertion inclusion |
| [#267] | Scope-exercising arc extension | P2/S | 2026-07-28 | 4 · ffe4d875 (2026-07-06) | live | no consumer measurement shows both components FIRED under a scope-matching edit |
| [#269] | Audit-index count-tiered shape + freshness hook | P3/S | 2026-07-28 | 0 · **none** | live | `docs/audits/README.md:5-6` states the count-tiered shape **is NOT built** and names this row |
| [#271] | Nightly proposal loop | P3/L | 2026-08-11 | 1 · a4fc652d (2026-08-13) | live | nightly loop not running under the §6 constraints; no 2-week survival review |
| [#273] | Changelog-review staleness escalation | P3/S | 2026-07-28 | 1 · 02389890 (2026-07-06) | live | no escalation line in the SessionStart digest; thresholds unrecorded |
| [#274] | Dogfood-signal prior in the /changelog-review ADO… | P3/S | 2026-07-28 | 2 · a4fc652d (2026-08-13) | live | the `/changelog-review` ADOPT rubric does not name the dogfood-signal prior |
| [#276] | D2 per-consumer waiver-honoring | P2/M | 2026-07-28 | 0 · **none** | live | neither deploy leg reads a `.methodology.yaml` divergence allowlist |
| [#277] | propose_closures signal repair | P2/M | 2026-08-13 | 2 · a4fc652d (2026-08-13) | live | the two STRONG false positives still surface; no better-than-49:0 run recorded |
| [#278] | Test-suite hygiene epic | P2/M | 2026-08-13 | 1 · a4fc652d (2026-08-13) | live | baseline-before-cleanup unmeasured; impacted-test selection not live |
| [#281] | Re-peg the ai-council ADR-66 story-map convergence | P2/S | 2026-07-28 | 0 · **none** | live | convergence not re-pegged to Wave-1 (or Track-X accepted) in the record |
| [#285] | Extend hub freshness gating to PLAYBOOK | P3/S | 2026-07-28 | 1 · a4fc652d (2026-08-13) | live | PLAYBOOK carries no `last_reviewed` frontmatter and is absent from `_FRESHNESS_FILES` |
| [#288] | Model-identity guard for unattended runs | P3/S | 2026-07-28 | 0 · **none** | live | no model-identity detector; ABSENT confirmed by the Wave-0 verification row |
| [#289] | Hub-own the OneDrive-Blue-Yonder guard | P2/M | 2026-07-28 | 0 · **none** | live | `block-onedrive.ps1` still per-machine in `~/.claude/hooks/`, no hub source, no carrier |
| [#293] | Consumer runbook fan-out | P3/S | 2026-08-09 | 1 · 9e6ceb63 (2026-07-08) | live | 0 of 6 consumers seeded; UN-DEFERRED 2026-08-09, work untouched |
| [#294] | `validate_backlog` deploy-carrier + `--path` de-h… | P3/M | 2026-08-09 | 1 · 71d3d7f7 (2026-07-08) | live | `validate_backlog.py` still hardcodes its BACKLOG path; no deploy carrier |
| [#296] | `audit.py repo <name> --repo-path` prints a repor… | P3/S | 2026-08-06 | 2 · 3a466bf7 (2026-08-06) | live | `audit.py repo --repo-path` still prints a path that is not written there |
| [#297] | Lightweight/dry `observe-arc` coverage mode | P3/S | 2026-08-09 | 1 · 71d3d7f7 (2026-07-08) | live | no dry/coverage `observe-arc` mode; UN-DEFERRED 2026-08-09 |
| [#298] | Handoff-generator polish | P3/S | 2026-08-09 | 1 · 71d3d7f7 (2026-07-08) | live | the three ruled generator enhancements (a)/(b)/(c) unbuilt |
| [#300] | Hermetization residual d.ii | P1/M | 2026-07-28 | 3 · e490275c (2026-07-22) | awaiting-ruling | "bundle sweep AWAITING explicit operator deletion GO (no drive-by deletion)"; Done-when leads with *the mode-boot home is ruled* |
| [#301] | Session-plan artifact class | P2/M | 2026-07-28 | 0 · **none** | live | no PLAN.md skeleton in an architect bundle; DEFER peg #298 open |
| [#303] | Make seed_runbook.py child-class-aware | P2/S | 2026-07-28 | 1 · 5eebee91 (2026-07-31) | live | `seed_runbook.py` still writes `docs/handoffs/README.md` unconditionally |
| [#305] | Add a verify-only / already-onboarded re-run mode… | P3/S | 2026-07-28 | 1 · e490275c (2026-07-22) | live | no verify-only re-run path; clause 2 needs the `preflight()` split, unbuilt |
| [#308] | Decide the `verify` skill's canonical home | P3/S | 2026-08-09 | 1 · 7e024317 (2026-08-09) | awaiting-ruling | "Decide (do not build today)" — the verify-skill home is a recorded decision |
| [#310] | Define the cold-bundle annotation surface + annot… | P3/S | 2026-08-10 | 4 · 3b711e87 (2026-08-11) | live | no sanctioned cold-annotation surface; the 07-05 bundle unannotated |
| [#317] | Default-parallel test invocation | P2/M | 2026-08-06 | 4 · 315a0345 (2026-08-06) | live | leg (a) verify-cadence parallel not pointed; D1 is operator-gated but leg (a) is not |
| [#322] | Fleet dashboard | P2/M | 2026-08-10 | 0 · **none** | live | three legs undecided; **DATED REVIEW 2026-09-09** — not yet ripe |
| [#323] | Design question | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "Decide (do not build) as a consumer-behavior policy call" |
| [#324] | Phase-6 axis-2 carrier | P3/M | 2026-07-28 | 2 · 8a091278 (2026-08-13) | live | night-batch routine + morning verdict-sheet + verb-list not codified |
| [#325] | Carry `/save` to consumers via a manifest command… | P3/S | 2026-08-09 | 1 · 7e024317 (2026-08-09) | live | carrier unbuilt; **peg #221 DEAD and unreplaced — row is stranded**, see §7 |
| [#327] | Protocols-as-interface genre ruling | P2/M | 2026-07-28 | 0 · **none** | live | corp's `protocols/README.md` markers sit UNMERGED on `docs/327-interface-genre-markers` |
| [#329] | VS Code ownership visualization | P3/S | 2026-07-28 | 1 · 36cc842a (2026-07-20) | live | no generator emits `.vscode` folder icon/colour config from the parity manifest |
| [#331] | Consumer BACKLOG schema adoption ruling | P2/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "A DECISION ticket, not the execution ... Output = an operator ruling recorded" |
| [#332] | Fleet dependency-version parity | P2/M | 2026-07-30 | 3 · 2bc02196 (2026-07-13) | live | clause 1 (versioned dependency manifest shipped with the package) unbuilt |
| [#334] | Fleet-wide ruff hook id migration `ruff` → `ruff-… | P3/S | 2026-07-28 | 1 · 97cf58e0 (2026-07-12) | live | all three repos still on the legacy `id: ruff` alias (hub `.pre-commit-config.yaml`) |
| [#335] | Exempt `templates/` from the `reconciled_versions… | P3/S | 2026-07-28 | 0 · **none** | live | `reconciled_versions` still flags the templates/ placeholder; disposition still standing |
| [#338] | codex-review drift consolidation | P2/S | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | legs (b)-(e) each unresolved; leg (a) struck by [#469] |
| [#340] | /ship pre-flight validator honors the consumer re… | P2/S | 2026-07-28 | 0 · **none** | live | `/ship` step-4 still prescribes the bare full suite |
| [#341] | Codex producer-lane activation mechanism | P2/S | 2026-08-13 | 1 · 8a091278 (2026-08-13) | live | legs (i)-(iv) unresolved; PLAYBOOK §16 describes no shipped mechanism |
| [#342] | fleet_parity gate-ahead max-fidelity hardening | P3/S | 2026-07-28 | 1 · ca8d3903 (2026-07-17) | live | the three fidelity items unbuilt |
| [#343] | fleet_parity ship-gate-only scoping | P3/S | 2026-07-28 | 0 · **none** | live | `check_fleet_parity` still runs the full walk under `audit.py health` |
| [#344] | Session-close gate for handoff generation + consu… | P2/M | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | neither Ask 1 (pre-handoff gate) nor Ask 2 (consumer PreToolUse guard) exists |
| [#345] | Externalize the ADR-101 frozensets → machine-read… | P2/M | 2026-07-28 | 0 · **none** | live | the four frozensets still live inside `scripts/validate_hermetization.py:96-172` |
| [#346] | Persist the two-tier new-path executor rule into… | P2/S | 2026-08-13 | 1 · 8a091278 (2026-08-13) | awaiting-ruling | the `~/.claude` EDIT is global-infra — "needs its own operator ruling; the behavior does not" (core-invariant #6) |
| [#347] | Formalize the engineering loop/harness end-to-end… | P2/M | 2026-08-13 | 1 · 8a091278 (2026-08-13) | awaiting-ruling | "the decomposition/design anchor, not the build"; safe-deletion is a "design question, not yet ruled" |
| [#348] | Backlog grooming as a standing routine, not ad-hoc | P3/S | 2026-08-11 | 5 · 09bce194 (2026-08-13) | live | grooming cadence not captured as a routine definition; review_date 2026-08-26 |
| [#349] | Mechanize session-discipline inheritance | P2/M | 2026-08-13 | 1 · 8a091278 (2026-08-13) | live | no boot-injected + Stop-gated test-then-close mechanism; no cold-session record |
| [#350] | Handoff-process refinements | P3/S | 2026-07-28 | 1 · 8a091278 (2026-08-13) | live | legs (a)/(b)/(c) unlanded; operator-dictated priority-program item 5 (LAST) |
| [#351] | Fleet-Python-upgrade ticket | P3/M | 2026-07-28 | 1 · 8a091278 (2026-08-13) | live | no coordinated fleet Python/target-version upgrade path defined |
| [#352] | Versioned `.vscode` region decoration | P3/S | 2026-07-28 | 4 · 3fc9458d (2026-07-20) | **dead** | _already-shipped_ — `.vscode/settings.json` `//boundary` block paints grey owner=hub / navy owner=repo keyed on markers only; CLAUDE.md carries 8+8 marker regions; landed `897577b7`; P4a shelf-life 2026-08-13 expired |
| [#353] | Session-boot contract hardening | P2/M | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | no mechanism refuses a mid-session order with unscoped side effects |
| [#354] | W6 seed-1 recurrence half | P2/M | 2026-07-28 | 0 · **none** | live | the staged-diff CO-CHANGE checker is unbuilt (the enforcement half of seed 1) |
| [#356] | RULING-W and the merge-delegation composite are L… | P2/M | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | neither RULING-W nor the merge-delegation composite carries a mechanism or a declared entry |
| [#357] | Silent-rule census run 2 | P2/M | 2026-08-13 | 2 · 8a091278 (2026-08-13) | live | the `docs/decisions/` sweep has not run; the [E8] denominator stays a floor |
| [#358] | `ecosystem/parity-surfaces.yaml` misdescribes its… | P2/S | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | `parity-surfaces.yaml:6` + `:93-94` and `fleet_parity.py:131` still say WARN-only/never-blocks |
| [#359] | PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.… | P1/M | 2026-08-12 | 0 · **none** | live | `HANDOFF_PROCESS.md:775-776` still reads "the parallelism ruling made mechanical" (verified) |
| [#361] | ADR-immutability's real coverage is declared only… | P3/S | 2026-07-31 | 3 · 8a091278 (2026-08-13) | live | the protocol still asserts four-of-four immutability while the guard scopes one deleted zone |
| [#362] | #242 carries a SUBSTANTIVE guard loss, not status… | P2/M | 2026-08-13 | 3 · 8a091278 (2026-08-13) | live | the 49 dropped MUST-rules are not enumerated or carried; blocks [#242]'s terminal status |
| [#364] | `doc_rot`'s length cap blocks [#353] from doing i… | P3/S | 2026-07-28 | 1 · 8a091278 (2026-08-13) | live | [#353] still sits under the `doc_rot` cap with no evidence-file or exemption path |
| [#365] | Promote `residual_completeness` from `exempt:` to… | P3/S | 2026-07-28 | 1 · 9f229f70 (2026-07-19) | live | `ecosystem/doc-code-edge.yaml:161` still lists `residual_completeness` under `exempt:` (verified) |
| [#366] | `residual_completeness` scans the WORKING TREE, n… | P2/S | 2026-08-13 | 1 · 8a091278 (2026-08-13) | live | `validate_residual_completeness` still reads the working tree, not the staged blob |
| [#369] | Wire `boundary_headers.py --check` into pre-commit | P3/S | 2026-08-13 | 2 · 35eb6d98 (2026-08-03) | live | `boundary_headers.py --check` is not registered in `.pre-commit-config.yaml` |
| [#371] | Consumer editor-config write-through — declared a… | P2/S | 2026-08-13 | 2 · 8a091278 (2026-08-13) | awaiting-ruling | "Vehicle decided by the buy-vs-build fleet-template ADR (intake pending) — do NOT implement bespoke"; Done-when leads with *an ADR names the carrier vehicle* |
| [#383] | Execution waves per surface | P2/L | 2026-08-13 | 7 · abbb1899 (2026-08-04) | live | 1 of 6 surfaces converged (caches wave); clause (c) operator read PENDING |
| [#385] | L4 tech-currency lane | P3/M | 2026-07-28 | 2 · 903638c5 (2026-07-26) | live | no proposal has flowed contract → ruling → deploy; depends-on 383 (open) |
| [#387] | Rewrite the buy-vs-build intake BEFORE anything i… | P2/S | 2026-08-13 | 3 · 5eb1269f (2026-08-13) | live | the buy-vs-build intake carries neither the ruled position nor a superseding doc |
| [#388] | The \"10–20 repo\" fleet-scale target is FABRICAT… | P3/S | 2026-07-28 | 2 · 31fe0e01 (2026-07-28) | live | the going-forward 5–8+ correction is not propagated to every restating surface |
| [#389] | Prompt-lint — gate the five architect fields befo… | P2/S | 2026-08-13 | 2 · 5eb1269f (2026-08-13) | live | no prompt-lint gate on the five ADR-87 fields; R6 unruled; depends-on 390 |
| [#390] | Resolve the ADR-87 effort-ownership contradiction… | P2/S | 2026-08-13 | 2 · bbacd6c0 (2026-08-11) | live | ADR-87 carries no resolution marker; `templates/prompt-template.md` effort enum still short |
| [#391] | Wire fleet_analytics into a nightly lane, or narr… | P3/S | 2026-07-28 | 1 · 423a372e (2026-07-22) | live | nothing invokes `scripts/fleet_analytics.py`; #384's nightly-lane claim still unbacked |
| [#392] | fleet_analytics rename-alias loses history on pat… | P3/S | 2026-07-28 | 0 · **none** | live | the rename-alias map still cannot represent `a→b→a`; no rename-back regression test |
| [#393] | corp-sca rot review — confirm-live-or-retire 3 ca… | P3/S | 2026-07-28 | 1 · 08aea7a7 (2026-08-08) | live | the 3 corp-sca rot candidates are neither confirmed-live nor retired |
| [#397] | scripts/ target structure — rule on the mapped gr… | P3/M | 2026-07-28 | 0 · **none** | awaiting-ruling | Done-when = "the operator rules adopt/reject on the mapped structure" |
| [#399] | `templates/handoff/v5/README.md.tmpl` — phantom s… | P2/S | 2026-08-13 | 1 · 5eb1269f (2026-08-13) | live | `HANDOFF_PROCESS.md:481`'s source claim still names a `.tmpl` no script reads |
| [#400] | Ownership-model: the hub-mandated-STRUCTURE / rep… | P3/S | 2026-07-28 | 2 · 952c10ad (2026-07-28) | live | no ownership-model ruling reaches the roster cell; the [#370] ruling stops at `~/.claude` |
| [#401] | ai-council routing still ARMED at the deleted hub… | P2/S | 2026-07-28 | 4 · 19cf25dc (2026-07-25) | live | (a) ai-council `target_projects` unfixed; (b) the ruled `routing.py` path-refusal unbuilt |
| [#402] | Intake naming clause — DEPLOY the `YYYY-MM-DD-<cl… | P3/S | 2026-07-28 | 1 · fb868199 (2026-07-23) | live | README §4 lacks the `<class>` grammar; the 4 post-ratification off-pattern docs undispositioned |
| [#403] | Extend `doc_claims` to ARCHITECTURE's machine-der… | P3/S | 2026-07-28 | 2 · 44e47b48 (2026-07-23) | live | neither carrier-set nor child-roster claims are gated by `doc_claims` or a regen-and-diff sibling |
| [#404] | gen_handoff execution-mode SUPPLEMENT leak (mode-… | P2/S | 2026-07-28 | 1 · de402b1c (2026-07-23) | live | execution-mode render still carries SUPPLEMENT framing + the unconditional P8 row |
| [#405] | Session-end leftover check — nothing verifies \"n… | P2/S | 2026-07-28 | 3 · b4dd3e48 (2026-07-27) | live | the ruled Stop-hook hygiene leg is unbuilt (ruling only, 2026-07-25) |
| [#406] | Commit-time doc_rot surfacing — an over-threshold… | P3/S | 2026-07-31 | 3 · 5eebee91 (2026-07-31) | awaiting-ruling | "Options, NONE chosen (ruling, not this filing)"; Done-when = an architect ruling picks the enforcement point |
| [#407] | Universal fleet Python style — functional-vs-OOP… | P3/M | 2026-07-31 | 1 · 5eebee91 (2026-07-31) | awaiting-ruling | "Filing only, zero build — the stance is an operator ruling, not a CC pick" |
| [#408] | Auto-coupled doc updates — closing a backlog item… | P2/M | 2026-08-13 | 3 · 5eb1269f (2026-08-13) | awaiting-ruling | per-section granularity is "an OPERATOR DECISION deliberately not settled ... the first gate on any build" |
| [#409] | Standing night batch — CODE review (formalize as… | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "ROW ONLY this session"; Done-when = defined as a routine **and ruled in or out** |
| [#410] | Standing night batch — ARCHITECTURE review (forma… | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "ROW ONLY this session"; Done-when = defined as a routine **and ruled in or out** |
| [#411] | Standing night batch — creative session, and the… | P3/S | 2026-07-28 | 0 · **none** | awaiting-ruling | "ROW ONLY this session"; Done-when = defined as a routine **and ruled in or out** |
| [#412] | Subagent / workflow routing + configured fan-out… | P3/M | 2026-07-28 | 0 · **none** | live | the Anthropic organ-set research is unrun and no routing doctrine is recorded |
| [#413] | Colors semantics — visually distinguish global/hu… | P2/S | 2026-08-13 | 2 · 5eb1269f (2026-08-13) | live | Done-when opens **on or after 2026-10-22** — not yet ripe; [#400] still open |
| [#414] | Self-acting-on-main incident family — a session c… | P2/S | 2026-08-13 | 4 · 5eb1269f (2026-08-13) | awaiting-ruling | "Organs, NONE chosen (a ruling)" — the build cannot start before the organ choice |
| [#415] | Tests must bind fixtures, not live mutable repo c… | P2/S | 2026-08-13 | 5 · 5eb1269f (2026-08-13) | live | no artifact enumerates the live-content-reading tests; only one was re-pointed |
| [#417] | `check_dirty_tree` runs with no pathspec, so the… | P3/S | 2026-07-28 | 0 · **none** | live | `session_end_backpressure.py:340-349` still calls a bare `git status --porcelain` |
| [#418] | `automation/fleet-audit` records 0–10 baselines a… | P2/S | 2026-08-13 | 1 · 5eb1269f (2026-08-13) | live | no reproduction artifact; no per-date baseline check |
| [#419] | We run routines whose output nobody consumes | P2/M | 2026-08-11 | 6 · bbacd6c0 (2026-08-11) | live | the absorb is still a habit — no trigger, no queue-depth detector, no scheduler-run check |
| [#420] | Does a TOP-LEVEL `docs/archive/` still make sense? | P3/S | 2026-07-28 | 1 · 27f033df (2026-07-25) | awaiting-ruling | "operator-raised structural question, filing only"; carries an explicit **Do NOT touch `docs/archive/`** order while open |
| [#422] | `reflow_framing`'s cold→FILLED flip is partial by… | P2/S | 2026-07-30 | 4 · 3b711e87 (2026-08-11) | live | no post-fold check FAILs on cold-state framing surviving a FILLED flip |
| [#423] | The integration sequence runs on prose every time… | P2/M | 2026-08-13 | 3 · 5eb1269f (2026-08-13) | live | `/ship` still checks no precondition; the eight steps stay prose |
| [#424] | Backlog `depends-on` gates are INERT — `_DEPID_RE… | P2/S | 2026-08-03 | 4 · 09bce194 (2026-08-13) | live | `validate_backlog.py:78` `_DEPID_RE` still requires the `#`; 2 clauses inert |
| [#425] | The suite is green on a format the file does not use | P2/S | 2026-08-13 | 4 · 781bd4ff (2026-08-13) | live | no artifact enumerates parser-facing corpora against accepted input forms |
| [#426] | Declare `consumer` + `consumption_path` for every… | P2/M | 2026-08-11 | 10 · 09bce194 (2026-08-13) | live | `routine_consumers` still gates only BACKLOG rows carrying a `· routine:` marker; review_date 2026-08-26 |
| [#427] | Region templates carry a repo-POSITION-DEPENDENT… | P3/S | 2026-07-28 | 1 · 863cb804 (2026-07-26) | live | the region templates still carry the bare hub-position `logs/TOKEN-LOG.md` path |
| [#428] | `nightly-triage` reports a dead producer to every… | P2/S | 2026-08-13 | 3 · 781bd4ff (2026-08-13) | live | `surface_triage.ps1` still reads the dead producer; the 15 Issues stay open |
| [#430] | Consumer template rejects root `conftest.py`; `fl… | P2/M | 2026-08-13 | 12 · 781bd4ff (2026-08-13) | live | (a) no ruling locator at the affected `parity-surfaces.yaml` row; (b) verdict still state-dependent |
| [#431] | `codex-review` silently drops the doc lane on any… | P2/S | 2026-07-28 | 6 · 0c64a76a (2026-08-03) | live | the mixed-diff doc-lane drop and the 0/0/0/0 counter both stand in the `~/.claude` wrapper |
| [#438] | Codify gate-class posture: terra design review BE… | P3/S | 2026-07-28 | 4 · 781bd4ff (2026-08-13) | live | PLAYBOOK carries no gate-class rule; no arc has run under it |
| [#440] | Make the `tasks/` id ledger tamper-evident — a de… | P2/S | 2026-07-28 | 2 · 78ab77b4 (2026-08-09) | live | a deleted retired `tasks/` record still frees its id with every leg green |
| [#442] | Plugin command-cache staleness — cached command t… | P2/M | 2026-07-28 | 1 · 952c10ad (2026-07-28) | live | no cache invalidation or load-time stamp on plugin command text |
| [#443] | Planning artifacts outside the three enforced cla… | P3/S | 2026-07-28 | 2 · 781bd4ff (2026-08-13) | live | handoff bundles / session plans / audit docs still carry no rent rule |
| [#445] | `codex-review` wrapper path-guard reports SUCCESS… | P2/S | 2026-07-29 | 1 · 2f924424 (2026-07-29) | live | the wrapper path-guard still reports success on a mixed diff with unreviewed prose |
| [#447] | Self-referential gate family — the committing act… | P3/S | 2026-07-30 | 3 · a54994a3 (2026-07-30) | live | a ratchet raise is still judged by the value it replaces; a wrap commit still cannot self-anchor |
| [#448] | A11 staged-diff guard — cover EVERY candidate bun… | P2/S | 2026-07-30 | 2 · a54994a3 (2026-07-30) | live | the A11 guard still verifies only `_select_active_bundle`'s pick |
| [#449] | Assembled-paste byte budget — should `PASTE_THIS.… | P3/S | 2026-07-30 | 1 · 65a549bf (2026-07-30) | awaiting-ruling | "QUESTION-SHAPED, no ruling taken"; Done-when = a ruling records a budget or an accepted-with-reason hold |
| [#450] | Per-section intake ratification — the `status:` f… | P3/S | 2026-07-30 | 0 · **none** | awaiting-ruling | "QUESTION-SHAPED, no ruling taken"; Done-when = a ruling records a schema or promotion-as-intended |
| [#451] | CA layer-edge check — port the ai-council layer-e… | P2/M | 2026-07-30 | 0 · **none** | live | no Layer-2 layer-edge check exists in the hub gate set |
| [#453] | Cloud night-run runbook — the container gaps that… | P2/M | 2026-08-13 | 3 · 781bd4ff (2026-08-13) | live | `SESSION_SETUP.md` records none of the three container gaps; no preflight unshallow/uv assert |
| [#454] | `closure_ids` negation defect — the parser reads… | P2/S | 2026-07-31 | 1 · 5eebee91 (2026-07-31) | live | `closure_ids` still reads a negated mention as a closure in both copies |
| [#456] | Ruling-blocked cohort sweep — re-route the remain… | P2/M | 2026-08-13 | 2 · 781bd4ff (2026-08-13) | live | the ~30-row ruling-blocked cohort is still un-enumerated in this row |
| [#457] | Two live-repo tests fail on main against green ga… | P2/S | 2026-08-05 | 28 · 5259b0f0 (2026-08-11) | live | both live-repo tests still fail on main for the recorded reasons |
| [#463] | win-tooling onboarding debt — 2 FAILs + 2 WARNs u… | P2/S | 2026-08-13 | 2 · 781bd4ff (2026-08-13) | live | the 2 FAILs + 2 WARNs are unchanged in `ecosystem/win-tooling/history/` |
| [#464] | corp-*/ai-council governance drift — five finding… | P2/S | 2026-08-13 | 2 · 781bd4ff (2026-08-13) | live | the five governance-drift findings are unchanged in the per-repo dailies |
| [#470] | `audit.py checks` crashes mid-listing on a cp1252… | P3/S | 2026-08-01 | 3 · 4306a46a (2026-08-04) | live | the U+2192 in `check_doc_code_edge`'s docstring first line is unswapped |
| [#477] | `deployed_methodology_version` keys the registry… | P2/S | 2026-08-03 | 2 · 8c0ed183 (2026-08-05) | live | `audit.py:2300` still keys `deployed_methodology_version` by repo-root basename |
| [#478] | `changelog_sentinel` drops PEP 440 suffixes — a p… | P2/S | 2026-08-03 | 1 · 0c64a76a (2026-08-03) | live | `changelog_sentinel.py:45-52` still discards PEP 440 suffixes |
| [#484] | ADR-106 system-Python divergence — named deferral… | P3/M | 2026-08-04 | 2 · 781bd4ff (2026-08-13) | live | the system-vs-locked Python divergence is neither closed nor permanent-deferred |
| [#485] | A shared LF-enforcing write helper — the mechanis… | P3/S | 2026-08-04 | 1 · 4306a46a (2026-08-04) | live | no shared LF-enforcing write helper; the CRLF gotcha still carries the guard |
| [#486] | `desired_state_report.py` dies on a cp1252 consol… | P3/S | 2026-08-05 | 1 · 8c0ed183 (2026-08-05) | live | the U+21C4 in `desired_state_report.py`'s HONEST LIMITS text is unswapped |
| [#487] | Closure-proposal consumption arc — repair the pip… | P2/L | 2026-08-13 | 3 · 781bd4ff (2026-08-13) | live | legs (i)-(iv) unbuilt in both copies; the ranked sheet does not exist |
| [#488] | Priority axis — the backlog has no ranking functi… | P2/M | 2026-08-05 | 0 · **none** | live | the research leg (a) has not reported measured comparisons; no axis ruling |
| [#491] | Gemini scanning lane — ruling R-G plus an accepta… | P3/S | 2026-08-05 | 2 · 781bd4ff (2026-08-13) | awaiting-ruling | Done-when leads with "the R-G one-line ruling is recorded" |
| [#492] | Grok review-lane acceptance — gated ≥ 2026-08-07,… | P3/S | 2026-08-13 | 3 · 5c6bc70d (2026-08-13) | live | peg unmet — Grok 4.6 unreleased (browser-verified 2026-08-10); **RE-CHECK 2026-08-17** |
| [#493] | B-2 investigation — the scheduled fleet-baseline… | P2/S | 2026-08-13 | 1 · 781bd4ff (2026-08-13) | live | no `docs/audits/` artifact names the cause of the scheduled-task silence |
| [#494] | Ladder ratification — L0–L5 promote-vs-leave is u… | P3/S | 2026-08-09 | 0 · **none** | awaiting-ruling | Done-when = "the ladder is ratified (or explicitly retired) by ADR"; the operative half (nothing cites L2 as authority) already binds |
| [#495] | Tech-currency cadence — give [#385] a recurring l… | P3/S | 2026-08-05 | 0 · **none** | awaiting-ruling | Done-when = "the cadence is ruled (monthly vs event-driven vs rejected)" |
| [#496] | `_ORGAN_TO_COMPONENT` attributes the pre-push org… | P3/S | 2026-08-05 | 0 · **none** | live | `enforcement_coverage.py:895` still maps the pre-push organ to `session-end-backpressure`; the test at `:619` pins the known-misfiled state |
| [#497] | Two stale claims on carrier/hook declarations | P3/S | 2026-08-05 | 4 · 315a0345 (2026-08-06) | live | both stale claims stand at `carrier_mesh.py:75` and `.pre-commit-hooks.yaml` |
| [#499] | Promote the review-artifact coverage leg to a har… | P3/M | 2026-08-05 | 4 · 3a466bf7 (2026-08-06) | live | HARD leg unbuilt; DEFER peg (0 FPs at two consecutive seals) not yet reported |
| [#500] | The Stop hook's BACKLOG advisory reads a correctl… | P3/S | 2026-08-05 | 3 · 78ab77b4 (2026-08-09) | live | the Stop advisory still reads a sanctioned row-DELETION close as nothing-closed |
| [#502] | mutmut 3.7.0 mutation-testing evaluation — CI-hosted | P3/M | 2026-08-06 | 12 · 781bd4ff (2026-08-13) | live | BLOCKED ON [#501]; the `uv run --locked` question unanswered, no CI pilot run |
| [#505] | Batch-protocol encoding — the parallel-execution… | P1/M | 2026-08-12 | 13 · bbacd6c0 (2026-08-11) | live | clause 1 live (falsified 4×); clause 2 re-pegged to the **next** batch, unmeasured |
| [#506] | Whole-set P10 grooming arc — the open set is unre… | P2/M | 2026-08-13 | 4 · 781bd4ff (2026-08-13) | live | **this census is evidence toward it, not its discharge** — the per-id verdicts are proposals only |
| [#507] | Report-only wall — decide the fourth recorded leg… | P3/S | 2026-08-07 | 1 · 945598f9 (2026-08-07) | live | the fourth report-only-wall leg is neither landed nor recorded as an accepted hold |
| [#509] | `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR` | P3/S | 2026-08-07 | 2 · 8c438220 (2026-08-07) | live | the dispatch wrapper still hands `<PROMPTS_DIR>` through unexpanded (cross-repo: win-tooling) |
| [#510] | Scope the R-1 exemption to the lanes its manifest… | P2/M | 2026-08-11 | 3 · 0136cec6 (2026-08-11) | live | all four ROSTER legs stand after the W1 grammar narrowing (`1c6d4255`) |
| [#511] | The 30-minute handoff cut is ~99.8% session autho… | P2/M | 2026-08-13 | 5 · 781bd4ff (2026-08-13) | live | no ruled cut of the non-mechanized loads in `HANDOFF_PROCESS.md`; R43/R50/R51 unlanded |
| [#514] | Two rival `LANE_BRANCH_RE` constants ship in one… | P1/M | 2026-08-11 | 2 · 0136cec6 (2026-08-11) | live | leg 1 (provisioning refusal on `KIND_UNKNOWN`) unbuilt — recorded as honest limit 3 |
| [#518] | `scripts/audit.py::_git` — one call site, two REP… | P2/S | 2026-08-09 | 1 · 7e024317 (2026-08-09) | live | `audit.py::_git` still runs without `env=` and without explicit decoding |
| [#519] | The close path is two edits, and nothing makes a… | P1/M | 2026-08-09 | 1 · 78ab77b4 (2026-08-09) | live | no test seeds a status-only close and FAILs on the generator revert |
| [#520] | No sanctioned way to retire a committed bundle wh… | P2/S | 2026-08-09 | 1 · 78ab77b4 (2026-08-09) | live | no retirement-marker surface; `check_seal_identity` still FAILs that bundle on every sweep |
| [#522] | A re-cut handoff sibling carries its predecessor'… | P2/M | 2026-08-11 | 1 · 3b711e87 (2026-08-11) | live | `--allow-suffix` still writes a sibling with no predecessor named |
| [#523] | Executive-index render leg on the generated `BACK… | P2/M | 2026-08-14 | 1 · d5d74612 (2026-08-12) | live | `BACKLOG.md` opens with no P1→P3 index (verified); no `--status` render mode |
| [#524] | Four ruled check extensions — the N2 set, Codex-p… | P2/S | 2026-08-13 | 2 · 62f42dad (2026-08-14) | **dead** | _already-shipped_ — all four legs on main at `62f42dad`; `scripts/audit.py:3970` (a), `scripts/validate_backlog.py:355` (b), `scripts/journal_anchor.py:238` (c), `scripts/audit.py:1660` (d); packet §2 reads **Complete.** |
| [#526] | Root-hygiene audit — which root files MUST be roo… | P3/S | 2026-08-14 | 0 · **none** | live | born 2026-08-14; no root-hygiene audit artifact exists yet |
| [#527] | Anti-direct-to-main mechanism — a commit-time loc… | P2/S | 2026-08-14 | 0 · **none** | live | born 2026-08-14; no pre-commit hook refuses a non-merge commit on `main` |
| [#528] | Lane-latency — the full suite multiplied by per-l… | P1/M | 2026-08-14 | 0 · **none** | live | born 2026-08-14; gate-run call sites, the tiered-suite rule and the telemetry leg all unlanded |

---

**Generated** 2026-08-14 by the read-only night-2 census lane on `claude/night2-census-audit-btqr42`, base `main` @ `7bbb067`.
**Zero edits beyond this file.** No close is executed by this artifact; every verdict above is a proposal for the booted architect's P10 pass ([#506]).
