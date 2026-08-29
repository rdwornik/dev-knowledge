All measurement done. Writing the artifact.

```
================================================================================
AUT-R3 — THE REPO AS A REINFORCEMENT ENVIRONMENT
Survey + blind-spot list · CLOUD, READ-ONLY · dispatched + executed 2026-08-29
================================================================================

LANE POSTURE, DISCHARGED
  Zero rows born. Zero tasks/ edits. Zero intakes. Zero ADRs. Zero commits, zero
  pushes. Working tree untouched; `git status` clean at entry and exit. Nothing
  below is filed — it is offered.

SUBSTRATE, DECLARED
  Invoked `python3` DIRECTLY (CPython 3.11.15, cloud image). No `uv run --locked`
  was attempted and no gate result is reported that I did not observe.
  CARRIED CAVEAT, first-class: pyproject declares `requires-python = ">=3.12"`.
  The image is 3.11.15 — BELOW the declared floor. Everything I ran, ran off-spec.
  Three declared deps are absent from the image (`click`, `rustworkx`, and the
  rest of the dev group), which bounded what I could execute — see LIMITS (§7).

  Ran clean:      funnel_coverage.measure() · governance_health.build_report()
                  telemetry_emit (import) · direct corpus counts over LESSONS.md
  Could NOT run:  funnel_lifecycle.measure()  — ModuleNotFoundError: click
                  file_purpose_graph          — ModuleNotFoundError: rustworkx
                  gen_handoff (FM-4 block)    — ModuleNotFoundError: click
  Network:        arxiv.org and infoq.com are BLOCKED by the egress proxy. Every
                  arXiv citation below is therefore cited by ID + title from
                  search-result metadata and is LABELLED "not read in full".
                  github.com, pypi.org and registry.npmjs.org WERE fetchable, so
                  all maturity numbers in §6 are primary-registry reads.


================================================================================
§1 — THE BLIND-SPOT LIST  (lead deliverable; ABSENT and PARTIAL only)
================================================================================

B1. THE WRITE-BACK ARC IS REAL BUT RUNS AT ~4%, AND NOTHING MEASURES IT.  [ABSENT]
  Measured on the live tree, 2026-08-29, by direct count over LESSONS.md:
      total entries (`^### `)                          315
      entries citing a `scripts/*.py` locator            12   (3.8%)
      entries citing STANDING_RULINGS.md or .claude/rules 11  (3.5%)
      entries mentioning a gate/hook at all              69   (21.9%)
      entries citing an ADR                              68   (21.6%)
      entries citing NO enforcement surface whatsoever  235   (74.6%)
  The `LESSONS -> rules -> gates` pattern is the arc's stated thesis. On its own
  corpus, roughly one lesson in twenty-six reaches code. That is not a criticism
  of the pattern — 3.8% may be the correct rate — but NO ORGAN COMPUTES THIS
  NUMBER. I had to write the count myself. There is a silent-rule ratchet over
  `protocols/` (baseline 443, `ecosystem/silent-rule-baseline.yaml`), a doc->code
  edge index over four declaration docs (`ecosystem/doc-code-edge.yaml`), and an
  enforcement-coverage reporter over five hub organs
  (`scripts/enforcement_coverage.py`) — and none of them takes LESSONS.md as
  input. `grep -rn LESSONS scripts/*.py` returns freshness exclusions
  (`canonical_freshness_gate.py:18`), a header normalizer
  (`scripts/normalize_headers.py:3`), a deletion guard
  (`scripts/nopack_sandbox.py:228`) and a citation-role classifier
  (`scripts/preflight_contract.py:109`). LESSONS.md is PROTECTED, INDEXED and
  NORMALIZED. It is never READ FOR CONTENT by anything that produces a rule.
  THE GAP IN ONE LINE: the memory store has no gradient. Experience is written
  in; nothing measures whether it came out the other side as enforcement.

B2. NO OUTCOME SIGNAL. THE LOOP HAS NO REWARD.                          [ABSENT]
  A reinforcement environment needs a scalar (or at least an ordinal) that says
  whether the last change made things better. This repo has:
    - many state measures (audit checks, funnel counts, ratchets, coverage)
    - a direction surface (`scripts/gen_trend_dashboard.py` -> ecosystem/trends.html)
    - and, by its own docstring, THREE ABSENT SERIES:
        commit-gate ms   store `logs/TELEMETRY.db`  ...  "ABSENT"
        suite wall-time  "-- no store exists --"    ...  "ABSENT"
        per-model quality "-- no store exists --"   ...  "ABSENT"
      (`scripts/gen_trend_dashboard.py`, the input table in the module docstring)
  So the only three series that would say "did the change help?" are exactly the
  three with no store. The dashboard is scrupulous — it renders them as labelled
  absences rather than inventing history — but the honesty does not close the gap.
  THE GAP: there is a rich observation space and no reward function. Every organ
  answers "what is the state"; none answers "did the last ruling improve it".

B3. TELEMETRY IS ONE-CALL-SITE-WIRED AND THE STORE IS UNPROVEN.        [PARTIAL]
  `scripts/telemetry_emit.py` shipped LIBRARY-ONLY by its own scope line ("it
  wires nothing"). Since then exactly ONE call site has landed:
  `scripts/block_commit_on_main.py:66` (`import telemetry_emit as _te`). Row
  `[#529]` remains open on four legs, of which leg 1 is "wire the call sites".
  `logs/` on this checkout contains ONE file — `TOKEN-LOG.md`. `logs/TELEMETRY.db*`
  is gitignored (`.gitignore:110`), so its absence here proves nothing about the
  operator's machine and I say so rather than scoring it.
  THE GAP: the telemetry->trends->rulings loop is built from BOTH ends and joined
  in the middle by one hook. Until N call sites emit, `trends.html`'s telemetry
  panels render an absence, and the loop's first leg is a design, not a signal.

B4. NOTHING MEASURES THE DECAY OF A LANDED RULE.                        [ABSENT]
  Every ratchet in the repo is MONOTONIC-BY-CONSTRUCTION: the silent-rule baseline
  "may be LOWERED or held. It may NOT be raised"
  (`ecosystem/silent-rule-baseline.yaml`, header). The funnel baseline works the
  same way. This is correct for preventing regression and USELESS for detecting
  a rule that landed, was obeyed for a week, and is now routinely bypassed.
  There is no organ that asks: of the gates armed in the last 90 days, which
  ones have FIRED? which have never fired? which are bypassed with `--no-verify`?
  `scripts/enforcement_coverage.py` measures FIRING-NOT-PRESENCE — the right
  question — but its unit is CONSUMER REPOS x FIVE HUB ORGANS, and its own
  docstring records "on the live fleet no consumer is a candidate for any organ",
  so its fire path is exercised only by hermetic fixtures. Nothing runs that
  question against the ~20 hub-local pre-commit hooks in CLAUDE.md §9.
  THE GAP: a gate that never fires is indistinguishable, in every surface this
  repo has, from a gate that works perfectly. Those are opposite facts.

B5. THE FUNNEL IS 90% UNCOVERED AND THE RATCHET CANNOT SHRINK IT.       [PARTIAL]
  Live measurement, `funnel_coverage.measure(Path('.'))`, run 2026-08-29:
      corpus         798        dispositioned   78        pending   2
      uncovered      718        ledgers          1        dangling  0   malformed 0
      -> disposition rate 9.8%
  Committed baseline (`ecosystem/audit-funnel-baseline.json`): corpus 797,
  uncovered 717 — so the live tree is exactly +1 artifact, +1 uncovered. The
  ratchet is holding the line and the line is at 90% uncovered. Also note the
  baseline's `measured_at`, `measured_at_sha` and `provenance` are all EMPTY
  STRINGS, so the committed number carries no provenance of its own.
  There is exactly ONE ledger in an 798-artifact corpus. ADR-111's funnel is
  therefore enforced against a denominator that one document is expected to serve.
  THE GAP: this is a coverage ratchet, not a coverage plan. It refuses to get
  worse; it has no mechanism that makes it get better, and at 9.8% "no audit is
  wasted" is aspiration with a gate attached to the wrong end.

B6. NO RETRIEVAL LAYER. THE BOOT SURFACE IS HAND-CURATED.               [ABSENT]
  Every boot path in CLAUDE.md §1/§6 is an ENUMERATED READ: this file, then
  ESSENTIALS, then the newest handoff bundle, then the last 5 JOURNAL entries.
  Selection is by RECENCY and by HUMAN CURATION. There is no learned or computed
  "what matters for THIS task" surface. `scripts/file_purpose_graph.py` is the
  nearest thing and is explicitly QUERY-ON-DEMAND (`why <path>`), not a ranker:
  it answers purpose/consumers/edges for a named path, and refuses on a path
  nothing explains. It cannot answer "given this brief, which 8 of 798 audits
  matter" — that is a retrieval question and no organ takes it.
  THE GAP: the repo's memory has grown past the point where recency is a good
  index (798 audits, 315 lessons, 435 ruling entries, 514+ tasks-derived rows).
  Curation is doing a retrieval job. This is the ONE blind spot where the small-
  local-model shelf (§4, §6 Shelf 2) has a direct, evidence-backed answer.

B7. THE EX-ANTE CRITERION IS FROZEN BUT NEVER SCORED AFTERWARD.         [PARTIAL]
  `scripts/preflight_contract.py --freeze` ships four pre-freeze predicates and
  demonstrably works — CLAUDE.md §12 records it reproducing all three known
  batch-1 contract errors plus a fourth the retrospective missed. That is the
  EX-ANTE half of ADR-108 §B, and it is live.
  What is absent is the EX-POST half: nothing reads a frozen contract back after
  the lane lands and scores DELIVERED-vs-FROZEN. `governance_health` gets closest
  — it quotes "what it bought" verbatim from close packets and renders
  `no value evidence` rather than inventing a sentence. Observed live today it
  returned `close packets read: 6` and `coverage: 0/0 rows carry sole value
  evidence` (window unavailable because FM-4's emitter could not import).
  THE GAP: contracts are checked before the work and narrated after it. Nothing
  computes the delta. In RL terms: the environment specifies the reward but never
  evaluates the episode against it.

B8. NO COUNTERFACTUAL, NO NEGATIVE MEMORY.                              [ABSENT]
  ADR-111's funnel has a REJECTED bucket and `STANDING_RULINGS.md` records
  rejections so they are not relitigated — good, and rare. But rejections are
  stored as PROSE IN A LIVING FILE, unindexed and unqueryable. The
  `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:71` line is the
  archetype: eighteen rejected candidates in ONE semicolon-delimited prose line
  ("agent-orchestration frameworks (LangGraph/CrewAI class — wrong layer) ·
  standalone worktree managers · external SaaS dead-man services · ..."). That
  line is the repo's most information-dense negative-result store and it is
  greppable only if you already guess the word.
  THE GAP: the environment remembers what it did. It barely remembers what it
  DECLINED, and not in a form any organ can consult before a new proposal.

B9. THE "AXIS (D) ORGANS" CANNOT ALL RUN IN THE SAME PROCESS.           [PARTIAL]
  Not a doctrine gap — an operational one, and I hit it directly. Of the five
  organs the brief names, THREE fail to import without the full dev group, and
  their failures cascade: `governance_health` renders every FUNNEL HEALTH field
  `unavailable` because `gen_handoff` cannot import `click`. The degrade is
  CORRECT and I want that on the record as a PRESENT property (§2 P7) — but the
  practical consequence is that the funnel's headline numbers are unavailable in
  any environment that is not a full `uv sync --locked` checkout, including every
  cloud reconnaissance seat like this one.
  THE GAP: the measurement surface is coupled to the CLI layer. A pure-stdlib
  `measure()` path for the four FM-4 fields would make the funnel readable from
  any seat. `funnel_coverage` already proves this is achievable — it imported and
  ran clean on bare CPython 3.11.15 with zero third-party deps.


================================================================================
§2 — THE CHECKPOINT LIST (axis d): equilibrium properties vs LIVE organs
================================================================================
Scored against what I READ and, where possible, RAN. I have deliberately kept the
PRESENT column short. Where a property is half-built I scored PARTIAL, not PRESENT.

P1  Append-only experience store
    PRESENT. `LESSONS.md` (315 entries), `logs/TOKEN-LOG.md`, `JOURNAL.md`
    (newest-first). Enforced by CLAUDE.md §5 rules 1-2 and guarded from deletion
    by `scripts/nopack_sandbox.py:209,228` (names LESSONS.md explicitly as a file
    a sandbox may not delete over one row). Immutability of ADRs/audits/handoffs
    is enforced at tool level by the `PreToolUse` guard
    `block_immutable_edits.py`. This is the strongest leg in the whole design.

P2  Experience -> enforcement conversion
    ABSENT as a mechanism; sparse as a practice. See B1. 12/315 lessons reach a
    `scripts/*.py` locator. No organ takes LESSONS.md as input for rule derivation.

P3  Deterministic gate mesh (the "environment dynamics")
    PRESENT, and it is the repo's genuine moat. ~20 pre-commit/commit-msg/pre-push
    hooks (CLAUDE.md §9), several fail-CLOSED by explicit design
    (`block_ff_push.py` exit 2 since ADR-85 amend. §A6; `block_unanchored_push.py`
    exit 2). The ADR-85 §A5 reasoning is the sharpest thing in the corpus and I
    quote it because it generalizes: "an organ that can be exhausted cannot carry
    teeth" — witnessed at nine identical Stop-hook firings, zero enforcement
    pressure. That is a real, dated, negative result about hook placement and it
    is better than most of the published literature on agent guardrails.

P4  Graph / structural index over the corpus
    PARTIAL. `scripts/file_purpose_graph.py` joins FIVE previously-disjoint
    surfaces (doc-code-edge.yaml, the audits index, [#595] citations both
    directions, tasks/ depends-on, deploy manifests) into one rustworkx graph and
    exposes `transitive_consumers()` = `rustworkx.ancestors`. Real capability.
    MISSING: it is a `why <path>` oracle, not a ranker, and it is governed-set-only
    ("a path is governed iff at least one of the five inputs names it"). It cannot
    answer a relevance query. Could not execute here (no rustworkx).

P5  State measurement / ratchets
    PRESENT. silent-rule ratchet (detector-pinned, `silent-rule-v5`, baseline 443,
    58 files, sha 236da477); funnel-coverage ratchet (baseline 797/717);
    audit-health as a blocking pre-commit gate. Note the ratchets are all
    monotonic-only — see B4 for what that costs.

P6  Trend / direction surface
    PARTIAL. `gen_trend_dashboard.py` exists, is analyst-grade, computes a
    direction verdict per panel, and reads only from git + TELEMETRY.db (no second
    store). But 3 of its 9 series are ABSENT for want of a store (B2), one is
    SPARSE, and one has 2 revisions. A direction verdict over 2 points is a line,
    not a trend, and the module says so.

P7  Honest degradation / refusal-to-invent
    PRESENT, and unusually strong — I verified it by OBSERVATION, not by reading.
    Running `governance_health.build_report()` in a deps-incomplete environment
    produced, verbatim:
        FM-4 emitter: unavailable — gen_handoff did not import — ...No module named 'click'
        intakes consumed-unarchived: unavailable
        ...
        (no closed rows in this window, or the window is unavailable)
    Not a zero. Not a stale cache. Not a plausible-looking number. Six
    independently-degrading fields plus a resolution report. `funnel_lifecycle`'s
    docstring makes the same commitment structurally ("every Z-G4 cannot-compute
    condition raises; the adapter renders every one of them `fail`"). Against the
    literature in §3, this is the property most agent-memory systems lack outright.

P8  Ex-ante acceptance criterion, frozen
    PRESENT. `scripts/preflight_contract.py --freeze`, four predicates, tests.
    CLAUDE.md §12 v2.68 records it catching a fourth error the human retrospective
    missed — an actual, dated superiority result for the mechanism over the habit.

P9  Ex-post scoring of that criterion
    PARTIAL -> effectively ABSENT. See B7. `governance_health` quotes value
    evidence; nothing scores delivered-vs-frozen.

P10 Outcome / reward signal
    ABSENT. See B2. This is the single largest structural gap between this repo
    and anything the RL framing would call an environment.

P11 Retrieval / relevance over the accumulated corpus
    ABSENT. See B6. Boot is enumerated and recency-ordered.

P12 Negative memory (what was tried and rejected), queryable
    PARTIAL. Rich in substance (STANDING_RULINGS.md, 435 entries; the intake
    rejection lines; the model-bus REJECT verdicts with reasons), zero in
    machine-readability. No index, no schema, no organ consults it pre-proposal.

P13 Credit assignment (which change caused which delta)
    ABSENT. `journal_anchor.py` binds a JOURNAL entry to a SHA range and
    `block_unanchored_push.py` enforces it — that is PROVENANCE, which is a
    necessary precondition and not the same thing. Nothing attributes a metric
    movement to a commit.

P14 Bypass / exception accounting
    PARTIAL. The escape hatches are deliberately narrowed to ONE (`git push
    --no-verify`) and made non-silent by the `journal_spine_anchor` audit
    backstop (a gap is FAIL, not WARN). That is good design. But there is no
    COUNT: nobody can say how many bypasses happened last month. See B4.

SCORE, stated plainly rather than averaged:
  PRESENT 6 (P1 P3 P5 P7 P8 + P5's ratchets) · PARTIAL 5 · ABSENT 5.
  The PRESENT column is concentrated entirely in ENFORCEMENT and HONESTY.
  The ABSENT column is concentrated entirely in FEEDBACK: outcome, retrieval,
  credit assignment, decay, negative-memory query. That is a coherent shape and
  it is worth naming as such: THIS REPO IS AN EXCELLENT ENVIRONMENT AND HAS NO
  LEARNING SIGNAL. It is the half of RL that people find boring, built to an
  unusually high standard, with the interesting half absent.


================================================================================
§3 — AXIS (a): THE REPOSITORY AS THE PERSISTENT MEMORY
================================================================================
QUESTION: does `LESSONS -> rules -> gates` have a named antecedent?
ANSWER: the first arrow does. The second does not. Stated precisely below.

WHAT THE LINEAGE ACTUALLY DID (verified against descriptions; papers not read in
full — arxiv.org is egress-blocked from this seat, so these are cited by ID and
title and I am not quoting internals I could not open):

  Reflexion (arXiv 2303.11366) — accumulates verbal self-critiques IN THE CONTEXT
    WINDOW. No structured retrieval, no persistence beyond the episode buffer.
    NOT an antecedent for a repo-as-weight-store: its memory dies with the run.
  Voyager (arXiv 2305.16291) — builds a SKILL LIBRARY of executable code, curriculum-
    driven, in Minecraft. This IS a persistent, executable memory store, and it is
    the closest structural ancestor to "write experience back as code". Difference,
    and it is the whole difference: Voyager's library is CAPABILITY (things the
    agent can now do). This repo's gates are CONSTRAINT (things the agent can no
    longer do). Nobody in that lineage writes experience back as REFUSAL.
  Generative Agents (arXiv 2304.03442) — memory stream + importance-weighted
    retrieval + reflection into higher-level statements. Contributes the RETRIEVAL
    half this repo lacks entirely (B6/P11) and contributes nothing on enforcement.
  ExpeL (arXiv 2308.10144) — "LLM Agents Are Experiential Learners": extracts
    natural-language INSIGHTS/RULES from a pool of successful and failed
    trajectories, stores them, retrieves them at inference. This is the nearest
    NAMED antecedent for `LESSONS -> rules`. It stops there: the rules are
    retrieved into a prompt. They are never compiled into anything that can refuse.

  THE STRONGEST ANTECEDENT, and it postdates the whole list above:
  ACE — "Agentic Context Engineering: Evolving Contexts for Self-Improving Language
  Models" (arXiv 2510.04618; Stanford / SambaNova / UC Berkeley; repo
  github.com/ace-agent/ace, VERIFIED by direct fetch: 1.3k stars, 164 forks,
  12 commits on main, launched Nov 2025). Generator -> Reflector -> Curator loop
  writing INCREMENTAL DELTAS to a structured playbook in the literal format
  `[section-ID] helpful=X harmful=Y :: content`, with per-bullet usefulness counts.
  Reported: +10.6% on agent benchmarks, +8.6% on finance reasoning; ReAct+ACE 59.4%
  vs IBM CUGA 60.3% on AppWorld with the smaller open DeepSeek-V3.1 (reported
  figures, from the repo/press summaries — I could not open the paper).
  TWO ACE CONCEPTS THIS REPO SHOULD ADOPT AS VOCABULARY, because it has both
  diseases and no name for either:
    - "BREVITY BIAS": automated optimization drifts toward short generic
      instructions that lose domain-specific detail. This repo runs a HARD
      200-line CLAUDE.md budget (§12 v2.68: "opened 197/200 ... Closes 196/200,
      headroom 4"). That budget is brevity bias INSTITUTIONALIZED. It may still be
      right — but ACE gives the cost a name and a measured direction.
    - "CONTEXT COLLAPSE": iterative full rewrites erode information. The repo's
      own countermeasure is the ADR-49/65 "condense to git history" move, applied
      three times to CLAUDE.md §12. ACE's finding is that DELTA-APPEND beats
      REWRITE. `LESSONS.md` is delta-append and is therefore already on the right
      side. `CLAUDE.md` §12 is rewrite-and-condense and is therefore on the wrong
      side, by ACE's own argument.

  ALSO NAMED, weaker, and I flag them as thin because I verified only their
  existence in a survey list and not their contents: Meta-Reflexion (2025,
  distills reflections into rules — the closest published analogue to
  rules-as-memory); AEL / "Agent Evolving Learning" (arXiv 2604.21725, Apr 2026,
  claims to jointly evolve tools AND memory, and its related-work section is the
  source of my Reflexion/Voyager/ExpeL characterizations above); RPMS
  "Rule-Augmented Memory Synergy" (arXiv 2603.17831). HYPOTHESIS, not claim: the
  2026 arXiv IDs are consistent with real preprints but I could not open any of
  them, and a survey's characterization of its own competitors is a biased source.
  A reader should re-verify before citing these three.

WHERE OUR PATTERN HAS NO NAMED ANTECEDENT — stated as the survey's finding:
  I found NO published work in which an agent's accumulated experience is
  compiled into a DETERMINISTIC PRE-COMMIT REFUSAL that binds the agent itself.
  Every system above writes memory into CONTEXT — a prompt, a playbook, a
  retrieved insight — and the agent may ignore it. This repo writes memory into
  an exit code. `block_ff_push.py` returning 2 is not advice.
  THAT IS THE ORIGINAL CONTRIBUTION, and it is worth stating in exactly those
  terms in the thesis: the literature's memory is ADVISORY; this repo's memory is
  ADJUDICATIVE. The trade is legibility for bindingness — a gate cannot express a
  nuance, which is why 74.6% of lessons never became one, and that ratio is the
  honest price of the design rather than a defect in it.

WHAT THE REPO ALREADY KNEW, credited: `docs/decisions/ADR-42-handoff-format-v3.md:87`
and `JOURNAL.md:25560` already name "LangGraph, AutoGen, Cline Memory Bank" as the
industry-pattern comparison set. The Cline Memory Bank comparison is the most apt
of the three and is the one nobody has taken further — it is markdown-as-memory
with no enforcement, i.e. exactly this repo minus the gates.


================================================================================
§4 — AXIS (b): SMALL LOCAL MODELS PER REPOSITORY
================================================================================
FINDING, one line: the evidence is strong and one-directional — small local models
are competitive-to-excellent at RETRIEVAL and RANKING, and measurably behind at
AGENTIC DECISION-MAKING. Every number below is a reported figure from a primary
blog/benchmark page or a search-surfaced paper abstract, labelled by source.

WHAT THEY ARE GOOD AT — retrieval, ranking, "where is what"
  - Qodo-Embed-1-1.5B scores 68.53 on CoIR, stated to surpass 7B-class models;
    Qodo-Embed-1-7B scores 71.5. (qodo.ai product blog — VENDOR SOURCE, treat the
    ranking claim as marketing and the CoIR number as reproducible-in-principle.)
  - voyage-code-3 reports +13.80% avg over OpenAI-v3-large and +16.81% over
    CodeSage-large across 32 code-retrieval datasets. (blog.voyageai.com — VENDOR
    SOURCE, and a hosted API, so it fails the local constraint anyway. Cited for
    the SIZE OF THE HEADROOM, not as a candidate.)
  - CoIR itself (arXiv 2407.02883) is the standardized code-IR benchmark that
    makes these comparable. Not read in full.
  A 1.5B embedder that beats 7B models at code retrieval is the shape of the whole
  finding: retrieval quality saturates at small scale.

WHAT THEY ARE NOT GOOD AT — decisions, generation on hard agentic tasks
  - "The best open-weight models now score around 80% on SWE-bench Verified versus
    roughly 90-95% for the top proprietary models, so the very hardest agentic
    problems still favor the cloud." (surfaced via search over 2026 local-model
    guides — SECONDARY SOURCE, and SWE-bench Verified numbers above ~75% should be
    treated with suspicion generally given contamination history. Directionally I
    am confident; the specific percentages I would not put in a thesis unquoted.)
  - Qwen3-Coder-Next: 44.3% SWE-Bench Pro; >70% SWE-bench Verified under the
    SWE-Agent scaffold; 80B total / 3B active MoE, Apache-2.0. (qwen.ai blog —
    VENDOR SOURCE.) Note what that architecture implies for THIS repo: 3B ACTIVE
    does not mean 3B RESIDENT. You still host 80B of weights. "Small model per
    repository" and "80B MoE" are not the same deployment story, and the guides
    that conflate them are wrong.
  - Qwen2.5-Coder-7B at 88.4% HumanEval is real and IRRELEVANT to this repo:
    HumanEval measures function-level synthesis from a docstring. Nothing this
    repo does looks like that. I flag it because it is the number that will be
    quoted at the operator, and it does not transfer.

THE RESULT THAT MATTERS MOST HERE, AND IT CUTS AGAINST EMBEDDINGS ENTIRELY
  "BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation
  Paradigms" (arXiv 2607.26497). Reported: BM25 retains 50.5 at full scale vs
  30.7 for file-system agents and 29.9 for dense retrieval; the crossover is
  around 10M corpus tokens, and BM25 leads every tier above it, margin approaching
  20 points. NOT READ IN FULL — arxiv is blocked from this seat — so I label this
  a strong-but-unverified citation, and it is the single most important line item
  in this section, so it deserves a real read before anything is built on it.
  Corroborating direction, same caveat: "Reformulate, Retrieve, Localize"
  (arXiv 2512.07022) reports query reformulation boosting BM25 first-file
  localization by 36%; SpIDER (arXiv 2512.16956) reports beating BM25 only by
  adding SPATIAL/GRAPH STRUCTURE to dense embeddings.
  READ TOGETHER, the three say: lexical + structure beats dense; dense wins back
  only when you give it a graph. THIS REPO ALREADY HAS THE GRAPH
  (`file_purpose_graph.py`, rustworkx, five joined inputs).

SIZING THIS REPO AGAINST THE CROSSOVER — the decisive number, computed here:
  The corpus is markdown governance text, not source. At ~117 B/line (the figure
  AGENTS.md itself uses for this corpus) and a corpus in the low tens of MB, this
  repo is ORDERS OF MAGNITUDE BELOW the ~10M-token crossover where dense retrieval
  loses. That means the BM25-wins-at-scale result DOES NOT CONDEMN embeddings
  here — it condemns them for large codebases. HYPOTHESIS, and I flag it as mine:
  at this corpus size, the honest expectation is that BM25/ripgrep and a local
  embedder perform SIMILARLY, and the embedder's marginal value is not recall but
  the ability to answer a query with no shared vocabulary ("what did we decide
  about always-running servers" — a query the repo's own model-bus audit records
  FAILING as a grep, at `docs/audits/2026-08-23-technical-research-model-bus.md`:
  "I could not locate the no-always-running-servers rule in any canonical in-repo
  doc (grep ... returns nothing)"). THAT specific failure — a real, dated,
  in-repo grep miss on a load-bearing constraint — is the strongest argument for
  a local index in the entire survey, and it is the repo's own evidence, not mine.

CONCLUSION FOR AXIS (b): a small local model earns its place HERE as a
  vocabulary-bridging retriever over a corpus a grep already mostly covers — a
  narrow, cheap, testable win. It earns NOTHING as a decision-maker, a reviewer,
  or a generator, and every published number that suggests otherwise is measuring
  function synthesis, not governance judgment.


================================================================================
§5 — AXIS (c): THE DIVISION-OF-STRENGTHS TRIAD — WHO BUILT IT, WHAT FAILED
================================================================================
The triad = frontier LLM + deterministic SE machinery + a local learned index.
Negative results first, because they are the load-bearing ones.

NEGATIVE RESULT 1 — SOURCEGRAPH BUILT THE TRIAD AND DELETED THE THIRD LEG.
  This is the closest anyone has come to the exact architecture, and it is the
  most instructive failure available. Sourcegraph had, simultaneously: a
  best-in-class deterministic code graph (a decade of code search + precise
  cross-repo navigation), a frontier LLM layer (Cody), and embeddings as the
  retrieval index. Per Sourcegraph's own posts and docs (sourcegraph.com/blog/
  how-cody-understands-your-codebase; sourcegraph.com/docs/cody/faq), EMBEDDINGS
  WERE REMOVED and replaced by Sourcegraph Search. Stated reasons:
      - scaling: needed retrieval that works across repos and at greater repo size
      - operational debt: embeddings setup + refresh was maintenance-heavy
      - data boundary: it required sending code to a third-party embedding provider
      - vector-DB management complexity
  They kept the graph, kept the LLM, and DROPPED THE LEARNED INDEX in favor of
  ten-year-old lexical search infrastructure. This is the BM25-wins result (§4)
  arriving independently from production rather than from a benchmark.
  Then the product itself contracted: Cody Free and Pro were discontinued
  2025-07-23 and Sourcegraph launched Amp for individuals; Cody survives as
  Enterprise-only (~$59/user/mo, annual). (Multiple 2026 secondary reviews concur;
  the discontinuation date is consistently reported. I treat the DATE as
  well-attested and the pricing as secondary.)
  DIRECT IMPLICATION FOR US, and it is uncomfortable: the two constraints that
  killed Sourcegraph's embedding leg — third-party data egress and refresh
  maintenance — are BOTH constraints this repo has independently adopted (private
  governance repo; "no always-running servers"). We would be re-running their
  experiment with their two blockers already binding. That is a reason to make any
  index LOCAL, SMALL and RECOMPUTABLE-FROM-SCRATCH, or not to build it.

NEGATIVE RESULT 2 — THE ORCHESTRATION LEG KEEPS CONSOLIDATING AWAY.
  Measured directly from PyPI, 2026-08-29 (primary registry reads):
      pyautogen           0.10.0   last upload 2025-07-15   0 files in 90d
      autogen-agentchat   0.7.5    last upload 2025-09-30   0 files in 90d
  BOTH AutoGen lines are ~11-13 months without a release. Microsoft merged AutoGen
  and Semantic Kernel into "Microsoft Agent Framework", 1.0 shipped 2026-04-03,
  and the migration guidance is explicit that SK/AutoGen are the maintenance-mode
  path. (Microsoft Learn + multiple 2026 write-ups; the merge is well-attested,
  the exact 1.0 date is from secondary posts.)
  This vindicates, on maintenance grounds rather than architectural ones, this
  repo's 2026-04-24 decision to skip the class
  (`docs/audits/2026-04-24-council-28-29-consolidated-actions.md:117`, P3-3).

NEGATIVE RESULT 3 — THE MEMORY-LAYER BENCHMARKS ARE NOT TRUSTWORTHY.
  Verified by direct fetch of the primary artifact: github.com/getzep/zep-papers
  issue #5, filed 2025-05-08 by Mem0's CTO, alleging Zep's 84% LoCoMo figure is
  inflated ~25.56pp by including an explicitly-excluded adversarial category in
  the numerator while excluding it from the denominator, plus inconsistent
  baselines (modified system prompt/retrieval template; single run vs 10-run
  averages). Mem0's corrected figure: 58.44% ± 0.20. Zep's public rebuttal claims
  75.14% and alleges misconfiguration. NO RESPONSE APPEARS IN THE ISSUE ITSELF.
  Independent commentary notes neither result is third-party reproducible because
  the contested choices are not prescribed by the benchmark.
  CONCLUSION: do not let any number from the agent-memory vendor space into a
  decision here. The two market leaders publicly accuse each other of a ~26pp
  and a ~17pp error respectively, on the same benchmark, and neither has been
  independently replicated.

WHO HAS ACTUALLY BUILT SOMETHING LIKE THE TRIAD AND SURVIVED
  - Aider's repo-map: tree-sitter (deterministic parse) + a PageRank-style graph
    ranking over symbol references, NO EMBEDDINGS. This is "deterministic machinery
    + graph-learned ranking + frontier LLM" with the learned leg implemented as
    graph centrality rather than as a model. Directly analogous to what
    `file_purpose_graph.py` could become at near-zero cost. HYPOTHESIS-LABELLED:
    I did not fetch Aider's source this pass; the architecture is widely described
    and I am confident in the shape, less so in current specifics.
  - Sourcegraph post-embeddings: graph + lexical + LLM. See above — this is the
    triad with the learned leg deliberately amputated, and it is the config they
    chose after running the other one in production.
  - Google's internal / Moderne-OpenRewrite / CodeQL-class systems: deterministic
    program representation + LLM, no learned index. Named for completeness;
    I verified nothing about them this pass and they are HYPOTHESIS-level here.
  THE PATTERN ACROSS ALL SURVIVORS: the deterministic leg and the frontier leg are
  stable. THE LEARNED INDEX IS THE LEG THAT GETS CUT. Nobody I found is running a
  production triad where a learned per-repo index is load-bearing.

WHAT THAT MEANS FOR THIS ARC, stated as a recommendation rather than a finding:
  Do not build the triad. Build the graph leg out (it is 60% built and it is the
  leg that survives everywhere), and treat the learned index as an OPTIONAL,
  DELETABLE Tier-S probe whose only job is vocabulary bridging (§4). If it is
  deleted in a month, the graph and the gates are unaffected. That is the correct
  coupling and it is what every survivor above converged on independently.


================================================================================
§6 — APPENDIX: LIBRARY-FIRST SWEEP
================================================================================
MATURITY DATA IS PRIMARY: every version/date/count below is a direct read of
pypi.org/pypi/<pkg>/json or registry.npmjs.org, performed 2026-08-29 from this
seat. "files/90d" = distribution files uploaded since 2026-06-01.

CARRIED CONSTRAINT applied per row: Windows wheel present? installable under
pinned uv 0.11.19 with requires-python >=3.12? server-dependent? The rustworkx
precedent is the bar — prebuilt hash-pinned `cp310-abi3-win_amd64` wheel, measured
in-lane, no fallback taken.

RECONCILIATION FIRST, as instructed — the prior LangChain verdict IS LOCATABLE:
  `docs/audits/2026-08-23-technical-research-model-bus.md:243-246` — "langchain /
  LangGraph — REJECT, already measured", pointing back to
  `docs/archive/2026-04-24-multi-agent-debate-patterns.md:44,185`, and noting
  ai-council runs its own PROVIDER_CLASSES. Upstream of that:
  `docs/audits/2026-04-24-council-28-29-consolidated-actions.md:117` (P3-3, "Skip
  — AI Council already implements proposer-critic-synthesizer at solo-dev scale";
  reopening trigger: "team grows beyond solo, or AI Council proves insufficient").
  And `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:71` lists
  "agent-orchestration frameworks (LangGraph/CrewAI class — wrong layer)".
  RE-ASSESSED AT TODAY'S SCALE, and the verdict CHANGES ITS REASON WITHOUT
  CHANGING ITS OUTCOME. The 2026-04 reason ("AI Council already does debate at
  solo-dev scale") is now the WRONG reason — the repo today runs parallel worktree
  lanes, epic lanes, cloud lanes, a merge queue and an integrator, which is
  genuinely multi-agent orchestration at a scale the 2026-04 note did not
  contemplate. The reopening trigger arguably fired. The verdict nonetheless holds
  on the 2026-08-06 reason, which is the durable one: WRONG LAYER. LangGraph is a
  state machine over LLM CALLS. This repo's lane plumbing is a state machine over
  GIT WORKTREES, PRE-COMMIT HOOKS AND A MERGE QUEUE — processes, filesystems and
  exit codes, not model invocations. LangGraph cannot hold a worktree, cannot
  install a hook, and cannot make a push fail. See the hypothesis attack below.

THE HYPOTHESIS I WAS ASKED TO ATTACK, NOT CONFIRM:
  "Could LangGraph-class state machines REPLACE hand-rolled lane plumbing while
  our gates stay?"
  ATTACKED, and it does NOT survive — for a reason I did not expect and that is
  worth more than the verdict. The lane plumbing is not a state machine that
  happens to be hand-rolled. Read `/lane-boot` and `/lane-integrate`: the lane
  lifecycle is provision-a-worktree -> seed ecosystem/*/state.yaml -> load a frozen
  contract -> state a decision budget -> ... -> serial merge queue -> a
  refuse-to-finish checklist. Every transition is a GIT or FILESYSTEM effect
  governed by CLAUDE.md §5 rule 9 ("no leftovers ... the provision->cleanup
  round-trip must leave the tree identical"). LangGraph's state is a Python object
  with a checkpointer. Adopting it would mean maintaining a SECOND state model
  alongside git's — and git is already the durable one. The failure mode is
  precise and nameable: TWO ANSWERS TO "WHAT STATE IS THIS LANE IN", which is
  exactly the defect class `funnel_lifecycle.py`'s own docstring says the FM batch
  exists to remove ("a second answer to 'is this intake consumed?' is precisely
  the defect"). REJECT — and record the reason as WRONG SUBSTRATE (git is the
  state store) rather than the weaker "wrong layer".
  ONE CONCESSION, because the hypothesis is not worthless: the lane DISPATCH
  surface — deciding which lanes exist, their dependencies, and what runs in
  parallel — IS a genuine DAG and is currently prose (PLAYBOOK Ch8) plus
  `gen_lane_contract.py` shape-checking. That sub-problem does not need LangGraph;
  it needs the graph library ALREADY DECLARED (rustworkx, R-A). Zero new deps.

--------------------------------------------------------------------------------
SHELF 1 — AGENT ORCHESTRATION
--------------------------------------------------------------------------------
| candidate | provides | maturity (primary, 2026-08-29) | verdict vs incumbent | cheapest experiment |
|---|---|---|---|---|
| LangGraph | stateful graph/state-machine over LLM calls, checkpointing, HIL | langgraph 1.2.11, last upload 2026-08-11, 18 files/90d, 276 releases — HEALTHY | REJECT (re-affirmed, reason UPGRADED to wrong-substrate). Incumbent: PLAYBOOK Ch8 dispatch + `gen_lane_contract.py` + worktree lanes. Pure-python wheel, would install fine — installability is not the objection | NONE WARRANTED. If revisited, the Tier-S probe is: model ONE past batch's lane DAG in LangGraph and check whether it can express "worktree removed and verified removed". It cannot. 30 min to falsify |
| LangChain | LLM abstraction layer | langchain 1.3.18, 2026-08-28, 36 files/90d, 514 releases — HEALTHY but enormous | REJECT, already measured (`...model-bus.md:243`). Reason unchanged: no consumer; ai-council owns PROVIDER_CLASSES | none |
| AutoGen | multi-agent conversation patterns | pyautogen 0.10.0 (2025-07-15, 0/90d); autogen-agentchat 0.7.5 (2025-09-30, 0/90d) — **BOTH STALLED**; succeeded by Microsoft Agent Framework 1.0 (2026-04-03) | REJECT on maintenance. This is now a CITABLE rejection: re-proposing AutoGen needs a new package, not a new argument | none |
| CrewAI | role-based crew orchestration | crewai 1.15.18, last upload 2026-08-29 (today), **212 files/90d across 425 releases** — hyperactive | REJECT. The churn is the objection, not the health: 212 uploads in 90 days is a moving target for a repo whose whole thesis is pinned, reproducible environments (ADR-106) | none |
| Microsoft Agent Framework | AutoGen+SK merged, workflows, state mgmt, telemetry | 1.0 shipped 2026-04-03 (secondary sources; not registry-verified this pass) | REJECT, same wrong-substrate argument as LangGraph. Named so the roster is current | none |
| pydantic-ai | typed agent framework | 2.36.0, 2026-08-29, 112 files/90d — very healthy | REJECT, already measured (`...model-bus.md:230`, 103-package closure). Health has improved since; the closure objection is unchanged | none |
| openai-agents / smolagents | lightweight agent loops | openai-agents 0.22.0 (2026-08-19, 34/90d) healthy; smolagents 1.26.0 (2026-05-29, 0/90d) — 3mo quiet | REJECT — same layer, same substrate mismatch. Listed to close the "current leader we are missing" question: there isn't one that changes the answer | none |

  SHELF-1 CONCLUSION: the brief's hypothesis is FALSIFIED and the moat statement
  is confirmed with a sharper reason. The moat is not "gates and contracts" in the
  abstract — it is that GIT IS THE STATE STORE. That is what no orchestration
  framework can adopt without duplicating.

--------------------------------------------------------------------------------
SHELF 2 — LOCAL MEMORY / INDEX  (the "small model per repo" core)
--------------------------------------------------------------------------------
| candidate | provides | maturity (primary, 2026-08-29) | verdict vs incumbent | cheapest experiment |
|---|---|---|---|---|
| **sqlite-vec** | vector search as a SQLite extension, pure C, zero deps; float/int8/binary vectors in `vec0` virtual tables | 0.1.9, last upload 2026-05-18, **0 files/90d**, 69 releases. **PRE-V1 — repo says verbatim "expect breaking changes"**. **`sqlite_vec-0.1.9-py3-none-win_amd64.whl` EXISTS** — clears the rustworkx bar on wheels. Mozilla Builders-backed | **BUY, Tier-S, AND IT IS THE ONLY SHELF-2 CANDIDATE THAT SHOULD BE TRIED.** Incumbent: nothing (B6/P11 is ABSENT). Ruling R-A already put stdlib `sqlite3` in the repo (11,684 edges answered in 1-4ms); this is one extension over a store the repo already runs. No server, no daemon, no egress | **THE PROBE, and it must run FIRST because it can kill the whole shelf:** on Windows under pinned uv, `sqlite3.Connection.enable_load_extension` may be unavailable in the CPython build. **If it is, sqlite-vec cannot load and Shelf 2 is closed on this substrate.** ~20 min: `python -c "import sqlite3; sqlite3.connect(':memory:').enable_load_extension(True)"`. Do this before reading further into the shelf |
| ChromaDB | embedded/served vector DB, batteries-included | 1.5.9, last upload **2026-05-05, 0 files/90d** after 130 releases — a ~4-month gap in a formerly-fast cadence. win_amd64 abi3 wheel present | REJECT. Server-shaped by default (collides with the no-always-running-servers constraint, which the model-bus audit honestly flags as NOT gate-backed), and the cadence break is a real signal against a dep this repo would pin | none unless sqlite-vec's probe fails AND a served option becomes acceptable |
| LanceDB | embedded columnar vector store, Rust-backed | 0.37.1, 2026-08-10, 12 files/90d, win_amd64 abi3 wheel — HEALTHY, and the best-maintained embedded option | DEFER, second choice. Genuinely embedded (no server), healthy, Windows wheel. Loses to sqlite-vec ONLY on the R-A precedent — the repo already runs sqlite, so sqlite-vec is one extension vs a new storage engine | only if the sqlite-vec probe fails. Then it is the same probe against LanceDB, ~1 hour |
| sentence-transformers | local embedding inference (the actual "small model") | 6.0.0, 2026-08-18, 8 files/90d — healthy, pure-python wheel | **BUY only as HALF of the sqlite-vec probe, never alone.** The wheel is trivial; the WEIGHT DOWNLOAD is the real cost and it is unpinned by uv.lock. Flag for ADR-106: a model checkpoint is a dependency the declared environment does not declare | fold into the sqlite-vec probe: embed the 315 LESSONS.md entries + 435 STANDING_RULINGS entries with a small local model, then run the 10 queries the repo has ALREADY FAILED as greps (start with the "no always-running servers" miss at `...model-bus.md`). Success = beats ripgrep on ≥3 of 10. ~2 hours |
| Mem0 | hosted/OSS agent memory layer | mem0ai 2.0.19, 2026-08-24, **28 files/90d**, 188 releases — very active | REJECT. Wrong shape (conversational user-memory, not corpus retrieval) and its benchmark claims are inside the disputed pair (§5 NR-3) | none |
| Letta (MemGPT) | agent server w/ tiered memory | letta 0.16.8, **2026-05-14, 0 files/90d**, requires-python `<3.14,>=3.11` | REJECT. Server-dependent by architecture (it IS an agent server) — fails the carried constraint outright — plus a 3.5-month release gap | none |
| Zep | temporal knowledge-graph memory | **zep-python 2.0.2 last released 2024-09-26 — 23 MONTHS STALE, effectively abandonware**; live line is zep-cloud 3.28.0 (2026-08-26, 22/90d) — i.e. **HOSTED ONLY** | REJECT, hard. The self-hostable python client is abandoned; the maintained path is a cloud service = third-party egress for a private governance repo. Plus §5 NR-3 | none |

  SHELF-2 CONCLUSION: exactly ONE candidate survives to a probe, the probe is
  ~20 minutes, and it is binary. Everything else on this shelf is rejected on
  either server-dependence or a maintenance signal, both of which are constraints
  this repo already holds. That is an unusually clean shelf.

--------------------------------------------------------------------------------
SHELF 3 — LOOP EVALUATION / OPTIMIZATION
--------------------------------------------------------------------------------
| candidate | provides | maturity (primary, 2026-08-29) | verdict vs incumbent | cheapest experiment |
|---|---|---|---|---|
| **DSPy** (+GEPA) | prompt-as-program; metric-driven optimizers. GEPA = reflective prompt evolution, ICLR 2026 Oral (arXiv 2507.19457): reported >GRPO by up to 20% at 35× fewer rollouts; >MIPROv2 by >10% (+12% AIME-2025) | dspy 3.3.1, 2026-08-21, 4 files/90d, 108 releases; `dspy-ai` is the same version (alias). Pure-python wheel, `<3.15,>=3.10` — installs clean under pinned uv. **NO PRIOR IN-REPO MENTION: `grep -rniI "dspy\|GEPA\|MIPRO"` over the whole corpus returns ZERO.** Genuinely unevaluated, not unlocatable | **EVALUATE, Tier-L — and with a specific caution the brief's framing invites.** As "scientific backbone for a PROMPT DISTILLER" the fit is real: GEPA optimizes text against a metric, which is exactly the distiller's problem. **BUT THREE PRECONDITIONS ARE MISSING HERE, and two are blockers:** (1) GEPA needs INTERPRETABLE FAILURE TRACES — "if the traces don't include why failures occur, the algorithm can't generate targeted improvements" (Decagon production write-up). This repo's traces are gate exit codes, which say WHAT failed, not WHY. (2) GEPA has NO NATIVE LENGTH CONSTRAINT (same source: must be encoded into the reflection prompt by hand) — and length is the ENTIRE point of a distiller against a 200-line budget. (3) **ACE's brevity-bias finding (§3) is a direct warning about this class of optimizer.** Reported sweet spot is 20-100 examples; more causes prompt bloat and worse generalization | **DO NOT START WITH DSPy. Start with the METRIC, which does not exist yet.** The Tier-L evaluation is blocked on Shelf-3's eval harness below: an optimizer without a metric optimizes nothing. Cheapest settling experiment, ~1 day, AFTER a harness exists: run GEPA over `CLAUDE.md` §5's critical rules with the harness as the metric and a hand-encoded length constraint; keep only if the distilled set passes ≥95% at fewer bytes |
| promptfoo | declarative LLM eval harness, assertions, matrix runs | **PyPI `promptfoo` is a DECOY: 0.1.4, 5 releases, last 2026-04-06.** The real project is **npm: 0.122.2, published 2026-08-28, 10 releases since 2026-06-01, 421 versions total — very healthy** | **BUY, Tier-S — and it is the highest-value item on this entire appendix, because it is the FIRST STEP TOWARD FIXING B2/P10.** Incumbent: NOTHING. **AND IT IS ALREADY SPECIFIED IN-REPO:** intake #35 (`docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md:84-89`) carries PROPOSED ROW R3 verbatim, with a testable Done-when — `npx promptfoo eval` ≥10 cases from core-invariants, non-zero exit below threshold, **a deliberately-weakened instruction set must FAIL**. That intake is still `status: DRAFT` and has birthed nothing. **CARRIED CONSTRAINT — honest and NOT disqualifying:** it is a Node tool, so it is invisible to uv. But this repo ALREADY runs a pinned Node toolchain (`package.json` pins `pyright@1.1.410` for the #193 reverse-dep oracle), so `npx promptfoo` adds a *second* pinned npm dep to an existing, precedented pattern rather than a new toolchain | **THE 10-CASE PROBE, exactly as intake #35 already wrote it.** Half a day. The falsification test is the good part and it is already in the Done-when: weaken the instruction set on purpose and confirm the harness FAILS. If it passes, the harness measures nothing and you delete it — a clean Tier-S try-and-delete |
| DeepEval | pytest-native LLM eval, metrics, CI | 4.2.0, 2026-08-24, **34 files/90d, 519 releases** — very active, pure-python wheel, `<4.0,>=3.9` | DEFER, second choice — but note the shape advantage: it is **pytest-native**, and this repo's entire gate cadence is `uv run --locked pytest`. That is a better substrate fit than promptfoo's YAML+npm. It loses only because intake #35 already specified promptfoo with a written Done-when, and re-deciding that costs more than running it | if the promptfoo probe stalls on the Node dependency, re-run the SAME 10 cases under DeepEval as pytest tests. Same half-day, and the artifact lands inside the existing suite |

  SHELF-3 CONCLUSION AND THE APPENDIX'S SINGLE STRONGEST RECOMMENDATION:
  The eval harness is not one shelf item among many — it is the missing REWARD
  FUNCTION from B2/P10. Everything else in this appendix is optional; without a
  metric, DSPy has nothing to optimize, the trend dashboard has nothing to trend,
  and the ex-post half of the contract (B7) has nothing to score. It is also the
  only recommendation here that is ALREADY WRITTEN DOWN IN THIS REPO, with an
  acceptance criterion, and simply never born.


================================================================================
§7 — LIMITS: WHAT I COULD NOT VERIFY, AND WHAT I WOULD NEED
================================================================================
EXECUTION LIMITS (substrate)
 1. Ran on CPython 3.11.15, BELOW pyproject's declared `>=3.12`. Every execution
    result above is therefore off-spec, including the ones that succeeded.
    NEED: a seat with `uv sync --locked`.
 2. `funnel_lifecycle.measure()` NEVER RAN (no `click`). Consequently the four
    FM-4 funnel fields — intakes consumed-unarchived, ADRs unexecuted, orphans
    forward, orphans backward — are UNMEASURED IN THIS ARTIFACT. B5's numbers come
    from `funnel_coverage`, a DIFFERENT organ with a different unit (audit
    artifacts, not intakes/ADRs/rows). Do not conflate them.
 3. `file_purpose_graph` never ran (no `rustworkx`). Every claim about the FPG in
    §2 P4 and §5 is READ FROM THE SOURCE, not observed. In particular I did not
    verify that the five-input join actually produces a connected graph on the
    live tree, or how many paths it classifies as "governed".
 4. `logs/TELEMETRY.db` is gitignored, so its absence on this checkout is
    EVIDENCE OF NOTHING about the operator's machine. B3 is scoped to the call-site
    count (which I did verify: exactly one, `block_commit_on_main.py:66`).
 5. I did not run the test suite, ruff, or any gate. No gate result is reported.

SOURCE LIMITS (network)
 6. **arxiv.org is EGRESS-BLOCKED from this seat.** Every arXiv citation in §3
    and §4 — ACE 2510.04618, ExpeL 2308.10144, BM25-Wins-at-Scale 2607.26497,
    CoIR 2407.02883, GEPA 2507.19457, AEL 2604.21725, RPMS 2603.17831, SpIDER
    2512.16956, Reformulate-Retrieve-Localize 2512.07022 — is cited by ID and
    title from search metadata and secondary summaries. **I READ NONE OF THEM.**
    The ACE mechanism description in §3 is the exception: it comes from a DIRECT
    FETCH of github.com/ace-agent/ace, which is a primary artifact.
    NEED: an unblocked seat, or the operator fetching 2607.26497 and 2510.04618.
    Those two carry the most weight per line in this artifact.
 7. infoq.com also blocked. The 2026-dated arXiv IDs (2603.*, 2604.*, 2605.*,
    2606.*, 2607.*) are ID-plausible but UNVERIFIED — I flagged the three thinnest
    inline. Treat the AEL/RPMS/Meta-Reflexion cluster as HYPOTHESIS.
 8. SWE-bench Verified percentages in §4 are SECONDARY (2026 guide articles).
    Directionally I am confident (open ~80 vs proprietary ~90-95); the specific
    figures should not enter a thesis unquoted.
 9. Vendor blogs (Qodo, Voyage, Qwen) are marked VENDOR SOURCE inline. Their
    benchmark numbers are reproducible in principle and their comparative rankings
    are marketing. I did not reproduce any.
10. Microsoft Agent Framework 1.0's 2026-04-03 date is secondary. The AutoGen
    STALLING is primary (PyPI). If only one of those matters, it is the stall.
11. Aider's repo-map architecture (§5) is described from general knowledge, not
    from a source read this pass. Labelled HYPOTHESIS there.

ANALYTIC LIMITS (mine)
12. The LESSONS.md conversion numbers in B1 are MY REGEX over entry HEADERS only,
    not entry bodies. A lesson whose header omits a locator but whose body names a
    gate is counted as unconverted. So **3.8% is a FLOOR, and the true rate is
    higher by an unknown margin.** The direction of the finding survives; the
    magnitude does not. NEED: a body-level pass, ~1 hour, which is exactly the
    organ B1 says does not exist.
13. §4's "this corpus is below the 10M-token crossover" is my estimate from a
    B/line figure, not a token count. I did not tokenize the corpus. It would take
    minutes on a proper seat and it changes the Shelf-2 recommendation if wrong.
14. I read module DOCSTRINGS for four of the five named organs rather than their
    full implementations (750 / 776 / 605 / 997 / 1219 lines respectively). These
    docstrings are unusually candid — several state their own defects verbatim —
    so I weighted them heavily. That is a judgment, and if a docstring overclaims
    relative to its code, my scores in §2 inherit the error. The one score I
    verified BY EXECUTION rather than by reading is P7 (honest degradation).

ONE THING I WOULD WANT RULED BEFORE ANY OF THIS IS ACTED ON
15. The "no always-running servers" constraint drives three REJECT verdicts in §6
    (ChromaDB, Letta, and half the Zep reasoning). The repo's OWN model-bus audit
    (`docs/audits/2026-08-23-technical-research-model-bus.md`) records that it
    **could not locate this rule in any canonical in-repo doc** and that it is
    "attributed to the operator ... and is NOT gate-backed". I inherited it, I used
    it, and I am flagging that I used an unlocated rule to reject three candidates.
    If it is not live, those three verdicts weaken and should be re-taken.

================================================================================
END AUT-R3
================================================================================
```

**Lane closed read-only as contracted** — zero rows, zero commits, zero pushes, tree clean.

Three things I'd flag above the rest if the arc only acts on a few:

1. **The shape of the gap is coherent, not scattered.** Everything PRESENT is enforcement and honesty; everything ABSENT is feedback (outcome signal, retrieval, credit assignment, decay, negative-memory query). The repo is a very good RL *environment* with no *learning signal*.
2. **The strongest recommendation was already written here and never born** — intake #35's PROPOSED ROW R3 (promptfoo, 10 cases, weakened-instructions-must-fail). It is the missing reward function, and its acceptance criterion is already drafted.
3. **Sourcegraph is the arc's most useful negative result.** They built the exact triad and *amputated the learned index*, for the two reasons this repo has independently adopted as constraints (no third-party egress, no refresh burden). Any index here should be local, small, and deletable.

Two honesty notes on my own numbers: the 3.8% LESSONS→code conversion rate is a **floor** (header-level regex, not bodies), and `funnel_lifecycle` never ran — so the four FM-4 funnel fields are unmeasured in this artifact, and B5's 9.8% comes from a different organ with a different unit.