# "Architekt Jutra" second pass — shipped-vs-specified, and a live head-to-head (2026-09-05)

> **Consumes** `docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md` — this
> arc is the execution half of that analysis, and exists to replace its documentary claims with
> execution witnesses. **Intake:** `#70`. **Governance:** ADR-111 — nothing enters the tree from
> this arc except this audit and CANDIDATEs through the funnel; no row is born here.
>
> **Method rule, applied throughout:** a capability is `RUNNING` only where a command was executed
> **in this arc** and produced an artifact whose path is recorded. "It is documented" is
> `SPECIFIED`, never `RUNNING`. Where I could not run it, the cell says so.

## §0 — The decision table

Fifteen rows: the frozen contract's enumeration
(`1,2,3,5,6,7,9,10,11,12,13,15,18,19,21`). The contract calls this "the 14 rows"; the
enumeration lists **15** and none of them is `BOTH-same`, so the "minus any BOTH-same" clause
subtracts nothing. The enumeration governs and nothing is dropped silently — see §4 D1. Row 8 is
`BOTH-different-name` and is **not** in the enumeration, so it is not scored here.

Legend — **AJ** and **DK** are shipped-vs-specified per side: `RUNNING` (executed in this arc,
artifact path given) · `SPECIFIED` (intake/ADR/doc/course locator only) · `ABSENT`.
Proposal is the arc's answer to the objective function.

| # | Capability | AJ | DK | Proposal | Witness |
|---|---|---|---|---|---|
| 1 | Per-loop trace inspection — every LLM/tool call with token counts | SPECIFIED — course only (`M01L02:111-139`, Phoenix); Maister emits **no** trace, and none appears in the 49 `.maister/` artifacts | **RUNNING** — but for *governance*, not model calls: `DEV_KNOWLEDGE_TELEMETRY=1 audit.py health` wrote **42 `check_run` events** with real per-check `duration_ms` | **REJECT (as framed)** — the model-call half is real but is not what either side ships; Maister does not have it either | `FR1-row01-audit-health-telemetry.txt`; `logs/TELEMETRY.db` (42 rows, e.g. `check_proof_layer pass 3469ms`) |
| 2 | Cost per command as an architecture signal | SPECIFIED — `M01L05:126-135` ($0.76 vs $0.56). Maister itself reports no cost | **ABSENT** — our own trend surface says so in its own words: `gate time per runner invocation ABSENT`, `suite wall-time ABSENT`, `per-model change quality ABSENT` | **ADOPT-INTO-HUB (candidate C-1)** — and this arc supplies the first real datum for it: a measured per-leg cost on one identical S row (§1 m10) | `FR1-row12-18-trend-dashboard.txt` (the three ABSENT panels); §1 m10 |
| 3 | Standards mined from the repo's own history | **RUNNING** — `/maister:init` derived a 7-file standards tree + 3 project-context files from the codebase, unprompted | **RUNNING** — `silent_rule_detector.py .` → `silent-rule-v5, files 61, count 439`; `propose_closures.py` → 2 strong proposals over 6519 commits | **ALREADY-RUNNING (both), with one real gap** — neither mines **review history**; ours mines the corpus, theirs mines the code | AJ: `.maister/docs/standards/global/*.md` (7 files), `.maister/docs/INDEX.md` · DK: `FR1-row03-silent-rule-detector.txt`, `FR1-row03b-artifact-PROPOSALS-2026-09-05-01.md` |
| 5 | A clarifications contract | **RUNNING** — `analysis/clarifications.md`, `scope-clarifications.md`, `technical-clarifications.md`, and 5 decisions recorded as `resolved by assumption, not consent` | **RUNNING** — `verify_handoff_probes.py` on the active v7 bundle: **13/13 probes pass, "binds to live state"** | **ALREADY-RUNNING, ours is stronger** — theirs records answers; ours **fails** when the repo contradicts one | AJ: `.maister/tasks/development/2026-09-05-fix-crux-refusal-word-boundaries/analysis/clarifications.md` · DK: `FR1-row05-handoff-probes.txt` |
| 6 | Intra-run phase decomposition with a machine state file | **RUNNING** — `orchestrator-state.yml`: 14 phases, `completed_phases`, `failed_phases`, `reverify_count`, resumable mid-phase | **RUNNING** — `gen_lane_contract.py emit --shape local` produced a 7-section frozen contract; leg D then provisioned `worktree-ai-council-119-crux-refusal` from it | **ALREADY-RUNNING at a different grain** — theirs resumes mid-phase, ours at lane boundaries. Real, and not obviously worse | AJ: `.../orchestrator-state.yml` · DK: `LANE-ai-council-119-crux-refusal.md`, `FR1-row07b-lane-contract-check.txt` |
| 7 | Characteristic flags that gate which phases fire | **RUNNING** — `task_characteristics: {has_reproducible_defect, modifies_existing_code, creates_new_entities, involves_data_operations, ui_heavy}` **derived**, and they demonstrably gated: `phase-4-skipped` (UI) with `ui_heavy: false` | **RUNNING but not derived** — `gen_lane_contract.py` shape-gates emission; `check` passed `OK · 7 sections, shape local`. The shape is **stated by the author**, never inferred | **ADOPT-INTO-HUB (candidate C-2)** — the *derivation* step is the genuine gap; the gating already exists | AJ: `orchestrator-state.yml` `task_characteristics` + `completed_phases` showing `phase-4-skipped` · DK: `FR1-row07b-lane-contract-check.txt` |
| 9 | Harnessability as a named quality attribute | SPECIFIED — `M01L01:137-139`, `M01L05:93`. No artifact in this arc names or measures it | **RUNNING (adjacent concept)** — `tests/test_legibility_graph_conformance.py` **5 passed, 1 skipped**. Ours means *observability*, not *harnessability* | **REJECT as vocabulary, ADOPT as question** — we have the word for the wrong thing; nothing here is worth copying wholesale | `FR1-row09-legibility-graph.txt` |
| 10 | Wave computation with a file-disjointness invariant | **RUNNING** — `implementation-plan.md` computed `Task Groups: 1`, declared `Files to Modify:` and stated *"Single group — nothing runs in parallel"* | **RUNNING — and the gap analysis was wrong to call ours hand-assembled.** `boot_frontier.py`: **5 proposed (width≤6, ledger≤5), 62 rows held back on serialize-group disjointness** | **ALREADY-RUNNING (both).** The genuine delta is the *unit*: their invariant is over **files**, ours over **declared serialize-groups** | AJ: `.../implementation/implementation-plan.md:64-67,198-200` · DK: `FR1-row10-boot-frontier.txt` |
| 11 | Model routing per prompt | SPECIFIED — `M01L02:336-345` (LiteLLM). Leg M ran **entirely on `claude-opus-5`**: 123 turns, 14 subagents, one model class, no cheap tier | **RUNNING** — `routing_agreement.py`: *"4 role(s) in ecosystem/routing-table.yaml corroborated by ~/.claude/ROUTING.md"* | **ALREADY-RUNNING, ours is the better placement** — and leg M is the evidence: an unrouted harness billed $48.53 doing an S row on the most expensive model | AJ: `FR2-legM-02-development.json` `modelUsage` (single class) · DK: `FR1-row11-routing-agreement.txt` |
| 12 | An operator dashboard of live run state | **RUNNING** — `dashboard.html` + `dashboard-data.js` written per phase, and the run **auto-opened a browser** (msedge, 19:32) | **RUNNING but different question** — `gen_trend_dashboard.py` printed a live fleet trend with a direction verdict per panel | **ADOPT-INTO-HUB (candidate C-3, narrow)** — "where is this task now" is genuinely missing; ours answers "what is the state of the fleet" | AJ: `.../dashboard.html`, `dashboard-data.js`; `FR2-legM-02-process-state.txt` (the browser launch) · DK: `FR1-row12-18-trend-dashboard.txt` |
| 13 | Adversarial re-verification as a role | **RUNNING** — `reality-check.md` re-ran the parser itself on **18 claims and 43 refusals written independently**, and did not trust the prior report | **RUNNING** — `routing-table.yaml:30-41` separates `reviewer` (codex/`gpt-5.6-terra`) from `adversarial` (sol); terra was run on both diffs for m9 (§1) | **ADOPT-INTO-HUB (candidate C-4)** — *re-execute, do not trust the report* is a posture we do not name. Our two roles judge a diff and attack a design; neither re-runs the prior leg's tests | AJ: `.../verification/reality-check.md` · DK: `FR1-row11-routing-agreement.txt`, §1 m9 |
| 15 | The greenfield inversion | SPECIFIED — `M02_ebook:p7`, `M02L07:103`; the mechanism (`/maister:init --standards-from`, `M01L04:40-46`) was **not** exercised here | **SPECIFIED** — `deploy/carrier_floor.py` and the manifest carriers seed a child from the mature hub, which *is* the inversion in practice; no doc states it as a principle | **ALREADY-RUNNING in mechanism, ABSENT as doctrine** — worth one sentence in PLAYBOOK, not a build | DK: `deploy/carrier_floor.py`, `deploy/manifest-v*.yaml`; no execution claimed |
| 18 | Artifact visualization against information overload | **RUNNING** — 4 `.html` companions emitted (`spec.html`, `implementation-plan.html`, `implementation-verification.html`, `dashboard.html`) | **RUNNING** — same trend run; every panel carries a direction verdict as word (`IMPROVING`/`WORSENING`/`ABSENT`/`INSUFFICIENT`) | **ALREADY-RUNNING (both).** No action | AJ: the four `.html` files under `.maister/tasks/.../` · DK: `FR1-row12-18-trend-dashboard.txt` |
| 19 | A benchmark for long-term modifiability | SPECIFIED — `M01L05:44-56` (SlopCodeBench). Not run here | **SPECIFIED (design) + RUNNING (its guard)** — the benchmark itself has never been executed; its guard has: `nopack_sandbox.py scan` found **6 files carrying answer-key content** | **REJECT for now** — neither side has run a modifiability benchmark. Ours is a design; theirs is a citation. Nothing to adopt from an unrun thing | DK: `FR1-row19-nopack-scan.txt`; design at `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` |
| 21 | A curated agent-run trajectory archive | SPECIFIED — the `architekt-jutra-code` job archive; **not** produced by this arc's run. Maister's 49 artifacts are a *task* record, not a judged trajectory set | **RUNNING** — `tests/test_lived_sandbox.py` + `test_lived_sandbox_observer.py`: **90 passed, 2 skipped**, over 4 committed session transcripts and the secret-scrub refusal | **ALREADY-RUNNING, ours is stronger** — their strip list is documented, ours *refuses*. Genuine delta: they keep a judged score beside the mechanical one; we keep only the mechanical | DK: `FR1-row21-lived-sandbox.txt`; fixtures `tests/fixtures/lived-workflow/*.jsonl` (4) |

**Coverage against the success criterion.** 30 cells (15 rows × 2 sides). `RUNNING` in **21**;
`SPECIFIED` in 8; `ABSENT` in 1. **Every one of the 21 RUNNING cells carries an artifact path**,
so NC6 holds and no cell is RED. The criterion asks for execution witnesses on ≥80 % of cells:
21/30 = **70 %** are RUNNING, but the criterion is about *witnessed* cells, and the 9 non-RUNNING
cells are witnessed too — each carries either a course locator or a recorded search. Read
strictly as "≥80 % of cells are RUNNING", **this arc misses at 70 %** and says so; read as "≥80 %
carry a witness", it is 100 %. The stricter reading is the one flagged in §4.

## §2 — FR3: operator practices

Behaviours a person performs, not mechanisms. Licensed course content: **paraphrase +
locator only** (NC4), no quotation beyond a few words. Locator grammar is the one the
gap-analysis arc ratified — `<lesson-slug>:<line>` against the canonical `.md`, `p<N>` for
ebooks, `README.md:<line>` for the plugin repo. Ten items; six we already do, four we do not.

| # | Practice (paraphrased) | Their locator | We do this today? |
|---|---|---|---|
| 1 | Judge a candidate library or infrastructure provider partly on its **AI-friendliness** — does it ship skills or an MCP server the agent can consume, so it arrives carrying its own good practice | `M01L05:239-246` | **No.** ADR-106 declares dependencies and ADR-112 sets a two-tier adoption bar, but neither asks whether a dependency is legible to an agent. Nothing in `pyproject.toml` or the ADR-112 fork test records it |
| 2 | Measure the token/cost effect of an optimisation **on your own usage**, rather than trusting a published benchmark — savings are workload-shaped | `M01L02:408-414` | **Partly.** ADR-112's Tier S is exactly "try it and keep or delete it", and `logs/TOKEN-LOG.md` is a weekly aggregate — but we have no per-tool before/after, which is candidate C-1 |
| 3 | When picking a framework for agent-driven work, weigh popularity, complexity **and cross-release stability together** — an unstable popular API confuses an agent trained across its versions | `M01L05:205-226` | **No.** No such criterion is recorded anywhere in `docs/decisions/` |
| 4 | Seed a greenfield project's standards from a mature sibling instead of starting blank — the sibling has already paid for the childhood diseases | `M01L04:40-46` | **Yes.** `deploy/carrier_floor.py` + `deploy/manifest-v*.yaml` carry the hub's matured corpus into a child; `.claude/CLAUDE-FLOOR.md` is the hash-guarded replica |
| 5 | Recognise the **"orchestrator went quiet after a long phase"** pattern and answer it with a plain nudge, rather than debugging it as a fault | `README.md:173` (Known Issues) | **No — and this arc paid for it.** Leg M ran 2 h 06 m unbounded before the omission was noticed; the operator had to rule a 15-min idle cap mid-arc (§4 D6). We had no such habit and no such cap |
| 6 | Run the agent from a directory that already holds sibling implementations, so it extends its context from real examples instead of working greenfield | `M02L07:103` | **No.** Our lane worktrees are provisioned per-lane at `.claude/worktrees/<name>`; nothing positions a lane beside comparable prior work deliberately |
| 7 | Decide deliberately what is fast enough for the tight in-loop check versus what belongs in the slower CI pass, instead of running everything every iteration | `M01L02:187-201` | **Yes.** `CLAUDE.md:65` — targeted tests per lane, the **full suite once, at integration**; pre-commit carries the fast gates |
| 8 | Keep the human accountable for system architecture even when it is reached through dialogue with the agent — the conversation informs, it does not own the decision | `M01L05:61-64` | **Yes.** ADR-108 §A splits it explicitly: the operator rules functional questions, the architect technical ones (`docs/decisions/ADR-108-*.md:40`) |
| 9 | Commit the orchestration and decision artifacts, so a later reader can reconstruct **why** and **by whom** a decision was made | `M01L04:223-226` | **Yes.** `docs/handoffs/*/` (73 committed `SUPPLEMENT.md`), `docs/audits/`, and the append-only newest-first `JOURNAL.md` |
| 10 | Start each stage of a chained workflow in a **fresh session** — the prior stage's artifacts already carry the context, so continuing the conversation only adds noise | `README.md:157` (Best Practices) | **Yes.** `protocols/PLAYBOOK.md:1527,1543` — a new session boots from the handoff bundle, and the named anti-pattern is opening one with a bare "continue what we were doing" |

**Count: 10 items, all with locators — the criterion asks for ≥8.** The four `No` rows are the
honest yield of FR3; items 1, 3 and 6 are cheap to adopt as habits and none of them needs a
build. Item 5 is the one this arc demonstrated the cost of first-hand.

Four further candidates were extracted and **cut** because they are software-architecture
judgement (when to adopt a plugin architecture, who authors plugins, trusting plugin authors,
anticipating a team bypassing a new boundary) rather than operator behaviour toward an agent.
They are real advice; they are not what FR3 asked for.

## §1 — FR2: the live comparison

**The task, identical text to both legs (NC3).** ai-council BACKLOG `[#119]` — `crux_check.py:137`
matches `_REFUSAL_MARKERS` as bare substrings, so *"Whether an AI cannot determine tumour grade
from images is the crux"* hits `i cannot` (inside "AI cannot") and `cannot determine`, and is
discarded as `MALFORMED` behind a `retrieval_unavailable` signal. FR2 offers a default of "one CLI
flag with a unit test" **or** an open `S` row if one exists — ai-council has 20, so **the open row
was used**, as FR2 directs. The defect was reproduced first-hand before either leg ran. Frozen at
`SEEDED-TASK.txt`; carried into leg D's contract verbatim (verified by string equality, not by eye).

**Both legs, same transport:** `claude -p --output-format json --setting-sources local
--permission-mode bypassPermissions --model opus`, run **sequentially**, never concurrently, so
neither leg's wall-clock is inflated by the other. Clone M was reset to pristine before the run
that counts (§4 D3).

| | **m — metric** | **Leg M (Maister)** | **Leg D (our lane contract)** |
|---|---|---|---|
| m1 | wall-clock | **7809 s — 2 h 10 m 09 s** (+ `/maister:init` ≈ 732 s beforehand) | **1225 s — 20 m 25 s** |
| m2 | tokens by model class | `claude-opus-5` only — in 742 · out 604 888 · cache-read 44 038 949 | `claude-opus-5` in 86 · out 36 808 · cache-read 2 552 062 · **plus `claude-haiku-4-5`** in 950 · out 22 |
| m3 | files created/modified | **2 modified** (`crux_check.py` +52/−6, `test_crux_check.py` +78) · **49 created** under `.maister/` | **3 modified/created** (`crux_check.py` +34/−4, `test_crux_check.py` +35, a 209-line lane report) · 3 commits |
| m4 | tests after the run (**I ran the suite; I did not read either report**) | **941 passed, 5 failed, 1 xfailed** — failing set byte-identical to baseline ⇒ **+8 passing, 0 regressions** | **937 passed, 5 failed, 1 xfailed** — same five names ⇒ **+4 passing, 0 regressions** |
| m5 | human prompts required | **0 asked**, but `gate_channel.available: false` and **5 design decisions (D1–D5) resolved "by assumption, not user consent"**; 6 analysis artifacts incl. three separate clarification files. Interactively this is ≥5 | **0 asked, 0 needed.** The lane contract's V-2 decision budget pre-authorises the classes it may decide, so the questions never arise |
| m6 | stalls | **0** on the run that counts. But see §4 D6 — it ran **2 h 06 m** before anyone knew whether it was alive, and the vendor's own README documents this failure mode | **0** |
| m7 | gate honesty | **No contradiction** — and unusually candid; detail below | **No contradiction** — detail below |
| m8 | resumable artifacts | **49** — `orchestrator-state.yml` (14 phases, `completed_phases`, `reverify_count`), work-log, TDD red/green gates, 6 verification reports, `dashboard.html` | **5** — 3 commits (RED test · repair · report), the frozen contract, the 209-line lane report. Resumable by `git log`, not by a state file |
| m9 | what it got wrong (terra, same rubric) | **SOLVES-WITH-DEFECTS · DEFECT_COUNT 2** | **SOLVES-WITH-DEFECTS · DEFECT_COUNT 2** |
| m10 | cost | **$48.53** · 123 turns · 14 subagents | **$3.00** · 51 turns · 0 subagents |

**The headline: 6.4× the wall-clock and 16.2× the cost, for the same verdict on the same task.**
Leg M read 44.0 M cache tokens against leg D's 2.55 M — 17×. Neither number is estimated; both are
the CLI's own `total_cost_usd` and `modelUsage`.

### m4, in full

Baseline before either leg (`FR2-baseline-summary.txt`): **5 failed, 933 passed, 1 xfailed**. Four
are Rich/ANSI console-wrapping assertions, one is a real `ImportError`. Neither leg is charged for
them; m4 is the **delta**.

- **Leg M:** 941 passed / 5 failed — `FR2-legM-suite-AFTER.txt`. Same five names. **+8, no regressions.**
- **Leg D:** ran in its own worktree venv. ai-council's root `conftest.py` **refused the first
  attempt** — `WRONG-TREE IMPORT — COLLECTION ABORTED`, because the editable install resolves
  `ai_council` to the primary checkout from any other interpreter. That guard is a credit to
  ai-council and cost one rebuild; leg D had already hit and documented it. After building the
  worktree's own venv: **937 passed / 5 failed / 1 xfailed** in 334 s, the same five names —
  **+4, no regressions** (`FR2-legD-suite-AFTER.txt`).

**So leg M bought twice the test growth (+8 vs +4) for 16× the money.** Whether four further
pinned cases are worth $45.53 is the operator's call; the arc's job is to put both numbers in one
table. Both legs left the suite with zero regressions.

### m7 — gate honesty, both legs

Neither leg's machine-readable state contradicts its verdict artifacts. Both are worth the detail
because this is the metric most likely to be flattered.

**Leg M.** `task.status: completed` is qualified in the same file by
`verification_context.last_status: passed_with_issues`. `issues_found` lists 8 items and **marks 3
`fixed: false`** — including `FLOOR-1`, that the work sits uncommitted on `main` with no branch,
which is a finding *against itself*. `gate_channel.note` states plainly that `AskUserQuestion` was
absent, that every mandatory gate is recorded auto-approved, and that *"No gate was skipped by
model judgment"*. It also **self-corrects**: its implementation summary says "935 passed / 4
failed"; finding `I-4` then corrects the pre-existing count to **5** — which matches my independent
baseline exactly.

**Leg D.** Its report's Verification table states 937 passed / 5 failed on the full suite and
proves the four non-import failures pre-existing **by stashing and re-running at the lane base**,
rather than asserting it. Its `Status` line reads *"Commit-and-STOP. Not merged, not pushed, no
PR."*, which `git log` confirms.

The honest asymmetry: **leg M's state file is a far richer resumption surface**, and nothing in our
lane shape is equivalent to `orchestrator-state.yml`.

### m9 — terra on both diffs, one rubric

Same rubric file, same reviewer (`codex-cli 0.145.0`, `gpt-5.6-terra`), code only — commit
messages and reports withheld from the reviewer so prose could not earn credit. **Both legs:
`SOLVES-WITH-DEFECTS`, `DEFECT_COUNT: 2`.** A tie on the tally, and the tally is not the whole
story:

- **Leg M** — both defects are behavioural `[HIGH]`, and they point in **opposite directions**:
  (a) subject-less markers now miss ordinary refusals with a non-`there` subject (*"We cannot
  determine a crux"* is released downstream as fact); (b) the unanchored `there is …` branch
  **still** discards valid claims. It has a false negative *and* an unfixed false positive.
- **Leg D** — one behavioural defect (`crux_check.py:104` allows only an exact first-token opener,
  so *"Unfortunately, cannot determine a crux…"* is released) plus one **test-quality** finding
  (the set does not discriminate the intended anywhere-match from a pure prefix matcher).

So: equal counts, but leg M's two are both live wrong-answer paths while one of leg D's is a
coverage gap. Leg M had *already found this class itself* (`reality-check.md` MEDIUM-1, and
`FN-1..FN-4` accepted knowingly) — it documented the residue and shipped it; terra found it anyway.
That is a point in favour of Maister's verification depth and against its judgement about what is
acceptable to release.

## §3 — Candidates (Z-C shape)

ADR-111: these are **CANDIDATEs**, not rows. Nothing here is filed as a backlog id by this arc;
the only path onward is intake (ADR-98) and then ratification. Each states what it is, what it
would cost, and the witness that produced it — an item with no witness from this arc is not here.

**C-1 · Per-unit-of-work cost, as a first-class measurement.**
*Witness:* `gen_trend_dashboard.py` prints `gate time per runner invocation ABSENT`, `suite
wall-time ABSENT`, `per-model change quality ABSENT` — our own trend surface saying the panel has
no data. This arc then produced exactly that datum by hand: **$48.53 vs $3.00** on one identical
S row. *Shape:* record `total_cost_usd`, `duration_ms` and `modelUsage` per dispatched lane —
the CLI already emits all three under `--output-format json`, so this is capture-and-store, not
new instrumentation. *Cost:* S. *Why it matters:* a 16× spread between two harnesses on the same
row was invisible before this arc and would be invisible again tomorrow.

**C-2 · Derive the lane shape instead of stating it.**
*Witness:* Maister's `task_characteristics` (5 booleans) were derived by an analysis phase and
**demonstrably gated execution** — `phase-4-skipped` because `ui_heavy: false`. Our
`gen_lane_contract.py` already shape-gates emission and `lane-contract-check` already enforces the
result; the shape is simply **typed by the author**. *Shape:* a pre-dispatch step that proposes
`--shape` and effort from the row text, which the author accepts or overrides. *Cost:* M.
*Guard:* proposal only — the author still signs the contract, per ADR-108 §A.

**C-3 · A "where is this lane right now" surface.**
*Witness:* `.maister/tasks/<task>/dashboard.html` + `dashboard-data.js`, rewritten per phase; the
run auto-opened a browser. Our dashboards answer *"what is the state of the fleet"*, a different
question — and this arc paid for the gap: leg M ran **2 h 06 m** with nobody able to tell whether
it was alive, because `-p --output-format json` buffers to the end. *Shape:* a lane writes a small
progress file each step; the operator reads one place. *Cost:* S. **This is the candidate the arc
most directly earned.**

**C-4 · Name the "re-execute, do not trust the report" role.**
*Witness:* Maister's `reality-assessor` re-ran the parser itself on 18 claims and 43 refusals it
wrote independently, and its finding (`MEDIUM-1`, a released refusal outside the documented set)
was **real** — terra found the same class. Our `routing-table.yaml` has `reviewer` (judges a diff)
and `adversarial` (attacks a design); neither is defined as *re-running the prior leg's tests*.
*Shape:* a third role in the routing table, plus one line in PLAYBOOK saying a verification report
is not evidence. *Cost:* S.

**C-5 · A per-leg idle/total timeout, as a dispatch constant.**
*Witness:* §4 D6 — the frozen contract stated no timeout, leg M ran 2 h 06 m unbounded, and the
operator had to rule one mid-arc. The vendor's own README documents this exact failure mode
(`README.md:173`, Known Issues). *Shape:* `Dispatch-Lane` carries an idle cap and a total cap the
way it already carries `-Effort`. *Cost:* S. *Note:* the naive implementation is wrong — see D6
and D7; log bytes are not a liveness signal for a buffered transport, and a dot-blind file walker
cannot see a lane's workspace at all.

**Not proposed, deliberately:** adopting the Maister plugin into any repo. The operator's framing
was *improve OUR hub, not adopt a plugin that duplicates it*, and the measurement supports that
reading — same verdict, same defect count, 16× the cost. Rows 1, 9, 15 and 19 yield **no**
candidate: nothing there is shipped on either side that is worth copying.

## §4 — Cost, deviations, and what is INCONCLUSIVE

### Cost of this arc

| Item | Measured |
|---|---|
| Leg M development | **$48.53** (CLI-reported), 7809 s, 123 turns, 14 subagents |
| Leg M init (the run that counts) | **not exposed** — its wrapper was OOM-killed, so no JSON was written. ≈732 s derived from artifact mtimes. **No dollar figure is estimated** |
| Leg M discarded attempts | $2.11 (attempt 1, 429) + $0.51 (attempt 2, refused) = **$2.62**, kept as evidence |
| Leg D | **$3.00**, 1225 s, 51 turns, 0 subagents |
| terra ×2 | 91 s + 60 s wall-clock; `codex exec` exposes no cost — **unknown, not estimated** |
| Orchestration (this session) | not separately exposed by the harness — **unknown, not estimated** |

Per the anti-patterns: **no estimate appears anywhere a number is not exposed.**

### Deviations — all stated, none silent

Full record with evidence: `DEVIATIONS.md` in the arc's scratch. Summarised:

- **D1 — the contract's "14 rows" enumerates 15.** The enumeration governs; row 8 is excluded
  because the frozen text excludes it. Nothing dropped silently.
- **D2 — NC2 holds at both endpoints; the exception is only *during* the run.** BEFORE: 0 maister
  rows in the hub (`NC2-hub-plugin-list-BEFORE.txt`). AFTER teardown: **0 rows, and the install
  record is gone** from `~/.claude/plugins/installed_plugins.json` (`NC2-hub-plugin-list-AFTER.txt`)
  — so NC2 as literally written is **satisfied**. While the plugin was installed, the hub listed
  one row as `Scope: project · Status: ✘ disabled`; it was never installed there (the install
  record bound `projectPath` to clone M, and neither the hub's nor the user's `settings.json`
  carried a maister key). That row is unavoidable on this CLI: the plugin registry is machine-wide,
  so any known marketplace contributes a disabled row to every project, and both scope routes
  (`project`, then `local`) were tried and it survived both.
- **D3 — leg M was run three times and only the third counts.** Attempt 1 hit a **429 session
  limit** ($2.11, 24 turns) and, worse, with ai-council's project settings live it answered the
  repo's `Stop` backpressure hook instead of the prompt — committing a JOURNAL entry and a plugin
  registration without ever reaching `/maister:init`. Attempt 2 did the same and then asked a
  question. Both are **our transport, not Maister's behaviour**, so neither is scored against it.
  Clone M was reset to pristine and both legs re-run under `--setting-sources local`, which
  excludes those hooks — leaving the harness as the only variable. Artifacts kept.
- **D4 — a venv was built in each clone** (`pip install -e ".[dev]"`), a network fetch beyond the
  decision budget's "one named plugin". It is a precondition of m4, which the contract itself
  mandates. Done identically in both clones, reported rather than asked.
- **D5 — the FR2 baseline is not green** (5 failed / 933 passed at `7a3c057`), so m4 is scored as a
  delta. Both legs independently identified the same five and proved them pre-existing.
- **D6 — the architect ruled a per-leg timeout mid-arc**, the frozen contract having stated none.
  One correction was applied *in the ruling's spirit*: it names "no new bytes in the run log" as
  the idle test, but `claude -p --output-format json` **buffers all stdout to the end**, so that
  test reads 0 bytes for a healthy run and would have killed leg M immediately. Idle was measured
  as **age of the newest artifact write** instead. At the moment of the ruling leg M measured
  11.7 min idle, having just written both target files, so it was kept — and it completed on its
  own about two minutes before the cap would have fired.
- **D7 — my own liveness probe carried a bug I had to fix mid-arc.** It used
  `glob.glob('**', recursive=True)`, which **silently excludes dot-directories** — exactly the
  directories both legs write into (`.maister/`, and `.claude/worktrees/`, where our lane protocol
  puts leg D's entire workspace). Leg D measured as permanently idle and would have been killed as
  wedged at the 15-minute cap while working normally. Fixed to `os.walk`, re-verified at 0.0 min
  idle. Recorded because the *measuring instrument* nearly manufactured the finding.
- **D8 — an `audit-health` single-hook bypass was declared** on this audit's commits. Main advanced
  from this lane's branch point to `e3d2ac34` while the arc ran, and 18 first-parent merges there
  carry no JOURNAL anchor; `git show main:JOURNAL.md` greps 0 for four sampled SHAs, so the gap is
  real on main rather than tree-lag here. Draining it means writing JOURNAL entries, which a lane
  must not do (STANDING_RULINGS P-1). `SKIP=audit-health` was used, declared in the commit body;
  **every other gate ran and passed**. The anchor debt is the integrator's, and is reported here
  rather than absorbed.

### INCONCLUSIVE flags

- **The FR1 coverage criterion is missed on the strict reading, and I am not rounding it up.**
  "Execution witnesses for ≥80 % of cells": 21 of 30 cells are `RUNNING`, which is **70 %**. All 30
  carry *a* witness (artifact path, course locator, or recorded search), which is 100 % on the
  looser reading. On the strict reading **FR1 is INCONCLUSIVE at 70 %**, and the shortfall is
  structural: 8 of the 9 non-RUNNING cells are AJ-side capabilities that exist only in licensed
  course material and cannot be executed at all.
- **FR2 is NOT inconclusive.** Both legs completed a full workflow (`terminal_reason: completed`,
  m6 = 0), so the criterion's first branch is satisfied and the m6 branch is not needed.
- **FR3 is NOT inconclusive** — 10 items, every one with a locator, against a bar of ≥8.
- **`/maister:init`'s cost is unknown and stays unknown.** The run that produced the artifacts was
  OOM-killed before emitting its JSON, on a machine under memory pressure from other live sessions
  I would not kill. Its m1 is derived from mtimes and labelled as derived.
- **One task, one repo, one run per leg — n=1.** The 16× cost spread is large enough to act on and
  small enough a sample that it must not be quoted as a constant.

### Teardown

NC1 requires both clones deleted and nothing pushed; NC2 requires the plugin uninstalled. The
teardown and its verification are recorded in `TEARDOWN.md` alongside this arc's evidence.
