# Ruling provenance audit — which architect rulings never landed?

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** ruling-provenance-audit
- **Source-session:** CLOUD lane `CLOUD-C2-ruling-provenance-audit`, branch
  `claude/ruling-provenance-audit`, cut from `main` @ `aeec0fd1` (detached HEAD at boot, branched
  before any write)
- **Status:** complete — READ-ONLY audit. One artifact plus a `JOURNAL.md` entry; no other file
  mutated. `protocols/STANDING_RULINGS.md` was **not** written to. No root `AGENTS.md` was created.
- **Model-in-effect:** configured `claude-opus-5` (the serving model may differ; declared per
  ADR-80 §5 rather than asserted)

---

## 0. Interpreter declaration (container check, executed before any measurement)

The brief required a probe, not an assumption. Both version strings, verbatim:

```
uv --version                      -> uv 0.8.17
pyproject.toml [tool.uv] line 25  -> required-version = "==0.11.19"
uv run --locked python --version  -> error: Required uv version `==0.11.19` does not match
                                     the running version `0.8.17`.
```

**MISMATCH.** The `uv run --locked` mesh refuses to run in this container, so every measurement
below was hand-run under the container interpreter:

```
python3 --version                 -> Python 3.11.15
pyproject.toml requires-python    -> ">=3.12"
.python-version (repo floor)      -> 3.12.10
```

**Stated as a limit rather than glossed:** the hand-run interpreter is itself *below* the repo's
declared floor. Every measurement in this artifact is either a pure-stdlib text read (regex over
`.md` files) or one import of `scripts/validate_hermetization.py`, which imported and executed
cleanly under 3.11.15 — its ADR-101 sanctioned-set logic is plain `frozenset` membership with no
3.12-only syntax. No gate, no test suite and no `audit.py` check was run, because none of them
would be running under their pinned toolchain and a green result from an unpinned mesh is worth
less than no result. D1 of the register (*"The exact `uv` pin is load-bearing for the entire organ
mesh"*) is the reason this is declared rather than routed around.

---

## 1. Step 1 — census of the register

`protocols/STANDING_RULINGS.md` read in full: **2,001 lines, 18 lettered sections (A–R)**.

### 1.1 The count

Two numbers, because the file carries two entry forms and one number would hide that:

```
heading-form entries (### / ####)                                    83
  minus 1 retirement marker  (#### H4 · RETIRED 2026-08-11)
  minus 2 container headings (### I-D · the DEFAULT BLOCK;
                              ### Q · The window-close block)
  minus 1 bookkeeping record (### Q · Anti-orphan discharge)
  = named single-ruling entries                                      79

block-form bullet rulings (no heading of their own)
  C  session-plan decisions              6
  I-D default block                     28
  J  batch-4 integration                 6
  K  window-close operator rulings       2
  Q  window-close block (Q1-Q10)        10
  = block-form rulings                                               52

TOTAL enumerated ruling units in the register                       131
```

Plus, held **by reference rather than transcribed**: section M declares *"the 2026-08-12
adjudication — per-item dispositions (**143 items**)"*, printed as 150 ids across M-1…M-11 and
reconciled in the file itself (`150 − 5 − 2 = 143`). Those 143 are summarized by 11 of the 79
entries; their per-item verdicts come from an off-repo sheet (`PICKER-2026-08-12-annotated.md`).

### 1.2 Coverage by date — the register's own shape

| Section | Window | Entries |
|---|---|---|
| A, C | 2026-08-05 | 6 + 6 |
| D, E | 2026-08-06 | 4 + 1 |
| F | 2026-08-07 | 6 |
| G | 2026-08-08 | 3 |
| H | 2026-08-09 | 4 (+1 retirement marker) |
| I | 2026-08-10 | 9 named + 28 block |
| J | 2026-08-11 | 6 |
| K | 2026-08-11/12 **and** 2026-08-16 | 2 |
| L, M | 2026-08-12 | 11 + 11 (covering 143) |
| N | 2026-08-13 | 3 |
| O | 2026-08-14 | 3 |
| P | 2026-08-19 | 2 |
| Q | 2026-08-19/20 | 10 |
| R | 2026-08-22 | 2 |
| B | undated / cross-window | 7 |

**Zero entries carry the dates 2026-08-15, 2026-08-17, 2026-08-18, 2026-08-21 or 2026-08-23.**
2026-08-16 is represented by exactly one entry (K-2), filed under a 2026-08-11/12 section heading.
Measured directly: `grep -c "2026-08-21"` → **0**; `grep -c "2026-08-23"` → **0**.

### 1.3 Does the file have a schema? — **No, and that is a finding**

There is no required-field grammar, and nothing validates one:

- **No id grammar.** Live id forms include `A1`, `B5`, `D1`, `F3`, `G2`, `I-P0`, `I-D9`, `I-F3`,
  `I-I2`, `J-1`, `K-1`, `L-11`, `M-7`, `N-3`, `O-1`, `P-2`, `Q7`, `R-1` — hyphenated and
  un-hyphenated, section-prefixed and not, in the same file.
- **No required date field.** Dates appear in section headings, in prose, or not at all.
- **No required mechanism field.** By keyword scan (`audit.py|check_|scripts/|pre-commit|hook|
  gate|validate_`), **34 of 83** heading entries name any enforcing mechanism.
- **`Expiry` is present on 24 of 83** heading entries, despite the register's own A2 entry ruling
  that *"every disposition or exemption names its own expiry so it cannot outlive its reason."*
  The register does not conform to the rule it carries.
- **The one machine-checked field is opt-in and rare.** `scripts/audit.py::check_landing_predicate`
  (logic in `scripts/validate_landing_predicate.py`) reads only fenced ```` ```landed ```` blocks.
  **5 of 83** entries carry one (F2, N-1, N-2, N-3, R-2). An entry with no block is invisible to
  the gate — and the gate returns `pass` with *"no landed: predicates declared"* when none exist,
  so a register of zero declarations passes cleanly.

No pre-commit hook targets `protocols/STANDING_RULINGS.md`. A hand-edited, mis-dated, id-colliding
or truncated register commits without complaint. **A register whose entries have no required
fields cannot be checked for completeness, which is precisely the property this audit was asked to
measure.**

### 1.4 The register's declared scope — load-bearing for every verdict below

> *"One repo file carrying the operating rulings that were ratified in chat and **have no other
> landed home yet**."* — `protocols/STANDING_RULINGS.md:3-4`

> *"Where an entry names a declared durable home … that home stays the doctrinal destination; this
> register is the **application surface** in the meantime, and an entry is retired from here once
> its declared home carries it."* — `:22-25`

So **"absent from the register" is not by itself drift.** A ruling that landed in an ADR, a row
body, a PLAYBOOK chapter or a rule file is *correctly* absent. This audit therefore reports two
distinct tallies — register-absent-but-landed, and landed-nowhere — and only the second is the
landing gap the lane exists to size.

---

## 2. Step 2 — rulings that live only in artifacts

### 2.1 Method, stated so the negatives are bounded

1. Full read of `protocols/STANDING_RULINGS.md` (2,001 lines).
2. Regex sweep of **all 693 files in `docs/audits/`** for eight ruling markers: `operator ruling`,
   `architect ruling`, `operator ruled`, `architect ruled`, `RULED <date>`, `RULED:`,
   `(architect, 20…` / `(operator, 20…`, `ruling of 20…` / `ruled 20…` (case-insensitive).
   → **156 files, 321 marker lines**, spanning 2026-06-23 to 2026-08-23.
3. The subset dated within the register's live period (**2026-08-05 → 2026-08-23**) enumerated
   line-by-line and read in context — the register did not exist before 2026-08-05, so a
   pre-registry ruling is out of scope for a landing question.
4. Each distinct ruling **set** cross-checked against the register by subject grep.
5. Named ruling sets and their claimed carriers verified against `tasks/`, `BACKLOG.md`,
   `JOURNAL.md`, `docs/decisions/`, `protocols/`, `CLAUDE.md` and the active handoff bundle.

**The calibration case surfaced under this method** (§2.3), which is the check the brief set. It
did not surface from the audit corpus alone: the `[#171]` claim has *no* ruling-marker line
anywhere in `docs/audits/`. It surfaced only because step 5 read the active handoff bundle. That
is a real limit of an audits-only sweep, recorded rather than smoothed over — **the method as
briefed was insufficient, and was widened.**

### 2.2 The census table

`id/subject · where recorded · in register? · date`. **Merit is not assessed anywhere below.**

| # | Ruling set / act | Date | Where recorded | In register? |
|---|---|---|---|---|
| 1 | Q7 register A1–A6 | 08-05 | handoff `SUPPLEMENT.md` (off-repo-issued) | **YES** — §A |
| 2 | Session-plan §H R-7 decisions (6) | 08-05 | off-repo session plan | **YES** — §C |
| 3 | V-1 lessons D1–D4 | 08-06 | — | **YES** — §D |
| 4 | E1 gap-weeks rule | 08-06 | intake #26 | **YES** — §E |
| 5 | Batch-2 arc F1–F6 | 08-07 | `2026-08-07-technical-batch-2-packet.md` | **YES** — §F |
| 6 | `max` held out of dispatch routing | 08-07 | `2026-08-21-technical-ch8-dispatch-codification.md:331` | **NO** |
| 7 | Batch-3 GO G1–G3 | 08-08 | — | **YES** — §G |
| 8 | Option (A) of batch-3 consolidation §8 | 08-08 | `2026-08-08-technical-batch-3-manifest.md:12` | **NO** |
| 9 | Batch-night dispatch authority (evening) | 08-08 | `2026-08-09-technical-batch-night-manifest.md:11` | **NO** |
| 10 | ARC-3 H1–H4 | 08-09 | — | **YES** — §H |
| 11 | ARC-9 seat-27 checklist (37 units) | 08-10 | off-repo `RULING-CHECKLIST-2026-08-10.md` | **YES** — §I |
| 12 | Batch-4 integration J-1…J-6 | 08-11 | batch-4 manifest amendment | **YES** — §J |
| 13 | Organ-index home; `scripts/audit_checks/` home | 08-11/16 | — | **YES** — §K |
| 14 | Adjudication-hour L-1…L-11 + 143 items | 08-12 | off-repo `PICKER-2026-08-12-annotated.md` | **YES** — §L/§M |
| 15 | `[#513]` landing predicates N-1…N-3 | 08-13 | — | **YES** — §N |
| 16 | Baseline re-pins O-1…O-3 | 08-14 | — | **YES** — §O |
| 17 | **Morning adjudication `D1.1–D1.7` + `D5.1–D5.3` (10)** | 08-15 | off-repo `MORNING-ADJUDICATION-2026-08-15.md`; **4 of 10** cited in-repo | **NO** |
| 18 | Phase-1 architect rulings `R1–R7` (7) | 08-15 | `2026-08-15-technical-batch-phase1-packet.md` §7, all seven verbatim + discharge | **NO** (landed) |
| 19 | Architect ruling `R3` — terra Layer-2 claim rejected | 08-15 | `2026-08-15-codex-p-review.md:63` (record of adjudication is off-repo) | **NO** |
| 20 | **Night-3 decision queue `D1–D14` (14)** | 08-15/16 | queue artifact carries **proposals**; picks visible only as JOURNAL outcomes | **NO** |
| 21 | **Phase-2 architect rulings `§A1–§A10` (10)** | 08-16 | off-repo `PHASE2-MAX-PACK.md`; **3 of 10** cited in-repo | **NO** |
| 22 | Architect ruling `D-1v2` — amended roster of 11 | 08-16 | `2026-08-16-technical-batch-6-manifest.md:192` AMENDMENT 1 | **NO** (K-2 cites it) |
| 23 | *"ADR-60 wins — a task row's stated path never overrides…"* | 08-16 | `2026-08-16-technical-k-293-…-lane-packet.md:107` | **NO** |
| 24 | **Architect standing ruling — audit-to-row conversion authority** | 08-17 | `2026-08-17-technical-batch-7a-manifest.md`, verbatim | **NO** |
| 25 | Architect ruled REGENERATE on the live tree | 08-18 | `2026-08-18-technical-p10-regen-lane-contract.md:8` | **NO** (discharged) |
| 26 | P-1 / P-2 anti-orphan | 08-19 | — | **YES** — §P |
| 27 | Architect ruling `b′` — N4 landing | 08-19 | `2026-08-19-technical-s1-seat-arc-contract.md:17` | **NO** |
| 28 | Window-close Q1–Q10 | 08-19/20 | off-repo chat window | **YES** — §Q |
| 29 | Architect batch `R1–R6` of 2026-08-20 (6) | 08-20 | `2026-08-22-technical-annotation-and-rulings-ledger.md` §2, verbatim + row bodies | **NO** (deliberate) |
| 30 | Parallel-flip APPROVED | 08-20 | `2026-08-20-technical-parallel-flip-lane-contract.md:10` | **NO** |
| 31 | Codespaces substrate / never-meter-buy | 08-20 | ledger §1.5 + `2026-08-20-technical-codespaces-audit.md` | **NO** |
| 32 | Library choice RULED — `rustworkx` | 08-21 | `2026-08-21-technical-graph-and-workflows-lane-contract.md:30` | **NO** |
| 33 | Batch-1 contract grandfathering (*"cutover ruled"*) | 08-21 | `CLAUDE.md` §9 `lane-contract-check` row | **NO** |
| 34 | **Cloud-wave close batched ruling — 9 disposition lines** | 08-22 | `2026-08-22-technical-cloud-wave-close-funnel.md` Amendment A1 | **PARTIAL** — 2 of 9 (§R-1, §R-2) |
| 35 | Ruling `B3a/B5` — annotation/ruling destination | 08-22 | ledger header, `:3-5` | **NO** |
| 36 | Architect DEFERRAL on `[#491]` | 08-22 | ledger §5.3 | **NO** |
| 37 | ADMISSION VERDICT (architect) | 08-23 | ledger §5.1, verbatim fenced block | **NO** |
| 38 | Top-10 items 8/9/10 *"YES as written"* | 08-23 | `2026-08-23-technical-lane-docs-governance.md:13` | **NO** |
| 39 | **`[#171]` leg 1 = option (b)** *(calibration)* | undated | **claimed** in handoff `SUPPLEMENT.md:75`; refuted elsewhere in the same bundle | **NO** |

**Tally.** 39 ruling sets discoverable in the register's live period. **15 are carried by the
register. 24 are not.** Of those 24:

- **20 are register-absent but landed in another in-repo surface** — a manifest, a packet, a lane
  contract, the rulings ledger, a row body, `CLAUDE.md` §9. By §1.4's scope boundary these are not
  drift; several (18, 25, 29) are batch-scoped rulings that expired on discharge and were never
  owed an entry.
- **4 are landed nowhere in full** — rows 17, 20, 21 and 39. These are the landing gap.

### 2.3 The unlanded four, quoted

#### 39 — `[#171]` leg 1 / F3 option (b) — the calibration case. **CONFIRMED unlanded.**

Four negative searches and one positive quote.

*Negative 1 — the register.* `grep -n "171" protocols/STANDING_RULINGS.md` → **no output.**
Aliases return zero as well: `conformance dashboard` (0), `gen_dashboard` (0), `ADR-86` (0),
`writer policy` (0).

*Negative 2 — the audits corpus.* No file in `docs/audits/` carries a ruling-marker line naming
`[#171]`. The only `[#171]` lines in ruling context are the finding that **asks** for the ruling:

> `docs/audits/2026-08-23-technical-window-seal.md:183`
> `| **F3 — [#171] leg 1** | The generator claims to commit its own output and has no commit path | **P1; blocks [#171]; needs the architect's (a)/(b)** |`

*Negative 3 — a prior lane already refuted the claim in writing.*

> `docs/audits/2026-08-23-technical-phase0-preconditions.md:425`
> `| **A** | [#171] leg 1 is **already ruled as option (b)** — an execution item, not a fork | **REFUTED** |`

> `:774` — *"Premise A found leg 1 is an **unruled (a)/(b) fork**, not an execution item. L4 cannot
> execute a ruling that does not exist."*

*Negative 4 — the active handoff bundle contradicts itself on this exact point.* Two of its files
say the fork is open:

> `docs/handoffs/2026-08-23-dev-knowledge-architect/RESIDUAL.md:62` (identical at
> `PASTE_THIS.md:344`) — *"**2. `[#171]` leg 1 — (a) or (b), and R3 says do not leave (c).** …
> Either implement the ADR-80 writer policy, or rule that human-committed satisfies "committed"
> and amend ADR-86 §2 plus the two artifact strings."*

*The positive quote — the single in-repo trace of the claimed ruling*, in the same bundle:

> `docs/handoffs/2026-08-23-dev-knowledge-architect/SUPPLEMENT.md:75-76`
> *"4. OPEN QUESTIONS (deliberately deferred): [#171] leg 1 execution under my standing (b)
> ruling (human-committed satisfies "committed" + ADR-86 amendment — **ruled, unexecuted**);"*

**Where it does appear:** one line of a handoff supplement, as a first-person assertion that a
ruling exists. **Where it should appear:** `protocols/STANDING_RULINGS.md` (it is an operating
disposition ratified in chat with no other landed home — the register's declared class), and
`tasks/171-…md` / the regenerated `BACKLOG.md`, whose Done-when leg 1 is the thing the ruling
resolves. It is in neither. Its own bundle files it under *OPEN QUESTIONS* while calling it
*ruled* — the ruling and its absence are asserted six lines apart.

#### 21 — Phase-2 architect rulings `§A1–§A10` (2026-08-16). **7 of 10 unlanded.**

> `docs/audits/2026-08-16-technical-batch-6-manifest.md:15`
> *"**Authority:** the phase-2 architect rulings §A1–§A10 of 2026-08-16, issued on
> `PHASE2-MAX-PACK.md`"* — an operator-side file, off-repo.

Neither the manifest nor `2026-08-16-technical-batch-6-packet.md` enumerates them; the packet
contains **zero** `§A` references. A verification lane measured the same gap the same week:

> `docs/audits/2026-08-16-verification-nb4-equilibrium.md:114`
> `| B11 | **— pick** §A1–§A10 (10 rulings) | §A3/§A4/§A6 cited at JOURNAL.md 2026-08-16 (b) and CLAUDE.md §12 v2.61 | **JUDGMENT** |`

Repo-wide grep confirms it: `§A4` and `§A6` and `§A10` appear in `JOURNAL.md` 2026-08-16 prose;
`§A1`, `§A2`, `§A5`, `§A7`, `§A8`, `§A9` have **no in-repo carrier of any kind** (the `§A2`/`§A5`/
`§A6`/`§A7`/`§A9` hits elsewhere in the tree are ADR-85 amendment sections — a different, colliding
namespace). **Where they should appear:** the register, or the batch-6 packet's discharge table,
which is the shape phase-1 used one day earlier and which works (row 18).

#### 17 — Morning adjudication `D1.1–D1.7` + `D5.1–D5.3` (2026-08-15). **6 of 10 unlanded.**

> `docs/audits/2026-08-16-verification-nb4-equilibrium.md:106`
> `| B2 | **— pick** D1.1–D1.7, D5.1–D5.3 (10 rulings) | D1.1 at JOURNAL.md 2026-08-15 (a); D1.3 at CLAUDE.md §12 v2.59; D1.7 at JOURNAL.md 2026-08-16 (b); D5.3 verbatim in docs/audits/2026-08-15-technical-527-block-main-lane-contract.md:2 | **JUDGMENT** |`

Four of ten have a named in-repo carrier. `D1.2`, `D1.4`, `D1.5`, `D1.6`, `D5.1`, `D5.2` have none;
the source of record is `MORNING-ADJUDICATION-2026-08-15.md`, off-repo.

#### 20 — Night-3 decision queue `D1–D14` (2026-08-15/16). **Ruling texts unlanded.**

The queue artifact is in-repo and explicitly binds nothing —
> *"the queue's own §8 **'Everything here is a proposal'**; outcomes visible at `JOURNAL.md`
> 2026-08-16 (a)/(b)"* (`2026-08-16-verification-nb4-equilibrium.md:112`)

so the **proposals** landed and the **picks** did not: what a reader can recover is a set of
downstream effects in JOURNAL prose, not fourteen decisions with their reasons. Same artifact
records the aggravating factor:

> `:117-122` — *"the window ran **four distinct ruling namespaces** — `D1.x`/`D5.x`, `R1–R7`,
> `§A1–§A10` — plus a **second, colliding `D`-series** in the night-3 queue (`D1–D14`) … Nothing in
> the tree distinguishes them; a reader resolves the collision by date-and-context or not at all."*

### 2.4 Two register-absent rulings worth naming even though they landed

Neither is in the unlanded four, but both are the register's declared class — general operating
rules with no expiry — sitting in an immutable artifact for a closed batch:

**Row 24, quoted in full because it is still binding today:**

> `docs/audits/2026-08-17-technical-batch-7a-manifest.md`, *"The architect standing ruling this
> batch executes"*: *"**Audit-to-row conversion authority, 2026-08-17.** Every audit artifact
> carries exactly one disposition: **ACTIONED** … **FILED** … **REJECTED** … **SUPERSEDED** … An
> undisposed audit is a defect, not a document."*

**Row 35**, which created the destination this window's verdicts land in:

> `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md:3-5` — *"**Sanctioned
> destination for verdict blocks and verbatim ruling texts, per the architect's ruling B3a/B5 of
> 2026-08-22.** That ruling SUPERSEDES the earlier 'land verbatim in the row body' instruction."*

A standing ruling whose only home is a manifest for a batch that closed on 2026-08-17 is one
`git log` away from being unfindable by the seat that needs it.

---

## 3. Step 3 — was root `AGENTS.md` ruled ADMITTED?

**Verdict: the ruling EXISTS and IS LANDED. The reading it rests on is NOT borne by ADR-53's text.
And a live gate blocks the file the ruling admits.** Three answers, not one.

### 3.1 Does ADR-53 bear the narrow reading? — **NO.**

`docs/decisions/ADR-53-claude-md-single-instruction-file.md`, read in full (49 lines). The
operative text:

> **`:23`** — *"1. **`CLAUDE.md` is the single canonical per-repo agent-instruction file.** ADR-52
> is superseded."*

> **`:25`** — *"2. **`AGENTS.md` as a separate per-repo file is retired.** Existing `AGENTS.md`
> files in `.dev-knowledge` and `ai-council` are to be removed and their content merged into each
> repo's `CLAUDE.md`."*

> **`:29`** — *"4. **CLAUDE.md — formerly defined as a thin pointer to AGENTS.md — is now the
> substantive single canonical per-repo agent-instruction file.**"*

And, decisively, the alternative the ADR considered and rejected:

> **`:47`** — *"- **Keep AGENTS.md alongside CLAUDE.md, with CLAUDE.md as a thin pointer** —
> rejected: perpetuates the two-file drift problem without benefit; both tools read CLAUDE.md
> directly, making any pointer model unnecessary overhead."*

**The phrase "two content-carrying files" appears nowhere in ADR-53.** Decision 2 names the file,
by name, and retires it; Decision 4 records that CLAUDE.md *was* a thin pointer to AGENTS.md and
that this is precisely what was undone. The shape R-1 admits — `AGENTS.md` carrying the portable
layer, `CLAUDE.md` keeping the remainder *and pointing at it* — is materially the alternative at
`:47`, which ADR-53 rejected on the ground that a pointer model is *"unnecessary overhead"* and
perpetuates *"the two-file drift problem."*

So R-1 is a **reinterpretation over** ADR-53, not a **reading of** it. That is not this audit's
opinion; it is what the decision packet's own routing note said *before* the ruling was made:

> `docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md:74` — *"The reading of a ratified
> ADR cannot be settled by an intake. **ADR-53 Decision 2 would need explicit supersession** — and
> the packet's own point is that a *silent* reinterpretation is the exact drift ADR-53 exists to
> end."*

R-1 itself half-concedes the point (*"a silent reinterpretation of a ruling is precisely the drift
ADR-53 was written to end, so the reading is recorded as a ruling rather than inferred"*), and the
register it lives in states its own limit: *"It is not an ADR and does not supersede one"*
(`:20`). **ADR-53 Decision 2 stands un-superseded, Status `Accepted`, today.** The two surfaces
disagree on the record. Which one governs is a question for the architect; this audit only reports
that the disagreement is live and unrecorded as such.

### 3.2 Does a ruling admitting root `AGENTS.md` exist in-repo? — **YES.** Three quoted carriers.

**(a) The register**, `protocols/STANDING_RULINGS.md:1920-1926`:

> *"### R-1 · `AGENTS.md` is ADMITTED, on the substance reading of ADR-53*
> *> ADR-53 Decision 2 forbids **two files that both carry content**, not the filename
> `AGENTS.md`. A root `AGENTS.md` carrying the portable layer, paired with a `CLAUDE.md` that
> keeps the Claude-runtime-specific remainder and points at it, satisfies the substance ADR-53
> protects — one place where doctrine lives — and is admitted on that reading."*

**(b) The funnel table's disposition line**,
`docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md:208`:

> `| **A2** \`AGENTS.md\` | **ADMITTED** — the size objection is dead (16.9 KiB headroom) and ADR-53 forbids two content-carrying files, not the name | \`protocols/STANDING_RULINGS.md\` **R-1**; execution filed as the bounded lane \`[#577]\` |`

**(c) Provenance, verified rather than assumed.** Section R entered the register in commit
`2af03f3` (*"docs(playbook,rulings,audits): D6 codification + the ruling recorded at its three
homes"*), dated **2026-08-22**, and `git merge-base --is-ancestor 2af03f3 origin/main` → **true**.

**This claim verifies.** It is the one claim in this audit that the brief flagged as suspect and
that survives its own check. The A2 line is also the counter-example to §2's pattern: it is a
batched chat ruling that reached a funnel table *and* the register the same day.

### 3.3 What does `[#577]`'s own row say it carries?

`tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md:13` (identical text at
`BACKLOG.md:229`), the load-bearing clauses:

> *"- [#577] [P2][M] **Adopt `AGENTS.md` as the portable instruction layer — the bounded execution
> lane** — **RULED ADMITTED (architect, 2026-08-22); this row is the execution, not the decision.**
> … **the doctrine reading is ruled** — ADR-53 forbids *two content-carrying files*, not the
> filename, so a one-line pointer preserves the substance ADR-53 protects. **Bounds, all four
> binding:** (1) `AGENTS.md` is **≤120 lines** … (4) the **guard is stated in BYTES, not lines** …
> **`CLAUDE.md` §10's first anti-pattern bullet is now false doctrine** ("Narrating or managing
> AGENTS.md — AGENTS.md is retired") and is inverted or deleted by this lane … **Gemini's
> `.gemini/settings.json` is explicitly NOT admitted** — it would be a new top-level directory that
> `validate_hermetization.py` Rule A blocks absent an ADR-101 §1 amendment …"*

> *"· Done when: **a root `AGENTS.md` ≤120 lines exists** carrying the portable layer, `CLAUDE.md`
> carries only the Claude-runtime remainder plus the permitted pointer, the combined global+root
> payload is asserted **in bytes** against the 32 KiB cap by a test, the scope resolution for the
> `~/.codex` collision is stated in the `AGENTS.md` header, and `CLAUDE.md` §10's retired-AGENTS.md
> anti-pattern is corrected in the same commit"*

So `[#577]` is the AGENTS.md execution lane, confirmed independently at
`docs/audits/2026-08-23-technical-phase0-preconditions.md:429` (*"premise E … ARCHITECT CORRECT;
mandate REFUTED"*) — it is **not** a provider-configuration carrier.

### 3.4 Is there a rule barring new repo-root files? — **YES, and it blocks `AGENTS.md`.**

`docs/decisions/ADR-101-…md:37`:

> *"- **Tier-1 — repo root.** Sanctioned directories: … Sanctioned file **classes** … living docs
> `UPPERCASE.md` (`VISION ARCHITECTURE CLAUDE CONTRIBUTING JOURNAL LESSONS BACKLOG`); dotfile/tool
> config … build/package manifests …"*

`:38`:

> *"- **Refused:** any **new** Tier-1 top-level directory, **any new Tier-1 top-level file outside
> a sanctioned class**, or any new `docs/<genre>/` folder."*

Mechanized as Rule A in `scripts/validate_hermetization.py` (pre-commit hook
`validate-hermetization`, prospective-only on staged ADDs). **Executed, not inferred** — the
module imported and the classifier called directly:

```
>>> validate_hermetization.classify('AGENTS.md')
"unsanctioned new top-level file 'AGENTS.md' -- Tier-1 files are a closed class
 (ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a drive-by add"

>>> 'AGENTS.md' in validate_hermetization.SANCTIONED_TIER1_FILES
False
>>> sorted(canonical_docs.CANONICAL_MANDATORY)
['ARCHITECTURE.md','BACKLOG.md','CLAUDE.md','CONTRIBUTING.md','JOURNAL.md','LESSONS.md','VISION.md']

>>> validate_hermetization.classify('codex/AGENTS.md')      -> None   (admitted; home is sanctioned)
>>> validate_hermetization.classify('.gemini/settings.json') -> "unsanctioned new top-level directory '.gemini/' …"
```

**Yes, `AGENTS.md` falls under it.** A staged add of root `AGENTS.md` is BLOCKED by the same Rule A
that R-1 and `[#577]` invoke — in the very sentence where they refuse `.gemini/settings.json` — to
justify refusing Gemini. **The ruling applied Rule A to the thing it refused and not to the thing it
admitted.** No ADR-101 §1 amendment admitting `AGENTS.md` exists: the amendment log runs
`.methodology.yaml` (07-13), `uv.lock`/`.python-version` (07-27), `tasks/` (07-27), `.github/`
(08-06), `.devcontainer/` (08-18) — and stops.

**Consequence, stated as fact rather than as a proposal:** `[#577]`'s Done-when (*"a root
`AGENTS.md` ≤120 lines exists"*) cannot be satisfied by any lane through the armed gate. The
available paths are `git commit --no-verify`, or an ADR-101 §1 amendment. Which one is the
architect's call; that there is no third is not.

*(Incidental, since it bears on the "does the name offend?" question: `codex/AGENTS.md` already
exists in the tracked tree and passes cleanly. What ADR-101 refuses is the **root** placement, not
the filename.)*

### 3.5 Step 3 verdict, compressed

| Question | Answer |
|---|---|
| ADR-53 bears the narrow reading? | **NO** — the phrase is absent; Decision 2 names the file; the admitted shape is materially the `:47` rejected alternative |
| A ruling admitting root `AGENTS.md` exists in-repo? | **YES** — register R-1, funnel line A2, row `[#577]`; landed `2af03f3`, on `origin/main` |
| `[#577]` carries it? | **YES** — *"RULED ADMITTED (architect, 2026-08-22); this row is the execution, not the decision"* |
| A rule bars new repo-root files? | **YES** — ADR-101 §1 / Rule A; **`AGENTS.md` falls under it**, verified by executing the classifier |

**The brief's suspicion was half right and it matters which half.** The *ruling* is not a phantom —
this one landed properly and the paperwork is clean. What does not survive checking is the *reason
given for it* and the *feasibility of executing it*: ADR-53 does not say what the ruling says it
says, and the gate refuses the file the ruling admits.

---

## 4. Step 4 — the shape of the gap

**24 of 39 ruling sets are absent from the register; 4 are absent from the repo entirely.** The
misses are not scattered. Five clusterings, each measured:

**(1) By window — a clean break on 2026-08-15.** Register coverage is *contiguous* from 2026-08-05
to 2026-08-14: every window in that span has a dated section. From 2026-08-15 onward it is
episodic — **0** entries for 08-15, 08-17, 08-18, 08-21, 08-23; **1** for 08-16; **2** each for
08-19/20 and 08-22. All four unlanded sets fall on or after 08-15, three of them inside the
08-15/08-16 window alone.

**(2) By issuance channel — off-repo pack, cited but never transcribed.** The register's own
sections cite off-repo sources too (§A a supplement, §I `RULING-CHECKLIST-2026-08-10.md`, §L/§M
`PICKER-2026-08-12-annotated.md`) — and those landed, because a seat was running whose *job* was
the transcription. Sections Q and R name that seat explicitly (*"transcription seat"*, *"landed the
day after they were given"*). **The variable is not the channel. It is whether a transcription seat
ran.** Where one did, an off-repo pack of 143 items landed in full. Where none did, a pack of 10
rulings left three citations.

**(3) By arc position — wave-close lands, mid-arc does not.** Every register section after §O is a
*close* artifact: P (night-adjudication), Q (window-close), R (wave-close funnel). Every unlanded
or artifact-only ruling was issued **mid-arc** — at dispatch (rows 8, 9, 22, 24), at integration
(17, 18, 21), inside a lane (25, 30, 32), or over a running fork (39). A mid-arc ruling lands in
the artifact of the arc that consumed it; `docs/audits/` is immutable, that arc closes, and the
ruling's only home is a document that describes a finished batch.

**(4) By generality — the wrong ones are missing.** Batch-scoped rulings that expire on discharge
(rows 18, 25, 29) are *correctly* absent under §1.4. The register-absent set that actually matters
is the standing, expiry-free operating rules: the 08-17 audit-to-row conversion authority (row 24),
the B3a/B5 destination ruling (35), the never-meter-buy substrate rule (31). **The selection is
inverted relative to the register's own scope**: expired batch rulings are documented at length in
packets, and open-ended doctrine sits in a closed batch's manifest.

**(5) The mechanical cause is measurable, and the architect has already named it as unruled.**
The register is inside the silent-rule ratchet corpus. Measured live this session:

```
python3 scripts/silent_rule_detector.py  ->  files: 59   count: 441
ecosystem/silent-rule-baseline.yaml      ->  baseline: 441
```

Headroom **zero**. `scripts/audit.py::check_silent_rule_ratchet` is **FAIL-class** and gates every
commit through the `audit-health` pre-commit hook, and the baseline *"may be LOWERED or held. It
may NOT be raised"* without an operator ruling. The register documents its own constraint:

> `protocols/STANDING_RULINGS.md:1972-1979` — *"Adding a normative keyword to this file therefore
> raises the count and FAILs the `silent_rule_ratchet` check, which blocks the commit through the
> `audit-health` hook. Entries here are phrased declaratively for that reason."*

And the question of whether the file may grow at all is itself open, in this window, blocking two
rows:

> `docs/handoffs/2026-08-23-dev-knowledge-architect/SUPPLEMENT.md:77-78` — *"**post-ratchet
> STANDING_RULINGS section-writing policy (blocks #491 + #344)**"*

> `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §5.3 — *"the 2026-08-22
> architect DEFERRAL — held on **the unmade policy of whether new `protocols/STANDING_RULINGS.md`
> sections may be written post-ratchet**"*

**So the register stopped absorbing rulings on 2026-08-15, and since at least 2026-08-22 there has
been a known, recorded, unresolved policy question about whether it may absorb any more.** The
2026-08-22 rulings ledger is the surface that grew in its place — an unratified successor with no
schema and no gate either.

**(6) A compounding factor the corpus already documented.** Four ruling namespaces ran concurrently
in one window with a fifth colliding (`D1.x`/`D5.x`, `R1–R7`, `§A1–§A10`, night-3 `D1–D14`, and
ADR-85's own `§A1–§A9`). A register keyed on ids cannot index rulings that have no stable id
namespace, and this audit hit that directly: distinguishing phase-2 `§A7` from ADR-85 amendment
`§A7` required reading context, not matching a string.

**Per the contract, the mechanism is not proposed here.** The shape is: *rulings land when a
close-arc seat with transcription as its job runs; they do not land when they are issued mid-arc
into an off-repo pack; the register that would hold them is at a hard gate ceiling with an
unresolved policy on whether it may grow; and the one durable class — standing doctrine with no
expiry — is the class most often left in a closed batch's immutable manifest.*

---

## 5. Coverage statement

### 5.1 What was searched

| Surface | Extent |
|---|---|
| `protocols/STANDING_RULINGS.md` | full read, 2,001 lines; entries parsed programmatically for expiry / `landed:` / mechanism keywords |
| `docs/audits/` | **all 693 files**, 8-pattern ruling-marker regex → 156 files / 321 lines; the 2026-08-05→23 subset (≈75 lines) read in context |
| `docs/decisions/` | ADR-53 in full (49 lines); ADR-101 §1 + all 7 in-file amendments; ADR-52 confirmed archived |
| `tasks/` · `BACKLOG.md` | `[#577]`, `[#171]`, `[#169]`, `[#322]` rows read in full |
| `JOURNAL.md` | 2026-08-23 entries (e)–(h) read in full; targeted grep for `#171`, `§A`, ruling markers |
| `docs/handoffs/2026-08-23-dev-knowledge-architect/` | `HANDOFF_BOOT.md`, `PASTE_THIS.md`, `RESIDUAL.md`, `SUPPLEMENT.md` — targeted reads |
| `scripts/` | `validate_hermetization.py` + `canonical_docs.py` **executed**; `silent_rule_detector.py` **executed**; `audit.py` grepped for register-touching checks; `ecosystem/silent-rule-baseline.yaml` read |
| repo-wide | `grep -rn` over `*.md` / `*.yaml` for `#577`, `#171`, `§A1–§A10`, `rustworkx`, `B3a`, `ADMISSION VERDICT`, `STANDING_RULINGS` |
| git | `log -S` on the register; `merge-base --is-ancestor 2af03f3 origin/main` |

### 5.2 What could not be reached — the honest limits

1. **The off-repo ruling packs.** Every window whose rulings went missing issued them into files in
   the operator's Downloads / prompts directories, outside the repo and outside this container:
   `PHASE2-MAX-PACK.md`, `MORNING-ADJUDICATION-2026-08-15.md`, `PHASE1-REVIEW-PACKET.md`,
   `CLEANUP-AND-NIGHT-BATCH-3.md`, `SESSION-CLOSE-BATCH-7A.md`,
   `SESSION-PLAN-2026-08-05-dev-knowledge-architect.md`, `PICKER-2026-08-12-annotated.md`,
   `RULING-CHECKLIST-2026-08-10.md`, `W4-WAVE2-INPUT.md`, `PHASE1-TERRA-RAW-2026-08-15.md`.
   **I can prove a ruling is absent from the repo. I cannot read what those packs actually said,**
   so "7 of 10 unlanded" means seven have no in-repo carrier — not that their texts are lost.
2. **The chat windows themselves.** A ruling issued in chat that reached *no* artifact is
   undetectable by construction. This audit measures rulings that left a trace; the true
   denominator is unknowable from inside the repo, and every count here is therefore a **floor**.
3. **Regex recall.** A ruling recorded in prose using none of the eight markers is invisible to the
   sweep. The calibration case proved this concretely — it carries no marker line anywhere in
   `docs/audits/` and was found only by widening to the handoff bundle (§2.1 step 5).
4. **Pre-2026-08-05 rulings are out of scope by construction** — the register did not exist, so
   their absence from it is not a landing failure. 165 of the 321 marker lines fall in that range
   and were not adjudicated.
5. **No gate, test suite or `audit.py` check was run** — the `uv` mesh refuses in this container
   (§0). Every mechanical claim here rests on direct function calls under an unpinned interpreter,
   which is weaker evidence than a gate run and is labelled as such at each use.
6. **L0 surfaces** (`~/.claude/`, `~/.codex/`) are outside this repository by ruling R-2 and were
   not read.
7. **Deleted history not walked.** A ruling that landed and was later removed would read as never
   landed. `git log -S` was run only on the register, not on the corpus.

### 5.3 Compliance with the closure contract

- **Did not** write to `protocols/STANDING_RULINGS.md`.
- **Did not** create root `AGENTS.md` (and §3.4 records that the gate would have refused it).
- **Did not** judge whether any ruling was correct — §3.1 assesses whether ADR-53's *text* bears a
  stated reading, which the brief set as the load-bearing question, and stops there.
- **Did not** report any ruling as landed without quoting its carrier.
- **Did not** report NOT FOUND without stating the searches (§2.3, §5.1, §5.2).
- **Did not** propose a mechanism (§4 closing paragraph).
- **Did not** touch `tasks/`, `BACKLOG.md`, or `docs/adr/`.
- **Did not** self-merge.

---

## 6. AMENDMENT 2026-08-23 — the mesh was armed after all, and every claim above was re-run under it

**This section is APPENDED, not edited in** (`CLAUDE.md` §5 rule 3 admits an in-file amendment
marker as the alternative to a superseding file; the 2026-08-22 rulings ledger §5 and the
2026-08-23 window seal §5 are the precedents). Everything in §0–§5 stands exactly as written. What
changes is the **strength of the evidence**, and one stated limitation is now discharged.

### 6.1 What §0 got wrong, and it was mine

§0 recorded that the `uv` mesh *"refuses in this container"* and routed every measurement to a
hand-run `python3` 3.11.15. The refusal was real. **The inference that the pin was unreachable was
not tested, and it was wrong.** `uv self update 0.11.19` fails here — but with
*"version 0.11.19 was not found for the app uv in workspace uv"*, which is a fact about how this
container manages `uv`, **not** about whether the version exists. It does:

```
python3 -m pip download "uv==0.11.19"   -> uv-0.11.19-py3-none-manylinux_2_17_x86_64.whl (24.9 MB), OK
python3 -m pip install --target ./uvpin "uv==0.11.19"   -> ./uvpin/bin/uv
PATH=./uvpin/bin:$PATH ; uv --version   -> uv 0.11.19 (x86_64-unknown-linux-gnu)
uv run --locked python --version        -> Python 3.12.10      (27 packages installed in 16ms)
```

**The mesh runs at exactly the declared pins** — `required-version = "==0.11.19"`, `.python-version`
3.12.10. The install is **container-local**: a wheel unpacked into the session scratchpad and
prepended to `PATH`. No repo file was touched by it, no `pyproject.toml`/`uv.lock` edit, nothing
committed from it. D1's *"the exact `uv` pin is load-bearing"* is upheld rather than routed around.

**The lesson is the one this audit is about.** A tool refusing is evidence about the invocation, not
about the world. §0 turned one failed command into a declared environmental limit and then built six
sections on the weaker footing — the same shape as §2.3's finding that a claimed ruling is not a
ruling. Recorded because an audit that would not apply its own standard to itself is worth less.

### 6.2 Every load-bearing measurement, re-run under the pinned mesh

| Claim | §-ref | Hand-run (3.11.15) | Pinned mesh (0.11.19 / 3.12.10) |
|---|---|---|---|
| Silent-rule ratchet at zero headroom | §4(5) | `count: 441` vs `baseline: 441` | **identical** — and `audit.py health` renders it `[OK] silent_rule_ratchet: live 441 <= baseline 441 under detector silent-rule-v4 (59 file(s) in scope)` |
| Rule A blocks root `AGENTS.md` | §3.4 | BLOCK message | **identical**, verbatim |
| `codex/AGENTS.md` classifies clean | §3.4 | `None` | **identical** |
| `AGENTS.md` not in the sanctioned set | §3.4 | `False` | **identical** |
| Session-end backpressure | §5.2(5) | exit 0 | **exit 0** under `uv run --locked`, the configured invocation |

**Zero divergence.** No conclusion in §1–§5 moves.

### 6.3 What the gate adds that the hand-run could not

`uv run --locked python scripts/audit.py health` → **`health: DEGRADED`**. Three results bear
directly on this artifact:

1. **§1.3's "5 of 83 entries carry the one machine-checked field" is confirmed by the checker
   itself.** `check_landing_predicate` emits exactly five findings — `F2`, `N-1`, `N-2`, `N-3`,
   `R-2` — all `[OK]`. The count was derived by grep in §1.3; the gate independently returns the
   same five ids.
2. **The unarmed hook stack is confirmed by the mesh, not just by me.**
   `[~~] fleet_parity: .dev-knowledge hooks-armed WARN-undeclared: pre-commit config present but
   stage(s) NOT armed: commit-msg, pre-commit, pre-push` — *"a carried config with dead hooks is the
   relic-hooksPath silence class."* The two commits carrying §1–§5 genuinely passed no gate;
   **nothing was bypassed, because there was nothing armed to bypass** (no `--no-verify`, no `SKIP=`).
3. **One `[!!]`, and it is this container's stale clone rather than this lane's content.**
   `journal_spine_anchor: backstop could not complete (AnchorError('disposition floor 24882f8cc is
   not an ancestor of main: … Not a valid object name'))`. Local `refs/heads/main` in this container
   is stale at `4541155b`, far behind `origin/main` at `aeec0fd1` — HEAD was detached from
   `refs/heads/main` at boot and this lane never touched either ref. Measured against the **real**
   base, the range is anchored:

```
git log --oneline origin/main..HEAD        -> acad6de, 3894da5   (2 commits, no others)
journal_anchor.spine_entries               -> ['acad6de8…', '3894da55…']
journal_anchor.unanchored_in_range         -> ['acad6de8…']      (the JOURNAL commit itself)
journal_anchor.range_is_anchored           -> True
```

`True` is the correct result: discharge is **range-level**, and JOURNAL 2026-08-23 (k) names
`3894da55`, a commit the range introduces. A JOURNAL commit cannot name its own hash — the exact
case register B6 and the ADR-85 §A5 predicate are built around. `block-unanchored-push` would have
passed had it been armed.

### 6.4 The limitation this amendment discharges, and the ones it does not

**Discharged:** §5.2 item 5 (*"No gate, test suite or `audit.py` check was run"*) — for the claims
in §6.2 and §6.3. Those now rest on the pinned mesh and, for three of them, on the gate's own output.

**Not discharged, unchanged:** §5.2 items 1, 2, 3, 4, 6 and 7. Arming the toolchain does not make
the ten off-repo ruling packs readable, does not make a chat-only ruling detectable, does not widen
the regex's recall, and does not walk deleted history. **The census counts in §2 are still floors**,
for exactly the reasons given there. `pytest` was not run — the audit changes no code, and the
suite's verdict bears on nothing claimed here.
