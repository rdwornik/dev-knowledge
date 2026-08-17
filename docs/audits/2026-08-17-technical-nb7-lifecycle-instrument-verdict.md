<!-- scope: meta -->
# Lifecycle instrument verdict — nb7-C · 2026-08-17

**Produced by:** CC, lane `nb7-C`, branch `claude/nb7-instrument-verdict-8yw1a2`. Read-only + web.
**Question:** the operator has asked three times for a system / tool / library that manages the
`intake → ADR → backlog` lifecycle so decisions cannot rot unowned. This is the verdict.

---

## §0 · The answer first

```
VERDICT: the instrument is NOT new. [#552] already specifies four of the five gap
requirements -- as PROPOSALS at a Stop hook writing a GITIGNORED artifact. What is
genuinely unowned is (i) the enforcement TIER, (ii) the age ARITHMETIC, (iii) the
durable VIEW. Compose those three; build no new system.

  Part A  schema/data     pin ADR-98 section 6's "~1 month" to 30 days at its
                          canonical home + land [#551]'s audit `status:` enum   ~0 new code
  Part B  one audit check `check_decision_carriers` -- promote [#552] leg (b)'s
                          four detections from proposal-tier to Finding-tier      ~180 lines
  Part C  one view        `ecosystem/lifecycle-ledger.md`, generated + freshness
                          -gated, 4th instance of a 3-precedent pattern          ~180 lines

  BIRTHS: 1 row (Part C). AMENDMENTS: 2 ([#552] gains leg (c); [#551] unchanged,
  named as the audit-corpus half). Net births under the [#555] campaign: +1.

  ALL SEVEN library candidates REJECTED as the store or the mechanism. Two
  (check-jsonschema, stdlib sqlite3) survive as OPTIONAL adjacencies at zero cost.
```

**The single most decisive piece of evidence in this report**, because it shows the gap is not
theoretical: the intake survival metric has fired **exactly once in the scene's history**, by
hand, and immediately went dark. `protocols/STANDING_RULINGS.md:1035-1044` records I-D7 —

> `docs/intake/2026-07-11-tech-c4-visualization-memo.md` (intake #10) has been `status: DRAFT` for
> **31 days** as of 2026-08-11, which fires the `docs/intake/README.md` §7 survival metric verbatim

That detection cost a GO ruling, a rejection commit (`f095a81f`), and a retirement append four days
later. Six days after that ruling, **six SEED docs sit at 40–41 days** with zero citing live task and
zero citing ADR (§2 G2), and nothing has fired. The metric is not weak — it is **uninstrumented**, so
it fires only when a human happens to look. That is the whole gap in one sentence.

---

## §1 · What already exists in the tree as lifecycle machinery

**17 live organs across the five classes named in the brief.** Every one is quoted from disk.
This section exists so the verdict cannot propose anything already built.

### 1.1 Generators (4) — the derivation direction is already flipped

**`scripts/gen_task_tree.py`** — `tasks/` is source of truth; `BACKLOG.md` is *generated*.

> THE DERIVATION RUNS TREE -> FILE. `tasks/` is the SOURCE OF TRUTH; `BACKLOG.md`
> is GENERATED from it. That direction was flipped by [#439] on 2026-07-28 under
> ADR-107 §7.2 […] `find_incoherences` REFUSES a file whose frontmatter disagrees with what its
> own body derives, precisely so that inert-looking metadata cannot rot into a quiet lie.

**`scripts/gen_intake_index.py`** — status-grouped intake navigation, derived on-edit from frontmatter.

> Navigation is via this generated index grouping by lifecycle state, derived on-edit from each
> doc's frontmatter `status:` (no sweep) […] This generator itself MOVES NO FILE

**`scripts/gen_audit_index.py`** — the audit corpus index; retention is *ruled*, shape is `[#269]`.

> The RETENTION policy is **ruled**: ADR-100 […] decided keep-all-accepted […] ADR-100 ALSO names a
> count-tiered index shape, which is **not built here**

**`scripts/gen_intake_tree.py`** — the intake residue-carrier split (ADR-109 §4 generality proof).

Two more generated-and-gated surfaces are the *pattern precedent* Part C reuses:
`scripts/generate_organ_index.py` → `ecosystem/organ-index.md`, and `scripts/gen_claude_rosters.py`.

### 1.2 Manifests (3) — reversibility carriers, already schema'd

**`tasks/manifest.json`** — the residue carrier that makes one-file→many-files reversible:

> every non-task prose line of BACKLOG.md, in order, interleaved with task-node pointers. It
> carries the document's STRUCTURE […] This is what makes one-file->many-files reversible

**`docs/intake/manifest.json`** — `intake-residue-manifest/v1`, and it already declares its own
projection honestly:

> `"projected_frontmatter_keys": ["intake-id", "status"]` […] `"intake_document_bodies"`: The
> unstructured wave-prose inside each docs/intake/*.md is not part of the monolith […] Bodies are
> deliberately NOT hashed: that would couple this manifest to every intake body edit and RED the
> gate on unrelated work

**`ecosystem/disposition-register.yaml`** (28 entries) — the ADR-75 decoration rule is the *exact
anti-rot discipline* Part B must inherit:

> Decoration rule (ADR-75): an entry that matches NO live WARN on a run is SURFACED as
> stale in the gate's output (awareness — it does not block); the register is not allowed
> to silently rot into paper suppressions.

### 1.3 Coherence checks (5)

| organ | locator | what it enforces | tier |
|---|---|---|---|
| `validate_backlog` | `scripts/validate_backlog.py` | `Done when:` present; `depends-on` **reference-existence + cycles**; `[S<n>]` story ids; done-task-must-leave | FAIL |
| `gen_task_tree --check` | `scripts/gen_task_tree.py` | `BACKLOG.md` on disk == tree render, and each task's frontmatter == its own body | FAIL (ship-gate leg) |
| `check_intake_tree_coherence` | `scripts/audit.py:2442` | the intake residue-carrier round-trip; four legs delegated to `gen_intake_tree.evaluate` | FAIL |
| `check_preflight_backlog_ids` | `scripts/audit.py:3037` | `kill-candidates:` values name a **still-open** row | **WARN by ruling** |
| `validate_reconciliation._SPEC_REGISTRY` + `coherence_nudge` | `scripts/validate_reconciliation.py:96-108`, `scripts/coherence_nudge.py` | the typed doc→spec edge `reconciled_with: <spec>@<version>`; content-changed-without-version-bump nudge | FAIL / nudge |

`validate_backlog` already proves the *hard part* of G1 is affordable — it resolves cross-reference
existence today:

> (#156 task-graph) a `· depends-on: #id` referencing an id that is not a live task
> (strict reference-existence — closed ids have left the file)

And `check_preflight_backlog_ids` already carries the honest limit Part B inherits verbatim:

> HONEST LIMIT (R3's named gap): this verifies id-LIVENESS of assertions, not correctness of
> PLACEMENT. A citation on the wrong line still passes.

### 1.4 Backpressure organs (3)

**`scripts/check_backlog_filing.py`** (commit-msg) — the add-side gate, and **leg 3 is already the
intake-traceability leg, deliberately toothless**:

> Leg 1 (BLOCK): the commit message MUST carry a `kill-candidates:` line […]
> Leg 3 (WARN, #279): a NEW L-sized new-feature epic that lacks an intake-id citation
> (ADR-98 section 3) earns an advisory WARN -- it NEVER blocks.

**`scripts/check_backlog_commit_msg.py`** (`backlog-id-on-close`) — the remove side.

**`scripts/propose_closures.py`** (Tier-1 Stop hook) — detect-and-propose, STRONG/WEAK tiers, and
the line that decides §5's Part C:

> **DETECT-AND-PROPOSE ONLY**: this script never closes, removes, or modifies a backlog item. […]
> The artifact is gitignored — it is ephemeral session scaffolding, not the durable record

### 1.5 Footprint (2) — and it is *receding*, which changes the verdict

**The `footprint:` clause** on backlog rows is the nearest existing thing to a carrier field.
Measured live on this branch:

```
open rows carrying footprint:      3   ([#502] [#506] [#507])
open rows total                  194   (7 P1 / 96 P2 / 91 P3)
share                            1.5%
```

The 2026-08-10 distillate measured **5 of 196 (2.6%)** and called the gap "widening". It has widened
further, and by a mechanism worth naming: the numerator fell because **three of the five rows closed
([#501] [#503] [#504]) and no new row adopted the field**. `footprint:` is not a convention spreading
slowly — it is a 5-row experiment now down to 3. **Building traceability on it would be building on a
receding surface**, which is why §5 does not.

**`ecosystem/doc-code-edge.yaml`** (176 lines) — the declared doc→code edge registry, and its header
states the design law Part B must obey:

> AUTHORITATIVE DECLARATION SOURCES ONLY (ADR-89 OQ1). Each entry is a doc that AUTHORITATIVELY
> declares an enforced rule -- declare a rule at its source, NEVER in a summary

### 1.6 The three status enums — and their asymmetry

| corpus | field | enum | validated by | live terminal values |
|---|---|---|---|---|
| `tasks/*.md` | `status:` | open · closed · deferred · retired · superseded | `gen_task_tree.find_incoherences` (frontmatter vs body) | all 5 in use (288 files) |
| `docs/intake/*.md` | `status:` | SEED · DRAFT · READY · ACCEPTED · CONSUMED · SUPERSEDED · REJECTED | **nothing** — only the *index generator* reads it | 0 terminal live (all 34 are live-state) |
| `docs/decisions/ADR-*.md` | prose `Status:` line | Accepted · Proposed · Superseded · Deprecated · Partially superseded | **nothing** | 83 Accepted · 3 Proposed · 2 Partially superseded · 1 Explored · **0 Superseded · 0 Deprecated** |
| `docs/audits/*.md` | — | **none** ([#551]) | — | 25 of 574 carry an ad-hoc off-schema `status:` (`complete`, `resolved`, `for-operator-review`, `snapshot (Phase A input…)`, …) |

The ADR row is the one that matters: `docs/decisions/README.md:18-19` already states why —

> **H3's archival bar keys on `Superseded` / `Deprecated`**, two values that appeared on
> zero live ADRs, so the bar's trigger was unreachable by its own wording.

Only two ADRs have ever reached `docs/decisions/archive/` (ADR-40, ADR-52). The lifecycle's terminal
half is, for the ADR corpus, **structurally unexercised** — which is exactly [#552]'s honest limit.

**e = 17 organs.** Nothing in §5 duplicates any of them.

---

## §2 · The gap, as requirements

Five requirements. Each carries a **live measurement**, so none is an aesthetic preference.

### G1 · Decision-carrier traceability — a live decision resolves to ≥1 live carrier, mechanically

`docs/intake/README.md` §1 and §3 already *declare* the join key:

> `intake-id` is permanent once assigned — it is the join key the accepting ADR and the
> resulting epic(s) cite back (§1).

Measured live on this branch (`intake #N` / `intake-id: N` citation over `docs/decisions/ADR-*.md`
and `tasks/[0-9]*.md`):

```
ADRs total                                    85
ADRs citing any intake                        10   (11.8%)
task files total                             288
task files citing any intake                  24   ( 8.3%)
intake docs (all live-state)                  34
  -- cited by ZERO live task                  20   (58.8%)
  -- cited by ZERO live task AND ZERO ADR      18   (52.9%)
```

**The two that matter most**, because their own frontmatter claims active consumption:

```
#31  ACCEPTED  disposition: active   age  8d   0 citing rows   0 citing ADRs
     docs/intake/2026-08-09-func-code-style-doctrine.md
#32  ACCEPTED  disposition: active   age  8d   0 citing rows   0 citing ADRs
     docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md
```

`docs/intake/README.md` §5 defines `disposition: active` as "**being consumed now**". Two documents
assert they are being consumed now, and nothing in the tree consumes them. That is a **self-refuting
frontmatter state that passes every gate**, which is precisely the class G1 must refuse.

**Requirement:** a live-status decision carrier (`docs/intake/` at `SEED|DRAFT|READY|ACCEPTED`) must
resolve to ≥1 live `#id` or `ADR-NN`, or carry an explicit `none — <reason>`. Third option: none.

### G2 · Age-of-unowned alarm — the rent rule computed, not remembered

`docs/decisions/ADR-98-intake-pipeline.md:51` and `docs/intake/README.md` §7:

> If intake docs go **unconsumed after ~1 month of operation**, the scene is **reviewed for removal**
> […] A folder that only accumulates SEED/DRAFT docs nobody triages has failed the same test a
> routine fails.

Measured live, age from each doc's own **origin date** (its filename date — the README §4 rule that
"the date is the **origin** date"), against today 2026-08-17:

```
live-state intakes with ZERO citing live task, by age:
   41d  #4   SEED   2026-07-07-arc5-pilot-followup-seeds.md
   41d  #5   SEED   2026-07-07-changelog-review-seeds.md
   40d  #6   SEED   2026-07-08-func-new-project-bootstrap.md
   40d  #7   SEED   2026-07-08-func-ai-council-interface.md
   40d  #8   SEED   2026-07-08-func-night-routines-suite.md
   40d  #9   SEED   2026-07-08-func-dashboards-local-html.md
   32d  #15  READY  2026-07-16-satellite-onboarding-prompts.md
   18d  #21  SEED   2026-07-30-tech-browser-architect-orientation.md
   12d  #24  DRAFT  2026-08-05-tech-currency-wave-1.md
   ...  (20 of 34 total)

BREACHING the ~1 month horizon:  7 docs (six at 40-41d, one READY at 32d)
FIRINGS to date:                 1 (intake #10, by hand, STANDING_RULINGS I-D7)
```

Folder composition: **10 SEED + 9 DRAFT = 19 of 34 (56%) in pre-triage states** — the literal
condition §7 names as failure ("a folder that only accumulates SEED/DRAFT docs nobody triages").

**Honest note on the age predicate, stated because it changes what a check may claim:** git add-date
is *not* usable here — `git log --diff-filter=A` returns `2026-08-11` for 32 of 34 intake docs (a
history event, not authorship), so a check keyed on git add-date would read every one of these as
6 days old and stay green forever. The filename origin date is the only honest clock, and it is
already the README-ruled semantic. A check must key on it and **say so**.

**Requirement:** the ~1 month horizon is pinned to a number, computed from origin date, and a breach
is emitted as a Finding — not discovered when a human happens to read the folder.

### G3 · Status lifecycle parity across the three corpora

Per §1.6: `tasks/` has a validated 5-value enum; `docs/intake/` has a ruled 7-value enum that
**nothing validates**; `docs/decisions/` has a 5-value enum in **five distinct prose formats** with
**zero live terminal values**; `docs/audits/` has **no field at all**, and 25 of 574 files carry
ad-hoc off-schema strings in its place.

[#552] already encodes the parser hazard, so it must not be rediscovered:

> three ADR status-line formats coexist (bold `Status:`, list-item bold `Status:`, and YAML
> frontmatter — ADR-61 only), and a single-format parser returns a false `None` on ADR-61.

My own measurement finds **five** on-disk shapes, not three (`- **Status:** X`, `**Status:** X`,
`Status: X`, `- **Status:** X — <date>`, plus ADR-61's frontmatter). Recorded so the parser is written
against the live corpus rather than the row's count.

**Requirement:** each corpus's status field has a **stated closed enum at a canonical home** and a
**mechanical reader**. The ADR corpus's terminal half being unexercised is [#242]/[#362], NOT this
requirement — G3 asks only that the field be *readable*, not that the corpus be re-dispositioned.

### G4 · Trigger / un-park resolvability

`docs/intake/README.md:194` states the intent:

> the un-park condition is part of the record, not tribal memory

And [#548] states the defect exactly: "**nothing checks that the trigger still RESOLVES**, so this
document is schema-conformant and permanently parked at the same time."

Measured live: **3 of 3** deferred ACCEPTED docs (#12, #13, #14) carry `trigger: "#328 build"`, and
`[#328]` does not exist — no `tasks/328-*.md`, zero `^- \[#328\]` rows. **Zero** intake docs use the
`review-date:` alternative the schema offers. So 100% of the parked corpus is parked on a departed id,
and the escape hatch the schema provides has never been exercised.

**Requirement:** a `trigger:` naming a `#id` that is not a live task FAILs. (Same predicate
`check_preflight_backlog_ids` already applies to `kill-candidates:` — import it, do not restate it.)

### G5 · One queryable view

There are four generated navigation surfaces (`BACKLOG.md`, `docs/intake/README.md` index,
`docs/audits/README.md`, `ecosystem/organ-index.md`) and **none of them joins the corpora**. The only
artifact that has ever answered "which decision is unowned" across corpora is
`docs/audits/2026-08-17-technical-audit-disposition-ledger.md` — a **one-shot, hand-run lane output**,
80 rows of a measured 129, with 49 named as follow-on.

And the surface [#552] routes its answer to is **gitignored**: `.gitignore:26` is `logs/PROPOSALS-*.md`,
and `git ls-files | grep -c PROPOSALS` returns **0**. So under [#552] as written, the answer to
"what is unowned" is computed at session end into a file that is deleted with the container and
never enters the record.

**Requirement:** one committed, generated, freshness-gated artifact, one row per decision carrier
across `docs/intake/` × `docs/decisions/` × `docs/audits/` × `tasks/`, with columns
kind · id · status · age · carrier · verdict.

**g = 5.**

---

## §3 · Library-first evaluation

Current versions verified against PyPI on 2026-08-17. Windows fit is called honestly, because
`mutmut` ([#502]) is the standing reminder that a `fork()` dependency makes a tool CI-only here.

### 3.1 `check-jsonschema` — **0.38.0 (2026-08-09)**, Apache-2.0, `>=3.10`

Pure-Python (`jsonschema` + `ruamel.yaml`), pre-commit-native, **Windows-clean**. Healthy: 0.37.4 →
0.38.0 in six weeks.

**Fit against the gap: poor, for two specific reasons.** (i) It validates **files that are JSON /
YAML / TOML**. `docs/intake/*.md`, `docs/decisions/ADR-*.md` and `tasks/*.md` are **markdown with a
frontmatter block** — the tool has no frontmatter extractor, so every target needs a
markdown→temp-YAML shim, and that shim is more code than the check it would replace. (ii) The three
requirements with teeth (G1 carrier resolution, G2 age arithmetic, G4 trigger liveness) are
**cross-file reference resolution and date math**, which are not expressible as JSON Schema
predicates at any version.

**Verdict: REJECT as the mechanism. Its standing ADOPT-candidacy is unchanged and I am narrowing,
not re-pricing, its scope** — adoption ledger item 35's target set is `deploy/manifest-v*.yaml` (6
files that already *are* YAML) plus `.github/workflows/report-only-wall.yml` (covered out of the box
by `check-github-workflows`). That remains correct and untouched by this report. What is new here is
the finding that **item 35 must not be stretched to cover the frontmatter corpora** — the file format
forbids it.

### 3.2 A `validate_decision_carriers` audit check on existing frontmatter — **zero new deps**

Reads what is already on disk. Rides three surfaces it does not have to build: the already-armed
`audit-health` pre-commit gate (so it is enforced at every commit with no new wiring), the `ship-gate`
`Finding.status` contract, and the `ecosystem/disposition-register.yaml` suppression path with its
ADR-75 stale-decoration rule (so a disposition that stops holding anything is surfaced, not silently
kept). It is the only candidate that can express G1, G2 and G4.

**Verdict: ADOPT.** This is Part B. Sizing anchor: `scripts/audit_checks/check_routine_consumers.py`
is **172 lines** for a comparable four-leg check.

### 3.3 SQLite view over the manifest (`datasette-lite` for read)

`datasette` **0.65.3 (2026-08-06)**, Apache-2.0; `sqlite-utils` **4.2.1 (2026-08-13)**. Both pure
Python, both Windows-clean (`datasette` is ASGI/uvicorn — it runs, no `fork()` issue).

**Three independent reasons to decline the committed-`.db` shape.** (i) `datasette-lite` is a
Pyodide/WASM page that loads a database **by URL over HTTP with CORS**. This repo is **private on the
GitHub Free tier** — the same constraint that makes ADR-101's recorder "REPORT-ONLY **permanently**"
because required checks are unavailable — so there is no host to serve a `.db` from, and a local file
cannot be loaded by the WASM page without standing up a local server. (ii) A binary `.db` is
undiffable in a tree whose entire discipline is `git ls-files`-greppable markdown, and ADR-101 Rule C
would refuse a new home for it anyway. (iii) The precedent already exists and points the other way:
`scripts/telemetry_emit.py` uses **stdlib `sqlite3` in WAL mode** and its own header rules the
posture —

> a local ephemeral artifact under `logs/` is an established in-repo pattern with four live instances
> […] This store joins that class: one local file, never committed, never touching a sibling repo.

**Verdict: REJECT as the committed view.** The view is generated markdown (Part C), matching three
live precedents. **Optional adjacency at zero dependency cost:** the same generator can take an
`--emit-sqlite` flag writing into the *existing* gitignored `logs/` store via stdlib `sqlite3`, giving
ad-hoc SQL for free. ~15 lines, no new dep, no new committed file. Offered, not required.

### 3.4 Git-trailer conventions (`Closes:` / `Decision-Ref:`) — zero deps, git-native

`git interpret-trailers --parse` is in every git. Adoption-ledger item 37 already measured the
migration cost:

> over `origin/main`'s 52 first-parent commits `CLOSES_RE` fires on 8 (7 ids) while `Closes:`/`Fixes:`
> trailers appear on ZERO, so a pure trailer matcher would lose 100% of the live signal

Re-measured on this branch over the last 60 first-parent commits: **3** trailer lines total, all
`kill-candidates:`. So the convention is present in shape and absent in the closure key.

**Verdict: REJECT for this instrument — and the reason is structural, not migration cost.** A trailer
annotates a **commit**. The gap is an **absence**: intake #31 has no carrier *because no work
happened*, so there is no commit to carry a trailer. **A trailer can only annotate presence; the gap
is defined by absence.** Item 37 stays a live P-B forward-convention candidate on its own merits
(it kills the `CLOSES_RE` false-positive class), and this report neither advances nor retires it.

### 3.5 `doorstop` — **3.2 (2026-07-10)**, LGPLv3, `>=3.10,<3.15`

**On the DECLINE list already** (distillate §3: "sphinx-needs / Doorstop / StrictDoc as the store").
Under DECLINE-list law I checked for new evidence and am recording what I found so the next reader
does not re-check: **3.2 shipped five weeks ago, so it is genuinely alive**, and `Operating System ::
OS Independent`. That is a real currency update.

**It is not new evidence against the decline, because liveness was never the reason.** The reason was
"imposes its own store while this repo's YAML frontmatter already *is* the node/edge source", and
that is verified unchanged: doorstop keeps one YAML item file per requirement in a `.doorstop.yml`
document tree, so the intake docs, ADRs and tasks would have to **migrate into its layout** — which
ADR-101 Rule C would refuse as a new home, and which would abandon the flip [#439] just landed.

Two further facts found while checking, worth recording: doorstop pulls **10 runtime deps** (`bottle`,
`openpyxl`, `plantuml-markdown`, `python-markdown-math`, `requests`, `six`, `verchew`, …) into a
governance repo whose entire dev group is 10 — and **one of them is `python-frontmatter`, which this
repo has already measured and disqualified**: `scripts/gen_task_tree.py` records "0/20 byte-identical,
with no config escape: PyYAML `sort_keys=True` reorders every key […] DISQUALIFIED on fidelity". Also
LGPLv3 against an otherwise permissive set.

**Verdict: STAYS DECLINED.** Currency updated (3.2, 2026-07-10); decline rationale re-verified intact.

### 3.6 Trace tooling from requirements engineering — `sphinx-needs`, `StrictDoc`

**`sphinx-needs` 8.3.1 (2026-08-11)** — I checked the one thing that could constitute new evidence,
namely whether it had shed its framework. It has not: its install requirements at the current version
are `sphinx>=7.4,<10`, `sphinx-data-viewer`, `sphinxcontrib-jquery`. **The exact reason for the
decline is verified unchanged at the current release. NO NEW EVIDENCE IS NAMED. sphinx-needs
STAYS DEAD.**

**`StrictDoc` 0.28.0 (2026-08-11)** — same class, own SDoc DSL, same distillate decline. **STAYS
DEAD.**

Also checked, since the distillate's Log4brains decline named it as the fallback: **`pyadr` 0.19.0,
last released 2022-04-05 — cold 4.4 years.** So of that decline's two named alternatives ("pyadr or
plain frontmatter first"), **only "plain frontmatter" survives**. Recorded as a currency finding.

**And the decline is what the verdict obeys, not what it works around.** The distillate's own
instruction was "**Copy the schema, not the tool**" — a stable typed id per artifact, typed links as
frontmatter keys. §5's Part A/B is literally that: no new store, the existing `intake-id` join key,
the existing `consumers:`/`trigger:` keys made resolvable, one reader.

### 3.7 DECLINE-list law — compliance statement

```
sphinx-needs  8.3.1  2026-08-11  reason re-verified (sphinx>=7.4,<10 still required)  STAYS DEAD
StrictDoc     0.28.0 2026-08-11  reason re-verified (own SDoc DSL)                    STAYS DEAD
doorstop      3.2    2026-07-10  ALIVE (currency updated) -- reason unchanged          STAYS DECLINED
Log4brains    n/a                Node/Next.js bring-in; unchanged                     STAYS DECLINED
pyadr         0.19.0 2022-04-05  COLD 4.4y -- strengthens the decline                  STAYS DECLINED
Google Colab  n/a                wrong shape (ephemeral fs); unchanged                STAYS DECLINED

Nothing on the decline list is re-priced by this report. Three currency facts are
recorded (doorstop alive, sphinx-needs still sphinx-bound, pyadr cold) so the next
reader inherits the check instead of repeating it.
```

---

## §4 · Why the verdict is an amendment and not a new system

This is the finding that shrinks the answer, and it deserves to be stated plainly: **[#552] already
specifies four of the five gap requirements.** Its leg (b), verbatim:

> **(b) The proposer:** a section folded into the existing Tier-1 Stop hook (`propose_closures.py`,
> already detect-and-propose and never-mutating) naming undispositioned new audits, discharged
> ACCEPTED intakes with a drafted `consumed-by:` line, deferrals whose `trigger:` id has departed,
> and ADR-98 §6 survival-metric breaches.

That is G1 (discharged ACCEPTED intakes), G2 (survival-metric breaches), G3-partial (undispositioned
audits) and G4 (departed triggers) — **all four, already filed, already sized, already
`serialize-group: audit-py`**. An operator asking three times for "a system" has, in fact, already
approved most of one.

**Three things [#552] does not carry, and they are exactly what the gap needs:**

1. **Enforcement tier.** Leg (b) is a *proposer* at a Stop hook. Leg (a) — the `archival_residency`
   check, the only *gate* in the row — is scoped to **status-versus-location residency** (a terminal
   doc outside its `archive/`). Intake #31 and #32 are `ACCEPTED / active` and in the right location,
   so they FAIL nothing under [#552] as written, forever.
2. **Age arithmetic.** "ADR-98 §6 survival-metric breaches" cites a horizon whose canonical text is
   the unquantified word **"~1 month"**. No row pins it to a number, and §2 G2 shows the only honest
   clock (filename origin date) is not the obvious one (git add-date), which a proposer written
   without that finding would get wrong and stay green.
3. **Durable view.** Leg (b)'s stated consumption path is `logs/PROPOSALS-ARCHIVAL.md`, and
   `logs/PROPOSALS-*.md` is `.gitignore:26` with 0 tracked files. The answer is computed and then
   discarded.

**Corollary, stated so it is not read as a duplicate proposal: my L3 (trigger resolvability) IS
[#552] leg (b)'s third clause.** I am not filing it again. What I propose is that it be a **Finding**
rather than a proposal — on the evidence that all 3 instances have now survived a full window as
proposals without being acted on.

---

## §5 · VERDICT — the smallest composed instrument

```
INSTRUMENT NAME:  the decision-carrier ledger

  Part A -- schema/data      pin the horizon + land the audit status enum     ~0 new code
  Part B -- one audit check  check_decision_carriers (audit_checks/)         ~180 lines
  Part C -- one view         ecosystem/lifecycle-ledger.md + freshness gate  ~180 lines

  new production code ~360 lines · with tests ~570 lines
  new dependencies     ZERO       · new hooks 1 (owed by precedent, not by choice)
  births 1 row · amendments 2
```

### Part A — schema/data, ~0 new code

1. **Pin ADR-98 §6's "~1 month" to `30` days** at its canonical home (`docs/intake/README.md` §7,
   with ADR-98 §6 unedited — it is immutable). A horizon a program cannot evaluate is not a horizon;
   this is the same reasoning `STANDING_RULINGS` I-D6 already applied to the WIP ceiling ("a ceiling
   that cannot be evaluated is not a ceiling"), and that entry's own expiry reads *"retires when a
   mechanism computes the working set and compares it to this number"* — the precedent is exact.
2. **Land [#551] unchanged** — `status: LIVE | CONSUMED | SUPERSEDED` on `docs/audits/*.md`, written
   by the disposition ledger, moving no file (ADR-100). Part C's audit rows read it. **No new row.**
3. **No new frontmatter key on any corpus.** G1 is served by making the *existing* `consumers:` key
   resolvable — the README already calls it "planned/forward consumers, legal at any status" — by
   admitting a closed token grammar `#<id>` | `ADR-<n>` | `none — <reason>`. A grammar on a ratified
   key, not a schema addition. This is the distillate's own "copy the schema, not the tool".

### Part B — one audit check, ~180 lines

`scripts/audit_checks/check_decision_carriers.py`, registered in `audit_checks/registry.py`
(3 lines). **Automatically carried by the already-armed `audit-health` pre-commit gate and the
`ship-gate` Finding contract — zero new wiring.** Four legs:

| leg | predicate | tier | live count today |
|---|---|---|---|
| L1 carrier resolution | live-status intake whose `consumers:` names no live `#id`/`ADR-n` and carries no `none — <reason>` | **WARN** | 20 of 34 |
| L2 rent-rule age | the same doc past 30 days by **filename origin date** | **FAIL** | 7 |
| L3 trigger liveness | `disposition: deferred` whose `trigger:` names a departed `#id` | **FAIL** | 3 of 3 |
| L4 self-refuting state | `disposition: active` with zero resolving carrier | **FAIL** | 2 (#31, #32) |

Constraints the implementation must obey, each with a named source:
- **Import** the liveness predicate from `preflight_contract`, as `check_preflight_backlog_ids`
  does — "so the tool and this leg cannot drift into disagreeing about what an assertion is".
- **One Finding per document**, never a bundle — the disposition-register whole-Finding contract
  ("else one matched token would wave through unrelated drift").
- **Docstring states the inherited honest limit**: presence and liveness of a carrier citation, not
  that the carrier is doing the work.
- **Docstring states the clock finding**: git add-date is unusable (32 of 34 read `2026-08-11`);
  the predicate is the README-ruled filename origin date.
- **L1 is WARN, not FAIL**, on the `check_preflight_backlog_ids` R3 precedent: a 20-of-34 day-one
  firing rate wired as FAIL REDs every commit by construction. L2/L3/L4 fire on 7/3/2 and are
  affordable as FAIL immediately.

### Part C — one view, ~180 lines

`scripts/gen_lifecycle_ledger.py` → **`ecosystem/lifecycle-ledger.md`**, plus a
`lifecycle-ledger-freshness` pre-commit hook (6 config lines).

**Home is `ecosystem/`, not `docs/`, and the precedent is exact**: `ecosystem/organ-index.md` was
relocated there by operator ruling K-1 of 2026-08-11 precisely because generated ecosystem state is
not one of the five `docs/` genres. This is the same class, so Rule C passes and no taxonomy question
is opened.

One row per decision carrier across all four corpora: `kind · id · status · age · carrier · verdict`.
Fourth instance of a pattern with three live precedents (`organ-index-freshness`,
`audit-index-freshness`, `intake-index-freshness`) — so the freshness hook is **owed by precedent**,
not an invention: three existing rows already name silent index rot as the failure class.

This is what replaces the gitignored `logs/PROPOSALS-ARCHIVAL.md` as G5's durable surface, and it is
the artifact that makes the operator's question answerable by `cat` instead of by a lane.

---

## §6 · Row drafts

### ROW DRAFT 1 — the only birth

```
- [#NNN] [P2][M] **Decision-carrier ledger — one generated view of what is unowned, and how old**
  — the durable half of the lifecycle instrument. [#552] leg (b) computes the four unowned-decision
  classes at session end and routes them to `logs/PROPOSALS-ARCHIVAL.md`, which is `.gitignore:26`
  with **zero tracked files** — so the answer to "which decision is rotting" is computed and then
  discarded with the container. This row builds the committed surface: `ecosystem/lifecycle-ledger.md`,
  generated by `scripts/gen_lifecycle_ledger.py`, one row per decision carrier across
  `docs/intake/` × `docs/decisions/` × `docs/audits/` × `tasks/` with columns
  kind · id · status · age · carrier · verdict, gated by a `lifecycle-ledger-freshness` regen-and-diff
  hook. **Home is `ecosystem/`, not `docs/`** — the `ecosystem/organ-index.md` precedent (operator
  ruling K-1, 2026-08-11: generated ecosystem state is none of the five `docs/` genres), so ADR-101
  Rule C passes and no taxonomy question is opened. **Fourth instance of a three-precedent pattern**
  (`organ-index-freshness`, `audit-index-freshness`, `intake-index-freshness`); the freshness hook is
  owed by that precedent, not invented here. Reads only fields that exist or are landed by [#551] —
  this row adds **no frontmatter key to any corpus**. Measured motivation, live 2026-08-17: 20 of 34
  live intakes cite zero live task, 7 breach the 30-day horizon, and the survival metric has fired
  **once ever** (intake #10, by hand, STANDING_RULINGS I-D7). Optional zero-dep adjacency, offered not
  required: `--emit-sqlite` into the existing gitignored `logs/` store via stdlib `sqlite3` for
  ad-hoc SQL (~15 lines; the `telemetry_emit.py` posture, never committed).
  · Done when: `ecosystem/lifecycle-ledger.md` is generated and hook-gated, carries one row per live
  decision carrier across the four corpora with age computed from each doc's own origin date, the
  20/7/3/2 live figures are re-derived at close rather than carried from this row, and a test asserts
  the generator is deterministic and its `--check` reds on a hand-edit
  · footprint: `scripts/gen_lifecycle_ledger.py`, `ecosystem/lifecycle-ledger.md`,
  `.pre-commit-config.yaml`, `tests/test_gen_lifecycle_ledger.py`
  · refs #552, #551, #548, #549, #550, #555, ADR-98, ADR-100, ADR-101, ADR-107,
  docs/audits/2026-08-17-technical-nb7-lifecycle-instrument-verdict.md
  · kill-candidates: none — [#552] owns the DETECTION legs (this row consumes them and adds no
  detector), [#551] owns the audit `status:` field this reads, [#269] owns the audit-index shape;
  no open row owns a committed cross-corpus lifecycle view
  · serialize-group: audit-py
  · source: docs/audits/2026-08-17-technical-nb7-lifecycle-instrument-verdict.md §5 Part C
```

### AMENDMENT 1 — to [#552] (no birth)

```
[#552] gains leg (c) and a pinned horizon. Rationale: legs (a)+(b) as written cannot fail on the
live corpus's actual defect. Leg (a) is scoped to status-versus-location residency, and intake #31
and #32 are `ACCEPTED / disposition: active` sitting in the correct location with ZERO resolving
carrier — a self-refuting frontmatter state that passes every gate forever. Leg (b) is a proposer.

  (c) `check_decision_carriers` in `scripts/audit_checks/` (therefore already carried by the
      `audit-health` gate), four legs: L1 carrier resolution WARN (20 of 34 live) · L2 rent-rule
      age FAIL past 30 days (7 live) · L3 trigger liveness FAIL (3 of 3 live) · L4 `disposition:
      active` with no carrier FAIL (2 live). L1 is WARN on the `check_preflight_backlog_ids` R3
      precedent — a 20-of-34 day-one rate wired as FAIL REDs every commit by construction.
      Imports the liveness predicate from `preflight_contract`; one Finding per document.

  Horizon pinned: ADR-98 §6's "~1 month" becomes 30 days at `docs/intake/README.md` §7 (ADR-98
  itself is immutable and unedited). STANDING_RULINGS I-D6 precedent: "a ceiling that cannot be
  evaluated is not a ceiling", and its own expiry reads "retires when a mechanism computes … and
  compares it to this number".

  CLOCK FINDING to encode rather than rediscover: git add-date is UNUSABLE — `--diff-filter=A`
  returns 2026-08-11 for 32 of 34 intake docs, so an add-date predicate reads every breach as 6
  days old and stays green. The honest clock is the README §4 filename origin date.

  PARSER FINDING: the row records three coexisting ADR status-line formats; the live corpus has
  FIVE (`- **Status:** X`, `**Status:** X`, `Status: X`, `- **Status:** X — <date>`, ADR-61
  frontmatter). Write the parser against five.

  L3 is NOT a new detection — it is leg (b)'s third clause promoted from proposal to Finding, on
  the evidence that all 3 instances survived a full window as proposals unacted.
```

### AMENDMENT 2 — to [#551] (no birth, no change to the row)

```
[#551] is unchanged and correct as filed. It is named here as the audit-corpus half of Part A:
Part C's audit rows READ the `status: LIVE | CONSUMED | SUPERSEDED` field [#551] lands, and the
ADR-100 no-move invariant is untouched by anything in this report. One currency correction for
the row's implementer, measured live: 25 of 574 audit files ALREADY carry an ad-hoc off-schema
`status:` (`complete`, `resolved`, `for-operator-review`, `snapshot (Phase A input…)`, `DRAFT`,
`open`), so the deploy is a MIGRATION of 25 off-enum values plus a fill of 549, not a greenfield
add — the same migrate-never-grandfather discipline the [#398] intake enum deploy used.
```

---

## §7 · Rejected alternatives — one line each

```
sphinx-needs 8.3.1        STAYS DEAD -- still requires sphinx>=7.4,<10 at the current release; no new evidence named.
StrictDoc 0.28.0          STAYS DEAD -- own SDoc DSL; same distillate decline, reason unchanged.
doorstop 3.2              STAYS DECLINED -- alive (2026-07-10) but imposes its own YAML item store, pulls 10 deps incl. the already-DISQUALIFIED python-frontmatter, and LGPLv3.
Log4brains                STAYS DECLINED -- Node/Next.js bring-in for a static site the repo does not need.
pyadr 0.19.0              REJECT -- cold 4.4 years (last release 2022-04-05); "plain frontmatter" is the surviving half of that decline.
check-jsonschema 0.38.0   REJECT as the mechanism -- cannot read markdown frontmatter, and cross-file resolution plus date math are not JSON Schema predicates; its item-35 candidacy for deploy/manifest-v*.yaml is unchanged.
committed sqlite + datasette-lite  REJECT -- lite needs an HTTP+CORS host and the repo is private on Free tier; a binary .db is undiffable and Rule C refuses a new home; telemetry_emit.py already rules sqlite stores gitignored under logs/.
git trailers (Closes:/Decision-Ref:)  REJECT for this gap -- a trailer annotates a commit, and the gap is an ABSENCE of work, so there is no commit to annotate; 0 Closes: trailers over 52 first-parent commits.
footprint: as the carrier field  REJECT -- receding surface: 3 of 194 open rows (1.5%), down from the distillate's 5 of 196, because three carriers closed and nothing adopted it.
a new frontmatter key    REJECT -- consumers: already exists and is "legal at any status"; a grammar on a ratified key beats a schema addition.
a new `decisions` genre / new top-level home  REJECT -- ADR-101 Rule A/C seal the taxonomy; ecosystem/organ-index.md is the exact precedent for generated ecosystem state.
a second registry (fleet-exceptions.yml style)  REJECT here -- intake #38 R19's own kill-candidate note already proposes the disposition register gain expiresOn rather than a second registry being born.
```

---

## §8 · Honest limits of this verdict

1. **Part B's L1 fires on 20 of 34 documents on day one.** That is a large advisory surface, and the
   `check_preflight_backlog_ids` R3 precedent exists precisely because a leg wired as FAIL at that
   rate REDs every commit. WARN is the correct tier and promotion needs measured evidence — but a WARN
   that nobody clears is how the `[stale]` disposition class in [#557] came about. **The ledger view
   (Part C) is what makes the WARN survivable**, and if Part C is descoped, Part B's L1 should be
   descoped with it rather than shipped alone.
2. **Nothing here closes the ADR corpus's terminal-status gap.** 83 Accepted / 0 Superseded / 0
   Deprecated with an archival bar keyed on values nothing writes is [#242]'s status half and
   [#362]'s substantive half. Part B reads ADR status; it does not re-disposition 85 ADRs, and this
   report makes no claim to.
3. **Carrier presence is not carrier progress.** A row that cites intake #31 and does nothing
   satisfies L1. This is `check_preflight_backlog_ids`'s stated limit inherited unchanged, and it is
   the reason G1 is worth only what it costs — a cheap liveness floor, not an ownership guarantee.
4. **The 30-day pin is a judgment, not a measurement.** ADR-98 §6 says "~1 month"; 30 is the nearest
   evaluable number and matches the `doc_rot` A1 calendar backstop already in `PLAYBOOK.md:1095`.
   A different number is defensible; an unevaluable word is not.
5. **I did not run the test suite, and the gate mesh was not executable in this lane's container.**
   No claim in this report depends on a test result; every count in §1–§3 was measured live with the
   command shape stated inline. But the environment condition is worth recording because **it is a
   verbatim recurrence of a filed defect**, and it recurred on a cloud lane exactly as adoption-ledger
   item 36 predicts. Measured here 2026-08-17: `uv` is **0.8.17** against the ADR-106 `==0.11.19` pin
   (so `uv sync --locked` refuses), `.git/hooks/` carries samples only, and `audit.py health` reports
   **`DEGRADED` before this lane touched anything** — the identical pairing item 36 records for
   2026-08-09 ("all five night lanes ran with NO executable gate mesh (uv 0.8.17 against the ADR-106
   ==0.11.19 pin; .git/hooks/ samples only)"). Two further confirmations from the same run: the clone
   is **shallow** (`.git/shallow` present, 307 commits), so `journal_spine_anchor` cannot resolve its
   disposition floor `24882f8cc` and fails closed per ADR-85 §A6 — correct behaviour, not a defect —
   and `canonical_freshness` reports **exactly 5** stale files, every one reading `last edit
   2026-08-11` (the graft boundary). That is **[#501]'s own documented failure mode reproduced to the
   count**: "shallow grafts read as whole-file creations — 5 false `canonical_freshness` FAILs". The
   gates this lane could run natively did pass: `validate_hermetization` clean on the added file,
   `gen_audit_index --check` clean after regeneration, `task_tree_coherence`, `intake_tree_coherence`
   and `preflight_backlog_ids` all OK. Nothing in this lane's own diff appears in any finding.
6. **`docs/intake/README.md` §5's manual-move clause stays manual.** "The move is MANUAL for now —
   the status-coupled validator that would gate/automate it is wave work, not built" (`:207`). Part B
   reads status; it moves no file, and [#552] leg (a) remains the row that owns residency.

---

## §9 · Amendment 2026-08-17 (same session, appended per CLAUDE.md §5 rule 3 — the text above stands as written)

**A fourth organ was silenced by the uv pin, and it was this lane's own session-end gate.** §8 item 5
listed the pre-commit mesh and `audit.py health`; the list was incomplete, and the missing entry
arrived after the report was committed. At Stop, the ADR-85 backpressure hook fired and could not run:

```
[uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"]:
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

This matters beyond one more instance, for two reasons.

1. **It is the class adoption-ledger item 36 already annotates, witnessed a further time on the cloud
   channel.** That annotation records "THREE organs silenced by the uv pin, **the third an unbidden
   fail-open Stop hook**". This is that third class, recurring — and the recurrence is now on a
   *remote* channel rather than the operator's host, which is the surface intake #32 and [#501] both
   reason about.
2. **It sharpens ADR-85 §A5's own argument rather than contradicting it.** §A5 retired the Stop hook's
   hard leg on the reasoning that "an organ that can be exhausted cannot carry teeth". The evidence
   here is adjacent and worse: on this channel the organ cannot *start*. An advisory organ that fails
   loudly is behaving correctly — it printed rather than passing silently — but the ADR-106 pin means
   the cloud channel has no session-end surfacing at all, which is a coverage fact the ARCHITECTURE
   Ch2 failure-posture table does not currently state.

**What this leaves owed, stated precisely so nothing is assumed discharged:**

- **Nothing was bypassed.** `scripts/block_unanchored_push.py:20` is explicit — "A push that does not
  target `main` is not this organ's business" — and this lane pushed to
  `claude/nb7-instrument-verdict-8yw1a2`. The ADR-85 hard leg never applied.
- **The JOURNAL anchor is owed at merge, not here.** Discharge is range-level, so it is the
  integrator's act at the `--no-ff` merge to `main`, on the same lane precedent `CLAUDE.md` §12 v2.57
  and v2.60 record for owed roster rows: a lane keeps its footprint out of a high-collision living
  file, and the debt is paid at the merge — the point at which the spine entry it anchors exists.
  This lane deliberately writes no `JOURNAL.md` entry.
- **Working tree is clean** (`git status --short` empty), satisfying `.claude/rules/git-discipline.md`.

No claim in §0–§8 changes. This amendment adds one witness and one owed-item statement.

---

**Final metric line —** gap requirements **5** · existing machinery **17 organs** · verdict instrument
**the decision-carrier ledger** = Part A pinned horizon + [#551]'s audit `status:` (~0 new code) ·
Part B `check_decision_carriers` (4 legs, ~180 lines) · Part C `ecosystem/lifecycle-ledger.md` +
freshness gate (~180 lines) · new-code estimate **~360 lines production / ~570 with tests** · new
dependencies **0** · births **1 row**, amendments **2** · declines re-verified **6**, re-priced **0**.
