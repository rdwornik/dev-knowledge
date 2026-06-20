<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Generated from templates/handoff/v5/SUPPLEMENT.md.tmpl.

  This bundle is COLD: produced by a CC-driven session-wrap audit, with no outgoing browser
  architect chat to interview. Per the §13 cold-handoff disposition, ANSWERS is left EMPTY and
  the file is still committed (a durable record that this session carried no transmissible
  browser-side strategic *why* — the CC-derived "why" lives in RESIDUAL.md §3–§5). The incoming
  §13(d) operator-context beat therefore fires FULL. CC never fabricates answers.
-->

# Architect strategic supplement — 2026-06-20-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-20

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect). **← THIS bundle: cold.**

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Architect design-intent handoff — dependency-legibility organ

> **What this is.** The v5.2 state-bundle (`docs/handoffs/2026-06-20-dev-knowledge-architect/`)
> captures *verifiable state* — what shipped, what's gated, the PROBES that bind it. This doc
> captures what the machinery **cannot** derive from the repo: the *design reasoning*. Read
> both. The bundle tells you where things are; this tells you **why**, and where the settled
> ground ends and your judgment begins.
>
> Frame: two layers. **The harmony** — settled decisions you inherit as given; do not
> re-derive them. **The frontier** — the open questions where you actually think. Most of a
> good handoff is being clear about which is which.
>
> State anchor: main @ `1c4663d`. Shipped: oracle (#193), refscan (#179), linter (#192),
> ADR-88/89 doctrine (both **Proposed**). #197 closed. #199 filed.

---

## 1. Strategic intent (the way-of-working goal — not a task)

**Give the organ teeth, then ratify it.** Right now the organ has *legibility* without
*enforcement*: the oracle (A) and the scan (C) **surface** dependency edges, but nothing yet
**stops** the silent-overwrite failure they were built to prevent. The oracle answers "what
depends on this" — but no gate consumes that answer to refuse an unsafe removal. So the
methodology goal is **Track D (safe-removal gate)**: turn the advisory legibility into an
enforced gate, *safely* — which is the same act as resolving ADR-89 OQ3 (advisory→gate
promotion). Legibility was this session; **teeth** is next.

Second: **ratify the doctrine.** ADR-88 and ADR-89 are still Proposed. The organ is currently
an experiment with a clear shape, not a ratified foundation. Completing the methodology means
the doctrine that *defines* the organ reaches Accepted — which gates on resolving the ADRs'
open OQs.

The deeper intent: **preserve the pattern this session established** while completing the
organ — declare-what-you-can't-compute / compute-what-you-can; advisory-first; closure-level
(not per-symbol) gating; and **dogfood the organ on its own corpus.** The pattern is the
inheritance; the remaining tracks are its application.

## 2. Tensions weighed — where I landed and why

1. **Recall vs precision (the scan).** Human-confirm makes false-positives cheap but
   false-*negatives* expensive (a missed edge = the staleness bug) — yet humans fatigue on
   noise. → **Tiered surfacing:** Tier 1+2 actionable, Tier 3 *retained-and-enumerated*
   below the line. Optimizes both: strong candidates get attention, weak signals stay
   auditable + promotable, **no silent recall loss.** This is the general pattern for any
   human-in-the-loop discovery surface.

2. **Registry-only vs all-specs (the authority set).** → **Registry-only.** The registry is
   the *declared* authority set — consistent with the thesis. "All specs" needs a fuzzy
   heuristic = a competing *undeclared* definition of spec-hood = drift; and it is
   self-contradictory to build the undeclared-edge scanner on an undeclared authority set.
   Growth lever = register more specs (the governed action). **The organ's own inputs must be
   declared.**

3. **Pyright vendoring (the oracle).** Reproducibility/fidelity vs repo-footprint purity. →
   **Local npm, pinned + gitignored.** For an oracle, **determinism is load-bearing** —
   ADR-89 mandates provenance precisely for auditability. The npm-pinned path is the *exact*
   benchmark-proven invocation (zero re-proving) and proves closure now; the pip-wrapper's
   `>=` floor + opaque bundled toolchain + *unproven* invocation eroded the determinism that
   justifies the oracle. Footprint cost (a node manifest in a markdown repo) is **tooling, not
   content** — acceptable.

4. **Disposition (A) vs push-past (B) for the ship-gate RED.** → **Disposition, sha-scoped.**
   And note: **I reversed my own filed lean** (was "B+C, reject A"). Live evidence falsified
   the framing — the RED was *recurring* (carried across multiple ships), not a one-off, so
   push-past had already eroded the gate; and #197's own done-when ("gate no longer RED")
   *requires* A, which B can't satisfy. **Update leans when live evidence contradicts them.**
   A safety gate that is permanently overridden is worse than one made honestly green.

5. **Prose-gating vs declared depends-on edges (the backlog reconcile).** → **Prose+refs**
   (matched #180/#181 precedent) — it's a filing, not a design decision, and phased gating
   (2a→A, 2b→spike) doesn't map to one item-level edge. **But** I flagged the dogfooding
   tension (the dependency-legibility project encoding its *own* task-gating as undeclared
   prose) as an open question, not a filing change. Don't smuggle design into filings.

6. **Universal PLAYBOOK vs hub-specific organ** (CC corrected my framing here). → The organ
   is **hub-specific tooling**; PLAYBOOK is the **universal** methodology; hub-specific lives
   in ARCHITECTURE + the ADRs. Documenting the organ in PLAYBOOK would wrongly universalize
   it (matches #77's direction). **Internalize this boundary** — it will come up every time
   you're tempted to "document the new thing in the PLAYBOOK."

## 3. Considered + rejected — do NOT relitigate

- **Custom code graph / codemap** for code→code — rejected; the benchmark proved Pyright
  suffices. Don't rebuild it.
- **All-specs authority set** — rejected (fuzzy/self-contradictory).
- **All-tiers / Tier-1-only** surfacing — rejected (flood vs miss).
- **pip-wrapper / global Pyright** — rejected (reproducibility/fidelity).
- **Push-past-RED as the gate resolution; a blanket "direct-commits OK" waiver** — rejected
  (disposition was sha-scoped, narrow).
- **Documenting the organ in PLAYBOOK** — rejected (hub-specific ≠ universal).
- **Auto-declaring edges in the scan** — rejected; **the human confirms every candidate.**
  This is the load-bearing safety rule of the scan — never weaken it.
- **Parallelizing tiny follow-through tasks** — rejected (worktree overhead > benefit).
- **Reopening #197 for mechanical FF-prevention** — rejected; that's **#153's** scope.
- **Closing #5/#77** — never; they cite the #167-misattribution and are standing
  false-positives.

## 4. Open questions — unresolved or deliberately deferred

- **ADR-89 OQ1 — doc→code rule-ID granularity** (clause vs heading vs file). **Gates Track B
  (#194).** My lean: **clause-level** (impl = a callable or a file-constant). **UNCONFIRMED.**
  This is *the* decision that unblocks the declared-edge half — likely worth a Council debate
  or a deliberate architect call, not a snap pick.
- **ADR-89 OQ3 — advisory→gate promotion.** The meta-question for the *whole* organ: by what
  criteria does an advisory edge-check earn the right to *enforce*? This is **intertwined with
  Track D** — the removal-gate *is* an advisory→enforced promotion. Resolve OQ3 and build D
  together, not separately.
- **ADR-88 OQ1–OQ4 — all open** (incl. OQ2 = the #170 issue↔commit edge). ADR-88 ratification
  gates on these.
- **Closure computation (#196 spike; the brief's OQ1)** — how to compute a removal *closure*
  across heterogeneous artifact kinds (tests→symbols, config string-refs, cross-language).
  **The hardest unsolved piece.** Gates Track D-2b. Attack it early to de-risk D.
- **Scan precision scope** — the refscan walks **gitignored temp/scratch** (a real bug CC
  surfaced) plus immutable-zone noise (#199). Where's the precision boundary?
- **Dogfooding gap** — should the organ's *own* task-gating be declared edges (not the
  prose+refs I filed)? Deferred.
- **#153 priority** — the mechanical pre-push direct-commit/FF block (the recurrence-prevention
  #197 delegated). Cheap, high-leverage; I'd elevate it.
- **Deferred by scope:** dashboard (#171); CLAUDE §11 stale-ADR groom.

## 5. Decomposition rationale — what NOT to redo vs what to decide fresh

**Why this shape.** The tracks are not arbitrary — they are the *distinct edge populations*.
The architect consolidation found that the original brief (code-coupled edges) and the 06-19
supplement (prose-internal + structure) cover **complementary, near-non-overlapping** edge
populations; **the organ = their union.** Each population needs its own mechanism:
- **A (code→code) computed** — Pyright. Shipped first: it's the keystone (settles ADR-89 OQ2,
  and Track D-2a depends on its oracle).
- **C (prose) shipped in parallel** — independent of A (different file surfaces).
- **B (doc→code) declared** — gated on the rule-ID granularity decision (OQ1) *because the
  ID-scheme shapes the entire mechanism; building before deciding = rework.*
- **D (removal-gate) phased** — 2a (process-gate, uses A's oracle, doable now) vs 2b
  (closure-gate, gated on the #196 spike) *because the closure computation is the hard unsolved
  piece — split the doable-now from the research-gated.*

**Do NOT re-decide (the harmony):** the track decomposition; the declare-vs-compute assignment;
Track A's oracle design (Pyright + provenance v1, OQ2 resolved); Track C's scan/linter; the
Fork-1/Fork-2 calls; the disposition; the A-first / B-gated / D-phased sequencing.

**DECIDE fresh (the frontier):** OQ1 (→ unblocks B); OQ3 (→ shapes D's enforcement); the #196
closure-computation design (→ unblocks D-2b).

## 6. Off-repo context

- **The disposition lean-reversal** (Q2.4) — the repo shows the final disposition; it does
  *not* show that the backlog item's recorded lean was "B+C, reject A." If you see that and
  wonder: it was correctly *superseded* at the decision point by live evidence. Don't reopen.
- **OQ-numbering hygiene** — the dependency-legibility *brief* numbered its OQs in a namespace
  that collided with ADR-89's. CC fixed the in-repo references; the standing lesson: **read the
  ADR's actual OQ numbers; never trust a brief's labels.**
- **Priorities (my read):** (1) **Track D-2a** is the highest-ready build — oracle shipped,
  gives the organ teeth. (2) **OQ1** is the highest-leverage *decision* — unblocks B. (3) the
  **#196 closure-spike** is the hardest — start it early to de-risk D-2b. (4) **#153** is cheap
  recurrence-prevention worth elevating.
- The **universal/hub-specific boundary** (Q2.6) — carry it; it's not written as a rule
  anywhere portable.

---

## Handoff-process meta — what worked, what didn't, what was missing

- **Worked:** the v5.2 bundle pattern — PASTE_THIS + **PROBES that bind live** (10/10) +
  RESIDUAL §3 plan / §4 open-decisions. The PROBES are the strength: they force the next
  session to *verify state*, not trust the summary. Keep that.
- **The gap:** the machinery captures **verifiable state** well and **design intent** not at
  all. The *why* — trade-offs weighed, options rejected, strategic intent, lean-evolutions —
  is not derivable from the repo; it lives in the outgoing architect's head and **must be
  written by hand.** This document is that missing layer. **Methodology improvement: the
  handoff bundle should carry a design-intent section (these 6 questions) as a first-class
  artifact, filled by the architect — not just the CC-generated state-bundle.** Without it, a
  successor re-derives settled trade-offs or, worse, relitigates rejected options.
- **Also weak:** the bundle records final state, not **decision evolution** (e.g. the B+C→A
  flip). A successor seeing a backlog lean that contradicts the shipped decision has no way to
  know it was a *reasoned supersession*. The intent layer must carry evolutions.

## The `claude -w` worktree lessons (→ #198; candidate for the lessons skill)

These recurred enough to be real, not anecdotal:
- `claude -w <name>` is the **one-verb** primitive (don't hand-roll `git worktree add`). It
  creates the worktree **and** a placeholder branch `worktree-<name>`. **Cleanup must delete
  both** (the work branch *and* the placeholder).
- **Parallel worktrees always collide on the 2nd `--no-ff` merge** on (a) `JOURNAL.md` — each
  journals → **keep both entries, newest-first**; and (b) any **shared additive claim** — both
  bumped `pytest_collected` to *different local values*, neither equal to the merged total →
  **reconcile to the live combined number, never assume.**
- The two CC instances named their work branches **inconsistently** (one committed onto the
  placeholder, one made a `feat/` branch). **#198 should codify the convention.**

These belong in **#198 (claude -w lifecycle)**, already filed. Whether to also write them to the
lessons/gotchas skill is a next-session call — not urgent; #198 is the owner.

## What remains to complete the methodology (your read was right — and here's the full set)

You saw it on the diagram: **Track B and Track D** remain. Confirmed — and the complete set is:

**Build (the unshipped edge organs):**
- **Track B (#194)** — doc→code declared edge. *Decision-gated* on OQ1 (rule-ID granularity).
- **Track D (#195)** — safe-removal gate. **2a is ready now** (oracle shipped); **2b is gated**
  on the #196 closure-spike.
- **#196 closure-spike** — the hard cross-artifact closure computation that D-2b needs.

**Doctrine (still Proposed — the organ isn't yet a ratified foundation):**
- **ADR-88 ratification** — OQ1–OQ4 all open.
- **ADR-89 ratification** — OQ1 (rule-ID granularity) + OQ3 (advisory→gate) open.

**Enforcement (the teeth):**
- **ADR-89 OQ3 — advisory→gate promotion.** The organ is advisory-first; making it *enforce*
  is the point of Track D. This + Track D are one problem.

**Hardening:** #153 (mechanical FF-block) · #199 + the gitignored-walk scan-precision gap.

**Deferred:** dashboard (#171) · CLAUDE §11 groom.

So: **the organ is half-built (A + C shipped; B + D + the spike remain) and the doctrine is
unratified.** "Complete" = build B + D + spike, give the organ teeth (resolve advisory→gate),
ratify ADR-88/89. That is the road. The map is in RESIDUAL §3; the *why* is here.

---

*Inherit the harmony. Think only at the frontier. The pattern holds — apply it.*
