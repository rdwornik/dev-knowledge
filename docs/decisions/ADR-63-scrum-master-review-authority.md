# ADR-63: Scrum-Master Review Authority Codification

<!-- scope: meta -->

- **Status:** Accepted
- **Date:** 2026-05-30
- **Related:** ADR-36 (audit tool — the read-only review mechanism), ADR-62 (v4 ratification — companion ADR; this codification is the lesson the v4 saga produced), `protocols/AGENT_FRAMEWORK.md` (v0.1 stub — the automated-enforcement extension), `protocols/PLAYBOOK.md`
- **Decommission:** none (additive — formalizes an already-practiced review relationship)
- **Source:** Operator decision (Rob, 2026-05-30) — **Path A** (direct ADR, no AI Council convene). Grounds: the pattern has clear empirical grounding pointing to one option; Council without insider context cannot add value. No Council transcript.

## Context

Two empirically-grounded review relationships have operated across the ecosystem,
both instances of the same structure — **a methodology-guardian holds standing,
asymmetric review authority over an execution layer**. This ADR codifies that
structure so it survives contributor change, session-context drift, and future
architect-LLM training updates, rather than living as ad-hoc habit.

**Facet 1 — institutional cross-repo review (the original BACKLOG P1 grounding).**
`.dev-knowledge` (the ecosystem strażnik / methodology guardian) produces a
structured, **read-only** review report identifying governance, documentation,
dead-code, and filename-compliance issues in a child repo; the operator routes the
report; the child-repo architect implements. Empirical grounding **N=3**: ai-council
(2026-05-12), corp-monorepo deep audit (2026-05-23), ai-council deep-audit re-pass
(2026-05-23). This is the facet BACKLOG P1 "Codify scrum-master review authority
pattern" was opened to capture.

**Facet 2 — intra-session operator→architect review (surfaced by the marathon arc).**
**5 total catches in 24h (May 29-30):** 3 operator catches at prompt emission
(`docs/strategic/`, `docs/handoffs/_scratch/`, two-cluster Phase 1 interview design) +
2 CC catches at execution (BACKLOG header convention drift, JOURNAL format drift during
v4.3.1 patch). Captured in LESSONS (2026-05-30) + JOURNAL:

- `docs/strategic/` folder creation — operator caught at prompt emission, redirected.
- `docs/handoffs/_scratch/` folder — operator caught, reverted to the existing
  `in-progress/` convention.
- A two-cluster Phase-1 interview design — operator caught at design level, collapsed
  to a single sage-frame cluster.
- BACKLOG header convention drift in the v4.3.1 patch prompt — caught by CC at
  execution time (not the operator) — meta-pattern recursion.
- JOURNAL format convention drift in the same prompt — caught by CC at execution time.

The 2026-05-29 ecosystem-coherence audit named the underlying condition **ML-2:
un-enforced guards** — the prompt-author convention is documented but not gated, so it
drifts under load.

Both facets share one shape: **the guardian reviews the executor's output; authority
is asymmetric (the executor does not review the guardian).** Without ADR-level
codification the pattern reads as ad-hoc and may not survive a contributor or
session-context change.

The operator's verbal articulation (2026-05-29 late session) — *"musimy zbudować agent
framework, który pewne rzeczy, żebym nie musiał po prostu powtarzać"* — is anchored as
`protocols/AGENT_FRAMEWORK.md` v0.1 stub; this ADR codifies the **human-operator side**
of that signal (the review relationship), while the agent framework is the future
**automated** side.

## Decision

Codify the scrum-master review authority pattern as an **architectural pattern for
`.dev-knowledge`**: the methodology guardian holds standing, asymmetric review
authority over the execution layer. The pattern manifests at two altitudes (Facet 1
and Facet 2 above) under one role-relationship.

For the **session-altitude facet (operator→architect)**, adopt **Option E (Hybrid
B+C): trigger-based review + per-artifact-class review.**

**Trigger-based review** — operator visual review fires when the architect proposes:

- a new folder name not yet established in repo conventions;
- a new naming convention or pattern (file names, branch names, commit prefixes, …);
- a new structural pattern (file types, folder hierarchies, organizational schemes);
- an architectural change at ADR-level scope (new process, constraint, or convention
  rule);
- a modification to an existing convention.

**Per-artifact-class review** — operator visual review fires as a standing pre-emit
gate on:

- all CC prompts authored by the architect (reviewed before passing to CC);
- all ADRs and amendments (reviewed before commit);
- all spec changes (`protocols/*.md` body edits — reviewed before commit).

**NOT reviewed pre-emit** (would be over-burden): routine conversational responses;
per-commit messages within established conventions; existing-pattern-following work.

For the **ecosystem-altitude facet (`.dev-knowledge` → child repo)**, the existing
mechanism stands: a structured read-only review report (the ADR-36 audit-tool /
strażnik review), routed by the operator, implemented by the child-repo architect.

**Facet 1 (cross-repo strażnik review) inherits ADR-36's mechanism unchanged — no new
machinery is added here.** ADR-63 codifies the *shared authority-asymmetry abstraction*
across both facets; the operational triggers and per-artifact-class apparatus (5 triggers
+ 3 artifact classes + 3 exclusions) apply to **Facet 2 (operator→architect review)**
specifically. A reader should not assume Facet 1 gets equal operationalization; the facets
share spine, not implementation.

### Asymmetry

- **Guardian → executor:** standing review authority. The guardian catches
  anti-patterns; the executor adjusts.
- **Executor → guardian:** no review authority. The guardian's calls are authoritative;
  the executor proposes, the guardian decides.
- **Operator → architect (Facet 2):** the operator is the guardian, the architect-LLM
  is the executor of methodology design.
- **Architect → CC:** the same shape one layer down — the architect designs prompts, CC
  executes; the architect's prompt outputs are gated by the operator (per-artifact-class)
  before CC execution.
- **`.dev-knowledge` → child repo (Facet 1):** the guardian repo reviews child-repo
  state; the child-repo architect implements.

This mirrors the agile **scrum-master / scrum-member** relationship: the scrum-master
holds process authority, members hold execution authority.

## Alternatives considered

1. **Option A (always-on review).** Rejected: defeats the architect's independent
   thinking, over-burdens operator energy, and would prevent the meta-design work the
   architect is positioned to do.

2. **Option B (trigger-based only).** Rejected: misses conversational-mode drift in
   routine CC prompts. The v4.3.1 BACKLOG/JOURNAL convention drifts were not fired by
   any named trigger — they were format-level prompt drift caught at execution time.

3. **Option C (per-artifact-class only).** Rejected: ignores triggers for non-routine
   architectural moves (e.g., a new folder name proposed mid-conversation that never
   reaches a per-artifact-class artifact would go uncaught).

4. **Option D (don't codify).** Rejected: the empirical grounding (Facet 1 N=3 + Facet
   2: 5 catches in 24h) is unprecedented in repo history; the pattern would not survive a
   contributor change, architect-LLM training update, or session-context drift without
   codification.

## Empirical grounding

- **Facet 1 — N=3 cross-repo strażnik reviews:** ai-council (2026-05-12), corp-monorepo
  deep audit (2026-05-23), ai-council deep-audit re-pass (2026-05-23). Three structured
  read-only reviews across two repos = sufficient pattern for ADR-level codification
  (BACKLOG P1, `docs/audits/2026-05-24-backlog-audit-and-universalization-scoping.md`
  §7).
- **Facet 2 — 5 total catches in 24h (May 29-30):** `docs/strategic/`, `docs/handoffs/_scratch/`,
  and the two-cluster interview design (LESSONS 2026-05-30 "New-folder/structural-pattern
  without checking existing convention"; JOURNAL 2026-05-29 "third unilateral
  folder/structure decision … in ~24h").
- **2+ prompt-level convention drifts** caught by CC at execution time (v4.3.1 BACKLOG
  `## P1` headers + freeform JOURNAL block; LESSONS 2026-05-30 "prompt-level convention
  drift" + "meta-pattern recursion").
- **All instances caught successfully** — operator catches prevented downstream
  commit/merge of bad patterns; CC catches prevented v4.3.1 from shipping convention
  drift.
- **ML-2 (un-enforced guards)** — the 2026-05-29 ecosystem-coherence audit names the
  structural reason the pattern needs codification: the convention is documented but not
  gated.

## Consequences

- **The architect explicitly invokes scrum-master review when a trigger fires** ("this
  introduces a new convention — operator approval required before proceeding"). A
  verbal/written checkpoint, not automation.
- **Operator visual review on all CC prompts** before the architect ships them:
  architect generates → presents → operator approves/redirects → architect ships to CC.
- **Operator visual review on all ADRs, amendments, and spec changes** before commit:
  architect drafts → presents → operator approves → CC commits.
- **The asymmetric authority structure is formalized.** Future architect-LLM sessions
  (different chat, possibly different model) inherit the relationship via this ADR +
  PLAYBOOK + LESSONS, not via in-context memory — so it survives session-context drift.
- **Operator energy cost is bounded and accepted.** The trigger + per-artifact-class
  scoping keeps it from firing on every micro-decision; the empirical value (5+
  successful catches in 24h preventing architectural drift) justifies the cost.
- **Future evolution:** the agent-framework full implementation (BACKLOG P1,
  `protocols/AGENT_FRAMEWORK.md`) may automate parts of Facet 2 — e.g., a pre-flight
  new-folder anti-pattern check before CC prompt emission. It would augment, not replace,
  operator review. This is the same enforcement-layer move ML-2 calls for (gate the
  documented guard).
- **BACKLOG P1 "Codify scrum-master review authority pattern" is closed by this ADR.**
  Note the scope reconciliation: P1 was opened on Facet 1 (cross-repo strażnik review,
  N=3); this ADR codifies the **unified** authority structure covering both that facet
  and the operator→architect facet the marathon arc surfaced. The Facet-1 grounding is
  preserved, not displaced.

## References

- `LESSONS.md` — 2026-05-30 batch: "New-folder/structural-pattern without checking
  existing convention" (Facet 2 N+3); "prompt-level convention drift applies to
  prompt-authoring"; "multi-step intermediate-state verification"; "honest no-op over
  fabricated commit"; "meta-level curse-of-knowledge recursion"
- `protocols/PLAYBOOK.md` (this ADR may motivate a future methodology-section addition)
- `protocols/AGENT_FRAMEWORK.md` v0.1 stub (the automated-enforcement extension)
- ADR-36 (audit tool architecture — the read-only review mechanism for Facet 1)
- ADR-62 (v4 ratification — companion ADR; this codification is the lesson the v4 saga
  produced)
- `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (the architect-level finding
  cluster that catalyzed the pattern recognition)
- `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (finding ML-2 — un-enforced
  guards)
- `docs/audits/2026-05-24-backlog-audit-and-universalization-scoping.md` §7 (Facet 1
  N=3 grounding; P1 promotion)
- `JOURNAL.md` — 2026-05-29 / 2026-05-30 entries (specific instance captures)
- BACKLOG Stream-C P1 "Codify scrum-master review authority pattern" (closed by this
  ADR)
