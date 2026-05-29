# Harness Engineering — Strategic Positioning + 90-Day Roadmap (2026-05-29)

<!-- scope: meta -->

> Strategic companion to the operational morning briefing. The briefing answers
> "what do I merge today." This answers "where does this harness sit in 2026
> industry maturity, and what should the next quarter build." Read in ~15 min.
>
> **Grounding:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (this
> session's 22 findings), `docs/audits/2026-05-29-overnight-morning-briefing.md`,
> `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (the 13 bugs that opened
> this track). Industry sources cited by author + date (see §9 on epistemics).

---

## §1 — Executive summary

- **Direction verdict:** the `.dev-knowledge` ecosystem is a **genuine Phase-3
  harness** (engineered guards, not just prompts/context) that is **strong on
  governance and cross-session continuity but weak on measurement** — it cannot yet
  see itself.
- **Top-3 strengths vs industry:** (1) ADR-39 immutability + amendment discipline;
  (2) the scrum-master independent-review pattern (an agent-on-the-loop guard most
  teams don't have); (3) a solved cross-session handoff contract (v3.4: claims +
  scope + applied-task probe + structured ratification).
- **Top-3 gaps vs industry:** (1) **no agent eval suite** — the v3.4 first run was
  ad-hoc and aborted; (2) **no observability** — JOURNAL is narrative, zero
  telemetry (tokens/actions/time); (3) **the meta-harness has no harness** — LESSON
  #9's guard was supposed to catch exactly the v3.4 multi-surface bug and didn't
  (ecosystem-audit finding ML-2).
- **Phase-3 maturity:** **early Phase 3.** The Information and Execution layers are
  mature; the Feedback layer *captures* but does not *enforce or measure*. The
  flywheel exists manually (this very session) but is not instrumented.

---

## §2 — The 2026 harness engineering framework (background)

A compressed rendering of the doctrine this positioning is measured against. (See
§9 — several sources are at/after my knowledge cutoff and are relayed as framed by
the task brief, not independently re-verified.)

**Phase 1 → 2 → 3 progression.** Prompt engineering (craft the instruction) →
context engineering (curate what the model sees) → **harness engineering** (build
the surrounding system of guards, tools, feedback, and evaluation that lets an agent
operate reliably). Phase 3 is the 2026 frontier: the unit of work is no longer the
prompt, it is the harness.

**Hashimoto principle (per Faros, 2026):** *every mistake becomes an engineered
guard.* A failure is not just fixed; it is converted into a mechanism that prevents
recurrence. This is the load-bearing idea for the rest of this document.

**Three-layer model (per Mysore, 2026):**
- **Information layer** — what the agent knows (docs, memory, conventions, state).
- **Execution layer** — what the agent can do and what constrains it (tools,
  validators, hooks, invariants).
- **Feedback layer** — how the system learns (evals, telemetry, lessons, review).

**Inner vs Outer Harness (per Masood, 2026):** the *inner* harness is what the
agent carries into a single run (system prompt, tools, in-run context); the *outer*
harness is the system around runs (eval suites, CI, observability, human review,
the loop that improves the inner harness). "Agent legibility" — the system being
able to see and explain what the agent did — is an outer-harness property.

**Humans-on-the-loop vs in-the-loop (per Fowler, 2026):** *in-the-loop* gates every
action on a human; *on-the-loop* lets the agent run and the human supervises,
intervening by exception. The **Agentic Flywheel** (Fowler) is the step beyond:
the agent itself proposes harness improvements, which humans ratify — the harness
improving the harness.

**2026 fault taxonomy (March 2026):** the recurring agentic failure classes —
*initialization failures* (bad/incomplete setup), *role deviation* (agent drifts
from its assigned role), *memory/state deficiencies* (loses or fabricates state),
*orchestration failures* (multi-step/multi-agent coordination breaks), *tool
integration errors* (wrong/failed tool use). Mature harnesses are designed to
detect each class.

---

## §3 — Mapping `.dev-knowledge` to the three-layer model

Components are actual files/ADRs surfaced by this session's audit. Maturity:
**strong** / developed / partial / **missing**.

### Information layer

| Component | Role | Maturity |
|---|---|---|
| VISION / PLAYBOOK / ESSENTIALS | norms, methodology, cheat-sheet | strong |
| CLAUDE.md (per-repo) | session contract / agent instructions | developed — but self-describes inaccurately (SK-1/SK-2/CD-1/CD-2) |
| ADRs + amendments | immutable decision record | strong (ADR-39) |
| LESSONS.md (144 entries) | generalized learnings | developed — capture healthy; ordering descriptor wrong (ML-1) |
| JOURNAL.md | tactical per-session log | strong (narrative) |
| BACKLOG.md | prioritized work queue | strong |
| `~/.claude/` runtime (gotchas, skills, memory, commands) | operator-level inner-harness config | partial — inventory drift (SK-2), vacuous evolution logs (SK-3) |
| ARCHITECTURE.md (+ codemap) | structural model + diagrams | developed — governing-ADR list stale (WF-1), validators list wrong (WF-2) |

### Execution layer

| Component | Role | Maturity |
|---|---|---|
| `scripts/audit.py` (7 checks) | self-conformance validator | strong; no handoff validator (by design) |
| pre-commit hooks (per repo) | mechanical gate | partial — ruff documented-but-absent here (HK-1); coverage uneven across repos (HK-4) |
| codemap freshness check | ARCHITECTURE drift gate | strong |
| ADR-39 immutability | append-not-edit discipline | strong |
| Handoff v3.4 | cross-session transfer | strong (post-fix) — retry-ready |
| AI Council pipeline (v1.0) | multi-agent decision process | developed |
| Layer-2 invariant (ADR-28/36) | validators-not-orchestration | strong |
| ADR-41 cross-repo ownership | repo-boundary discipline | strong (held this session) |
| Scrum-master review pattern | independent pre-execution review | developed — works, not yet codified (open P1) |
| `block-onedrive.ps1` PreToolUse hook | safety guard | strong |

### Feedback layer

| Component | Role | Maturity |
|---|---|---|
| LESSONS append | learning capture | developed — capture good, **enforcement weak** (ML-2) |
| ADR amendments | decision evolution | strong |
| JOURNAL/BACKLOG cycle | work-state feedback | strong |
| Audit reports (this session ×3) | periodic deep review | strong |
| gotcha `verify:` lines | re-checkable guards | developed (code-repo scoped) |
| Evolution logs (`.jsonl`) | trend/correction telemetry | **missing** — referenced everywhere, exist nowhere (SK-3/HK-2) |
| SessionStop automation | session-close feedback | **missing** (HK-3) |
| Eval suite | output validation | **missing** (see §5) |
| Observability metrics | run telemetry | **missing** (see §5) |

**Read of the table:** Information + Execution are mature; Feedback *records* well
but *measures and enforces* poorly. That asymmetry is the strategic story.

---

## §4 — Where the ecosystem EXCEEDS typical 2026 practice

| Area | Industry baseline | This ecosystem's superset | Evidence |
|---|---|---|---|
| Decision durability | amend-in-place changelogs; history is mutable | **ADR-39 immutability** — bodies frozen, corrections are appended amendments with supersede markers | this session corrected 6 ADRs by amendment-only (fix campaign), zero body edits |
| Pre-execution review | humans-on-the-loop (human spot-checks output) | **scrum-master review pattern** — an independent reviewer (often another agent) challenges a *plausible* output before execution; an agent-on-the-loop guard | the v3.4 abort itself: review caught a chat-mode narrative that only file:line ground-truth exposed (process audit §7) |
| Multi-agent decision | single agent or naive voting | **AI Council** — blind multi-model debate + explicit synthesis + ADR capture (AI_COUNCIL_PROCESS v1.0) | ADR-55/56/57/58 each trace to a Council Q-debate |
| Cross-session continuity | mostly unsolved; context lost at session end | **handoff v3.4** — invariant floor + scoped operational layer + structured claims + applied-task gate + structured ratification | HANDOFF_PROCESS v3.4; retry-ready per fix-campaign verification |
| Self-governance boundary | agents orchestrate freely | **Layer-2 invariant** — the governance repo may *validate* but never *orchestrate* (ADR-28/36) | audit.py is read-only; no script drives child-repo state |
| Flywheel grounding | aspirational | the pattern is **empirically grounded N=12+** — this session is itself another instance (independent review → audit → guard) | ecosystem-audit ML-2/ML-3 + scrum-master P1 |

**Honest caveat:** "exceeds" is measured against *typical* practice. Frontier labs
and mature platform teams have eval suites and observability this ecosystem lacks
(§5). The superset is in **governance discipline and cross-session design**, not in
measurement.

---

## §5 — Where the ecosystem LACKS vs industry standard

| # | Gap | Industry standard (ref) | This ecosystem's absence | Risk | First step |
|---|---|---|---|---|---|
| 1 | **No agent eval suite** | deterministic eval scenarios run through the agent, scored against expected outputs (QubitTool eval-harness patterns, 2026; Masood outer-harness) | the v3.4 first real run *was* the test — ad-hoc, and it aborted | **high** — no repeatable way to know a harness change works before shipping | minimal eval: 2-3 canned handoff scenarios with expected Stage-1 outputs |
| 2 | **No observability metrics** | token spend, action count, time-per-phase, success/abort rates (Inner/Outer harness "agent legibility", Masood) | JOURNAL is narrative prose; no telemetry store | **high** — can't measure improvement, cost, or regression trend | auto-capture per-session tokens/actions/time (SessionStop hook) |
| 3 | **No formal max-iterations / max-steps counters** | systematic loop/step budgets to bound runaway agents (fault taxonomy: orchestration failures) | hard-stops live in prompt prose, ad-hoc per task | medium | a documented step-budget convention + a Stop-hook tripwire |
| 4 | **No tool mocking / resilience tests** | mock tool failures to test agent recovery (fault taxonomy: tool integration errors) | none | medium | not urgent for a docs-governance repo; higher value in corp-monorepo |
| 5 | **Single-operator system** | reproducibility across operators/CI (Anthropic Feb 2026 autonomy study on supervised autonomy) | one operator (Rob); CI/headless reproducibility untested | medium | run `/boot` + audit.py in a headless CI context once |
| 6 | **The meta-harness has no harness** | the harness that builds harnesses is itself guarded (Hashimoto: every mistake → guard) | **LESSON #9** (universal-without-cross-case-verification, 2026-05-14) produced a guard that was *advisory prose, not a gate* — and v3.4's multi-surface amendment skipped it, reproducing the exact failure | **high** — the system's central principle (mistakes become guards) failed at its own meta-level | convert the cross-case-trace guard into an enforced amendment checklist (ML-2) |

**Gap #6 is the headline.** It is a Hashimoto-principle violation at the meta-level:
the ecosystem wrote the lesson, wrote the guard, and then did not wire the guard, so
the lesson recurred. Every other gap is "not built yet"; this one is "built as text,
not as mechanism" — a more instructive failure.

---

## §6 — Phase 1-7 audit findings in harness-engineering terms

Synthesis of this session's 22 findings (`docs/audits/2026-05-29-ecosystem-coherence-audit.md`
§3) mapped to the three layers.

- **Skills audit (SK-1..SK-5) → Information layer maturity.** The inner-harness
  inventory (skills/commands) has drifted from its self-description in CLAUDE.md, and
  the evolution memory store (`.jsonl` logs) referenced by boot.md doesn't exist
  (SK-3). The Information layer is *rich but mis-indexed* — the map disagrees with the
  territory.
- **Hooks audit (HK-1..HK-4) → Execution + Feedback layers.** ruff is
  documented-as-enforced but absent (HK-1) — an Execution-layer guard that exists on
  paper only. Lifecycle hooks (SessionStart/Stop) fire but read empty logs (HK-2) and
  do no functional close-out work (HK-3) — the Feedback layer's instrumentation is
  wired to nothing.
- **Workflows audit (WF-1..WF-3) → Execution layer.** ARCHITECTURE omits two binding
  ADRs (one of which grounds three audit.py checks) and lists a validator that
  doesn't exist (WF-2) — the Execution-layer documentation under-describes its own
  guards and over-claims others.
- **Goals audit (GO-1/GO-2) → cross-layer coherence.** Goals are sound and all P1s
  trace to VISION; the only gap is a *named-but-unmeasured* health signal (GO-1) —
  itself a micro-instance of the §5 observability gap.
- **corp-monorepo coherence (CM-1/CM-2) → cross-repo Information integrity.** ADR-41
  held — zero cross-repo writes; the boundary works. A security-finding extraction
  sits on an unmerged branch (CM-1), and the child still uses the pre-ADR-42 flat
  handoff (CM-2). The cross-repo Information layer is *consistent but lagging*.
- **Cross-doc harmony (CD-1/CD-2) → Information-layer drift detection.** The same
  v3.3.3-straggler class that caused the v3.4 abort persists in CLAUDE.md §7 (CD-1) —
  proof the straggler sweep itself needs a wider net. Drift detection exists
  (audit.py) but doesn't cover version-string consistency across narrative docs.
- **Memory/feedback/lessons (ML-1..ML-4) → Feedback-layer loop integrity.** This is
  where the audit bites hardest: the lesson→guard→enforcement chain breaks at
  enforcement (ML-2), the latest failure isn't yet a lesson (ML-3), and two canonical
  feedback artifacts are mis-described (ML-1) or absent (ML-4, TOKEN-LOG.md). The
  Feedback layer is the least mature of the three.

**Cross-cutting pattern:** 12 of 22 findings are *documentation-truth drift* — the
governance docs describe a harness slightly different from the one that exists. For a
repo whose VISION is "drift detected proactively," the drift is in the drift-detector.

---

## §7 — 90-day roadmap

Sequenced. Each item: **layer** (I/E/F) · effort (model + scope) · sessions ·
dependencies · success criterion. Priorities reflect the audit's actual severities
(no critical/high surfaced; gap #6 / ML-2 is the de-facto top).

### Month 1 — close immediate gaps

1. **Handoff v3.4 retry** · F · Opus, medium · 1 · dep: fix-campaign branch merged ·
   *success:* a full v3.4 handoff completes Stage 1→3 with claims+scope+probe present
   and structured ratification passing.
2. **Doc-truth sweep** · I · Sonnet, medium · 1 · dep: none · *success:* SK-1/SK-2/
   CD-1/CD-2/WF-1/WF-2/ML-1/ML-4 closed; CLAUDE.md + ARCHITECTURE match disk; ML-1
   verified against ADR-29.
3. **Feedback-loop enforcement (gap #6 / ML-2)** · F · Opus, medium · 1 · dep: none ·
   *success:* the cross-case-trace guard is an enforced amendment checklist (not
   prose); the v3.4 abort is promoted to a LESSON (ML-3); ties into the scrum-master
   codification P1.
4. **SessionStart/Stop hook + evolution logs (SK-3/HK-2/HK-3)** · F · Sonnet/Opus,
   medium · 1 · dep: none · *success:* lifecycle hooks read/write a real store; one
   read-only session-close check (clean-tree + audit.py health) runs at Stop.

### Month 2 — Phase-3 maturity steps

5. **Minimal agent eval suite (gap #1)** · F · Council-first, then Opus · 2 · dep:
   Council decision (§8) · *success:* 2-3 canned handoff/audit scenarios run through CC
   with expected outputs; a harness change can be validated before shipping.
6. **Observability instrumentation (gap #2)** · F · Sonnet/Opus, medium · 1-2 · dep:
   #4 (Stop hook is the capture point) · *success:* per-session tokens/actions/time
   auto-recorded; a trend is queryable.
7. **Cross-stage consistency check (audit.py expansion)** · E · Opus, medium · 1 ·
   dep: none · *success:* audit.py (or a sibling read-only check) flags multi-surface
   version/inventory drift of the v3.4 kind before it ships — the mechanical form of
   gap #6's guard.

### Month 3 — meta-harness hardening

8. **v3.5 handoff direction** · F · Council-first · 2 · dep: §8 decision · *success:*
   a decided direction (shrink contract surfaces vs add validator code) with an ADR.
9. **Agentic flywheel (gap toward Fowler)** · F · Opus · 1 · dep: #4, #6 · *success:*
   an end-of-session CC self-reflection on harness gaps observed, ratified by operator
   — the harness proposing its own improvements.
10. **Scale check** · E/F · Sonnet, low · 1 · dep: none · *success:* re-run the
    durability + ecosystem audit patterns against the next 5 ADRs to confirm the
    governance model scales.

**Re-prioritization note:** the audit surfaced **no critical/high** finding, so no
roadmap item is promoted ahead of the retry + enforcement work. If the v3.4 retry
(#1) itself surfaces a new failure, that becomes the new #1 (Hashimoto: turn it into a
guard immediately).

---

## §8 — Open questions for AI Council debate

Framed as briefs, not as decisions for any single actor (operator standing
preference: architecture decisions go to Council). Each has genuine multi-framing
uncertainty.

1. **Eval suite substrate.** Should the agent eval suite be a *pytest-style runner*
   in-repo (reuses existing test infra, Layer-2-friendly), a *separate harness binary*
   (cleaner separation, more to maintain), or a *third-party* tool (Promptfoo /
   LangSmith — capability vs external dependency + the "no new deps without
   confirmation" rule)? Trade-off axis: Layer-2 invariant vs capability.
2. **Observability store.** Per-session *JOURNAL prepend* (human-readable, no new
   infra), a *separate telemetry store* (queryable trends, new artifact), or *both*
   (narrative + structured)? Trade-off: ADHD-friendly narrative vs machine-queryable
   metrics.
3. **v3.5 handoff direction.** *Shrink* the contract surfaces (claims/probe/scope add
   real load — is the bundle too heavy, per ADR-57's own "may remain heavy" risk?) or
   *add validator code* (the ADR-42 Q5 deferred mechanical gate)? Trade-off: simplicity
   vs enforcement. (This is the direct successor question to the whole v3.4 arc.)
4. **Flywheel trigger.** Should agent self-reflection on harness gaps be *opt-in
   per-session* (low friction, easily skipped) or a *mandatory SessionStop hook*
   (systematic, but Layer-2 must stay read-only/advisory)? Trade-off: consistency vs
   the no-orchestration invariant.
5. **Enforcement philosophy (the meta-question).** Gap #6 shows guards-as-prose fail.
   But mechanical enforcement everywhere risks brittleness + the very over-engineering
   the Layer-2 invariant resists. *Where is the line between an enforced gate and a
   documented convention?* This is the deepest question the audit raises and the one
   most worth a Council debate.

---

## §9 — Honest meta-observation (epistemics of this document)

This section is part of the deliverable, not a disclaimer.

- **This document is an LLM synthesis and should be verified, not trusted.** Its
  claims about repo state are grounded in artifacts I produced earlier this same
  session — which means a single session's blind spots could propagate into both the
  audit *and* this synthesis. The §8 Council route exists precisely so the decisions
  here are not made by the agent that wrote them.
- **Industry sources are partly relayed, not independently verified.** My knowledge
  cutoff is January 2026. Several cited sources — the "March 2026 fault taxonomy," the
  "Anthropic Feb 2026 autonomy study," and "Faros Phase 3 doctrine (2026)" — are at or
  after that cutoff. I have rendered the framework **as the task brief framed it** and
  as consistent with pre-cutoff direction-of-travel; I have **not** independently
  confirmed these specific 2026-dated publications. Treat author+date citations as
  pointers to verify, not as established fact.
- **Numeric/industry claims are point-in-time.** Any specific figure (e.g. the often-
  cited "~80% of agentic-AI implementation time is data engineering," attributed to
  McKinsey) should be treated as a point-in-time claim and re-checked before it is
  load-bearing in a decision.
- **The document does not validate itself.** There is no eval that ran this analysis
  against ground truth — which is itself an instance of gap #1. The honest position:
  this is a *hypothesis about where the harness stands*, to be tested by (a) operator
  review, (b) the Council debates in §8, and (c) the eval suite once it exists.
- **Strongest claim I'd stand behind:** the asymmetry is real — Information and
  Execution layers are mature, the Feedback layer measures poorly, and gap #6 (a
  guard that was prose, not a gate) is a literal, evidenced Hashimoto-principle
  violation. That conclusion is grounded in this session's own artifacts and the
  v3.4 abort, not in any post-cutoff source.
