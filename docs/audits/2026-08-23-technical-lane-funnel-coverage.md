# L2 — Audit funnel coverage checker (M3)

**Lane:** L2 · `funnel-coverage` · contract `LANE-L2-funnel-coverage.md` (frozen)
**Branch:** `worktree-funnel-coverage`
**Merge base:** `aeec0fd1`
**Mode:** plan → execute. Effort xhigh.
**Adversarial review:** `gpt-5.6-sol` (1 pass, 8 routes, ungraded — §5.1) + `terra` (5 rounds, graded)
**Tally:** 0/17/10/0 (C/H/M/L) — the terra loop's graded findings across all five rounds; sol's eight routes are ungraded by construction and tabulated in §5.1.

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

---

## 2. The measured baseline — Step 2

**Nothing here is dispositioned.** This is measurement, and the contract's `What NOT to do` list
is honoured exactly: the 613 uncovered artifacts are counted and enumerated, not routed.

### 2.1 Method, and how it was validated

`scripts/funnel_coverage.py` walks `docs/audits/*.md`, parses **every** ledger table in **every**
file, and classifies the corpus. A ledger table is one whose header carries a file-ish column, a
`disposition` column **and** an `evidence locator` column — the exact columns the 2026-08-17
lane-a contract specified at `:87-92`. Reproduce with:

```
python scripts/funnel_coverage.py --report
python scripts/funnel_coverage.py --list-uncovered
```

**The validation that makes the number trustworthy is a reconciliation, not an assertion.** The
2026-08-17 ledger states its own result in its §0 packet line:

```
audits 80 · ACTIONED 49 · FILED 25 · REJECTED 2 · SUPERSEDED 2 · PENDING 2
```

The parser was never given those figures. It independently produced **ACTIONED 49 · FILED 25 ·
REJECTED 2 · SUPERSEDED 2 · PENDING 2 = 80**. An exact five-way match against a number the ledger
computed by a different method, six days earlier, is what separates *"the check ran"* from
*"the check read what it claims to read"* — which is the contract's named failure mode.

**It did not match on the first run, and the way it failed is worth recording.** The first pass
reported ACTIONED **47** and two "malformed" rows carrying the terms `SHALL\` and `\`. The ledger's
`final metric line` column quotes each artifact verbatim, and those quotes contain escaped pipes
(`\|`); a naive `split("|")` shredded two real rows. **The undercount looked exactly like a clean
parse** — 0 errors, a plausible total — and only the reconciliation against the ledger's own
self-report caught it. The cell splitter now honours the escape, and a test pins it.

### 2.2 The baseline

```
detector      funnel-coverage/v1
corpus N      693   (docs/audits/*.md, excluding the generated README.md)
ledgers        1    2026-08-17-technical-audit-disposition-ledger.md
dispositioned X = 78    ACTIONED 49 · FILED 25 · REJECTED 2 · SUPERSEDED 2
pending        2    recorded open question, neither coverage nor absence
uncovered  N-X = 613
malformed      0
dangling       0    (no ledger row names an artifact absent from disk)
```

`78 + 2 + 613 = 693`. **Coverage is 11.3%**, or 11.5% counting PENDING as looked-at.

`README.md` is excluded because it is generated and cites every artifact by construction — the
same exclusion the 2026-08-17 ledger applied, on its own stated reasoning, rather than a fresh
judgement call here.

**The uncovered set is enumerated by name in `ecosystem/audit-funnel-baseline.json`** (613
entries, `artifacts:`). It is not restated in prose here: CLAUDE.md §4 forbids restating a roster
instead of citing the surface that computes it, and that file *is* the surface — it is what the
check reads.

### 2.3 What the 613 are, because a bare number invites the wrong conclusion

| dimension | shape |
|---|---|
| **by month** | 2026-03 **1/1** · 2026-04 **17/17** · 2026-05 **65/65** · 2026-06 **92/92** · 2026-07 **170/170** · 2026-08 **268/348** |
| **by class** | technical 259 · codex 140 · *(no ADR-101 class)* 137 · conformance-nightly-digest 19 · ecosystem-audit 17 · verification 14 · census 11 · fresh-eyes 8 · changelog-review 6 · qa 2 |

**Every artifact dated before 2026-08 is uncovered — 345 of them, without exception.** That is not
a defect the ledger introduced; it is the ledger's own declared scope. Its §1 says so plainly: it
ledgered *"the newest 80"* against a measured candidate set of 129, and named the remaining **49
as a follow-on list rather than a row** — *"a mechanical second pass, not an arc."* This check
counts those 49 as uncovered, correctly: a name in a prose list is not a disposition with a
locator, and the whole point of the instrument is that the distinction is now machine-visible
instead of resting on a reader remembering §4 exists.

**The 137 `(no ADR-101 class)` files are a second, independent finding.** They predate the closed
11-class enum and are grandfathered by `validate_hermetization`'s prospective-only Rule B, so
their filenames carry no class token at all. Reported, not acted on — renaming them would edit
immutable artifacts.

### 2.4 The number that justifies arming now rather than later

The 2026-08-17 ledger measured **567** tracked artifacts in `docs/audits/`. Six days later the
corpus is **693**.

```
2026-08-17   567 tracked   80 ledgered  (14.1%)
2026-08-23   693 tracked   78 covered   (11.3%)
             +126 artifacts in 6 days   ~21/day, and every one of them undispositioned
```

**Coverage fell while the ledger's work stood still**, because the corpus outran it. That is the
argument for a ratchet in one line: a one-off ledger pass is a snapshot that decays at ~21
artifacts per day, and nothing noticed. A ratchet does not fix the 613 — it makes 614 visible.

### 2.5 Two things the measurement surfaced that are NOT this lane's to fix

1. **The 2 PENDING artifacts are honest, and both are blocked on the operator, not on work.**
   `2026-08-14-qa-night2-quality.md` (*"do the seven LOW findings get an owner, or are they
   recorded accepted-with-reason?"*) and `2026-08-16-census-nb6-archive-sweep.md` (*"does the
   operator GO the 3 intake status transitions…"*). Both carry the exact question the ruling asks
   for. They are reported as PENDING and are deliberately **not** counted as coverage.
2. **The register orphan shape the contract predicted is live in this data too.** The contract
   flagged it in `ecosystem/disposition-register.yaml`'s `[stale]` entries; the same shape exists
   here as a **FILED row whose owning id later closes** — P-2 (a closed row cannot carry an
   obligation) means the disposition orphans while the ledger row still reads FILED. **Detected
   cheaply? No — and that is a finding, not a silence.** Resolving it needs a row-liveness join
   against `tasks/*.md` frontmatter, which is a second corpus and a second failure mode inside a
   pre-commit-reachable gate. §7 reports it with its cost; the contract's *"do not extend scope to
   fix it in this lane"* is honoured.

### 2.6 A measured false positive in a sibling organ, found by arming this one

The baseline was first written as `ecosystem/audit-funnel-baseline.yaml` — the obvious home,
alongside `ecosystem/silent-rule-baseline.yaml`. **The commit was refused by `audit-health`:**

```
[!!] silent_rule_ratchet: silent-rule pool GREW: live 444 > baseline 441 (+3) under
     detector silent-rule-v4 across 60 file(s) — drain the additions or record an
     operator ruling; the baseline does not rise on a commit
```

`silent_rule_detector`'s governed corpus includes `ecosystem/*.yaml`, and it counts occurrences
of `\b(?:must|shall|never)\b`. Of the +3: **two were my own header prose** (removable, and
removed — that reasoning belongs in the module docstring, not in a machine-read data file), and
**one is a filename**:

```
ecosystem/audit-funnel-baseline.yaml:240   - 2026-07-06-arc5-must-verification.md
```

**An audit whose slug happens to contain the word `must` scores as rule accretion.** That is not
a defect this lane introduced and not one it can drain — it is `silent_rule_detector`'s own
stated residual limit reaching a new class: *"occurrences in examples, quotations and
already-enforced rules still count… This is a proxy."* A **data enumeration** is the third case,
and it is the one that bites hardest, because a coverage baseline is a list of filenames by
construction. Enumerate the corpus and you move a rule-accretion metric.

**The lawful fix is the exclusion class the detector already applies twice** — to
`ecosystem/silent-rule-baseline.yaml` (*"would otherwise count its own provenance prose, making
the metric self-referential"* — that file carries **6** such tokens today and is exempt for
exactly this reason) and to `ecosystem/parity-surfaces.yaml` (*"enum values… enforced by
construction… would make the ratchet fire when someone ADDS ENFORCEMENT — precisely backwards"*).
A ratchet's baseline is data, not doctrine, and this is a second ratchet's baseline in the same
directory.

**That fix was NOT taken, and the reason is a boundary rather than a preference.**
`silent_rule_detector`'s docstring requires *"Bump this string whenever ANY clause of the
detector contract above changes"*; a fourth `EXCLUDED_RELPATHS` member is such a clause. The bump
forces a re-measure and re-stamp of **another ratchet's curated baseline** — and
`_ratchet_findings` turns a detector migration into a WARN demanding explicit operator review,
by design. That is a curated-baseline touch and an operator act, taken while five sibling lanes
are in flight. **A lane does not re-stamp another organ's baseline to make its own commit pass.**

**What was done instead, and it is the reversible half of the fork.** The baseline is
`ecosystem/audit-funnel-baseline.json`. JSON is outside `silent_rule_detector`'s ruled
denominator (`ecosystem/*.yaml`), so no exclusion is needed and no contract is touched — and it
is independently the honest shape for this file: machine-generated, machine-read, carrying no
doctrine and needing no comments. It also keeps the detector **stdlib end-to-end**, since the
facade no longer needs `yaml.safe_load`.

**Stated plainly, because a reviewer should not have to ask:** the format choice is *partly* to
stay outside another organ's measurement corpus. That is recorded here rather than presented as
a neutral preference. It is reversible in one constant and one regeneration, which is why it was
decided rather than escalated. **§7 carries it as the architect's call**, with the finding —
*a coverage baseline cannot live in `ecosystem/*.yaml` without either an exclusion or a
false-positive* — as the durable part.

---

## 3. The instrument — Step 3

`scripts/funnel_coverage.py`. Stdlib only, read-only, no git. Two layers, deliberately split:
a **detector** (`measure`) that classifies the corpus, and a **pure ratchet** (`ratchet_findings`)
that turns a measurement plus a baseline into `(status, evidence)` pairs. The split is what lets
the four ratchet contract cases be pinned without standing up a repo — the same reason
`_ratchet_findings` exists as a separate testable core in `[#436]`.

### 3.1 What it admits, and what it refuses

A file is **covered** when some ledger row names it with a term from the ruled closed set **and**
a non-empty evidence locator. A **ledger** is a markdown table whose header carries a file-ish
column, a `disposition` column **and** an `evidence locator` column — the columns the 2026-08-17
lane-a contract specified at `:87-92`.

| the check counts as coverage | the check refuses, and a test pins each refusal |
|---|---|
| `ACTIONED` / `FILED` / `REJECTED` / `SUPERSEDED` with a locator | a term outside the ruled set (`WILL FIX`) → **malformed**, not coverage |
| a ledger row in **any** artifact, including one dispositioning itself | a ruled term with an **empty** locator → **malformed**, not coverage |
| a row in the **second** table of a file, or the **80th** row of a table | a table lacking the `evidence locator` column → **not a ledger at all** |
| — | `PENDING` → its own third state: neither coverage nor absence |
| — | a row naming an artifact not on disk → **dangling**, reported, never coverage |
| — | `docs/audits/README.md` → outside the corpus (generated, cites everything) |

**Requiring the locator column is a measured decision, not a taste.**
`docs/audits/2026-05-24-dev-knowledge-self-audit.md` carries a table literally headed
**"## Disposition ledger"** with `File` and `Disposition` columns. It predates the ruling, cites
nothing, and grades in `WILL FIX`. **The predicate admits 0 of its 16 rows.** That is the
false-admit number, produced the same way `review_artifact_coverage` produced its
0-of-13 — by measuring the nearest miss on the real corpus rather than reasoning about it. A
predicate that admitted that table would have reported 16 artifacts as dispositioned in a
vocabulary nobody ruled.

### 3.2 Three defects the tests were written to catch, all of which were real

1. **Escaped pipes.** Covered in §2.1. Found by reconciliation, not by a test — the test came
   after, which is the honest order and is recorded as such.
2. **First-table-only reading — the `[#560]` class, avoided by adopting its lesson rather than
   inheriting its bug.** `test_scan_reads_every_table_not_just_the_first` builds a document whose
   *first* table is unrelated and whose *second* carries the only disposition. A
   `.search`-shaped scanner returns nothing and the artifact reads as waste. This is precisely
   what `[#560]` records: *"lane E was reviewed but sits in the SECOND triple of a two-branch
   artifact and `.search` takes the first."*
3. **A bundled Finding.** `[#560]` lists *"bundled Finding"* as a live structural rider in
   `review_artifact_coverage`. It matters because the `#147` register suppresses an **entire**
   Finding on a substring match, so one bundled line lets a single dispositioned artifact wave
   through every other regression beside it. This leg emits **one Finding per regressed
   artifact**, and `test_ratchet_emits_one_finding_per_regression_never_a_bundle` asserts each
   Finding names exactly one.

### 3.3 The ratchet is identity-based, and that is the design's load-bearing choice

`[#436]`'s ratchet compares integers, because a normative-keyword occurrence count has no
attribution to compare. Here the unit is a filename, so a stronger form is available for free:

```
regressions = live_uncovered - baseline_set      # WARN, one Finding each, named
drained     = baseline_set   - live_uncovered    # pass, "ratchet-down available"
stale       = baseline_set   - corpus            # WARN: baseline names an artifact that is gone
```

**`test_ratchet_REFUSES_THE_SWAP_that_a_count_would_wave_through` is the test that earns the
design.** Drain one arm-time artifact, add one new undispositioned one: the total is unchanged,
so an integer ratchet (`live <= baseline`) passes clean while the corpus silently trades old debt
for new. The identity form still surfaces it, by name. Given a corpus growing ~21 artifacts/day,
that swap is not a theoretical evasion — it is the default outcome of ordinary work.

### 3.4 WARN-tier, proven at the source

The architect's ruling is *"do not arm RED. WARN with a ratchet."*
`test_ratchet_is_structurally_incapable_of_failing` reads `inspect.getsource(ratchet_findings)`
and asserts no `"fail"` literal appears, exactly as
`tests/test_review_artifact_coverage.py::test_leg_is_structurally_incapable_of_failing` does —
because an observational test only proves a fail path was not **reached**, which is what a latent
one looks like. `test_no_fixture_produces_a_non_advisory_status` is its observational companion.

### 3.5 Honest limits — what a green here does NOT mean

Stated in the module docstring and repeated here, because the contract's failure mode is a check
that passes while testing nothing:

- **It verifies a disposition was RECORDED, not that it is TRUE.** A ledger row reading
  `ACTIONED | deadbeef` passes without `deadbeef` being a real commit, and nothing here resolves
  the locator. This converts an unfalsifiable claim into a checkable one; it does not make it a
  true one — the same limit `review_artifact_coverage` states about a fabricated tally.
- **It does not verify the row's provenance.** `FILED` records that a row owns the artifact; it
  is silent on whether that row was born through intake as ADR-111 §2 requires. Checking that is
  a different edge with a different corpus.
- **It does not detect the P-2 orphan.** When a `FILED` row's owning id later closes, the
  disposition orphans while the ledger still reads FILED. Detecting it needs a liveness join
  against `tasks/*.md` frontmatter — a second corpus inside a pre-commit-reachable gate. Reported
  in §7 with its cost; the contract's *"do not extend scope to fix it in this lane"* is honoured.
- **It reads the working tree, not `git ls-files`.** An untracked draft in `docs/audits/`
  therefore counts as uncovered. That is deliberate — the artifact is about to be committed — but
  it is the opposite of `silent_rule_detector`'s choice, which reads the index precisely so an
  untracked draft cannot move its metric. The divergence is named rather than left for a reader
  to trip over.
- **It sees one ledger today.** The predicate admits any conforming table anywhere in
  `docs/audits/`, so the surface is general — but the *measured* evidence is a single ledger, and
  a second one has never been parsed by this code in anger.

### 3.6 Test inventory

`tests/test_funnel_coverage.py` — **33 tests, all passing** (13.6s) at Step 3.
**Superseded: the suite is 66 tests after Step 5 — see §5.6 for the current figures and
for the extent of mutation coverage, which does NOT span all 66.**


| group | n | what it holds |
|---|---|---|
| cell splitting | 3 | including the escaped-pipe regression |
| ledger admission — what counts | 4 | every table, every row |
| ledger admission — what it **refuses** | 7 | the false-admit twins for each admission rule |
| the ratchet | 10 | the four contract cases plus the swap, INERT, migration, WARN-tier |
| baseline I/O | 3 | malformed JSON and a non-string list both refuse rather than coerce |
| live corpus | 5 | invariants and monotone bounds, no pinned totals |
| the shipped facade wrapper | 1 | §4.3 |

**No live totals are pinned.** This repo has already been bitten by `ALL_CHECKS` count pins
living in six places; these assert **invariants** (`corpus == dispositioned + pending +
uncovered`) and **monotone bounds** (`dispositioned >= 78`, since dispositions only ever
accrue), so adding an audit does not red the suite while a genuine parser regression still does.

### 3.7 Mutation check — 10/10 caught

A passing test proves nothing until it can fail. Each mutation below was applied to
`scripts/funnel_coverage.py` in isolation, the named test run alone, and the source restored and
re-verified byte-identical:

| # | mutation | guarding test | verdict |
|---|---|---|---|
| M1 | escaped-pipe handling removed | `..._honours_escaped_pipes` | **CAUGHT** |
| M2 | stop after the FIRST table (the `[#560]` class) | `..._reads_every_table_not_just_the_first` | **CAUGHT** |
| M3 | `evidence locator` column no longer required | `..._without_an_evidence_locator_column_is_not_a_ledger` | **CAUGHT** |
| M4 | empty locator accepted as coverage | `..._with_an_EMPTY_locator_is_not_coverage` | **CAUGHT** |
| M5 | off-vocabulary term accepted as coverage | `..._outside_the_ruled_set_is_not_coverage` | **CAUGHT** |
| M6 | ratchet made COUNT-based instead of identity-based | `..._REFUSES_THE_SWAP...` | **CAUGHT** |
| M7 | missing baseline silently treated as empty (fail-open) | `..._is_INERT_and_says_so...` | **CAUGHT** |
| M8 | a hard-verdict literal introduced | `..._is_structurally_incapable_of_failing` | **CAUGHT** |
| M9 | PENDING collapsed into coverage | `..._is_neither_coverage_nor_absence` | **CAUGHT** |
| M10 | README no longer excluded from the corpus | `..._is_excluded_from_the_corpus` | **CAUGHT** |

M6 and M7 are the two that matter most: M6 is the identity-vs-count property the whole baseline
shape exists for, and M7 is the fail-open a missing baseline would otherwise produce.

---

## 4. Arming — Step 4

**Armed as WARN against a zero-baseline ratchet at the measured baseline of 613**, per the
architect's ruling. Not RED. The ruling was not re-litigated and the derivation did not refute
it — §2.4's growth number (~21 undispositioned artifacts/day) is if anything a stronger argument
for it, since a RED would have blocked every audit-producing commit in the repo on day one for a
debt none of those authors created.

### 4.1 Where the WARN actually bites, stated so nobody is surprised

`ALL_CHECKS` membership makes this a **ship-gate leg by construction**, and the two gates treat
it differently:

| gate | posture | effect of this leg's WARN |
|---|---|---|
| `audit-health` (pre-commit, every commit) | **FAIL-only** | none — a WARN informs and the commit proceeds |
| `ship-gate` (at `/ship`, per arc) | FAIL **and** new/undispositioned WARN block | **blocks the arc** until the artifact is ledgered or the WARN is dispositioned in `ecosystem/disposition-register.yaml` |

So the practical contract is: *you may commit an undispositioned audit; you may not ship an arc
that leaves one.* That is the pressure the mandate asks for, applied at the boundary where a
human is already reading — and it is why WARN rather than RED is not a weak arming.

### 4.2 The registration — FENCED DIFF, not applied

`scripts/audit.py` is shared with two sibling lanes, so **nothing below is applied by this
lane.** The integrator applies all three lanes' registrations in one commit.

**(a) the detector import**, alongside the existing `_srd` / `_gtt` adapters (`scripts/audit.py`,
after the `silent_rule_detector` block at ~`:161`):

```diff
 try:
     from scripts import silent_rule_detector as _srd
 except ImportError:
     import silent_rule_detector as _srd
 
+# M3 audit funnel-coverage detector — the PINNED definition of the disposition predicate
+# (ledger table shape + the ruled closed set + detector id). Same module-import + thin-adapter
+# shape as _srd above; the check is an adapter so the detector contract stays independently
+# testable (tests/test_funnel_coverage.py).
+try:
+    from scripts import funnel_coverage as _fc
+except ImportError:
+    import funnel_coverage as _fc
+
 # [#433]/C1 derived-tree coherence gate — the `tasks/` emitter, imported so the check can
```

**(b) the check**, immediately after `check_landing_predicate` and before the `ALL_CHECKS`
literal (`scripts/audit.py`, ~`:3425`):

```diff
+def check_funnel_coverage(repo_path: Path) -> list[Finding]:
+    """M3 — ADVISORY leg: an audit artifact in docs/audits/ carrying no disposition record.
+
+    THE GAP, in ADR-111's own words: "No organ checks that an audit's findings are triaged,
+    and none is built here." The architect standing ruling of 2026-08-17 then closed the
+    artifact-level set — ACTIONED / FILED / REJECTED / SUPERSEDED, "an undisposed audit is a
+    defect, not a document" — and a ledger applied it to 80 artifacts. Nothing read it.
+
+    WARN-TIER BY RULING, never a hard verdict: arming RED against an unmeasured corpus turns
+    the gate off on day one, because everyone routes around a gate that blocks work for a debt
+    they did not create. The flip to RED is a later act with its own ruling. The property is
+    asserted structurally by the test suite (no hard-verdict literal appears in
+    funnel_coverage.ratchet_findings), because an observational check only proves such a path
+    was not REACHED — which is exactly what a latent one looks like.
+
+    ZERO-BASELINE RATCHET, keyed on IDENTITY rather than a count. The committed baseline
+    (ecosystem/audit-funnel-baseline.json) names the 613 artifacts uncovered at arm time; the
+    leg reports `live - baseline` BY NAME. A count-based ratchet is satisfied by draining one
+    old artifact while adding one new undispositioned one — net zero, debt unchanged, gate
+    silent — and with the corpus growing ~21 artifacts/day that swap is the default outcome of
+    ordinary work, not a contrived evasion.
+
+    ONE FINDING PER CONCERN. The #147 register suppresses an ENTIRE Finding on a substring
+    match, so a bundled Finding would let one dispositioned artifact wave through every other
+    regression beside it. [#560] records "bundled Finding" as a live structural rider in
+    check_review_artifact_coverage; it is not repeated here.
+
+    HUB-ONLY by repo identity: the disposition-ledger convention is a hub practice (one ledger
+    here, none in a consumer), so scanning consumers would manufacture a fleet gap — the
+    enforcement-organs-are-not-homogeneous class. Read-only (Layer-2); no git, no writes.
+
+    HONEST LIMIT: this verifies a disposition was RECORDED, not that it is TRUE. A row reading
+    `ACTIONED | deadbeef` passes without `deadbeef` being a real commit, and nothing here
+    resolves the locator. It converts an unfalsifiable claim into a checkable one; it does not
+    make it a true one. It also does not verify that a FILED row's owner was born through
+    intake (ADR-111 §2), nor detect the P-2 orphan when that owner later closes.
+    """
+    name = _fc.CHECK_NAME
+    if not _is_hub(repo_path):
+        return [_na(name, _NA_NOT_APPLICABLE,
+                    "hub-only -- the audit-disposition ledger is a hub practice")]
+    try:
+        root = Path(repo_path)
+        m = _fc.measure(root)
+        baseline = _fc.load_baseline(root)
+    except Exception as exc:  # noqa: BLE001 -- advisory leg: never wedge a gate on its own input
+        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]
+    return [Finding(name, status, evidence.replace("|", "/"))
+            for status, evidence in _fc.ratchet_findings(m, baseline)]
+
+
 ALL_CHECKS = [
     check_vision_md,
```

**(c) the `ALL_CHECKS` entry** — appended last, which is where every recent addition went and
which leaves the existing emission order (a byte-identical output contract the git hooks depend
on) untouched:

```diff
     check_landing_predicate,   # [#513] propagation-completeness — GATING (FAIL-capable), one
                                # Finding per declared ruling in STANDING_RULINGS.md
+    check_funnel_coverage,   # M3 — ADVISORY (WARN-tier by ruling); zero-baseline ratchet over
+                             # docs/audits/ disposition coverage, keyed on artifact identity
 ]
```

**(d) `scripts/audit_checks/registry.py`** — `CHECK_ORDER` must stay in agreement with
`ALL_CHECKS` (its own docstring records that nothing asserts this yet, so it is maintained by
hand):

```diff
-# The canonical order of `audit.ALL_CHECKS`, by function name. 43 entries; the count is pinned
+# The canonical order of `audit.ALL_CHECKS`, by function name. 44 entries; the count is pinned
 # in ARCHITECTURE.md, .claude/commands/{handoff-verify,preflight}.md, deploy/release_lint.py and
@@
     "check_landing_predicate",            # facade — DISPOSITION_REGISTER/_is_hub seams
+    "check_funnel_coverage",              # facade — _is_hub seam; detector in funnel_coverage.py
 )
```

**(e) `ecosystem/doc-code-edge.yaml`** — a new `ALL_CHECKS` member must be `coverage_scope`-
annotated or exempt, or `check_doc_code_coverage_drift` reds. **A `# rule:` marker is wrong
here** and would register as a `code_orphan`: the rule this leg embodies lives in a lane
contract and a ledger, **not in a living doc** (see the registration gap in §1(b)). Same posture
as `review_artifact_coverage`, and temporary for the same reason:

```diff
   - review_artifact_coverage
+  # M3 audit funnel-coverage leg. **TEMPORARY** — expires when the 2026-08-17 audit-disposition
+  # ruling is written into a living doc and registered in protocols/STANDING_RULINGS.md. You
+  # cannot hard-gate an unwritten rule, and today this one is carried only by
+  # docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md:22-27 plus the ledger that
+  # applied it — locatable, but not where a `# rule:` marker could point. When it lands, this
+  # entry converts to coverage_scope and the marker is added. Same shape as the
+  # review_artifact_coverage row directly above.
+  - funnel_coverage
```

**(f) the count pins.** `43 → 44`. **Do not trust the roster in `registry.py`'s own
docstring — three of the five sites it names carry no pin at all, and a fourth's count
moved to another file in `#222`; see §7.6.** These are the sites that actually resolve,
each verified individually:

```
tests/test_audit.py:2207              assert len(aud.ALL_CHECKS) == 43
tests/test_audit.py:2223              assert len(aud.ALL_CHECKS) == 43
tests/test_doc_code_edge.py:248       assert len(aud.ALL_CHECKS) == 43
tests/test_doc_code_edge.py:713       assert len(aud.ALL_CHECKS) == 43
tests/test_writer_integrity.py:185    assert len(aud.ALL_CHECKS) == 43
scripts/audit_checks/registry.py:119  "43 entries" (comment, per (d) above)
```

Each carries a running "N -> N+1: <check> added (<reason>, <date>)" history comment; the
convention is to append, e.g. `43 -> 44: check_funnel_coverage added (M3 — ADVISORY leg,
WARN-tier by ruling; zero-baseline identity ratchet over docs/audits/ disposition coverage,
2026-08-23)`.

**(g) `ecosystem/doc-counts.md`** — regenerate after applying, `python scripts/gen_doc_counts.py
--write`. This lane regenerated it for its own +32 tests; **applying (c) moves the check count
43 → 44 and it must be regenerated again.** It is deliberately outside `_FRESHNESS_FILES`
(decoupled by `#222`), so this does not force a `last_reviewed` re-stamp.

### 4.3 The diff was executed, not just written

A fenced diff nobody ran is a claim.
`test_the_shipped_wrapper_maps_pairs_to_findings_and_is_hub_gated` defines the wrapper body of
(b) **verbatim** and exercises it against the real `audit.Finding`, `audit._is_hub`,
`audit._na` and the live corpus, asserting: the hub gate returns exactly one classified `n/a`;
the hub path returns real `Finding` objects named `funnel_coverage` with advisory statuses only;
every evidence string is free of the literal `|` the locked coherence-spine contract forbids;
and an unreadable corpus degrades to a WARN rather than raising.

**Its honest weakness, stated rather than implied:** it is a *copy* of the shipped body, not an
import of it, because the real thing cannot exist until the integrator applies (b). Two copies
in one artifact is visible to a reviewer; it is still weaker than executing the merged code, and
the integrator should re-run the suite after applying.

---

## 5. Adversarial passes — Step 5 (sol, then five terra rounds)

**Model:** `gpt-5.6-sol`, `codex exec --sandbox read-only`, `model_reasoning_effort=high`.
**Question asked, and the only one asked:** *what is the cheapest way for a real author — not an
attacker, an ordinary person under deadline pressure — to make this check pass without actually
dispositioning anything?*

**sol's verdict, quoted rather than paraphrased:**

> **The check is theatre as a disposition control:** the author controls both the asserted
> artifact and the exemption set, and the implementation explicitly refuses nothing when that
> exemption set rises.

**That verdict is accepted.** It was correct at the time it was given, and five of its eight
routes were holes this lane had not found. **Every reading sol gave was verified against the
source before being acted on** — the separator really was optional, `PENDING` really did accept
an empty locator, there really was no fence tracking. Four routes are now closed and the
residual is recorded honestly rather than argued away.

### 5.1 The eight routes, and what each one is now

| # | route sol found | cost then | status now |
|---|---|---|---|
| 1 | delete the artifact | 0 lines | **vacuous** — sol's own note: "no artifact survives". A *baseline* artifact vanishing is already reported as a stale entry. |
| 2 | escape the shallow glob (`docs/audits/sub/x.md`, or `.markdown`) | 0 lines | **bounded, not closed** — see §5.3 |
| 3 | add the basename to `CORPUS_EXCLUDE` | 1 line | **out of class** — see §5.3 |
| 4 | add the filename to the baseline JSON | 1 line | **cost raised**; residual remains — §5.2 |
| 5 | re-run `--write-baseline` | 1 command | **CLOSED** — the tool now refuses to raise |
| 6 | a blank `PENDING` self-row, no locator, no question | 2 lines | **CLOSED** — a real defect against the ruling |
| 7 | a fabricated closed-set self-row, any 1-character locator | 2–3 lines | **cost raised** — per-term locator shape |
| 8 | a pseudo-ledger inside a fenced code example | 2–4 lines | **CLOSED** — fenced regions are skipped |

### 5.2 The five fixes taken, each measured against the live corpus before arming

**S1 — `PENDING` now requires a non-empty locator.** This was not merely an evasion; it was a
**defect against the governing ruling**, which says an undecidable artifact is *"PENDING with
the exact question it needs"*. A `PENDING` with no question is not the ruling's PENDING. Both
live PENDING rows carry a `Q: …` locator, so **0 false positives**.

**S2 — fenced code regions are skipped.** sol's sharpest finding, because **it bites this very
artifact**: a document that *documents* the ledger shape would otherwise have its examples read
as evidence, and a lane artifact showing a worked example could disposition itself by accident.
Fence-awareness is established practice here — the `markdown_it` fence-region ADOPT is a
`landing_predicate`-tracked ruling with four named sites. Measured: the live ledger is not
fenced, so **coverage is unchanged at 78**.

**S3 — the header separator row is now required.** It removes sol's "2 parser lines" minimum by
making a real markdown table the entry price. The live ledger carries `|---|---|---|---|`, so
**0 false positives**.

**S4 — the locator must carry a reference SHAPED for its term.** `ACTIONED` → a ≥7-hex sha;
`FILED` → a `[#id]`; `SUPERSEDED` → a dated `.md` **that exists in the corpus**. This is what
turns sol's *"any one-character locator passes"* into "a correctly-shaped, and for SUPERSEDED a
resolving, reference". **Measured across all 78 live rows before arming: 0 mismatches for all
three terms, and both SUPERSEDED targets resolve to artifacts that exist.**

**`REJECTED` is deliberately left unshaped, and the reason is measured, not lazy.** A ruling has
no uniform locator form; both live REJECTED locators are prose sentences (144 and 253
characters). Any shape rule strong enough to matter would have false-positived 2 of 2. **So
REJECTED-with-prose is now the cheapest fabricated route, and that is stated rather than hidden.**

**S5 — `--write-baseline` refuses to raise.** The tool that produced the baseline will no longer
silently bless new debt: adding names requires an explicit `--allow-raise`, and the refusal
prints every name it would have added. This closes sol's route 5 (a one-command rebaseline) and
makes route 4 a deliberate, self-describing act. `load_baseline` additionally refuses a baseline
whose `uncovered` count disagrees with `len(artifacts)`, so the laziest hand-edit — one line
added, counts untouched — is refused outright.

### 5.3 Two routes deliberately NOT closed, with the reasoning

**Route 3 — editing `CORPUS_EXCLUDE`.** This is *"edit the checker to disable the check"*, which
is available against every organ in this repo and is not a property of this one. Closing it
inside the check is impossible by construction. It is a code review concern, and it is one line
in a diff.

**Route 2 — the corpus boundary.** The corpus is `docs/audits/*.md`, which is the **ruled**
corpus: the 2026-08-17 ledger measured exactly that set. A **nested** file is already refused by
a live gate — ADR-101 Rule C allowlists the home `docs/audits` and not `docs/audits/*`, so
`validate-hermetization` blocks the added path. A **differently-suffixed** file (`.markdown`) is
outside the corpus *by definition* rather than by oversight — but nothing detects one, and that
is the honest half of this row.

### 5.4 The residual, stated plainly

**A fabricated but well-shaped locator still passes.** `ACTIONED | deadbeef1` is admitted
without `deadbeef1` being a real commit. Closing this means resolving locators: a batched
`git cat-file --batch-check` for shas, a `tasks/` liveness join for ids. **Not taken** — the
`tasks/` half is the P-2 orphan work the contract explicitly scoped out (§7.4), and the git half
adds a dependency to a leg reachable from a pre-commit gate, which is the 236s lesson
`review_artifact_coverage`'s docstring exists to record.

**A baseline raise is still possible** by an author who passes `--allow-raise`, or who edits the
name list and the count together. **sol's recommended hardening — compare the baseline against
the merge base and refuse additions — is the right fix and is OWED, not done.** sol prices it at
*"roughly 30–50 LOC plus 4–6 tests, a git dependency in the gate, and deliberate operator
friction during legitimate detector migrations"*, and it is the exact mechanism
`silent_rule_ratchet` already has (`_target_baseline_state`) and this one does not. **On that
axis this ratchet is measurably weaker than its sibling, and the gap is named rather than
implied.**

### 5.5 The terra loop — five rounds, not one

A terra pass was run against the same code while the Step-4 commit was in flight, so its findings
could fold into **this** edit rather than into a second round of churn. **It did not stop at one
round.** The loop's own lesson, already recorded in this repo, is that *each round finds what the
last graded clean* — and that is precisely what happened here. Rounds 2, 3 and 5 each landed HIGHs
**on the fixes the previous round had just made**, and a single predicate — *"do not read the
examples"* — took **three separate rounds** to get right.

**Five rounds: 0 Critical / 17 High / 10 Medium across 27 findings, 23 regression tests.**

| round | reported | tests | what it attacked | the finding that mattered most |
|---|---|---|---|---|
| 1 | 0C / 4H / 1M | 4 | the Step-3/Step-4 code | T1 — a short row terminated the whole table scan |
| 2 | 0C / 5H / 2M | 6 | **round 1's own fixes** | a one-sided token boundary that *read as solved* |
| 3 | 0C / 2H / 3M | 4 | **round 2's own fixes** | corruption silently treated as bootstrap |
| 4 | 0C / 3H / 2M | 5 | the remaining admission surface | a detector change rebaselined without review |
| 5 | 0C / 3H / 2M | 4 | normalisation and I/O | `errors="replace"` reproducing a known silent-zeroing class |

**The severities are counted honestly rather than flatteringly.** The per-round figures above are
terra's own report; the inline attribution on each fix is my classification of the *fix*, and the
two do not agree everywhere — round 4's five fixes are each annotated HIGH in source while terra
reported 3H/2M. Where they disagree the table follows terra, and the discrepancy is stated rather
than reconciled by picking the more impressive number.

**The class terra kept finding, and sol did not, was the FALSE WARN.** That inverts the framing
Step 5 started with: sol was asked how an author *evades* the check; terra kept finding ways the
check would **wrongly accuse** an author who had done the work. **Four landed defects were of that
kind** — round 1's short-row scan abort, round 2's invisible presentation-marked header, round 3's
rejected uppercase commit locator, and round 5's mismatched term normaliser. Each would have
reported a **correctly dispositioned artifact as UNCOVERED**. A further **three proposed
tightenings were declined for the same reason**, each against a measurement rather than a hunch:
terra's minimum-hyphen floor (a single hyphen is valid markdown), a required trailing pipe
(optional in GFM), and a shape rule for `REJECTED` (it would have false-positived 2 of the 2 live
rows). For a leg whose entire value is gathering zero-false-positive evidence toward a later hard
flip, this is the more dangerous half — and it is the half a purely adversarial pass did not
surface.

#### Round 1 — three defects nobody else found

It returned **0 Critical / 4 High / 1 Medium**. Two of its four HIGHs were sol's fence and
separator routes, independently found. **Three findings were nobody else's, and two are outright
bugs rather than evasions:**

**T1 (HIGH) — a short row terminated the whole table scan.** `if body is None or len(body) <=
widest: break`. One `| a bare note |` line between two ledger rows silently discarded **every
row after it**. This is the `[#560]` stop-early class arrived at by a different route, and its
consequence is the worst kind this leg can have: **correctly dispositioned artifacts reported as
newly UNCOVERED** — a false WARN, which is exactly what corrupts the zero-false-positive
evidence a later hard flip would rest on. Fixed: a malformed row is skipped; only a non-row ends
the table.

**T2 (HIGH) — a filename prefix bound to the wrong artifact.** `_AUDIT_NAME_RE` is non-greedy up
to `.md`, so a File cell reading `2026-08-01-technical-a.md.bak` matched
`2026-08-01-technical-a.md` — a backup reference or a typo silently becoming coverage and
suppressing the WARN. Fixed with a trailing token-boundary lookahead; three live decorations
(backticked, path-prefixed, bare) are pinned so the fix cannot over-tighten.

**T3 (MEDIUM) — the wrapper test proves a copy, not the registration.** terra is right, and
**half of it is unfixable in this lane**: the real function cannot exist until the integrator
edits `scripts/audit.py`. §4.3 already stated that weakness rather than implying it. **The other
half was fixable and is fixed** — the two copies could silently *diverge*, shipping one wrapper
in the artifact while the test proved a different one.
`test_the_fenced_registration_diff_and_the_wrapper_test_cannot_DRIFT` now extracts the shipped
body **from the artifact's own fenced diff** and asserts every executable line appears in the
test. It earned its place immediately: it failed on first run, on a real difference between the
two copies.

**Neither T1 nor T2 was reachable by the corpus as it stands** — the live ledger has no short
rows and no `.md.bak` cells, which is why the measurement was correct before and after. They
were latent, and a latent false-WARN generator inside an evidence-gathering leg is worth more
than its severity suggests.

#### Round 2 — five HIGHs, on round 1's own hardening

Round 2 attacked the round-1 fixes themselves — the fence tracker, the boundary lookahead, the
separator requirement — which is exactly where new code is weakest.

- **A one-sided boundary (HIGH).** Round 1's T2 fix added a **right** boundary and left the left
  one open, so `typo2026-08-01-technical-a.md` still dispositioned the real artifact. **A fix
  that closes one end of a boundary and not the other is the more dangerous kind: it reads as
  solved.** Both sides are now required.
- **A nested *shorter* fence reopened scanning (HIGH).** The tracker toggled on **any** fence, so
  a three-backtick example inside a four-backtick block closed the outer fence — the exact hole
  the tracker was added to close, reintroduced one level down.
- **Presentation-marked headers were invisible (HIGH, and a FALSE WARN).** Disposition cells were
  normalised for bold; header cells were matched raw. A valid table headed `| **File** | … |`
  was not seen at all, and **every artifact it dispositioned would have been reported uncovered.**
- **Separator column count must match the header (HIGH).** A real table's separator always does,
  so requiring it refuses a fabricated pseudo-table without refusing a well-formed one. **terra's
  proposed minimum-hyphen floor was deliberately NOT adopted:** a single hyphen is valid markdown,
  so a three-hyphen floor would false-WARN a genuinely well-formed ledger.
- **An absent `uncovered` field disabled its own guard (MEDIUM).** The count-vs-identity integrity
  check only fired when the field was *present*, so omitting it skipped the check a hand-edit was
  supposed to trip. The field is now required.
- **The WARN-only proof never executed two of its branches (MEDIUM).** The source-literal test is
  beatable by a dynamically built status, and no fixture had ever supplied a measurement carrying
  malformed or dangling rows. Both tests are kept: the source test catches the honest mistake,
  the observational one catches the clever one.

#### Round 3 — the third variant of one hole

- **An invalid fence *closer* reopened scanning (HIGH).** After "any fence closes" (round 1) and
  "a shorter fence closes" (round 2), this is the **third** variant of the same predicate: a
  CommonMark closing fence carries only whitespace after its marker, so a fence marker followed
  by an info string inside a block is an opener-shaped line, not a closer. **Three rounds on one
  predicate is the honest measure of how hard "skip the examples" actually is.**
- **Corruption silently treated as bootstrap (HIGH).** `load_baseline` returns `None` for both an
  absent and an unreadable baseline, so keying the raise guard on it alone meant **deleting or
  corrupting the committed baseline silently blessed every regression** — a one-command,
  attacker-free defeat of the identity ratchet. A genuinely absent file is a first arm; a
  present-but-unreadable one is indeterminate, and an indeterminate baseline is not replaced
  without the operator saying so.
- **An uppercase commit locator was rejected (MEDIUM, FALSE WARN).** A git object name is
  hexadecimal and case-insensitive; `DEADBEEF` names a commit exactly as well as `deadbeef`. The
  ruling asks for a commit, not for lowercase formatting.
- **A documentation claim was the half that was wrong (MEDIUM).** The docstring claimed outer
  pipes were required while the code only ever enforced the leading one. A leading pipe is what
  discriminates a row from prose; a trailing pipe is optional in GFM, and requiring it would
  false-WARN a well-formed ledger. **The claim was corrected; the behaviour was kept.**

#### Round 4 — the remaining admission surface

- **An indented code block is a code block (HIGH).** CommonMark makes a 4-space-indented line a
  code block, and `split_cells` stripped the indentation away before looking — the same
  "documentation becomes evidence" class as the fence tracker, reached without a fence.
- **An HTML comment is the other way a document carries an example it does not mean (HIGH).**
- **A bare token is not a rejection reason (HIGH).** `REJECTED | x` reached the success path
  because no *shape* rule is possible for a ruling citation. A **substance** floor is the only
  rule this corpus supports, and it is **the weakest predicate in the module**: it separates a
  recorded reason from a token and nothing more. Measured: the two live REJECTED locators are
  144 and 253 characters.
- **A PENDING locator must actually ask something (HIGH).** Straight from the ruling's own words —
  PENDING carries *"the exact question it needs"*, and a question is punctuated. Both live PENDING
  rows open with `Q:` and contain `?`, so requiring the mark cost **0 false positives**.
- **A detector change rebaselined without review (HIGH).** `--write-baseline` compared artifact
  sets and never the detector id, so a predicate revision that happened to *lower* the count read
  as a drain, quietly wrote the new id, and the mismatch WARN never fired again. That is exactly
  the failure `[#436]`'s detector-id discipline exists to prevent, reproduced in a sibling.

#### Round 5 — normalisation and I/O

- **Two normalisers, one corpus, different rules (HIGH, FALSE WARN).** Term cells stripped only
  `*` while header cells already stripped backticks, so a valid backticked `ACTIONED` read as
  malformed and left a genuinely dispositioned artifact uncovered.
- **`errors="replace"` reproduced a known silent-zeroing class (HIGH).** `silent_rule_detector`'s
  own contract records that its arm-time probe used a platform default encoding and *"SILENTLY
  ZEROED several files before erroring — a silent decode failure is the exact measurement-error
  class this metric must not reproduce"*. An unreadable byte anywhere in the corpus left the
  ratchet passing on a read that had **partly failed**. Decoding is now strict and a failure
  RAISES. Measured: all 693 live artifacts are valid UTF-8, so strict decoding costs nothing today
  and refuses loudly the day it doesn't.
- **Recovering a corrupt baseline is its own act, not a raise (HIGH).** Round 3 accepted
  `--allow-raise` for this; round 5 split the two, because *adding names to a valid baseline* and
  *destroying a damaged one* are different decisions. `--recover-corrupt-baseline` now names the
  second.
- **Duplicate baseline names (MEDIUM).** The ratchet compares **sets**, so a duplicated name
  satisfied the count-vs-list check and then collapsed to one identity — the declared count
  agreeing with the *list* while disagreeing with the *identity set the ratchet actually uses*.

### 5.6 Re-measured after every fix, because a tightening that changes the number is a bug

```
before hardening      :  corpus 693 · dispositioned 78 · pending 2 · uncovered 613 · malformed 0 · dangling 0
after sol + round 1   :  corpus 693 · dispositioned 78 · pending 2 · uncovered 613 · malformed 0 · dangling 0
after rounds 2-5      :  corpus 693 · dispositioned 78 · pending 2 · uncovered 613 · malformed 0 · dangling 0
```

**Identical, three times.** Across sol's four tightenings of the admission predicate (fences,
separator, locator shape, PENDING) and five terra rounds — a further eleven predicate changes
including strict UTF-8 decoding, indented-code and HTML-comment blanking, both-sided filename
boundaries, separator width matching, a REJECTED substance floor and a PENDING interrogative
requirement — the live corpus never moved. **That is the evidence the tightenings closed evasion
routes rather than manufacturing false WARNs**, and it is worth more here than anywhere else,
because four of terra's landed findings were themselves false-WARN bugs (§5.5). Each change was measured
against all 78 live rows before it was armed; `REJECTED` was left shape-free precisely because
that measurement said a shape rule would have false-positived 2 of 2.

**Suite after the whole pass: 66 tests, all green in 7.9s** — 33 at Step 3, 47 after sol + terra
round 1, 66 after terra rounds 2–5. The 19 tests added by rounds 2–5 are named regressions, one
per finding that admitted a dedicated fixture; the rounds' remaining findings are pinned by
inline attribution at the fix site in `scripts/funnel_coverage.py`. These figures supersede
§3.6/§3.7, which were accurate at Step 3.

**Mutation coverage is stated at its real extent, not extrapolated.** **19/19 mutations caught**
covers the Step-3 and round-1 surface — the 10 of §3.7 plus 9 pinning sol's hardening (fence
blanking, separator requirement, short-row handling, filename boundary, locator shape, SUPERSEDED
resolution, blank PENDING, baseline count agreement, the `--write-baseline` raise guard). **The
19 regressions from rounds 2–5 were NOT mutation-checked.** Each was written against a
reproducing failure and observed to fail before its fix, which is weaker evidence than a mutation
sweep and is not the same claim. Extending the sweep to the full 66 is owed, not done — it is the
one piece of this lane's own evidence standard that the lane did not hold itself to.

### 5.7 What the check is, after the pass

Not theatre, and not a guarantee. **It converts silence into a signed, attributable claim.**
Before it, an audit whose findings nobody routed simply joined the pile and no surface knew.
After it, passing requires writing a term from a ruled closed set with a correctly-shaped
locator into a real markdown table, or deliberately raising a curated baseline that names the
excused file in the diff. That is the same honest ceiling `review_artifact_coverage` states
about its own tally — *"a fabricated header passes… it converts an unfalsifiable claim into a
checkable one; it does not make it a true one"* — and claiming more would be exactly the
overclaim this pass exists to catch.
