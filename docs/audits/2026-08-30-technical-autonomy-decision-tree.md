# CAPSTONE (a) — THE DECISION TREE: every AUTONOMY finding, routed

> **Generated 2026-08-30** by the integrator's filing pass from
> `docs/audits/2026-08-29-technical-autonomy-synthesis.md` §(a). **Every leaf carries an id or a
> reason. Nothing is unrouted** — that is the property this artifact exists to prove, and it is
> checkable by counting: the tally below sums to the leaf count, and no row reads "unrouted".

- **Consumed by:** `[#624]`, intake #35 (2026-08-30 amendment), intake #63 (2026-08-30
  amendment), and the AUTONOMY arc's next batch. It routes the five AUT research artifacts, so
  those artifacts are CONSUMED rather than orphaned.

## The tally

```
leaves routed            55
TRUE GAP                 18
already-in-intake        9
DISCHARGED               9
REJECTED                 6
CORRECTION-TO-RECORD     5
already-in-ADR           4
already-a-row            3
not-a-candidate          1
```

**Read the shape, not just the numbers.** Only **18 of 55** are TRUE GAPs, and of those only
**two** became rows. That is not under-filing — it is the sequence the synthesis found:
*every absent property is downstream of a metric, and the metric is RANK 1*. A gap parked behind
a named trigger is routed; a gap birthed ahead of its blocker is a row that cannot be worked.

## TRUE GAPs — each with its destination

```
R1-2  Telemetry-ranked catalog curation (what has fired, how often
    -> PARKED: PARKED -- trigger: intake #35 R3 (the metric) lands; this IS the usage half of that metric
R1-3  Cross-artifact consistency check over the intake->ADR->row->
    -> ROW: [#624] -- cross-artifact consistency is the same detection gap, generalised
R1-9  Re-measure ADR-87's STEP 1 by-class self-load finding
    -> PARKED: PARKED -- trigger: intake #35 R3 (the metric) lands; a re-measurement with no measurer is a plan, not a task
R2-2  Reference-class forecasting over the repo's own history
    -> PARKED: PARKED -- trigger: intake #35 R3 (the metric) lands; reference-class forecasting needs the history the metric records
R2-3  Minority report as a first-class output
    -> AMENDED: intake #35 -- minority report is an output SHAPE of the eval harness
R2-4  Premortem as an ex-ante contract section
    -> AMENDED: intake #35 -- premortem is an ex-ante contract section, same object as the acceptance criterion
R2-5  Doctrine: contrived vs authentic dissent are not the same cl
    -> AMENDED: intake #35 -- the dissent-class doctrine rides the same clause
R2-6  Fuzzy-band acceptance -- the ADR-81 deferred arc
    -> ROW: ADR-116 landed by batch-D lane f (claude/lane-f-000-adr81-fuzzy-band, d8f2993)
R2-10 The V-2 budget's "<=2 operator interactions per lane-batch" 
    -> ROW: [#624] -- an unmeasured budget clause is a citation whose target nobody watches
B1   LESSONS -> rules -> gates conversion runs at ~4% and nothing 
    -> AMENDED: intake #63 -- the LESSONS->rules->gates rate IS the learning-loop signal
B8   No counterfactual, no negative memory, not queryable
    -> AMENDED: intake #63 -- counterfactual/negative memory is the loop's store
B9   The axis-(d) organs cannot all run in the same process
    -> PARKED: PARKED -- trigger: two axis-(d) organs are needed in ONE process; today none are
Lane resume-point convention (NOT a framework)
    -> PARKED: PARKED -- trigger: a lane is lost mid-run and the loss costs more than the convention
DSPy / GEPA
    -> PARKED: PARKED -- trigger: intake #35 R3 (the metric) lands -- "WRONG ORDER, not wrong tool"
DeepEval
    -> PARKED: PARKED -- trigger: promptfoo proves insufficient; 65 packages for a binary question it answers at zero
Harbor
    -> PARKED: PARKED -- trigger: a second executor is admitted; unlocatable prior, scored against on substrate
nasde-toolkit
    -> PARKED: PARKED -- trigger: its product page reads from an unblocked network (unknown #2, RESOLVED but unread)
OpenCode · pi (as EXECUTORS, not as AGENTS.md readers)
    -> PARKED: PARKED -- trigger: ecosystem/substrate-registry.yaml admits a non-Claude executor
```

## Already carried — routed to the object that already owns it

```
already-in-intake  R1-1  Contract compiles to a checked plan, incl. substrate + tier
already-in-intake  R1-6  Propose-only unattended runs with a human adjudication gate
already-in-intake  B2   No outcome signal -- the loop has no reward                [TWO L
already-in-intake  B4   Nothing measures the decay of a landed rule
already-in-intake  B6   No retrieval layer -- the boot surface is hand-curated
already-in-intake  B7   The ex-ante criterion is frozen but never scored afterward
already-in-intake  sqlite-vec (+ model2vec as the embedder)
already-in-intake  promptfoo
already-in-intake  SkillsBench / BenchFlow
already-in-ADR     R2-13 Authority routing by kind (P6)            already-in-ADR -- ADR-
already-in-ADR     R2-15 The finding funnel (P8)                   already-in-ADR -- ADR-
already-in-ADR     R2-16 Decision budget / escalation classes (P9) already-in-ADR + rulin
already-in-ADR     B5   The funnel is 90% uncovered and the ratchet cannot shrink it
already-a-row      R1-4  Deferred / on-demand loading of the always-on catalog
already-a-row      R1-5  One machine-readable per-step routing source
already-a-row      B3   Telemetry is one-call-site-wired and the store is unproven
DISCHARGED         R2-1  ADR options-decay surfacing                    [TWO LEGS, split]
DISCHARGED         R2-9  Calibrated ratings / agent self-scored confidence (P10)
DISCHARGED         R2-11 Heterogeneous second reader (P3)          DISCHARGED -- the terr
DISCHARGED         R2-12 Dissent-carrying synthesis (P5)           DISCHARGED -- protocol
DISCHARGED         pydantic-ai, openai-agents, smolagents, Google ADK
DISCHARGED         OpenTelemetry GenAI semantic conventions
DISCHARGED         Arize Phoenix          DISCHARGED -- cost-usage-telemetry.md:63 lists 
DISCHARGED         Langfuse               DISCHARGED -- cost-usage-telemetry.md:118 names
DISCHARGED         LangSmith              DISCHARGED -- docs/audits/2026-05-29-harness-en
not-a-candidate    The harness-portability map
```

## REJECTED — with the reason, so it is not relitigated

```
R1-7  Consultation-with-weights
R1-8  Learned / dynamic model routing (RouteLLM class)
R2-7  Multi-agent debate as a decision mechanism
R2-8  Cognitive-bias checklist for agents
R2-14 Recorded rejection as anti-relitigation   already-in-ADR -- ADR-111 §1(d),
ChromaDB · LanceDB · Mem0 · Letta/MemGPT · Zep · sentence-transformers
```

The unifying reason, stated once because it covers most of them (synthesis §1.3): **"PLURALITY
BUYS LITTLE; ASYMMETRY AND HETEROGENEITY BUY A LOT."** Consultation-with-weights, multi-agent
debate and a prompted-critic second opinion are **the same rejected object wearing three names**,
and the repo already owns the two configurations that DO have evidence — cross-vendor terra, and
ADR-108 §A asymmetric authority routing.

## CORRECTIONS TO THE RECORD — carried because the record is immutable

```
Orchestration frameworks -- LangGraph, LangChain, AutoGen, CrewAI, Microsoft Agent Frame
The "quota-source field"
AutoGen is abandonware. docs/archive/2026-04-24-multi-agent-debate-patterns.md:116 still
Zep's open-source edition no longer exists. "Zep Community Edition is no longer supporte
LOCOMO does not reliably measure what its title says. Contested replication (Mem0 report
```

## The two unknowns that stay UNKNOWN

Carried verbatim rather than resolved-by-assertion: **`PPI`** (Shelf 1) and **`tracys.com`**
(Shelf 3). The dispatch record gives placement evidence — harness shelf and observability shelf
respectively, favouring `pi` and Traceloop — which **narrows neither to a resolution**. The third,
`nasde`, is RESOLVED but its product page needs one read from an unblocked network.
