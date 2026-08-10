# Night N3 — ratification pack for the batch-4 GO (intakes #28–#32 + the ARC-2 distillate)

> # DRAFT — status flips happen ONLY in the operator's single ratification batch at the GO
>
> Nothing in this file changes any `status:`, writes any `decided-by:`, edits any intake, births any
> row, or appends to JOURNAL. Every "DRAFT" text below is a **paste-block for the operator's batch**,
> not an applied edit. The banked ruling this pack serves says so in its own words
> (`protocols/STANDING_RULINGS.md:818-820`): *"status/decided-by flip lands ONLY in the single
> ratification batch at the GO with §A, #29–#32 and the distillate."*

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** night-n3-ratification-pack
- **Lane:** night N3, cloud, READ-ONLY. Branch `claude/night-n3-ratification-pack-r2jxj0`.
- **Base:** `origin/main` tip **`5455c2a2a008e0ce8cc1d8ac77d2835cfd767376`** (fetched at lane start;
  `5455c2a` = *"Merge branch 'docs/arc9-lane-census' — ARC-9 queue lane 3"*).
- **Inputs (PARTIAL protocol, as N1):** live texts of `docs/intake/` #28 #29 #30 #31 #32 · the ARC-2
  triage distillate (`docs/audits/2026-08-09-technical-consolidation-report.md` §6) and the reconcile
  packet (`docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` Mandate 3) ·
  `protocols/STANDING_RULINGS.md` §I (the banked #28 §B decision at I-F2) · Lane A's erratum findings.
- **Consumer:** the operator's single ratification batch at the batch-4 GO, and the seat that
  executes it.
- **Gate posture — declared, not claimed.** This container carries `uv 0.8.17` against the ADR-106
  `==0.11.19` pin, `.git/hooks/` holds only samples, and `pre-commit` is not on PATH — so **the hook
  mesh did not execute for this lane**. Per intake #32's own proposed rule, a run that cannot prove
  its gates executed is **untrusted, not green**; re-gate at integration. Exactly what was and was not
  run, so the claim is checkable rather than a shrug:
  - `python scripts/gen_audit_index.py --check` → **exit 0** before writing, index regenerated after,
    `--check` **exit 0** again — so `audit-index-freshness` will not fire on this commit.
  - `python scripts/validate_hermetization.py` (staged) → **exit 0** — the ADR-101 R3/R4 name grammar
    accepts `2026-08-10-technical-night-n3-ratification-pack.md`.
  - `python scripts/audit.py health` → **could not run**: `ModuleNotFoundError: No module named
    'click'`. The `audit-health` pre-commit gate is therefore **unevaluated**, not passed.
  - `pytest`, `ruff`, `pre-commit` → **not available**. Unevaluated, not passed.
  - This is the fifth witness of the class intake #32's attestation rule generalizes (§5.2).

---

## 0. What this pack is, and the two things it deliberately is not

**Is:** one section per ratification item — the live frontmatter and the decision-bearing sections
**quoted** so the GO reads the artifact rather than a summary of it; the amendments owed with their
source locators; DRAFT erratum footnote texts; DRAFT `decided-by` lines; and the ceiling arithmetic
before and after each possible outcome.

**Is not, first:** an adjudication. Four of the five intakes carry no operator decision at all; the
fifth (#28 §B) carries one that is **banked and explicitly not executed**. This pack does not add a
decision, and where the record is silent it says so rather than inferring.

**Is not, second:** a claim that the batch is complete. Two gaps found by the Fable review are
reproduced here because they change what the GO must cover — **#28 §A and intake #32 are dropped from
plan v2's ratify surface** (M4-1, High), and **commission 5's session-continuity half has no in-repo
destination** (M4-2, High). Both are carried into §4 as owed amendments rather than left in a review
nobody re-reads.

### 0.1 The ratification surface, enumerated

| # | Item | Live status | Carries a decision already? | Ratification act |
|---|---|---|---|---|
| 1 | intake **#28 §A** — two-tier adoption bar | DRAFT | **No** | ratify or amend |
| 2 | intake **#28 §B** — hub DONE-manifest v1.0 | DRAFT | **Yes — banked, I-F2** | execute the banked flip **+ 2 amendments** |
| 3 | intake **#29** — multi-model execution, telemetry, distillation | DRAFT | No | ratify or amend (+1 amendment owed) |
| 4 | intake **#30** — verification organ, repeatable execution | DRAFT | No | ratify or amend (+1 amendment owed) |
| 5 | intake **#31** — code-style doctrine | DRAFT | No | ratify or amend |
| 6 | intake **#32** — compute placement / remote execution | DRAFT | No | ratify or amend (+1 erratum owed) |
| 7 | the **ARC-2 triage distillate** | *(no status field — §6 of an immutable audit)* | Partly (10 of 38 adjudicated) | rule the **18 routed items**; no status flip exists to make |

**#28 counts as one document with two independently-ruled halves.** That is a schema problem, not a
presentation choice — see §7.4.

---

## 1. Intake #28 — Skills-tier adoption, the operator's 14, and the hub finish line

**Path:** `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md`

### 1.1 Live frontmatter (quoted, lines 1–6)

```yaml
---
intake-id: 28
status: DRAFT
origin: "Layer-1 architect (outgoing 2026-08-06 window seat), 2026-08-08 — the operator's 14-candidate inspiration list plus the window's reflection round; landed VERBATIM by the frozen contract ARC-file-intakes-28-29 (S-write, zero births)"
note: "Class: functional. Provenance (from the body): operator paste 2026-08-08 (14 candidates); tool facts verified by web research 2026-08-08. Triage rides the batch-4 planning GO as ONE ratification batch with intake #29 (the intake-#27 §C pattern) — this filing DECIDES nothing. …"
---
```

*(the `note:` value is truncated above at the sentence boundary; it continues with the schema-carrier
explanation and the id-verification note, and is quoted in full nowhere in this pack because no
amendment touches it)*

### 1.2 §A — decision-bearing, quoted verbatim (lines 17–23)

> ## §A — Proposed ruling 1: TWO-TIER ADOPTION BAR
>
> The ledger's single bar (full measured-divergence eval) matches LIBRARIES — anything entering code,
> gates, or organs. It over-prices SKILLS/PLUGINS, which are additive, sandboxed, and reversible.
> Proposal:
>
> - **Tier L (libraries/code):** unchanged — measured-divergence eval, ADOPT/REJECT on numbers, §E1
>   gap-week consumption.
> - **Tier S (skills/plugins/commands):** install → 30-minute sandbox try → KEEP or DELETE → one
>   ledger line either way. No eval ceremony, no births. A kept skill that later steers code-impact
>   behavior graduates to Tier L review.
> - Guard: Tier S never touches gates, hooks that block, or `scripts/` — anything that would, is Tier
>   L by definition.

### 1.3 §B — decision-bearing, quoted verbatim (lines 25–27)

> ## §B — Proposed ruling 2: HUB DONE-MANIFEST v1.0 (the finish line "zakończyć .dev-knowledge" currently lacks)
>
> Hub reaches v1.0 when ALL hold (each mechanically checkable or packet-witnessed): (1) W-wave landed
> (intake #25 births closed); (2) closure harvest is a routine organ (≥2 consecutive windows with the
> opened/closed/net line and net ≤ 0); (3) open backlog < 100; (4) satellite onboarding = one command
> from the template; (5) handoff cut < 10 min measured; (6) provider-swap demonstrated once on a real
> lane (Tier: codex-plugin-cc or terminal codex — producer lane, CC verifier); (7) zero standing suite
> REDs without a dispositioned owner; (8) a weekly so-what packet exists. **Reaching v1.0 flips the
> default window class from hub-process to product (satellite backlogs).**

### 1.4 Acceptance criterion, quoted (line 57)

> §A and §B ratified (or amended) at the batch-4 planning GO as one batch; §C verdicts recorded into
> ledger #27 as a cross-referenced amendment; §D items visible in the successor's planning surface.

### 1.5 The banked decision — quoted verbatim from `protocols/STANDING_RULINGS.md` I-F2 (lines 816–820)

> The intake #28 §B half is **DECIDED and banked, not executed.** Recorded verbatim:
>
> > intake #28 §B DECIDED — ratify with two amendments (add zero-mechanically-untestable-Done-when
> > criterion; clause 5 <10 min stays); status/decided-by flip lands ONLY in the single ratification
> > batch at the GO with §A, #29–#32 and the distillate

and the gap it names (`:822-824`):

> So intake #28 carries an operator decision that its own frontmatter does not yet show. That gap is
> deliberate and dated here: the flip is one atomic act at the batch-4 GO, and this arc leaves every
> intake `status:` untouched.

### 1.6 Amendments owed against #28

**A-1 · add a ninth §B criterion: zero mechanically-untestable Done-when.**
Source: `protocols/STANDING_RULINGS.md:818` (the banked ruling, verbatim above).
Evidence the criterion should be written against — **measured two lanes ago and it is not flattering
to a bare "zero"**: `docs/audits/2026-08-10-technical-backlog-testability-census.md` grades all 170
open Done-when clauses **MECHANICAL 75 (44.1%) · PROSE-CONVERTIBLE 72 (42.4%) · PROSE-JUDGMENT 15
(8.8%) · DEFECTIVE 8 (4.7%)**, with the honest headline figures **95 (55.9%) not-testable-as-written**
and **23 (13.5%) neither testable nor convertible**. A criterion reading literally "zero mechanically
untestable" is therefore **95 rows away from true on the day it is written**, and 15 of those are
PROSE-JUDGMENT — which the census's own grading says cannot be converted, only re-authored. The
drafting fork is flagged, not resolved: does the criterion mean *zero* (95 rows of work), *zero
DEFECTIVE* (8 rows), or *zero non-convertible* (23 rows)? The ruling's text does not say and this pack
does not choose.

**A-2 · clause 5 (`handoff cut < 10 min measured`) STAYS.**
Source: `protocols/STANDING_RULINGS.md:818` (same sentence). This is a **negative** amendment — it
records that clause 5 survives the `[#511]` re-scope rather than being softened by it. Its companion
is I-F2's first half (`:812-815`): `[#511]` is re-scoped to the **non-mechanized** cut load precisely
*because* the machinery half is ~4.5 s of a ~30-minute wall clock. Clause 5 is therefore a criterion
about the **non-mechanized** load, and reads as such once `[#511]` is the row behind it.

**A-3 · §A must be on the ratify surface at all.**
Source: `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` M4-1 (High), quoted:

> Closure criterion (2) names "#28 §B, #29, #30, #31 + the ingest distillate"; Phase 2's ratify-line
> bullet names #29/#30/#31 and mentions #32 only as a landed fact in the reconcile parenthesis. …
> #28's own acceptance criterion is "**§A and §B** ratified (or amended) at the batch-4 planning GO as
> one batch" — §A (the two-tier adoption bar, which gates the whole Tier-S try-batch and #28 §C's 14
> verdicts) appears nowhere in plan v2.

Not an amendment to the document — an amendment to the **batch's own enumeration**. Recorded here so
the drop cannot repeat silently a fourth seat running. (M4-1 cites the recorded "#28–#32 … ONE batch"
intent as `JOURNAL.md:562`; **that locator has drifted and the live one is `JOURNAL.md:843`** — see
§9.2.)

### 1.7 DRAFT `decided-by` — #28

```yaml
decided-by: "operator ruling at the batch-4 planning GO, 2026-08-<DD> — §A and §B ratified as one act per this document's own acceptance criterion. §B carries the two amendments banked 2026-08-10 and recorded verbatim at protocols/STANDING_RULINGS.md I-F2 (add the zero-mechanically-untestable-Done-when criterion; clause 5 '<10 min measured' STAYS, read against [#511]'s non-mechanized scope). The §B half was DECIDED 2026-08-10 and deliberately not executed then — this flip is the execution of that banked decision, not a fresh ruling. In-repo carrier for the GO: docs/audits/<the GO's recording artifact>.md"
disposition: active
```

**Schema note, load-bearing:** `docs/intake/README.md` §3 makes `decided-by` **and** `disposition`
REQUIRED at ACCEPTED and forbidden at any other status ("leave absent at any other status"). So the
line above is only writable **paired with** the status flip — it cannot be pre-landed at DRAFT to
de-risk the GO. Intake #25's `decided-by` records the same rule being learned the hard way: *"a bare
status flip parses (the enum in `gen_intake_index.py` accepts it) but is schema-invalid."*

---

## 2. Intake #29 — Multi-model execution flow, session-cost instrumentation, and the distillation engine

**Path:** `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md`

### 2.1 Live frontmatter (quoted, lines 1–6)

```yaml
---
intake-id: 29
status: DRAFT
origin: "Layer-1 architect (outgoing seat), 2026-08-08 — the operator's problem statement on long single-model sessions; landed VERBATIM by the frozen contract ARC-file-intakes-28-29 (S-write, zero births)"
note: "Class: functional. Provenance (from the body): the \"distillation engine\" intent carried NO repo locator until this intake — third instance of the intention-without-locator class; this filing is the F5-style repair. …"
---
```

### 2.2 Decision-bearing scope, quoted verbatim (lines 21–25)

> **S1 · Contract-level routing (zero build):** the lane/arc contract template gains a SUB-AGENT
> ROUTING section — retrieval, reads, greps, doc summarization → haiku sub-agents; bounded specified
> edits + suite/gate runs → sonnet sub-agent; design, judgment, review, integration → the main opus
> thread. Guard: sub-agents never decide against doctrine — they retrieve and execute specs; ambiguity
> routes UP.
>
> **S2 · Versioned agents, adopt-native:** 2–3 repo agents in `.claude/agents/` with explicit
> `model:` — `reader` (haiku, read-only toolset), `mechanic` (sonnet, applies specified diffs, runs
> `uv run --locked pytest -n auto`), `gatekeeper` (sonnet, runs the gate mesh, reports verbatim).
> Referenced from Ch8; CC-native subagent mechanism = the library (library-first discharged by
> construction). Acceptance: one real lane runs with ≥2 sub-agent delegations and its packet reports
> the split.
>
> **S3 · Distillation engine, MEASURE-FIRST:** (a) instrumentation before machinery — per-arc
> phase/time/token logging via hooks (session duration, per-phase wall-clock, model mix), two windows
> of data; (b) only then scope the engine against the measured sink (candidate shapes, to be chosen by
> data: contract-payload distiller · packet condenser · gate-context slimmer); (c) the engine, if
> built, is Tier-L (enters code) with a measured-divergence acceptance target derived from (a).
> Building (c) before (a) is out of scope by this intake's own text.

### 2.3 The bake-off bar — decision-bearing and directly load-bearing on the owed amendment (lines 80–85)

> **The model-comparison bar, which binds any future bake-off:** paired within-task designs, ≥5–10
> repeats per model, distributions with bootstrap confidence intervals, gated on a **private,
> versioned seeded-defect corpus**. Nondeterminism persists at temperature 0; public benchmarks are
> contaminated; the METR RCT found experienced developers were **19% slower** with AI while believing
> they were 20% faster. Consequence for this repo, ruled: the 2026-07-31 single-diff A/B is
> **precedent for method, not an admission instrument**, and **no bake-off runs before the
> seeded-defect corpus exists.**

### 2.4 Acceptance criterion, quoted (line 37)

> S1 ratified and live in the template; S2's acceptance lane demonstrated; S3a producing per-arc
> breakdowns in packets; the "distillation engine" question answerable with numbers by the window
> after next.

### 2.5 Amendment owed against #29 — the seeded-defect corpus spec

**Source locators, three, all pointing the same way:**

1. `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:210` (Mandate 3, commission
   3 row), quoted: *"Fold A is the distillate; **the corpus spec is the genuinely-new delta and
   exists NOWHERE in-repo**"* … *"the seeded-defect corpus design — which gates `[#491]`, `[#492]` and
   the Copilot channel — is lost entirely"*.
2. Same file `:218`: *"the single highest-value un-landed content is the **seeded-defect corpus
   spec** (row 3), which three lanes gate on."*
3. Same file `:339` (recommendation 4): *"the seeded-defect corpus spec (gates #491/#492/Copilot)
   exists nowhere in-repo until the ingest arc lands it — it is the single highest-value un-landed
   artifact."*

**What already exists in-repo, so the amendment is scoped and not re-derived:**
`docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md` is the read-only precursor —
its own header states it *"**builds no corpus**. It inventories what already exists so the corpus row
can be born at batch-4 GO with an evidence-backed shape and an operator-approved path."* So the
amendment owed to #29 is the **spec** (shape, seeding harness, versioning, admission bar), and the
substrate inventory is its input, not its duplicate.

**Honest limit on this amendment:** the corpus *spec* the reconcile packet says is lost lives in
off-repo memo `wf-02c940ef`. This pack cannot reconstruct it and does not try. The amendment #29 owes
is therefore either (a) the spec itself, if the memo is ingested before the GO, or (b) an explicit
**owed-with-owner-and-trigger** line, which is the plan's own never-silent bar (F25-1). Ratifying #29
without one of the two leaves three rows (`[#491]`, `[#492]`, the Copilot channel) gated on an
artifact that has no existence and no owner.

### 2.6 DRAFT `decided-by` — #29

```yaml
decided-by: "operator ruling at the batch-4 planning GO, 2026-08-<DD> — S1/S2/S3 ratified as the measurement-and-routing authority, with the S3a MEASURE-FIRST precondition intact and binding on both folds (§Amendment 2026-08-09). Amended at ratification: the seeded-defect corpus spec — the bake-off gate this document's own §Fold A bar names, and the delta the reconcile packet grades as the highest-value un-landed content (docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:210,218) — is <landed here | owed to <owner> on <trigger>>. Substrate input: docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md. In-repo carrier for the GO: docs/audits/<the GO's recording artifact>.md"
disposition: active
```

---

## 3. Intake #30 — The verification gap, repeatable execution, and the cost of parallelism

**Path:** `docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md`

### 3.1 Live frontmatter (quoted, lines 1–6)

```yaml
---
intake-id: 30
status: DRAFT
origin: "Layer-1 architect (predecessor seat), 2026-08-09 — consolidating the challenge answer `CHALLENGE-ANSWER-2026-08-09`, the operator directives of 2026-08-08/09, and the predecessor review; authored off-repo and filed verbatim by the ARC-3 hygiene close-out"
note: "BODY FILED VERBATIM — zero edits, zero births. The body's own header bullet still reads `intake-id: 30 (PROPOSED — verify next-free before filing)`; that check is now DISCHARGED and the id is 30, held in reserve for this document since intake #32 recorded 30/31 as RESERVED rather than free. The bullet is left unedited because the archival value of a verbatim filing outranks tidying a resolved parenthetical."
---
```

### 3.2 §A — decision-bearing, quoted verbatim (lines 15–19)

> ## §A — Proposed ruling 1: an organ for HALF-LANDED RULINGS (the challenge's central diagnosis)
>
> **Evidence (from the answer, six independent instances found by five lanes that never spoke to each
> other):** `markdown_it` ruled ADOPT, landed at 1 of 3 sites; `yaml.safe_load` ruled ADOPT,
> unimplemented six days on; two `LANE_BRANCH_RE` constants with different grammars disagreeing on 8
> of 11 real merged branches; the intake area's two generator-carriers with one hooked; an
> ADR-archival bar existing only in a commit body; ADR-100's ruled-but-unbuilt index split. **The repo
> is excellent at ruling and has no organ that notices a ruling only half-landed.**
>
> **Proposal:** every ruling that names an adoption or a mechanism carries a machine-checkable
> *landing predicate* (the file/symbol/site count that proves it landed), and a periodic organ
> verifies the set. Shape to be chosen at ratification against the library-first bar: a check in
> `audit.py` reading the rulings register · or the register gaining a `landed:` field validated by an
> existing validator. **Predecessor commentary:** this is the highest-value item in the whole answer —
> it is the meta-defect behind X-1, X-2 and X-8 alike, and it is the only proposal here that makes
> future rulings self-policing rather than adding another rule to remember.

### 3.3 §B and §C — decision-bearing, quoted verbatim (lines 21–31, condensed to the proposal clauses)

> **§B … Proposal, two legs, both required:** (1) a pin strategy that a fresh container can satisfy
> (`mise` or equivalent — ledger item 36, now evidence-backed rather than speculative); (2) a
> **cloud-lane contract clause**: the single sanctioned response to an unsatisfiable toolchain, the
> mandatory `--unshallow` before any history claim, declared-bypass form, read-mostly scope, zero
> merges to main, and re-gating locally at integration. **Operator's routing intent, recorded:**
> read-mostly lanes (audits, research, recon, evidence sheets) run in the cloud; gated mutations run
> locally — this is also the mitigation for §C.

> **§C … Proposal:** (1) name the class in the batch protocol — batch width has an operator-machine
> cost, and cloud routing (§B) is its release valve; (2) decide the durable form of the editor-hygiene
> config: **user-level** … versus **per-repo via the doc-carrier** … Predecessor recommendation: keep
> user-level as the working fix, and ratify the carrier version only if the fleet gains other
> editor-shared settings, so a folder is not created for one file.

### 3.4 §D — the pointer that already amends #29 (quoted, lines 33–35)

> ## §D — Amendment pointer: DEVELOPMENT TELEMETRY (extends intake #29 S3a, no new intake)
>
> The operator's stated purpose: *compare models and know whether development actually got faster.*
> #29 S3a currently scopes per-arc instrumentation; extend it to a **persisted per-day / per-window
> record** … Acceptance: two consecutive windows of data before any optimization is designed (the
> [#511] discipline — the 30-minute handoff was 0.25% machinery).

### 3.5 Acceptance criterion, quoted (line 51)

> §A/§B/§C ratified or amended at the batch-4 GO; §D folded into #29 as an amendment; §E consulted at
> the cut and departed from only with a stated reason.

### 3.6 Amendment owed against #30 §A — the decision-lifecycle half of commission 5

**Source locator:** `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:212`
(Mandate 3, commission 5 row), quoted verbatim:

> | 5 | session continuity & decision lifecycle | **NONE** | memo `wf-fafd931b` ("Session Continuity
> and the Decision Lifecycle…"): **ZERO in-repo trace — the id appears nowhere in the tree** | owed
> entirely; plan v2 routes only the decision-lifecycle HALF (→ #30 §A); the session-continuity half
> has no named destination anywhere | **TOTAL loss.** Nothing in-repo names, cites, or summarizes this
> commission |

and the recommendation that pairs with it, same file `:336-338`:

> 4. COMMISSION 5 (High): route BOTH halves. Plan folds only decision-lifecycle -> #30 §A;
>    the session-continuity half of memo wf-fafd931b has no destination, and that memo has
>    ZERO in-repo trace — the only commission that vanishes completely if the file is lost.

**Re-verified independently by this lane, with the review's own wording tightened.** `wf-fafd931b` is
not literally absent from the tree — it returns **four hits across two files**: `JOURNAL.md:260` and
the review itself at `:212`, `:276`, `:337`. **All four are the report of the absence, not the
commission's content.** So the accurate statement is the one the review's last column already makes —
*"Nothing in-repo names, cites, or summarizes this commission"* — and its middle column's *"the id
appears nowhere in the tree"* is now false about the tree it was written into, because writing it put
the id there. **The substantive finding is unchanged and stands: zero in-repo carrier holds any of the
commission's content.**

So the amendment #30 §A owes is the decision-lifecycle content itself — and §A is the *right*
destination on the merits, since a "landing predicate per ruling" **is** a decision-lifecycle
mechanism. The half-landed-rulings organ §A proposes is, on its own terms, the organ that would have
caught this commission going half-routed.

### 3.7 DRAFT `decided-by` — #30

```yaml
decided-by: "operator ruling at the batch-4 planning GO, 2026-08-<DD> — §A/§B/§C ratified or amended per this document's acceptance criterion; §D confirmed as folded into intake #29 (no new intake). Amended at ratification: §A absorbs the decision-lifecycle half of research commission 5 (memo wf-fafd931b, off-repo, ZERO in-repo trace as of 2026-08-10) — the routing named at docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:212. The commission's SESSION-CONTINUITY half is routed separately to [#511] and is NOT carried by this document. In-repo carrier for the GO: docs/audits/<the GO's recording artifact>.md"
disposition: active
```

---

## 4. Intake #31 — Universal code-style doctrine for an LLM-written Python fleet

**Path:** `docs/intake/2026-08-09-func-code-style-doctrine.md`

### 4.1 Live frontmatter (quoted, lines 1–6)

```yaml
---
intake-id: 31
status: DRAFT
origin: "Layer-1 architect (predecessor seat), 2026-08-09 — operator directive of 2026-08-09 plus the commissioned research report 'Enforcing a universal code-style doctrine across an LLM-written Python fleet'; authored off-repo and filed verbatim by the ARC-3 hygiene close-out"
note: "BODY FILED VERBATIM — zero edits, zero births. The body's own header bullet still reads `intake-id: 31 (PROPOSED — verify next-free before filing)`; that check is now DISCHARGED and the id is 31, held in reserve for this document since intake #32 recorded 30/31 as RESERVED rather than free. The bullet is left unedited because the archival value of a verbatim filing outranks tidying a resolved parenthetical."
---
```

### 4.2 §A — decision-bearing, quoted verbatim (lines 15–19)

> ## §A — Proposed ruling 1: the doctrine is ONE page, and it separates TASTE from MECHANISM
>
> Written doctrine (taste — stated once, never gated): **"functional core, imperative shell"** as the
> fleet's paradigm sentence (Cosmic Python); **deep modules over thin layers** (Ousterhout, *A
> Philosophy of Software Design*) — explicitly NOT Clean Code's very-short-function rule, which is
> contested and conflicts with deep modules; Google Python Style Guide's falsifiable mechanics
> (comprehension/lambda limits, no globals) copied as the concrete style paragraph; *Effective Python*
> / *Fluent Python* named as the idiom references. **Recorded as a do-not-relitigate item:**
> "Functional Programming in Scala" is a MISMATCH as a fleet source of truth — its type-driven FP has
> no idiomatic Python equivalent and fights the style Python tooling enforces; no book text is copied
> into the repo (copyright).
>
> Everything else in this intake is mechanism. **The paradigm question is not gateable — the
> enforceable proxy is structural: size caps, complexity ceilings, naming rules, import boundaries.**

### 4.3 §B — decision-bearing, quoted verbatim (lines 21–28)

> ## §B — Proposed ruling 2: the mechanism stack, in adoption order (each retires something)
>
> 1. **ruff rule-family expansion**, shipped from one canonical config: `C901` ·
>    `PLR0912/0913/0915/1702` (size/branch/nesting) · `N` (pep8-naming — kills naming drift) ·
>    `SIM/RET/ARG/TRY/ERA/FURB/B` · `I/TID/TC`. Per-file ignores for tests. Retires: ad-hoc per-repo
>    lint opinions.
> 2. **One type checker fleet-wide** (mypy, or basedpyright for speed/strictness) with a **baseline** —
>    the machine-checkable contract that most constrains agent output.
> 3. **Count ratchets** on the complexity rules and type debt — a direct extension of the existing
>    `silent_rule_ratchet` shape …
> 4. **import-linter contracts** (actively maintained, v2.13 Jul 2026) — the one architecture gate …
>    NOTE: prefer it over `tach`, whose original upstream lapsed in 2025.
> 5. **Agent gates:** a PostToolUse hook running the quality gate on every agent edit … and a
>    PreToolUse guard that blocks writes to paths outside governance …
> 6. **Fleet propagation:** a versioned config package published from the hub + `copier` … Retires:
>    copy-paste drift.

### 4.4 §D and §F — decision-bearing, quoted (lines 34–36, 42–44)

> **§D — Proposed ruling 4: NO fleet-wide refactor without a hotspot measurement.** … **Refactor only
> where high churn ∩ high complexity, tests first where coverage is thin; everywhere else, ratchets +
> opportunistic improvement as agents touch the code.** Big-bang rewrites are the recorded failure
> mode …

> **§F — The hand-rolled pieces, declared.** Two items have no established OSS equivalent and
> therefore need a measured-divergence justification per the library-first rule: the **prompt
> pre-dispatch checker** (intake #29's Rule-C shape …) and the **checksum carrier verification**.
> Propagation itself must NOT be hand-rolled — `copier` covers it.

### 4.5 Acceptance criterion, quoted (line 52)

> §A ratified as the written doctrine; §B ordered into batch-4/5 waves with each item's owning row;
> §C's deptry+semgrep pair scheduled; §D's hotspot measurement run BEFORE any refactor row is born;
> §E recorded in the do-not-relitigate register.

### 4.6 Amendments owed against #31 — **none new**, but one live conflict the GO must resolve

No amendment is owed to #31 by any input to this pack. **What is owed is a reconciliation**, and it
is between #31 §B and the ARC-2 distillate, which already **DECLINED** part of §B's stack on measured
grounds — `docs/audits/2026-08-09-technical-consolidation-report.md` §6.4, quoted:

> **One well-argued proposal DECLINED on measured, repo-specific grounds.** The code-style memo
> (`wf-8a83eb70`) proposes a complexity-ratchet stack — `xenon` hard ceilings over `radon`, `wily`
> trend ratchets, `complexipy` cognitive complexity, and a set of ruff `PLR*`/`C901` size rules.
> **Declined**, on this repo's own numbers: [1] 0 of 41 audit checks are generic lint · [2] the whole
> 41-check mesh is 11.66 s, ~0.2 % of an integration arc · [3] the one measured performance defect was
> an `rglob` path-walking bug, not complexity · [4] `silent_rule_ratchet` already exists and no
> hotspot measurement exists · [5] two of the three tools are maintenance risks by the memo's own text.

**So #31 §B item 1 (`C901`, `PLR0912/0913/0915/1702`) and item 3 (count ratchets) are the same
proposals the distillate declined**, and the two artifacts arrive at the GO in the same batch saying
opposite things. This is not a defect in either — the distillate declined the *memo's* stack, #31 is
the *intake* carrying it — but ratifying both as written ratifies a contradiction. The GO must either
(a) ratify §B minus the declined items, (b) overturn the §6.4 decline with a stated reason, or
(c) ratify §B and record the decline as governing the *ordering* only (§D's hotspot measurement first,
which both documents already require). This pack names the fork and does not pick.

Also note the distillate holds §B item 1's exact scope **open, not ruled** (§6.4): *"the code-style
ruff rule-family list and the graph storage choice (DuckDB vs SQLite) **read like decisions and are
not** — the author flags both as his least-defended."*

### 4.7 DRAFT `decided-by` — #31

```yaml
decided-by: "operator ruling at the batch-4 planning GO, 2026-08-<DD> — §A ratified as the fleet's written code-style doctrine and §E entered in the do-not-relitigate register per this document's acceptance criterion. §B's adoption order is ratified <as written | minus items 1 and 3 | subject to §D's hotspot measurement landing first>, reconciling the measured DECLINE of the complexity-ratchet stack recorded at docs/audits/2026-08-09-technical-consolidation-report.md §6.4; the ruff rule-family list is held OPEN there and is <ruled here | left open>. §D binds: no refactor row is born before a hotspot measurement. In-repo carrier for the GO: docs/audits/<the GO's recording artifact>.md"
disposition: active
```

---

## 5. Intake #32 — Compute placement and remote execution

**Path:** `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md`

### 5.1 Live frontmatter (quoted, lines 1–6)

```yaml
---
intake-id: 32
status: DRAFT
origin: "commissioned research memo (workflow wf-1dc18e42, \"Compute Placement & Remote Execution for a Solo-Operator LLM-Agent Fleet\"), read 2026-08-09; filed by the ARC-2 consolidation under architect amendment 3"
note: "ID CHOICE: 30 and 31 are RESERVED, not free — the operator holds two authored-but-unfiled drafts (INTAKE-30 verification-organ-and-repeatable-execution, INTAKE-31 code-style-doctrine) that the RESEARCH-INGEST contract assigns those ids. Taking 30 here would have collided with a permanent join key. Filed at 32 and the gap is reported, not silently closed. EXTERNAL EVIDENCE: the memo is advisory until ratified; nothing here is doctrine by virtue of being filed, and zero backlog rows are born by this document."
---
```

**Frontmatter fact worth recording at the GO:** the `note:` reservation has since **discharged** —
#30 and #31 were filed by the ARC-3 hygiene close-out, so the id gap 30/31/32 is closed and no
renumbering is owed. The note is left as the record of why 32 was taken, which is the same
verbatim-filing discipline #30/#31's own notes invoke.

### 5.2 The one ruled item — decision-bearing, quoted verbatim (lines 37–48)

> ## The one thing here that IS a rule, and is ruled
>
> **Toolchain parity plus fail-closed attestation.** Any remote executor must reproduce the exact
> `uv`/hook toolchain from the lockfiles and **fail closed if a gate did not run** — a run that cannot
> prove its gates executed is treated as **untrusted, not as green**.
>
> This is not aspirational. It is the direct generalization of a **four-times-witnessed** class: on
> 2026-08-09 all five night lanes ran with **no executable gate mesh at all** (`uv` 0.8.17 against the
> ADR-106 `==0.11.19` pin, so every `uv run --locked` hook entry refused; `.git/hooks/` held only
> samples), which is why those five reports had to be re-verified locally after the fact. `[#453]`
> owns the container gaps; **the attestation rule is the part `[#453]` does not carry**, and it is
> what this intake exists to get ratified.

**Reproduced live by this lane, making it five-times-witnessed:** this container is `uv 0.8.17`,
`.git/hooks/` samples-only, `pre-commit` absent from PATH. The condition #32 describes is the
condition this pack was written under.

### 5.3 The headline refusal — decision-bearing, quoted verbatim (lines 22–35)

> ## WHAT the memo actually concludes — the headline is a refusal
>
> **"Fix the laptop first — most of this is a local defect, not a capacity limit."** The memo declines
> its own premise on this fleet's own instrumentation, and every number it cites is one this repo
> measured, not one it supplied:
>
> - the suite is **wait-bound at ~14.6% CPU** (N3-11), so more cores buy little;
> - **~24% of the worktree slowdown is a fixable `rglob` path-walking defect** (N3-03/N3-26), not load;
> - `pytest-xdist` already took the suite **1785.6s → ~539s** (STANDING_RULINGS E1);
> - the remaining levers are **filesystem placement, antivirus scanning and editor indexing** …
>
> **All of it is $0.** The memo's own words: *"Buying compute now would paper over a bug."*

*(the third bullet is the site of erratum E-1, §6.1 below)*

### 5.4 Open questions the GO must answer — quoted verbatim (lines 59–66)

> 1. Does the attestation rule ratify **standalone** (it binds the existing cloud lanes today), or
>    does it wait on a host decision it does not depend on?
> 2. Stage 0 is a list of **operator-machine** changes (Defender, WSL2, Pylance). Is any of it in
>    scope for a repo-governed methodology at all, or is it operator-owned and merely recorded here?
> 3. The worktree model is called "defensible but over-provisioned" (ten full checkouts multiply
>    indexing and scan load). Does that reopen the lane-count ceiling, or is it Stage 0 noise?

**Question 3 is not idle** — intake #30 §C independently reports the same class ("at ~10 worktrees the
operator's editor reported an excessive source-file count"), so #30 §C and #32 Q3 are one question
asked twice and should be adjudicated once. That is the F-class discipline the distillate already
applied to `LANE_BRANCH_RE` ("one ruling, asked twice").

### 5.5 Amendments owed against #32

**E-1 · the xdist/E1 figure mis-attribution** — full text at §6.1.
**A-4 · #32 must be on the ratify surface at all** — same M4-1 finding as #28 §A (§1.6 A-3); plan v2
mentions #32 only as a landed fact, against `JOURNAL.md:562`'s recorded "#28–#32 … ONE batch" intent
and #32's own three open questions, which are addressed to "the receiving architect".

### 5.6 DRAFT `decided-by` — #32

```yaml
decided-by: "operator ruling at the batch-4 planning GO, 2026-08-<DD> — the toolchain-parity + fail-closed attestation rule ratified <standalone | pending the host decision> per this document's open question 1; the fix-local-first verdict accepted, with no host provisioned by this ratification (its own non-goal). Open question 2 (Stage-0 operator-machine changes) ruled <in scope | operator-owned, recorded only>; open question 3 (lane-count ceiling) adjudicated ONCE together with intake #30 §C, which asks the same question. Amended at ratification by the erratum recorded in this frontmatter. In-repo carrier for the GO: docs/audits/<the GO's recording artifact>.md"
disposition: active
```

---

## 6. DRAFT erratum footnote texts

Two errata are owed. Both are **drafts for the ratification batch** — neither is applied by this lane.

**Where an erratum lands, per live convention.** The repo has two shapes and both are in use:
frontmatter (`note:` or `decided-by:`) carrying a dated `ERRATUM …` block — intake #27 carries three
that way, intake #25's `decided-by` carries one — or an in-body dated amendment marker, as
`docs/audits/2026-07-30-technical-intake18-ratification-record.md:120` does. **For a DRAFT intake the
frontmatter `note:` is the correct home**, on intake #27's own recorded standing: *"while `status:
DRAFT` this ledger is editable."*

### 6.1 E-1 — intake #32 line 30: the xdist figures are attributed to a register entry that does not carry them

**The site**, quoted exactly (`docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md:30`):

> - `pytest-xdist` already took the suite **1785.6s → ~539s** (STANDING_RULINGS E1);

**What E1 actually records** (`protocols/STANDING_RULINGS.md:404-408`), quoted:

> - **Applied instance:** §A item 33 (`pytest-xdist`), evaluated under the contract that landed this
>   entry — ADOPTED on a 5.2× measured speedup (serial 1785.61s vs `-n auto` 358.77s / 330.15s) with
>   pass/fail/skip counts identical across all three runs. Landed as `addopts = "-n auto"`,
>   commit `d11dda35`.

**The defect, stated precisely so the erratum does not over-reach.** The *pointer* is correct — E1 **is**
the xdist eval record, and intake #27 row 33 says so in as many words (*"its eval record is
`protocols/STANDING_RULINGS.md` E1"*). What is wrong is the **pair of figures attributed to it**:

- `1785.6s` **is** E1's serial baseline (E1 writes `1785.61s`). ✔
- `~539s` is **not in E1**. E1's post-adoption figures are `358.77s` / `330.15s`. ✘
- `539.12s` is a *different measurement class* — the live full-suite wall clock on merged `main`,
  `docs/audits/2026-08-08-technical-batch-3-packet.md:46` (`1 failed, 2716 passed, 3 skipped, 1
  xfailed in 539.12s`), re-measured at
  `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:94`.
- The two endpoints therefore span **different test populations** (the E1 A/B held pass/fail/skip
  identical across all three runs; the 539.12s run is a later tree at 2716 passed), which is the exact
  confound `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md` §1a names for a
  neighbouring claim: *"the cited pair is confounded, and the record contains a cleaner one the claim
  does not use."*
- **Net effect on the argument:** the fused pair implies **≈3.3×** where E1 records **5.2×**. The
  mis-citation *understates* the adoption's measured benefit — so it does not flatter the intake's
  own case, and the correction strengthens rather than weakens #32's "fix local first" conclusion.

**The correct-form precedent is already in the corpus.** Intake #27 §A row 33
(`docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:52`) carries both numbers and keeps
them **separate, each with its own locator**: *"serial **1785.61s** → `-n auto` **358.77s** /
**330.15s**, ~5.2× … Live full-suite wall clock on merged main: **539.12s (0:08:59)** … —
`docs/audits/2026-08-08-technical-batch-3-packet.md:46`, re-measured
`docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:94`."* The erratum below
conforms #32 to that shape.

**DRAFT erratum text — append to intake #32's frontmatter `note:` at the GO:**

```
ERRATUM 2026-08-<DD> (batch-4 ratification GO): the WHAT-the-memo-concludes bullet at line 30 reads
"`pytest-xdist` already took the suite **1785.6s → ~539s** (STANDING_RULINGS E1)". The POINTER is
correct — E1 is the xdist eval record (intake #27 §A row 33 names it as such) — but the FIGURE PAIR
attributed to it is not E1's. E1 (`protocols/STANDING_RULINGS.md:404-408`) records the adoption A/B as
serial **1785.61s** vs `-n auto` **358.77s / 330.15s**, a **5.2x** speedup with pass/fail/skip
identical across all three runs, landed at `d11dda35`. The **539.12s** figure is a different
measurement class entirely — the live full-suite wall clock on merged `main`
(`docs/audits/2026-08-08-technical-batch-3-packet.md:46`, re-measured
`docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:94`) — taken on a later tree
at 2716 passed rather than the A/B's fixed population. Fusing the two endpoints crosses runs AND test
populations and implies ~3.3x where the record says 5.2x, i.e. it UNDERSTATES the adopted tool's
measured benefit; the intake's fix-local-first conclusion is unaffected and if anything strengthened.
READ LINE 30 AS: "`pytest-xdist` already took the suite 1785.61s -> 358.77s/330.15s, ~5.2x
(STANDING_RULINGS E1); the live full-suite wall clock on merged main is 539.12s
(docs/audits/2026-08-08-technical-batch-3-packet.md:46)". SCOPE, stated so it does not over-reach:
this corrects the figure attribution on line 30 only. No other citation in this document is touched,
no status, conclusion, non-goal or open question changes, and zero backlog rows are born. The
correct-form precedent this conforms to is intake #27 §A row 33, which already carries both numbers
with separate locators.
```

### 6.2 E-2 — the "no home for external research artefacts" premise, five sites

**The premise**, quoted from its intake-side site
(`docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md:71-73`):

> **The memo file itself is deliberately NOT landed in this repo** — no governance clause defines a
> home for external research artefacts, and ADR-101 seals the tree against inventing one.

**All five in-repo sites, located by this lane:**

| # | Site | Class | Editable? |
|---|---|---|---|
| 1 | `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md:71-73` (#32 Provenance) | intake, DRAFT | **yes** (the #27 DRAFT-editability standing) |
| 2 | `docs/intake/2026-08-05-func-simplification-distribution-wave.md:141-143` (#25 Provenance) | intake, **ACCEPTED** | living doc, but body filed verbatim — erratum-by-frontmatter only |
| 3 | `docs/audits/2026-08-09-technical-consolidation-report.md:208` (§5.2 RESEARCH-INGEST table, *"COVERED, and the answer is DO NOT LAND"*) | audit | **no — immutable** (CLAUDE.md §5 rule 3) |
| 4 | `docs/audits/2026-08-09-technical-consolidation-report.md:445-446` (§11) | audit | **no — immutable** |
| 5 | `JOURNAL.md:818` | JOURNAL | **no — append-only** |

**What this lane verified about the premise, clause by clause.** It has two clauses and they do not
have the same truth value:

- **Clause (b) — "ADR-101 seals the tree against inventing one" — TRUE, verified.**
  `scripts/validate_hermetization.py:86-88` pins `SANCTIONED_GENRES = {archive, audits, decisions,
  handoffs, intake}` as a CLOSED set, and Rule A blocks a new `docs/<genre>/` on staged ADDs. A
  `docs/research/` cannot be created without an ADR-101 amendment. No defect here.
- **Clause (a) — "no governance clause defines a home" — NOT ESTABLISHED, and the conclusion does not
  follow from it.** `docs/audits/` **is** a sanctioned genre, and `technical` **is** a member of the
  CLOSED audit-class enum (`validate_hermetization.py:94-104`, `"technical"` at `:96`). The live corpus already carries
  commissioned research landed under exactly that grammar —
  `docs/audits/2026-08-06-technical-night-library-research.md` and
  `docs/audits/2026-08-08-technical-library-research.md`, both self-labelled *"Library-first
  research"*. So a **conforming path exists**; what does not exist is a **ruling that an
  externally-authored artifact may land at it**. Those are different absences, and the premise as
  written collapses them.

**Why this matters at the GO rather than as a footnote.** Site 3 is the sentence that converted the
premise into an executed outcome — the RESEARCH-INGEST contract clause *"land the five memos,
taxonomy-correct home"* was closed as **"COVERED, and the answer is DO NOT LAND"** on this reasoning.
The reconcile packet then measured the cost: **all six commissioned memos exist only in the operator's
Downloads**, commission 5 has *"ZERO in-repo trace"*, and the seeded-defect corpus spec — which gates
`[#491]`, `[#492]` and the Copilot channel — is *"lost entirely"* if that file is. The premise is
therefore load-bearing on three open rows, and it rests on a clause this lane could not establish.

**Stated as a fork, not a finding, because the resolution is the operator's:** either (i) the premise
stands and the memos remain off-repo — in which case the amendment owed is an explicit
**owner + trigger** for each un-landed artifact (the plan's own never-silent bar), or (ii) the
premise is corrected, `docs/audits/<date>-technical-<slug>.md` is confirmed as the conforming home for
an ingested external memo, and the ingest arc lands them. This pack does not choose, and note that
**this lane is read-only and could not have landed them either way.**

**DRAFT erratum text — append to intake #32's frontmatter `note:` at the GO (site 1; site 2 takes the
same text with its own memo id):**

```
ERRATUM 2026-08-<DD> (batch-4 ratification GO): the Provenance paragraph states that the memo file is
not landed because "no governance clause defines a home for external research artefacts, and ADR-101
seals the tree against inventing one". The SECOND clause is verified TRUE — `SANCTIONED_GENRES` in
`scripts/validate_hermetization.py` is a CLOSED set {archive, audits, decisions, handoffs, intake} and
Rule A refuses a new `docs/<genre>/` on staged ADDs, so no `docs/research/` may be invented. The FIRST
clause is NOT ESTABLISHED as written: `docs/audits/` is a sanctioned genre, `technical` is a member of
the CLOSED audit-class enum, and the live corpus already carries commissioned research under exactly
that grammar (`docs/audits/2026-08-06-technical-night-library-research.md`,
`docs/audits/2026-08-08-technical-library-research.md`). A CONFORMING PATH therefore exists; what does
not exist is a RULING that an externally-authored artifact may land at it. The premise collapses those
two absences, and the "DO NOT LAND" outcome it produced
(`docs/audits/2026-08-09-technical-consolidation-report.md:208`) is load-bearing on three open rows:
per `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` Mandate 3, all six
commissioned memos exist only off-repo, commission 5 (`wf-fafd931b`) has ZERO in-repo trace, and the
seeded-defect corpus spec gating `[#491]`/`[#492]`/Copilot is lost with its file. RULED AT THIS GO:
<the premise stands, and each un-landed memo carries an owner + trigger | the premise is corrected and
`docs/audits/<date>-technical-<slug>.md` is the conforming home; the ingest arc lands them>. SCOPE:
this corrects the stated PREMISE only. No status, conclusion, non-goal or open question changes and
zero backlog rows are born. The four sibling sites are recorded, not edited — sites 3/4
(`docs/audits/2026-08-09-technical-consolidation-report.md:208,445-446`) are immutable audit text and
site 5 (`JOURNAL.md:818`) is append-only, per CLAUDE.md §5 rules 1-3; they are superseded by pointer.
```

---

## 7. The five-intake ceiling arithmetic

### 7.1 The ceiling itself is UNLOCATABLE, and that is a verified finding rather than a gap in this lane's search

`docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md:160-163`, quoted:

> The "five-intake working ceiling" itself is **UNLOCATABLE in-repo** — nearest statement is #29's
> amendment ("take the pending set from four to seven and break the same ceiling"); reported as
> unlocatable, not as unruled.

This lane re-ran that search independently on base `5455c2a` and reproduces it: the only in-repo
sentence that constrains the *count* of pending intakes is
`docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:43-46`, quoted:

> Two of the six research commissions had **no owning intake**. Rather than file two more intakes —
> which would take the pending set from four to seven and break the same ceiling this consolidation
> enforces on rows — they fold in here …

**Two readings, both reported because the sentence does not disambiguate them:**

- **R1 (numeric).** "Four → seven breaks it" puts the ceiling in **[4, 6]**; the exact value is
  written nowhere. Under R1 the live working set of **5** is *already above the number the sentence
  treats as safe*, and has been since #32 was filed on 2026-08-09.
- **R2 (rate, not number).** "The same ceiling this consolidation enforces on rows" points at the
  **capacity law** — births capped by demonstrated close capacity, net ≤ 0 — which is a *rate* rule,
  not a count. Under R2 there is no numeric intake ceiling at all, which is consistent with no number
  being findable. All four DRAFT intakes state "ZERO at filing (capacity law)" in their own Births
  sections, which is the rate rule being obeyed, not a count.

**Consequence for the GO, stated plainly:** the arithmetic below is exact; what it is measured
*against* is not. If the ceiling matters to a decision at the GO, it needs a number ruled — and that
ruling is cheap, because §7.3 shows every accept-shaped outcome moves the count the same way.

### 7.2 Baseline — live counts, verified this lane on base `5455c2a`

Method: read `status:` from every `docs/intake/*.md` frontmatter at depth 1 (archive excluded);
cross-checked against the generated index — `python scripts/gen_intake_index.py --check` exits 0.

| Quantity | Symbol | Live value |
|---|---|---|
| Batch-4 ratification working set (#28–#32) | **W** | **5** |
| DRAFT, total | D | 8 |
| — of which NOT in the batch | | 3 (#10, #24, #27) |
| SEED | S | 10 |
| READY | R | 1 (#15) |
| ACCEPTED (live standing authorities) | A | 9 |
| **Live total** | **L** | **28** |
| Terminal, in `docs/intake/archive/` | T | 6 |

Distribution `10 SEED · 8 DRAFT · 1 READY · 9 ACCEPTED = 28` agrees with the reconcile packet's
independent read (`…-fable-adversarial-plan-review.md:155-156`), and with the manifest.

### 7.3 Per-intake outcome deltas (one document, one outcome)

Outcomes are the `docs/intake/README.md` §5 enum. `ACCEPTED` is **not terminal** — a standing
authority stays live and visible — so it moves no document into `archive/`.

| Outcome at the GO | ΔW | ΔD | ΔA | ΔR | ΔL (live) | ΔT (archive) |
|---|---|---|---|---|---|---|
| **ACCEPTED** (with or without amendments — amendments are body/frontmatter edits, not a status class) | −1 | −1 | **+1** | 0 | **0** | 0 |
| **READY** (approved, waiting on its consumer) | −1 | −1 | 0 | +1 | 0 | 0 |
| **HOLD at DRAFT** (deferred to a later GO) | 0 | 0 | 0 | 0 | 0 | 0 |
| **CONSUMED** (content flowed into ADRs/epics) | −1 | −1 | 0 | 0 | **−1** | **+1** |
| **REJECTED** (reason recorded, doc kept) | −1 | −1 | 0 | 0 | **−1** | **+1** |

**CONSUMED is the wrong shape for all five and should not be offered at the GO.** Each of #28/#30/#31
states its own acceptance criterion as *"ratified (or amended)"*, and #29's and #32's content is
standing requirements rather than a one-shot decomposition. ACCEPTED is the outcome their own text
asks for; the terminal outcomes would remove live standing authorities from the index for no gain.

### 7.4 The #28 split is not expressible in the schema — the one arithmetic that does not work

`status:` is a **per-document** field. #28 carries two independently-ruled halves: §B is **DECIDED**
(I-F2, banked) and §A is **undecided** and was dropped from plan v2's ratify surface (M4-1). There is
no `PARTIALLY-ACCEPTED` member of the §5 enum, so at the GO exactly three moves exist:

1. **Rule §A too, flip #28 whole.** W −1. The shape #28's own acceptance criterion asks for
   (*"§A and §B ratified (or amended) … as one batch"*), and the shape I-F2 assumes (*"with §A"*).
2. **Flip #28 whole without examining §A.** W −1, but §A — the two-tier adoption bar gating the whole
   Tier-S try-batch and §C's 14 verdicts — becomes ratified doctrine unread. This is exactly the
   failure intake #25's `decided-by` erratum records happening once already: *"ratified doctrine that
   never landed its status … while its content was already being cited as governing."*
3. **Hold #28 at DRAFT.** W unchanged at 5 for this half of the batch, and the §B decision banked
   2026-08-10 stays invisible to the schema for a second window — a half-landed ruling, which is the
   precise defect class **intake #30 §A exists to detect**.

All three are legal. Only (1) satisfies both #28's acceptance criterion and I-F2's own sentence.

### 7.5 Before/after, per outcome scenario

| Scenario | W | D | A | R | L | T |
|---|---|---|---|---|---|---|
| **S0 — baseline (no GO / batch deferred)** | 5 | 8 | 9 | 1 | 28 | 6 |
| **S1 — all five ACCEPTED** (the shape §15 and I-F2 both describe) | **0** | **3** | **14** | 1 | **28** | 6 |
| S2 — four ACCEPTED, one held at DRAFT | 1 | 4 | 13 | 1 | 28 | 6 |
| S3 — three ACCEPTED, two held | 2 | 5 | 12 | 1 | 28 | 6 |
| S4 — four ACCEPTED, one REJECTED | 0 | 3 | 13 | 1 | **27** | **7** |
| S5 — all five ACCEPTED except #28 held (the §7.4 move 3) | 1 | 4 | 13 | 1 | 28 | 6 |
| S6 — any intake routed to READY instead of ACCEPTED | −1 per | −1 per | 0 | +1 per | 28 | 6 |

**Reading S1 against the ceiling.** Under R1 the working set clears entirely (5 → 0) and lands
**below** every candidate ceiling value in [4, 6]. Under R2 nothing about the ceiling changes, because
R2 is a rate rule and this batch births zero rows by construction. **Either way S1 is the only
scenario that fully unloads the working set**, and every hold carries the ceiling question into the
next window unchanged.

**Reading S4 against the archive.** A REJECT is the only outcome in the whole table that reduces the
**live** total, because REJECTED is terminal and relocates byte-identical to `docs/intake/archive/`
(README §5). None of the five reads as a reject candidate on its inputs; it is tabulated for
completeness, not proposed.

### 7.6 The count the batch cannot fix, and it should be said at the GO

Even at **S1 — all five accepted — DRAFT does not clear: it lands at 3** (#10, #24, #27). And **#10
(`2026-07-11-tech-c4-visualization-memo.md`) has been DRAFT for 30 days as of this GO**, which trips
the README §7 survival metric verbatim:

> **Survival metric:** intake docs sitting unconsumed after **~1 month of operation** trigger a review
> of the scene for removal (ADR-98 §6). A folder that only accumulates SEED/DRAFT docs nobody triages
> has failed the same test a routine fails.

The reconcile packet flags the same three as sitting *"outside every ratification line in plan v2"*
(`:157-160`), and adds READY #15. So: **the intake whose age trips the folder's own survival metric is
not in the batch**, and no outcome in §7.5 changes that. One line at the GO — a triage date or an
explicit hold-with-trigger for #10/#24/#27 and #15 — closes it. This pack files it rather than
widening its own scope to it.

---

## 8. The ARC-2 triage distillate

**Path:** `docs/audits/2026-08-09-technical-consolidation-report.md` §6 (with §6.4 the memo-proposal
cross-check and §11 the orphan-commission routing). **Immutable** — an audit, CLAUDE.md §5 rule 3.

### 8.1 Why it contributes zero to every count in §7

The distillate has **no `status:` field and no frontmatter to flip** — it is a section of an audit, not
an intake. Ratifying it therefore moves W, D, A, R, L and T by **0** in every scenario. Its
ratification act is different in kind: **rule the routed items and record them**, with the landing
site being `protocols/STANDING_RULINGS.md` (the register), exactly as §I recorded the seat-27
checklist. Naming this asymmetry matters because "one batch of six items" invites the assumption that
six status flips happen; **five do.**

### 8.2 What is already adjudicated vs what the GO owes — quoted from §6.3

> - **Adjudicated by this arc (10):** N1 R-4 · R-8 · R-13 · N2 R7 + N4 R1 (`LANE_BRANCH_RE` — **one
>   ruling, asked twice**) · N5 R4 · N1 R-9 · N5 R3 + N1 R-15 · N4 R3.
> - **Routed to the ratification batch (18):** every remaining N1/N2/N3/N5 item whose answer is a
>   decision the operator or a ratified intake must supply.
> - **OPERATOR (7):** N1 R-5, R-14 · N2 R6 · N3 4 · N5 R1 — plus the two in §7.

**So the distillate's ratification surface is the 18 routed items**, plus the (c) CANDIDATE routes in
§6.2 that were **HELD** pending an intake — and those holds join this batch directly:

| Held row | Route recorded in §6.2 | Ratified by |
|---|---|---|
| `[#515]` | *"HELD — enforcement reach as a three-layer property → intake #32"* | **#32** |
| `[#516]` | *"HELD → intake #29 Fold B (measured there at 5/168)"* | **#29** |
| `[#517]` | *"HELD → intake #32 (its central rule)"* | **#32** (the attestation rule, §5.2) |

Three held births are therefore **downstream of #29 and #32 specifically** — which is a second reason
S5 (#28 held) is cheaper than holding #29 or #32.

### 8.3 The triage counts, quoted (§6.1)

> | Outcome | Findings | Ruling items | Memo proposals | Total |
> | (a) OWNED | 34 | 6 | 3 | **43** |
> | (b) DISCHARGED | 52 | 4 | 9 | **65** |
> | (c) CANDIDATE | 39 | 18 | 14 | **71** |
> | (d) REJECTED | 20 | 3 | 12 | **35** |
> | OPERATOR | 8 | 7 | 0 | **15** |
> | **Total** | **153** | **38** | **38** | **229** |

These are the four outcomes ADR-111 ratified as law on 2026-08-10 (I-F1, Option A, as written) — so
**the distillate is the first corpus triaged under a rule that is now Accepted**, and its counts are
the n=1 evidence for ADR-111's own n=2 measurement clause.

### 8.4 DRAFT `decided-by` — the distillate

There is no frontmatter to carry one. The equivalent act is a register entry; drafted in that shape:

```
### <J1> · The ARC-2 triage distillate is ratified

The 229-item triage at `docs/audits/2026-08-09-technical-consolidation-report.md` §6 is ratified at
the batch-4 planning GO, 2026-08-<DD>. Scope, stated so the gaps read as deliberate: the 10 items §6.3
records as already adjudicated are NOT re-ruled; the 18 items §6.3 routes to this batch are ruled here
<one line each, or by reference to the GO's recording artifact>; the 7 OPERATOR items and §7's
15 operator-owed lines are <ruled | carried>. The three HELD births — `[#515]` and `[#517]` (intake
#32) and `[#516]` (intake #29 Fold B) — are unblocked by their intakes' ratification in this same
batch and are born <at this GO | at batch-4 planning against demonstrated close capacity>. The
distillate carries NO `status:` field and none is invented: it is a section of an immutable audit, so
this register entry IS its ratification and no intake count moves. Its (a)/(b)/(c)/(d) outcome set is
the first corpus triaged under ADR-111, Accepted 2026-08-10 (I-F1), and stands as n=1 toward that
ADR's own n=2 measurement clause.
```

---

## 9. Amendments owed — consolidated

| # | Amendment | Destination | Source locator | Type |
|---|---|---|---|---|
| A-1 | zero-mechanically-untestable-Done-when criterion (a ninth §B criterion) | **#28 §B** | `protocols/STANDING_RULINGS.md:818` (banked I-F2). Evidence for drafting: `docs/audits/2026-08-10-technical-backlog-testability-census.md` (75/72/15/8 of 170) | banked ruling, executes at GO |
| A-2 | clause 5 (`handoff cut < 10 min measured`) **STAYS** | **#28 §B** | `protocols/STANDING_RULINGS.md:818`; companion `:812-815` ([#511] re-scope) | banked ruling, executes at GO |
| A-3 | **#28 §A must be on the ratify surface** | the batch's enumeration | `…-fable-adversarial-plan-review.md` M4-1 (High); **`JOURNAL.md:843`** (M4-1 says `:562` — drifted, §9.2); #28's own acceptance criterion (`:57`) | scope repair |
| A-4 | **#32 must be on the ratify surface** | the batch's enumeration | same M4-1 | scope repair |
| A-5 | seeded-defect corpus spec — **or** an explicit owner+trigger | **#29** | `…-fable-adversarial-plan-review.md:210, 218, 339`. Input: `docs/audits/2026-08-08-technical-seeded-defect-substrate-inventory.md` | content owed |
| A-6 | decision-lifecycle half of commission 5 (`wf-fafd931b`) | **#30 §A** | `…-fable-adversarial-plan-review.md:212`, `:336-338` | content owed |
| A-7 | **session-continuity** half of commission 5 | **`[#511]`** attach, per the seat's ruling | ruling carried by the N3 brief; the gap it answers is `…-fable-adversarial-plan-review.md:212` (*"has no named destination anywhere"*). Row: `tasks/511-handoff-cut-cost-is-session-authoring.md` | content owed |
| E-1 | xdist/E1 figure mis-attribution | **#32** frontmatter `note:` | §6.1 above | erratum |
| E-2 | the "no home" premise | **#32** (+ #25) frontmatter `note:` | §6.2 above | erratum / fork |

### 9.1 One flag on A-7, because it is the same defect class the batch is ratifying

The `[#511]` attach for the session-continuity half is carried by this lane's brief as *"the seat's
ruling"*. This lane searched and **found no in-repo record of it**: `protocols/STANDING_RULINGS.md` §I
records I-F2's `[#511]` re-scope but says nothing about commission 5, and `wf-fafd931b` returns zero
hits tree-wide. So A-7 is, right now, **a ruling that exists off-repo and has not landed** — which is
precisely the half-landed-ruling class **intake #30 §A** is being ratified to detect. Recording it
here is the cheapest available discharge; the GO should land the register line in the same act, or
§30 §A's first live instance will be its own ratification batch.

### 9.2 Two locator defects this lane surfaced in its own inputs, both in the reconcile packet

Recorded because the GO will otherwise re-cite them, and because both are the class the 3b-4 citation
convention was adopted for on 2026-08-10 (`protocols/STANDING_RULINGS.md` I-D, *"ADOPTED as a PLAYBOOK
drafting rule, advisory — it earns a check only on n=2 evidence"*). **These two are that n=2**, arriving
inside one day of the adoption, in the artifact that itself caught the first instance.

1. **`JOURNAL.md:562` has drifted; the live anchor is `JOURNAL.md:843`.** M4-1 cites `:562` for the
   recorded *"ratification batch (intakes **#28–#32** + the triage distillate as ONE batch, ADR-111
   riding it)"* intent. On base `5455c2a` that sentence is at **`:843`**, inside entry
   **2026-08-09 (i)** (*"ARC-2 Phases B–F — the pipeline ruled, 229 items triaged…"*), and its
   `**Next:**` line is where it lives. Line 562 now sits inside a **different entry** —
   2026-08-10 (a), the ARC-4 disposition arc — so the citation does not merely point a few lines off,
   it points into the wrong session. Cause is structural and not a mistake by the review: `JOURNAL.md`
   is **newest-first prepend**, so every line number in it is invalidated by the next entry. **A
   JOURNAL line-number citation is a decaying locator by construction**; the durable form is
   entry-date + quoted phrase. Reported, not ruled — whether that becomes a drafting rule is the
   operator's, and it would extend 3b-4 rather than start something new.
2. **`wf-fafd931b` "appears nowhere in the tree" is now false about the tree.** Four hits, two files,
   all of them the report of the absence (§3.6). The review's own last column states it correctly;
   only the middle column over-claims. **Self-referential class worth naming once:** an artifact that
   records "X appears nowhere" makes its own sentence false the moment it lands, so an absence claim
   should be scoped to *carriers of the content*, never to *occurrences of the string*. The
   substantive finding is untouched and this pack relies on it.

Neither defect changes any conclusion in the reconcile packet, and neither is proposed as a row.

---

## 10. What this pack does not answer

Stated so the gaps read as deliberate rather than as coverage.

1. **The ceiling's number.** Reported as unlocatable (§7.1), reproducing the reconcile packet's
   finding. Not invented.
2. **The #31 §B vs distillate §6.4 conflict.** Named as a fork with three resolutions (§4.6); not
   picked — both artifacts are inputs to the same GO and the choice is the operator's.
3. **The "no home" premise's resolution.** Both branches drafted (§6.2); not picked. This lane is
   read-only and could not have landed the memos under either branch.
4. **The A-1 drafting fork.** "Zero mechanically-untestable Done-when" has three defensible readings
   (95 rows / 8 rows / 23 rows of work); the banked ruling does not disambiguate and this pack does
   not choose for it (§1.6).
5. **FORK 4 (the births package).** Out of scope by §I's own stated scope, and untouched here.
6. **Whether any intake should be REJECTED.** Tabulated for completeness in §7.5 (S4); none is
   proposed, because nothing in the inputs argues for one.
7. **The 18 routed distillate items, item by item.** They are enumerated by reference (§8.2) because
   §6.3 names them as a class rather than a list; expanding that list is an adjudication, which this
   pack is not.

---

## 11. Lane self-check

| # | Constraint from the brief | Verdict |
|---|---|---|
| 1 | Base = `origin/main` tip, printed in line 1 | **PASS** — `5455c2a2a008e0ce8cc1d8ac77d2835cfd767376` |
| 2 | Read-only | **PASS** — the only writes are this report and the mandatory `docs/audits/README.md` regen |
| 3 | Zero edits to any intake | **PASS** — `git status` shows no `docs/intake/` path |
| 4 | Zero births | **PASS** — no `tasks/` or `BACKLOG.md` path touched; no `[#id]` allocated |
| 5 | No JOURNAL | **PASS** — `JOURNAL.md` untouched |
| 6 | ONE report | **PASS** — this file |
| 7 | One section per intake #28–#32 plus the distillate | **PASS** — §1–§5, §8 |
| 8 | Live frontmatter + decision-bearing sections QUOTED | **PASS** — §1.1–1.4, §2.1–2.4, §3.1–3.5, §4.1–4.5, §5.1–5.4 |
| 9 | Amendments owed with source locators | **PASS** — §9, nine rows, every one with a `file:line` |
| 10 | DRAFT erratum footnote texts | **PASS** — §6.1, §6.2 |
| 11 | DRAFT decided-by lines | **PASS** — §1.7, §2.6, §3.7, §4.7, §5.6, and §8.4's register-shaped equivalent |
| 12 | Five-intake ceiling arithmetic before/after each possible outcome | **PASS** — §7.3 per-outcome deltas, §7.5 six scenarios |
| 13 | DRAFT header | **PASS** — the blockquote at the top of this file |
| 14 | Gate posture declared honestly | **PASS** — header; no gate in the mesh could execute in this container |
