# AUTONOMY arc — what is REJECTED, and what is PARKED with a trigger

**Batch:** night-batch-2 · **Lane:** `pn-audits` (items C6 + C7) · **Date:** 2026-08-29
**Repo:** `.dev-knowledge` @ `worktree-pn-audits`, cut from `66662c70`
**Rows born:** ZERO — this lane holds no write on `tasks/`.
**Precedent for the form:** `protocols/ENVIRONMENT.md` §"Rejected (do NOT revisit before Q3)" — read for
voice, **not edited** (it belongs to a sibling lane in this batch).

---

## 0. Why this file exists, and what it is not

This repo already records what it declines. The `ENVIRONMENT.md` Rejected list is the precedent, and
its most useful property is visible in its own entries: two of the five carry **later annotations that
partially reverse them** (Codex CLI — *"REVERSED, and no longer binding"*; Mandatory TDD — narrowed by
ADR-108 §B rather than reinstated). A rejection here is therefore a **dated decision with its reasoning
attached**, not a permanent ban. That is the shape below.

**What this file is not:** it is not a triage of audit findings (that is §E6's sheet, a separate
artifact), and it does not birth, amend or kill a backlog row. Every item below was decided in the
AUTONOMY arc's framing conversation; this file is the record, written so that the next reader can
re-open a decision on evidence rather than re-litigate it on taste.

**Honest limit, stated up front.** Three of the four items below are rejections of things this repo has
**never built**, so there is no measured cost-of-removal to report — the evidence is corpus scale and
existing doctrine, not a post-mortem. Item C7 is the opposite: it is parked *against a hot spot that has
already been measured once*, and that measurement changed the answer. Read C7 first if you are short of
time.

---

## 1. The sheet

Flat, fenced, copy-safe:

```
id  item                                          outcome    binds until
--  --------------------------------------------  ---------  -------------------------------------------
C6a Fibonacci / golden-ratio NODE COUNTS          REJECTED   a consumer is named that reads the number
C6b TFP-class probabilistic inference over the    REJECTED   a query exists that a deterministic index
    governance corpus                                        provably cannot answer
C6c neural-network-as-implementation metaphor     REJECTED   (no re-open condition — the referent is
                                                             already built under its own name)
C7  formal cache layer for graph / derivation     PARKED     the four-part trigger in §3 fires, in order
    queries
```

**Scope note that matters: C6a is NOT the `[#488]` question.** See §2.1 — they share a word and nothing
else, and conflating them would silently kill an open row this lane has no licence to touch.

---

## 2. REJECTED — with reasons

### 2.1 · C6a — Fibonacci / golden-ratio **node counts** — **REJECTED**

**The proposal.** Size the governance structures — nodes per tier, children per parent, entries per
index — on Fibonacci or golden-ratio proportions.

**Reason: aesthetics with no measurable consumer.** The test this repo applies to any proposed number is
*who reads it, and what changes when it changes*. A node count chosen for proportion has no reader: no
gate asserts it, no generator emits it, no query ranks on it. It would be a constraint that can only ever
be violated, never used — and this repo has an explicit name for that class. `docs/audits/2026-07-04-rot-algorithm-design.md:37`
refuses a persistent graph store as *"machinery without a customer"*; the same bar refuses this, and it
refuses it more cheaply, because a cache at least has a hypothetical customer.

**The second reason is the one that would actually hurt.** A proportion constraint on node counts is a
rule that fights the corpus's own growth. Measured on this worktree:

```
docs/decisions/*.md      91
docs/intake/*.md         64
docs/audits/*.md        830
tasks/**/*.md           371
                      -----
governance objects    1,356        (git ls-files '*.md' = 2,254 tracked overall)
```

None of those four stores grows by choice — an ADR is born when a decision is ruled, an audit when a lane
closes. A target count would be missed by construction on every one of them, so the constraint's only
possible effect is to generate a standing violation nobody can fix. That is the failure mode
`CLAUDE.md` §4 names in its own words: *"a number typed into a doc is stale at the next commit."*

**DO NOT read this as killing the `[#488]` Fibonacci question — it is a different subject with the same
word, and the collision is the whole reason this paragraph exists.** `[#488]` and intake #17 §3 concern a
**Fibonacci ESTIMATE SCALE** for backlog sizing and overdue-ruling thresholds — a *ranking function's
input domain*, not a structural proportion. Its status is live and explicitly carried:
`docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:7` records §3 Fibonacci as
*"carried forward, not ruled here"*, and §7.4 says so again. `docs/audits/2026-08-19-technical-c4-ruling-prework.md:300`
measures today's actual scale as `S 116 · M 61 · L 6` — *"(3-value enum, NOT Fibonacci)"*. That question
has a consumer (a ranking function) and is therefore admissible on exactly the bar C6a fails. **Nothing
here touches it.**

**Re-open condition:** name a consumer that *reads* the node count and behaves differently at a different
value. Absent that, this is not revisited.

---

### 2.2 · C6b — TensorFlow-Probability-class probabilistic inference over the corpus — **REJECTED**

**The proposal.** Model the governance corpus probabilistically — a TFP-class inference layer over
~1k objects, yielding posterior beliefs about rows, findings or organs.

**Reason 1: deterministic indexes already answer in milliseconds, and the corpus is immutable by rule.**
The queries an inference layer would serve — which rows depend on which, which doc cites which code rule,
which finding resolves where — are already answered exactly, not probabilistically, by
`build_edge_index` / `scan_structural_integrity` (`scripts/validate_doc_code_edge.py`), the task-tree
dependency edges, and the disposition register. The corpus's own scale is the argument:
`docs/audits/2026-08-26-technical-perf-recon.md:66` records it as **immutable by rule** (CLAUDE.md §5.3 —
ADRs, transcripts, handoffs and audits never change after landing), and 1,356 objects is a size at which
a full rebuild-from-source is *cheaper than maintaining a belief state about it*. Probabilistic inference
buys uncertainty quantification; here the ground truth is on disk, tracked, and re-derivable, so the
uncertainty being quantified would be **manufactured by the model, not present in the subject**.

**Reason 2: the one genuine probabilistic need is real, and it is scipy-level.** This is the half worth
preserving, because rejecting the dependency should not reject the need. Benchmark work in this repo —
the SDA-1 instrument line, `docs/audits/2026-08-28-technical-sda1-benchmark-design-adversarial.md` and
its 2026-08-29 successors — has a legitimate statistical requirement: **power analysis and confidence
intervals on measured run-to-run differences**, so that "lane A is faster than lane B" is a claim with an
interval rather than a single wall-clock reading. That is a `scipy.stats` call. It is not a TFP-class
dependency, it needs no graph-mode compute, no probabilistic programming language, and no new fleet
baseline row.

**Reason 3: the dependency bar.** ADR-106 declares the environment via `pyproject.toml` + `uv.lock` with
`uv` pinned exactly, and `CLAUDE.md` §4 scopes `ecosystem/dependency-baseline.yaml` to *"only deps a
consumer needs to operate a methodology mechanism."* A TFP-class stack is the largest possible dependency
for the smallest demonstrated need, in a repo whose stated identity is *"NOT a code project"*
(`CLAUDE.md` §3). The `perf-recon` audit already applied this bar once and reached the same verdict about
a much smaller candidate — `:141-145` assesses `diskcache` / `joblib.Memory` and refuses them because they
*"solve a problem this repo does not"* have.

**Re-open condition:** exhibit a question about the corpus that a deterministic index provably cannot
answer — not merely one it answers slowly. Slowness is C7's subject, not this one.

---

### 2.3 · C6c — the neural-network-as-implementation metaphor — **REJECTED**

**The proposal.** Frame the system's development as a neural network: commits as weight updates, the
repo as a trained model, sessions as training epochs.

**Reason: a commit is not a weight update, and the real loop is already built under its own name.** The
metaphor fails on the property that makes a weight update a weight update — it is a *small, reversible,
gradient-directed adjustment*, applied in bulk, individually meaningless. A commit here is the opposite of
every one of those: it is discrete, reviewed, individually auditable, gated, and **deliberately
irreversible on the immutable classes** (an ADR, an audit, a handoff supersedes; it does not update).
`CLAUDE.md` §5 spends four of its nine critical rules on precisely this property. A metaphor whose central
mechanic is contradicted by the subject's central invariant is not a lens — it is a misdescription that
would take work to correct downstream.

**The real feedback loop exists, is named, and is running.** Telemetry → trends → rulings:

```
telemetry   logs/TOKEN-LOG.md · logs/PARITY-EVENTS.jsonl · logs/COHERENCE-NUDGE.log
            ecosystem/*-baseline.{yaml,json} · the nightly conformance digest
trends      ecosystem/conformance.md · ecosystem/doc-counts.md · the audit corpus itself
rulings     docs/decisions/ADR-*.md · protocols/STANDING_RULINGS.md
            ecosystem/disposition-register.yaml
```

That loop is slow, discrete, human-ruled and fully auditable, which is what this repo wants and what a
gradient is not. **The metaphor would not add a mechanism; it would rename one that already works, and
rename it inaccurately.** ADR-111's funnel is the same point made structurally: a finding is triaged into
exactly one of four *named* outcomes by a decision-maker, never averaged.

**Evidence that this is a live rejection, not a strawman:** grepped repo-wide over `*.md`,
`neural.network` / `weight update` / `backprop` return **zero** hits. Nothing has adopted the framing;
this record exists to keep it that way, and to say why in one place rather than in the next design
conversation.

**Re-open condition: none.** This is not a deferral. The referent is built and named.

---

## 3. PARKED — C7, with a trigger precise enough to test

### 3.1 · The item

**A formal cache layer for graph / derivation queries** — a persistent, invalidating cache in front of
`build_edge_index`, the task-tree dependency resolution, the anchor index, and the rot-algorithm's
reverse-reference multimap.

**Outcome: PARKED. Build it only when trends/telemetry show a measured hot spot — and the trigger below
is four-part and ordered, because the one time this trigger has already fired, a cache was the wrong
answer.**

### 3.2 · Why parked rather than rejected — the honest case FOR it

This is not a polite rejection. The case is real and is recorded:

- **A hot spot has been measured, not hypothesised.** `docs/audits/2026-08-29-technical-nb2-m-packet.md:317`
  — `build_edge_index` *"re-tokenizes every `.py` once PER RULE — **14.53s for 16 rules vs 0.75s for a
  single pass**, identical id set, on a query a human runs interactively."* A 19× gap on an interactive
  query is exactly the shape that justifies a cache.
- **Caching is already in the tree**, so the layer would not be novel: three `lru_cache` sites in
  `scripts/journal_anchor.py` (`:153`, `:275`) plus `_MAP_GENERATION`
  (`docs/audits/2026-08-26-technical-perf-recon.md:65`).
- **The corpus is immutable by rule** (ibid. `:66`), which is the single best precondition a cache can
  have: most of what would be cached *cannot* go stale, because the underlying artifact cannot be edited.

### 3.3 · Why it is parked anyway — the three counterweights

**(a) The one time this exact trigger fired, the correct answer was not a cache.** Lane M measured the
14.53s and shipped **a single pass** — *"parse once, run every rule over one pass"* — not a cache. It got
19× by removing repeated work rather than by memoising it, and it did so while *"the hardened scanners
(`markers_in_source`, `DOC_RE`) are still reused rather than re-derived."* A cache over the O(rules × files)
algorithm would have preserved the wrong algorithm and made its cost invisible. **This is the load-bearing
reason for the ordering in §3.4.**

**(b) Rebuild-per-run is ruled doctrine, and it is a correctness guarantee, not a performance default.**
`docs/audits/2026-07-04-rot-algorithm-design.md:37`: *"A persistent/incremental graph store would be
machinery without a customer — rebuild-per-run is the correctness guarantee, the same doctrine as
`validate_doc_code_edge.build_edge_index` (rebuildable index, **never a hand-kept cache**)."* ADR-88 P3
carries the same. A cache layer amends this doctrine; it does not merely add a component, so it is an
architect's ruling (ADR-108 §A — technical question), not an executor's optimisation.

**(c) The existing caches have already produced a correctness defect of exactly the feared class.** The
Codex review of the W2A perf work — `docs/audits/2026-08-26-codex-w2a-perf-core.md:29` and `:51` — raised
as **CRITICAL**: *"`journal_anchor.py:265` — parent-map cache can return a **stale Git graph**"*, in a
runner that *"holds one process across 46 checks"* while *"a test commits mid-process."* Three memoised
functions were enough to create a stale-answer window in a **fail-closed** gate. That is the empirical
cost of caching here, measured on this codebase, and it is why the trigger's part (4) exists.

### 3.4 · THE TRIGGER — four parts, in order. All four must hold.

A future reader can test each of these mechanically. It has **not** fired as of 2026-08-29.

```
(1) MEASURED, not felt.   A named query's wall time is recorded in a dated artifact
                          (docs/audits/** or logs/**), from a repeatable command, at
                          >= 2s on the interactive path -- or >= 10% of a gate's
                          total runtime. A recollection is not a measurement.

(2) ALGORITHM FIRST.      The single-pass / redundant-work fix has been ATTEMPTED and
                          its residual measured. Lane M's 14.53s -> 0.75s is the
                          precedent: if restructuring the work still gets the win, the
                          cache is not the fix and this trigger has NOT fired.

(3) REPEATED, not one-shot.  The query runs >= 2x per session on the same unchanged
                          inputs. A query run once per session cannot profit from a
                          cache no matter how slow it is -- that is (2)'s subject.

(4) INVALIDATION IS STATABLE.  The cache key and its invalidation event can be written
                          in one sentence, on an input that is immutable by rule or
                          content-hashed. If the answer depends on the live git graph
                          or another repo's working tree, part (4) FAILS -- that is the
                          journal_anchor.py:265 stale-graph CRITICAL, and it is a
                          refusal, not a caveat.
```

**How to test whether it has fired:** find a dated artifact satisfying (1); confirm (2) by locating the
attempted single-pass fix and its residual number; confirm (3) by counting call sites on an unchanged
input; confirm (4) by writing the invalidation sentence. If any part is missing, the item stays parked and
**this record is the answer** — it is not re-litigated in the design conversation that raised it.

**If all four hold, it is not a licence to build either.** It is a licence to file an intake (ADR-98),
because part (2)(b) above makes the cache layer an amendment to ruled doctrine, and ADR-108 §A puts a
technical question of that shape with the architect.

---

## 4. What this lane could NOT do, named rather than dropped

- **No backlog row born, amended or killed.** `tasks/` belongs to a sibling lane in this batch. If the
  operator wants C7's trigger to carry a watching row, that row must be born by the filings lane or the
  integrator — this file is its complete content, and no row is required for the decision to bind.
- **`protocols/ENVIRONMENT.md` NOT edited.** Its Rejected list is the acknowledged precedent for this
  file's form and was read for voice only; it is owned by another lane. **A candidate for the integrator:**
  whether the three C6 rejections should also be summarised as entries on that list, given that
  `ENVIRONMENT.md`'s list is the surface a future session actually boots past. This file is the reasoned
  record either way; the question is only whether a one-line pointer belongs there too.
- **No gate asserts any of this.** These are decisions of record, enforced by being findable. There is no
  detector that would fire if someone proposed golden-ratio node counts tomorrow, and this file does not
  pretend otherwise.
- **The `docs/audits/README.md` index is left STALE by design** — `[#590]` narrowed the index hook so a
  batch lane does not regenerate it. The integrator owns it.
