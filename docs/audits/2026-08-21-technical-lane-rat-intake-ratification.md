# ARTIFACT — LANE-RAT (batch 1, lane D) — DRAFT-intake ratification

**Lane:** `worktree-lane-rat-intakes` · **Repo:** `.dev-knowledge` · **Date:** 2026-08-21
**Contract:** `LANE-RAT-intakes.md` (frozen, ruled split R5 per outgoing-architect Q4)
**Owned files:** `docs/intake/**` (sole owner this batch) + this artifact. `tasks/` and
`BACKLOG.md` untouched.

> **PATH DEVIATION — the contract's artifact path was REFUSED by a live gate.** The contract
> specifies `ARTIFACT-lane-rat.md` at the worktree root. Committing it there is impossible:
> the `validate-hermetization` pre-commit hook (ADR-101 §1 Rule A) refuses it verbatim —
> *"unsanctioned new top-level file 'ARTIFACT-lane-rat.md' — Tier-1 files are a closed class
> (ADR-101 §1); a genuinely new class is an ADR-101 amendment, not a drive-by add"* — and a
> lane has no authority to amend ADR-101, nor to reach for `--no-verify`. The alternative,
> leaving it uncommitted, loses the artifact at worktree teardown. It therefore lands here,
> at `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md`, on the sibling-lane
> precedent of 2026-08-20 (`2026-08-20-technical-grok-ab-results-2.md` and its peers) and
> conforming to the ADR-101 R3/R4 filename grammar `<date>-<class>[-<slug>]` with the
> `technical` class. **Every in-repo reference written by this lane points here, not at the
> root path.** Seat and integrator: this file is the deliverable the contract calls
> `ARTIFACT-lane-rat.md`.

**Governing protocol, quoted as the contract requires.** Intakes are governed by
**`docs/intake/README.md`** — the ADR-98 requirements spine. §2 fixes the eight-section doc
format, §3 the frontmatter schema, §4 the naming convention, §5 the lifecycle enum
(`SEED → DRAFT → READY → ACCEPTED (decided-by + disposition) | CONSUMED | SUPERSEDED |
REJECTED`), §5a the partial-ratification convention, §6 the confirm-gate. The fill-in skeleton
it points at is `templates/intake-template.md`. Both were read end-to-end before any edit. The
anti-orphan rule applied at every ratification is `protocols/STANDING_RULINGS.md` **P-2**.

---

## 1. Enumeration and classification (live, not assumed)

Enumerated live from frontmatter `status:` across `docs/intake/*.md` — **exactly 7 DRAFT**,
matching the generated index's `### DRAFT (7)` group at the time of boot.

**Classification — the three touching the server-side-enforcement ADR fork:** #35, #36, #37.
Verified by reading each doc's `Section C — what this supersedes or contradicts in current
doctrine`, not taken from the contract. The three share one axis — *does an enforcement rule
move out of advisory prose into a mechanism the agent cannot get past* — but each states its
own fork:

- **#36 carries the fork proper.** Its Section C heading is literally *"GENUINE FORK — R9 vs
  standing doctrine"*: the memo wants a `PreToolUse` hook rejecting `--no-verify` / `SKIP=`
  outright; ADR-85 amendment 2026-08-03 §A2 deliberately keeps that escape and makes it
  non-silent instead. Section C also records the repo-level fact under all of this — *"this
  repo has **no CI backstop**; every gate named in `CLAUDE.md` §9 is client-side and
  bypassable."*
- **#35's fork is the same question one layer up:** AGENTS.md against `CLAUDE.md` §10's named
  anti-pattern and ADR-53's single-instruction-file ruling — *which* instructions are allowed
  to leave prose at all, and into what file.
- **#37's fork is the same question one layer down:** R12 stores a `done_when.verify`
  predicate inside `tasks/`, against `CLAUDE.md` §5 rule 7 (*"No executable rules in this
  repo"*). Section C says outright: *"These cannot both stand as written."*

**The 4 non-fork:** #24, #27, #33, #34.

---

## 2. Seven-row status table

```
id   file                                                    before  after      leg
#24  2026-08-05-tech-currency-wave-1.md                       DRAFT   ACCEPTED   prep + transition (deferred, dated)
#27  2026-08-06-tech-adoption-consolidation-intake.md         DRAFT   ACCEPTED   prep + transition (active)
#33  2026-08-12-func-repo-self-description-consolidation.md   DRAFT   ACCEPTED   prep + transition (active)
#34  2026-08-16-code-architecture-enforcement.md              DRAFT   DRAFT      prep only - BLOCKED, see 4b
#35  2026-08-17-tech-agent-instruction-layers-...md           DRAFT   DRAFT      prep only - held for R7
#36  2026-08-17-tech-repository-autonomy-...md                DRAFT   DRAFT      prep only - held for R7
#37  2026-08-17-tech-machine-verifiable-done-when.md          DRAFT   DRAFT      prep only - held for R7

prep commits:        #24 0a445396 · #27 de418e44 · #33 61e0a0fb · #34 d5cee408
                     #35 c75b72fa · #36 ef956cb5 · #37 9be8c4d8
transition commits:  #27 5c29a3cb · #33 226d8c66 · #24 513a190a
```

**3 of 4 non-fork transitioned, not 4.** #34 is the one deviation from the contract's item 3,
taken under the contract's own decision budget (*"ambiguity → prep-only + report"*) rather than
by preference — see §4b. Every other contract item is discharged in full.

**Per-intake prep result** (completeness pass against README §2–§5 + the template):

- **#24** — 8 of 8 template sections missing as sections. Body landed **verbatim** (operator
  ruling 2026-08-05), so it was **not** restructured: the eight sections are *mapped* to where
  the verbatim body already carries them (`WHY` → Problem/motivation; `WHAT — candidates` →
  Functional requirements; `Do-not-relitigate` → Non-goals) and the four genuine absences
  (Scenarios, Acceptance criteria, Impact sketch, Open questions) are **recorded, not
  back-filled**. `## Status` added. Frontmatter: empty `consumed-by:` removed (off-schema at
  DRAFT per §3).
- **#27** — same shape, same treatment (`WHY` → Problem/motivation; `§A` + `§C` → Functional
  requirements; `§B` → Non-goals). Zero §A rows, statuses, priority classes or item text
  touched. `## Status` added. Frontmatter already on-schema.
- **#33** — 2 of 8 missing. **Functional requirements** added, *derived* from Sections A/B/C
  and the existing A1–A4 acceptance criteria (no new ask anywhere in it), plus **Status**. The
  other six were already conformant.
- **#34** — 8 of 8 missing; mapped and recorded as for #24. Empty `consumed-by:` removed.
  Two findings recorded in-file (§4b, §6).
- **#35 / #36 / #37** — **conformant, no fixes required.** All eight sections present
  (Section C is the one extra top-level section, per the lane-R contract of record);
  frontmatter on-schema (`note:` and `consumers:` are the optional descriptive keys ratified
  at the [#398] deploy); naming conformant. A dated prep-pass record was appended to each
  doc's existing `## Status` section; **frontmatter `status:` untouched.**

**Why absences were recorded rather than filled.** README §2 calls Scenarios *"the load-bearing
section — a requirement with no scenario behind it is suspect"*. Writing scenarios into a
verbatim-landed doc after the fact would manufacture exactly the authority the doc's own
library-first bar refuses, and would make a fabrication look like conformance. Recording the
absence keeps the gap visible and checkable.

---

## 3. Both-generators evidence

Two generators serve `docs/intake/`, and **only one is hook-gated** — `intake-index-freshness`
(`CLAUDE.md` §9) gates `gen_intake_index.py`; `gen_intake_tree.py` is armed only via
`audit.py`'s `intake_tree_coherence` check, so running one and not the other is the known
trap. **Both were run on every transition, and on the two prep commits that changed
frontmatter keys** (the residue carrier records per-doc frontmatter key names, so a
frontmatter edit alone makes the manifest stale — witnessed live below).

```
prep #24 (frontmatter key removed)
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 1   (FAIL: manifest stale vs README)
  python scripts/gen_intake_tree.py  --write   -> exit 0   (wrote manifest.json)
  python scripts/gen_intake_tree.py  --check   -> exit 0

prep #27 (body only)
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0

prep #33 (body only)
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0

prep #34 (frontmatter key removed)
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --write   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0

transition #27  (DRAFT -> ACCEPTED)
  python scripts/gen_intake_index.py --write   -> exit 0   (wrote docs/intake/README.md)
  python scripts/gen_intake_tree.py  --write   -> exit 0   (34 item nodes, 281 residue lines)
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0   (315 nodes, 19825 README bytes)

transition #33  (DRAFT -> ACCEPTED)
  python scripts/gen_intake_index.py --write   -> exit 0
  python scripts/gen_intake_tree.py  --write   -> exit 0
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0

transition #24  (DRAFT -> ACCEPTED)
  python scripts/gen_intake_index.py --write   -> exit 0
  python scripts/gen_intake_tree.py  --write   -> exit 0
  python scripts/gen_intake_index.py --check   -> exit 0
  python scripts/gen_intake_tree.py  --check   -> exit 0
```

**The trap fired once, in this lane, and is worth recording.** At the prep-#24 commit the
pre-commit `audit-health` gate returned `health: DEGRADED` on
`[!!] intake_tree_coherence: manifest is stale versus README.md` and **blocked the commit** —
caused by removing one frontmatter key, with no README edit at all. The index generator was
clean throughout (exit 0), so an index-only workflow would have shipped the staleness. This is
the concrete case for the contract's "run BOTH" instruction: the hook-gated generator is not
the one that noticed.

Index movement, as generated: `DRAFT (7) → DRAFT (4)`, `ACCEPTED (16) → ACCEPTED (19)`.

---

## 4. What was held, and why

### 4a. #35–#37 — held on the architect's R7 ADR-fork ruling

Prep only; `status:` untouched, per the contract. Never this lane's call. Evidence block for
the ruling in §5.

### 4b. #34 — held under the contract's ambiguity budget (the one deviation)

#34's own `## What ratification would have to settle` opens with: *"Land the source artifact
in-repo (it is the evidence base and is currently operator-held)"*, and its frontmatter
`origin:` says the artifact *"lands with the ratification"*. **A lane cannot satisfy that
precondition** — the artifact is operator-held and not in this repo, and item 5 (price the
adoption per ADR-112's two-tier bar) is likewise unpriced. Flipping it to ACCEPTED would
create a standing authority whose own stated evidence base is absent, and would silently
discharge a precondition the document itself wrote down.

The contract's decision budget prescribes exactly this handling — *"zero questions; ambiguity →
prep-only + report"* — so #34 was prepped in full and left at DRAFT, with the blocker recorded
in the file as well as here. **What the operator/architect owes to unblock it:** land the
source artifact in-repo, then #34 transitions on a later lane with no other work needed.

---

## 5. R7 evidence block — the ADR fork, for the architect's ruling

Each option ≤3 lines with its consequence. Nothing here is a recommendation; the lane has no
authority over this fork and takes none. **Read the three sub-forks first, then the packaging
question — they are separable, and packaging is the cheaper decision to get wrong.**

### 5.1 The three sub-forks, as the docs state them

```
FORK A (#36 R9) — the bypass valve.  "Block --no-verify/SKIP=" vs "make bypass non-silent".
  A1  Build R9: a PreToolUse hook refuses --no-verify / SKIP= outright.
      Consequence: removes the pressure-release valve ADR-85 amendment 2026-08-03 SSA2
      deliberately kept; every legitimate declared bypass (Q1's sanctioned lane-branch skip)
      needs a new escape, or the merge queue wedges.
  A2  Record a REFUSAL of R9 and keep the ADR-85 answer.
      Consequence: the client-side stack stays bypassable by design; the honest claim becomes
      "we detect bypass", never "we prevent it" -- and #36's own finding stands that
      block-ff-push is "the real teeth" only relative to the other client-side hooks.
  A3  Move the teeth server-side instead (intake #24 P1's CI second wall).
      Consequence: answers the fork by relocating it -- a server-side record is out of the
      agent's reach, so the valve can stay open locally without being the last line. Costs
      the CI build #24 P1 prices, and its "Open verification item" (private-repo
      required-checks may need a paid plan) is unresolved.

FORK B (#35 R1) — the instruction file.  AGENTS.md vs ADR-53's single instruction file.
  B1  Adopt AGENTS.md.
      Consequence: overturns a named CLAUDE.md SS10 anti-pattern and ADR-53; two independent
      commissions now recommend it, so declining silently is no longer available.
  B2  Refuse, on ADR-53 as written.
      Consequence: the 200-line budget stays the pressure valve and keeps being relieved by
      condensing history into git -- the mechanism CLAUDE.md SS12 shows firing repeatedly.
  B3  Rule the narrow question #35 Q1 actually asks: does ADR-53 forbid AGENTS.md, or forbid
      two files that both carry content?
      Consequence: a one-line CLAUDE.md = @AGENTS.md pointer satisfies the second reading and
      violates the first; ruling the reading disposes of B1/B2 without re-opening ADR-53.

FORK C (#37 R12) — the executable predicate.  done_when.verify in tasks/ vs CLAUDE.md SS5 rule 7.
  C1  Rule the genres distinct (behavioural rules vs acceptance evidence) and rename one use
      of "verify:" so the two stop colliding.
      Consequence: R12 becomes buildable; rule 7 keeps its meaning; one keyword rename lands
      across ~.claude/ rules and the task schema.
  C2  Refuse R12 on rule 7 as written.
      Consequence: Done-when stays prose; #37's whole build (R12-R17) falls, and the intake
      spine's "acceptance criteria copy VERBATIM into the epic's UAT" seam stays clerical.
  C3  Relocate the predicate outside this repo to satisfy rule 7 literally.
      Consequence: satisfies the letter and breaks the join -- the predicate leaves the file
      the generator reads, which is the whole point of #37 Q3.
```

### 5.2 The packaging question — how many ADRs

```
P1  ONE ADR: "where enforcement lives", ruling A/B/C together.
    Consequence: the shared axis is ruled once and the three docs cite one id; the cost is a
    single fork that fails to rule cleanly blocking all three intakes.
P2  THREE ADRs, one per fork, one per intake.
    Consequence: each intake transitions the moment its own fork is ruled; the cost is three
    ADRs that must not contradict each other on the shared axis.
P3  ONE ADR now for Fork A only (the server-side fork proper); B and C wait.
    Consequence: #36 transitions and #35/#37 stay DRAFT; matches the docs' own weighting --
    #36 is the only one whose Section C says "GENUINE FORK".
P4  Zero ADRs -- record refusals in the intakes and leave all three DRAFT.
    Consequence: cheapest today; ADR-98 SS3 says an ADR is owed where "a reasonable person
    could choose otherwise and reversal is costly", which all three forks satisfy, so this
    defers rather than decides.
```

**One evidence-driven constraint on any packaging choice, from the docs themselves:** #36's R7
(mutation testing) and #37's R17 are *the same build*, and #37's own Status section says it
"must not be born twice". Whatever packaging is chosen, that build is filed once. Likewise
#36's Section C says nothing about #35's or #37's forks, and neither of theirs mentions R9 —
the *docs* treat the three as separable even though the axis is shared.

**Partial-ratification option, available under README §5a and not counted above.** If only part
of a doc is ruled, the ADR-108 pattern applies: transcribe the ruled sections into an ADR whose
title names them, carry a scope boundary listing what it does **not** ratify, and leave the
intake at DRAFT with a pointer. §5a is explicit that promotion is **not** an ACCEPTED flip, so
it triggers no carrier requirement — which makes it the cheapest way to rule Fork A's R9 alone
without moving #36's status.

---

## 6. Carrier-row specs (for the SEAT — `tasks/` is not this lane's to touch)

`protocols/STANDING_RULINGS.md` **P-2**: *"An intake flipped to `ACCEPTED` carries at least one
live carrier row, or a `disposition: deferred` naming a live, DATED trigger. `ACCEPTED` with
zero carriers and no dated deferral is not a lawful terminal state."*

**Measured before ratifying, not assumed:** a sweep of `tasks/*.md` for `intake #24`,
`intake #27`, `intake #33`, `intake #34` returned **zero** rows. None of the four had a
pre-existing carrier.

**Discharge chosen per intake:**

| intake | branch taken | needs a row from the seat |
|---|---|---|
| #27 | carrier row | **yes — spec 1 below** |
| #33 | carrier row | **yes — spec 2 below** |
| #24 | dated deferral (`trigger:` + `review-date: 2026-09-20`) | no |
| #34 | not ratified | no |

**#24 takes the deferral branch deliberately.** #27 is #24's successor ledger for the
adoption-status view and already carries the same candidates as §A rows; a second carrier
against #24 would duplicate #27's. `trigger:` names #27's W-wave batch and `review-date:`
dates the un-park, which is what P-2 asks of a zero-carrier ACCEPTED doc. Both keys are used
together on purpose: README §3 offers `review-date:` as an alternative to `trigger:`, but P-2
wants a trigger that is *dated*, and only the pair says both what un-parks it and when it
expires.

### Spec 1 — carrier for intake #27

```
FILE: tasks/<next-free-id>-consume-the-tech-adoption-ledger-w-wave.md
---
id: "[#NNN]"
title: "Consume intake #27's W-wave rows — the deferred half of the tech-adoption ledger"
status: open
priority: P2
size: L
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: environment
generates: BACKLOG.md
---

- [#NNN] [P2][L] **Consume intake #27's W-wave rows — the deferred half of the tech-adoption
  ledger** — Intake #27 was ratified ACCEPTED (`disposition: active`) on 2026-08-21 and is the
  fleet's standing adoption ledger; this row is its carrier. Six §A rows carry
  `DEFERRED(W-wave batch — after intake #25 acceptance + births)` and #25 is already ACCEPTED,
  so the peg is live rather than pointing at a finished event. Scope is **the deferred rows
  only** — every ADOPTED-live / REFUTED / EVAL-RUN row is settled and is not re-litigated, and
  §B's do-not-relitigate list binds. Adoption of any item still owes its MEASURED divergence
  run on this repo plus ADR-112 two-tier pricing; ratification of the ledger is not
  authorisation to adopt. **Ledger edits are now appended amendments, not in-place edits** —
  the `status: DRAFT` editability the three 2026-08-06/08/09 errata relied on ended at
  ratification. · Done when: every §A row still reading `DEFERRED(W-wave batch …)` has been
  either run (result recorded as an appended amendment), re-pegged to a live dated trigger, or
  refused with a reason — and no row is left pointing at a spent peg · refs intake #27,
  intake #24, intake #25, ADR-112, `protocols/STANDING_RULINGS.md` E1, G1 ·
  kill-candidates: none — the ledger has no other carrier (measured 2026-08-21: zero `tasks/`
  rows cite intake #27) and this row is what makes its ACCEPTED status lawful under P-2 ·
  serialize-group: environment
```

### Spec 2 — carrier for intake #33

```
FILE: tasks/<next-free-id>-define-architecture-described-surface.md
---
id: "[#NNN]"
title: "Define \"architecture-described surface\" + the architecture-freshness check (intake #33 A1)"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: docs-gate
generates: BACKLOG.md
---

- [#NNN] [P2][M] **Define "architecture-described surface" + the architecture-freshness check
  (intake #33 A1)** — Intake #33 was ratified ACCEPTED (`disposition: active`) on 2026-08-21;
  this is the **single** row its A1 criterion calls for, and #33's Births section is explicit
  that Section A's row is born from the definition, not from the filing. Produce a written
  definition a grep can evaluate, then the check that flags a commit touching such a surface
  when `ARCHITECTURE.md` carries no matching delta and no explicit no-impact note. **Zero new
  organ families** (A1) and **zero new top-level directories** (A4) — both bind. The definition
  also discharges the three routed obligations A1 names: the `N1-D11`/G-7 consumer, the
  `N2-E1-1` W-wave referent, and the `N2-R2-07` re-peg decision. Q3 (advisory-only in v1?) is
  open and is answered by this row, not assumed. Sections B and C of #33 are **out of scope**:
  B is a belief repair owned alongside `[#420]`, C is a carrier-or-ADR decision that must
  declare which it is before any file is authored (A3). · Done when: the definition is written
  and grep-evaluable, the check exists and fires on a fixture where an architecture-described
  surface changed with no `ARCHITECTURE.md` delta, Q3's advisory-vs-blocking posture is
  recorded as a decision rather than a default, and the three routed obligations are each named
  as discharged · refs intake #33, `[#420]`, ADR-51, ADR-101 · kill-candidates: none —
  measured 2026-08-21: zero `tasks/` rows cite intake #33, and this row is what makes its
  ACCEPTED status lawful under P-2 · serialize-group: docs-gate
```

**Seat notes — three things that will bite if skipped.**

1. **Derive the ids at landing time**, from the max bracketed id across all history +1 — never
   from this artifact. Two specs, so two consecutive ids.
2. **Run both `tasks/` generators** as that surface requires, and write the task files with
   **LF** endings — a CRLF task file reads as foreign to the task tree and the error does not
   say so.
3. The `kill-candidates:` line is **required by the `backlog-filing-backpressure` commit-msg
   hook** on any commit adding a new task id, and the hook's regex is **line-anchored** — it
   must be flush-left in the commit message body, not indented.

---

## 7. PENDING-CARRIER — the merge-ordering dependency

**#27 and #33 are ACCEPTED with no carrier row on disk.** Inside this lane that is unavoidable:
P-2 wants the row in the same commit as the flip, and `tasks/` is SEAT-owned this batch. The
contract's answer is sequencing, and it is a hard dependency, not a preference:

> **The integrator merges the SEAT's carrier rows BEFORE this lane's branch.** In that order no
> commit on `main` ever shows an ACCEPTED intake without its carrier, and no orphan window
> exists. Merged in the other order, `main` carries two P-2 violations for the length of the
> gap.

#24 (dated deferral) and #34 (not ratified) carry no such dependency.

---

## 8. Audit evidence

```
python scripts/audit.py health   ->  health: OK      (44 [OK], 46 [~~] WARN, 0 [!!] FAIL)
  [OK] intake_tree_coherence: intake residue carrier coherent (315 node(s), 19825 README bytes)
python scripts/gen_intake_index.py --check  -> exit 0
python scripts/gen_intake_tree.py  --check  -> exit 0
```

`python scripts/audit.py` with no subcommand prints usage and runs nothing (the
"validators with no args = vacuous pass" anti-pattern); `health` is the subcommand the
pre-commit gate itself runs, so that is what was run.

**Green of this lane's making, stated honestly.** Zero FAILs. The 46 WARNs are **inherited, not
produced here** — the intake-touching ones are `undeclared_edges` (ADR-88 FC2) prose edges, and
each traces to text that predates this lane: #27's is line 47 of the §A ledger, an original row
citing `templates/prompt-template.md`. No WARN names a line this lane wrote. Every one of the
ten commits passed the full pre-commit stack with no `--no-verify` and no `SKIP=`; the one
`audit-health` block (prep #24, §3) was fixed by regenerating, not bypassed.

---

## 9. Findings for the architect (recorded, not acted on)

1. **`templates/intake-template.md` contradicts `docs/intake/README.md` §3 on `consumed-by:`.**
   The template seeds the key with *"leave blank until status: CONSUMED"*; §3 says companion
   fields are *"REQUIRED at their status … leave absent at any other status"*. The template is
   where the two off-schema empty keys found in #24 and #34 came from. Fixed at the two docs
   this lane owns; **the template itself is not this lane's file** and still seeds the defect.
2. **#34's filename carries no `{func|tech}` genre infix** —
   `2026-08-16-code-architecture-enforcement.md`, created well after §4's 2026-07-08
   ratification, and its own HTML comment declares `class: tech`. **Deliberately not renamed:**
   `gen_intake_tree.py` is contracted never to move or restyle an intake doc, a rename
   invalidates the path every other artifact cites, and it is a structural act outside a prep
   pass.
3. **#24's and #27's `# titles` still read "INTAKE DRAFT — …"** while both now render under
   `### ACCEPTED` in the generated index. The titles are part of the verbatim-landed bodies, so
   editing them is a bigger breach than the stale label; the index shows the mismatch plainly.
   Flagged for an operator ruling rather than repaired.
4. **This lane's frozen contract is not a committed repo artifact.** It was read from
   `~/Downloads/LANE-RAT-intakes.md`, and grep finds no `LANE-RAT` anywhere in the repo, while
   sibling lanes of 2026-08-20 all carry theirs at
   `docs/audits/<date>-technical-<slug>-lane-contract.md`. `protocols/STANDING_RULINGS.md`
   **Q6** rules *"contract-as-file without exception — the frozen contract is a committed repo
   artifact at dispatch time"*. Reported, not repaired: `docs/audits/` is outside this lane's
   owned files. The `decided-by:` fields therefore cite the contract as an **off-repo** ruling,
   per the section-I off-repo-ratifying-act precedent, rather than claiming an in-repo locator
   that does not exist.
5. **#35–#37 record that they never cleared the §6 confirm-gate** (*"Not operator-approved; the
   `docs/intake/README.md` §6 confirm-gate has not been cleared"*), while §6 says a doc that
   has not cleared approval *"does not belong in this folder yet"*. Pre-existing, self-declared
   by lane R, and untouched here — but it is a live inconsistency between three filed docs and
   the protocol that governs the folder.

---

**Lane status: COMPLETE.** 7 prepped · 3 transitioned · 1 held on evidence (#34) · 3 held on
the R7 ruling (#35–#37) · 2 carrier-row specs emitted · both generators evidenced on every
transition · `audit.py health: OK`, zero FAILs.
