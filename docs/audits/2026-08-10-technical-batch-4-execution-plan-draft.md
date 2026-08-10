# Batch-4 execution plan — DRAFT — the browser seat adjudicates; nothing here is a decision

**Proposed lanes, frozen-contract skeletons, serialization order, integration walk, sizing.** The
mandated header declaration above is carried verbatim; the subject prefix exists only so the
generated `docs/audits/README.md` index line names what this file is.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** batch-4-execution-plan-draft
- **Seat:** CC (Opus 5), cloud lane N2, branch `claude/night-n2-batch4-plan-qmd38e`
- **Base:** `origin/main` @ `5455c2a2a008e0ce8cc1d8ac77d2835cfd767376` (fetched at lane start;
  the tip of ARC-9 queue lane 3)
- **Posture: READ-ONLY.** Zero births, zero edits, zero closes. No row / intake / ADR /
  `BACKLOG.md` / `JOURNAL.md` touched. No freshness-class verdict is issued anywhere below. This
  report is the lane's only write.
- **Every line below is a PROPOSAL.** Nothing here is ruled, and no lane is dispatched by this
  file. Items requiring a ruling that has not been made are marked **GATED(ruling)** at their site
  and collected in §9.

## Run conditions — what this lane could and could not do

- Cloud container, fresh clone. **The clone arrived SHALLOW — 293 commits, earliest 2026-08-06 —
  and was unshallowed before any history claim below was taken.** See the run-conditions finding
  immediately after this list; the distinction is load-bearing and not a formality.
- **No test run and no `audit.py health` run.** This lane changes no code; nothing below is
  reported as a test result. The three live measurements taken are named at their sites and each
  is a single read-only script or regex evaluation.
- **`uv` is not exercised here, and the container cannot satisfy the pin.** Live: `uv 0.8.17`
  against the ADR-106 `==0.11.19` pin, so every `uv run --locked` entry would refuse; `pre-commit`
  is not importable and `.git/hooks/` holds only samples, so **no gate ran on this lane's commit.**
  Every measurement below was taken with a bare interpreter over read-only modules that import no
  pinned dependency. Two validators were attempted and **could not run**:
  `validate_doc_structure.py` (`ModuleNotFoundError: markdown_it`) and, by the same cause, anything
  routed through `scripts/toc/`. Nothing they would have verdicted is claimed as verified.
  This is intake #30 §B's cloud-toolchain condition, witnessed again and still unruled.
- **The operator's machine, sibling repos and `~/.claude` are not reachable.** Any claim about a
  consumer repo below is carried from an input report and labelled as carried.
- **GitHub Actions run history is not readable from this seat** — the batch4-prep report's single
  scheduling-relevant UNCERTAIN (`[#502]`) is therefore *not* resolved here either.
- Filename verified against both consuming parsers before writing:
  `validate_hermetization.classify()` → `None`, `rule_a_violation()` → `None`,
  `rule_b_violation()` → `None`; and `PurePosixPath.match(batch_manifest.MANIFEST_GLOB)` → `False`,
  so **this file is not a batch manifest and grants no ADR-110 exemption.**

### The shallow-clone finding — intake #30 §B's condition, reproduced live and measured both ways

This is recorded as a run condition because it is also **evidence for a lane in this very plan**,
and because the size of the error is not obvious.

The container's clone was shallow: `git rev-parse --is-shallow-repository` → `true`, 293 commits,
earliest `b8957c9` (2026-08-06). Two of the SHAs this plan cites — `9fc1a8b4` (the 2026-07-21
refutation behind the K-4 supersession pointer) and `27c37ae3` (the `-n 0` mutmut fix) — were
**MISSING** from the object store, while `cf039756`, `12ef9c91`, `8f09c12d`, `19aca464`, `3cf3a5b0`
and `67e5518c` all resolved because they fall inside the shallow window. **A seat that spot-checks
a few SHAs and finds them present concludes the history is complete.** That inference is wrong, and
this lane made it before testing it.

**The measured cost, on one figure.** `git log --since=2026-06-01` counting `kill-candidates:`
lines in commit messages:

| | total | `none` branch | share |
|---|---|---|---|
| shallow (before `--unshallow`) | 38 | 38 | 100.0% |
| full history (after) | **351** | **332** | **94.6%** |

The shallow read is off by ~9× on the denominator and would have reported a **100%** formality rate
for a gate whose real rate is 94.6%. `git fetch --unshallow origin` was run (exit 0; 4812 commits;
`is-shallow-repository` → `false`), every missing SHA then resolved, and **only then** was the
figure taken. `origin/main` is unchanged at the base SHA after the fetch.

**Two consequences carried into the plan.** (1) The full-history figure **independently reproduces
batch4-prep's 331/350 at 94.6%** — a one-commit delta, which is one `none`-branch commit landing
between the two measurements. That is confirmation of Lane G's baseline, not a correction of it.
(2) It is a fresh instance of the class intake #30 §B names — *"the mandatory `--unshallow` before
any history claim"* — and it belongs in that intake's evidence at ratification. Recorded here; **no
intake is edited by this lane.**

---

## 1. Inputs consumed — the PARTIAL protocol, stated

Four inputs were named. Three resolved in-repo; one has no in-repo definition and is reconstructed
with its reconstruction declared.

| Input | Resolved as | Status |
|---|---|---|
| batch4-prep report | `docs/audits/2026-08-10-technical-batch-4-prep-evidence.md` (997 lines) | **read in full** — 6 evidence sheets, the 6×6 matrix, 6 skeletons, 4 paste-blocks, the F24-2 feature verdict |
| backlog-testability census | `docs/audits/2026-08-10-technical-backlog-testability-census.md` (891 lines) | **read in full** — all 170 gradings, the 42 P1/P2 drafts, §5 removal feed, §6 cheapest conversions, §8 questions |
| STANDING_RULINGS §I | `protocols/STANDING_RULINGS.md:707-874` | **read in full** — I-P0/I-P1, the 25-line I-D DEFAULT BLOCK, I-F1/I-F2/I-F3, I-I1/I-I2, I-D2 |
| the research-corpus distillate | `docs/audits/2026-08-09-technical-consolidation-report.md` §5.2 + §6 (the ARC-2 Phase-C triage: 229 items across OWNED / DISCHARGED / CANDIDATE / REJECTED / OPERATOR) | **read for the batch-4-relevant slice** — §6.2's (c) CANDIDATE table and §6.4's memo cross-check |

**Declared reconstruction — "the research-corpus distillate".** The phrase has no in-repo
definition. Three facts fix the referent and are recorded so the architect can overrule it in one
line: (1) `protocols/STANDING_RULINGS.md:820` and `JOURNAL.md:843` both name *"the distillate"* as
one member of the single ratification batch alongside intakes §A/#29–#32; (2) the consolidation
report's §5.2 checklist row *"3 the distillate: one table, LANDED-ALREADY column"* is marked
**COVERED → §6**; (3) the six research memo FILES are confirmed off-repo (Fable review Mandate 3 —
all six exist only as `compass_artifact_wf-*` files in the operator's Downloads, and the
consolidation report §11 records *"No memo file was landed … ADR-101 seals the tree against
inventing one"*). **So the distillate that exists in-repo is the §6 triage, not a memo corpus.**
Everything drawn from it below is drawn from §6.

**What that reconstruction costs, stated rather than hidden.** The `ingest-research-corpus` lane
named as *"last"* in the JOURNAL's three most recent `Next:` lines has **not run**. If that lane
is what produces the distillate the brief means, then this plan is built on the ARC-2 triage
instead — a superset in scope but a different artifact. **GATED(ruling) — see §9 G-9.**

---

## 2. The proposed lane set

Seven candidate lanes. Six are the classes the brief names; **Lane G is added from the batch4-prep
report's own §3.4 decomposition and is the one lane the brief did not ask for** — flagged so it is
trivially droppable.

| Lane | Worktree name | Branch | Subject | Size | Gate status |
|---|---|---|---|---|---|
| **A** | `lane-a-514-lane-regex` | `worktree-lane-a-514-lane-regex` | `[#514]` reconcile the two rival `LANE_BRANCH_RE` constants, provisioning-first | **M** | clear, with one empirical leg |
| **B** | `lane-b-270-operator-load-gauge` | `worktree-lane-b-270-operator-load-gauge` | `[#270]` operator-load gauge | **M** | clear; one leg GATED |
| **C** | `lane-c-132-organ-index` | `worktree-lane-c-132-organ-index` | `[#132]` organ-index generator — the feature-class lane | **M**, trending L | clear; scope choice owed |
| **D** | `lane-d-30-landing-predicate` | `worktree-lane-d-30-landing-predicate` | intake #30 §A — the landing-predicate organ (the A5 row) | **L** | **GATED(ruling) ×2** |
| **E** | `lane-e-28-donewhen-conversion` | `worktree-lane-e-28-donewhen-conversion` | Done-when conversion campaign from the census's 42 P1/P2 drafts | **L** (M if scoped) | **GATED(ruling)** |
| **F** | **unnameable — see §3** | — | the ARCHITECTURE soft-observations sweep | **M**, L tail | **GATED(ruling)** — no id exists |
| **G** | **unnameable — see §3** | — | the `kill-candidates:` refusal check + the ARC-7 §6-item-3 site (batch4-prep D+F, one lane) | **M** | **GATED(ruling)** — no id, birth unauthorized |

### 2.1 Why these subjects and not others

- **A `[#514]`** — P1, and the only row in the open set whose defect wedges the batch's own merge
  queue. batch4-prep Sheet B: `exempt()` requires an open manifest **and** a loose-regex match, so
  the sequence (provisioning refusal FIRST, delete the loose regex SECOND) is the row's load-bearing
  clause. Census: MECHANICAL, *"exactly ONE definition remains"* is grep-countable.
- **B `[#270]`** — P1, 34 days idle, unblocks three rows (`[#271]`, `[#348]`, and `[#117]`'s DEFER
  peg), and is the top-ranked feature-shaped row in batch4-prep's F24-2 verdict. Census: MECHANICAL
  on all three legs.
- **C `[#132]`** — batch4-prep's F24-2 rank **2**; rank 1 is `[#270]`, which is already Lane B. The
  literal `[#490]`-class successor is **`[#383]`**, and it is **not** proposed as a lane: `[#490]`
  is closed, and the census grades `[#383]` **DEFECTIVE** (its Done-when pins *"the 8 rows at
  `parity-surfaces.yaml:834-899`"*; live is **9** rows at **`:910-978`**). `[#383]` needs the
  re-scope in census §5 before it can carry a contract. Named substitute for C if the architect
  prefers: **`[#171]`** (rank 3, un-deferred 2026-08-09, un-blocks the `[#169]`/`[#322]` chain).
- **D — intake #30 §A** — the "A5" landing-predicate organ. See §9 G-1 for the two rulings it waits
  on and for what `A5` does and does not denote in-repo.
- **E — the conversion campaign** — the census drafted 42 conversions for the P1+P2 band and **21
  of them are Form E and nothing else**, so one register decision converts most of the lane.
- **F — the ARCHITECTURE sweep** — operator ruling I-D item 12 commissioned this as a batch-4 lane.
  Its *checkably-false* half is **already discharged**: ARC-9 lane 1 fixed 16 claims at `cf039756`
  and I-D2 superseded the review's count of 14 as a floor. What remains is the residual — see §4.6.
- **G — the batch4-prep D+F pair** — included because batch4-prep's matrix note 2 establishes they
  **cannot be separate lanes** (both re-stamp `CLAUDE.md`; `canonical_freshness` A2 wedges
  `audit-health`, a *pre-commit* gate, so it blocks even the commit explaining it).

### 2.2 What is deliberately NOT a lane

- **`[#502]` mutmut** — batch4-prep Sheet C shows two of its stated premises are false at HEAD and
  its size is unknowable until a `workflow_dispatch` runs. **A lane whose step 1 is a measurement
  is not a lane; it is a 10-minute pre-GO act.** Recommend the architect (or the integrator, from
  the primary) dispatches the pilot before the GO and the result decides whether `[#502]` is a lane
  at all. Not resolvable from this seat.
- **`[#510]`** — batch4-prep matrix note 5: it re-keys the same `exempt()` function Lane A deletes a
  regex from. **If both are in batch 4 they are ONE lane** — folded into A as an option, never a
  parallel lane.
- **Consumer-repo work** — the census's highest-yield untested cohort (27 open rows with an
  off-repo predicate; batch4-prep counts 17 open `[E6]` rows plus five named others). It is the only
  real *product/consumer* pool available to satisfy §8's cap, **and it cannot run from a cloud
  lane** (batch4-prep §2 recommendation). Not proposed here because this plan cannot verify a
  sibling repo; recorded as the batch's named blind spot.

---

## 3. The naming check — run, not asserted

Every proposed name was classified by the live validator, `scripts/validate_branch_naming.py`, in
this checkout. **Two of the seven lanes cannot be named conformantly, and the reason is the same
defect Lane A exists to fix.**

| Proposed worktree name | `validate_lane_worktree_name()` | `classify('worktree-…').kind` |
|---|---|---|
| `lane-a-514-lane-regex` | `None` (conforming) | `batch-lane` |
| `lane-b-270-operator-load-gauge` | `None` | `batch-lane` |
| `lane-c-132-organ-index` | `None` | `batch-lane` |
| `lane-d-30-landing-predicate` | `None` | `batch-lane` |
| `lane-e-28-donewhen-conversion` | `None` | `batch-lane` |
| `lane-f-architecture-soft-sweep` | **REFUSED** — *"does not match lane-\<letter\>-\<id\>-\<slug\>"* | **`unknown`** |
| `lane-g-filing-gate-and-boot-site` | **REFUSED** — same | **`unknown`** |

### 3.1 The grammar requires an id, and two lanes have no row

`LANE_BRANCH_RE` (strict, `validate_branch_naming.py:85`) is
`^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`. The `\d+` segment is **mandatory**. Lanes F
and G have no owning `tasks/` row — batch4-prep Sheet D searched and rejected `[#440]`, `[#488]`,
`[#487]`, `[#519]` as owners of the filing gate, and Sheet F records the ARC-7 site as *"a
knowingly-left-standing residual, declared in the file it lives in"* with no ticket. This lane
re-checked the ARCHITECTURE sweep against the `architecture` serialize-group rows and found the
same: no open row owns doctrinal re-derivation of `ARCHITECTURE.md`.

**Two grammar-legal workarounds exist and this plan picks neither**, because STANDING_RULINGS **F2**
(*"names, paths and identifiers derive from validators and enums"*) forecloses inventing one:

1. **A sentinel id.** `lane-f-0-architecture-soft-sweep` passes the validator (`\d+` accepts `0`) —
   verified live. But `0` as "no row" is a convention nothing in the repo defines. Inventing it in a
   batch plan is exactly the silent-enum-entry the naming rule's governing clause forecloses.
2. **Borrowing a non-task id.** Lane D's proposed name already does this: `30` is an **intake** id,
   not a task id, and the grammar cannot tell them apart. That is either a useful degree of freedom
   or an ambiguity, and it is the architect's to say which. Lane E's `28` has the same property.

**GATED(ruling) — G-2 and G-3 in §9.**

### 3.2 The finding this produced: `[#514]`'s defect is live inside batch 4's own lane set

Reproduced in this checkout, both regexes evaluated against the same string:

| Branch | loose (`batch_manifest.LANE_BRANCH_RE` — grants the ADR-110 exemption) | strict (`validate_branch_naming`) |
|---|---|---|
| `worktree-lane-f-architecture-soft-sweep` | **matches** | **`unknown`** |
| `worktree-lane-g-filing-gate-and-boot-site` | **matches** | **`unknown`** |
| `worktree-lane-a-514-lane-regex` | matches | `batch-lane` |

An id-less lane branch would therefore be **granted the ADR-110 anchoring exemption by the loose
constant while the naming validator classifies it `unknown`** — the exact disagreement `[#514]`
describes, arriving inside the batch that would fix it. Two consequences the plan must carry:

- It is **evidence for `[#514]`**, and Lane A's step 1 should record it in the packet as a live
  instance rather than as a hypothetical.
- **It is a sequencing hazard.** Once Lane A's provisioning refusal lands, an id-less lane
  provisioned *after* it is BLOCKED at boot. Ch8 dispatches all lanes from one plan, so in the
  normal case every lane is provisioned before any lane's work merges and the hazard does not fire
  — but a lane re-provisioned mid-batch (a teardown-and-retry, a late addition) would hit it.
  **Recommendation: the contract for Lane A states that the refusal is armed but the batch's own
  lanes are provisioned before it lands, and the packet reports whether any lane was
  re-provisioned.**

---

## 4. Frozen-contract skeletons — one per lane

**None of these is a frozen contract.** Each is a skeleton the architect freezes by supplying the
Done-when. Decision-budget stubs follow the V-2 shape the `/lane-boot` step-5 line states: escalate
only on (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) fork classes with no
standing ruling; everything else decided per contract and reported in the end packet.

**One clause belongs in every contract, verbatim** (batch4-prep §3.2, on the ARC-5 `19aca464`
precedent):

> `BACKLOG.md`, `tasks/manifest.json` and `ecosystem/doc-counts.md` are **generated**. On any
> conflict, regenerate; never hand-merge. Verify with the generator's `--check` exit 0 and a
> conflict-marker grep before staging.

**And one budget belongs in every contract that touches `protocols/`, `templates/` or
`ecosystem/*.yaml`** — see §5.3: the silent-rule ratchet has **headroom 1**.

### 4.1 Lane A — `[#514]` reconcile the rival `LANE_BRANCH_RE` constants

**Purpose.** Two constants share a name and disagree on grammar, so both organs cannot be enforced.
Reconcile to one, **in the row's stated order**, because the reverse order is a merge-queue outage.

**Candidate Done-when** (from batch4-prep Skeleton B, with leg 3 sharpened):

1. **Step 1 first.** Provisioning refuses an off-enum lane name: the boot path classifies
   `git branch --show-current` and BLOCKs on `KIND_UNKNOWN` under the `worktree-lane-` prefix.
   Pinned by a test asserting refusal on `worktree-lane-foo` **and on
   `worktree-lane-f-architecture-soft-sweep`** (this plan's live instance, §3.2) and pass on
   `worktree-lane-a-514-lane-regex`.
2. **Step 2 only after step 1.** `scripts/batch_manifest.py` imports the strict constant;
   `grep -c "LANE_BRANCH_RE *=" scripts/` returns **1**. Pinned by a test asserting the two modules
   resolve to the *same object*.
3. *"One clean batch runs under it"* — **empirical, not a test.** The contract names which batch
   discharges it. **GATED(ruling) G-4.**

**Steps.** (1) Re-measure the disagreement over real merged lane branches and put the count in the
packet — the row cites *"8 of 11"*; re-measure rather than carry it. (2) Build and test the
provisioning refusal. (3) Update `.claude/commands/lane-boot.md` step 1. (4) **Only then** collapse
the constants; run `tests/test_batch_manifest.py` and `tests/test_validate_branch_naming.py`. (5)
`protocols/PLAYBOOK.md` Ch8 + an append-only ADR-110 amendment marker **only if** the exemption's
shape moved. (6) Suite + gates; commit-and-STOP.

**Decision budget.** ESCALATE: whether `[#510]` folds in (same file, same function); whether ADR-110
needs an amendment marker (an ADR touch is (a)); how leg 3 discharges. DECIDE-AND-REPORT: which
module owns the surviving constant; whether the guard is a new script or a
`validate_branch_naming.py` mode; the refusal's exit code.

### 4.2 Lane B — `[#270]` operator-load gauge

**Purpose.** The gating first element of any Tier-2 nightly layer: a `[load]` funnel-count section
in the existing `fleet_health.py` SessionStart digest plus a per-run CSV. Its ex-ante metric and
pre-registered kill criterion **are** the contract.

**Candidate Done-when** (batch4-prep Skeleton A, unchanged — the census grades all three row legs
MECHANICAL and no conversion is owed):

1. `scripts/fleet_health.py` emits a `[load]` block carrying all five funnel counts, each from a
   live producer — pinned by a test seeding each producer and asserting the rendered count.
2. `logs/OPERATOR-LOAD.csv` gains exactly one row per digest run, header-stable — pinned by a test
   asserting append-not-overwrite across two runs.
3. `.gitignore` carries `logs/OPERATOR-LOAD.csv` — pinned by asserting `git status --porcelain` is
   clean after a run. (batch4-prep verified the line is **absent** today; the sibling ephemera are
   all listed, so this is an omission, not a policy.)
4. The closing commit carries `^load-gauge-metric:` and `^load-gauge-kill-criterion:` lines.
   **GATED(ruling) G-5** — it adds a commit-message convention.

**Steps.** (1) Read the digest assembly and the five producers; state which are already read and
which are new I/O. (2) Failing tests first. (3) Implement `[load]`. (4) CSV append + `.gitignore`.
(5) Regenerate `ecosystem/doc-counts.md`. (6) **`ARCHITECTURE.md` is OUT OF SCOPE for this lane**
under §5.2's recommendation — the owed Ch2/Ch6 row is collected by the integrator. (7) Suite +
gates; commit-and-STOP.

**Decision budget.** ESCALATE: leg 4's convention; whether the CSV is gitignored or tracked (the row
says gitignored — a durability requirement to the contrary is a (b) conflict). DECIDE-AND-REPORT:
column set and order; where in the digest the block renders; whether an erroring producer renders
`n/a` or omits its row.

### 4.3 Lane C — `[#132]` organ-index generator (the feature lane)

**Purpose.** Emit `docs/ORGAN-INDEX.md` on the established generator + freshness-hook pattern, so
the organ roster stops being something the operator supplies from memory. Absorbs `[#248]`.

**Candidate Done-when** — the census's §4 draft, quoted and then **narrowed**:

> *"the generator emits `docs/ORGAN-INDEX.md` covering every organ class enumerated in
> `ARCHITECTURE.md` Ch2's organ map, a regen-and-diff pre-commit hook FAILs on a stale index (with
> a test), and `ecosystem/doc-counts.md` reflects the new gate"*

**The narrowing, and why it is proposed rather than assumed.** As drafted, this lane lands a new
pre-commit gate — which historically forces a `CLAUDE.md` §9 roster row **and** an `ARCHITECTURE.md`
Ch2 gate-list row. Both are collisions (§5.2). Two scopings, architect's pick:

- **C-narrow (RECOMMENDED).** The lane ships generator + document + hook + `doc-counts`; the
  `CLAUDE.md` §9 and `ARCHITECTURE.md` Ch2 roster rows are **explicitly owed to the integrator**
  and named in the packet. Keeps the lane **M** and keeps it out of both collision files.
- **C-wide.** The lane owns its own roster rows — then **C and G are one lane**, for the same
  `canonical_freshness` reason batch4-prep gave for D+F.

**Steps.** (1) Read Ch2's organ map and fix the class denominator in the contract *before* writing
code. (2) Failing tests. (3) Generator, read-only (ADR-28/36 — Layer 2 never executes). (4)
Regen-and-diff hook on the `codemap-freshness` / `toc-freshness` pattern. (5) Regenerate
`ecosystem/doc-counts.md` — note it moves pre-commit gates 17 → 18, which **re-breaks `[#369]`'s
already-DEFECTIVE *"16 gates"* clause**; record that in the packet, do not repair it here.
(6) Suite + gates; commit-and-STOP.

**Decision budget.** ESCALATE: C-narrow vs C-wide; whether `docs/ORGAN-INDEX.md` is a new
top-level `docs/` file class (ADR-101 Rule A — `validate-hermetization` is prospective-only on
staged ADDs and **would fire on an unsanctioned new file class**; this must be checked before the
lane writes, not after). DECIDE-AND-REPORT: the generator's module name; the index's section order;
whether absent organ classes render as gaps or are omitted.

### 4.4 Lane D — intake #30 §A, the landing-predicate organ ("the A5 row")

**Purpose.** Every ruling that names an adoption carries a machine-checkable landing predicate, and
an organ verifies the set. Intake #30 §A calls this *"the highest-value item in the whole answer …
the only proposal here that makes future rulings self-policing"*.

**This lane cannot be frozen today.** Two independent gates, both unmade:

- **Intake #30 is `status: DRAFT`.** I-F2 records that the ratification flip *"lands ONLY in the
  single ratification batch at the GO with §A, #29–#32 and the distillate"*, and that ARC-9 left
  every intake `status:` untouched. Verified: #28–#32 are all DRAFT at this base.
- **FORK 4 — the births package at the batch-4 GO — is not answered.** STANDING_RULINGS §I says so
  in terms: *"FORK 4 (the births package at the batch-4 GO) is not answered here and is not recorded
  here."* The row this lane would build **does not exist**.

**Candidate Done-when (skeleton only, shape unchosen).** Intake #30 §A offers two shapes and defers
the pick to ratification *"against the library-first bar"*: (i) a check in `audit.py` reading the
rulings register, or (ii) the register gaining a `landed:` field validated by an existing validator.
A mechanically-testable phrasing exists for either, but writing it before the shape is picked would
be inventing the decision:

1. A ruled adoption with a declared landing predicate that is **absent** at ≥1 named site is
   reported, pinned by a test seeding a partial adoption.
2. The three live instances the challenge answer names are each conformant or exempted with a
   recorded reason.
3. The organ runs inside an existing gate set rather than as a new standing job (library-first bar).

**Note the overlap with `[#513]`.** `[#513]` (P2/M, open) is *"propagation completeness — a ruled
adoption that landed at some sites and not others"*, and its row text says **"the landing predicate
is the DETECTOR, not the fixes."** That is the same detector. **Whether #30 §A births a new row or
amends `[#513]` is a real fork and this plan does not pick it — GATED(ruling) G-1.** If it amends
`[#513]`, the lane is nameable today (`lane-d-513-landing-predicate`) and needs no birth.

**Decision budget.** ESCALATE: everything above; plus, if the shape is (i), `scripts/audit.py` is
the `audit-py` serialize-group's shared file and the largest such group in the census.
DECIDE-AND-REPORT: nothing until the shape is ruled.

### 4.5 Lane E — the Done-when conversion campaign

**Purpose.** Land the census's drafted conversions so the open set's finish lines become
verdictable. The census drafted **42** (every PROSE-CONVERTIBLE row at P1 or P2; there are no
PROSE-CONVERTIBLE P1s).

**The lane's size is decided by one ruling, not by its own work.** Census §8 Q2: *"Where does a
'recorded with a reason' record live?"* — 37 open rows carry an unhomed escape hatch, 30 are
PROSE-CONVERTIBLE for that reason alone, and **21 of the 42 drafts are Form E and nothing else**.
The drafts are written against `protocols/STANDING_RULINGS.md` and are paste-ready *if* that is the
ruled home; if a different home is named, the substitution is textual but must be made 21 times.
**GATED(ruling) G-6.**

**Candidate Done-when.**

1. Each of the N rows named in this contract carries its census-drafted Done-when **verbatim**, or
   a deviation is recorded per-row in the packet with its reason.
2. `gen_task_tree.py` regenerates cleanly; `BACKLOG.md` and `tasks/manifest.json` are byte-identical
   to a fresh regeneration (`--check` exit 0).
3. **No row's status changes and no row is born or closed by this lane** — verified by diffing the
   `status:` field of every touched file before and after.
4. `validate_doc_rot.scan_backlog_accretion` is not newly WARNing on any touched row — its threshold
   is ≥3 full `YYYY-MM-DD` dates **and** >700 chars, **or** >1200 chars (batch4-prep Block 1
   "Watch"). Edits are net-neutral in length where a row is near the bound.

**Steps.** (1) Freeze the row list — **N is the architect's, not the lane's.** (2) Apply drafts
in id order, committing in batches so a bad substitution is bisectable. (3) Regenerate. (4) Run the
accretion check over the touched set. (5) Suite + gates; commit-and-STOP.

**Scoping options, in ascending size.** **E-min (M):** the 21 Form-E-only drafts, after G-6 lands —
one substitution, 21 times, zero judgment. **E-mid (M/L):** E-min plus the census §6 top-10
cheapest, *"nine of the ten cost one sentence."* **E-full (L):** all 42.

**Decision budget.** ESCALATE: G-6; the row list N; whether any DEFECTIVE row's repair (census §5:
`[#359]` re-peg, `[#360]`, `[#241]`, `[#369]`, `[#383]`, `[#170]`, `[#505]` clause 2, `[#452]`) rides
this lane — **note `[#360]` was already converted to a dated review by ARC-9 (I-I1) on a premise the
census then refuted, so it is the architect's to revisit and is NOT touched here.**
DECIDE-AND-REPORT: commit batching; per-row deviations.

### 4.6 Lane F — the ARCHITECTURE soft-observations sweep

**"Soft observations" has no in-repo definition.** Grepped case-insensitively across the tree: zero
hits. The scope below is therefore **reconstructed from what the checkably-false half left behind**,
and the architect should correct it if the term meant something else. **GATED(ruling) G-7.**

**What is already discharged, so the lane does not re-do it.** ARC-9 lane 1 fixed **16** claims at
`cf039756`; **I-D2** superseded the Fable review's *"14 checkably-FALSE"* as a floor produced by a
bounded read. The `last_reviewed` stamp moved to 2026-08-10 with an honest limit in the header.

**The residual, from the fix commit's own words** — `cf039756`, STEP 3: *"HONEST LIMIT recorded in
the header: it did NOT re-derive doctrinal correctness against the full text of every cited ADR."*
That is the sweep's subject. Three candidate scope members, each with an in-repo locator:

1. **Doctrinal re-derivation** — each `ARCHITECTURE.md` claim that cites an ADR is checked against
   that ADR's text, not against the repo's current shape. This is the named residual.
2. **The anti-rot method, applied where it was not** — I-D2 records re-pointing a volatile
   cardinality *"at the surface that computes it"* rather than restating it, and names its expiry:
   *"retires when a mechanism computes these claims at stamp time."* A sweep can enumerate the
   remaining restated-value claims without fixing them.
3. **The Fable review's Low-severity ARCHITECTURE-adjacent items** — notably the **ADR-45
   index-vs-file inconsistency** (`docs/decisions/README.md:34` says *"Superseded by …"* while the
   file says *"Explored, not adopted"* — one of the two surfaces is wrong).

**Candidate Done-when.**

1. Every ADR-citing claim in `ARCHITECTURE.md` is verdicted against the cited ADR's text, with the
   verdict set recorded in a `docs/audits/` artifact (filename verified against the class enum
   first).
2. Each claim verdicted false is corrected **or** recorded with its reason for standing.
3. Where a claim restates a volatile value, it is re-pointed at the computing surface per I-D2, or
   the artifact records why it cannot be.
4. **The re-stamp obligation is the architect's to state, not this plan's.** I-D item 12 says
   *"re-stamp only once the fix lands"*, and Fable H3 killed the *"leave it honest and stale"*
   option. **This plan issues no freshness verdict and takes no position on the stamp.**

**Steps.** (1) Enumerate the ADR-citing claims mechanically before reading any of them. (2)
Verdict each. (3) Correct or record. (4) Write the artifact. (5) Suite + gates; commit-and-STOP.

**Decision budget.** ESCALATE: the scope reconstruction itself (G-7); the stamp; any correction that
would move doctrine rather than the map (`ARCHITECTURE.md`'s own preamble: *"Fix the map when
reality moves; fix the **source** when the doctrine moves"*). DECIDE-AND-REPORT: the artifact's slug;
the enumeration's exact predicate.

### 4.7 Lane G — the filing gate + the ARC-7 boot site (batch4-prep D+F, one lane)

**Purpose.** `check_backlog_filing.py`'s whole acceptance predicate is one regex (`:35`) with four
measured refusal gaps; and `CLAUDE.md` §6 item 3 plus its carrier still read *"Read most recent
handoff"*, the phrase §1 item 3 was fixed for. **One lane because both re-stamp `CLAUDE.md`.**

**Candidate Done-when** (batch4-prep Skeletons D and F, merged):

1. `check_backlog_filing.py` BLOCKs a bare `kill-candidates: none` with no reason — pinned by a test
   that flips one character. (Doctrine at `PLAYBOOK.md:3812` already requires the reason; the regex
   does not.)
2. It BLOCKs a line naming a `#id` with no file in `tasks/` — pinned with a fabricated id.
3. It BLOCKs **or** WARNs a line naming an id whose `status` is terminal — **architect's call**.
4. **No existing convention is retroactively invalidated** — the last 50 `kill-candidates:` lines
   are replayed through the new predicate and the block-count is reported **before** leg 3's
   severity is decided. (Measured baseline: **331 of 350** commit messages since 2026-06-01 take the
   `none` branch. **Re-measured on full history by this lane: 332 of 351 — 94.6%, reproducing
   batch4-prep's figure to one commit.** See the shallow-clone finding in Run conditions for why
   the re-measurement was not free.)
5. `templates/claude-regions/session-start-protocol.md` item 3 names the live predicate
   (`_select_active_bundle`, newest by **git add-date**), mirroring `first-read.md:5`; `CLAUDE.md`
   §6 matches it byte-for-byte so
   `tests/test_boundary_headers.py::test_hub_region_bodies_still_byte_match_the_templates` passes.
6. `PLAYBOOK.md` §10 and the `CLAUDE.md` §9 roster row state the gate's **actual** predicate.

**Steps.** (1) **Carrier first**, then the `CLAUDE.md` region — the order the coupling test enforces.
(2) Failing tests for the filing gate. (3) Extend the predicate. (4) Run leg 4 and put the number in
the packet before deciding leg 3. (5) Doc sites. (6) The `CLAUDE.md` cost: a genuine twelve-section
re-read, a §12 entry, an L10 version bump. **This lane is buying a `CLAUDE.md` re-read, not a line
edit.** (7) Confirm the ratchet is unmoved (§5.3). (8) Suite + gates; commit-and-STOP.

**Decision budget.** ESCALATE: **whether the filing-gate half earns a birth at all — it has none
today, and filing one costs a `kill-candidates:` line on its own filing commit, which is the gate
under review** (GATED(ruling) G-3, and it sits inside FORK 4's unopened pool); BLOCK vs WARN for
leg 3; whether a minimum reason length is imposed (a (c) fork class — no standing ruling on
prose-quality gates); whether consumer copies of the `session-start-protocol` region are in scope
(**UNCERTAIN — unresolvable from this seat**, and core-invariant #6 bars a unilateral `~/.claude`
edit). DECIDE-AND-REPORT: exact error text; whether the existence lookup reads `tasks/` or
`tasks/manifest.json`.

---

## 5. Dependency and serialization order

### 5.1 Hard dependencies

| Edge | Kind | Basis |
|---|---|---|
| **A before everything that re-provisions** | provisioning | §3.2 — once A's refusal lands, an `unknown`-classified lane branch is BLOCKed at boot |
| **A excludes `[#510]`** | same-file | batch4-prep matrix note 5 — same `exempt()` function; if both are in batch 4 they are ONE lane |
| **F owns `ARCHITECTURE.md` exclusively** | file | five of seven lanes plausibly touch it (§5.2) |
| **C-wide ⇒ C and G are one lane** | freshness gate | both re-stamp `CLAUDE.md`; `canonical_freshness` A2 wedges `audit-health`, a *pre-commit* gate |
| **D after the GO's ratification batch** | ruling | I-F2 — intake #30's flip is one atomic act at the GO |
| **D after FORK 4** | ruling | the row does not exist; FORK 4 is unopened |
| **E after G-6 (the Form E register home)** | ruling | 21 of 42 drafts are Form E and nothing else |
| **E last in the merge queue** | generated files | E touches up to 42 `tasks/` files; every other lane's close-time row edit regenerates the same two artifacts |

### 5.2 The two shared files, and the rule proposed for each

**`ARCHITECTURE.md`.** Plausibly touched by **B** (7 `fleet_health` mentions), **C** (Ch2 gate list
if C-wide), **D** (a new organ ⇒ the organ map), **F** (certain), **G** (1 mention, Ch2 gate list).
batch4-prep's recommendation was *at most ONE lane may edit it, or it is out of scope for all lanes
and the integrator collects the owed rows*. **This plan adopts the stronger form: F owns it; every
other contract declares it OUT OF SCOPE and names its owed row in the packet.** Reason: the file
carried claims that were already false under its own review stamp at `8f09c12d`, and a lane editing
it inherits that problem.

**`CLAUDE.md`.** Touched by **G** (certain — §9 roster + §6 region), **C-wide** (§9 roster row for a
new gate), **B** (UNCERTAIN — §9's SessionStart row names `fleet_health.py`; only fires if the
digest's *declared* contents change). It is freshness-gated, and the gate is **pre-commit**, so it
blocks even the commit that explains it. **Proposed rule: exactly one lane owns `CLAUDE.md` in
batch 4 — G by default. B and C declare it out of scope and owe their roster rows to the
integrator.**

**`protocols/PLAYBOOK.md`.** A (Ch8) and G (§10). Different sections of one 3800+-line file, so git
usually merges them — but `toc-freshness-playbook` fires on both, and *"different sections"* is
exactly the reasoning that produces a race. Marked OVERLAP deliberately.

**Generated files** (`BACKLOG.md`, `tasks/manifest.json`, `ecosystem/doc-counts.md`) are excluded
from the disjointness question by the §4 clause and the ARC-5 resolve-by-regeneration precedent.

### 5.3 The budget no file-disjointness matrix can see

**The silent-rule ratchet has headroom 1.** Measured in this checkout with
`python scripts/silent_rule_detector.py`:

```
detector: silent-rule-v4
files:    57
count:    440
```

against `ecosystem/silent-rule-baseline.yaml` `baseline: 441`. The corpus (`_SCOPE_RULES`) is
`protocols/*.md`, `templates/**/*.md`, `templates/**/*.tmpl`, `ecosystem/*.yaml`.

**Four lanes write inside that corpus** — A (`PLAYBOOK.md` Ch8), E (`STANDING_RULINGS.md`, if Form E
lands there), G (`PLAYBOOK.md` §10 **and** `templates/claude-regions/session-start-protocol.md`), F
(no corpus file — `ARCHITECTURE.md` is a root file and outside it). **They share one token of
headroom.** The check is a FAIL that blocks the commit through `audit-health`, and the baseline
*"may be LOWERED or held … not raised"* without an operator ruling.

**RECOMMENDATION: every contract touching the corpus carries the sentence** *"add no `must`,
`shall` or `never` token; phrase declaratively"* — the discipline `STANDING_RULINGS`' own editing
note already uses — **and the batch's first corpus-touching lane to merge re-measures and reports
the count in the packet.** Note the register's own editing note states *"live measurement equals the
committed baseline exactly (441 = 441)"*; the live figure is **440**, matching `cf039756`'s
*"unmoved at 440<=441"* and `CLAUDE.md` §12 v2.55. The note is one window stale. **Recorded as an
observation for the architect, not repaired here** — it is inside an immutable-adjacent register and
outside this lane's read-only posture.

### 5.4 Serialize-groups, and why they do not drive this order

Groups across the set: A none · B none · C `pre-commit-config` · D `audit-py` or `gates`
(shape-dependent) · E every group at once · F `architecture` (if a row existed) · G `gates` +
`claude-md`. **STANDING_RULINGS G2** governs: *"two rows sharing a `serialize-group` MAY run
parallel iff their file footprints are witnessed disjoint at dispatch (witnessed = read live by the
dispatching arc, never derived from row prose)."* So the order above is keyed on **witnessed
footprints** and not on group labels — and the witnessing this plan performed is a *cloud* read of
the tree, which is evidence about `5455c2a` and not about the dispatch moment. **The dispatching arc
re-witnesses; this plan does not discharge G2's witnessing requirement.**

### 5.5 Proposed wave structure

- **Wave 1 (parallel):** A · B · F — no shared file under §5.2's rules; three different subsystems
  (`scripts/` lane machinery · `scripts/fleet_health.py` · `ARCHITECTURE.md`).
- **Wave 2 (parallel):** C · G — parallel **only under C-narrow**; under C-wide they are one lane.
- **Wave 3 (serial, conditional):** D — dispatches only if G-1 *and* the ratification batch land.
- **Wave 4 (last):** E — after every other lane's row edits, so the regeneration is one final pass.

---

## 6. Integration walk order

Run from the **primary checkout, on `main`** (`/lane-integrate` §0 — never from inside a worktree).
One operator **GO** authorizes the whole integration; that GO plus the end-of-batch packet are the
batch's two operator touches.

**Proposed queue, serial, one merge at a time:**

```
A → B → F → C → G → D → E
```

| # | Lane | Why here |
|---|---|---|
| 1 | **A** `[#514]` | P1 and the merge-queue wedge itself. If its leg 3 is discharged by batch 4, the fix must land **before** the rest of the queue or the row cannot close in-batch (batch4-prep Sheet B). |
| 2 | **B** `[#270]` | P1, fully disjoint under §5.2's rules, no doc collisions once `ARCHITECTURE.md` is out of scope. Merges cleanly against a queue that has only touched `scripts/` lane machinery. |
| 3 | **F** ARCHITECTURE | Before any lane that would add a Ch2 row, so the sweep verdicts a file no later lane has moved. |
| 4 | **C** `[#132]` | After F, so its Ch2 gate row (C-wide) or its owed-row note (C-narrow) lands against the swept file. |
| 5 | **G** filing gate + boot site | After C, because both may want `CLAUDE.md`; whichever merges second inherits the `last_reviewed` obligation and **exactly one lane should**. |
| 6 | **D** landing predicate | Latest of the build lanes — it is the most gated and the most likely to be dropped at the GO; a dropped tail lane costs the queue nothing. |
| 7 | **E** conversions | **Last, deliberately.** It regenerates `BACKLOG.md` + `tasks/manifest.json` over up to 42 rows; every earlier lane's close-time row edit is already in the tree, so the regeneration is one pass instead of N conflicts. |

**The five-item refuse-to-finish checklist runs mechanically after the walk** (`/lane-integrate` §3):
lane branches merged-or-explicitly-abandoned · full suite once on the merged result · `git worktree
list` == primary only · manifest/packet archived · `git stash list` empty. **Item 5 is not covered by
1–3** — `refs/stash` lives in the common git dir and outlives `worktree remove`, `prune` and the
branch delete.

**Three integration facts this plan carries forward rather than rediscovering:**

1. **The manifest must land at DISPATCH, not at integration.** Both prior batches landed it late and
   both recorded it. `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md` states the
   practice: *"'Commit the manifest at DISPATCH' stands as the correct practice and was not met."*
   The manifest names `closed_by:` — the packet path — and openness expires when that path appears
   in the committed tree, with no edit anywhere.
2. **A clean auto-merge skips `pre-commit` entirely.** JOURNAL 2026-08-10 (h) and (i) witnessed this
   from both sides on the same file in one session: a conflict-free merge runs only `commit-msg`
   hooks, so a generated file rots silently. **The trailing regen commit is mandatory whether or not
   anything conflicted.**
3. **Teardown is two branches, not one** — the work branch and the `worktree-<name>` provisioning
   branch (`.claude/rules/git-discipline.md`). And `automation/*` is now explicitly protected
   alongside `claude/conformance-*` (I-D 3c-3).

---

## 7. Sizing

Sizes use the repo's own S/M/L vocabulary. Where a lane's own row carries a size, it is quoted and
then either confirmed or contested with a reason.

| Lane | Row size | **Proposed** | Basis |
|---|---|---|---|
| **A** `[#514]` | M | **M** | Two code files + two test files + one command file + PLAYBOOK Ch8. Contained. Leg 3 is empirical and does not add build size — it adds a scheduling decision. |
| **B** `[#270]` | M | **M** | One script + tests + `.gitignore`. batch4-prep: *"aggregation, not new measurement"* — all five funnel counts have a live producer in-repo. `ARCHITECTURE.md` out of scope keeps it M. |
| **C** `[#132]` | M | **M under C-narrow · L under C-wide** | New generator + new document + new gate + `doc-counts` is M. Adding the `CLAUDE.md` §9 and `ARCHITECTURE.md` Ch2 roster rows buys a re-stamp obligation and a collision, which is what tips it. |
| **D** #30 §A | — (no row) | **L** | Shape unchosen (audit.py check vs register field), a new organ, a birth, and an intake ratification upstream. Intake #30's own §A closing line: candidate rows at batch-4 planning are *"ZERO at filing (capacity law)."* |
| **E** conversions | — (no row) | **M as E-min · M/L as E-mid · L as E-full** | 21 Form-E-only substitutions is one decision applied 21 times. All 42 adds per-row judgment on the 21 non-Form-E drafts. Census §6: *"Nine of the ten [cheapest] cost one sentence."* |
| **F** ARCH sweep | — (no row) | **M, with an L tail** | The expensive half is already spent — 16 claims fixed at `cf039756`. The residual is enumerate-and-verdict over an 901-line file. The L tail is the case where doctrinal re-derivation surfaces structural drift rather than claim drift. |
| **G** filing gate + site | — (no row) | **M** | batch4-prep grades the filing gaps *"MECHANICAL — every gap is a regex-plus-lookup change with a directly pinnable test"* and the ARC-7 site *"MECHANICAL, cheaply."* The size is **not** the edits: it is the genuine twelve-section `CLAUDE.md` re-read the freshness gate makes mandatory. |

**Sizing honesty note.** Three of seven lanes have no row and therefore no independently-recorded
size; their sizes above are this lane's estimate and carry no row's authority.

---

## 8. The process-lane cap — the structural problem this plan cannot solve

`protocols/PLAYBOOK.md:1888`, ratified, denominator ratified 2026-08-08:

> **Process-lane cap — from batch 2 onward, at most 1/4 of a batch's lanes target methodology or
> hub-process surfaces.** The remainder carry product/consumer work. A batch that cannot fill its
> non-process lanes **reports the shortfall** in its end-of-batch packet and runs narrower;
> backfilling the gap with additional process lanes defeats the cap … The cap is evaluated against
> **dispatched width**.

**Ex-ante assignment rule, proposed** — responsive to the Fable review's recorded caution that
*"the class assignment is self-declared post-hoc; the packet should state the assignment rule
ex-ante"*:

> A lane is a **PROCESS** lane iff its Done-when *mutates* a methodology or hub-process surface —
> the `protocols/` corpus, `CLAUDE.md`, `ARCHITECTURE.md`, the commands/hooks roster, the batch
> protocol itself, or the backlog's own rows or schema. A lane is a **PRODUCT** lane iff its
> Done-when ships a validator, generator, gate or document whose *output* is consumed by the
> operator or a consumer repo without a methodology surface changing. A **read-only** research or
> audit lane is neither and is not counted — the batch-3 precedent, whose packet records *"no
> process lane was dispatched (the ≤1/4 process-lane cap was left unfilled by design)"*.

**Applying it to this lane set:**

| Lane | Class | Why |
|---|---|---|
| A | **PROCESS** | mutates PLAYBOOK Ch8, `/lane-boot`, and the batch protocol's own machinery |
| B | **PRODUCT** | ships a digest section + a CSV the operator reads; touches no methodology surface once `ARCHITECTURE.md` is out of scope |
| C-narrow | **PRODUCT** | ships a generator + a document + a gate; the roster rows are owed, not taken |
| C-wide | **PROCESS** | takes the `CLAUDE.md` §9 and `ARCHITECTURE.md` Ch2 roster rows |
| D | **PROCESS** | an organ over the rulings register |
| E | **PROCESS** | mutates backlog rows en masse |
| F | **PROCESS** | mutates `ARCHITECTURE.md` |
| G | **PROCESS** | mutates `PLAYBOOK.md` §10 and `CLAUDE.md` |

**At width 7 the cap permits 1 process lane. Under C-narrow this plan proposes 5. The batch as
scoped exceeds the cap by four lanes.** That is not a defect in the plan and not one in the cap —
it is the two meeting for the first time in a *build* batch. Batch 3 never hit it because all five
of its lanes were read-only.

**Three readings, and a recommendation.**

- **(a) The cap binds as written.** Batch 4 dispatches ≤1 process lane plus as many product lanes as
  it can fill, and reports the shortfall rather than backfilling. The only real product pool is the
  consumer-repo cohort — **and batch4-prep's recommendation is that consumer-repo rows must be LOCAL
  worktree lanes, never cloud lanes.** Consequence: batch 4 becomes ~1 process lane + N consumer
  lanes, and five of the six classes the brief names do not run.
- **(b) The cap's denominator does not exist in a Layer-2 hub.** `CLAUDE.md` §5 rule 4 makes this
  repo the layer that never executes, so — as batch4-prep put it — *"a 'feature' here can only ever
  be a new validator, generator, or surface."* A cap whose remainder must *"carry product/consumer
  work"* has no remainder to allocate in the hub. Under this reading the cap governs **fleet**
  batches and needs an amendment naming its scope.
- **(c) Extend the batch-3 precedent.** It does not reach: batch 3's lanes were read-only, batch 4's
  are builds.

**RECOMMENDATION (not a ruling): (b), with an explicit scope amendment.** The cap's own stated
reason — *"methodology work is the class that expands to fill whatever width is available"* — is a
fleet-level concern, and the hub is the single repo where methodology work **is** the product. But
this is squarely an operator decision about a ratified rule, and the plan will not assume it.
**GATED(ruling) G-8. Until it is answered, batch 4's width is undecided, and so is which of these
seven lanes runs at all.**

---

## 9. GATED(ruling) register

Every item below requires a ruling that has not been made. Nothing here is decided by this plan.

| # | Gate | What it blocks | Where the question already lives |
|---|---|---|---|
| **G-1** | **FORK 4 — the births package** is unopened (STANDING_RULINGS §I scope note), **and** #30 §A may amend `[#513]` rather than birth a row | Lane D entirely; Lane G's filing-gate half | §I scope note; `tasks/513-*.md` (*"the landing predicate is the DETECTOR"*); intake #30 §A |
| **G-2** | The lane-name grammar requires `\d+`; two lanes have no row | Lanes F and G cannot be named conformantly (§3) | `validate_branch_naming.py:85`; STANDING_RULINGS F2 |
| **G-3** | Does the `kill-candidates:` refusal check earn a birth? It has none today | Lane G's filing-gate half | batch4-prep Sheet D + its batched question 4 |
| **G-4** | `[#514]` leg 3 — which batch discharges *"one clean batch runs under it"*? | Whether `[#514]` can close in-batch | batch4-prep Sheet B + batched question 3 |
| **G-5** | Does `[#270]` adopt a closing-commit token convention (`^load-gauge-metric:`)? | Lane B's leg 4 | batch4-prep Skeleton A |
| **G-6** | Census Q2 — where does a *"recorded with a reason"* record live? | 21 of Lane E's 42 drafts; 30 open rows by substitution | census §4 Form E + §8 Q2 |
| **G-7** | What does *"ARCHITECTURE soft observations"* denote? Zero in-repo hits | Lane F's scope (§4.6) | reconstructed from `cf039756` STEP 3's honest limit + I-D2 |
| **G-8** | Does the ≤1/4 process-lane cap bind a hub build batch? | **Batch 4's width, and which lanes run at all** | `PLAYBOOK.md:1888`; ADR-110 amendment 2026-08-08 |
| **G-9** | Is *"the research-corpus distillate"* the ARC-2 §6 triage, or the output of the not-yet-run `ingest-research-corpus` lane? | Whether §1's reconstruction stands | JOURNAL `Next:` lines; consolidation report §5.2 row 3 |
| **G-10** | Intake #30's `status:` flip lands *"ONLY in the single ratification batch at the GO"* | Lane D's precondition | STANDING_RULINGS I-F2 |

**Two further items are ruled but their execution is unassigned**, and a batch-4 lane is the natural
carrier for each — recorded so they are not lost, and **not** claimed as lanes here: the `[#241]`
cardinality-free re-phrase and the `[#390]` Effort-cell fix, both **ruled** (I-D 3a-3 and 3a-1) with
their row text **owed to batch4-prep's paste-blocks 1 and 2**, which are drafted and unapplied.
Both are single-row edits and both fit inside Lane E's footprint.

---

## 10. Batched questions

None blocked this lane. Each is a GO-day input, ordered by how much of the plan it moves.

1. **G-8 — does the process-lane cap bind here?** It decides the batch's width and which lanes exist.
   Everything else in this plan is downstream of it.
2. **G-1 — is FORK 4 opened, and does #30 §A amend `[#513]` instead of birthing?** It decides Lane D
   and half of Lane G, and the amend route makes Lane D nameable today.
3. **G-6 — the Form E register home.** One decision converts 30 open rows and sets Lane E's size
   from L to M.
4. **G-2 — how is an id-less lane named?** Two grammar-legal forms exist and both are inventions;
   F2 says the name derives from an enum, so this is a ruling, not a choice.
5. **Which lane owns `ARCHITECTURE.md`, and which owns `CLAUDE.md`?** This plan proposes F and G
   respectively. Either answer is workable; **no answer is not** — two lanes on one freshness-gated
   file wedges a pre-commit gate.
6. **Has the `mutation-pilot` job run since `27c37ae3`?** Still unanswerable from a cloud seat, still
   the fact that decides whether `[#502]` is a lane or a ten-minute close. Carried unchanged from
   batch4-prep.
7. **Is `[#383]` re-scoped before batch 4?** It is the literal `[#490]`-class successor and it is
   DEFECTIVE as written. If it is re-scoped at the GO it becomes a candidate substitute for Lane C.

---

## Packet

**Lanes proposed:** 7 — A `[#514]` · B `[#270]` · C `[#132]` (feature) · D intake #30 §A · E the
Done-when conversion campaign · F the ARCHITECTURE sweep · G the filing gate + ARC-7 boot site.
Six are the brief's classes; **G is added from batch4-prep's own §3.4 decomposition and is the one
droppable addition.**

**Contract skeletons:** 7 — each with purpose, mechanically-phrased candidate Done-when, steps, and
V-2 decision-budget stubs. **None is frozen.**

**Order:** four waves (A·B·F ∥ C·G ∥ D ∥ E); integration walk **A → B → F → C → G → D → E**, E last
so the `tasks/` regeneration is one pass.

**Sizing:** A M · B M · C M/L · D L · E M→L by scope · F M+ · G M. Three lanes have no row and
therefore no recorded size; those three sizes are this lane's estimate.

**Four findings the plan produced rather than carried:**

0. **The cloud clone arrived shallow, and the error it would have caused was measured.** 293
   commits, earliest 2026-08-06; two cited SHAs absent while six resolved. One figure taken before
   and after `--unshallow`: **38/38 (100.0%)** vs **332/351 (94.6%)** — a ~9× denominator error that
   would have read as a *stronger* version of the finding it was measuring. A fresh instance of
   intake #30 §B's condition, and the full-history figure independently reproduces batch4-prep's
   331/350 to one commit.

1. **`[#514]`'s defect is live inside batch 4's own lane set.** An id-less lane branch
   (`worktree-lane-f-architecture-soft-sweep`) **matches** the loose constant that grants the ADR-110
   exemption while the strict validator classifies it `unknown` — reproduced here, both regexes
   evaluated on one string. It is evidence for the row and a sequencing hazard for the batch.
2. **The silent-rule ratchet has headroom 1** (live 440, baseline 441, corpus 57 files) and **four
   of seven lanes write inside its corpus** — a shared budget no file-disjointness matrix can see.
   The register's own editing note says 441 = 441 and is one window stale; recorded, not repaired.
3. **The ≤1/4 process-lane cap and a hub *build* batch meet here for the first time.** Batch 3 never
   hit it because all five of its lanes were read-only. Under any honest ex-ante assignment rule,
   five of this plan's lanes are process lanes and the cap permits one.

**GATED(ruling):** 10 items in §9. Two ruled-but-unassigned executions (`[#241]`, `[#390]`) recorded
as Lane-E-shaped, not claimed.

**Posture at STOP:** read-only honoured. Zero births, zero edits to any row / intake / ADR /
`BACKLOG.md`. No freshness-class verdict issued. No `JOURNAL.md` entry — a lane never journals; the
integrator does. No merge, no `SKIP=`, no `--no-verify`. This report is the lane's only write.
