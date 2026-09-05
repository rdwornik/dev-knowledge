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
