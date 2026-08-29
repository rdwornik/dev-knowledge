# AUT-R4-B — machinery: orchestration · local memory/index · loop optimization (CLOUD, READ-ONLY)

**Repo:** `.dev-knowledge` (bound to `main`) · **Substrate:** cloud (read-only reconnaissance, no
gate dependency)
**Arc:** AUTONOMY. Sibling lanes already dispatched: **AUT-R1** (autonomous SDLC orchestration),
**AUT-R2** (decision-quality frameworks), **AUT-R3** (repo-as-reinforcement-environment), and your
own sibling **AUT-R4-A** (harness · evals · observability). You will not see their output; do not
speculate about it.
**Dispatched:** 2026-08-29, side-session.
**Deliverable:** ONE artifact. Print it in full as your final message; it returns by harvest.

## KNOWN OVERLAP — read this before you plan your work

**AUT-R3 is running concurrently with you, and its brief carries a three-shelf "library-first
sweep" appendix covering the same three shelves as this brief** — agent orchestration, local
memory/index, and loop evaluation/optimization — with substantially the same candidate lists. That
overlap is **known and deliberate at dispatch time**, and it changes your job in one specific way:

- AUT-R3 treats these three shelves as an **appendix** to a different thesis. Its attention on them
  is secondary.
- **You treat them as the entire deliverable.** Your job is **primary depth**: more candidates,
  actual maturity signals, real numbers, negative results, and the reconcile-first work AUT-R3's
  appendix has no room for.

So: **do not assume you are the only pass, and do not aim for coverage — aim for depth.** A shallow
restatement of the obvious candidates is worthless here, because a second lane is already producing
exactly that. Where you can only produce a thin answer on a candidate, say so and spend the effort
on one you can take deep.

## WHAT YOU ARE AND ARE NOT DOING

**ZERO ROWS.** You birth no backlog row, no `tasks/` edit, no intake file, no ADR — not even a
draft. You commit nothing and push nothing. If a hook or a closure proposal invites you to commit,
decline and say the lane is read-only by contract. Your entire output is the artifact text.

**Gates:** you need none. A cloud image may carry the wrong `uv`, so invoke `python3` directly and
**declare that you did**. Do not attempt `uv run --locked`; never report a gate result you did not
observe.

**ONLINE RESEARCH IS EXPECTED AND REQUIRED.** These are surveys of a fast-moving field. Use the web.
Cite real, resolvable sources.

## HONESTY RULES — acceptance criteria, not preamble

- **Sources or it didn't happen.** Never invent a citation, URL, product, paper, version number or
  figure. If no real source exists, write **"no source found"** and label the item a **hypothesis**.
- **Evidence tier on every claim**, exactly one of: **measured** (a study or reported result) ·
  **practiced** (organisations do it, no measurement) · **asserted** (someone recommends it).
- **Negative results are first-class.** What the industry tried and abandoned outranks a list of
  things that sound good. Abandonware, benchmarks that do not measure what their title says, and
  loudly-launched projects that went quiet are among the most valuable things you can return.
- **Recency:** note roughly when each source is from, and flag what you would want re-verified.
- Prefer primary sources — papers, framework repos, maintainer write-ups, release histories — over
  listicles and over LLM-generated summaries.
- Where you cannot verify, say so in the artifact rather than smoothing it.

## THIS REPO IS UNUSUAL — say plainly how a pattern transfers, or that it doesn't

`.dev-knowledge` is a **governance and methodology hub that never executes** (Layer 2 of a
three-layer ecosystem model): markdown governance files plus hub-local validators, generators and
gates. No script here drives state in a child repo. It is **markdown-first**, **single-operator**
with AI agents as the other participants, and **heavily gated** (pre-commit, commit-msg, pre-push
hooks plus a self-conformance audit). Read `CLAUDE.md`, `AGENTS.md` and `ARCHITECTURE.md` before
scoring anything.

A pattern built for a multi-engineer product codebase with CI runners may transfer here badly or
not at all. **Say which.** An artifact that scores candidates as if this were a normal application
repo is useless. This bites hardest on Shelf 4: most orchestration frameworks assume a running
service, and this repo is by invariant a thing that does not run.

## VERDICT ENUM — exactly three, per candidate

- **`already-have-it`** — name the organ **and its locator** (`path:line` or a heading).
- **`partial`** — name the organ, its locator, and **precisely what is missing**.
- **`absent`** — and you must **search before declaring absence**. If you looked and could not
  find it, say "searched `<what you searched>`, not found" rather than a bare "absent".

**Reconcile before recommending.** If a candidate was evaluated in this repo before, find the prior
verdict or intake and **re-assess at today's scale** — never relitigate silently. If you cannot
locate a prior verdict, say **"unlocatable"** — do not say "unevaluated".

## ADOPTION FRAMING + THE HARD CONSTRAINT

**ADR-112 two-tier adoption bar:** Tier **L** evaluates; Tier **S** tries and keeps or deletes. For
every candidate, name **the cheapest experiment that would settle adoption here** — concretely, not
"pilot it".

**CARRIED CONSTRAINT, first-class for every candidate:** Windows wheels + installability under the
pinned `uv` (`required-version = "==0.11.19"`). The `rustworkx` precedent is the bar.
**Self-hosted-friendly scores above SaaS-only. Heavyweight server-dependent stacks score against
it** — say so explicitly, per candidate, rather than in a general caveat at the end. This constraint
does more work on this lane than on any other: several Shelf 5 and Shelf 6 candidates are the exact
shape it excludes.

## THE SURVEY — three shelves

### Shelf 4 — AGENT ORCHESTRATION

**LangChain / LangGraph, AutoGen, CrewAI, plus any current leader we are missing** — versus our
**PLAYBOOK Ch8 dispatch + lane contracts + the sentinel**. Read those before scoring.

**Hypothesis to attack, not to confirm:** *our moat is gates and contracts, not call-orchestration*
— so **could LangGraph-class state machines replace hand-rolled lane plumbing while our gates
stay?** Argue it both ways and land a verdict.

**RECONCILE FIRST:** LangChain was evaluated in this repo before. Find the prior verdict or intake
and **re-assess at today's scale** rather than relitigating from zero. If you cannot find it, say
**"unlocatable"** — do not say "unevaluated".

Note the Layer-2 tension explicitly: an orchestration framework that wants to *run* things collides
with the invariant that this repo never executes. Say whether that kills the candidate here, or
merely relocates it to a child repo.

### Shelf 5 — LOCAL MEMORY / INDEX (the "small model per repo" core)

**`sqlite-vec`** — note that **this repo already runs sqlite per ruling R-A, so it is the natural
first probe** — plus **ChromaDB**, **LanceDB**, **sentence-transformers** local embedders, and the
agent-memory layers **Mem0 / Letta (MemGPT) / Zep**.

Assess against **our actual need**: a learned **"where is what / what matters"** index feeding the
**file-purpose graph (FPG)** and the **boot surfaces**. Read the FPG work and the boot surfaces
before scoring; a verdict written against an imagined need is worthless.

**Say clearly what local models are actually good for** — retrieval, ranking, importance-learning —
**versus not** — decision-making, generation quality. **Evidence, with numbers where numbers
exist**, and evidence tiers throughout. This is the empirical core of the shelf, not a framing
sentence.

### Shelf 6 — LOOP EVALUATION / OPTIMIZATION

**DSPy** — prompt-as-program with metric-driven optimization. Assess specifically as **the
scientific backbone for the PROMPT DISTILLER filing**, which is **adjacent to `[#617]`**; resolve
that row and read it, and say "unlocatable" if you cannot.

Plus **promptfoo** and **DeepEval** as the eval harness — **SDA-1 already told us to check these
before hand-rolling anything**. Find that instruction if it is locatable in-repo.

**A finding from AUT-R4-A's shelf binds your verdicts here, and you should treat it as given
unless your own sources contradict it** (in which case say so): on **SkillsBench**, human-authored
skills raise pass rates **~16.2 pp** while **LLM-authored skills give no measurable gain**, and
**SkillAxe-style evaluation-guided refinement** is the published fix. **The consequence: a
prompt/skill distiller without an eval loop ships a useless library.** Verify it against the primary
source, then apply it — a DSPy verdict that ignores the eval-loop requirement has missed the point
of the shelf.

## SHAPE OF THE ARTIFACT

1. **Lead with the Shelf 4 verdict** — can a LangGraph-class state machine replace our lane
   plumbing while the gates stay, yes or no, and on what evidence. It is the arc's live question.
2. Then the three shelves in order, each with its candidates.
3. Then **one consolidated verdict table**: shelf · candidate · what it actually provides ·
   maturity/maintenance signal (last release, commit cadence, open-issue shape) · Windows/`uv`
   installability · self-hosted vs SaaS · verdict (`already-have-it` / `partial` / `absent`) ·
   cheapest experiment.
4. Keep sources inline with their evidence tier and rough date.
5. **Rank by fit × value. Six well-sourced candidates beat twenty thin ones.**
6. **State your own limits at the end:** what you could not verify, what you marked unlocatable, and
   what you would need in order to settle each.

Because AUT-R3 is covering these shelves at appendix depth concurrently, add one closing paragraph
naming **where you went deeper than a survey would** — it is how the architect will know which of
the two artifacts to trust on each candidate.
