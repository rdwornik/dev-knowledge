<!-- scope: meta -->
# Orphan census — every decision-bearing surface, tested for a carrier · 2026-08-17

**Produced by:** CC (`claude-opus-5`), lane `nb7-A`, branch `claude/nb7-orphan-census-mhgcx3`.
**Posture:** READ-ONLY. This report is the lane's entire write footprint (plus the
`audit-index-freshness`-mandated regeneration of `docs/audits/README.md`). **Zero rows born, zero
rows edited, zero registers touched, nothing merged.** Every row below is a *draft*; birthing it is
an architect act.

> **The standing complaint, verbatim from the brief:** *"decisions get made and never get owners."*
> Thrice repeated, thrice under-answered. This sweep tests the complaint mechanically rather than
> agreeing with it.

---

## §0 · The answer first

```
surfaces swept 10 · decisions tested 598 · orphans 54 · oldest age 41 days
row drafts 16 · reject/supersede 3 · escalate-to-operator 1
```

**Three things this pass establishes that were not established before it:**

1. **The complaint is correct, and the largest single block is not new work — it is 15 rulings
   that already name their own durable home and were never moved into it.** `STANDING_RULINGS`
   carries ten entries whose own text reads *"Declared durable home: … — **not landed yet**"*, and
   the 2026-08-17 handoff supplement adds five more terms with named PLAYBOOK homes. All 15 were
   tested by grep against every declared home: **0 hits, every one.** One of them is worse than
   unlanded — the register asserts *"candidate landed in LESSONS at batch-6 wrap"* for **admission
   control**, and `LESSONS.md` returns **0 occurrences of the string `admission`**. The record of
   where a ruling went is itself wrong.

2. **One operator-ratified rule has no carrier at all, and the intake that carries it says so in
   terms.** Intake #32's toolchain-parity + fail-closed attestation rule was ratified standalone at
   the 2026-08-11 GO. The intake states *"`[#453]` owns the container gaps; **the attestation rule
   is the part `[#453]` does not carry**"* — and `attestation` returns **zero hits** across
   `tasks/`, `BACKLOG.md`, `STANDING_RULINGS.md` and `scripts/` (the two PLAYBOOK hits are prose
   that explicitly routes the question back to intake #32). A ruling that names its own gap and
   still gets no owner is the complaint in its purest form.

3. **The sweep that ran nine hours ago left no verdict record for 84 of 86 ADRs.** Batch-7a lane b
   was contracted to classify **every** ADR CURRENT / STALE / SUPERSEDED-BY / TERMINAL-UNARCHIVED
   (its contract, step 1). It committed 8 rows and no report: `git diff --stat 99ec4b19^1 99ec4b19`
   shows 12 files, none of them an audit artifact beyond its own contract of record, and the batch
   packet's lane-b section reports only the archival count. **The classification exists nowhere in
   the tree.** So "does the tree implement this ADR's Decision?" was re-derived here from scratch
   rather than read.

---

## §1 · Method, and its honest limits

**Carrier test.** A decision has a carrier iff at least one of: (a) an open/deferred row in
`tasks/` whose *Done-when* would discharge it; (b) a landed mechanism (a script, hook, config or
gate) verified live; (c) a `STANDING_RULINGS` entry that IS the landing (not one that names an
unlanded home); (d) a recorded REJECT/SUPERSEDE with grounds. Anything else is an **orphan**.

**Dedupe rule.** A decision restated on several surfaces is one orphan, filed at its **oldest
committing source**, with the corroborating surfaces named. Intake #25's `copier` item, lane c's
§A #7, and ADR-109 §E's propagation tail are the same decision; it appears once.

**Ages** are from the committing artifact's own date to 2026-08-17.

**Four limits, stated so the counts are not over-read:**

- **`m` counts tests, not distinct decisions.** Surfaces overlap by construction — the disposition
  ledger, the north-star inventory and intake #27 all re-describe intake #25's W-items. The
  per-surface breakdown in §2 makes the overlap visible; `k` is deduped, `m` is not.
- **The ADR sweep tested Decision sections, not full ADR bodies.** An ADR whose Decision is
  implemented but whose *consequences* section names an unbuilt follow-on reads CARRIED here.
- **SEED intakes were tested against ADR-98 §6 only** (the survival metric), not clause by clause.
  A SEED is a parking lot per register L-1; it carries no decision to orphan.
- **Consumer repos were not read.** Two orphans (W-3 pre-commit native distribution, G3
  win-tooling remote) have execution that lands outside this repo; they are recorded as hub-side
  gaps, and their consumer-side state is lane c's §B measurement, not this lane's.

---

## §2 · Surfaces swept, and what each was tested for

| # | surface | population | decisions tested | orphans found |
|---|---|---|---|---|
| 1 | `docs/intake/` (live) | 34 docs — 14 ACCEPTED · 1 READY · 9 DRAFT · 10 SEED | 57 clauses of the 14 ACCEPTED + 1 READY | 25 |
| 2 | `docs/intake/archive/` | 7 docs | 7 terminal dispositions verified present | 0 |
| 3 | `docs/decisions/` | 86 live ADRs + `archive/` | 86 Decision sections | 2 |
| 4 | `protocols/STANDING_RULINGS.md` | sections A–O | 106 named entries (the M-table's 150 ids read as dispositions of items already counted) | 10 |
| 5 | `docs/handoffs/*/SUPPLEMENT.md` | 66 files | 20 ratified-in-chat register entries, across the 4 windows carrying one | 5 |
| 6 | `JOURNAL.md` | 20,444 lines | 43 ruling-bearing statements | 0 net (all resolve to surfaces 4/5) |
| 7 | `docs/audits/2026-08-17-technical-audit-disposition-ledger.md` | 80 dispositions | 80 + the 49-name follow-on list | 4 |
| 8 | `docs/audits/2026-08-17-census-north-star-inventory.md` | 78 master-table rows | 78 (incl. §A's 16 DECIDED-UNFILED) | 0 net (all dedupe into surface 1) |
| 9 | intake #27 tech-adoption ledger | 38 items | 38 | 0 net (all dedupe into surfaces 1/3) |
| 10 | `BACKLOG.md` / `tasks/` | 218 live rows (194 open + 24 deferred) | 30 `DEFER — peg:` clauses + 4 `depends-on` clauses | 3 |

**Totals: surfaces 10 · tests 598 · orphans 54 after dedupe.**

Surfaces 8 and 9 produced **zero net new orphans** — every DECIDED-UNFILED item lane c named, and
every unplaced row in the 38-item ledger, resolves to an intake clause already counted at surface 1.
That is a corroboration result, not an empty one: **three independent sweeps on three different
days reached the same set**, which is the strongest evidence in this report that the set is real
and that nothing has moved it.

---

## §3 · The orphans

Each: **source locator · the decision verbatim · age · proposed owner or disposition.**
Row drafts are collected in §4 and referenced here by `R#`.

### §3.1 · Register-promotion debt — 15 orphans, oldest 12 days

The class: a ruling that **names its own durable home** and never moved there. Every one below was
tested by literal grep against `protocols/PLAYBOOK.md`, `LESSONS.md`, `protocols/ESSENTIALS.md` and
`tasks/*.md`. **All 15 returned 0 hits at every declared home.** Owner: **R1**.

| # | locator | decision (verbatim, one line) | declared home | age |
|---|---|---|---|---|
| 1 | `STANDING_RULINGS.md` A1 | *"a failure that is a mechanical consequence of the arc's own diff, where the gate prints its own named fix and that fix clears it … is not a third failure"* | PLAYBOOK (verification §) | 12d |
| 2 | A2 | *"every disposition or exemption names its own expiry so it cannot outlive its reason"* | PLAYBOOK (disposition-register §) | 12d |
| 3 | A5 | *"the review-tool defect class where an over-broad suppression rule fails toward reporting nothing"* | LESSONS | 12d |
| 4 | A6 | *"a pending curated-baseline decision leaves the tree visibly dirty rather than stashed, bypassed, or unilaterally baselined"* | LESSONS | 12d |
| 5 | D1 | *"The exact `uv` pin is load-bearing for the entire organ mesh"* | PLAYBOOK (environment §) | 11d |
| 6 | D2 | *"Mid-flight corrections to a probe lane are indistinguishable from injection"* | PLAYBOOK (fan-out / lane-contract §) | 11d |
| 7 | D3 | *"A read of `origin/*` is evidence about the remote only after a fetch"* | LESSONS | 11d |
| 8 | D4 | *"A worktree lane's bare `pytest` tests the primary tree's environment"* | PLAYBOOK (batch-protocol §, `[#505]`) | 11d |
| 9 | E1 | *"a gap-week consumes at least one P-B eval; the bar is measured divergence, and an eval whose verdict is NO counts as a full success"* | PLAYBOOK (eval / adoption §) | 11d |
| 10 | F6 | *"The bg-isolation guard … stays as-is, everywhere"* + its sanctioned exact-match-patch route | *"a more durable home than this register"* | 10d |
| 11 | `2026-08-17-…-3/SUPPLEMENT.md:54` | *"audit-to-row conversion authority · every audit carries exactly one disposition ACTIONED/FILED/REJECTED/SUPERSEDED"* | PLAYBOOK batch-close § | 0d |
| 12 | same | *"admission control · local batch width bounded by measured schedulable concurrency, default 6 on this machine class"* | PLAYBOOK §8 | 0d |
| 13 | same | *"reserved id blocks · concurrent-birth safety via per-lane disjoint id ranges printed at dispatch"* | PLAYBOOK batch protocol | 0d |
| 14 | same | *"PINNED-BY-TESTS section · mandatory lane-contract section listing live-tree properties the lane legitimately changes"* | PLAYBOOK §8b | 0d |
| 15 | same | *"teleport one-way / no VS-Code-attach to remote bg · substrate constraint from wf-fe444def"* | intake #39 ratification | 0d |

**Two findings inside this block that are not just "unlanded":**

- **#8 names `[#505]` as a co-home, and `[#505]`'s Done-when does not carry it.** Read live: the
  row's Done-when is *"a fresh seat runs a full batch from repo artifacts alone; the next batch
  executes under it …; hygiene WARN and branch-prefix enum are validator-checked; the
  refuse-to-finish checklist is mechanical."* Per-lane `uv run --locked` appears nowhere in it. A
  named row is not the same as a discharging clause, and this is the difference.
- **#12's own provenance line is false.** The register says the admission-control candidate
  *"landed in LESSONS at batch-6 wrap — promote"*. `grep -c admission LESSONS.md` → **0**. The
  promotion debt is one step deeper than the register believes.

`priority order v2` — the sixth term in that supplement's §7 — is **NOT** counted as an orphan: its
declared home is the supplement amendment itself, which is landed (56 insertions, 0 deletions).

### §3.2 · Intake #25's W-wave — 11 orphans, all 12 days

`docs/intake/2026-08-05-func-simplification-distribution-wave.md`, `status: ACCEPTED`,
`disposition: active`, `decided-by` the 2026-08-11 batch-4 GO. Its own §F priced *"~6–8 births"*.
**Births to date: zero.** Every item below was carrier-tested by grep over `tasks/*.md`.

| # | item | decision (verbatim, one line) | carrier test | disposition |
|---|---|---|---|---|
| 16 | **W-1** copier | *"the deployable shape of .dev-knowledge becomes a copier template"* | `copier` → 1 hit in `tasks/`, inside `[#387]` as a *do-not-ingest* mention | **R2** |
| 17 | **W-2** kernel/lab split + package | *"The kernel ships as an installable package from the hub (git-tag-pinned dependency: `uv add dev-knowledge-kernel @ git+<hub>@vX.Y`)"* | `dev-knowledge-kernel` → **0 hits tree-wide** | **R2** (also unblocks #52) |
| 18 | **W-3** pre-commit native distribution | *"Consumers' `.pre-commit-config.yaml` references the hub repo + rev"* | no row; lane c measured 2 of 5 consumers with no `.pre-commit-config.yaml` at all | **R2** (also unblocks #52) |
| 19 | **W-4** reusable workflow | *"`kernel.yml` lives in the hub; every consumer's workflow is three lines of `uses:`"* | `reusable workflow` → 0 hits in `tasks/`; only the hub's own `report-only-wall.yml` exists | **R2** |
| 20 | **W-5** pytest-testmon | *"Test-impact analysis … re-runs only tests affected by the change"* | `testmon` → **0 hits in `tasks/`** | **R2** |
| 21 | **W-6** schema-as-code | *"Schemas replace hand validators for ecosystem/\*.yaml and tasks/\*.md frontmatter"* | `check-jsonschema` → **0 hits in `tasks/`** | **R2** |
| 22 | **W-7** sphinx-needs | *"Full migration is a study row with a measured pilot, not a commitment"* | 0 hits; P-D dormant since filing | **SUPERSEDE** (§5.1) |
| 23 | **W-8** local-vs-reference matrix | *"code and structure by reference (versioned, updatable), state and identity local"* — proposed as **the standing rule** | 0 hits; intake #27 row 20 calls it *"candidate for a one-line register ruling"*, never made | **R2** |
| 24 | **W-9(b)** VISION→README | *"**VISION.md → README.md** — the universal repo front door"* | `VISION.md` is live at hub root; CLAUDE.md §5 rule 5 forbids recreating root `README.md` | **REJECT** (§5.2) |
| 25 | **W-9(d)** skills symlink | *"`.claude/skills/` ↔ `.agents/skills/` via symlink (same standards family)"* | 0 hits; its parent W-9(a) was reversed by ADR-53 | **REJECT** (§5.3) |
| 26 | **V-6** seal velocity metrics | *"Three numbers join the seal report: lead time per row (open→merged), operator interactions per arc, wall-clock per arc"* | register H2 legislates a *different* trio (`opened · closed · net · open-total`); intake #27 row 29 grades V-6 `PARTIAL(qualitative only)` | **R2** |

**V-4** (*"Local pre-commit target: <60s"*) is **carried** — `[#317]`'s Done-when names a sub-60s
targeted run. **V-1/V-2/V-3/V-5** are landed (batch protocol, this register, prompt-template v1.6,
`[#429]` closed). **W-10** is carried by `[#341]` + `[#491]` + `[#492]`. Those five are the
counter-examples that make the eleven above legible as gaps rather than as the whole wave.

### §3.3 · Intake #28 — 5 orphans, 9 days

`docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md`, ACCEPTED 2026-08-11.
Its acceptance criterion has three limbs; **limb 1 landed (ADR-112 + the §B flip), limbs 2 and 3
did not.**

| # | clause | decision (verbatim, one line) | carrier test | owner |
|---|---|---|---|---|
| 27 | §B | *"Hub reaches v1.0 when ALL hold"* — the 8-clause DONE-manifest | `DONE-manifest` → 0 hits tree-wide; `[#505]` (which the disposition ledger names as owner) is the **batch-protocol** row and its Done-when contains no clause of the manifest | **R4** |
| 28 | acceptance limb 2 | *"§C verdicts recorded into ledger #27 as a cross-referenced amendment"* | intake #27's amendments stop at *"Ratification amendment — 2026-08-08 (batch-3 GO)"*; no §C amendment exists | **R3** |
| 29 | §C | *"DE-FACTO ADOPTED — formalize (one ledger line)"* — `gh` CLI | no ledger line; lane c §A #15 calls it *"smallest-cost item on this list"* | **R3** |
| 30 | §C | *"Tier S · TRY-NOW: ponytail · skill-creator (anthropics/skills)"* | `ponytail`/`skill-creator` → **0 hits tree-wide**; no trial, no KEEP/DELETE line | **R3** |
| 31 | §D + acceptance limb 3 | *"§D items visible in the successor's planning surface"* — 4 organ candidates | 2 carried (`[#271]` harvest, `[#491]`/`[#492]` bake-off); **skills-first universalization** and **hub-as-copier-template** appear on no planning surface | **R4** |

### §3.4 · Intakes #29 / #30 / #31 / #32 — 9 orphans, all 8 days

| # | source | decision (verbatim, one line) | carrier test | owner |
|---|---|---|---|---|
| 32 | #29 Fold B | *"Ruled by this consolidation as a **landing predicate on new and touched rows** — never a backfill migration"* (`footprint:`) | **6 of 218 live rows** carry `footprint:`; `grep footprint scripts/validate_backlog.py` → **0** — nothing checks it | **R5** |
| 33 | #29 Fold B | *"a committed, regenerated JSONL **edge log** that the *existing* validators emit into"*; storage *"**open**, not ruled"* | `edge log` / `DuckDB` → 0 hits in `tasks/` and `scripts/` | **R6** |
| 34 | #30 §B leg 1 | *"a pin strategy that a fresh container can satisfy (`mise` or equivalent)"* | `mise` as a token → 0 real hits in `tasks/` (all matches are substrings of *promise*/*compromise*) | **R7** |
| 35 | #30 §C(1) | *"name the class in the batch protocol — batch width has an operator-machine cost"* | 0 hits in PLAYBOOK Ch8; the sibling `admission control` term (#12) is the same gap arriving from the other side | **R8** |
| 36 | #31 §B | *"the mechanism stack, in adoption order (each retires something)"* — ruff families · type checker + baseline · count ratchets · import-linter · agent gates · config package + copier | `import-linter`, `mypy`, `basedpyright`, `PLR0912`, `pep8-naming` → **0 hits in `tasks/`**; `[#407]` owns only §A's paradigm/naming half | **R9** |
| 37 | #31 §C | *"`semgrep` custom rules are the mechanical form of the library-first rule"* + `deptry` | `semgrep`, `deptry` → **0 hits tree-wide** | **R9** |
| 38 | #31 §D | *"**SecD BINDS: no refactor row is born before a hotspot measurement**"* (`decided-by`, verbatim) | `hotspot` → **0 hits** in `tasks/`, `protocols/`, `BACKLOG.md`. The ruling's own **binding precondition on §B has no owner**, so §B cannot legally start | **R9** |
| 39 | #31 §E | *"§E recorded in the do-not-relitigate register"* (acceptance criterion) | `Goodhart`, `Shepperd`, `Maintainability Index` → 0 hits in any register | **R9** |
| 40 | #32 | *"Any remote executor must reproduce the exact `uv`/hook toolchain from the lockfiles and **fail closed if a gate did not run**"* — ratified STANDALONE, report-only form | `attestation` → 0 hits in `tasks/`, `BACKLOG.md`, `STANDING_RULINGS.md`, `scripts/`; the intake itself states `[#453]` does **not** carry it | **R7** |

**#38 is the sharpest of these** and deserves naming separately: intake #31's own `decided-by`
makes the hotspot measurement a **precondition** on the whole §B stack, and then nobody owns taking
the measurement. Six ratified mechanism items are gated behind an unowned prerequisite — which is
the transitive-orphan pattern of §3.8, occurring inside a single ratification.

### §3.5 · Intake lifecycle and one older operator item — 2 orphans

| # | source | decision (verbatim, one line) | age | owner |
|---|---|---|---|---|
| 41 | `docs/intake/README.md` §7 / ADR-98 §6 | *"intake docs sitting unconsumed after **~1 month of operation** trigger a review of the scene for removal"* | **41d** | **R11** |
| 42 | intake #17 §6 R-N | *"Confirm 8 days as the overdue-ruling threshold (Fibonacci per §3.2) — or name another family member"* | 23d | **R10** |

**#41 is the oldest orphan in this census and it is the rule that would have caught the rest.**
The metric has fired on **seven live documents** and nothing dispositioned any of them: intake #4
and #5 (SEED, 2026-07-07, **41 days**), #6/#7/#8/#9 (SEED, 2026-07-08, 40 days), and #15 (READY,
2026-07-16, 32 days). The precedent for what should happen exists and was executed once — register
I-D7 fired this exact metric on intake #10 at 31 days, opened the review, and the operator rejected
and archived the doc. It has not fired since. Intake **#15** is the costliest instance: it holds
four operator-approved, ready-to-fire onboarding execution prompts, and lane c's consumer survey
measured **zero deployed runbooks in any repo, hub or consumer** — an approved execution artifact
sitting unfired for a month while the gap it closes is separately reported as a top-10 cost. It is
also partly stale on its own terms: two of its four targets (`life-architect`, `demo-prep`) are not
in the ADR-104 five-repo member set.

**#42 is the meta-item.** An 8-day overdue-ruling threshold, had it been confirmed 23 days ago,
would have escalated most of §3.1–§3.4 automatically. `[#488]` carries *"Fibonacci binding for any
estimated field"* but not the threshold; the two were separated when #488 was written and the
threshold half fell out.

### §3.6 · ADR-level — 2 orphans

| # | source | decision (verbatim, one line) | carrier test | owner |
|---|---|---|---|---|
| 43 | ADR-111:117-120 | *"it should be measured on the next two audits before any gate is proposed"* (the n=2 clause) | no row owns taking the measurement; **register I-D9 defers the `kill-candidates:` refusal check *behind* it**, so an unowned measurement is blocking a designed gate. ≥6 audits have landed since | **R12** |
| 44 | ADR-112 §Tier S | *"Install → 30-minute sandbox try → KEEP or DELETE → **one ledger line either way**"* | no ledger surface is named anywhere for Tier S lines, and **zero lines exist**; the two TRY-NOW candidates (#30) have never been tried | **R13** |

The other 84 Decision sections tested CARRIED or were verified landed. Notable near-misses that are
**not** orphans, recorded so a re-sweep does not re-raise them: ADR-83 (`protocols/archive/` exists
with two tombstoned files), ADR-97 (`epic/` is in `LANE_PREFIXES`; zero epic branches is usage, not
a gap), ADR-90 (`validate_doc_code_edge.py` implements the N-site resolver), ADR-109 §E (the chain
is `[#382]`→`[#383]`→`[#385]`, all live — its *propagation tail* is the copier orphan #16, counted
there, not twice).

### §3.7 · Audit-corpus residue — 4 orphans

| # | source | the item | age | owner |
|---|---|---|---|---|
| 45 | disposition ledger §2, `2026-08-16-census-nb6-archive-sweep` | **PENDING**: *"does the operator GO the 3 intake status transitions (#26, #28, #18) and the `[#300]` handoff-bundle deletion?"* — the sweep's own §1.3: *"3 documents are fully discharged and would become archivable the moment someone proposes the status flip — **and nothing proposes it**"* | 0d | **ESCALATE** (§5.4) |
| 46 | disposition ledger §2, `2026-08-14-qa-night2-quality` | **PENDING**: *"do the seven LOW findings … get an owner, or are they recorded accepted-with-reason?"* | 3d | **R16** |
| 47 | disposition ledger §4 | 49 earlier uncited audits, *"a named list, not a row"* — and the ledger's own §3 says a packet **Owed** list is *"a list that owns nothing and is watched by no organ"* | 0d | **R14** |
| 48 | batch-7a lane b contract step 1 vs `99ec4b19` | *"Classify **every** ADR (86 live …) into exactly one of CURRENT / STALE / SUPERSEDED-BY / TERMINAL-UNARCHIVED"* — 8 rows committed, **no verdict record for the other 84** | 0d | **R14** |

**#47 and #48 are the same defect at two scales**, which is why they share a row draft: a
classification pass whose *output* was a list or nothing at all, rather than a durable artifact
anything reads. #47 is self-aware about it — the ledger names the pattern in §3 while creating a
fresh instance of it in §4.

### §3.8 · Adjudication residue and transitive orphans — 6 orphans

| # | source | the item | age | owner |
|---|---|---|---|---|
| 49 | `2026-08-15-…-night2-consolidated-briefing.md` D3.1 | `N2-D1-02` — *"**STILL PROPOSED · trigger now MET** — W3 landed 2026-08-13; `[#513]` DISCHARGED"*. Ruled *"reassess after W3 lands"*; W3 landed, nobody reassessed | 2d | **R10** |
| 50 | same, D3.2 | intake #33 — *"born as ruled (one doc, Sections A/B/C) and is sitting at `status: DRAFT` awaiting ratification"* | 5d | **R10** |
| 51 | same, D3.3 | `N2-D2-iii` — *"**STILL OPEN** — the six sunset/review candidates stand with their named blockers"* | 5d | **R10** |
| 52 | `[#294]` + `[#308]` | both carry `DEFER — peg: the intake #25 W-wave carrier decision (W-2/W-3)`; register **L-7**: *"**that decision has no in-repo referent**"*, and *"the re-peg decision is **owed at the consolidation-intake filing**"* — that filing is intake #33, still DRAFT (#50) | 8d | **R15** (unblocked by **R2**) |
| 53 | `[#325]` | *"DEFER — peg #221 **DEAD, unreplaced** 2026-08-09 … **Stays open, stranded**"* | 8d | **R15** |
| 54 | `[#102]` | *"DEFER — peg: a repo whose codemap is generator-MANAGED (#262/#295 closed 2026-07-25 … **so no fleet codemap migration is coming to peg on**)"* | 23d | **R15** |

**These six are one shape: a decision parked behind a condition that cannot fire.** The repo has
already ruled the fix for exactly this — register I-D item 13, on `[#322]`: *"a peg whose referent
will not occur tests nothing, so the trigger is a date."* That ruling was applied once, to one row,
and never generalized. `[#102]`, `[#325]`, `[#294]` and `[#308]` are four rows in the same
condition today.

Two `depends-on` clauses were also tested and are **inert but already owned**: `depends-on: 390`
and `depends-on: 383` are written bare, and `[#424]` records that `_DEPID_RE` requires a `#`. Not
counted as orphans — `[#424]` is the carrier.

---

## §4 · Row drafts — 16, ready to birth

Each is schema-shaped for `tasks/`: title, one-line why, testable Done-when, size, flush-left
`kill-candidates:`, `source:`. **Sizes were checked against the `[P][S|M|L]` enum** — the batch-7a
lane-a ledger records `validate-backlog` refusing an `XS`, and that refusal is not re-earned here.

**R1 — Promote the 15 register rulings that name their own unlanded home**
Why: fifteen ratified rulings each declare a durable home and none reached it; a ruling reachable
only from a register an agent may not read is a ruling with no teeth.
Done when: each of `STANDING_RULINGS` A1, A2, A5, A6, D1, D2, D3, D4, E1, F6 and the four
2026-08-17 supplement §7 terms (`audit-to-row conversion authority`, `admission control`,
`reserved id blocks`, `PINNED-BY-TESTS section`) plus `teleport one-way` either appears at its
declared home (grep-verifiable, one named locator per entry) or carries a re-homing note with a
reason; the false *"landed in LESSONS at batch-6 wrap"* provenance on `admission control` is
corrected; and `D4`'s clause is either written into `[#505]`'s Done-when or re-homed.
Size: **M** · kill-candidates: `none — no open row owns register-to-home promotion; [#538] owns the
NB4-C twelve-act PLAYBOOK gap, which is a disjoint set of acts` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.1

**R2 — Disposition every intake-#25 W-item, and rule the W-2/W-3 carrier decision**
Why: an ACCEPTED, `disposition: active` intake priced ~6–8 births and produced zero in 12 days,
while two live rows are deferred behind one of its unmade decisions.
Done when: each of W-1, W-2, W-3, W-4, W-5, W-6, W-7, W-8, W-9(b), W-9(d) and V-6 carries exactly
one of — a named owning row, a REJECT with grounds, or SUPERSEDED-by with its successor — recorded
at intake #25 as an appended amendment; and the W-2/W-3 carrier decision named by `[#294]`/`[#308]`
resolves to a locator those two rows can cite.
Size: **M** · kill-candidates: `none — [#387] mentions copier only as a do-not-ingest note, [#293]
owns runbook fan-out not template distribution, and no open row owns any W-item` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.2

**R3 — Discharge intake #28 §C: the three ledger lines it is owed**
Why: an acceptance criterion that says *"recorded into ledger #27 as a cross-referenced amendment"*
was never executed, so ten classified verdicts including two TRY-NOW skills live only in the intake.
Done when: intake #27 carries a dated §C cross-reference amendment; the `gh` de-facto-adoption
ledger line exists; and `ponytail` + `skill-creator` each carry a Tier-S KEEP or DELETE line under
ADR-112's *"one ledger line either way"*.
Size: **S** · kill-candidates: `none — [#502] is the mutmut Tier-L eval and owns no Tier-S line;
[#491]/[#492] own provider lanes, not skills` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.3

**R4 — Hub DONE-manifest v1.0 tracker**
Why: the eight-clause finish line was ratified at the batch-4 GO and no row measures it, so
*"zakończyć .dev-knowledge"* has a definition and no instrument.
Done when: one surface reports all 8 clauses of intake #28 §B with a live measurement per clause and
its filter named (register H2), and intake #28 §D's `skills-first universalization` and
`hub-as-copier-template` each appear on it as tracked or explicitly out-of-scope.
Size: **S** · kill-candidates: `none — [#505] is batch-protocol encoding and its Done-when contains
no §B clause; [#555] owns net-negative closure, which is clause 2 only` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.3

**R5 — Enforce the ruled `footprint:` landing predicate**
Why: ruled as a landing predicate on new and touched rows 8 days ago; 6 of 218 live rows carry it
and no validator reads the field.
Done when: `validate_backlog` (or the filing-backpressure hook) requires `footprint:` on an added or
edited row, with the never-a-backfill scope stated in the check's own docstring and a test pinning
that an untouched legacy row does not fire.
Size: **S** · kill-candidates: `none — [#424] owns depends-on parsing, not footprint presence` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.4

**R6 — Rule the edge-log storage question before any graph work**
Why: intake #29 Fold B flags storage as *"one of the memo's two least-defended sections … reads like
a decision and is not"*, and the open question blocks the whole dependency-graph leg.
Done when: DuckDB-vs-SQLite-vs-plain-JSONL is ruled with a measured basis or recorded
deliberately-deferred with a trigger, and `[#383]`'s Done-when cites the ruling.
Size: **S** · kill-candidates: `[#383] — execution waves per surface, if the architect rules the
edge log is that row's v1 rather than a sibling` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.4

**R7 — Cloud toolchain pin + fail-closed gate attestation**
Why: the one rule intake #32 exists to get ratified was ratified and given no carrier, and the
intake states in terms that `[#453]` does not carry it.
Done when: a remote/cloud lane cannot report green without an attestation that names which gates
executed; a run whose gate mesh did not execute is reported UNTRUSTED rather than passing; and the
pin strategy (intake #30 §B leg 1) is either landed or recorded declined with its reason.
Size: **M** · kill-candidates: `none — [#453] owns the three named container gaps and its Done-when
stops at a runbook plus a preflight assert; [#484] owns the ADR-106 divergence deferral` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.4

**R8 — Name the batch-width externality class in the batch protocol**
Why: parallelism has a measured operator-machine cost (indexing, search, `git status`, disk) that no
doctrine names, and the sibling `admission control` term arrives at the same gap from dispatch.
Done when: PLAYBOOK Ch8 states the class, names cloud routing as its release valve, and cites the
measured default width; `admission control` retires from the promotion-debt list by landing here.
Size: **S** · kill-candidates: `[#528] — lane-latency, if the architect rules width-cost and
suite-cost are one measurement rather than two` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.4

**R9 — Code-style mechanism stack: run the binding hotspot measurement first**
Why: intake #31's `decided-by` makes the hotspot measurement a **precondition** on the whole §B
stack and gives it no owner, so six ratified mechanism items are gated behind an unowned step.
Done when: the churn×complexity hotspot measurement is run and recorded; §B's six items are then
each scheduled or declined against it; `deptry`+`semgrep` carry a scheduled slot or a decline; and
§E's caveats are in the do-not-relitigate register.
Size: **M** · kill-candidates: `none — [#407] owns §A's paradigm/naming half only and explicitly
files no build; [#533] is the audit.py decomposition, which import-linter would guard but does not
own` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.4

**R10 — Overdue-decision staleness organ, and the four decisions it would already have caught**
Why: intake #17 §6 R-N asked for an overdue-ruling threshold 23 days ago; without one, a PROPOSED
item whose trigger has fired is invisible, which is how D3.1's met trigger, intake #33's
ratification and six ADR review candidates all went quiet.
Done when: the threshold is confirmed (or another Fibonacci member named); a detector surfaces a
PROPOSED/DRAFT decision past it; and the four live instances — `N2-D1-02`, intake #33, `N2-D2-iii`,
and R-N itself — each carry a disposition.
Size: **M** · kill-candidates: `[#488] — priority axis, which carries the Fibonacci binding but not
the threshold; fold only if the architect rules ranking and staleness are one function` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.5, §3.8

**R11 — Disposition the seven intakes whose survival metric has fired**
Why: ADR-98 §6's metric has fired on seven live documents for up to 41 days with no review, and the
costliest (#15) holds four operator-approved onboarding prompts against a measured zero deployed
runbooks fleet-wide.
Done when: each of intake #4, #5, #6, #7, #8, #9 (SEED) and #15 (READY) carries a recorded
disposition on the I-D7 precedent — fire, re-scope, or REJECT-and-archive with a reason — and #15's
two non-member targets (`life-architect`, `demo-prep`) are reconciled against ADR-104.
Size: **S** · kill-candidates: `[#552] — its leg (b) proposes ADR-98 §6 breaches going forward; this
row disposes the seven that already fired, which a forward-looking proposer never reaches` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.5

**R12 — Take ADR-111's n=2 measurement, then build or refuse G-3**
Why: an unowned measurement is blocking a designed gate — register I-D9 defers the
`kill-candidates:` refusal check explicitly behind this clause, and ≥6 audits have landed since.
Done when: the finding-triage rule is measured on two named audits, the result is recorded, and the
G-3 refusal check is built or refused on that evidence.
Size: **S** · kill-candidates: `none — [#555] owns the kill-candidates *collection* step at close
time; this is the refusal check at proposal time, which I-D9 names as a separate organ` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.6

**R13 — Give ADR-112's Tier-S ledger a home**
Why: the ADR mandates *"one ledger line either way"* and names no surface, so the mechanism that
stops a candidate being re-tried every quarter cannot be written to.
Done when: the Tier-S ledger surface is named at a canonical home, its line shape is stated, and the
first entries exist (the #30 TRY-NOW pair, either direction).
Size: **S** · kill-candidates: `none — intake #27 §A is the Tier-L adoption ledger and ADR-112
distinguishes the tiers by construction` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.6

**R14 — Second-pass disposition: the 49 named audits and the 84 unrecorded ADR verdicts**
Why: two classification passes this window produced a bare list and nothing respectively, and the
disposition ledger's own §3 names that shape as *"residue the standing ruling exists to convert."*
Done when: each of the 49 named follow-on audits carries a disposition under the 2026-08-17 standing
ruling, and every ADR carries a recorded CURRENT/STALE/SUPERSEDED-BY/TERMINAL-UNARCHIVED verdict in
a durable artifact rather than in a lane's session.
Size: **M** · kill-candidates: `[#551] — the per-audit status field, which is the *carrier* this
row would write into; land [#551] first and this row becomes a population pass rather than a design`
· source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.7

**R15 — Repair the four rows parked behind a condition that cannot fire**
Why: register I-D item 13 already ruled the fix — *"a peg whose referent will not occur tests
nothing, so the trigger is a date"* — and it was applied to one row and never generalized.
Done when: `[#102]`, `[#325]`, `[#294]` and `[#308]` each carry a live peg — a date, or an id that
resolves — and a check refuses a new `DEFER — peg:` naming a closed or non-existent id.
Size: **S** · kill-candidates: `none — [#424] owns depends-on inertness, which is a different clause
and a different parser; no open row owns peg liveness` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.8

**R16 — Owner-or-accept for the qa-night2 LOW set**
Why: the disposition ledger left seven LOW findings PENDING precisely because disposition is
per-artifact and not per-finding, so they are owned by nothing.
Done when: L-1..L-4, L-6, L-7 and the L-5 maintenance cost each carry an owning row or a recorded
accepted-with-reason entry, and the choice between the two is stated once rather than per finding.
Size: **S** · kill-candidates: `[#529] — M-2/M-3/L-5 already feed it; fold those three and this row
covers the remainder` ·
source: `docs/audits/2026-08-17-census-nb7-orphan-census.md` §3.7

---

## §5 · Proposed dispositions — 3 reject/supersede, 1 escalate

**§5.1 · W-7 sphinx-needs — SUPERSEDE.** Grounds: the item is a *study*, not an adoption
(*"Full migration is a study row with a measured pilot, not a commitment"*), and its two named
extractable wins have both been overtaken. Win (a), `needs.json` as the fleet interchange format,
is now `ecosystem/schema/desired_state.py` under ADR-109 — a typed contract that shipped. Win (b),
conditional-link validation, is `validate_backlog._check_dep_references` plus `preflight_backlog_ids`,
both live. Successor: ADR-109. Intake #27 has graded it P-D dormant since filing and no trigger has
been named in 12 days.

**§5.2 · W-9(b) VISION→README — REJECT.** Grounds: `CLAUDE.md` §5 rule 5 records that root
`README.md` was **deleted 2026-05-23** under the ADR-38 A5 amendment as *"redundant with VISION +
CLAUDE.md + ARCHITECTURE for this internal-only repo"* and instructs *"do not recreate it."* W-9(b)
proposes recreating exactly that file. The intake did not know it was reversing a ruling — the
rename's premise is *"the universal repo front door"*, which is a public-repo argument applied to an
internal one. This is the same shape as W-9(a), which ADR-53 already reversed; recording it as a
reject rather than leaving it ACCEPTED-but-unbuilt is what stops it being re-proposed.

**§5.3 · W-9(d) `.claude/skills` ↔ `.agents/skills` symlink — REJECT.** Grounds: its stated
justification is *"same standards family"* as W-9(a), and W-9(a) is reversed (ADR-53; lane c's
master table records the reversal as a closed loop). With `AGENTS.md` retired fleet-wide and lane
c's survey confirming **no repo carries a root `AGENTS.md`**, an `.agents/` tree would be a
directory created for one symlink pointing at a standard the fleet has left — and ADR-101 Rule C
would refuse the path anyway without an operator approval nobody would be asking for on these
grounds.

**§5.4 · Ledger PENDING 1 — ESCALATE, deliberately neither a row nor a reject.** The item is
*"does the operator GO the 3 intake status transitions (#26, #28, #18) and the `[#300]`
handoff-bundle deletion?"*. A status flip is a ruling, not an execution — the archive sweep's own
lane-D row says so — so a row would be a process row for asking a question, which the 2026-08-17
standing ruling declines (*"the architect ruling births rows for CONCLUSIONS, not for lane
residue"*). It is carried here verbatim so the question survives this seat, and it is counted in
`k` because it is genuinely unowned. Note the coupling: **R11** proposes dispositions for a
different seven intakes; these three are already-discharged ACCEPTED docs awaiting a flip, and the
two sets are disjoint.

---

## §6 · What this census deliberately does not do

- **It births nothing and edits no row.** Sixteen drafts, zero commits to `tasks/`. Filing 16 rows
  against a capacity law that caps births — and against a window whose acceptance test is *net
  closure* (`[#555]`) — is the architect's call, not this lane's. The drafts are ordered by nothing;
  §3's ages are the only ranking input offered.
- **It does not re-open a settled decision.** Where a decision was ruled and landed, it reads
  CARRIED and does not appear. Where a decision was ruled REJECTED (vale, commitlint, Vibe Kanban,
  mnemosyne/hindsight, Backlog.md-as-engine, the two lock libraries), it is not relitigated.
- **It does not adjudicate lane b's ADR sweep.** #48 records that the verdict set is absent from the
  tree. Whether the classification was performed and not written, or not performed, is not
  determinable from `git`, and this report does not guess.
- **`m` double-counts across surfaces by design**, and §1 says so. Surfaces 8 and 9 contributed zero
  net orphans; presenting them as zero-value would be the dishonest simplification, because their
  agreement with surface 1 is the corroboration that makes `k` trustworthy.
- **Consumer repos were not read.** Two orphans have consumer-side execution; their hub-side gap is
  what is recorded.
- **One structural asymmetry, stated plainly:** the two sweeps that ran this window with *births
  authorized* (lanes a and b) produced 17 rows; the one that ran *births forbidden* (lane c)
  produced a 16-item DECIDED-UNFILED list that is still 16 items long, and this lane — also
  read-only — is adding 54. **A census with no birth authority cannot close the loop it measures.**
  That is not a complaint about the contract; it is the reason the same set keeps being re-found,
  and it is the single most actionable observation in this report.

---

**surfaces swept 10 · decisions tested 598 · orphans 54 · oldest age 41 days · row drafts 16 · reject/supersede 3**
