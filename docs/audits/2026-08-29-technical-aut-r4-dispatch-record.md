# SIDE-SESSION 2026-08-29 — AUT-R4 DISPATCH (two parallel cloud lanes)

**Paste this whole file into a FRESH CC session.** Dispatch-only: touch NO worktree, NO merge
queue, NO manifest of batch D. If any item collides with running work, defer it and say so.

**Do NOT re-dispatch AUT-R3** — it is already active (repo-as-reinforcement-environment), and
its intake seed (#63, universal per-repo learning loop) is already filed. This paste dispatches
its two siblings.

**Both lanes: CLOUD, READ-ONLY.** Zero writes, zero commits, zero rows, no gate runs (the cloud
image may carry the wrong `uv` — invoke `python3` and declare it; never report a gate result you
did not observe). **Online web research is expected and required** — these are surveys of a
fast-moving field; cite real sources. Each lane ends with EXACTLY ONE self-contained artifact,
harvested by `Harvest-Cloud` (it exists — alias to `Save-CloudSessionReport`) or by operator
paste. Copy each launch line from PLAYBOOK Ch8's dispatch table; capture the three receipt gates.

**Shared honesty rules (acceptance criteria for both lanes):**
- **Sources or it didn't happen.** Never invent a citation, URL, product, paper or figure. If no
  real source exists, say *"no source found"* and label the item a hypothesis. Operator-named
  products are hypotheses until verified.
- **Evidence tiers** per claim: *measured* (study/reported result) · *practiced* (orgs do it, no
  measurement) · *asserted* (someone recommends it).
- **Negative results are first-class** — what the industry tried and abandoned outranks a list of
  things that sound good.
- **Recency:** note roughly when each source is from; flag what you'd want re-verified.
- **This repo is unusual:** a governance/methodology hub that never executes (Layer 2),
  markdown-first, single-operator with AI agents as the other participants, heavily gated. Say
  plainly how a pattern transfers here — or that it doesn't.
- **Verdict enum per candidate, exactly three:** `already-have-it` (organ + locator) · `partial`
  (organ + locator + precisely what is missing) · `absent`. Search before declaring absence.
- **Adoption framing:** ADR-112 — Tier L evaluates, Tier S tries and keeps or deletes. For every
  candidate name the **cheapest experiment** that would settle adoption here.
- **Hard constraint, first-class for every candidate:** Windows wheels + installability under the
  pinned `uv` (the rustworkx precedent); self-hosted-friendly scores above SaaS-only; heavyweight
  server-dependent stacks score against it.
- **Reconcile before recommending:** if a candidate was evaluated here before, find the prior
  verdict and re-assess at today's scale — never relitigate silently.
- Rank by fit × value. Six well-sourced candidates beat twenty thin ones.

---

## LANE AUT-R4-A — "foundations: harness · evals · observability"

**Shelf 1 — INDEPENDENT HARNESS.** OpenCode and current open-source agent-harness peers (also
verify the operator's *"PPI"* — unresolved name; find what it refers to or mark it unknown)
versus our CC-as-harness. Core question: which of our organs (frozen contracts, the Ch8 dispatch
table, gates, worktree lanes) are **harness-portable** versus **CC-coupled**? This is the
harness-swap resilience test of our provider-agnostic doctrine — today CC is both producer and
harness, a single point of dependency.

**Shelf 2 — EVAL SUBSTRATE.** Harbor (the Terminal-Bench team's framework: task/trial/verifier
abstraction, containers, registry) + SkillsBench and kin. Assess Harbor as the substrate for our
SDA-1 admission packs and skill evaluations **instead of hand-rolling the harness** — sol's
C-6/C-15 named that build cost explicitly. Carry this measured finding into the verdicts: on
SkillsBench, human-authored skills raise pass rates ~16.2 pp while LLM-authored skills give no
measurable gain, and SkillAxe-style evaluation-guided refinement is the published fix. The
consequence for us: **a prompt/skill distiller without an eval loop ships a useless library.**
Also verify `noesisvision.com` "nasde" — unknown to both operator and architect.

**Shelf 3 — AGENT OBSERVABILITY.** Arize Phoenix (OTel-based OSS), LangSmith, **plus Langfuse**
and the **OpenTelemetry GenAI semantic conventions** (resolve the operator's *"tracys.com"* or
mark unknown). Fit against our LIVE incumbents: the telemetry store, `trends.html`, the
quota-source field, lane packets. Verdict frame: **buy the collector and tracing, keep our
verdict layer** (telemetry → trends → rulings stays ours). Assess error-handling and usage-stats
coverage explicitly.

---

## LANE AUT-R4-B — "machinery: orchestration · local memory · loop optimization"

**Shelf 4 — AGENT ORCHESTRATION.** LangChain/LangGraph, AutoGen, CrewAI, plus any current leader
we are missing — versus our PLAYBOOK Ch8 dispatch + lane contracts + sentinel. **Hypothesis to
attack:** our moat is gates and contracts, not call-orchestration; could LangGraph-class state
machines replace hand-rolled lane plumbing while our gates stay? **Reconcile first:** LangChain
was evaluated in this repo before — find the prior verdict/intake and re-assess at today's scale.

**Shelf 5 — LOCAL MEMORY / INDEX** (the "small model per repo" core). `sqlite-vec` (note: we
already run sqlite per ruling R-A — the natural first probe), ChromaDB, LanceDB,
sentence-transformers local embedders, and agent-memory layers Mem0 / Letta (MemGPT) / Zep.
Assess against our actual need: a learned **"where is what / what matters"** index feeding the
file-purpose graph (FPG) and the boot surfaces. Say clearly what local models are good for
(retrieval, ranking, importance-learning) versus not (decision-making, generation quality).

**Shelf 6 — LOOP EVALUATION / OPTIMIZATION.** DSPy (prompt-as-program with metric-driven
optimization — assess as the scientific backbone for the PROMPT DISTILLER filing, adjacent to
[#617]), plus promptfoo / DeepEval as the eval harness SDA-1 already told us to check before
hand-rolling anything. Shelf 2's SkillsBench finding binds these verdicts.

---

## AFTER DISPATCH

Report both receipts here (session ids + the three gates), then stop. Artifacts return by harvest
or paste; the architect consumes them together with AUT-R1, AUT-R2 and AUT-R3 to cut the AUTONOMY
arc. **File nothing from this session** — the reconcile-and-file pass happens when the artifacts
land.
