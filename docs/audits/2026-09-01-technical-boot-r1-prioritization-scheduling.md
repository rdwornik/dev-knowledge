# BOOT-R1 — Prioritization and scheduling algorithms for a task graph under constraints: survey, measurement and fit-assessment

**Lane:** BOOT-R1 (read-only) · **Date:** 2026-09-01 · **Feeds:** F1 / `[#611]` — the `/boot-session` boot-inversion carrier
**Repo state at survey:** `worktree-boot-r1-survey` @ `9addeba8` (main incl. the batch-F freeze merge), clean tree
**Rows birthed:** zero · **Existing files edited:** zero · **Gates run:** none
**Format note:** flat markdown, no pipe tables (CLAUDE.md §4 output-formatting).

---

## 0. Method, and what to distrust in it

**What I ran.** Repo reads (`grep`/`sed`/`cat`); five read-only measurement scripts executed with
`uv run --locked python` from this worktree, each writing nothing to the tree. Every number below
is reproduced on **this** tree at `9addeba8`, not inherited from a prior artifact. Every one was first taken at `12720fcf` and **re-run unchanged** after a `--ff-only` sync-merge advanced the lane to `9addeba8` (three `tasks/` files moved); all figures were identical across both trees. Web search and
`WebFetch` for the external half.

**Source provenance is marked on every external citation**, on AUT-R1's convention:

- `[FETCHED]` — I opened the page in this session and am quoting it.
- `[SNIPPET]` — the search tool returned quoted content; I could not open the page. Second-hand.
- `[BLOCKED]` — the publisher refused (`onlinelibrary.wiley.com` and `dl.acm.org` both returned
  **HTTP 403**). Anything from those is `[SNIPPET]` at best.

**What to distrust, stated up front.**

1. **The practitioner literature on WSJF/RICE/ICE is almost entirely vendor-authored.** Of the
   ~25 results returned across four searches, the overwhelming majority are product-tool blogs
   (airfocus, ProductPlan, monday.com, Plane, Rock, Intercom, Whatfix). They are evidence of
   **practice**, not of **effect**. I have graded them accordingly in §3 and no verdict rests on one.
2. **My measurements are a single snapshot of one repo.** 169 open rows on one day. They are
   strong evidence about *this* population's **structure** (which is stable) and weak evidence
   about its **dynamics** (which I did not observe over time).
3. **The 0-of-7 predictive result in §7.2 has a benign reading** and I give it in full there.
   Do not quote the number without the reading.

---

## 1. Reconciliation with AUT-R1 — what I consume rather than repeat

`docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md` is the AUTONOMY-arc
survey whose **axis 3 (self-planning repositories)** overlaps this brief. I take the following as
**settled and do not re-derive it**:

- **The verdict enum is the ruled three** — `already-have-it` · `partial` · `absent`
  (AUT-R1 §1; stated explicitly at `docs/audits/2026-08-29-technical-aut-r2-decision-quality-frameworks.md:24`).
- **Axis 3's verdict stands:** `already-have-it` (doctrine) / `partial` (enforcement). The
  propose-only envelope, the frozen bundle, the consumption ledger and the ~5/night cap are ahead
  of anything AUT-R1 could source. I do not re-survey propose-only agent architectures.
- **The one-reviewer population is the binding constraint**, not the substrate. AUT-R1: *"Every
  axis-3 instance I found assumes a CI cluster and a team of reviewers… Here there is one
  reviewer, and the ceiling is his morning."* This is load-bearing for §4 and I build on it.
- **The industry's answer to prose-that-does-not-bind is a permission boundary, not a better
  sentence** (gh-aw safe-outputs). Consumed; not repeated.
- **AUT-R1 §7's negative result** — no published operator-scale (n=1) autonomous SDLC practice
  exists. Every cost/concurrency figure in the field assumes a team.

**Where this lane departs from AUT-R1, deliberately.** AUT-R1 surveyed *how work gets proposed*.
This lane surveys *how the proposal gets ordered and cut into a batch* — and AUT-R1 flagged the
seam itself at its §6 fit-assessment: *"This is backlog ranking, not catalog ranking — the two are
different problems and the repo should not let one stand in for the other."* AUT-R1 was speaking
of catalog curation; the same sentence applies one level down, and §7.3 below shows the repo is
currently letting **queue ordering** stand in for **batch selection**, which are also two problems.

**Also consumed — the routing law from the decision tree.** `docs/audits/2026-08-30-technical-autonomy-decision-tree.md`:
*"every absent property is downstream of a metric, and the metric is RANK 1."* Eighteen of 55
leaves were TRUE GAPs and only two became rows; the rest were PARKED behind a named trigger. That
law governs my own recommendations: **nothing here that needs a measurement it does not have
becomes a row.** It becomes a parked finding with its trigger named.

---

## 2. The governing measurement — the graph is not the problem

Everything downstream turns on this, so it comes before the survey rather than after it. All
figures measured on `tasks/` at `9addeba8`, predicate stated per line.

```
population                     360 task files; 169 with `status: open` in frontmatter
priority mix (open)            P1 17 · P2 102 · P3 50

THE PRECEDENCE GRAPH (`depends-on:`, open->open edges only)
  edges                        13
  distinct rows touched        24
  isolated vertices            145 of 169  (85.8%)
  longest chain                2 nodes / 1 hop   <-- no transitive chain exists anywhere
  rows BLOCKED by an open dep  12
  TOPOLOGICAL FRONTIER         157 of 169  (92.9% of the queue)

THE DISJOINTNESS GRAPH (`serialize-group:` = mutual exclusion, one clique per group)
  groups (open)                11    audit-py 34 · architecture 22 · handoff 11 · gates 8 ·
                                     pre-commit-config 7 · settings-json 7 · playbook 6 ·
                                     claude-md 4 · environment 4 · codex-review 3 · docs-gate 1
  ungrouped open rows          62
  conflict edges               947
  MAXIMUM INDEPENDENT SET      73     (= 11 groups + 62 ungrouped)

ADR-110 batch ceiling          4-10 design target; batch F dispatched 7
  slack at the ceiling         73 - 7 = 66
```

**Three conclusions, and they reshape the brief.**

**(a) The precedence DAG is very nearly empty.** A topological filter removes **12 rows out of
169**. There is no chain longer than one hop, so there is no critical path to compute: *critical
path* and *longest path* are defined on chains, and the longest chain here is a single edge.
`dag_longest_path` over this graph returns 2. Every classical CPM/PERT construct — float, slack,
the critical chain — is **identically trivial** on this population. This is not a claim that
precedence does not matter; it is a claim that precedence is nearly always already satisfied.

**(b) Disjointness is the real constraint, and it is 73× denser** — 947 edges against 13. The
brief's instinct ("disjointness as a resource") is correct and the ratio quantifies it.

**(c) But disjointness does not bind at the batch ceiling either.** The maximum set of mutually
co-runnable rows is **73**; the batch protocol dispatches **4–10**. You need 7 disjoint rows and
you have 73. **Neither structural constraint is scarce at the width the repo actually runs.**

**The load-bearing structural fact — why no solver is needed.** `serialize-group` is
**single-valued in practice**: I checked all 360 task files and **zero** carry more than one
`serialize-group:` frontmatter key or more than one `· serialize-group:` body clause, and
`gen_task_tree.derive_serialize_group` (`scripts/gen_task_tree.py:326`) uses `.search()` — it
reads the **first** clause and no other. So each row belongs to at most one group, the conflict
graph is a **disjoint union of cliques** (a cluster graph), and on a cluster graph:

> Maximum (weight) independent set = **take the best member of each clique, plus every isolated
> vertex.** It is a `sort` followed by a first-seen filter — exact, O(n log n), no solver.

**This is the whole answer to the brief's part (2), and it forecloses OR-Tools here.** CP-SAT
solves a problem this repo does not have.

**The honest limit, and it is a real one.** That property is **contingent and ungated**.
`scripts/validate_backlog.py:34-38` states the *design* admits multi-group rows — *"A task may carry
≥1 such clause — one per shared surface it collides on (multi-surface collision, #167) — and is
placed in EVERY named group"* — while the deriver reads exactly one. The spec and the deriver
**disagree**, and nothing tests the disagreement. Today the population makes the question moot
(zero multi-group rows). The moment one is filed, the conflict graph stops being a cluster graph,
greedy stops being exact, and `derive_serialize_group` silently drops the second group. §10 turns
this into the cheapest check I found.

---

## 3. Part (1) — scoring models: what is measured, what is practiced, what is asserted

The brief asks for the evidence grade, so I grade rather than summarize.

### 3.1 MEASURED — the small honest core

**Berntsson Svensson & Torkar, "Not All Requirements Prioritization Criteria Are Equal at All
Times: A Quantitative Analysis"** `[FETCHED arxiv.org/abs/2104.06033]`. Journal of Systems and
Software (2024); arXiv 2021. **Design, verbatim from the abstract:** *"a quantitative study of one
completed project from one software developing company by extracting **32,139 requirements
prioritization decisions** based on **eight** requirements prioritization criteria for **11,110
requirements**."* **Finding, verbatim:** *"not all requirements prioritization criteria are equally
important, and this change depending on how far a requirement has reached in the development
process."*

This is the largest quantitative dataset I could reach, and it is the one result that **directly
contradicts the shape of WSJF and RICE**: both apply a **fixed** weighting across an entire
backlog. The paper's finding is that criterion importance is **stage-dependent**. A single formula
applied uniformly to a queue is contradicted by the best available measurement, and its own
authors note the criteria in practice *"are often identified by gut feeling instead of an in-depth
analysis."* Note the population — one company, one project — so this is one strong study, not a
literature.

**Scalability of pairwise methods.** *Scalability and Limitations of Existing Software
Requirements Prioritization Techniques: A Systematic Literature Review*, Yaseen et al., Journal of
Software: Evolution and Process 37(8), 2025 `[SNIPPET — onlinelibrary.wiley.com and dl.acm.org
both 403 BLOCKED]`. Reported findings: AHP is the most-cited of **49** identified techniques, and
*"AHP and pairwise comparison techniques experience scalability issues, with complexity increasing
to four times the effort as the number of requirements doubles"* — i.e. **O(n²)**. On 169 open
rows AHP is ~14,196 pairwise comparisons. **Foreclosed on arithmetic**, and note this is the same
argument the repo already made for itself in `tasks/566-…`: *"WSJF alone = 732 new estimates"*.
I could not open the paper; treat the "four times" phrasing as second-hand.

### 3.2 PRACTICED — real adoption, no controlled evidence

WSJF (SAFe's `Cost of Delay ÷ Job Duration`), RICE (`Reach × Impact × Confidence ÷ Effort`), ICE,
MoSCoW. These are genuinely and widely used. **What I could not find is a controlled study showing
that any of them produces better outcomes than the ranking it replaced.** The most candid vendor
statement in the corpus is the honest one `[SNIPPET agility-at-scale.com]`: *"In most cases,
there's no way to empirically know that you've made the right decision until after you've made it
and executed."* SAFe's own extended guidance concedes the denominator is *"estimated subjectively:
a team guesses duration and moves on"* `[SNIPPET framework.scaledagile.com/wsjf]`.

The one improvement with a mechanism behind it: *"Teams that replace subjective duration estimates
with **empirical cycle-time data** produce more accurate WSJF rankings"* `[SNIPPET]`. That is a real
lesson and it is **the opposite of adding estimates** — it says replace a guessed input with a
measured one. It is the only part of WSJF this repo could adopt honestly, and §9 uses it.

### 3.3 ASSERTED — the numeric shell

RICE's failure mode is named consistently and independently across the vendor corpus, which is
weak evidence of practice but *consistent* weak evidence: **false precision.** `[SNIPPET
airfocus.com, rock.so, pmtoolkit.ai]` — *"a score of 812 looks exact but is built on estimates";
"a score of 42.7 vs 41.3 does not mean one feature is truly better"; "the precision is inherited
from the estimate quality, not the formula"; "Confidence is self-reported and easy to inflate."*
Four uncertain inputs multiplied and divided yield a number whose apparent resolution is entirely
manufactured. MoSCoW has the opposite pathology — it is a four-bucket ordinal with no tiebreak, so
it degenerates the moment "Must" exceeds capacity.

### 3.4 How aging/rot enters the score — and the finding that matters most here

The brief asks specifically how aging enters. The answer in the product-management literature is:
**it does not.** Neither WSJF, RICE, ICE nor MoSCoW contains a wait-time term. WSJF's
*Time Criticality* is a **deadline** property of the item, not a function of how long it has
waited; re-scoring is manual and event-driven (*"a competitor launches, a market window shifts"*
`[SNIPPET]`).

The discipline that **does** have a rigorous answer is operating-system scheduling, and the
concept is exactly named:

> **Starvation / indefinite blocking** — *"a low-priority process keeps waiting indefinitely
> because higher-priority processes continuously get the CPU"*; **aging** — *"a technique that
> gradually increases the priority of waiting processes"*, *"based on its waiting time in the
> ready queue"* `[SNIPPET geeksforgeeks.org, en.wikipedia.org/wiki/Aging_(scheduling), Silberschatz
> is the standard textbook source]`.

**This repo's ranking key has textbook starvation, and I measured it.** The live key is
`(P-enum, −contention, id)` — strictly lexicographic, so **every P1 and P2 precedes every P3**, and
`id` (the age proxy) only ever breaks a tie *within* a tier. Measured on the open queue:

```
oldest open P3 is [#130]; oldest open P1 is [#359]; oldest open P2 is [#112]
[#130] is older than ALL 17 open P1 rows ahead of it
rows that must clear before the oldest P3 becomes reachable: 119
8 of the 12 oldest open rows in the whole queue are P3
```

Age cannot promote across a tier. A P3 row can wait forever, and **the starvation is already
realized, not hypothetical** — two thirds of the queue's oldest rows are the ones the key can
never reach.

**I am not recommending an aging term.** Whether P3 *should* starve is a **functional** question —
"P3" may well be the operator's deliberate way of saying *never, unless it is free* — and ADR-108
§A routes functional questions to the operator, not to a research lane. What BOOT-R1 owes is the
measurement and the named choice, which is §9.3.

---

## 4. Part (2) — dependency-aware scheduling on a DAG under resource constraints

### 4.1 The classical frame, and why most of it does not land

Resource-Constrained Project Scheduling (RCPSP) is the textbook home for "a DAG plus renewable
resources", and it is NP-hard in general. Its machinery — critical path, float, resource
levelling, disjunctive constraints — assumes **durations**, **a resource pool**, and **chains long
enough for slack to mean something**. Measured against §2: the repo has no durations on rows, no
renewable resource other than the operator, and a longest chain of **one hop**. The frame does not
land, and importing it would be importing a vocabulary rather than a capability.

The construct that *does* land is the narrow one the brief named: **disjointness as a resource** —
which is not RCPSP but **mutual exclusion**, and on this population reduces to §2's cluster-graph
result.

### 4.2 The library call — measured, not assumed

Measured in this worktree, `uv run --locked`, CPython 3.12.10, `Windows-11-10.0.26200-SP0`:

```
rustworkx  0.18.1   ALREADY INSTALLED and already a declared dependency (pyproject.toml,
                    prebuilt wheel rustworkx-0.18.1-cp310-abi3-win_amd64.whl, hash-pinned
                    in uv.lock, numpy transitive cost already stated in the pyproject comment)
networkx            ModuleNotFoundError -- absent
ortools             ModuleNotFoundError -- absent
```

**Everything F1 needs is already importable at zero dependency cost.** Present in `rustworkx`
0.18.1, verified by introspection rather than from docs:

```
topological_sort · lexicographical_topological_sort · topological_generations
dag_longest_path · dag_longest_path_length · dag_weighted_longest_path(_length)
transitive_reduction · descendants · digraph_find_cycle · simple_cycles
graph_greedy_color · max_weight_matching · digraph_bfs_layers · layers
```

Two specific picks for `scripts/boot_frontier.py`, with reasons:

- **`lexicographical_topological_sort`, not `topological_sort`.** A plain topological sort is free
  to return any valid order; a boot artifact that is regenerated and gate-diffed needs a
  **deterministic** one. The lexicographic variant takes a sort key and yields a reproducible
  order — that is the difference between a generator that can be drift-gated and one that cannot.
- **`topological_generations`** gives the frontier directly as generation 0, rather than
  hand-rolling an in-degree sweep.

**Rejected, with reasons — and note the reason is never "the dependency is expensive":**

- **`networkx`** — REJECTED. Standing ruling R-A already settles the choice (*"if a consumer is
  ever named, the library is rustworkx, not networkx"*, quoted in `pyproject.toml`), and rustworkx
  is already paid for. Adding networkx would be a second graph library for zero capability.
- **OR-Tools / CP-SAT** — REJECTED, and this is the substantive call. Not on wheel grounds
  (OR-Tools does ship Windows wheels) and not on dependency-policy grounds, but because **the
  problem is polynomial and the exact answer is a sort** (§2). A CP-SAT model over 169 boolean
  row-variables with 947 mutual-exclusion clauses would return, after a solver invocation, the
  answer that `sorted(...)` plus a `seen` set returns exactly. Adopting it would add a
  constraint-programming dependency, a modelling surface, a solver-version pin and a nondeterminism
  risk (CP-SAT is deterministic only under a fixed seed and worker count) to compute a greedy.
  **Reach for CP-SAT if and only if the cluster-graph property breaks** (multi-group rows appear,
  §2's honest limit) *and* the width constraint starts binding. Neither holds; the trigger is named.
- **Dedicated scheduling libraries** (`simpy`, `pyschedule`-class) — REJECTED. They model
  durations and resource pools the repo does not have.

### 4.3 What the frontier is actually worth

Since 92.9% of the queue is on the frontier, the topological leg of `boot_frontier.py` is
**correct but nearly inert**: it removes 12 rows. That is not an argument against building it —
it is cheap, it is already a declared dependency, and it is the leg that stays correct if the
dependency graph ever thickens. It **is** an argument against believing it is the hard part. The
hard part is the scoring seam, and §7.3 shows why.

---

## 5. Part (3) — determinism vs judgment: where the line is drawn, and how the override is audited

**Where practitioners draw the line.** Consistently, and it is the one place the vendor corpus and
the AI-governance corpus agree: **the computed score orders, the human decides, and the override
is a recorded event rather than a mutation of the inputs.** From the governance literature
`[SNIPPET link.springer.com, presidio.com, cobbai.com]`: *"formally accountable human actors retain
decision authority, explicit override rights, and responsibility for approval, escalation, and
post hoc justification"*; HITL designs *"maintain actionable logs of interventions including
timestamps, conditions, and rationale"*; *"visibility into the inputs used, the policies applied,
who reviewed or overrode the decision, and what happened as a result."*

**The failure mode is specific and it is the most important sentence in the whole survey**
`[SNIPPET technical-leaders.com]`:

> *"Teams adjust scores until the spreadsheet agrees with what they already believed. The
> framework didn't remove bias. It just hid it."*

That is **score laundering**, and it is the mechanism by which a scoring model becomes theatre
(§6). The structural defense against it is the one this repo already implements: **keep the human
judgment as an explicit, first-class, human-owned field that the computed part may only order
*under*, never overwrite.** If judgment has a declared home, it does not need to be smuggled into a
Confidence multiplier.

**This is `already-have-it`.** The hand-set `[P1..P3]` **is** the override, and its architecture is
already correct on all three counts the literature asks for:

- **It is primary, not a modifier.** `rank_key` (`scripts/gen_task_tree.py:1558`) puts `P-enum`
  first; the derived term can only order a tie block. `render_ranking` prints this in the report
  itself: *"contention measures THROUGHPUT, not value — it orders a tie block, it never overrides
  a hand-set P."*
- **It is authored, not derived.** The module comment is explicit: *"The whole axis is DERIVED. It
  authors no field."*
- **It is audited by construction.** The override lives in a committed, diffable file under
  `tasks/`, so every change to it is a commit with a message, an author and a date. The
  governance literature's "log interventions with timestamps and rationale" is *git*, and the repo
  gets it for free. `[#589]`'s VIEW-projection split (`BACKLOG.md` generated from `tasks/`) means
  the override has exactly one home.

**One gap against the literature's bar, stated precisely.** The recorded override carries **no
rationale field** — a priority flip is visible in `git log` as a value change, and the *reason*
survives only if the commit message happens to carry it. Nothing requires it. I am **not** filing
this: it is a schema change to the backlog source of truth, which `scripts/funnel_lifecycle.py`
already establishes is *"a ruling, not a check"* (its leg-(c) note makes exactly this argument for
a `source:` key and declines to invent it). Recorded as a finding for the operator.

---

## 6. Part (4) — negative results: prioritization schemes that decayed into theatre

Four distinct decay mechanisms, separated because they have different fixes.

**(a) Score laundering — the score is fitted to the conclusion.** §5's quote. The tell is that
scores get *adjusted* in the meeting until the ranking matches the prior. **Fix:** give judgment a
declared home so it need not hide. **Repo status:** defended — `[P1..P3]` is that home.

**(b) False precision — resolution manufactured by arithmetic.** §3.3. Four guesses combine into
`812`. **Fix:** ordinal buckets and a refusal to rank within noise. **Repo status:** defended —
`[P1..P3]` is a 3-bucket ordinal, and the derived tiebreak is an integer *count* (group size − 1),
not an estimate. Nothing in the live key is a guess.

**(c) Estimate-cost collapse — the model costs more than it returns.** The pairwise-comparison
O(n²) result (§3.1) and the repo's own *"WSJF alone = 732 new estimates"* are the same failure.
A model requiring per-row human inputs across a 169-row queue will be filled in once, carefully,
and thereafter by pattern-matching. **Fix:** derive every term from fields that already exist for
another reason. **Repo status:** defended, and this is the strongest thing in the repo's design —
`tasks/566-…`'s LEAN takes `priority`, `serialize-group` and `id` because all three are *already
authored for other purposes*, so the ranking *"adds nothing to maintain and cannot rot
independently of the queue it ranks."* That is a genuinely good idea and I found no industry
source that states it as clearly.

**(d) The persistence gap — the ranking does not survive contact with execution.**
`[SNIPPET technical-leaders.com]`: *"Teams run RICE scoring… and leave planning sessions with clear
priority orders, but three weeks later, engineering is working on something that wasn't even in
the top ten."* The diagnosis offered is that *"prioritization frameworks solve the wrong problem —
the hard part isn't deciding what's most important, but making those decisions persist."*
**Repo status: this is the live one, and §7.2 measures it.**

**A fifth, from AUT-R1, consumed:** a ranking can go **dormant** without anyone noticing a cost —
STANDING_RULINGS' R1–R4 retirement ranking has been inert since the `[#487]` refutation
(`docs/audits/2026-08-08-technical-successor-prep.md:76`). An unused ranking decays silently
because nothing measures whether it fired. That is a real precedent *in this repo* for the
decay this section catalogues.

---

## 7. Fit-assessment against the organs

### 7.1 The organs, and what each already answers

- **`tasks/` graph** — 360 files, frontmatter `id|status|priority|serialize-group|depends-on`.
  The source of truth since the `[#439]` flip. It already carries **every input any defensible
  scoring model would need**, and nothing more would need to be authored.
- **`serialize-group`** — mutual exclusion over a shared mutable surface. Derived, single-valued in
  practice, and the basis of `validate_backlog.py`'s parallel-safety rule: *"two tasks co-run iff
  no depends-on path links them and they share no group."* **That sentence is already an exact
  specification of batch legality** — F1 does not need to invent one, it needs to implement this.
- **`gen_task_tree.py --rank`** (`[#566]`/`[#488]` LEAN) — **built and live**. Read-only, writes
  nothing, `(P-enum, −contention, id)`. Its own docstring carries the honest limit: *"this ranks
  THROUGHPUT, not value… a strong secondary key and a poor sole one."*
- **`funnel_lifecycle.py`** — four legs over end-of-lifecycle objects (terminal-status intake at
  depth 1; ACCEPTED-but-consumed; terminal ADR not archived; post-ARM_DATE row with no provenance;
  WARN on stale READY). It answers *"did this object leave its lifecycle"*, **not** *"how urgent is
  it"*. F1's contract names it as the source of **rot/orphans**, and that is exactly right — it is
  a *health* signal, and §9 keeps it out of the *ranking*.
- **Ledger rules** — PLAYBOOK Ch8 phase 5. The consumption ledger is a **REQUIRED** output, and its
  binding property is that **rejected items are listed with their reason**. AUT-R1 found no
  industry equivalent. It is the anti-relitigation organ, and it is what "ledger-bounded" in F1's
  contract must mean.
- **Decision tree** — `docs/audits/2026-08-30-technical-autonomy-decision-tree.md`. 55 leaves
  routed, every leaf carrying an id or a reason, and the metric-first law (§1).
- **`[#528]` integration cost** — *"full suite 1001 s, and a 4-leg batch lane pays that roughly
  once per lane plus once per merge, ~50 min wall-clock."* Legs 1+2 merged at `7d1f6ce0`; **leg 3
  (emit `test_run` duration via telemetry) is OWED.** This is the only real *cost* term available
  to any scheduler, and it is not yet measured per-row.
- **ADR-110** — ONE plan → N **file-disjoint** lanes → ONE integrator; serial integration;
  **exactly 2 operator touches per batch** (GO · end-of-batch packet).

### 7.2 The predictive test — and the honest reading

The one test that matters for a batch proposer: **does the computed rank predict what the operator
actually dispatched?** Batch F's manifest names its seven lanes' rows. Measured against the live
key over the 169-row open queue:

```
[#611]  rank 106 of 169   P2   contention 0
[#626]  rank 117          P2   contention 0
[#276]  rank  87          P2   contention 0
[#621]  rank 115          P2   contention 0
[#627]  rank 118          P2   contention 0
[#629]  rank  17          P1   contention 0
[#630]  rank 119          P2   contention 0

OVERLAP WITH THE COMPUTED TOP-7:  0 of 7
```

**The benign reading, and I believe it is the correct one.** This is **not** evidence that the
ranking is broken. The operator cut batch F on a **theme** — *"substrate, debt and the two ruled
predicates"* — which is an arc-coherence judgment the key cannot see and, I would argue, **should
not** see. Six of the seven are P2, so the operator deliberately reached past 17 open P1 rows to
assemble a *coherent* batch rather than a *high-scoring* one. That is exactly the strategic act
§6(d) says frameworks cannot replace.

**But it does establish one thing decisively, and F1 must not miss it:** a computed rank is **not**
a batch proposal, and shipping one as *"PROPOSED NEXT BATCH"* would propose seven rows the operator
demonstrably would not have picked. The gap between rank and selection is where judgment lives, and
the boot artifact's job is to **inform** that judgment, not to pre-empt it.

### 7.3 The defect this lane found — the contention term inverts under batch selection

This is the finding with the most direct consequence for F1's build.

`contention DESC` prefers rows in the **largest** serialize-groups — the throughput logic of
"clear the bottleneck". But a **batch** requires **mutually disjoint** rows, and at most **one**
row may be taken from any group. So the term that ranks a row *up* is precisely the term that
makes its neighbours *ineligible*. Measured, width 7, over the frontier:

```
WITH contention (the live --rank key)
  top-7 groups   audit-py, audit-py, audit-py, architecture, architecture, architecture, handoff
  colliding rows 4
  RUNNABLE AS A BATCH:  3 of 7

WITHOUT contention (P-enum, id)
  top-7 groups   handoff, none, architecture, environment, none, none, architecture
  colliding rows 1
  RUNNABLE AS A BATCH:  6 of 7

DISJOINT-GREEDY over the whole frontier (one per group, best first)
  fills 7 of 7 -- and all seven are P1:
  [#581] audit-py · [#519] architecture · [#359] handoff · [#528] environment ·
  [#514] none · [#555] none · [#579] none
```

**Three things follow.**

1. **Naively slicing `--rank`'s top-K into a batch loses 4 of 7 lanes.** F1's contract says
   *"PROPOSED NEXT BATCH (decision-tree ranked, ledger-bounded)"*; if "ranked" means the live key
   sliced at width, the proposal is maximally colliding by construction.
2. **A one-line disjointness filter recovers all of it** — 7 of 7, every one a P1. The fix is
   `seen = set()` over the sorted frontier. No solver, no new dependency, ~5 lines.
3. **Under that filter, the contention term becomes inert at width 7** — both orderings yield the
   same seven rows. So contention is *harmful* without the filter and *irrelevant* with it. It
   should not appear in the batch-selection path at all. **It remains correct where it lives** —
   `--rank` answers "what should I work on next", a different question with a different right
   answer. `[#566]` is not defective; **reusing it unmodified for batch selection would be.**

This is AUT-R1's own warning, one level down: *"the two are different problems and the repo should
not let one stand in for the other."*

---

## 8. Verdicts — the ruled three

```
Scoring models for backlog prioritization (WSJF/RICE/ICE/MoSCoW)
  VERDICT: already-have-it -- and the incumbent is BETTER than the alternatives surveyed.
  No candidate has controlled evidence; the best measured study contradicts fixed weights;
  all four require per-row estimates the LEAN already foreclosed on arithmetic.
  Recommendation: BUILD NOTHING. This is a closed question, not an open one.

Aging / anti-starvation as a scoring term
  VERDICT: absent -- measured, real, and NOT a technical question.
  119 rows block the oldest P3; age cannot cross a tier. Whether that is a defect or the
  intent of "P3" is FUNCTIONAL -> operator (ADR-108 §A). Named in §9.3, not filed.

Dependency-aware scheduling on a DAG (critical path, topological frontier)
  VERDICT: partial -- built where it matters, and correctly near-inert.
  Frontier = 92.9%; longest chain = 1 hop. Worth implementing (cheap, already-paid,
  future-proof); NOT worth believing is the hard part.

Disjointness as a resource / batch selection under mutual exclusion
  VERDICT: partial -- the SPEC exists and is exact (validate_backlog.py:36); the
  IMPLEMENTATION for batch selection does not, and the nearest reusable organ
  (--rank) inverts under it (§7.3). This is the one real gap, and it is ~5 lines.

Constraint solvers (OR-Tools CP-SAT) / a second graph library (networkx)
  VERDICT: absent -- and recommend NOT building. The conflict graph is a cluster graph,
  so the exact optimum is a sort. Trigger for revisiting is NAMED in §2's honest limit.

Determinism-vs-judgment: the override and its audit
  VERDICT: already-have-it. [P1..P3] is primary, authored-not-derived, and git-audited.
  One sub-gap: no rationale field on an override. A ruling, not a check. Not filed.
```

---

## 9. What F1 should do — the scoring seam, pinned

F1's contract states: *"BOOT-R1's survey is still RUNNING, so the scoring rule is a **declared seam
pinned later**, not a model invented to fill the gap."* This section is that pin.

### 9.1 The pin: no new scoring model

**The scoring seam should be pinned to the existing key, and the seam should stay a seam.**
`(P-enum, −contention, id)` from `gen_task_tree.rank_key` is reused **as an import, not a
reimplementation** — one ranking function, one home, no second copy to drift. §8 is the argument:
every surveyed alternative is either unevidenced, arithmetically foreclosed, or contradicted by
the best measurement available. Inventing a model here would be exactly the *"model invented to
fill the gap"* the contract forbids.

### 9.2 The three legs F1 should actually build

```
LEG 1  FRONTIER  rustworkx lexicographical_topological_sort / topological_generations over
                 the open depends-on graph. Removes ~12 rows. Cheap, deterministic,
                 already-paid, stays correct if the graph thickens. Assert acyclicity --
                 validate_backlog already guarantees it, so a violation is a real regression.

LEG 2  ORDER     import gen_task_tree.rank_key. Do not reimplement, do not extend.

LEG 3  SELECT    THE ONE NEW THING. Walk the ordered frontier, take a row only if its
                 serialize-group is unseen, stop at width. Exact on a cluster graph (§2).
                 ~5 lines, no dependency, no solver.
                 GUARD IT: assert each row yields at most one group. That assertion is the
                 §2 honest limit made load-bearing -- if a multi-group row is ever filed,
                 this fails loudly instead of silently dropping a constraint.
```

**And one thing F1 should NOT do: present the output as a decision.** §7.2 measured 0-of-7 against
the operator's real cut. The boot artifact should render the top-N *with its inputs visible*
(`P`, group, contention, age, rot flags) so the operator can see **why** a row surfaced and
override in one glance — the "explanation pack with score breakdowns" the governance literature
asks for, which here costs nothing because every input is already a field. Label it a **candidate
set**, never a proposed batch. That framing is also what keeps the V-2 budget intact: an artifact
that must be argued with costs an operator touch; one that informs does not.

### 9.3 The one question that is the operator's, not F1's

> **Should age be able to promote a row across a priority tier?**
>
> Today it cannot: 119 rows block the oldest P3, and `[#130]` is older than all 17 open P1s.
> **(a)** No — "P3" means *never unless free*, and the starvation is the intent. Change nothing.
> **(b)** Yes — add an aging term to the boot view *only* (not to `--rank`, not to `tasks/`), e.g.
> surface the N oldest untouched rows as a separate "starving" section rather than reordering.
>
> **(b) is the cheaper of the two even if wanted**, because a separate section changes no ranking
> and needs no ruling about what a tier means. I recommend **(b) as a display section** if the
> operator wants the visibility at all, and **(a)** otherwise. Either way this is ADR-108 §A
> functional territory and BOOT-R1 does not rule it.

---

## 10. The cheapest ADR-112 Tier-S experiment

**The Tier-S constraint, honored explicitly.** ADR-112 §"Tier S": *"Tier S never touches gates,
hooks that block, or `scripts/` — anything that would, is Tier L from the start."* So the obvious
candidate — a `validate_backlog` leg asserting single-valued `serialize-group` — **is Tier L, not
Tier S**, and I do not propose it as one. It is recorded in §2 as a finding with its trigger named.

**The Tier-S trial, and it is genuinely cheap:**

> **A repo-level `.claude/commands/batch-candidates.md`** — one command, no `scripts/` change, no
> gate, no hook, **zero rows**. It runs the existing `gen_task_tree.py --rank` (already read-only,
> already built), applies the §9.2 LEG-3 first-seen filter over `serialize-group` in the prompt
> body, and prints a width-N candidate set with each row's inputs shown.
>
> **Why this one.** It is the *only* proposal here that produces the missing evidence **before**
> anyone builds `boot_frontier.py`. It makes §7.3's claim falsifiable by the operator in a single
> use: if the disjoint candidate set is one he would actually have dispatched, LEG 3 is validated
> and F1 builds it knowing so; if he reaches past it again, that is the measurement saying the
> boot artifact should present *health and candidates*, not a batch — and F1 builds something
> smaller. Either outcome is worth more than the command costs.
>
> **Keep-or-delete, per ADR-112:** keep if it changes what the operator dispatches or how fast he
> decides; delete after one batch otherwise. **It births no row either way.**

**Cost:** one markdown file. **Blast radius:** none — it reads, prints, and writes nothing.

**What I deliberately do NOT propose.** A telemetry-backed cost term for `[#528]` leg 3
(`test_run` duration per row) would be the one genuinely new *input* worth having — it is the only
way to get the empirical cycle-time that §3.2 identifies as WSJF's one honest lesson. **It is
PARKED, not filed**, under the decision tree's law: it is downstream of a metric that does not
exist yet, and its trigger is already named and owned — **`[#528]` leg 3 landing**. A gap birthed
ahead of its blocker is a row that cannot be worked.

---

## 11. Sources, and what I would want re-verified

**Fetched.** `arxiv.org/abs/2104.06033` — Berntsson Svensson & Torkar, *Not All Requirements
Prioritization Criteria Are Equal at All Times: A Quantitative Analysis* (JSS 2024; arXiv 2021).
Abstract quoted verbatim in §3.1.

**Blocked (403), used at snippet strength only.** `onlinelibrary.wiley.com/doi/10.1002/smr.70039`
and `dl.acm.org/doi/abs/10.1002/smr.70039` — Yaseen et al., *Scalability and Limitations of
Existing Software Requirements Prioritization Techniques: A Systematic Literature Review*, J.
Software: Evolution and Process 37(8), 2025.

**Snippet-only.** framework.scaledagile.com/wsjf · agility-at-scale.com · airfocus.com ·
productplan.com · rock.so · pmtoolkit.ai · technical-leaders.com · prodpad.com ·
michaelgoitein.com · geeksforgeeks.org · en.wikipedia.org/wiki/Aging_(scheduling) ·
link.springer.com/article/10.1007/s43681-026-01147-7 · presidio.com · cobbai.com

**In-repo, all opened.** `docs/audits/2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md`
(§1, §4, §5, §6, §7) · `docs/audits/2026-08-29-technical-aut-r2-decision-quality-frameworks.md:24`
(verdict enum) · `docs/audits/2026-08-30-technical-autonomy-decision-tree.md` (tally + metric-first
law) · `docs/audits/2026-09-01-technical-batch-f-manifest.md` (lane roster, the F1 boot-inversion
block) · `scripts/gen_task_tree.py` (`derive_serialize_group` :326, the `[#566]` axis :1491,
`contention_scores` :1536, `rank_key` :1559, `render_ranking`) · `scripts/validate_backlog.py`
(parallel-safety rule :34-38, `_parse_deps` :108) · `scripts/funnel_lifecycle.py` (module docstring,
four legs) · `scripts/validate_hermetization.py:149` (`AUDIT_CLASS_ENUM`) · `pyproject.toml`
(rustworkx declaration + R-A ruling + measured wheel) · `docs/decisions/ADR-110-*.md` (:41 batch
protocol, :150 width) · `docs/decisions/ADR-112-*.md` (:63 the Tier-S guard sentence) ·
`protocols/PLAYBOOK.md` Ch8 (phases, ledger) · `tasks/528-*.md` · `tasks/566-*.md`

**What I would want re-verified.**

- **The Wiley SLR's "four times the effort as requirements double".** I never opened the paper.
  The O(n²) shape is standard for pairwise comparison and the conclusion does not depend on the
  exact phrasing, but do not quote the figure in a ruling without fetching it.
- **The single-valued `serialize-group` property (§2).** True today across 360 files, guaranteed by
  nothing. It is the assumption LEG 3's exactness rests on, which is why §9.2 makes it an assertion.
- **The 0-of-7 predictive result (§7.2).** One batch, n=1. Batches D and E have manifests and the
  same measurement can be run over them retrospectively at zero cost — that would take it from an
  anecdote to a trend, and it is the first thing the §10 command should be pointed at.
- **`[#528]` leg 3's status.** Read from the row body, which records it OWED after `[#529]`. If it
  has since landed, the parked cost-term finding in §10 has had its trigger fire.
- **ADR-110's width line.** `:150` reads *"§2's 4–10 range is a design target, not a measured
  ceiling. No batch above 3 has run."* Batch F dispatched 7, so that sentence is stale at HEAD.
  Not my lane's to fix; flagged.
- **A discrepancy I could not resolve and am not papering over.** The `SessionStart` digest at boot
  reported `17 P1 / 119 P2 / 82 P3`. My predicate (`status:` in `tasks/` frontmatter) measures
  `open` = 17/102/50 and `open+deferred` = 19/122/82. P3 matches `open+deferred` exactly; P1
  matches `open` exactly; P2 matches neither. The two surfaces are counting different populations.
  Worth one look by whoever owns the digest; it is not load-bearing for anything above, because
  every figure in this artifact states its own predicate.

---

**END OF ARTIFACT — BOOT-R1. Zero rows birthed. No existing file edited. No gate run and none reported.**
