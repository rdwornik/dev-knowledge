# Seeded-defect substrate inventory — the A/B method template, the real historical instances, and the two gap lists

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** seeded-defect-substrate-inventory
- **What this is:** the read-only precursor to the `[#491]`/`[#492]` provider bake-off. `[#492]` names
  four defect classes as prose only, with no persisted corpus and no seeding harness — so the row's
  own rule (*"Entry by measured acceptance, never vibes"*) currently has no substrate to measure on.
  This document **builds no corpus**. It inventories what already exists so the corpus row can be
  born at batch-4 GO with an evidence-backed shape and an operator-approved path.
- **Status:** RETRIEVAL + LIVE PROBE ONLY — **zero rows born, zero rows closed, zero directories
  created, zero defects seeded, zero provider lanes run.** No path is invented anywhere in §3.
- **Source-session:** hub sandbox worktree `lane-seeded-defect-substrate`, branch
  `worktree-lane-seeded-defect-substrate`, base `3ed60c4c`.
- **Topology:** one Opus orchestrator + four haiku retrieval subagents (one per defect class),
  parallel. Every SHA a subagent returned was re-resolved against `git log` by the orchestrator
  before landing here; one was wrong and is corrected in place (§2.4 note).
- **Consumer:** the batch-4 seat that decides whether the corpus row is born, and in what shape.

---

## 1. Method template — what the 2026-07-31 Grok/Terra shadow A/B actually did

Source: `docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md`. Quoted, not paraphrased.

### 1.1 The decisive question the recon flagged `unknown`: seeded or natural?

**ANSWERED — the A/B used a NATURAL diff. It seeded nothing.** The artifact names its subject diff
directly (`:5-6`):

> Subject diff: the W2 schema build (`71ba8f1a`+`2ee3376d`, reviewed pre-fix). Both reviewers saw
> the SAME diff.

This is real in-flight work reviewed before its own fix landed — not a constructed defect set. There
is no ground-truth defect list anywhere in the artifact, and no statement that any defect was
introduced deliberately. **The `unknown` is now closed: the prior A/B is not a precedent for
seeding.** It is a precedent for *same-diff parallel review*, which is a different instrument.

That distinction is the single most consequential finding in this document, and §3.3 turns on it.

### 1.2 The lanes and the cost leg (`:7-10`, `:32-34`)

> **Lanes:** terra = `codex-review.ps1` (codex-cli 0.145.0, code profile) →
> `docs/audits/2026-07-31-codex-382-w2-schema-v1.md`. grok = grok CLI 0.2.102
> (`--always-approve --max-turns 20 -p`, headless), wall **335s**, raw output preserved
> verbatim below the rule.

> **Cost:** grok wall 335s; terra wall ~4min (same order). **Neither CLI exposes token
> pricing — the cost leg of the §C criterion is INCONCLUSIVE on hard numbers** and is
> recorded as wall-clock-comparable, not "cheaper".

### 1.3 How findings were tallied (`:14-27`)

Severity volume, per lane:

> **Volume:** terra 1 Critical + 7 High (0 M/L). grok 2 Critical + 5 High + 9 Medium + 5 Low
> + a per-constraint coverage table.

Then three separate comparisons — **unique catches per lane, overlap, and factual accuracy**:

> **Unique load-breaking catches (grok only):** C1 — `RefKind` missing the live `audit`
> provenance kind (verified on disk; would refuse real parity rows at load) and C2 — four
> Surface sparse fields are dict-shaped on disk […] where the schema held scalars. grok actually READ
> `parity-surfaces.yaml`; terra reasoned from the diff + ADR. Both accepted and fixed (`1b964e4e`).

> **Unique architectural catch (terra only):** the CRITICAL root under-build (missing D1/D3
> component layer + composition) — grok found it too but ranked it High.

> **Overlap:** enforcement-vocabulary drift (terra H7 ≡ grok H4), component layer
> (terra C ≡ grok H1) — independent convergence on both.

> **Accuracy:** terra 0 factual errors; grok 1 factual overstatement ("81/81 surfaces use
> `kind: audit`" — actual: 1 occurrence; the drift itself was real) and some cosmetic Lows.

### 1.4 How acceptance rates were computed (`:28-31`)

> **Acceptance rate after triage:** terra 6.5/8 accepted (H2 partial, H5 partial-rejected on
> an ADR-recorded open point). grok ~17/21 accepted (L1/L2/L4 dispositioned, C1 count
> corrected). grok's Mediums were high-yield: M6 (dangling `gate_rev_ahead` reference = silent
> payload loss) became a root validator; M9 became the live enum↔disk exhaustiveness lock.

**Read the denominator carefully.** It is *the lane's own finding count*, not a known defect
population. `6.5/8` means "of the 8 things terra raised, 6.5 survived human triage" — a **precision**
measure. Nothing in this method measures **recall**, because with a natural diff nobody knows what
the full defect set was. Half-points are used for partial acceptance.

### 1.5 The recorded verdict (`:35-39`)

> **Verdict (recommendation, operator rules):** the two lanes are COMPLEMENTARY, not
> redundant — grok verified against live disk state, terra against spec fidelity. Keep the
> grok shadow on foundational diffs. The operator's "cheaper-and-possibly-better" hypothesis:
> *better-in-part witnessed* (2 unique load-breaking catches), *cheaper unproven* (no price
> surface).

The artifact also records its own unrun debt (`:50-57`), including that **"the grok lane ran ad-hoc
(hand-built prompt, no wrapper) — a `grok-review` wrapper symmetric to `codex-review.ps1` would make
the shadow repeatable + comparable."** That is a live input to §3.2.

---

## 2. Historical instance inventory — real fleet defects, per class

Every SHA below was re-resolved against `git log` in this worktree. Instances are the raw material a
corpus would be built *from*; nothing here has been extracted, copied, or staged into a corpus.

### 2.1 Vacuous test — 7 landed instances, plus 1 documented near-miss

| # | Defect as it appeared | Present at | Fixed by |
|---|---|---|---|
| V1 | `tests/test_adr85_integration_enforcement.py` T6 asserted `git push --no-verify` bypassed the pre-push organ, but **never installed the hook** — the push would have succeeded whether or not the organ did anything | `8543841f` | `e44d9737` |
| V2 | `tests/test_normalize_headers.py` asserted headings using `_heading_lines`, **the same helper the code under test uses** — tautological; and made **zero assertions** if no corpus file changed | `75fce455` | `98d973d0` |
| V3 | `tests/test_boundary_headers.py` case-sensitivity test was a real RED on Windows but a **vacuous pass on Linux/macOS** (`fnmatch` already case-sensitive) — CI could green with the bug fully restored | `4e2c809b` | `98d973d0` |
| V4 | `detect_unconditionally_inert_checks()` was **called only by tests**; `run`/`health`/`ship-gate` bypassed it — the detector had no production effect | `f020e0b9` | `7ead2cd3` |
| V5 | `tests/test_writer_integrity.py` filtered for `"INERT"` and **passed even when the live roster emitted `writer_integrity` warnings** | `f020e0b9` | `7ead2cd3` |
| V6 | `audit.py` checks `handoff_tag_canonicity` + `floor_integrity` **asserted nothing about live hub state yet returned `pass`**, inflating the self-audit pass-count | pre-`c39634c4` | `c39634c4` |
| V7 | `scripts/validate_scope_tags.py` no-args fallback **passed without scanning any file** | pre-`446abbef` | `446abbef` |

**Near-miss, recorded because the arc itself is about mechanisms that measure nothing** — the obvious
regression test for the `shutil.rmtree` `onerror`→`onexc` swap would have been `assert no
DeprecationWarning`; on CPython 3.12 the deprecation lives in the *docstring* and emits no runtime
warning, so that assertion **passes identically before and after the fix**. Caught before landing and
replaced with kwarg-distinguishing tests (`546d583b`).

> **Honest correction to the retrieval leg:** the vacuous-test hunt returned 10 items. Two are
> re-filed rather than counted here — one is a fail-open handler (now F7) and one is a same-day
> state-comparison bug in `audit.py:456` that is a correctness defect, not a vacuous test. Counting
> them under this class would have inflated it.

### 2.2 Fail-open `except` — 7 instances

The densest and best-evidenced class. Six of seven sit in the ADR-85 enforcement organs.

| # | Defect as it appeared | Present at | Fixed by |
|---|---|---|---|
| F1 | `block_ff_push.main()` — the flagship, quoted verbatim below | `94652fdf` | `8543841f` (§A6) |
| F2 | `block_ff_push._read_stdin()` — `except (OSError, ValueError): return ""`, and `""` resolves to *"not a push to main"* → exit 0 | `94652fdf` | `e44d9737` |
| F3 | `block_ff_push.violations_in_range()` delegated to a detector whose **documented contract returns `[]` on any git error** — a failed scan is indistinguishable from a clean tree | `94652fdf` | `e44d9737` |
| F4 | `session_end_backpressure.main()` — `except Exception: return 0`, silently indistinguishable from a clean run | `dfbb5853` | `8543841f` |
| F5 | `block_unanchored_push` returned 0 when pre-commit forwarded only one ref pair, **skipping main's range entirely** | `8543841f` | `e44d9737` |
| F6 | `journal_anchor` floor lookup used `.search()` — with a duplicate or malformed floor line beside a valid one, an **ambiguous boundary silently changed which history was exempted** | `8543841f` | `e44d9737` |
| F7 | `scripts/normalize_headers.py:100` — `except Exception` returned the original text unlogged, so a rewriting gate **silently no-opped while reporting success** | `75fce455` | `98d973d0` |

F1, recovered verbatim from `git show 94652fdf:scripts/block_ff_push.py` — this is the exact shape
`CLAUDE.md` §9 records as having *"silently auto-allowed the exact push it exists to refuse"*:

```python
        return 0  # not a push to main (or a main deletion) — nothing to gate
    violations = violations_in_range(_repo_root(), rng)
except Exception as exc:  # noqa: BLE001 — fail-soft is the contract
    print(f"block_ff_push: degraded ({exc}) — allowing push", file=sys.stderr)
    return 0
```

The comment `# fail-soft is the contract` is worth preserving in any corpus: **the defect was written
deliberately, with a stated rationale.** This class does not look like a mistake in situ, which is
precisely what makes it a good discriminator between review lanes.

### 2.3 Stale locator — 9 instances (8 historical + 1 self-witnessed today)

| # | Defect as it appeared | Present at | Fixed by |
|---|---|---|---|
| S1 | `CLAUDE.md` §4 said **"three"** machine-produced lane prefixes while `validate_branch_naming.py` already accepted **four** — the canonical boot file contradicted its own validator for one night | `3879d28b` | `c358d95c` |
| S2 | Eight sites (CONTRIBUTING ×6, DEFINITION_OF_DONE ×1, `override.md` ×1) described paths ADR-85 §A2 had **retired underneath them** | pre-`59b191c5` | `59b191c5` |
| S3 | `CLAUDE.md` §7 called `/override` *"the gate's only escape"* after the amendment retired that path | pre-`e44d9737` | `e44d9737` |
| S4 | `tests/test_reverse_dep_oracle.py` pinned `class Finding` at lines 242/241; `ca83eb13` inserted 5 lines above it, shifting it to 247 | post-`ca83eb13` | `06add3a6` |
| S5 | `ARCHITECTURE.md` Ch6 claimed *"the client-side gate set re-run off-host"* — actually **3 of 17** gates re-run | pre-`d388d0f2` | `d388d0f2` |
| S6 | `enforcement_coverage._seb_fire` probed for a Stop-hook `{"decision":"block"}` that §A5 had deleted — **answered ABSENT for every repo, including those with the hard leg installed** | pre-`0c8647c2` | `0c8647c2` |
| S7 | Seven BACKLOG rows carried stale pointers: unqualified paths, `audit.py:1961`→`:2425`, `HANDOFF_PROCESS.md:502-503`→`:517-518`, a falsified premise, and two dead `[#221]` references | pre-`0c7f04e9` | `0c7f04e9` |
| S8 | Post-ADR-107 flip, six surfaces still described **direct BACKLOG edits** as the closure mechanism after `tasks/` became source-of-truth | pre-`1d9a0096` | `1d9a0096` |
| S9 | **Found by this arc, still live** — see below | `HEAD` | *unfixed* |

**S9, self-witnessed and unrepaired.** `docs/audits/2026-08-08-technical-successor-prep.md:279-281`
cites, verbatim:

> see `docs/audits/2026-08-08-technical-library-research.md` §8 for what the network could and could
> not establish tonight

That file's §8 is *"Sweep of the remaining P-B candidates against tonight's problems"*, and a grep of
the whole file for `grok|4\.6|xAI` returns exactly one line — `| pre_commit | 4.6.1 | 4.6.1 | ✓ |`.
**The citation does not resolve to anything about Grok 4.6.** Recorded as a finding, not fixed:
audits are immutable, and repairing a sibling artifact is outside this contract's Writes section.
Note the recursion — a stale locator inside the very document that catalogued the stale-locator class.

Two structural observations this class supports and the others do not:
- **S1/S2/S3 are one claim rotting across nine sites and taking two arcs to drain.** A corpus entry
  for this class arguably needs to be *multi-site*, or it under-represents the real failure mode.
- **S4 is the only instance a compiler-like tool could catch.** The rest require reading prose
  against live state — which is exactly the axis on which the A/B found grok stronger (§1.3: *"grok
  actually READ `parity-surfaces.yaml`; terra reasoned from the diff + ADR"*).

### 2.4 Fence corruption — 4 instances

| # | Defect as it appeared | Present at | Fixed by |
|---|---|---|---|
| C1 | `mermaid_emit()` returned **bare Mermaid source with no triple-backtick wrapper** — rendered as plain text instead of a diagram | `79788902` | `cf9d5832` |
| C2 | `audit.py` declaration-anchor parser **scanned inside code fences**, so a fenced *example* marker could be accepted as the real declaration; compounded by `\b` after an id, where `-` is not a word character | pre-`d0d58549` | `d0d58549` |
| C3 | `toc/generator.py:parse_headers()` used `startswith("```")` + a boolean toggle. Blind to: `~~~` fences, longer `~~~~` fences, fences indented 1–3 spaces, and a legal 3-backtick line inside a 4-backtick fence — the last **closed the outer fence early and swallowed the document tail** | `0d000282` | `62592646`, then `229c8813` |
| C4 | `normalize_headers.py` `_FENCE = re.compile(r"^```")` + toggle, same four blind spots — and this hook **rewrites files in place**, so every false negative silently edited committed content | `451e07d1` | `75fce455` |

> **Correction applied.** The retrieval leg returned `799789025` for C1's introducing commit. That
> SHA does not resolve (`fatal: ambiguous argument`); the real one is `79788902`, recovered via
> `git log --diff-filter=A -- scripts/codemap/mermaid_emit.py`. Transposed digits. Flagged here
> because it is the one fabricated-looking locator in 26 and the reason every SHA was re-resolved.

**C3 and C4 are the same defect in two organs**, fixed the same day by the same technique (hand-rolled
toggle → `markdown_it` tokens). C4 is the more severe: a *rewriting* hook with a broken fence detector
corrupts content rather than merely mis-reporting it.

### 2.5 Cross-class chain — an independent cross-validation

The two hunts ran blind to each other and their outputs interlock at `75fce455`:

`451e07d1` ships the fence bug (C4) → `75fce455` fixes it, and in the same commit ships **both** a
vacuous test (V2) **and** a fail-open handler (F7) → `98d973d0` fixes those two.

Two subagents, given different class definitions, independently landed on the same commit in
complementary roles. That is corroboration, not duplication — and it is also the substrate's most
useful specimen: **one real commit carrying three of the four classes at once.**

### 2.6 Tally

| Class | Landed instances | Density |
|---|---|---|
| Vacuous test | 7 (+1 near-miss) | concentrated in test files, 2026-08-03/04 |
| Fail-open `except` | 7 | 6 of 7 in ADR-85 enforcement organs |
| Stale locator | 9 (8 fixed, 1 live) | spread across docs, tests, probes, BACKLOG |
| Fence corruption | 4 | 2 pairs, each one defect in two organs |
| **Total** | **27** | all four classes have real instances |

**No class returned "none found."** The `[#492]` prose picked four classes this fleet genuinely
produces.

---

## 3. What a corpus would need — requirements only

**Shape only.** No path is proposed, no directory named, no file created. Each item below is a
*requirement or an open question* for the operator to rule on at batch-4 GO.

### 3.1 Artifacts

- **R1 — Provenance is mandatory per entry.** Every entry carries its introducing SHA, its fixing
  SHA, and the file it lived in. §2 shows why: one in 26 locators came back wrong, and only
  re-resolution caught it. A corpus without verifiable provenance inherits that error rate.
- **R2 — The form question is open, and it is the first ruling needed.** Three candidate forms, each
  with a different cost: *(a)* pointers-only (SHA pairs, zero new content, but the harness must
  reconstruct each defect); *(b)* extracted patches (self-contained, but duplicates content the
  ADR-29/immutability posture keeps in git); *(c)* a manifest indexing *(a)* with metadata. **Not
  ruled here.** Note that *(b)* is the only form that creates a new content class, which is the one
  that would engage ADR-101's tree-seal gate.
- **R3 — Entries must be re-injectable into a diff.** F1 was deleted, not edited; C1 was a missing
  wrapper; S4 was a line-number drift. A single patch format may not cover all four classes, and
  whether it must is an open question.
- **R4 — Multi-site entries must be representable** (§2.3): a stale claim rotting across nine sites
  is the real shape of that class, and a single-file entry would under-represent it.
- **R5 — The severity each defect actually carried should ride the entry**, since `[#492]` already
  binds the lane to *"writes its severity tally into the artifact body"* from day one.

### 3.2 Harness

- **R6 — Repeatability is already a named gap.** The A/B's own debt list records that the grok lane
  *"ran ad-hoc (hand-built prompt, no wrapper)"* and that a wrapper symmetric to `codex-review.ps1`
  *"would make the shadow repeatable + comparable."* A measured comparison needs both lanes invoked
  identically; today only terra has a wrapper. **This is a prerequisite, not a nicety.**
- **R7 — Both lanes must see the same diff, and must not see the fix.** The A/B achieved this by
  reviewing pre-fix (*"Both reviewers saw the SAME diff"*). A seeded harness must reproduce that
  property deliberately rather than by timing.
- **R8 — Contamination is a live hazard unique to seeding.** Every defect in §2 is *already
  described in this repo's own audits, JOURNAL and commit messages* — including this document. A lane
  with repo read access can find the answer key by grep instead of by review. Whether the harness
  isolates the diff from the record, accepts the contamination, or measures it is **unruled and
  material to the result's validity.** This risk did not exist for the natural-diff A/B.
- **R9 — The blind spot must be declared.** A seeded corpus measures only the classes it contains.
  The A/B's most valuable single catch (grok's C1, reading live disk state) belongs to *none* of the
  four classes, and a seeded run would have scored it zero.

### 3.3 Scoring — where the A/B does **not** transfer

This is the sharpest finding in the document. `[#492]` asks to *"compare catch rate against the terra
baseline."* The A/B computed **no catch rate** and could not have: with a natural diff there is no
denominator (§1.4). Its `6.5/8` and `~17/21` are **precision after triage**, not recall.

- **R10 — Seeding inverts the instrument.** A known defect set finally supplies a denominator, so
  *catch rate* (recall) becomes computable for the first time. It is a **new** measure, not a
  continuation of the A/B's.
- **R11 — Precision must be retained alongside it.** A lane that reports every line as defective
  scores 100% recall. The A/B's triage-based precision leg and its **accuracy** leg (*"grok 1 factual
  overstatement"*) are the guards against that, and both must survive into the new method.
- **R12 — "Catch" needs a written predicate before the run.** Terra ranked the root under-build
  Critical where grok ranked it High (§1.3) — same defect, different severity. Whether a
  severity-mismatched catch counts is a scoring rule that must be **fixed ex ante**, or the result is
  adjudicable after the fact.
- **R13 — Unseeded findings need a disposition.** The A/B's whole verdict (*"COMPLEMENTARY, not
  redundant"*) rests on **unique** catches. If a seeded run scores only seeded defects, it structurally
  cannot reproduce the finding that justified keeping both lanes.
- **R14 — Cost stays inconclusive.** *"Neither CLI exposes token pricing"* — unchanged today. Any
  cost claim remains wall-clock-comparable, per the A/B's own recorded limit.

---

## 4. Gap list — `[#492]` Grok lane

Done-when, quoted from `BACKLOG.md:270`:

> the comparison has run on ≥1 real diff set post-4.6 and the lane is admitted or refused on the
> measured result

| Clause | State | Evidence |
|---|---|---|
| "the comparison has run" | **MISSING** | no post-4.6 comparison exists |
| "on ≥1 real diff set" | **PARTIAL** | the 2026-07-31 A/B ran on a real diff — but pre-4.6, and the row calls a 4.5 run *"a burned test"* |
| "post-4.6" | **BLOCKED** | see §4.1 |
| "the lane is admitted or refused" | **MISSING** | no verdict; row is `status: deferred` |
| "on the measured result" | **BLOCKED** | no substrate: no corpus, no seeding harness, no grok wrapper (R6), no scoring predicate (R12) |

### 4.1 Live availability probe — answered, not UNKNOWN

The contract permitted an UNKNOWN here. It is not needed: the question is answerable read-only from
the local CLI, with **no network model call and no inference**.

```
$ grok --version
grok 0.2.102 (ab5ebf69ac) [stable]

$ grok models
You are using XAI_API_KEY.

Default model: grok-4.5

Available models:
  * grok-4.5 (default)
```

*(Key **name** only, per contract; no value was read or echoed. `grok models` is a metadata listing —
"List available models and exit" — not a model invocation.)*

**Three findings:**

1. **No 4.6-class model is served.** The CLI offers exactly one model, `grok-4.5`. The row's peg —
   *"DEFER — peg: ≥ 2026-08-07, the Grok 4.6 release"* — has a date component that has passed
   (today is 2026-08-08) but a **release component that has not been met on this machine**. The
   calendar date alone does not lift the gate; a 4.5 run remains the burned test the row forbids.
2. **The CLI is byte-identical to the one that ran the burned A/B** — `0.2.102`, the exact version
   recorded at `2026-07-31-technical-382-w2-grok-shadow-ab.md:8`. Nothing has moved in nine days.
3. **This supersedes S9.** The successor-prep called 4.6 availability *"an off-repo fact this section
   does not assert"* and pointed at a citation that does not resolve (§2.3 S9). It is assertable
   locally, and now asserted.

**Consequence for batch-4:** `[#492]` cannot close on its own terms today, regardless of how much
substrate gets built. Corpus work is still worth doing — it is the row's genuine critical path and
survives any release date — but the row's *acceptance* is blocked on an external release, not on
this fleet's effort. **A model-availability check belongs at the front of the eval, before corpus
work is commissioned.**

---

## 5. Gap list — `[#491]` Gemini lane

Done-when, quoted from `BACKLOG.md:271`:

> the R-G one-line ruling is recorded and the lane has passed one real-work acceptance run with
> spot-verification evidence

| Clause | State | Evidence |
|---|---|---|
| "the R-G one-line ruling is recorded" | **MISSING** | grep of `protocols/STANDING_RULINGS.md` for `R-G`/`Gemini`/`gemini`: **no match**. Independently re-confirmed here; matches the successor-prep's finding |
| "one real-work acceptance run" | **MISSING** | no run has occurred |
| "with spot-verification evidence" | **MISSING** | no artifact exists |

### 5.1 What that run would be, given what exists today

The row names two candidate workloads. **They are not equally available.**

- **`[#487]`'s ranked sheet — input does not exist.** `[#487]` is open, `[P2][L]`, and was re-scoped
  2026-08-06 to *pipeline-repair-first*: legs (i)–(iv) must land before a sheet is produced. So this
  option is **blocked on another open row**, not merely unstarted.
- **The fleet dependency scan — no locatable definition.** A repo-wide grep for `fleet dependency
  scan` returns three hits: the `[#491]` row itself, its `tasks/` twin, and the successor-prep line
  quoting the row. **The workload is named nowhere but in the row that names it.** Whoever runs this
  must first define what it is — that scoping is unowned work not currently on any row.

### 5.2 What *is* available

- **The CLI is present and current:** `gemini 0.49.0`, on PATH. Not a blocker.
- **`GEMINI_API_KEY` plumbing lives in a different repo** (per recon; not re-probed here — out of
  this contract's read-only hub scope). Key name only; no value read.
- **The binding constraint is already ruled and must ride any contract:** *"retrieval-not-classification
  is baked into every Gemini contract"* — the row records this as **a measured incident, not a style
  preference** (a fan-out leg fabricated an ADR count). This constrains which workload is even
  eligible: a task requiring classification against a doctrine clause is **outside the lane's
  competence by ruling.** Note that a dependency scan is retrieval-shaped and a *ranked* sheet is
  classification-shaped — which is a live tension between the two candidates that the row does not
  resolve.

### 5.3 The asymmetry worth carrying to batch-4

`[#491]` is **open**, not deferred, and **nothing blocks the R-G ruling** — it is one line in
`STANDING_RULINGS.md`, needs no corpus, no harness, and no external release. That is a materially
cheaper first move than anything on `[#492]`, whose acceptance is externally blocked (§4.1). The
acceptance *run* remains blocked on workload definition (§5.1); the *ruling* does not.

Stated as an observation for the operator's dispatch decision. **This document rules nothing and
births nothing.**

---

## 6. SELF-TEST — acceptance contract, re-run before STOP

| # | Contract item | Verdict | Evidence |
|---|---|---|---|
| 1 | A/B method quoted, seeded-vs-natural answered or marked unknown | **PASS** | §1, quoted at `:5-10`, `:14-39`, `:50-57`. **ANSWERED: natural diff** (§1.1) — the recon's `unknown` is closed, not deferred |
| 2 | Each of four classes has an instance list, or an explicit "none found" | **PASS** | §2.1 (7+1), §2.2 (7), §2.3 (9), §2.4 (4) = 27. No class empty |
| 3 | Corpus shape as requirements, zero invented paths, zero directories created | **PASS** | §3 = R1–R14, all requirement- or question-shaped. No path proposed; R2 leaves the form question explicitly open. `git status` shows exactly one new file, no new directory |
| 4 | Both gap lists derived from the rows' own Done-when text, quoted | **PASS** | §4 quotes `BACKLOG.md:270`; §5 quotes `BACKLOG.md:271`; both tabulated clause-by-clause |
| 5 | One commit: report + mandated index regen; tree clean at STOP | **PASS** | this file + `docs/audits/README.md` via `gen_audit_index.py --write`; no `--no-verify` |

**Contract prohibitions — all observed:** no corpus built · no directory created · no defect seeded ·
no provider lane run · no row births · no BACKLOG edits · `[#492]` left `deferred` · no JOURNAL entry
(this is a lane; the integrator anchors) · no network model call · key **names** only, never values ·
no `pre-commit run --all-files`.

**Honest limits of this document:**
- The four hunts were retrieval passes, not exhaustive audits. 27 instances is a **floor, not a
  census** — absence of an instance is not evidence of absence.
- §2 records what artifacts and commit messages *say* the defects were. For F1 and S9 the defect was
  re-read from disk verbatim; the rest rest on the record, which is the same evidence any corpus
  builder would use.
- S9 is reported unfixed. Repairing an immutable sibling artifact is outside this contract.
- §3 is deliberately incomplete where a ruling is owed. R2, R8 and R12 are **open questions, not
  recommendations**, and this document does not prefer an answer to any of them.
