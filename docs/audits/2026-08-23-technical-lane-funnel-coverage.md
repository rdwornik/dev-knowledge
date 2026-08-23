# L2 — Audit funnel coverage checker (M3)

**Lane:** L2 · `funnel-coverage` · contract `LANE-L2-funnel-coverage.md` (frozen)
**Branch:** `worktree-funnel-coverage`
**Merge base:** `aeec0fd1`
**Mode:** plan → execute. Effort xhigh.

> **Intent, restated so the artifact reads without the contract.** Make *"no audit is wasted"*
> verifiable instead of promised: every artifact in `docs/audits/` should carry a disposition from
> a closed set, and the absence of one should be a machine-detected signal rather than something a
> human notices later. This lane measures the corpus, builds the detector, and arms it as a **WARN
> against a zero-baseline ratchet** per the architect's ruling. The flip to RED is a later,
> separate act with its own ruling and is not taken here.

---

## 1. Library-first and prior-art verdict — Step 1

All four legs were run in the contract's order, before any design. Each verdict is recorded with
the evidence that produced it.

### Leg 1 — prior art in this repo

**VERDICT, in two halves, because the contract's question has two answers and reporting only the
first would be the more convenient lie.**

> **(a) At the INSTRUMENT level: prior art does not win.** `review_artifact_coverage` asks a
> different question along every axis that matters, with a **132-artifact measured divergence**.
> A second leg is justified.
>
> **(b) At the VOCABULARY and DATA level: prior art wins outright, and this lane consumes it
> rather than replacing it.** An architect standing ruling of 2026-08-17 already defines the
> artifact-level disposition set, and a populated ledger already applies it to 80 artifacts. This
> lane builds the **reader** for a surface that already exists. **Nothing is invented.**

#### (a) `review_artifact_coverage` — the same corpus, a different edge

The organ resolves; premise C of the phase-0 packet is confirmed live rather than taken on trust:

```
scripts/audit.py:3184   def check_review_artifact_coverage(repo_path: Path) -> list[Finding]:
scripts/audit.py:3443       check_review_artifact_coverage,   # [#480] P3 -- ADVISORY (WARN-tier)
```

Read end to end, it answers a different question:

| axis | `review_artifact_coverage` | this lane |
|---|---|---|
| unit of coverage | a **merge** on `main`'s first-parent spine | an **artifact** in `docs/audits/` |
| direction of the edge | merge → *does a review artifact exist for it?* | artifact → *did it reach an outcome?* |
| corpus walked | spine entries since a UTC cutoff, code-impact only | the `docs/audits/` directory |
| predicate | `^# Codex Review` + a `**Branch:**`/`**HEAD:**` field + a 4-digit `**Tally:**` | a ledger row with a ruled term and a resolvable locator |
| vocabulary | severity digits (C/H/M/L) | ACTIONED / FILED / REJECTED / SUPERSEDED |
| what a green means | *a review happened and was recorded* | *a finding was routed, not dropped* |

The only overlap is a shared **input** — both read `docs/audits/*.md` — which is not a shared
question. **Measured on the live corpus of 693 artifacts** (`explore/divergence`, reproduced in §2):

```
review_artifact_coverage would ADMIT as review artifacts      148
  ...of which carry a parseable **Tally:** line                46
admitted-as-review AND funnel-UNCOVERED                       132
admitted AND tallied AND funnel-UNCOVERED                      32
funnel-COVERED but not a review artifact at all                64
overlap — covered under BOTH notions                           16
```

**32 artifacts are, to `review_artifact_coverage`, perfectly covered — linked to their merge and
carrying a parseable tally — and are exactly the waste this lane exists to detect.** An overlap of
16 out of 148/80 is not two spellings of one check. The divergence is measured, so the second
instrument is justified on the contract's own terms rather than on preference.

**What IS adopted from it — the shape, which is the part worth more than the code.** The contract's
principle ("a known-defective instrument that is the right shape is worth more than a correct
instrument of the wrong shape") applies to the shape even where the question differs:

1. **A predicate measured against the corpus before it is trusted, with the false-admit count
   stated.** Its `_REVIEW_TITLE_RE` was ruled only after measuring 0 admits among 13
   `**Branch:**`-bearing non-reviews. §2 does the same and reports the number. *(Incidental
   re-measurement: that 13 is now **18**. The corpus grew; the discrimination still holds.)*
2. **WARN-tier by ruling, with no code path to a hard verdict**, asserted structurally by a test —
   because an observational check only proves such a path was not *reached*, which is precisely
   what a latent one looks like.
3. **An honest-limits paragraph naming what a green does NOT mean.** Carried into §3 and §5.
4. **Never wedge the gate on its own input** — the outer handler degrades to a WARN.
5. **Batched reads, never per-entry.** Its docstring records the per-entry form costing 236s on a
   1317-entry spine *inside a pre-commit gate*. This detector touches git not at all (§3).

**And one lesson adopted by name.** `[#560]` (P2, open) exists because `review_artifact_coverage`
reads only the **first** `Branch`/`HEAD` triple per file, so a real review sitting in a second
triple is invisible to it. This scanner walks **every table in a file and every row in a table**,
and a fixture whose *second* table carries the only disposition pins it (§3). **`[#560]`'s own
defect is NOT fixed here** — it belongs to that open row and lives in `scripts/audit.py`, the
collision file this lane is barred from editing. Not fixed, not partly fixed, not improved in
passing.

*Locator drift, reported not swept (CLAUDE.md §4 M1):* `[#560]`'s `refs` cite
`scripts/audit.py:3117-3320`; the function now begins at **3184**. The range still contains it, so
the locator resolves, but its start has drifted — the phase-0 packet flagged the same thing. Worth
re-pointing when the row is next touched. Not this lane's to edit.

#### (b) The ruling and the ledger — prior art that wins

**This is the finding that reshaped the build, and it was nearly missed.** The first pass of Leg 1
searched for a *code* organ, found `review_artifact_coverage`, and would have concluded "build
new". Searching the corpus for the disposition *vocabulary* instead surfaced an
**architect standing ruling that already closes the set at the artifact level**
(`docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md:22-27`, committed `875509bd`;
re-quoted at the head of `docs/audits/2026-08-17-technical-audit-disposition-ledger.md`):

> *Audit-to-row conversion authority, 2026-08-17.* Every audit artifact carries exactly one
> disposition: **ACTIONED** (conclusion already live — cite the commit), **FILED** (a row owns it —
> cite the id), **REJECTED** (a ruling declined it — cite it), **SUPERSEDED** (a later artifact
> replaced it — cite it). **An undisposed audit is a defect, not a document.**

and a **populated ledger applying it to 80 artifacts**, with the shape specified in the same
contract at `:87-92` — `| file | final metric line | disposition | evidence locator |`.

So the mandate's core sentence is **already ruled doctrine**, and the gap is exactly and only that
nothing reads the ledger. ADR-111 states the same gap in its own Consequences, verbatim:

> **Unenforced, and this ADR does not pretend otherwise.** No organ checks that an audit's findings
> are triaged, and none is built here.

**Consequence for the build, taken rather than noted.** The detector does not define a schema, ask
for frontmatter, or introduce a term. It parses **the ledger table already on disk**, in **the
vocabulary already ruled**, and reports what is missing. The validation of that decision is that
the parser independently reproduces the ledger's own self-reported packet line — see §2.

**Registration gap, reported (not fixed here).** This ruling is **locatable but unregistered**:
`ACTIONED` appears in 8 audit artifacts and 5 handoff files and **0 times in
`protocols/STANDING_RULINGS.md`**. Under the register discipline (K-1) a standing ruling that
governs a closed vocabulary belongs in the register; this one is carried only by a lane contract
and a ledger. It is **ruled, not unruled** — the distinction matters and the wording here is
deliberate — but a reader who checks the register first will not find it. **Filing this is
outside this lane's scope**; it is reported in §7 as a finding for the funnel.

### Leg 2 — the disposition vocabulary already exists

**VERDICT: it exists, it is ruled, and it is ARTIFACT-level. The check enforces that set
unchanged. The mandate's four terms diverge from it, and the divergence is reported for the
architect rather than resolved here.**

Three vocabularies are live in this repo, and **the first thing to get right is that two of them
are about a different unit**:

| source | unit | terms |
|---|---|---|
| **ADR-111 §1** (Accepted 2026-08-10) | **finding** | OWNED · DISCHARGED · CANDIDATE · REJECTED |
| **PLAYBOOK Ch8 D4** (the wave close) | **finding** | MECHANICAL · ADR · INTAKE · REJECT · COVERED — *"ADR-111 §1's four outcomes, plus the executed case"* |
| **Architect ruling 2026-08-17** | **artifact** | ACTIONED · FILED · REJECTED · SUPERSEDED (+ PENDING for the undecidable) |

**This lane's unit is the artifact**, because the closure contract's item 1 counts *files* in
`docs/audits/`. So the governing vocabulary is the third, and ADR-111 / PLAYBOOK Ch8 are cited but
**not enforced by this check** — they govern the findings *inside* an artifact, which is a
different measurement and a different lane. Enforcing a finding-level set at the artifact level
would have been the fifth vocabulary the contract forbids, arrived at by accident.

Reconciled against the mandate's four terms:

| mandate term | ruled artifact-level equivalent | status |
|---|---|---|
| rejected-with-reason | **REJECTED** — *"a ruling declined it — cite it"* | **exact match** |
| →backlog row | **FILED** — *"a row owns it — cite the id"* | **exact match** |
| →intake | *no equivalent* | **DIVERGENT** |
| →ADR | *no equivalent* | **DIVERGENT** |
| — | **ACTIONED** — *"conclusion already live — cite the commit"* | absent from the mandate |
| — | **SUPERSEDED** — *"a later artifact replaced it — cite it"* | absent from the mandate |

**The divergence, stated precisely, because it points both ways.**

1. **The mandate is missing the two terms that carry most of the live corpus.** ACTIONED and
   SUPERSEDED account for **51 of the 78** dispositioned artifacts (§2). A check built on the
   mandate's four terms would have called 49 correctly-ACTIONED artifacts uncovered.
2. **The mandate adds two routes the artifact-level ruling does not name** — →intake and →ADR.
   Both are real and lawful at the *finding* level (ADR-111 §1(c) CANDIDATE, split by ADR-98 §3's
   fork test), so this is a **level confusion rather than a contradiction**: an artifact whose
   findings went to intake is, at the artifact level, either FILED (the intake's carrier row owns
   it) or ACTIONED. **The architect reconciles; this lane does not.**
3. **One term needs its lawfulness stated, not assumed.** ADR-111 §2 says *"A finding may not
   become a backlog row without triage… A finding may not be filed directly as a row."* FILED does
   not violate that: it records that **a row owns the artifact**, which is ADR-111 §1(a) OWNED, and
   is silent on how the row was born. The check counts FILED as coverage and **does not verify the
   row's provenance**. Stated as an honest limit in §3 rather than smoothed over.

**No new vocabulary is introduced. The closed set the detector enforces is the ruled four, plus
PENDING handled as its own third state — neither coverage nor absence** (the ruling's own
*"a wrong ACTIONED is worse than an honest PENDING"*).

### Leg 3 — stdlib before dependency

**VERDICT: stdlib only. Not even `pyyaml` in the detector itself. No new dependency, nothing to
price.**

The problem decomposes into directory walking (`pathlib`), table parsing (`re` + a hand-written
cell splitter), and set arithmetic (`set`). The baseline file is YAML and is read with
`yaml.safe_load`, already a declared baseline dependency used by `audit.py::_load_dispositions` —
and that read lives in the `audit.py` facade wrapper, not in the detector, so
`scripts/funnel_coverage.py` imports **nothing outside the standard library**.

Two candidates were considered and declined for stated reasons rather than by omission:

- **`markdown-it-py`** (in the baseline) for a structural table parse. **Declined.** The corpus's
  tables are not uniform enough for a structural parse to beat a line-oriented one, the n5 sweep
  already ruled `markdown_it` adoption is a per-site call rather than a sweep, and this code is
  reachable from a pre-commit gate where an added import is a cost paid on every commit.
- **A hand-rolled `str.split("|")`.** **Declined, and this one was not theoretical.** The live
  ledger quotes each artifact's final metric line verbatim, and those quotes contain `\|`. A naive
  split shredded two ACTIONED rows into the tokens `SHALL\` and `\` during the measurement pass —
  a **silent two-row undercount that looked exactly like a clean parse**. The cell splitter honours
  the escape, and §2's reconciliation is what caught it.

### Leg 4 — external tooling

**VERDICT: settled by five prior rulings at their locators. Not re-run, and no new candidate is
proposed.**

- **`python-frontmatter` — REJECTED, "OUT, full stop"** (0/20 byte-identical round-trips;
  `sort_keys=True` reorders every key, not configurable) —
  `docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md:38,96`.
- **Vale / markdownlint plugins, Sphinx-include class, doctest class — REJECTED** at the locators
  cited in `docs/audits/2026-08-09-technical-night-n5-library-first-sweep.md:59`.
- **`ruamel.yaml` — no swap** (templates are authored fresh, not round-tripped) — same file,
  `:39-40,99-114`.
- **SARIF — `NO-SARIF`**; *"the format is not the constraint"* —
  `docs/audits/2026-08-08-technical-library-research.md`.
- **`jsonschema` — KEEP, justified**: *"no uniform corpus schema exists to bind to"* — n5 sweep
  row 13.

**One prior finding is decisive for the design and is therefore quoted rather than summarised**
(n5 sweep, item 5):

> **`docs/audits/` frontmatter (informational, no action requested).** 57 of 442 audit files carry
> frontmatter and all 57 are batch manifests. If audits are ever meant to be machine-queryable,
> that is a doctrine decision with a **385-file backfill** behind it.

Re-measured live on today's corpus: **70 of 693** artifacts begin with a `---` frontmatter fence
(the figure is 70, not the sweep's 57 — the corpus grew from 442 to 693; the *shape* of the finding
is unchanged and they remain batch manifests). Separately, **537 files contain a `---` line
somewhere**, which is the horizontal-rule glyph and not frontmatter — a trap for exactly the naive
grep that would have been used to "confirm" a frontmatter surface exists.

**This forecloses the obvious design.** A check requiring an in-file `disposition:` frontmatter key
would demand precisely the ~620-file backfill the sweep flagged as an unruled doctrine decision —
and would demand it against artifacts **§5 rule 3 makes immutable**. A gate whose only discharge
path is a rule violation is not a gate. The detector therefore reads a **reader-side** surface,
which is the same conclusion `[#560]` reached independently for its own repair: *"Artifacts are
IMMUTABLE (§5 rule 3), so the repair is reader-side."*

### Leg summary

| leg | verdict | consequence for the build |
|---|---|---|
| 1a · code prior art | **not the same question** — 132-artifact measured divergence | a second leg is justified |
| 1b · ruling + ledger | **prior art WINS** — ruled vocabulary, populated ledger, no reader | build the *reader*, invent nothing |
| 2 · vocabulary | **ruled, artifact-level**; the mandate diverges on 2 of 4 terms | enforce the ruled four + PENDING; report the divergence |
| 3 · stdlib | **stdlib only** in the detector | no new dependency |
| 4 · external | **settled, five prior rulings**; frontmatter foreclosed | reader-side surface, no backfill demanded |

**The library-first finding, recorded so it is never re-derived** (closure contract item 5):

> *The vocabulary, the ledger shape and the ledger data all already existed and were already ruled
> — on 2026-08-17, at the artifact level, with 80 artifacts dispositioned. What did not exist was
> anything that reads them. `review_artifact_coverage` is the right shape aimed at a different
> edge (132-artifact divergence, 16-artifact overlap). Every frontmatter approach is foreclosed by
> a ruled rejection plus §5 rule 3's immutability. Every external linter was measured and lost.
> **The correct build was therefore the smallest one: a stdlib reader for a surface that already
> existed** — and the reason it was nearly missed is that the first prior-art sweep looked for a
> script and not for a ruling.*

### What Step 1 changes about the remaining steps

Prior art wins at (b) and not at (a), so steps 3–4 remain a build — but a **much smaller one than
the contract anticipated**, and two contract branches close without being taken:

- *"If you fix `review_artifact_coverage`'s first-triple-only defect, prove the fix with a case the
  old code missed"* — **not taken.** The defect is real, is `[#560]`'s, and lives in the collision
  file. Its *lesson* is adopted (every table, every row) and pinned by a test.
- *"If prior art wins, the rest of this lane is a fix-and-extend"* — **half true, and reported as
  half.** No code is extended; the ruled vocabulary and the on-disk ledger are consumed unchanged.
  The build is the reader they never got.
