> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a6-langgraph-class-rejection-record` | receipt id `cse_01N8WRkWp8dyqipeKpxZFzWZ` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a6-langgraph-class-rejection-record.md`.
> Selection rule: the LONGEST assistant text, not the last - text #2 of 10 across 4 pages.
> Bytes written unchanged: **28,318**.
> Harvester DEVIATION, recorded not repaired: the report contains no markdown heading at all; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** ADR-111 section 1(d) (recorded rejection as anti-relitigation).
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

**Receipt (both halves)**
- `git-source-resolves-non-empty:` `https://github.com/rdwornik/dev-knowledge` (fetch+push, `origin`), HEAD `ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b`, clean tree
- `first-assistant-text-echoed:` 118 lines; final line: `- No edits outside this lane's declared footprint. Prose in English; hyphen-only names.`

**Write-scope compliance:** zero files written, zero commits, zero rows. `git status --porcelain` empty at start and unchanged. No gate run, none asserted (contract: read-only, no test leg). Read-only tools throughout (`git grep`, `sed`, `awk`, `grep`).

The record follows, in full. It is fenced and flat per CLAUDE.md §4 output-formatting, so it copies out without border glyphs.

```
================================================================================
RECORDED REJECTION — THE ORCHESTRATION-FRAMEWORK CLASS ("LangGraph-class")
Lane: batch-e-a6-langgraph-class-rejection-record
Drafted 2026-08-31 against ec8731a. RECORD ONLY — no build, no adoption, no trial.
Proposed destination: protocols/STANDING_RULINGS.md section B, new entry B8.
Landing it is the integrator's act. This lane wrote nothing.
================================================================================

--------------------------------------------------------------------------------
0. WHY THIS RECORD EXISTS (the failure it closes)
--------------------------------------------------------------------------------
This class has been adjudicated FOUR times in four months — 2026-04-24 (Council
P3-3), 2026-08-23 (model-bus), 2026-08-29 (AUT-R3), 2026-08-29 (AUT-R4-B) — and
re-routed a fifth time at the 2026-08-30 capstone. Each pass located the prior
verdict and re-affirmed it. That is four correct reconciliations and four wasted
adjudications: the record was locatable but never sat on a surface an agent reads
BEFORE it starts researching.

Two concrete defects make re-derivation likely again, and both are unfixable in
place because their homes are immutable:

  D1  docs/audits/2026-08-30-technical-autonomy-decision-tree.md renders both its
      CORRECTIONS and REJECTED blocks in code fences TRUNCATED AT 88 CHARACTERS.
      Line 123 literally ends mid-word: "Orchestration frameworks -- LangGraph,
      LangChain, AutoGen, CrewAI, Microsoft Agent Frame". The correction's content
      is NOT recoverable from the capstone. It is recoverable only from
      docs/audits/2026-08-29-technical-autonomy-synthesis.md:465-474, which the
      capstone was generated from.

  D2  The DISCHARGED locator for four members (Google ADK, pydantic-ai,
      openai-agents, smolagents) resolves to
      docs/audits/2026-04-24-council-28-29-consolidated-actions.md:117 — a ruling
      headed "P3-3: LangGraph / AutoGen / CrewAI frameworks", which NAMES NONE OF
      THE FOUR. The discharge is sound only by class extension, and the class
      boundary was never drawn. ADR-111 section 1(b) requires the locator to
      resolve; it resolves to a document, not to a naming. Section 3 of this
      record draws the boundary that makes that discharge sound.

This record is the consolidation. It is not a new adjudication and adds no new
argument to the nine members that already carry one.

--------------------------------------------------------------------------------
1. WHAT IS REJECTED
--------------------------------------------------------------------------------
Adoption, as a declared dependency of this repo or of any organ it ships, of any
third-party library whose value proposition is OWNING THE CONTROL FLOW of a
multi-step or multi-agent LLM run — graphs, crews, conversation loops, agent
loops, checkpointed workflows.

Enumerated members (section 4 gives each one's verdict and locator):
  LangChain · LangGraph (incl. langgraph-checkpoint-*) · AutoGen (pyautogen,
  autogen-agentchat) · CrewAI · Microsoft Agent Framework · Semantic Kernel ·
  Google ADK · pydantic-ai · openai-agents · smolagents · LlamaIndex used as an
  agent orchestrator.

The enumeration is illustrative of a boundary, not exhaustive. A library not
listed is inside the class if it meets the section 3 test.

--------------------------------------------------------------------------------
2. THE REASON
--------------------------------------------------------------------------------
Stated in decreasing durability. R1 and R2 are sufficient alone; R3-R5 are why
the answer has not moved as the libraries improved.

R1 — WRONG LAYER / WRONG SUBSTRATE.  (primary; framework-independent)
    First stated docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:71
    ("agent-orchestration frameworks (LangGraph/CrewAI class -- wrong layer)"),
    upgraded to wrong-SUBSTRATE by AUT-R3 and argued at length by AUT-R4-B
    section 1. A lane's state IS its branch. git log, git worktree list, git
    stash list and the branch-name grammar are the checkpoint store, and they
    survive machine death, process death and session death with no runtime at
    all. Of the five properties that define a lane, four are assertions about
    the git object database and the filesystem and the fifth is a governance rule
    about which decisions a seat may take. Not one is a node, an edge or a state
    transition. A StateGraph plus checkpointer replaces NONE of them, because it
    does not know what a worktree is — and it cannot express the CLAUDE.md
    section 5 rule 9 obligation "removed AND VERIFIED REMOVED".

R2 — THE LAYER-2 INVARIANT IS CONSTITUTIONAL, NOT A PREFERENCE.
    CLAUDE.md section 5 rule 4 / ADR-28 / ADR-36: Layer 2 never executes;
    validators, generators and gates are in scope, orchestration scripts are not.
    An orchestration framework is by definition an executor. No library
    measurement — health, closure size, benchmark — can clear a constitutional
    bar. This is the reason that does not decay.

R3 — LIBRARY-FIRST ADOPTION ORDER, AND THE CLOSURE COST.
    PLAYBOOK section 11 (ruled 2026-08-04): stdlib > an existing dependency > a
    new distribution, and an adoption claim carries a MEASURED divergence rather
    than a preference. Measured: langgraph resolves to a 35-package closure —
    exactly the size of this repo's entire current lock — 38 with the SQLite
    checkpointer; pydantic-ai to 103 packages, roughly 3x the lock. For a
    capability with no consumer.

R4 — CHURN VERSUS A PINNED, REPRODUCIBLE ENVIRONMENT (ADR-106).
    Measured 2026-08-29: crewai 212 uploads in 90 days across 425 releases;
    langchain 514 releases, roughly one every 2.5 days. This repo's uv pin is
    exact and a bump is its own gated change. Hyperactivity is not ill health —
    it is a moving target, and that is the objection.

R5 — TWO SOURCES OF TRUTH FOR LANE STATE IS WORSE THAN ONE.
    A checkpointer would add a second, weaker durability layer that does not know
    about the first (git) and cannot be reconciled with it.

R6 — PLURALITY BUYS LITTLE (covers the debate-shaped members only).
    Synthesis section 1.3, quoted once because it covers most of the class:
    "PLURALITY BUYS LITTLE; ASYMMETRY AND HETEROGENEITY BUY A LOT."
    Consultation-with-weights, multi-agent debate and a prompted-critic second
    opinion are the same rejected object wearing three names. The repo already
    owns the two configurations that DO have evidence — cross-vendor terra, and
    ADR-108 section A asymmetric authority routing.

WHAT THE REASON IS NOT — recorded so the class cannot be reopened on a strawman:
  - NOT installability. langgraph ships pure-Python py3-none-any wheels, resolves
    cleanly, needs no server and no LangSmith account. AUT-R4-B section 2.1 says
    so explicitly and this record repeats it.
  - NOT library health. langgraph 1.2.11 (2026-08-11) HEALTHY; crewai 1.15.18
    (2026-08-29) hyperactive; pydantic-ai 2.36.0 very healthy.
  - NOT the "40-50% cost reduction" figure. It is attributed to [Perplexity] with
    no primary citation, and AUT-R4-B section 2.0 rules it the weakest evidence
    in the in-repo record on this shelf. DO NOT CARRY IT FORWARD in either
    direction. It has already been cited twice since.
  - NOT AutoGen's maintenance stall. That is a supporting reason for ONE member
    (section 4), not the class reason. If AutoGen shipped tomorrow, R1 and R2
    would still bind it.

--------------------------------------------------------------------------------
3. THE CLASS BOUNDARY
--------------------------------------------------------------------------------
TEST (all three must hold): the library is (a) a third-party distribution, that
(b) owns the control flow of an LLM run at runtime — it decides what executes
next — and (c) is proposed as a substitute for, or a layer beneath, this repo's
lane plumbing, dispatch or gate mesh.

EXPLICITLY OUT OF CLASS — each has its own home; do not fold, do not stretch this
record to cover them:

  OUT-1  The harness itself — Claude Code, Codex CLI. The incumbent, not a
         candidate. STANDING_RULINGS names the active toolset.
  OUT-2  Observability / eval SaaS — LangSmith, Langfuse, Arize Phoenix,
         OpenTelemetry GenAI conventions. Separately DISCHARGED at
         decision-tree:96-99. Different shelf. LangSmith is a commercial
         LangChain product; shared vendor is not class membership.
  OUT-3  Memory and vector stores — ChromaDB, LanceDB, Mem0, Letta/MemGPT, Zep,
         sentence-transformers (REJECTED, decision-tree REJECTED block);
         sqlite-vec, model2vec (already-in-intake, intake #63). Different shelf.
  OUT-4  Multi-agent debate AS A DECISION MECHANISM — WISE,
         consultation-with-weights, cognitive-bias checklists. REJECTED as a
         METHOD at decision-tree (R1-7, R2-7, R2-8), not as a library. R6 above
         is the shared reason; the dispositions stay separate.
  OUT-5  Provider SDKs and model buses — anthropic, openai, ai-council's
         PROVIDER_CLASSES. The incumbent layer this class would sit on top of.
  OUT-6  Retrieval libraries used only as retrieval — LlamaIndex in that role.
         UNVERDICTED and out of class. See section 4.
  OUT-7  General-purpose, non-LLM workflow engines — Temporal, Prefect, Airflow.
         Never proposed here, no verdict exists, and none is created by this
         record. Named so the record is not stretched to cover them later.

DISPOSITION VOCABULARY — the two words are not interchangeable (ADR-111 §1):
  REJECTED   = §1(d), recorded with its reason and not relitigated.
  DISCHARGED = §1(b), already done or ALREADY RULED, recorded with a locator.
The class carries BOTH, and the relation is not a contradiction: the class was
REJECTED on 2026-04-24, and every later look is correctly DISCHARGED against that
rejection. The right disposition for the NEXT proposal in this class is
DISCHARGED-against-this-record, not a fresh adjudication.

--------------------------------------------------------------------------------
4. PER-FRAMEWORK RECONCILIATION — 11 members, 9 cite, 2 new
--------------------------------------------------------------------------------
Format: framework | prior verdict | where | new verdict?
Locators verified against ec8731a this pass unless marked otherwise.

LangChain | REJECTED, re-affirmed 3x | 2026-04-24-council-28-29-consolidated-actions.md:117 (P3-3 "Skip", by class); 2026-08-23-technical-research-model-bus.md:243 ("REJECT, already measured ... the prior outcome stands"); 2026-08-29-...-aut-r3-...md:606 (health re-measured, reason unchanged: no consumer, ai-council owns PROVIDER_CLASSES) | NO — cites

LangGraph | REJECTED, re-affirmed 3x, reason UPGRADED | P3-3:117 (named in heading); model-bus.md:243; aut-r3:605 ("REJECT (re-affirmed, reason UPGRADED to wrong-substrate)"); argued at length aut-r4b sections 1 and 2.1; routed synthesis:465-474; filed decision-tree:123 (TRUNCATED, defect D1) | NO — cites

AutoGen (pyautogen, autogen-agentchat) | REJECTED on maintenance, measured | P3-3:117 (named in heading); aut-r3:607 and :490-494 — pyautogen 0.10.0 last upload 2025-07-15, autogen-agentchat 0.7.5 last upload 2025-09-30, both 0 files in 90d, 11-13 months quiet; succeeded by Microsoft Agent Framework 1.0 | NO — cites. Per-member reopening rule T5 applies: re-proposing AutoGen needs a NEW PACKAGE, not a new argument

CrewAI | REJECTED on churn | P3-3:117 (named in heading); aut-r3:608 — crewai 1.15.18, 212 files/90d across 425 releases. "The churn is the objection, not the health" | NO — cites

Microsoft Agent Framework | REJECTED, wrong substrate | aut-r3:609 (first and only lane-level verdict; not in P3-3, which predates it); carried in the synthesis:465 block | NO — cites. EVIDENCE CAVEAT, carried forward from aut-r3:694: the 1.0 / 2026-04-03 date is SECONDARY and was not registry-verified. The verdict does not rest on that date (R1/R2 do the work), but the date must not be quoted as measured

Semantic Kernel | NONE — mentions only | 2026-04-24-multi-agent-debate-patterns.md:62,125 rank it as "supports debate but lower for pure multi-agent production scale"; aut-r3:493 records only that Microsoft merged it with AutoGen into Microsoft Agent Framework. No lane ever verdicted it standing alone | YES — NEW, and DERIVATIVE. REJECTED by class membership (section 3 test: met) plus successor-merged: its declared successor MAF is verdicted at aut-r3:609 on R1/R2, and a maintenance-mode predecessor of a rejected successor cannot clear a bar the successor did not. Derivation stated so it can be attacked rather than inherited

Google ADK | DISCHARGED | decision-tree:95 and synthesis:470-471, locator council-actions:117 (P3-3) | NO — cites. NOTE defect D2: P3-3 does not name it; the discharge holds by the class boundary drawn in section 3, and only by it. Independent supporting fact already in the record, archive:94,141: ADK ties users to a specific provider (model lock-in) — relevant, and NOT the reason relied on

pydantic-ai | REJECTED on cost-for-purpose, then routed DISCHARGED | model-bus.md:230 ("REJECT on cost-for-purpose", 103-package closure, roughly 3x the current lock); re-affirmed aut-r3:610 ("Health has improved since; the closure objection is unchanged"); routed DISCHARGED decision-tree:95 | NO — cites. DISPOSITION SPLIT, recorded not merged: lane-level REJECT, capstone-level DISCHARGED. Both are correct under ADR-111 — the capstone discharges against the lane's rejection. Do not read the capstone as overturning the lane

openai-agents | REJECTED, same substrate | aut-r3:611 (openai-agents 0.22.0, 2026-08-19, 34/90d, healthy — "same layer, same substrate mismatch"); routed DISCHARGED decision-tree:95 | NO — cites. Same disposition split as pydantic-ai. Listed by aut-r3 specifically to close the "current leader we are missing" question: there is not one that changes the answer

smolagents | REJECTED, same substrate | aut-r3:611 (smolagents 1.26.0, 2026-05-29, 0 files/90d — 3 months quiet); routed DISCHARGED decision-tree:95 | NO — cites. Same disposition split

LlamaIndex as an agent orchestrator | NONE — mentions only | archive:58,117 (CrewAI interop), :142 ("complement debates in data-heavy cases but aren't debate-primary") | YES — NEW, and NARROW. REJECTED in the orchestrator role only, by class membership. LlamaIndex as a RETRIEVAL library is OUT-6: out of class, UNVERDICTED, and this record creates no verdict for it. Anyone proposing it for retrieval starts from zero, not from this rejection

TALLY: 11 members. 9 CITE an existing verdict. 2 receive a new one (Semantic
Kernel, LlamaIndex-as-orchestrator), both derivative, both flagged as derivative.
That ratio is the point: reconcile-before-birth, applied.

--------------------------------------------------------------------------------
5. REOPENING TRIGGERS
--------------------------------------------------------------------------------
A rejection with no reopening condition is a prejudice. Five, and each is
checkable by someone other than its author.

T1 — THE ORIGINAL, STILL LIVE (2026-04-24, P3-3, verbatim):
     "team grows beyond solo, or AI Council proves insufficient".
     Carried unchanged. It has not fired.

T2 — THE CONSTITUTIONAL TRIGGER (governs R2):
     A ratified ADR amends or supersedes the Layer-2-never-executes invariant
     (ADR-28 / ADR-36 / CLAUDE.md section 5 rule 4). Until that happens, R2 binds
     regardless of any measurement, and a proposal arguing only from library
     quality has not engaged the reason. Conversely, if T2 fires, this record
     drops to R1 + R3-R5 and must be re-argued rather than cited.

T3 — THE SUBSTRATE FALSIFIER (governs R1; frozen by AUT-R3, carried verbatim in
     shape): model ONE past batch's lane DAG in a LangGraph StateGraph and show
     it can (a) express "worktree removed and verified removed" and (b) reconcile
     its checkpoint against `git worktree list` as a single source of truth.
     AUT-R3's stated expectation: it cannot. 30 minutes to falsify. This is a
     TIER-S PROBE and this record does NOT authorise running it — running it is a
     separate ratified decision. If it succeeds, R1 falls and only R2-R5 remain.

T4 — THE EVIDENCE TRIGGER, and the gap this record must not bury:
     The lane resume-point gap is a TRUE GAP, not a framework need. The synthesis
     files it as "Lane resume-point convention (NOT a framework)", verified live:
     grep -rli "resume" over tasks/ returns ZERO, and PLAYBOOK's five night phases
     have no mechanism for a lane that dies at 03:00 to resume where it died. That
     is real, and durable execution is the strongest thing the pro-adoption side
     has. The trigger: a NATIVE resume-point convention is built AND fails —
     two consecutive batches in which a lane dies mid-step and git-state recovery
     cannot resume it. Then the durable-execution argument reopens ON EVIDENCE,
     against a measured incumbent, rather than on appeal to a missing feature.
     Until the native convention exists, the gap is an argument for BUILDING IT,
     not for adopting a framework.

T5 — THE PER-MEMBER MAINTENANCE TRIGGER (governs the AutoGen row only):
     A member rejected on maintenance reopens on a NEW PACKAGE, not a new
     argument. Same shape as model-bus.md:241-242. Note the asymmetry that makes
     this honest: a new release clears the maintenance objection ONLY; R1 and R2
     still bind, so clearing T5 alone does not reopen adoption.

SCOPE OF THE FORECLOSURE — stated so the record does not over-reach:
This forecloses ADOPTION. It does not foreclose READING. Studying LangGraph's
durable-execution design to inform a NATIVE resume-point convention (T4) is
explicitly permitted and is arguably the highest-value thing on this shelf.
Citing this record to refuse that reading would be a misuse of it.

--------------------------------------------------------------------------------
6. DESTINATION — one, argued
--------------------------------------------------------------------------------
CHOSEN: protocols/STANDING_RULINGS.md, section B, as new entry
        "B8 · the orchestration-framework class -- do not relitigate".
        (B1-B7 exist; B8 is the next free number as of ec8731a.)

Three reasons, in order:

  1. It is the file agents read at arc start AND APPLY SILENTLY — the file's own
     header: "A ruling already issued is not a question." That is precisely the
     property whose absence caused the four re-adjudications in section 0. An
     anti-relitigation record on a surface nobody reads before researching is not
     an anti-relitigation record.
  2. B3 is the established precedent shape in the same section: "rejected engines
     -- do not relitigate" — verbatim rejection list, then WHY, then the governing
     rule it descends from. This entry is the same genre one layer up. It also
     improves on B3, which carries no reopening trigger.
  3. STANDING_RULINGS is LIVING (CLAUDE.md section 4). When T1-T5 fire, the entry
     can be annotated or retired IN PLACE — the pattern ENVIRONMENT.md's Rejected
     list already uses for the reversed Codex CLI entry, where the record is
     annotated rather than erased. An immutable artifact cannot do that, and
     un-updatability is exactly what produced defects D1 and D2.

REJECTED DESTINATIONS, with the reason:

  An ADR. Fails the ADR-98 section 3 test as restated in ADR-111 section 4: an
  ADR is authored only when a reasonable person could choose otherwise AND
  reversal is costly. Neither holds. Four independent passes across four months
  reached the same verdict on measured evidence, and reversal is CHEAP — T3 is a
  30-minute falsifier. An ADR here would also be the wrong instrument for the
  live half: ADRs are immutable but for their status line, and this record's
  triggers must stay editable. If T2 ever fires, THAT is the ADR moment.

  A new audit under docs/audits/. The class "technical" is in
  validate_hermetization.AUDIT_CLASS_ENUM, so the name would be legal — the
  objection is genre, not grammar. It would be the FIFTH immutable artifact on
  one class, restating four, on a surface nobody reads at arc start. It would
  reproduce D1/D2 rather than close them, and it collides head-on with this
  batch's binding rule: reconcile, do not duplicate.

  protocols/ENVIRONMENT.md "Rejected (do NOT revisit before Q3)". Right shape,
  wrong file: that list is a Council-decision + environment-config record, its
  time bound ("before Q3") is long expired, and a library-class doctrine is not
  environment configuration.

  A backlog row. Forbidden. ADR-111 section 2: the only path from a finding to a
  row is CANDIDATE -> intake -> ratification. This is outcome (d) REJECTED, and
  (d) exists precisely so it never approaches the backlog.

STANDING_RULINGS' own scope boundary applies: where an entry names a declared
durable home, that home stays doctrinal and the register is the application
surface in the meantime. If T2 fires, the durable home is an ADR and B8 retires
into it.

--------------------------------------------------------------------------------
7. EVIDENCE INDEX — every locator in this record, resolved at ec8731a
--------------------------------------------------------------------------------
docs/audits/2026-04-24-council-28-29-consolidated-actions.md:117
    RESOLVES. "### P3-3: LangGraph / AutoGen / CrewAI frameworks", Source
    "Multi-agent debate research", Status "Skip -- AI Council already implements
    proposer-critic-synthesizer pattern at solo-dev scale", Reopening trigger
    "team grows beyond solo, or AI Council proves insufficient". THE ROOT VERDICT,
    and the shape this record's spine is copied from.

docs/audits/2026-08-23-technical-research-model-bus.md:230, :243-246
    RESOLVE. :230 pydantic-ai REJECT on cost-for-purpose (103-package closure);
    :243 "langchain / LangGraph -- REJECT, already measured ... the prior outcome
    stands".

docs/audits/2026-08-29-...-aut-r3-repo-as-reinforcement-environment.md
    :166, :490-494, :554-563, :570-597, :605-611, :694 all RESOLVE. :605-611 is
    the seven-row per-framework verdict table with PyPI measurements; :605 carries
    the T3 probe verbatim.

docs/audits/2026-08-29-...-aut-r4b-orchestration-memory-loop.md
    :30, :44-52, :62-87 RESOLVE. Section 2.0 is the reconcile-first pass; section
    2.1 carries the 35-package closure measurement and the explicit
    "excluded on the Layer-2 invariant and on dispatch visibility, NOT on
    installability".

docs/audits/2026-08-29-technical-autonomy-synthesis.md:465-474
    RESOLVES. THE AUTHORITATIVE UNTRUNCATED TEXT of the class routing — the nine
    names in one block, DISCHARGED, with all three locators and
    "THE REASON IS UPGRADED BY BOTH LANES AND THE UPGRADE IS THE VALUABLE PART".
    Use this, not decision-tree:123, whenever the correction's content is needed.

docs/audits/2026-08-30-technical-autonomy-decision-tree.md:95, :120-127
    RESOLVE, WITH DEFECT D1 — both fences truncated at 88 chars. :95 is the
    four-name DISCHARGED line; :123 the truncated orchestration correction; :125
    the truncated AutoGen correction.

docs/intake/2026-08-06-tech-adoption-consolidation-intake.md:71
    RESOLVES. "agent-orchestration frameworks (LangGraph/CrewAI class -- wrong
    layer)" — the origin of R1 and the most durable single phrase in the record.

docs/decisions/ADR-111-*.md:59, and sections 2 and 4
    RESOLVE. :59 "(d) REJECTED -- recorded with its reason, and not relitigated"
    — the mechanism this record instantiates. Cited, not re-invented.

docs/archive/2026-04-24-multi-agent-debate-patterns.md:116
    RESOLVES — see the premise correction in the end packet below.

protocols/STANDING_RULINGS.md:172-195 (B3), :264 (B7, last B entry)
    RESOLVE. B3 is the precedent shape; B7 fixes B8 as the next free number.

MEASURED THIS PASS: 14 tracked files mention the class outside tests/ and
JOURNAL.md — matching the brief's freeze-time figure exactly (19 total matches,
minus 4 tests/fixtures/lived-workflow/*.jsonl, minus JOURNAL.md).

================================================================================
END OF RECORD
================================================================================
```

**End packet — reported, not asked (V-2, decision budget)**

Nothing hit escalation classes (a), (b) or (c). Five items are reported rather than repaired, per Q10 — a disclosure discharges the reporting duty, it does not authorise a repair, and every home below is immutable:

1. **Brief premise, inverted phrasing (not refuted).** The brief says `docs/archive/2026-04-24-multi-agent-debate-patterns.md:116` "carries a claim about AutoGen that the tree calls stale (*'AutoGen is abandonware'*)". Resolved: line 116 asserts the **opposite** — `| **AutoGen (Microsoft Agent Framework)** | ... | Excels at "agents arguing to consensus"; 54,600+ GitHub stars | ... human-in-loop best-in-class |`. "AutoGen is abandonware" is the **decision tree's correction headline at :125**, not the archive's claim. The underlying fact is intact and the record uses it correctly. Separately: "abandonware" is stronger than the measurement supports — AUT-R3:492-494 says maintenance-mode with an explicit successor and migration guidance, which is not abandonment. The record states the measurement, not the epithet.

2. **The brief asks for a REJECTED record; the capstone routes the class DISCHARGED.** Not a contradiction, and reconciled in §3 rather than papered over: the class was REJECTED on 2026-04-24, and every later look correctly DISCHARGES against that rejection. The brief's own guardrail — "`pydantic-ai` and `smolagents` are already DISCHARGED, a different disposition from REJECTED" — holds at the capstone; underneath it, the synthesis discharged all nine names in **one block**, and the capstone's split into two lines is an artifact of its filing pass, not a second adjudication.

3. **Defect D1** — the decision tree's CORRECTIONS and REJECTED code fences are truncated at 88 characters in the tracked file; the orchestration correction ends mid-word at "Microsoft Agent Frame". Immutable artifact, not repaired. The record routes readers to synthesis:465-474 for the recoverable text.

4. **Defect D2** — the DISCHARGED locator for Google ADK, pydantic-ai, openai-agents and smolagents resolves to a ruling (P3-3) that names none of them. Sound only by class extension, which is why §3 exists.

5. **Two stale locators in immutable audits**, reported for the next reader:
 - AUT-R3:371 cites `JOURNAL.md:25560` for "LangGraph, AutoGen, Cline Memory Bank". That line is a 2026-05-22 drift-burndown entry. The actual line is **26277** — JOURNAL is newest-first-prepend, so line-number locators into it decay with every prepend. Structural hazard, worth a rule someday; not this lane's to file.
 - model-bus:243 cites `archive/...:44,185`. `:44` resolves (the cost/error-amplification/evaluation finding); **`:185` is blank** — the intended target is `:184`. Off by one.

No merges, no pushes, no JOURNAL entry, no index regeneration, no branch created. The lane is read-only by contract; if a Stop-hook closure proposal fires on this session, decline it.